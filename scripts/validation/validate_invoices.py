
import argparse
import csv
import json
import sys

from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from scripts.common.transaction_config import (
    CURRENCY_CODE,
    INVOICE_STATUSES,
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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

DEFAULT_INVOICES_FILE = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "invoices"
    / "invoices_20261119_111536_710746.csv"
)

DEFAULT_SALES_FILE = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "sales"
    / "sales_20261119_111536_710746.csv"
)

PRODUCTS_FILE = (
    PROJECT_ROOT
    / MASTER_DATA_DIR
    / MASTER_FILES["products"]
)

TAX_FILE = PROJECT_ROOT / TAX_CONFIG_FILE

MONEY_PRECISION = Decimal("0.01")
ZERO = Decimal("0.00")
ONE_HUNDRED = Decimal("100.00")
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


def parse_decimal(value, field_name: str) -> Decimal:

    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(
            f"Invalid decimal value for {field_name}: {value}"
        )

    if not result.is_finite():
        raise ValueError(
            f"Non-finite value for {field_name}: {value}"
        )

    return result


def parse_date(value: str, field_name: str) -> date:

    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid {field_name}: {value}"
        )


# ---------------------------------------------------------
# LOAD CSV
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

        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError(
            "Product master must be a non-empty JSON list."
        )

    products = {}

    for record in records:

        product_id = str(
            record.get("product_id", "")
        ).strip()

        if not product_id:
            raise ValueError("Blank product_id in product master.")

        if product_id in products:
            raise ValueError(
                f"Duplicate product_id: {product_id}"
            )

        mrp = to_money(record["mrp"])
        standard_cost = to_money(record["standard_cost"])

        if mrp <= ZERO:
            raise ValueError(
                f"Invalid MRP for product {product_id}"
            )

        if standard_cost < ZERO:
            raise ValueError(
                f"Invalid standard cost for product {product_id}"
            )

        products[product_id] = {
            "mrp": mrp,
            "standard_cost": standard_cost,
        }

    return products


# ---------------------------------------------------------
# LOAD TAX CONFIGURATION
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

        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError(
            "Tax configuration must be a non-empty JSON list."
        )

    tax_lookup = defaultdict(list)

    for record in records:

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

        tax_rate = parse_decimal(
            record["tax_rate_pct"],
            "tax_rate_pct",
        )

        if end_date < start_date:
            raise ValueError(
                f"Invalid tax period for {product_id}"
            )

        if tax_rate < ZERO or tax_rate > ONE_HUNDRED:
            raise ValueError(
                f"Invalid tax rate for {product_id}"
            )

        tax_lookup[product_id].append({
            "start_date": start_date,
            "end_date": end_date,
            "tax_rate_pct": tax_rate,
        })

    # Check for overlapping effective periods.
    for product_id, periods in tax_lookup.items():

        periods.sort(
            key=lambda x: x["start_date"]
        )

        for previous, current in zip(
            periods,
            periods[1:],
        ):

            if current["start_date"] <= previous["end_date"]:
                raise ValueError(
                    f"Overlapping tax periods for {product_id}"
                )

    return tax_lookup


def get_effective_tax_rate(
    product_id: str,
    invoice_date: date,
    tax_lookup: dict,
) -> Decimal:

    matches = [
        record["tax_rate_pct"]
        for record in tax_lookup.get(product_id, [])
        if (
            record["start_date"]
            <= invoice_date
            <= record["end_date"]
        )
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one tax rate for product "
            f"{product_id} on {invoice_date}; found {len(matches)}."
        )

    return matches[0]


# ---------------------------------------------------------
# BUILD SOURCE LOOKUPS
# ---------------------------------------------------------

def build_order_lookup(orders: list) -> dict:

    lookup = {}

    for order in orders:

        order_id = str(order["order_id"]).strip()

        if not order_id or order_id in lookup:
            raise ValueError(
                f"Blank or duplicate order_id: {order_id}"
            )

        lookup[order_id] = {
            "order_date": parse_date(
                order["order_date"],
                "order_date",
            ),
            "delivery_date": parse_date(
                order["requested_delivery_date"],
                "requested_delivery_date",
            ),
            "order_status": order["order_status"].strip().upper(),
        }

    return lookup


def build_order_item_lookup(order_items: list) -> dict:

    lookup = {}

    for item in order_items:

        item_id = str(item["order_item_id"]).strip()

        if not item_id or item_id in lookup:
            raise ValueError(
                f"Blank or duplicate order_item_id: {item_id}"
            )

        lookup[item_id] = {
            "order_id": str(item["order_id"]).strip(),
            "product_id": str(item["product_id"]).strip(),
            "ordered_quantity": int(item["ordered_quantity"]),
            "unit_price": to_money(
                item["requested_unit_price"]
            ),
            "discount_pct": parse_decimal(
                item["requested_discount_pct"],
                "requested_discount_pct",
            ),
        }

    return lookup


# ---------------------------------------------------------
# INDEPENDENT VALIDATION
# ---------------------------------------------------------

def validate_invoice_data(
    orders: list,
    order_items: list,
    invoices: list,
    sales: list,
    products: dict,
    tax_lookup: dict,
) -> dict:

    errors = []

    order_lookup = build_order_lookup(orders)
    order_item_lookup = build_order_item_lookup(order_items)

    invoice_lookup = {}
    sales_ids = set()
    invoice_item_pairs = set()

    sales_by_invoice = defaultdict(list)

    # Quantity from ISSUED invoices only.
    issued_quantity_by_item = defaultdict(int)

    # All invoiced quantities, including VOID, for audit.
    all_quantity_by_item = defaultdict(int)

    # -----------------------------------------------------
    # 1. INVOICE HEADER CHECKS
    # -----------------------------------------------------

    for row_number, invoice in enumerate(invoices, start=2):

        invoice_id = str(invoice["invoice_id"]).strip()
        order_id = str(invoice["order_id"]).strip()

        if not invoice_id:
            errors.append(
                f"Invoice row {row_number}: blank invoice_id."
            )
            continue

        if invoice_id in invoice_lookup:
            errors.append(
                f"Duplicate invoice_id: {invoice_id}"
            )
            continue

        invoice_lookup[invoice_id] = invoice

        if order_id not in order_lookup:
            errors.append(
                f"Invoice {invoice_id}: unknown order_id {order_id}."
            )
            continue

        order = order_lookup[order_id]

        invoice_date = parse_date(
            invoice["invoice_date"],
            "invoice_date",
        )

        due_date = parse_date(
            invoice["payment_due_date"],
            "payment_due_date",
        )

        if not (
            order["order_date"]
            <= invoice_date
            <= order["delivery_date"]
        ):
            errors.append(
                f"Invoice {invoice_id}: invoice date outside "
                f"order/delivery date range."
            )

        if due_date != invoice_date + timedelta(
            days=PAYMENT_CREDIT_DAYS
        ):
            errors.append(
                f"Invoice {invoice_id}: incorrect payment_due_date."
            )

        if invoice["invoice_status"] not in INVOICE_STATUSES:
            errors.append(
                f"Invoice {invoice_id}: invalid status."
            )

        if invoice["currency_code"] != CURRENCY_CODE:
            errors.append(
                f"Invoice {invoice_id}: unexpected currency."
            )

        if order["order_status"] != "CONFIRMED":
            errors.append(
                f"Invoice {invoice_id}: parent order is not CONFIRMED."
            )

        if not invoice["created_at"]:
            errors.append(
                f"Invoice {invoice_id}: missing created_at."
            )

    # -----------------------------------------------------
    # 2. SALES LINE CHECKS
    # -----------------------------------------------------

    for row_number, line in enumerate(sales, start=2):

        sales_id = str(line["sales_id"]).strip()
        invoice_id = str(line["invoice_id"]).strip()
        item_id = str(line["order_item_id"]).strip()
        product_id = str(line["product_id"]).strip()

        if not sales_id:
            errors.append(
                f"Sales row {row_number}: blank sales_id."
            )

        elif sales_id in sales_ids:
            errors.append(
                f"Duplicate sales_id: {sales_id}"
            )

        sales_ids.add(sales_id)

        if invoice_id not in invoice_lookup:
            errors.append(
                f"Sales {sales_id}: unknown invoice_id {invoice_id}."
            )
            continue

        if item_id not in order_item_lookup:
            errors.append(
                f"Sales {sales_id}: unknown order_item_id {item_id}."
            )
            continue

        if product_id not in products:
            errors.append(
                f"Sales {sales_id}: unknown product_id {product_id}."
            )
            continue

        invoice = invoice_lookup[invoice_id]
        original_item = order_item_lookup[item_id]

        invoice_order_id = str(invoice["order_id"]).strip()

        # The order item must belong to the invoice's order.
        if original_item["order_id"] != invoice_order_id:
            errors.append(
                f"Sales {sales_id}: order item belongs to another order."
            )

        # Product must match the original order item.
        if original_item["product_id"] != product_id:
            errors.append(
                f"Sales {sales_id}: product does not match order item."
            )

        # One order item may appear only once per invoice.
        pair = (invoice_id, item_id)

        if pair in invoice_item_pairs:
            errors.append(
                f"Duplicate order_item_id on invoice: {pair}"
            )

        invoice_item_pairs.add(pair)

        try:
            quantity = int(line["invoiced_quantity"])

            if quantity <= 0:
                raise ValueError

        except (ValueError, TypeError):
            errors.append(
                f"Sales {sales_id}: invalid invoiced quantity."
            )
            continue

        all_quantity_by_item[item_id] += quantity

        if invoice["invoice_status"] == "ISSUED":
            issued_quantity_by_item[item_id] += quantity

        # ---------------------------------------------
        # 2A. PRICE AND DISCOUNT
        # ---------------------------------------------

        unit_price = to_money(line["unit_price"])
        unit_cost = to_money(line["unit_cost_at_invoice"])

        discount_pct = parse_decimal(
            line["discount_pct"],
            "discount_pct",
        )

        if unit_price != original_item["unit_price"]:
            errors.append(
                f"Sales {sales_id}: unit price differs from order item."
            )

        if discount_pct != original_item["discount_pct"]:
            errors.append(
                f"Sales {sales_id}: discount differs from order item."
            )

        expected_cost = products[product_id]["standard_cost"]

        if unit_cost != expected_cost:
            errors.append(
                f"Sales {sales_id}: unit cost snapshot differs "
                f"from product master."
            )

        if discount_pct < ZERO or discount_pct > ONE_HUNDRED:
            errors.append(
                f"Sales {sales_id}: invalid discount percentage."
            )
            continue

        # ---------------------------------------------
        # 2B. TAX RATE VALIDATION
        # ---------------------------------------------

        invoice_date = parse_date(
            invoice["invoice_date"],
            "invoice_date",
        )

        try:
            expected_tax_rate = get_effective_tax_rate(
                product_id,
                invoice_date,
                tax_lookup,
            )
        except ValueError as error:
            errors.append(str(error))
            continue

        actual_tax_rate = parse_decimal(
            line["tax_rate_pct"],
            "tax_rate_pct",
        )

        if actual_tax_rate != expected_tax_rate:
            errors.append(
                f"Sales {sales_id}: tax rate does not match "
                f"effective product tax configuration."
            )

        # ---------------------------------------------
        # 2C. RE-CALCULATE LINE AMOUNTS
        # ---------------------------------------------

        gross = (
            Decimal(quantity) * unit_price
        ).quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )

        discount_amount = (
            gross * discount_pct / ONE_HUNDRED
        ).quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )

        taxable = gross - discount_amount

        tax_amount = (
            taxable * expected_tax_rate / ONE_HUNDRED
        ).quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )

        line_total = taxable + tax_amount

        expected_values = {
            "gross_amount": gross,
            "discount_amount": discount_amount,
            "taxable_amount": taxable,
            "tax_amount": tax_amount,
            "line_total": line_total,
        }

        for field, expected in expected_values.items():

            actual = to_money(line[field])

            if actual != expected:
                errors.append(
                    f"Sales {sales_id}: incorrect {field}. "
                    f"Expected {expected}, found {actual}."
                )

        sales_by_invoice[invoice_id].append(line)

    # -----------------------------------------------------
    # 3. QUANTITY VALIDATION
    # -----------------------------------------------------

    for item_id, original_item in order_item_lookup.items():

        ordered_quantity = original_item["ordered_quantity"]

        issued_quantity = issued_quantity_by_item.get(
            item_id,
            0,
        )

        all_quantity = all_quantity_by_item.get(
            item_id,
            0,
        )

        # Business rule: actual fulfillment is based on ISSUED
        # invoices, not VOID invoices.
        if issued_quantity > ordered_quantity:
            errors.append(
                f"Order item {item_id}: ISSUED quantity "
                f"{issued_quantity} exceeds ordered quantity "
                f"{ordered_quantity}."
            )

        # Additional audit check: even including VOID invoices,
        # generated allocations must not exceed ordered quantity.
        if all_quantity > ordered_quantity:
            errors.append(
                f"Order item {item_id}: total allocated quantity "
                f"including VOID invoices exceeds ordered quantity."
            )

    # -----------------------------------------------------
    # 4. INVOICE HEADER TOTAL VALIDATION
    # -----------------------------------------------------

    invoice_totals = {}

    for invoice_id, invoice in invoice_lookup.items():

        lines = sales_by_invoice.get(invoice_id, [])

        if not lines:
            errors.append(
                f"Invoice {invoice_id}: no corresponding sales lines."
            )
            continue

        calculated_totals = {
            "subtotal_amount": sum(
                (to_money(line["gross_amount"]) for line in lines),
                ZERO,
            ),
            "discount_amount": sum(
                (to_money(line["discount_amount"]) for line in lines),
                ZERO,
            ),
            "taxable_amount": sum(
                (to_money(line["taxable_amount"]) for line in lines),
                ZERO,
            ),
            "tax_amount": sum(
                (to_money(line["tax_amount"]) for line in lines),
                ZERO,
            ),
            "invoice_total": sum(
                (to_money(line["line_total"]) for line in lines),
                ZERO,
            ),
        }

        for field, expected in calculated_totals.items():

            actual = to_money(invoice[field])

            if actual != expected:
                errors.append(
                    f"Invoice {invoice_id}: {field} mismatch. "
                    f"Expected {expected}, found {actual}."
                )

        invoice_totals[invoice_id] = calculated_totals

    # -----------------------------------------------------
    # 5. RECOGNIZED REVENUE
    # -----------------------------------------------------

    issued_revenue = sum(
        (
            invoice_totals[invoice_id]["invoice_total"]
            for invoice_id, invoice in invoice_lookup.items()
            if invoice["invoice_status"] == "ISSUED"
            and invoice_id in invoice_totals
        ),
        ZERO,
    )

    issued_tax = sum(
        (
            invoice_totals[invoice_id]["tax_amount"]
            for invoice_id, invoice in invoice_lookup.items()
            if invoice["invoice_status"] == "ISSUED"
            and invoice_id in invoice_totals
        ),
        ZERO,
    )

    issued_net_sales = issued_revenue - issued_tax

    void_invoice_count = sum(
        invoice["invoice_status"] == "VOID"
        for invoice in invoices
    )

    issued_invoice_count = sum(
        invoice["invoice_status"] == "ISSUED"
        for invoice in invoices
    )

    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "order_count": len(orders),
        "order_item_count": len(order_items),
        "invoice_count": len(invoices),
        "sales_count": len(sales),
        "issued_invoice_count": issued_invoice_count,
        "void_invoice_count": void_invoice_count,
        "issued_revenue": issued_revenue,
        "issued_tax": issued_tax,
        "issued_net_sales": issued_net_sales,
        "issued_quantity": sum(
            issued_quantity_by_item.values()
        ),
        "void_quantity": sum(
            all_quantity_by_item.values()
        ) - sum(
            issued_quantity_by_item.values()
        ),
    }


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Independently validate invoices and sales."
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
        "--invoices-file",
        type=Path,
        default=DEFAULT_INVOICES_FILE,
    )

    parser.add_argument(
        "--sales-file",
        type=Path,
        default=DEFAULT_SALES_FILE,
    )

    args = parser.parse_args()

    print("=" * 65)
    print("INVOICE AND SALES INDEPENDENT VALIDATION STARTED")
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

    invoices = load_csv(
        args.invoices_file,
        {
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
        },
    )

    sales = load_csv(
        args.sales_file,
        {
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
        },
    )

    products = load_products(PRODUCTS_FILE)
    tax_lookup = load_tax_config(TAX_FILE)

    print(f"Loaded orders: {len(orders):,}")
    print(f"Loaded order items: {len(order_items):,}")
    print(f"Loaded invoices: {len(invoices):,}")
    print(f"Loaded sales lines: {len(sales):,}")
    print(f"Loaded products: {len(products):,}")
    print(f"Loaded tax-configured products: {len(tax_lookup):,}")

    result = validate_invoice_data(
        orders=orders,
        order_items=order_items,
        invoices=invoices,
        sales=sales,
        products=products,
        tax_lookup=tax_lookup,
    )

    print("\n" + "=" * 65)
    print("INVOICE VALIDATION SUMMARY")
    print("=" * 65)

    print(f"Orders checked: {result['order_count']:,}")
    print(f"Order items checked: {result['order_item_count']:,}")
    print(f"Invoices checked: {result['invoice_count']:,}")
    print(f"Sales lines checked: {result['sales_count']:,}")

    print(
        f"ISSUED invoices: {result['issued_invoice_count']:,}"
    )

    print(
        f"VOID invoices: {result['void_invoice_count']:,}"
    )

    if not result["passed"]:

        print(f"\nFAILED: {len(result['errors'])} error(s).")

        for error in result["errors"][:30]:
            print(f"ERROR: {error}")

        if len(result["errors"]) > 30:
            print(
                f"... and {len(result['errors']) - 30} more errors."
            )

        print("\nINVOICE VALIDATION FAILED.")
        sys.exit(1)

    print("\nQUANTITY SUMMARY")

    print(
        f"ISSUED invoiced units: {result['issued_quantity']:,}"
    )

    print(
        f"VOID invoice units: {result['void_quantity']:,}"
    )

    print("\nFINANCIAL SUMMARY")

    print(
        "Recognized invoice value including tax: "
        f"INR {result['issued_revenue']:,.2f}"
    )

    print(
        "Tax on ISSUED invoices: "
        f"INR {result['issued_tax']:,.2f}"
    )

    print(
        "Net sales excluding tax: "
        f"INR {result['issued_net_sales']:,.2f}"
    )

    print("\nPASS: All independent invoice and sales checks passed.")
    print("INVOICE AND SALES VALIDATION SUCCESSFUL.")

    print("=" * 65)


if __name__ == "__main__":
    main()
