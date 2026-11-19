
import argparse
import csv
import json
import sys

from collections import Counter
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from scripts.common.transaction_config import (
    MIN_ORDER_QUANTITY,
    MAX_ORDER_QUANTITY,
    MIN_PRODUCTS_PER_ORDER,
    MAX_PRODUCTS_PER_ORDER,
    MIN_DISCOUNT_PCT,
    MAX_DISCOUNT_PCT,
    ORDER_ITEM_ID_PREFIX,
    TRANSACTION_OUTPUT_DIR,
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

PRODUCTS_FILE = (
    PROJECT_ROOT
    / MASTER_DATA_DIR
    / MASTER_FILES["products"]
)

MONEY_PRECISION = Decimal("0.01")


# ---------------------------------------------------------
# LOAD CSV
# ---------------------------------------------------------

def load_csv(file_path: Path, required_columns: set) -> list:

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

    if not isinstance(products, list):
        raise ValueError(
            "Product master must contain a JSON list."
        )

    product_lookup = {}

    for product in products:

        product_id = str(product.get("product_id", "")).strip()

        if not product_id:
            raise ValueError(
                "Product master contains a blank product_id."
            )

        if product_id in product_lookup:
            raise ValueError(
                f"Duplicate product_id: {product_id}"
            )

        try:
            mrp = Decimal(str(product["mrp"])).quantize(
                MONEY_PRECISION,
                rounding=ROUND_HALF_UP,
            )
        except (KeyError, InvalidOperation, ValueError):
            raise ValueError(
                f"Invalid MRP for product: {product_id}"
            )

        if not mrp.is_finite() or mrp <= 0:
            raise ValueError(
                f"MRP must be positive: {product_id}"
            )

        product_lookup[product_id] = {
            "mrp": mrp
        }

    return product_lookup


# ---------------------------------------------------------
# VALIDATE ORDER MASTER
# ---------------------------------------------------------

def validate_orders(orders: list) -> dict:

    order_lookup = {}
    errors = []

    for order in orders:

        order_id = order["order_id"]

        if not order_id:
            errors.append("Blank order_id found.")
            continue

        if order_id in order_lookup:
            errors.append(
                f"Duplicate order_id: {order_id}"
            )
            continue

        if not order["created_at"]:
            errors.append(
                f"Missing created_at for order: {order_id}"
            )

        order_lookup[order_id] = {
            "created_at": order["created_at"]
        }

    if errors:
        raise ValueError(
            "Invalid orders source data: "
            + "; ".join(errors[:10])
        )

    return order_lookup


# ---------------------------------------------------------
# VALIDATE ORDER ITEMS
# ---------------------------------------------------------

def validate_order_items(
    orders: list,
    order_items: list,
    products: dict,
) -> dict:

    errors = []

    order_lookup = validate_orders(orders)

    valid_product_ids = set(products.keys())

    seen_item_ids = set()
    seen_order_products = set()

    order_item_counts = Counter()

    total_quantity = 0
    gross_value = Decimal("0.00")
    discount_value = Decimal("0.00")
    net_requested_value = Decimal("0.00")

    for row_number, item in enumerate(order_items, start=2):

        item_id = item["order_item_id"]
        order_id = item["order_id"]
        product_id = item["product_id"]

        # ---------------------------------------------
        # 1. Primary key validation
        # ---------------------------------------------

        if not item_id:
            errors.append(
                f"Row {row_number}: blank order_item_id."
            )

        elif item_id in seen_item_ids:
            errors.append(
                f"Row {row_number}: duplicate order_item_id {item_id}."
            )

        else:
            seen_item_ids.add(item_id)

        if not item_id.startswith(ORDER_ITEM_ID_PREFIX):
            errors.append(
                f"Row {row_number}: invalid order_item_id prefix."
            )

        # ---------------------------------------------
        # 2. Order foreign key validation
        # ---------------------------------------------

        if order_id not in order_lookup:
            errors.append(
                f"Row {row_number}: invalid order_id {order_id}."
            )
            continue

        order_item_counts[order_id] += 1

        # ---------------------------------------------
        # 3. Product foreign key validation
        # ---------------------------------------------

        if product_id not in valid_product_ids:
            errors.append(
                f"Row {row_number}: invalid product_id {product_id}."
            )
            continue

        # ---------------------------------------------
        # 4. Unique order_id + product_id
        # ---------------------------------------------

        combination = (order_id, product_id)

        if combination in seen_order_products:
            errors.append(
                f"Row {row_number}: product {product_id} "
                f"appears more than once in order {order_id}."
            )

        seen_order_products.add(combination)

        # ---------------------------------------------
        # 5. Quantity validation
        # ---------------------------------------------

        try:
            quantity = int(item["ordered_quantity"])

            if str(quantity) != item["ordered_quantity"].strip():
                raise ValueError

            if not (
                MIN_ORDER_QUANTITY
                <= quantity
                <= MAX_ORDER_QUANTITY
            ):
                errors.append(
                    f"Row {row_number}: quantity outside "
                    f"allowed range for {item_id}."
                )
            else:
                total_quantity += quantity

        except (TypeError, ValueError):
            errors.append(
                f"Row {row_number}: invalid integer quantity "
                f"for {item_id}."
            )
            continue

        # ---------------------------------------------
        # 6. Unit price validation against MRP
        # ---------------------------------------------

        try:
            unit_price = Decimal(
                item["requested_unit_price"]
            ).quantize(
                MONEY_PRECISION,
                rounding=ROUND_HALF_UP,
            )

            expected_mrp = products[product_id]["mrp"]

            if not unit_price.is_finite() or unit_price <= 0:
                errors.append(
                    f"Row {row_number}: invalid unit price "
                    f"for {item_id}."
                )

            elif unit_price != expected_mrp:
                errors.append(
                    f"Row {row_number}: unit price does not "
                    f"match product MRP for {item_id}."
                )

        except (InvalidOperation, TypeError, ValueError):
            errors.append(
                f"Row {row_number}: invalid unit price "
                f"for {item_id}."
            )
            continue

        # ---------------------------------------------
        # 7. Discount validation
        # ---------------------------------------------

        try:
            discount_pct = Decimal(
                item["requested_discount_pct"]
            )

            if not discount_pct.is_finite():
                raise InvalidOperation

            if not (
                Decimal(str(MIN_DISCOUNT_PCT))
                <= discount_pct
                <= Decimal(str(MAX_DISCOUNT_PCT))
            ):
                errors.append(
                    f"Row {row_number}: discount outside "
                    f"allowed range for {item_id}."
                )
                continue

        except (InvalidOperation, TypeError, ValueError):
            errors.append(
                f"Row {row_number}: invalid discount "
                f"for {item_id}."
            )
            continue

        # ---------------------------------------------
        # 8. created_at consistency
        # ---------------------------------------------

        expected_created_at = order_lookup[order_id]["created_at"]

        if item["created_at"] != expected_created_at:
            errors.append(
                f"Row {row_number}: created_at does not match "
                f"parent order for {item_id}."
            )

        # ---------------------------------------------
        # 9. Recalculate expected line values
        # ---------------------------------------------

        line_gross = (
            Decimal(quantity) * unit_price
        ).quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )

        line_discount = (
            line_gross * discount_pct / Decimal("100")
        ).quantize(
            MONEY_PRECISION,
            rounding=ROUND_HALF_UP,
        )

        line_net = line_gross - line_discount

        gross_value += line_gross
        discount_value += line_discount
        net_requested_value += line_net

    # ---------------------------------------------
    # 10. Every order must have 1–5 items
    # ---------------------------------------------

    for order_id in order_lookup:

        item_count = order_item_counts.get(order_id, 0)

        if not (
            MIN_PRODUCTS_PER_ORDER
            <= item_count
            <= MAX_PRODUCTS_PER_ORDER
        ):
            errors.append(
                f"Order {order_id} has {item_count} items. "
                f"Expected {MIN_PRODUCTS_PER_ORDER}–"
                f"{MAX_PRODUCTS_PER_ORDER}."
            )

    if errors:

        print("\nORDER ITEM VALIDATION FAILED")
        print(f"Total errors: {len(errors)}")

        for error in errors[:30]:
            print(f"ERROR: {error}")

        if len(errors) > 30:
            print(
                f"... and {len(errors) - 30} more errors."
            )

        return {
            "passed": False,
            "errors": errors,
        }

    return {
        "passed": True,
        "errors": [],
        "order_count": len(order_lookup),
        "order_item_count": len(order_items),
        "product_count": len(products),
        "total_quantity": total_quantity,
        "gross_value": gross_value,
        "discount_value": discount_value,
        "net_requested_value": net_requested_value,
        "item_counts": order_item_counts,
    }


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Validate generated order items."
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

    args = parser.parse_args()

    print("=" * 65)
    print("ORDER ITEM INDEPENDENT VALIDATION STARTED")
    print("=" * 65)

    required_order_columns = {
        "order_id",
        "created_at",
    }

    required_item_columns = {
        "order_item_id",
        "order_id",
        "product_id",
        "ordered_quantity",
        "requested_unit_price",
        "requested_discount_pct",
        "created_at",
    }

    orders = load_csv(
        args.orders_file,
        required_order_columns,
    )

    order_items = load_csv(
        args.order_items_file,
        required_item_columns,
    )

    products = load_products(PRODUCTS_FILE)

    print(f"Loaded orders: {len(orders):,}")
    print(f"Loaded order items: {len(order_items):,}")
    print(f"Loaded products: {len(products):,}")

    result = validate_order_items(
        orders=orders,
        order_items=order_items,
        products=products,
    )

    print("\n" + "=" * 65)
    print("VALIDATION SUMMARY")
    print("=" * 65)

    if not result["passed"]:
        print(f"FAILED: {len(result['errors'])} error(s).")
        print("ORDER ITEM VALIDATION FAILED.")
        sys.exit(1)

    print(f"Orders checked: {result['order_count']:,}")
    print(f"Order items checked: {result['order_item_count']:,}")
    print(f"Products checked: {result['product_count']:,}")
    print(f"Total units ordered: {result['total_quantity']:,}")

    print(
        "Gross requested value: "
        f"INR {result['gross_value']:,.2f}"
    )

    print(
        "Requested discount: "
        f"INR {result['discount_value']:,.2f}"
    )

    print(
        "Net requested value before tax: "
        f"INR {result['net_requested_value']:,.2f}"
    )

    counts = list(result["item_counts"].values())

    print(
        f"Minimum items per order: {min(counts)}"
    )

    print(
        f"Maximum items per order: {max(counts)}"
    )

    print("\nPASS: All independent order item checks passed.")
    print("ORDER ITEM VALIDATION SUCCESSFUL.")

    print("=" * 65)


if __name__ == "__main__":
    main()
