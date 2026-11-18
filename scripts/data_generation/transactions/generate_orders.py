
"""
Generate FMCG secondary-sales order headers.

Initial test:
python -m scripts.data_generation.transactions.generate_orders --limit 100

Full generation:
python -m scripts.data_generation.transactions.generate_orders --limit 100000
"""

import argparse
import csv
import random

from datetime import date, datetime, time, timedelta
from pathlib import Path

from scripts.common.file_utils import PROJECT_ROOT
from scripts.common.logger import logger

from scripts.common.transaction_config import (
    TRANSACTION_START_DATE,
    TRANSACTION_END_DATE,
    TARGET_ORDER_COUNT,
    RANDOM_SEED,
    ORDER_ID_PREFIX,
    TRANSACTION_OUTPUT_DIR,
    DEFAULT_ORDER_SAMPLE_SIZE,
    ORDER_CANCELLATION_RATE,
    MIN_DELIVERY_DAYS,
    MAX_DELIVERY_DAYS,
)

from scripts.validation.master_validation_config import (
    MASTER_DATA_DIR,
    MASTER_FILES,
)


OUTPUT_DIR = (
    PROJECT_ROOT
    / TRANSACTION_OUTPUT_DIR
    / "orders"
)

OUTPUT_COLUMNS = [
    "order_id",
    "retailer_id",
    "distributor_id",
    "sales_channel_id",
    "order_date",
    "requested_delivery_date",
    "order_status",
    "created_at",
    "updated_at",
]


def load_master_data(dataset_name: str) -> list:
    """Load a master dataset using its explicitly configured file."""

    relative_path = MASTER_FILES[dataset_name]

    file_path = (
        PROJECT_ROOT
        / MASTER_DATA_DIR
        / relative_path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Master data file not found: {file_path}"
        )

    import json

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError(
            f"Invalid or empty master dataset: {dataset_name}"
        )

    return records


def parse_master_date(value: str) -> date:
    """Convert an ISO date string into datetime.date."""

    if not isinstance(value, str):
        raise ValueError(f"Expected date string, received {value!r}")

    return date.fromisoformat(value[:10])


def load_transaction_dates(date_records: list) -> list:
    """Select valid transaction dates from the date dimension."""

    transaction_dates = []

    for record in date_records:

        if not isinstance(record, dict):
            continue

        transaction_date = parse_master_date(
            record["full_date"]
        )

        if (
            TRANSACTION_START_DATE
            <= transaction_date
            <= TRANSACTION_END_DATE
        ):
            transaction_dates.append(transaction_date)

    transaction_dates = sorted(set(transaction_dates))

    if not transaction_dates:
        raise ValueError(
            "No date-dimension records found in the transaction period."
        )

    expected_days = (
        TRANSACTION_END_DATE - TRANSACTION_START_DATE
    ).days + 1

    if len(transaction_dates) != expected_days:
        raise ValueError(
            f"Date dimension coverage is incomplete. "
            f"Expected {expected_days} dates, "
            f"found {len(transaction_dates)}."
        )

    return transaction_dates


def prepare_mappings(
    mappings: list,
    retailer_ids: set,
    distributor_ids: set
) -> list:
    """Validate and prepare distributor-retailer assignments."""

    prepared = []

    for index, record in enumerate(mappings):

        retailer_id = record["retailer_id"]
        distributor_id = record["distributor_id"]

        if retailer_id not in retailer_ids:
            raise ValueError(
                f"Mapping record {index}: "
                f"Unknown retailer_id {retailer_id}"
            )

        if distributor_id not in distributor_ids:
            raise ValueError(
                f"Mapping record {index}: "
                f"Unknown distributor_id {distributor_id}"
            )

        start_date = parse_master_date(
            record["effective_start_date"]
        )

        end_date = parse_master_date(
            record["effective_end_date"]
        )

        if start_date > end_date:
            raise ValueError(
                f"Mapping record {index}: Invalid effective period."
            )

        prepared.append({
            "retailer_id": retailer_id,
            "distributor_id": distributor_id,
            "effective_start_date": start_date,
            "effective_end_date": end_date,
        })

    return prepared


def get_active_mappings(
    order_date: date,
    mappings: list,
    cache: dict
) -> list:
    """Get assignments valid on a particular order date."""

    if order_date not in cache:

        cache[order_date] = [
            mapping
            for mapping in mappings
            if (
                mapping["effective_start_date"]
                <= order_date
                <= mapping["effective_end_date"]
            )
        ]

    return cache[order_date]


def generate_order_record(
    order_number: int,
    transaction_dates: list,
    active_mappings: list,
    sales_channel_ids: list,
    rng: random.Random
) -> dict:
    """Generate one order header."""

    order_date = rng.choice(transaction_dates)

    order_id = (
        f"{ORDER_ID_PREFIX}-{order_number:06d}"
    )

    mapping = rng.choice(active_mappings)

    sales_channel_id = rng.choice(
        sales_channel_ids
    )

    delivery_days = rng.randint(
        MIN_DELIVERY_DAYS,
        MAX_DELIVERY_DAYS
    )

    requested_delivery_date = (
        order_date + timedelta(days=delivery_days)
    )

    # Keep requested delivery within the configured
    # transaction year for this initial synthetic dataset.
    requested_delivery_date = min(
        requested_delivery_date,
        TRANSACTION_END_DATE
    )

    order_status = (
        "CANCELLED"
        if rng.random() < ORDER_CANCELLATION_RATE
        else "CONFIRMED"
    )

    order_time = time(
        hour=rng.randint(8, 19),
        minute=rng.choice([0, 15, 30, 45]),
        second=rng.randint(0, 59)
    )

    created_at = datetime.combine(
        order_date,
        order_time
    )

    return {
        "order_id": order_id,
        "retailer_id": mapping["retailer_id"],
        "distributor_id": mapping["distributor_id"],
        "sales_channel_id": sales_channel_id,
        "order_date": order_date.isoformat(),
        "requested_delivery_date": (
            requested_delivery_date.isoformat()
        ),
        "order_status": order_status,
        "created_at": created_at.isoformat(
            sep=" ",
            timespec="seconds"
        ),
        "updated_at": created_at.isoformat(
            sep=" ",
            timespec="seconds"
        ),
    }


def validate_orders(
    orders: list,
    retailer_ids: set,
    distributor_ids: set,
    sales_channel_ids: set
) -> bool:
    """Perform initial order-header validations."""

    errors = []

    seen_order_ids = set()

    for index, order in enumerate(orders):

        order_id = order["order_id"]

        if order_id in seen_order_ids:
            errors.append(
                f"Duplicate order_id: {order_id}"
            )

        seen_order_ids.add(order_id)

        if order["retailer_id"] not in retailer_ids:
            errors.append(
                f"Invalid retailer_id in {order_id}"
            )

        if order["distributor_id"] not in distributor_ids:
            errors.append(
                f"Invalid distributor_id in {order_id}"
            )

        if order["sales_channel_id"] not in sales_channel_ids:
            errors.append(
                f"Invalid sales_channel_id in {order_id}"
            )

        order_date = parse_master_date(
            order["order_date"]
        )

        delivery_date = parse_master_date(
            order["requested_delivery_date"]
        )

        if order_date < TRANSACTION_START_DATE:
            errors.append(
                f"Order date before configured period: {order_id}"
            )

        if order_date > TRANSACTION_END_DATE:
            errors.append(
                f"Order date after configured period: {order_id}"
            )

        if delivery_date < order_date:
            errors.append(
                f"Delivery date before order date: {order_id}"
            )

        if order["order_status"] not in {
            "CONFIRMED",
            "CANCELLED",
        }:
            errors.append(
                f"Invalid initial order status: {order_id}"
            )

    if errors:
        for error in errors:
            logger.error(error)

        raise ValueError(
            f"Order validation failed: {len(errors)} errors."
        )

    logger.info(
        f"Order validation successful. Records: {len(orders):,}"
    )

    return True


def save_orders(orders: list) -> Path:
    """Save generated orders to a timestamped CSV."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    output_file = (
        OUTPUT_DIR
        / f"orders_{timestamp}.csv"
    )

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=OUTPUT_COLUMNS
        )

        writer.writeheader()
        writer.writerows(orders)

    logger.info(
        f"Orders saved successfully: {output_file}"
    )

    return output_file


def main():

    parser = argparse.ArgumentParser(
        description="Generate FMCG secondary-sales orders."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_ORDER_SAMPLE_SIZE,
        help="Number of orders to generate."
    )

    args = parser.parse_args()

    if args.limit <= 0:
        parser.error("--limit must be greater than zero.")

    if args.limit > TARGET_ORDER_COUNT:
        parser.error(
            f"--limit cannot exceed {TARGET_ORDER_COUNT:,}."
        )

    logger.info("Order generation started.")

    rng = random.Random(RANDOM_SEED)

    # Load master data.
    retailers = load_master_data("retailers")
    distributors = load_master_data("distributors")
    sales_channels = load_master_data("sales_channels")
    mappings = load_master_data(
        "distributor_retailer_mappings"
    )
    dates = load_master_data("dates")

    retailer_ids = {
        record["retailer_id"]
        for record in retailers
    }

    distributor_ids = {
        record["distributor_id"]
        for record in distributors
    }

    sales_channel_ids = [
        record["sales_channel_id"]
        for record in sales_channels
    ]

    transaction_dates = load_transaction_dates(dates)

    prepared_mappings = prepare_mappings(
        mappings,
        retailer_ids,
        distributor_ids
    )

    logger.info(
        f"Loaded retailers: {len(retailer_ids):,}"
    )

    logger.info(
        f"Loaded distributors: {len(distributor_ids):,}"
    )

    logger.info(
        f"Loaded transaction dates: {len(transaction_dates):,}"
    )

    logger.info(
        f"Loaded distributor-retailer mappings: "
        f"{len(prepared_mappings):,}"
    )

    # Cache active mappings by order date.
    mapping_cache = {}

    orders = []

    for order_number in range(1, args.limit + 1):

        order_date = rng.choice(transaction_dates)

        active_mappings = get_active_mappings(
            order_date,
            prepared_mappings,
            mapping_cache
        )

        if not active_mappings:
            raise ValueError(
                f"No active distributor-retailer mapping "
                f"for {order_date}."
            )

        # Generate the order using the selected date.
        order = generate_order_record(
            order_number=order_number,
            transaction_dates=[order_date],
            active_mappings=active_mappings,
            sales_channel_ids=sales_channel_ids,
            rng=rng
        )

        orders.append(order)

    validate_orders(
        orders,
        retailer_ids,
        distributor_ids,
        set(sales_channel_ids)
    )

    save_orders(orders)

    logger.info(
        f"Order generation completed. "
        f"Records: {len(orders):,}"
    )


if __name__ == "__main__":
    main()
