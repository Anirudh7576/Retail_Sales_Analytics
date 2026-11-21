
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from collections import Counter, defaultdict


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORDERS_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/orders/"
    / "orders_20261118_121559_771171.csv"
)

ORDER_ITEMS_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/order_items/"
    / "order_items_20261119_104252_195977.csv"
)

INVOICES_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/invoices/"
    / "invoices_20261119_111536_710746.csv"
)

SALES_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/sales/"
    / "sales_20261119_111536_710746.csv"
)

RECONCILED_ORDERS_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/orders_reconciled/"
    / "orders_reconciled_20261119_114019_453348.csv"
)

VALID_ORDER_STATUSES = {
    "CONFIRMED",
    "PARTIALLY_FULFILLED",
    "FULFILLED",
    "CANCELLED",
}

VALID_INVOICE_STATUSES = {"ISSUED", "VOID"}

TOLERANCE = Decimal("0.01")


# ============================================================
# 2. COMMON UTILITY FUNCTIONS
# ============================================================

def load_csv(file_path):

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(
                f"CSV header is missing: {file_path}"
            )

        rows = list(reader)

        return reader.fieldnames, rows


def resolve_column(headers, candidates, file_name):

    normalized_headers = {
        header.strip().lower(): header
        for header in headers
    }

    for candidate in candidates:

        if candidate.lower() in normalized_headers:
            return normalized_headers[candidate.lower()]

    raise ValueError(
        f"Could not find any of these columns "
        f"{candidates} in {file_name}. "
        f"Available columns: {headers}"
    )


def optional_column(headers, candidates):

    normalized_headers = {
        header.strip().lower(): header
        for header in headers
    }

    for candidate in candidates:

        if candidate.lower() in normalized_headers:
            return normalized_headers[candidate.lower()]

    return None


def get_value(row, column):

    return str(row.get(column, "")).strip()


def to_decimal(value, field_name):

    try:
        result = Decimal(str(value).strip())

        if not result.is_finite():
            raise ValueError(
                f"{field_name} is not a finite number"
            )

        return result

    except (InvalidOperation, ValueError):
        raise ValueError(
            f"Invalid numeric value for {field_name}: {value}"
        )


def find_duplicates(values):

    return [
        value
        for value, count in Counter(values).items()
        if count > 1
    ]


# ============================================================
# 3. LOAD ALL TRANSACTION FILES
# ============================================================

def load_transaction_data():

    print("=" * 70)
    print("TRANSACTION DATA LOADING")
    print("=" * 70)

    orders_headers, orders = load_csv(ORDERS_FILE)

    order_items_headers, order_items = load_csv(
        ORDER_ITEMS_FILE
    )

    invoices_headers, invoices = load_csv(
        INVOICES_FILE
    )

    sales_headers, sales = load_csv(
        SALES_FILE
    )

    reconciled_headers, reconciled_orders = load_csv(
        RECONCILED_ORDERS_FILE
    )

    print(f"Orders loaded: {len(orders)}")
    print(f"Order items loaded: {len(order_items)}")
    print(f"Invoices loaded: {len(invoices)}")
    print(f"Sales lines loaded: {len(sales)}")
    print(
        f"Reconciled orders loaded: "
        f"{len(reconciled_orders)}"
    )

    return {
        "orders": (orders_headers, orders),
        "order_items": (order_items_headers, order_items),
        "invoices": (invoices_headers, invoices),
        "sales": (sales_headers, sales),
        "reconciled": (reconciled_headers, reconciled_orders),
    }


# ============================================================
# 4. RESOLVE CSV COLUMN NAMES
# ============================================================

def resolve_all_columns(data):

    columns = {}

    orders_headers = data["orders"][0]
    item_headers = data["order_items"][0]
    invoice_headers = data["invoices"][0]
    sales_headers = data["sales"][0]
    reconciled_headers = data["reconciled"][0]

    columns["order_id"] = resolve_column(
        orders_headers,
        ["order_id"],
        "orders.csv",
    )

    columns["item_order_id"] = resolve_column(
        item_headers,
        ["order_id"],
        "order_items.csv",
    )

    columns["order_item_id"] = resolve_column(
        item_headers,
        ["order_item_id"],
        "order_items.csv",
    )

    columns["item_product_id"] = resolve_column(
        item_headers,
        ["product_id"],
        "order_items.csv",
    )

    columns["ordered_quantity"] = resolve_column(
        item_headers,
        ["ordered_quantity", "quantity_ordered", "order_quantity"],
        "order_items.csv",
    )

    columns["invoice_id"] = resolve_column(
        invoice_headers,
        ["invoice_id"],
        "invoices.csv",
    )

    columns["invoice_order_id"] = resolve_column(
        invoice_headers,
        ["order_id"],
        "invoices.csv",
    )

    columns["invoice_status"] = resolve_column(
        invoice_headers,
        ["invoice_status", "status"],
        "invoices.csv",
    )

    columns["invoice_total"] = resolve_column(
        invoice_headers,
        [
            "invoice_total",
            "total_invoice_amount",
            "invoice_amount",
            "total_amount",
        ],
        "invoices.csv",
    )

    columns["sales_id"] = resolve_column(
        sales_headers,
        [
            "sales_id",
            "sale_id",
            "sales_line_id",
        ],
        "sales.csv",
    )

    columns["sales_invoice_id"] = resolve_column(
        sales_headers,
        ["invoice_id"],
        "sales.csv",
    )

    

    columns["sales_item_id"] = resolve_column(
        sales_headers,
        ["order_item_id"],
        "sales.csv",
    )

    columns["sales_product_id"] = resolve_column(
        sales_headers,
        ["product_id"],
        "sales.csv",
    )

    columns["sales_quantity"] = resolve_column(
        sales_headers,
        [
            "quantity",
            "invoiced_quantity",
            "sales_quantity",
            "fulfilled_quantity",
        ],
        "sales.csv",
    )

    columns["sales_line_total"] = resolve_column(
        sales_headers,
        [
            "line_total",
            "line_total_amount",
            "total_line_amount",
        ],
        "sales.csv",
    )

    columns["reconciled_order_id"] = resolve_column(
        reconciled_headers,
        ["order_id"],
        "orders_reconciled.csv",
    )

    columns["original_status"] = resolve_column(
        reconciled_headers,
        ["original_order_status"],
        "orders_reconciled.csv",
    )

    columns["reconciled_status"] = resolve_column(
        reconciled_headers,
        ["reconciled_order_status"],
        "orders_reconciled.csv",
    )

    columns["reconciled_ordered_qty"] = resolve_column(
        reconciled_headers,
        ["ordered_quantity_total"],
        "orders_reconciled.csv",
    )

    columns["reconciled_fulfilled_qty"] = resolve_column(
        reconciled_headers,
        ["fulfilled_quantity_total"],
        "orders_reconciled.csv",
    )

    columns["reconciled_remaining_qty"] = resolve_column(
        reconciled_headers,
        ["remaining_quantity_total"],
        "orders_reconciled.csv",
    )

    return columns


# ============================================================
# 5. PRIMARY KEY VALIDATION
# ============================================================

def validate_primary_keys(data, columns):

    errors = []

    key_definitions = [
        (
            "orders",
            data["orders"][1],
            columns["order_id"],
        ),
        (
            "order_items",
            data["order_items"][1],
            columns["order_item_id"],
        ),
        (
            "invoices",
            data["invoices"][1],
            columns["invoice_id"],
        ),
        (
            "sales",
            data["sales"][1],
            columns["sales_id"],
        ),
        (
            "reconciled orders",
            data["reconciled"][1],
            columns["reconciled_order_id"],
        ),
    ]

    for table_name, rows, key_column in key_definitions:

        values = [
            get_value(row, key_column)
            for row in rows
        ]

        if any(not value for value in values):
            errors.append(
                f"{table_name}: Blank primary key found"
            )

        duplicates = find_duplicates(values)

        if duplicates:
            errors.append(
                f"{table_name}: Duplicate primary keys "
                f"found: {duplicates[:5]}"
            )

    return errors


# ============================================================
# 6. BUILD LOOKUP DICTIONARIES
# ============================================================

def build_lookups(data, columns):

    orders = {
        get_value(row, columns["order_id"]): row
        for row in data["orders"][1]
    }

    order_items = {
        get_value(row, columns["order_item_id"]): row
        for row in data["order_items"][1]
    }

    invoices = {
        get_value(row, columns["invoice_id"]): row
        for row in data["invoices"][1]
    }

    reconciled = {
        get_value(row, columns["reconciled_order_id"]): row
        for row in data["reconciled"][1]
    }

    return {
        "orders": orders,
        "order_items": order_items,
        "invoices": invoices,
        "reconciled": reconciled,
    }


# ============================================================
# 7. ORDER AND ORDER ITEM VALIDATION
# ============================================================

def validate_order_items(data, columns, lookups):

    errors = []

    for row in data["order_items"][1]:

        order_id = get_value(
            row, columns["item_order_id"]
        )

        product_id = get_value(
            row, columns["item_product_id"]
        )

        quantity = get_value(
            row, columns["ordered_quantity"]
        )

        if order_id not in lookups["orders"]:
            errors.append(
                f"Order item references missing order: {order_id}"
            )

        if not product_id:
            errors.append(
                f"Order item has blank product_id: "
                f"{get_value(row, columns['order_item_id'])}"
            )

        try:
            qty = to_decimal(quantity, "ordered_quantity")

            if qty <= 0 or qty != qty.to_integral_value():
                errors.append(
                    f"Invalid ordered quantity for order item "
                    f"{get_value(row, columns['order_item_id'])}"
                )

        except ValueError as error:
            errors.append(str(error))

    return errors


# ============================================================
# 8. INVOICE VALIDATION
# ============================================================

def validate_invoices(data, columns, lookups):

    errors = []

    for row in data["invoices"][1]:

        invoice_id = get_value(
            row, columns["invoice_id"]
        )

        order_id = get_value(
            row, columns["invoice_order_id"]
        )

        status = get_value(
            row, columns["invoice_status"]
        )

        if order_id not in lookups["orders"]:
            errors.append(
                f"Invoice {invoice_id} references missing order "
                f"{order_id}"
            )

        if status not in VALID_INVOICE_STATUSES:
            errors.append(
                f"Invoice {invoice_id} has invalid status: {status}"
            )

        try:
            total = to_decimal(
                get_value(row, columns["invoice_total"]),
                "invoice_total",
            )

            if total < 0:
                errors.append(
                    f"Invoice {invoice_id} has negative total"
                )

        except ValueError as error:
            errors.append(str(error))

    return errors


# ============================================================
# 9. SALES LINE VALIDATION
# ============================================================


def validate_sales(data, columns, lookups):

    errors = []

    for row in data["sales"][1]:

        sales_id = get_value(
            row, columns["sales_id"]
        )

        invoice_id = get_value(
            row, columns["sales_invoice_id"]
        )

        order_item_id = get_value(
            row, columns["sales_item_id"]
        )

        product_id = get_value(
            row, columns["sales_product_id"]
        )

        # ------------------------------------------------
        # 1. Validate invoice relationship
        # ------------------------------------------------

        if invoice_id not in lookups["invoices"]:

            errors.append(
                f"Sales line {sales_id} references missing "
                f"invoice {invoice_id}"
            )

            continue

        # Retrieve invoice BEFORE accessing its columns.
        invoice = lookups["invoices"][invoice_id]

        invoice_order_id = get_value(
            invoice, columns["invoice_order_id"]
        )

        # ------------------------------------------------
        # 2. Validate order item relationship
        # ------------------------------------------------

        if order_item_id not in lookups["order_items"]:

            errors.append(
                f"Sales line {sales_id} references missing "
                f"order item {order_item_id}"
            )

            continue

        order_item = lookups["order_items"][order_item_id]

        item_order_id = get_value(
            order_item, columns["item_order_id"]
        )

        item_product_id = get_value(
            order_item, columns["item_product_id"]
        )

        # ------------------------------------------------
        # 3. Validate order relationship
        # ------------------------------------------------

        if invoice_order_id != item_order_id:

            errors.append(
                f"Sales line {sales_id}: Invoice order ID "
                f"does not match order item order ID"
            )

        # ------------------------------------------------
        # 4. Validate product relationship
        # ------------------------------------------------

        if product_id != item_product_id:

            errors.append(
                f"Sales line {sales_id}: Product ID does "
                f"not match its order item"
            )

        # ------------------------------------------------
        # 5. Validate invoiced quantity
        # ------------------------------------------------

        try:

            quantity = to_decimal(
                get_value(row, columns["sales_quantity"]),
                "sales_quantity",
            )

            if quantity <= 0:

                errors.append(
                    f"Sales line {sales_id}: "
                    f"Quantity must be greater than zero"
                )

            elif quantity != quantity.to_integral_value():

                errors.append(
                    f"Sales line {sales_id}: "
                    f"Quantity must be a whole number"
                )

        except ValueError as error:

            errors.append(str(error))

        # ------------------------------------------------
        # 6. Validate sales line total
        # ------------------------------------------------

        try:

            line_total = to_decimal(
                get_value(row, columns["sales_line_total"]),
                "sales_line_total",
            )

            if line_total < 0:

                errors.append(
                    f"Sales line {sales_id}: "
                    f"Negative line total"
                )

        except ValueError as error:

            errors.append(str(error))

    return errors

# ============================================================
# 10. INVOICED QUANTITY VALIDATION
# ============================================================

def validate_invoiced_quantities(data, columns, lookups):

    errors = []

    invoiced_quantity_by_item = defaultdict(Decimal)

    fulfilled_quantity_by_order = defaultdict(Decimal)

    for row in data["sales"][1]:

        invoice_id = get_value(
            row, columns["sales_invoice_id"]
        )

        order_item_id = get_value(
            row, columns["sales_item_id"]
        )

        invoice = lookups["invoices"] [invoice_id]

        order_id = get_value(
            invoice, columns["invoice_order_id"]
        )

        if (
            invoice_id not in lookups["invoices"]
            or order_item_id not in lookups["order_items"]
        ):
            continue

        invoice = lookups["invoices"][invoice_id]

        status = get_value(
            invoice, columns["invoice_status"]
        )

        try:
            quantity = to_decimal(
                get_value(row, columns["sales_quantity"]),
                "sales_quantity",
            )
        except ValueError:
            continue

        # Only ISSUED invoices count toward fulfillment.
        if status == "ISSUED":

            invoiced_quantity_by_item[order_item_id] += quantity

            fulfilled_quantity_by_order[order_id] += quantity

    # Compare total ISSUED invoice quantities against ordered quantities.
    for order_item_id, order_item in lookups["order_items"].items():

        try:
            ordered_quantity = to_decimal(
                get_value(order_item, columns["ordered_quantity"]),
                "ordered_quantity",
            )
        except ValueError:
            continue

        invoiced_quantity = invoiced_quantity_by_item[
            order_item_id
        ]

        if invoiced_quantity > ordered_quantity:

            errors.append(
                f"Order item {order_item_id}: "
                f"Issued invoice quantity {invoiced_quantity} "
                f"exceeds ordered quantity {ordered_quantity}"
            )

    # Cancelled orders must not have issued invoice quantities.
    for order_id, order in lookups["orders"].items():

        original_status = get_value(
            order, columns["order_id"]
        )

        # The original order status is read from the reconciled
        # file below, where it is explicitly preserved.
        reconciled = lookups["reconciled"].get(order_id)

        if reconciled is None:
            continue

        status = get_value(
            reconciled, columns["original_status"]
        )

        if (
            status == "CANCELLED"
            and fulfilled_quantity_by_order[order_id] > 0
        ):
            errors.append(
                f"Cancelled order {order_id} has issued "
                f"invoice quantities"
            )

    return errors, fulfilled_quantity_by_order


# ============================================================
# 11. INVOICE TOTAL VS SALES LINE TOTAL
# ============================================================

def validate_invoice_totals(data, columns, lookups):

    errors = []

    sales_total_by_invoice = defaultdict(Decimal)

    for row in data["sales"][1]:

        invoice_id = get_value(
            row, columns["sales_invoice_id"]
        )

        if invoice_id not in lookups["invoices"]:
            continue

        try:
            line_total = to_decimal(
                get_value(row, columns["sales_line_total"]),
                "sales_line_total",
            )

            sales_total_by_invoice[invoice_id] += line_total

        except ValueError as error:
            errors.append(str(error))

    for invoice_id, invoice in lookups["invoices"].items():

        try:
            invoice_total = to_decimal(
                get_value(invoice, columns["invoice_total"]),
                "invoice_total",
            )

        except ValueError as error:
            errors.append(str(error))
            continue

        sales_total = sales_total_by_invoice[invoice_id]

        if abs(invoice_total - sales_total) > TOLERANCE:

            errors.append(
                f"Invoice {invoice_id}: Header total "
                f"{invoice_total} does not match sales-line total "
                f"{sales_total}"
            )

    return errors


# ============================================================
# 12. RECONCILED ORDER VALIDATION
# ============================================================

def validate_reconciled_orders(
    data,
    columns,
    lookups,
    fulfilled_quantity_by_order,
):

    errors = []

    order_quantity_by_order = defaultdict(Decimal)

    for row in data["order_items"][1]:

        order_id = get_value(
            row, columns["item_order_id"]
        )

        try:
            quantity = to_decimal(
                get_value(row, columns["ordered_quantity"]),
                "ordered_quantity",
            )

            order_quantity_by_order[order_id] += quantity

        except ValueError as error:
            errors.append(str(error))

    original_order_ids = set(lookups["orders"])
    reconciled_order_ids = set(lookups["reconciled"])

    if original_order_ids != reconciled_order_ids:

        errors.append(
            "Original orders and reconciled orders "
            "do not contain identical order IDs"
        )

    for order_id, reconciled in lookups["reconciled"].items():

        ordered_from_items = order_quantity_by_order[order_id]

        fulfilled_from_sales = fulfilled_quantity_by_order[order_id]

        try:
            reconciled_ordered = to_decimal(
                get_value(
                    reconciled,
                    columns["reconciled_ordered_qty"],
                ),
                "reconciled ordered quantity",
            )

            reconciled_fulfilled = to_decimal(
                get_value(
                    reconciled,
                    columns["reconciled_fulfilled_qty"],
                ),
                "reconciled fulfilled quantity",
            )

            reconciled_remaining = to_decimal(
                get_value(
                    reconciled,
                    columns["reconciled_remaining_qty"],
                ),
                "reconciled remaining quantity",
            )

        except ValueError as error:
            errors.append(
                f"{order_id}: {error}"
            )
            continue

        if reconciled_ordered != ordered_from_items:

            errors.append(
                f"{order_id}: Reconciled ordered quantity "
                f"{reconciled_ordered} does not match order items "
                f"{ordered_from_items}"
            )

        if reconciled_fulfilled != fulfilled_from_sales:

            errors.append(
                f"{order_id}: Reconciled fulfilled quantity "
                f"{reconciled_fulfilled} does not match "
                f"ISSUED sales quantity {fulfilled_from_sales}"
            )

        if (
            reconciled_ordered
            != reconciled_fulfilled + reconciled_remaining
        ):

            errors.append(
                f"{order_id}: Ordered quantity does not equal "
                "fulfilled plus remaining"
            )

        original_status = get_value(
            reconciled, columns["original_status"]
        )

        reconciled_status = get_value(
            reconciled, columns["reconciled_status"]
        )

        if original_status == "CANCELLED":

            expected_status = "CANCELLED"

        elif original_status == "CONFIRMED":

            if fulfilled_from_sales == 0:
                expected_status = "CONFIRMED"

            elif fulfilled_from_sales < ordered_from_items:
                expected_status = "PARTIALLY_FULFILLED"

            elif fulfilled_from_sales == ordered_from_items:
                expected_status = "FULFILLED"

            else:
                continue

        else:

            errors.append(
                f"{order_id}: Unexpected original order status "
                f"{original_status}"
            )
            continue

        if reconciled_status != expected_status:

            errors.append(
                f"{order_id}: Expected status {expected_status}, "
                f"found {reconciled_status}"
            )

    return errors


# ============================================================
# 13. MAIN EXECUTION
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("TRANSACTION INTEGRITY VALIDATION STARTED")
    print("=" * 70)

    data = load_transaction_data()

    columns = resolve_all_columns(data)

    lookups = build_lookups(data, columns)

    results = {}

    results["Primary key validation"] = (
        validate_primary_keys(data, columns)
    )

    results["Order item validation"] = (
        validate_order_items(data, columns, lookups)
    )

    results["Invoice validation"] = (
        validate_invoices(data, columns, lookups)
    )

    results["Sales line validation"] = (
        validate_sales(data, columns, lookups)
    )

    quantity_errors, fulfilled_quantity_by_order = (
        validate_invoiced_quantities(
            data,
            columns,
            lookups,
        )
    )

    results["Invoiced quantity validation"] = quantity_errors

    results["Invoice total validation"] = (
        validate_invoice_totals(data, columns, lookups)
    )

    results["Reconciled order validation"] = (
        validate_reconciled_orders(
            data,
            columns,
            lookups,
            fulfilled_quantity_by_order,
        )
    )

    print("\n" + "=" * 70)
    print("TRANSACTION VALIDATION RESULTS")
    print("=" * 70)

    all_passed = True

    for check_name, errors in results.items():

        if errors:

            all_passed = False

            print(
                f"FAIL: {check_name} "
                f"({len(errors)} errors)"
            )

            for error in errors[:10]:
                print(f"  - {error}")

            if len(errors) > 10:
                print(
                    f"  ... and {len(errors) - 10} more errors"
                )

        else:

            print(f"PASS: {check_name}")

    print("\n" + "=" * 70)

    print(
        f"Total orders: {len(data['orders'][1])}"
    )

    print(
        f"Total order items: {len(data['order_items'][1])}"
    )

    print(
        f"Total invoices: {len(data['invoices'][1])}"
    )

    print(
        f"Total sales lines: {len(data['sales'][1])}"
    )

    issued_invoices = sum(
        1
        for row in data["invoices"][1]
        if get_value(row, columns["invoice_status"]) == "ISSUED"
    )

    void_invoices = sum(
        1
        for row in data["invoices"][1]
        if get_value(row, columns["invoice_status"]) == "VOID"
    )

    print(f"ISSUED invoices: {issued_invoices}")
    print(f"VOID invoices: {void_invoices}")

    print("\n" + "=" * 70)

    if all_passed:

        print("PASS: Transaction integrity validation successful.")

    else:

        print("FAIL: Transaction integrity validation found errors.")

    print("=" * 70)


if __name__ == "__main__":
    main()
