
import argparse
import csv
import json
import random

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from scripts.common.transaction_config import (
    RANDOM_SEED,
    ORDER_ITEM_ID_PREFIX,
    MIN_ORDER_QUANTITY,
    MAX_ORDER_QUANTITY,
    MIN_PRODUCTS_PER_ORDER,
    MAX_PRODUCTS_PER_ORDER,
    MIN_DISCOUNT_PCT,
    MAX_DISCOUNT_PCT,
    TRANSACTION_OUTPUT_DIR,
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

PRODUCTS_FILE = (
    PROJECT_ROOT
    / MASTER_DATA_DIR
    / MASTER_FILES["products"]
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "order_items"
)

MONEY_PRECISION = Decimal("0.01")

DISCOUNT_OPTIONS = [
    Decimal("0.00"),
    Decimal("2.50"),
    Decimal("5.00"),
    Decimal("7.50"),
    Decimal("10.00"),
    Decimal("12.50"),
    Decimal("15.00"),
    Decimal("20.00"),
]


# ---------------------------------------------------------
# LOAD ORDERS
# ---------------------------------------------------------

def load_orders(file_path: Path) -> list:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Orders file not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "order_id",
            "created_at",
        }

        missing_columns = required_columns - set(
            reader.fieldnames or []
        )

        if missing_columns:
            raise ValueError(
                f"Missing order columns: {missing_columns}"
            )

        orders = list(reader)

    if not orders:
        raise ValueError("Orders file contains no records.")

    order_ids = [order["order_id"] for order in orders]

    if len(order_ids) != len(set(order_ids)):
        raise ValueError("Duplicate order_id found in orders file.")

    for order in orders:
        if not order["order_id"]:
            raise ValueError("Blank order_id found.")

        if not order["created_at"]:
            raise ValueError(
                f"Missing created_at for order {order['order_id']}"
            )

    return orders


# ---------------------------------------------------------
# LOAD PRODUCTS
# ---------------------------------------------------------

def load_products(file_path: Path) -> dict:

    if not file_path.exists():
        raise FileNotFoundError(
            f"Products master file not found: {file_path}"
        )

    with open(
        file_path,
        mode="r",
        encoding="utf-8",
    ) as file:

        products = json.load(file)

    if not isinstance(products, list) or not products:
        raise ValueError(
            "Products master must contain a non-empty JSON list."
        )

    product_lookup = {}

    for product in products:

        product_id = product.get("product_id")

        if not product_id:
            raise ValueError("Product record has a blank product_id.")

        if product_id in product_lookup:
            raise ValueError(
                f"Duplicate product_id in master: {product_id}"
            )

        try:
            mrp = Decimal(str(product["mrp"])).quantize(
                MONEY_PRECISION,
                rounding=ROUND_HALF_UP,
            )
        except (KeyError, InvalidOperation, ValueError):
            raise ValueError(
                f"Invalid or missing MRP for product {product_id}"
            )

        if not mrp.is_finite() or mrp <= 0:
            raise ValueError(
                f"MRP must be positive for product {product_id}"
            )

        product_lookup[product_id] = {
            "product_id": product_id,
            "mrp": mrp,
        }

    return product_lookup


# ---------------------------------------------------------
# GENERATE ONE ORDER ITEM
# ---------------------------------------------------------

def generate_order_item(
    item_number: int,
    order: dict,
    product: dict,
    rng: random.Random,
) -> dict:

    quantity = rng.randint(
        MIN_ORDER_QUANTITY,
        MAX_ORDER_QUANTITY,
    )

    discount = rng.choice(DISCOUNT_OPTIONS)

    return {
        "order_item_id": (
            f"{ORDER_ITEM_ID_PREFIX}{item_number:09d}"
        ),
        "order_id": order["order_id"],
        "product_id": product["product_id"],
        "ordered_quantity": quantity,
        "requested_unit_price": str(product["mrp"]),
        "requested_discount_pct": str(discount),
        "created_at": order["created_at"],
    }


# ---------------------------------------------------------
# GENERATE ALL ORDER ITEMS
# ---------------------------------------------------------

def generate_order_items(
    orders: list,
    products: dict,
    rng: random.Random,
) -> list:

    product_list = list(products.values())

    if len(product_list) < MIN_PRODUCTS_PER_ORDER:
        raise ValueError(
            "Insufficient products to generate order items."
        )

    order_items = []
    item_number = 1

    for order in orders:

        number_of_products = rng.randint(
            MIN_PRODUCTS_PER_ORDER,
            min(MAX_PRODUCTS_PER_ORDER, len(product_list)),
        )

        selected_products = rng.sample(
            product_list,
            number_of_products,
        )

        for product in selected_products:

            item = generate_order_item(
                item_number=item_number,
                order=order,
                product=product,
                rng=rng,
            )

            order_items.append(item)
            item_number += 1

    return order_items


# ---------------------------------------------------------
# VALIDATE GENERATED ORDER ITEMS
# ---------------------------------------------------------

def validate_order_items(
    orders: list,
    products: dict,
    order_items: list,
) -> None:

    errors = []

    valid_order_ids = {
        order["order_id"] for order in orders
    }

    valid_product_ids = set(products.keys())

    order_item_ids = set()
    order_product_combinations = set()
    order_item_counts = {}

    for item in order_items:

        item_id = item["order_item_id"]
        order_id = item["order_id"]
        product_id = item["product_id"]

        if item_id in order_item_ids:
            errors.append(
                f"Duplicate order_item_id: {item_id}"
            )

        order_item_ids.add(item_id)

        if order_id not in valid_order_ids:
            errors.append(
                f"Invalid order_id: {order_id}"
            )

        if product_id not in valid_product_ids:
            errors.append(
                f"Invalid product_id: {product_id}"
            )

        combination = (order_id, product_id)

        if combination in order_product_combinations:
            errors.append(
                f"Duplicate product within order: {combination}"
            )

        order_product_combinations.add(combination)

        try:
            quantity = int(item["ordered_quantity"])

            if quantity <= 0:
                errors.append(
                    f"Invalid quantity for {item_id}"
                )

        except (TypeError, ValueError):
            errors.append(
                f"Non-integer quantity for {item_id}"
            )

        try:
            price = Decimal(item["requested_unit_price"])
            discount = Decimal(item["requested_discount_pct"])

            if not price.is_finite() or price <= 0:
                errors.append(
                    f"Invalid unit price for {item_id}"
                )

            if (
                not discount.is_finite()
                or discount < Decimal(str(MIN_DISCOUNT_PCT))
                or discount > Decimal(str(MAX_DISCOUNT_PCT))
            ):
                errors.append(
                    f"Invalid discount for {item_id}"
                )

        except (InvalidOperation, TypeError, ValueError):
            errors.append(
                f"Invalid price or discount for {item_id}"
            )

        order_item_counts[order_id] = (
            order_item_counts.get(order_id, 0) + 1
        )

    # Every order must have at least one item.
    for order_id in valid_order_ids:

        if order_item_counts.get(order_id, 0) < 1:
            errors.append(
                f"Order has no order items: {order_id}"
            )

    if errors:

        print("\nORDER ITEM VALIDATION FAILED")

        for error in errors[:20]:
            print(f"ERROR: {error}")

        raise ValueError(
            f"Validation failed with {len(errors)} error(s)."
        )

    print("Order item validation successful.")


# ---------------------------------------------------------
# SAVE CSV
# ---------------------------------------------------------

def save_order_items(
    order_items: list,
    output_file: Path,
) -> None:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "order_item_id",
        "order_id",
        "product_id",
        "ordered_quantity",
        "requested_unit_price",
        "requested_discount_pct",
        "created_at",
    ]

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
        writer.writerows(order_items)

    print(f"Order items saved: {output_file}")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(
        description="Generate order_items.csv"
    )

    parser.add_argument(
        "--orders-file",
        type=Path,
        default=DEFAULT_ORDERS_FILE,
        help="Path to the source orders CSV.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on the number of orders.",
    )

    args = parser.parse_args()

    print("=" * 65)
    print("ORDER ITEM GENERATION STARTED")
    print("=" * 65)

    if args.limit is not None and args.limit <= 0:
        raise ValueError("--limit must be greater than zero.")

    orders = load_orders(args.orders_file)

    if args.limit is not None:
        orders = orders[:args.limit]

    products = load_products(PRODUCTS_FILE)

    print(f"Loaded orders: {len(orders):,}")
    print(f"Loaded products: {len(products):,}")

    rng = random.Random(RANDOM_SEED + 1)

    order_items = generate_order_items(
        orders=orders,
        products=products,
        rng=rng,
    )

    print(f"Generated order items: {len(order_items):,}")

    validate_order_items(
        orders=orders,
        products=products,
        order_items=order_items,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    output_file = (
        OUTPUT_DIR
        / f"order_items_{timestamp}.csv"
    )

    save_order_items(
        order_items=order_items,
        output_file=output_file,
    )

    print("=" * 65)
    print("ORDER ITEM GENERATION COMPLETED")
    print("=" * 65)


if __name__ == "__main__":
    main()
