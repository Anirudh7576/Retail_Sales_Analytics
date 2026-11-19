
import argparse
import csv
import json
import math
import random

from collections import defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from scripts.common.transaction_config import (
    RANDOM_SEED,
    CURRENCY_CODE,
    INVOICE_ID_PREFIX,
    SALES_ID_PREFIX,
    INVOICE_STATUSES,
    TRANSACTION_END_DATE,
    TRANSACTION_OUTPUT_DIR,
    TAX_CONFIG_FILE,
)

from scripts.validation.master_validation_config import (
    MASTER_DATA_DIR,
    MASTER_FILES,
)


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_ORDERS_FILE = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "orders"
    / "orders_20261118_121559_771171.csv"
)

DEFAULT_ORDER_ITEMS_FILE = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "order_items"
    / "order_items_20261119_104252_195977.csv"
)

PRODUCTS_FILE = (
    PROJECT_ROOT
    / MASTER_DATA_DIR
    / MASTER_FILES["products"]
)

TAX_FILE = PROJECT_ROOT / TAX_CONFIG_FILE

INVOICES_OUTPUT_DIR = (
    PROJECT_ROOT / TRANSACTION_OUTPUT_DIR / "invoices"
)

SALES_OUTPUT_DIR = (
    PROJECT_ROOT / TRANSACTION_OUTPUT_DIR / "sales"
)

MONEY_PRECISION = Decimal("0.01")
ZERO = Decimal("0.00")
FULFILLMENT_MIN_PERCENT = 80
MULTI_SHIPMENT_PROBABILITY = 0.35
VOID_INVOICE_PROBABILITY = 0.01
PAYMENT_CREDIT_DAYS = 30


# ---------------------------------------------------------
# COMMON HELPERS
# ---------------------------------------------------------

def to_money(value) -> Decimal:

    try:
        result = Decimal(str(value)).quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"Invalid monetary value: {value}")

    if not result.is_finite():
        raise ValueError(f"Non-finite monetary value: {value}")

    return result


def format_money(value: Decimal) -> str:

    return str(
        value.quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )
    )


def parse_date(value: str, field_name: str) -> date:

    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid {field_name}: {value}"
        )


# ---------------------------------------------------------
# LOAD CSV DATA
# ---------------------------------------------------------

def load_csv(
    file_path: Path,
    required_columns: set,
) -> list:

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        actual_columns = set(reader.fieldnames or [])
        missing_columns = required_columns - actual_columns

        if missing_columns:
            raise ValueError(
                f"Missing columns in {file_path.name}: "
                f"{sorted(missing_columns)}"
            )

        records = list(reader)

    if not records:
        raise ValueError(
            f"No records found in {file_path.name}"
        )

    return records


# ---------------------------------------------------------
# LOAD PRODUCT MASTER
# ---------------------------------------------------------

def load_products(file_path: Path) -> dict:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Product master not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        encoding="utf-8",
    ) as file:

        products = json.load(file)

    if not isinstance(products, list) or not products:
        raise ValueError(
            "Product master must be a non-empty JSON list."
        )

    product_lookup = {}

    for product in products:

        product_id = str(
            product.get("product_id", "")
        ).strip()

        if not product_id:
            raise ValueError("Blank product_id in product master.")

        if product_id in product_lookup:
            raise ValueError(
                f"Duplicate product_id: {product_id}"
            )

        mrp = to_money(product["mrp"])
        standard_cost = to_money(product["standard_cost"])

        if mrp <= ZERO:
            raise ValueError(
                f"Invalid MRP for product {product_id}"
            )

        if standard_cost < ZERO:
            raise ValueError(
                f"Invalid standard cost for product {product_id}"
            )

        product_lookup[product_id] = {
            "mrp": mrp,
            "standard_cost": standard_cost,
        }

    return product_lookup


# ---------------------------------------------------------
# LOAD PRODUCT TAX CONFIGURATION
# ---------------------------------------------------------

def load_tax_config(file_path: Path) -> dict:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Tax configuration not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        encoding="utf-8",
    ) as file:

        tax_records = json.load(file)

    if not isinstance(tax_records, list) or not tax_records:
        raise ValueError(
            "Tax configuration must be a non-empty JSON list."
        )

    tax_lookup = defaultdict(list)

    for record in tax_records:

        product_id = str(
            record.get("product_id", "")
        ).strip()

        if not product_id:
            raise ValueError(
                "Blank product_id in tax configuration."
            )

        start_date = parse_date(
            record["effective_start_date"],
            "tax effective_start_date",
        )

        end_date = parse_date(
            record["effective_end_date"],
            "tax effective_end_date",
        )

        if end_date < start_date:
            raise ValueError(
                f"Invalid tax date range for {product_id}"
            )

        tax_rate = Decimal(str(record["tax_rate_pct"]))

        if (
            not tax_rate.is_finite()
            or tax_rate < ZERO
            or tax_rate > Decimal("100")
        ):
            raise ValueError(
                f"Invalid tax rate for product {product_id}"
            )

        tax_lookup[product_id].append({
            "tax_rate_pct": tax_rate,
            "effective_start_date": start_date,
            "effective_end_date": end_date,
        })

    # Detect overlapping periods.
    for product_id, records in tax_lookup.items():

        records.sort(
            key=lambda x: x["effective_start_date"]
        )

        for previous, current in zip(
            records,
            records[1:],
        ):

            if (
                current["effective_start_date"]
                <= previous["effective_end_date"]
            ):
                raise ValueError(
                    f"Overlapping tax periods for {product_id}"
                )

    return tax_lookup


# ---------------------------------------------------------
# GET TAX RATE FOR PRODUCT AND INVOICE DATE
# ---------------------------------------------------------

def get_tax_rate(
    product_id: str,
    invoice_date: date,
    tax_lookup: dict,
) -> Decimal:

    matching_rates = [
        record["tax_rate_pct"]
        for record in tax_lookup.get(product_id, [])
        if (
            record["effective_start_date"]
            <= invoice_date
            <= record["effective_end_date"]
        )
    ]

    if len(matching_rates) != 1:
        raise ValueError(
            f"Expected exactly one effective tax rate for "
            f"product {product_id} on {invoice_date}; "
            f"found {len(matching_rates)}."
        )

    return matching_rates[0]


# ---------------------------------------------------------
# PREPARE AND VALIDATE SOURCE DATA
# ---------------------------------------------------------

def prepare_source_data(
    orders: list,
    order_items: list,
    products: dict,
) -> tuple:

    order_lookup = {}
    items_by_order = defaultdict(list)

    for order in orders:

        order_id = str(order["order_id"]).strip()

        if not order_id:
            raise ValueError("Blank order_id in orders.")

        if order_id in order_lookup:
            raise ValueError(
                f"Duplicate order_id: {order_id}"
            )

        order_date = parse_date(
            order["order_date"],
            "order_date",
        )

        delivery_date = parse_date(
            order["requested_delivery_date"],
            "requested_delivery_date",
        )

        if delivery_date < order_date:
            raise ValueError(
                f"Delivery date precedes order date: {order_id}"
            )

        if order_date > TRANSACTION_END_DATE:
            raise ValueError(
                f"Order date outside transaction period: {order_id}"
            )

        status = order["order_status"].strip().upper()

        if status not in {"CONFIRMED", "CANCELLED"}:
            raise ValueError(
                f"Unexpected initial order status {status} "
                f"for {order_id}."
            )

        order_lookup[order_id] = {
            "order_id": order_id,
            "order_date": order_date,
            "delivery_date": delivery_date,
            "order_status": status,
        }

    seen_item_ids = set()
    seen_order_products = set()

    for item in order_items:

        item_id = str(item["order_item_id"]).strip()
        order_id = str(item["order_id"]).strip()
        product_id = str(item["product_id"]).strip()

        if not item_id or item_id in seen_item_ids:
            raise ValueError(
                f"Blank or duplicate order_item_id: {item_id}"
            )

        seen_item_ids.add(item_id)

        if order_id not in order_lookup:
            raise ValueError(
                f"Order item references unknown order: {order_id}"
            )

        if product_id not in products:
            raise ValueError(
                f"Order item references unknown product: {product_id}"
            )

        combination = (order_id, product_id)

        if combination in seen_order_products:
            raise ValueError(
                f"Duplicate product within order: {combination}"
            )

        seen_order_products.add(combination)

        quantity = int(item["ordered_quantity"])

        if quantity <= 0:
            raise ValueError(
                f"Invalid ordered quantity for {item_id}"
            )

        unit_price = to_money(
            item["requested_unit_price"]
        )

        if unit_price <= ZERO:
            raise ValueError(
                f"Invalid requested unit price for {item_id}"
            )

        if unit_price > products[product_id]["mrp"]:
            raise ValueError(
                f"Requested unit price exceeds MRP for {item_id}"
            )

        discount_pct = Decimal(
            item["requested_discount_pct"]
        )

        if (
            not discount_pct.is_finite()
            or discount_pct < ZERO
            or discount_pct > Decimal("100")
        ):
            raise ValueError(
                f"Invalid discount percentage for {item_id}"
            )

        items_by_order[order_id].append({
            "order_item_id": item_id,
            "order_id": order_id,
            "product_id": product_id,
            "ordered_quantity": quantity,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
        })

    # Every confirmed order must have at least one item.
    for order_id, order in order_lookup.items():

        if (
            order["order_status"] == "CONFIRMED"
            and not items_by_order.get(order_id)
        ):
            raise ValueError(
                f"Confirmed order has no items: {order_id}"
            )

    return order_lookup, items_by_order


# ---------------------------------------------------------
# CALCULATE ONE INVOICE SALES LINE
# ---------------------------------------------------------

def create_sales_line(
    sales_number: int,
    invoice_id: str,
    item: dict,
    invoiced_quantity: int,
    invoice_date: date,
    products: dict,
    tax_lookup: dict,
) -> dict:

    product_id = item["product_id"]

    unit_price = item["unit_price"]
    discount_pct = item["discount_pct"]

    unit_cost = products[product_id]["standard_cost"]

    tax_rate_pct = get_tax_rate(
        product_id=product_id,
        invoice_date=invoice_date,
        tax_lookup=tax_lookup,
    )

    gross_amount = (
        Decimal(invoiced_quantity) * unit_price
    ).quantize(
        MONEY_PRECISION,
        rounding=ROUND_HALF_UP,
    )

    discount_amount = (
        gross_amount * discount_pct / Decimal("100")
    ).quantize(
        MONEY_PRECISION,
        rounding=ROUND_HALF_UP,
    )

    taxable_amount = (
        gross_amount - discount_amount
    ).quantize(
        MONEY_PRECISION,
        rounding=ROUND_HALF_UP,
    )

    tax_amount = (
        taxable_amount * tax_rate_pct / Decimal("100")
    ).quantize(
        MONEY_PRECISION,
        rounding=ROUND_HALF_UP,
    )

    line_total = (
        taxable_amount + tax_amount
    ).quantize(
        MONEY_PRECISION,
        rounding=ROUND_HALF_UP,
    )

    return {
        "sales_id": (
            f"{SALES_ID_PREFIX}{sales_number:09d}"
        ),
        "invoice_id": invoice_id,
        "order_item_id": item["order_item_id"],
        "product_id": product_id,
        "invoiced_quantity": invoiced_quantity,
        "unit_price": format_money(unit_price),
        "unit_cost_at_invoice": format_money(unit_cost),
        "gross_amount": format_money(gross_amount),
        "discount_pct": str(discount_pct),
        "discount_amount": format_money(discount_amount),
        "taxable_amount": format_money(taxable_amount),
        "tax_rate_pct": str(tax_rate_pct),
        "tax_amount": format_money(tax_amount),
        "line_total": format_money(line_total),
    }


# ---------------------------------------------------------
# GENERATE INVOICE HEADERS AND SALES LINES
# ---------------------------------------------------------

def generate_invoice_data(
    order_lookup: dict,
    items_by_order: dict,
    products: dict,
    tax_lookup: dict,
    rng: random.Random,
) -> tuple:

    invoices = []
    sales = []

    invoice_number = 1
    sales_number = 1

    confirmed_orders = [
        order
        for order in order_lookup.values()
        if order["order_status"] == "CONFIRMED"
    ]

    for order in confirmed_orders:

        order_id = order["order_id"]
        order_date = order["order_date"]
        delivery_date = order["delivery_date"]

        order_items = items_by_order[order_id]

        # Determine the quantity that will actually be fulfilled.
        fulfillment = {}

        for item in order_items:

            ordered_quantity = item["ordered_quantity"]

            minimum_fulfillment = max(
                1,
                math.ceil(
                    ordered_quantity
                    * FULFILLMENT_MIN_PERCENT
                    / 100
                ),
            )

            fulfilled_quantity = rng.randint(
                minimum_fulfillment,
                ordered_quantity,
            )

            fulfillment[item["order_item_id"]] = (
                fulfilled_quantity
            )

        # A second shipment is possible only when at least
        # one order item has at least two fulfilled units.
        can_split = any(
            quantity >= 2
            for quantity in fulfillment.values()
        )

        use_two_shipments = (
            can_split
            and rng.random() < MULTI_SHIPMENT_PROBABILITY
        )

        shipment_allocations = {
            1: [],
            2: [],
        }

        for item in order_items:

            fulfilled_quantity = fulfillment[
                item["order_item_id"]
            ]

            if use_two_shipments and fulfilled_quantity >= 2:

                first_quantity = rng.randint(
                    1,
                    fulfilled_quantity - 1,
                )

                second_quantity = (
                    fulfilled_quantity - first_quantity
                )

                shipment_allocations[1].append(
                    (item, first_quantity)
                )

                shipment_allocations[2].append(
                    (item, second_quantity)
                )

            else:

                shipment_allocations[1].append(
                    (item, fulfilled_quantity)
                )

        # Generate invoice date for each non-empty shipment.
        max_delivery_days = (
            delivery_date - order_date
        ).days

        first_invoice_date = order_date + timedelta(
            days=rng.randint(0, max_delivery_days)
        )

        shipment_dates = {
            1: first_invoice_date,
        }

        if shipment_allocations[2]:

            second_invoice_date = first_invoice_date + timedelta(
                days=rng.randint(
                    0,
                    (delivery_date - first_invoice_date).days,
                )
            )

            shipment_dates[2] = second_invoice_date

        # Create invoice header and corresponding sales lines.
        for shipment_number in (1, 2):

            allocations = shipment_allocations[shipment_number]

            if not allocations:
                continue

            invoice_id = (
                f"{INVOICE_ID_PREFIX}{invoice_number:09d}"
            )

            invoice_date = shipment_dates[shipment_number]

            invoice_status = (
                "VOID"
                if rng.random() < VOID_INVOICE_PROBABILITY
                else "ISSUED"
            )

            if invoice_status not in INVOICE_STATUSES:
                raise ValueError(
                    f"Unsupported invoice status: {invoice_status}"
                )

            invoice_sales = []

            for item, quantity in allocations:

                sales_line = create_sales_line(
                    sales_number=sales_number,
                    invoice_id=invoice_id,
                    item=item,
                    invoiced_quantity=quantity,
                    invoice_date=invoice_date,
                    products=products,
                    tax_lookup=tax_lookup,
                )

                invoice_sales.append(sales_line)
                sales.append(sales_line)

                sales_number += 1

            # Aggregate invoice header amounts from its sales lines.
            subtotal = sum(
                (Decimal(row["gross_amount"]) for row in invoice_sales),
                ZERO,
            )

            discount = sum(
                (Decimal(row["discount_amount"]) for row in invoice_sales),
                ZERO,
            )

            taxable = sum(
                (Decimal(row["taxable_amount"]) for row in invoice_sales),
                ZERO,
            )

            tax = sum(
                (Decimal(row["tax_amount"]) for row in invoice_sales),
                ZERO,
            )

            invoice_total = sum(
                (Decimal(row["line_total"]) for row in invoice_sales),
                ZERO,
            )

            created_at = datetime.combine(
                invoice_date,
                datetime.min.time(),
            ).replace(
                hour=12,
                minute=0,
                second=0,
            )

            invoices.append({
                "invoice_id": invoice_id,
                "order_id": order_id,
                "invoice_date": invoice_date.isoformat(),
                "payment_due_date": (
                    invoice_date
                    + timedelta(days=PAYMENT_CREDIT_DAYS)
                ).isoformat(),
                "invoice_status": invoice_status,
                "currency_code": CURRENCY_CODE,
                "subtotal_amount": format_money(subtotal),
                "discount_amount": format_money(discount),
                "taxable_amount": format_money(taxable),
                "tax_amount": format_money(tax),
                "invoice_total": format_money(invoice_total),
                "created_at": created_at.isoformat(),
            })

            invoice_number += 1

    if not invoices or not sales:
        raise ValueError(
            "No invoices or sales lines were generated. "
            "Check whether any confirmed orders exist."
        )

    return invoices, sales


# ---------------------------------------------------------
# VALIDATE GENERATED INVOICE AND SALES DATA
# ---------------------------------------------------------

def validate_generated_data(
    invoices: list,
    sales: list,
    order_lookup: dict,
    items_by_order: dict,
) -> None:

    errors = []

    invoice_lookup = {}
    sales_ids = set()
    invoice_item_pairs = set()

    invoiced_quantity_by_item = defaultdict(int)

    for invoice in invoices:

        invoice_id = invoice["invoice_id"]
        order_id = invoice["order_id"]

        if invoice_id in invoice_lookup:
            errors.append(
                f"Duplicate invoice_id: {invoice_id}"
            )

        invoice_lookup[invoice_id] = invoice

        if order_id not in order_lookup:
            errors.append(
                f"Invoice references unknown order: {invoice_id}"
            )

        elif order_lookup[order_id]["order_status"] != "CONFIRMED":
            errors.append(
                f"Invoice generated for non-confirmed order: {invoice_id}"
            )

    for row in sales:

        sales_id = row["sales_id"]
        invoice_id = row["invoice_id"]
        order_item_id = row["order_item_id"]

        if sales_id in sales_ids:
            errors.append(
                f"Duplicate sales_id: {sales_id}"
            )

        sales_ids.add(sales_id)

        if invoice_id not in invoice_lookup:
            errors.append(
                f"Sales row references unknown invoice: {sales_id}"
            )
            continue

        invoice_order_id = invoice_lookup[invoice_id]["order_id"]

        matching_items = [
            item
            for item in items_by_order.get(invoice_order_id, [])
            if item["order_item_id"] == order_item_id
        ]

        if len(matching_items) != 1:
            errors.append(
                f"Order item does not belong to invoice order: {sales_id}"
            )
            continue

        pair = (invoice_id, order_item_id)

        if pair in invoice_item_pairs:
            errors.append(
                f"Duplicate order item on invoice: {pair}"
            )

        invoice_item_pairs.add(pair)

        quantity = int(row["invoiced_quantity"])

        if quantity <= 0:
            errors.append(
                f"Invalid invoiced quantity: {sales_id}"
            )

        invoiced_quantity_by_item[order_item_id] += quantity

    # Total invoiced quantity cannot exceed ordered quantity.
    for order_id, items in items_by_order.items():

        for item in items:

            item_id = item["order_item_id"]

            total_invoiced = (
                invoiced_quantity_by_item.get(item_id, 0)
            )

            if total_invoiced > item["ordered_quantity"]:
                errors.append(
                    f"Invoiced quantity exceeds ordered quantity: "
                    f"{item_id}"
                )

    # Check invoice header totals against their sales lines.
    sales_by_invoice = defaultdict(list)

    for row in sales:
        sales_by_invoice[row["invoice_id"]].append(row)

    for invoice_id, invoice in invoice_lookup.items():

        invoice_lines = sales_by_invoice[invoice_id]

        expected_totals = {
            "subtotal_amount": sum(
                (Decimal(row["gross_amount"]) for row in invoice_lines),
                ZERO,
            ),
            "discount_amount": sum(
                (Decimal(row["discount_amount"]) for row in invoice_lines),
                ZERO,
            ),
            "taxable_amount": sum(
                (Decimal(row["taxable_amount"]) for row in invoice_lines),
                ZERO,
            ),
            "tax_amount": sum(
                (Decimal(row["tax_amount"]) for row in invoice_lines),
                ZERO,
            ),
            "invoice_total": sum(
                (Decimal(row["line_total"]) for row in invoice_lines),
                ZERO,
            ),
        }

        for field, expected_value in expected_totals.items():

            actual_value = Decimal(invoice[field])

            if actual_value != expected_value:
                errors.append(
                    f"Invoice total mismatch: {invoice_id}, {field}"
                )

    if errors:

        print("\nINVOICE GENERATION VALIDATION FAILED")

        for error in errors[:30]:
            print(f"ERROR: {error}")

        raise ValueError(
            f"Generated data has {len(errors)} validation error(s)."
        )

    print("Invoice and sales data validation successful.")


# ---------------------------------------------------------
# SAVE CSV
# ---------------------------------------------------------

def save_csv(
    records: list,
    output_file: Path,
    fieldnames: list,
) -> None:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(records)

    print(f"Saved: {output_file}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Generate invoices and invoice sales lines."
    )

    parser.add_argument(
        "--orders-file",
        type=Path,
        default=DEFAULT_ORDERS_FILE,
    )

    parser.add_argument(
        "--order-items-file",
        type=Path,
        default=DEFAULT_ORDER_ITEMS_FILE,
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on the number of orders.",
    )

    args = parser.parse_args()

    if args.limit is not None and args.limit <= 0:
        raise ValueError("--limit must be greater than zero.")

    print("=" * 65)
    print("INVOICE AND SALES GENERATION STARTED")
    print("=" * 65)

    orders = load_csv(
        args.orders_file,
        {
            "order_id",
            "order_date",
            "requested_delivery_date",
            "order_status",
        },
    )

    if args.limit is not None:
        orders = orders[:args.limit]

    order_items = load_csv(
        args.order_items_file,
        {
            "order_item_id",
            "order_id",
            "product_id",
            "ordered_quantity",
            "requested_unit_price",
            "requested_discount_pct",
        },
    )

    products = load_products(PRODUCTS_FILE)
    tax_lookup = load_tax_config(TAX_FILE)

    print(f"Loaded orders: {len(orders):,}")
    print(f"Loaded order items: {len(order_items):,}")
    print(f"Loaded products: {len(products):,}")
    print(f"Loaded tax-configured products: {len(tax_lookup):,}")

    order_lookup, items_by_order = prepare_source_data(
        orders=orders,
        order_items=order_items,
        products=products,
    )

    confirmed_count = sum(
        order["order_status"] == "CONFIRMED"
        for order in order_lookup.values()
    )

    cancelled_count = sum(
        order["order_status"] == "CANCELLED"
        for order in order_lookup.values()
    )

    print(f"Confirmed orders: {confirmed_count:,}")
    print(f"Cancelled orders excluded: {cancelled_count:,}")

    rng = random.Random(RANDOM_SEED + 2)

    invoices, sales = generate_invoice_data(
        order_lookup=order_lookup,
        items_by_order=items_by_order,
        products=products,
        tax_lookup=tax_lookup,
        rng=rng,
    )

    print(f"Generated invoices: {len(invoices):,}")
    print(f"Generated sales lines: {len(sales):,}")

    validate_generated_data(
        invoices=invoices,
        sales=sales,
        order_lookup=order_lookup,
        items_by_order=items_by_order,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    invoice_file = (
        INVOICES_OUTPUT_DIR
        / f"invoices_{timestamp}.csv"
    )

    sales_file = (
        SALES_OUTPUT_DIR
        / f"sales_{timestamp}.csv"
    )

    invoice_columns = [
        "invoice_id",
        "order_id",
        "invoice_date",
        "payment_due_date",
        "invoice_status",
        "currency_code",
        "subtotal_amount",
        "discount_amount",
        "taxable_amount",
        "tax_amount",
        "invoice_total",
        "created_at",
    ]

    sales_columns = [
        "sales_id",
        "invoice_id",
        "order_item_id",
        "product_id",
        "invoiced_quantity",
        "unit_price",
        "unit_cost_at_invoice",
        "gross_amount",
        "discount_pct",
        "discount_amount",
        "taxable_amount",
        "tax_rate_pct",
        "tax_amount",
        "line_total",
    ]

    save_csv(
        records=invoices,
        output_file=invoice_file,
        fieldnames=invoice_columns,
    )

    save_csv(
        records=sales,
        output_file=sales_file,
        fieldnames=sales_columns,
    )

    issued_count = sum(
        invoice["invoice_status"] == "ISSUED"
        for invoice in invoices
    )

    void_count = sum(
        invoice["invoice_status"] == "VOID"
        for invoice in invoices
    )

    recognized_revenue = sum(
        (
            Decimal(invoice["invoice_total"])
            for invoice in invoices
            if invoice["invoice_status"] == "ISSUED"
        ),
        ZERO,
    )

    print("\n" + "=" * 65)
    print("GENERATION SUMMARY")
    print("=" * 65)

    print(f"Orders processed: {len(orders):,}")
    print(f"Invoices generated: {len(invoices):,}")
    print(f"ISSUED invoices: {issued_count:,}")
    print(f"VOID invoices: {void_count:,}")
    print(f"Sales lines generated: {len(sales):,}")

    print(
        "Recognized revenue (ISSUED invoices only): "
        f"INR {format_money(recognized_revenue)}"
    )

    print("\nINVOICE AND SALES GENERATION COMPLETED.")
    print("=" * 65)


if __name__ == "__main__":
    main()
