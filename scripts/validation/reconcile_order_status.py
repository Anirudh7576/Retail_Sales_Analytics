
import argparse
import csv

from collections import defaultdict
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from scripts.common.transaction_config import (
    TRANSACTION_OUTPUT_DIR,
    ORDER_STATUSES,
    INVOICE_STATUSES,
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

OUTPUT_DIR = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "orders_reconciled"
)

PERCENT_PRECISION = Decimal("0.01")


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
# PREPARE ORDER LOOKUP
# ---------------------------------------------------------

def prepare_orders(orders: list) -> dict:

    order_lookup = {}

    for order in orders:

        order_id = str(order["order_id"]).strip()

        if not order_id:
            raise ValueError("Blank order_id found.")

        if order_id in order_lookup:
            raise ValueError(
                f"Duplicate order_id: {order_id}"
            )

        original_status = order["order_status"].strip().upper()

        if original_status not in ORDER_STATUSES:
            raise ValueError(
                f"Invalid original order status for {order_id}: "
                f"{original_status}"
            )

        order_lookup[order_id] = {
            "original_status": original_status,
            "source_record": order,
            "ordered_quantity": 0,
            "fulfilled_quantity": 0,
        }

    return order_lookup


# ---------------------------------------------------------
# PREPARE ORDER ITEM LOOKUP
# ---------------------------------------------------------

def prepare_order_items(
    order_items: list,
    order_lookup: dict,
) -> dict:

    item_lookup = {}

    for item in order_items:

        item_id = str(item["order_item_id"]).strip()
        order_id = str(item["order_id"]).strip()

        if not item_id:
            raise ValueError("Blank order_item_id found.")

        if item_id in item_lookup:
            raise ValueError(
                f"Duplicate order_item_id: {item_id}"
            )

        if order_id not in order_lookup:
            raise ValueError(
                f"Order item references unknown order: {order_id}"
            )

        try:
            quantity = int(item["ordered_quantity"])

            if quantity <= 0:
                raise ValueError

        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid ordered quantity for {item_id}"
            )

        item_lookup[item_id] = {
            "order_id": order_id,
            "product_id": str(item["product_id"]).strip(),
            "ordered_quantity": quantity,
        }

        order_lookup[order_id]["ordered_quantity"] += quantity

    # Every order must contain at least one order item.
    for order_id, order in order_lookup.items():

        if order["ordered_quantity"] <= 0:
            raise ValueError(
                f"Order has no valid order items: {order_id}"
            )

    return item_lookup


# ---------------------------------------------------------
# PREPARE INVOICE LOOKUP
# ---------------------------------------------------------

def prepare_invoices(invoices: list) -> dict:

    invoice_lookup = {}

    for invoice in invoices:

        invoice_id = str(invoice["invoice_id"]).strip()
        order_id = str(invoice["order_id"]).strip()
        status = invoice["invoice_status"].strip().upper()

        if not invoice_id:
            raise ValueError("Blank invoice_id found.")

        if invoice_id in invoice_lookup:
            raise ValueError(
                f"Duplicate invoice_id: {invoice_id}"
            )

        if status not in INVOICE_STATUSES:
            raise ValueError(
                f"Invalid invoice status for {invoice_id}: {status}"
            )

        invoice_lookup[invoice_id] = {
            "order_id": order_id,
            "invoice_status": status,
        }

    return invoice_lookup


# ---------------------------------------------------------
# CALCULATE FULFILLED QUANTITIES
# ---------------------------------------------------------

def calculate_fulfilled_quantities(
    sales: list,
    order_lookup: dict,
    item_lookup: dict,
    invoice_lookup: dict,
) -> None:

    seen_sales_ids = set()
    seen_invoice_items = set()

    for line in sales:

        sales_id = str(line["sales_id"]).strip()
        invoice_id = str(line["invoice_id"]).strip()
        item_id = str(line["order_item_id"]).strip()
        product_id = str(line["product_id"]).strip()

        if not sales_id:
            raise ValueError("Blank sales_id found.")

        if sales_id in seen_sales_ids:
            raise ValueError(
                f"Duplicate sales_id: {sales_id}"
            )

        seen_sales_ids.add(sales_id)

        if invoice_id not in invoice_lookup:
            raise ValueError(
                f"Sales line references unknown invoice: {invoice_id}"
            )

        if item_id not in item_lookup:
            raise ValueError(
                f"Sales line references unknown order item: {item_id}"
            )

        invoice = invoice_lookup[invoice_id]
        order_item = item_lookup[item_id]

        invoice_order_id = invoice["order_id"]
        item_order_id = order_item["order_id"]

        if invoice_order_id not in order_lookup:
            raise ValueError(
                f"Invoice references unknown order: {invoice_id}"
            )

        if invoice_order_id != item_order_id:
            raise ValueError(
                f"Order mismatch between invoice {invoice_id} "
                f"and order item {item_id}"
            )

        if product_id != order_item["product_id"]:
            raise ValueError(
                f"Product mismatch for sales line {sales_id}"
            )

        invoice_item_key = (invoice_id, item_id)

        if invoice_item_key in seen_invoice_items:
            raise ValueError(
                f"Duplicate order item on invoice: {invoice_item_key}"
            )

        seen_invoice_items.add(invoice_item_key)

        try:
            quantity = int(line["invoiced_quantity"])

            if quantity <= 0:
                raise ValueError

        except (ValueError, TypeError):
            raise ValueError(
                f"Invalid invoiced quantity for {sales_id}"
            )

        # VOID invoice quantities do not count as fulfilled.
        if invoice["invoice_status"] == "VOID":
            continue

        order = order_lookup[invoice_order_id]

        if order["original_status"] == "CANCELLED":
            raise ValueError(
                f"Cancelled order {invoice_order_id} "
                f"has an ISSUED invoice."
            )

        order["fulfilled_quantity"] += quantity

    # Ensure issued quantities do not exceed ordered quantities.
    for order_id, order in order_lookup.items():

        fulfilled = order["fulfilled_quantity"]
        ordered = order["ordered_quantity"]

        if fulfilled > ordered:
            raise ValueError(
                f"Fulfilled quantity exceeds ordered quantity "
                f"for {order_id}: {fulfilled} > {ordered}"
            )


# ---------------------------------------------------------
# RECONCILE ORDER STATUS
# ---------------------------------------------------------

def reconcile_order_status(
    order_lookup: dict,
    reconciliation_timestamp: str,
) -> list:

    reconciled_orders = []

    for order_id, order in order_lookup.items():

        original_status = order["original_status"]

        ordered_quantity = order["ordered_quantity"]
        fulfilled_quantity = order["fulfilled_quantity"]

        remaining_quantity = (
            ordered_quantity - fulfilled_quantity
        )

        if original_status == "CANCELLED":

            final_status = "CANCELLED"

        elif fulfilled_quantity == 0:

            final_status = "CONFIRMED"

        elif fulfilled_quantity == ordered_quantity:

            final_status = "FULFILLED"

        else:

            final_status = "PARTIALLY_FULFILLED"

        fulfillment_pct = (
            Decimal(fulfilled_quantity)
            / Decimal(ordered_quantity)
            * Decimal("100")
        ).quantize(
            PERCENT_PRECISION,
            rounding=ROUND_HALF_UP,
        )

        reconciled_record = dict(
            order["source_record"]
        )

        reconciled_record.update({
            "original_order_status": original_status,
            "reconciled_order_status": final_status,
            "ordered_quantity_total": ordered_quantity,
            "fulfilled_quantity_total": fulfilled_quantity,
            "remaining_quantity_total": remaining_quantity,
            "fulfillment_pct": str(fulfillment_pct),
            "reconciled_at": reconciliation_timestamp,
        })

        reconciled_orders.append(reconciled_record)

    return reconciled_orders


# ---------------------------------------------------------
# VALIDATE RECONCILED ORDERS
# ---------------------------------------------------------

def validate_reconciled_orders(
    reconciled_orders: list,
) -> dict:

    errors = []
    seen_order_ids = set()

    status_counts = defaultdict(int)

    for order in reconciled_orders:

        order_id = order["order_id"]

        if order_id in seen_order_ids:
            errors.append(
                f"Duplicate reconciled order_id: {order_id}"
            )

        seen_order_ids.add(order_id)

        original_status = order["original_order_status"]
        final_status = order["reconciled_order_status"]

        ordered = int(order["ordered_quantity_total"])
        fulfilled = int(order["fulfilled_quantity_total"])
        remaining = int(order["remaining_quantity_total"])

        # Quantity reconciliation.
        if ordered != fulfilled + remaining:
            errors.append(
                f"Quantity mismatch for {order_id}"
            )

        if fulfilled < 0 or remaining < 0:
            errors.append(
                f"Negative quantity for {order_id}"
            )

        # Status reconciliation.
        if original_status == "CANCELLED":

            if final_status != "CANCELLED":
                errors.append(
                    f"Cancelled order status changed: {order_id}"
                )

            if fulfilled != 0:
                errors.append(
                    f"Cancelled order has fulfilled quantity: {order_id}"
                )

        elif fulfilled == 0:

            if final_status != "CONFIRMED":
                errors.append(
                    f"Incorrect zero-fulfillment status: {order_id}"
                )

        elif fulfilled == ordered:

            if final_status != "FULFILLED":
                errors.append(
                    f"Incorrect fulfilled status: {order_id}"
                )

        else:

            if final_status != "PARTIALLY_FULFILLED":
                errors.append(
                    f"Incorrect partial fulfillment status: {order_id}"
                )

        status_counts[final_status] += 1

    if errors:

        print("\nRECONCILIATION VALIDATION FAILED")

        for error in errors[:20]:
            print(f"ERROR: {error}")

        raise ValueError(
            f"Reconciliation has {len(errors)} error(s)."
        )

    return dict(status_counts)


# ---------------------------------------------------------
# SAVE RECONCILED ORDERS
# ---------------------------------------------------------

def save_reconciled_orders(
    records: list,
    output_file: Path,
) -> None:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(records[0].keys())

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

    print(f"Reconciled orders saved: {output_file}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Reconcile order statuses using issued invoices."
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
    print("ORDER STATUS RECONCILIATION STARTED")
    print("=" * 65)

    orders = load_csv(
        args.orders_file,
        {
            "order_id",
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
        },
    )

    invoices = load_csv(
        args.invoices_file,
        {
            "invoice_id",
            "order_id",
            "invoice_status",
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
        },
    )

    print(f"Loaded orders: {len(orders):,}")
    print(f"Loaded order items: {len(order_items):,}")
    print(f"Loaded invoices: {len(invoices):,}")
    print(f"Loaded sales lines: {len(sales):,}")

    order_lookup = prepare_orders(orders)

    item_lookup = prepare_order_items(
        order_items,
        order_lookup,
    )

    invoice_lookup = prepare_invoices(invoices)

    calculate_fulfilled_quantities(
        sales=sales,
        order_lookup=order_lookup,
        item_lookup=item_lookup,
        invoice_lookup=invoice_lookup,
    )

    reconciliation_timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    reconciled_orders = reconcile_order_status(
        order_lookup=order_lookup,
        reconciliation_timestamp=reconciliation_timestamp,
    )

    status_counts = validate_reconciled_orders(
        reconciled_orders
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    output_file = (
        OUTPUT_DIR
        / f"orders_reconciled_{timestamp}.csv"
    )

    save_reconciled_orders(
        records=reconciled_orders,
        output_file=output_file,
    )

    print("\n" + "=" * 65)
    print("RECONCILIATION SUMMARY")
    print("=" * 65)

    print(f"Total orders: {len(reconciled_orders):,}")

    for status in [
        "CONFIRMED",
        "PARTIALLY_FULFILLED",
        "FULFILLED",
        "CANCELLED",
    ]:
        print(
            f"{status}: {status_counts.get(status, 0):,}"
        )

    total_ordered = sum(
        int(row["ordered_quantity_total"])
        for row in reconciled_orders
    )

    total_fulfilled = sum(
        int(row["fulfilled_quantity_total"])
        for row in reconciled_orders
    )

    total_remaining = sum(
        int(row["remaining_quantity_total"])
        for row in reconciled_orders
    )

    print("\nQUANTITY SUMMARY")

    print(f"Total ordered quantity: {total_ordered:,}")
    print(f"Total fulfilled quantity: {total_fulfilled:,}")
    print(f"Total remaining quantity: {total_remaining:,}")

    print("\nPASS: Order status reconciliation successful.")

    print("=" * 65)


if __name__ == "__main__":
    main()
