
import argparse
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from scripts.validation.master_validation_config import (
    MASTER_DATA_DIR,
    MASTER_FILES,
)


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_ORDERS_FILE = (
    "data/generated/transactions/orders/"
    "orders_20261118_120729_181778.csv"
)

MAX_ERROR_EXAMPLES = 10


# ============================================================
# FILE LOADING
# ============================================================

def load_json_records(file_path: Path) -> list:
    """Load a JSON master dataset and ensure it contains a list."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Master dataset not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(
            f"Expected a list of records in {file_path}"
        )

    return records


def load_orders(file_path: Path) -> list:
    """Load generated orders from CSV."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Orders CSV not found: {file_path}"
        )

    with file_path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_master_datasets() -> dict:
    """Load the exact approved master-data files."""

    master_directory = PROJECT_ROOT / MASTER_DATA_DIR

    datasets = {}

    required_masters = [
        "retailers",
        "distributors",
        "sales_channels",
        "distributor_retailer_mappings",
    ]

    for master_name in required_masters:

        if master_name not in MASTER_FILES:
            raise KeyError(
                f"{master_name} is missing from MASTER_FILES"
            )

        file_path = (
            master_directory / MASTER_FILES[master_name]
        )

        datasets[master_name] = load_json_records(file_path)

        print(
            f"Loaded {master_name}: "
            f"{len(datasets[master_name]):,} records"
        )

    return datasets


# ============================================================
# DATA NORMALIZATION
# ============================================================

def normalize_id(value):
    """Normalize numeric IDs from CSV and JSON."""

    if value is None or str(value).strip() == "":
        return None

    try:
        numeric_value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid ID value: {value!r}")

    return str(numeric_value)


def parse_date(value, field_name: str) -> date:
    """Convert an ISO date string to datetime.date."""

    try:
        return date.fromisoformat(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError(
            f"Invalid {field_name}: {value!r}"
        )


# ============================================================
# ERROR REPORTING
# ============================================================

def add_error(errors: dict, category: str, message: str):
    errors[category].append(message)


def print_error_summary(errors: dict):
    """Print validation failures with a limited number of examples."""

    total_errors = sum(len(items) for items in errors.values())

    for category, messages in errors.items():

        if not messages:
            continue

        print(f"\nFAIL: {category} ({len(messages)} errors)")

        for message in messages[:MAX_ERROR_EXAMPLES]:
            print(f"  - {message}")

        remaining = len(messages) - MAX_ERROR_EXAMPLES

        if remaining > 0:
            print(f"  ... and {remaining} more")

    return total_errors


# ============================================================
# MASTER ID VALIDATION
# ============================================================

def build_master_id_sets(datasets: dict) -> dict:
    """Build lookup sets for master primary keys."""

    master_id_fields = {
        "retailers": "retailer_id",
        "distributors": "distributor_id",
        "sales_channels": "sales_channel_id",
    }

    master_ids = {}

    for dataset_name, id_field in master_id_fields.items():

        ids = []

        for record in datasets[dataset_name]:

            if id_field not in record:
                raise KeyError(
                    f"{id_field} missing in {dataset_name}"
                )

            ids.append(normalize_id(record[id_field]))

        if None in ids:
            raise ValueError(
                f"Null primary key found in {dataset_name}"
            )

        if len(ids) != len(set(ids)):
            raise ValueError(
                f"Duplicate primary keys found in {dataset_name}"
            )

        master_ids[dataset_name] = set(ids)

    return master_ids


# ============================================================
# MAPPING MASTER VALIDATION
# ============================================================

def validate_mapping_master(
    mappings: list,
    master_ids: dict,
    errors: dict,
) -> dict:
    """
    Validate mapping foreign keys, date periods,
    duplicate mapping IDs, and overlapping assignments.
    """

    mappings_by_retailer = defaultdict(list)
    mapping_ids = set()

    for row_number, mapping in enumerate(mappings, start=1):

        mapping_id = normalize_id(mapping.get("mapping_id"))
        retailer_id = normalize_id(mapping.get("retailer_id"))
        distributor_id = normalize_id(
            mapping.get("distributor_id")
        )

        if mapping_id is None:
            add_error(
                errors,
                "Mapping master primary keys",
                f"Row {row_number}: missing mapping_id",
            )

        elif mapping_id in mapping_ids:
            add_error(
                errors,
                "Mapping master primary keys",
                f"Row {row_number}: duplicate mapping_id "
                f"{mapping_id}",
            )

        else:
            mapping_ids.add(mapping_id)

        if retailer_id not in master_ids["retailers"]:
            add_error(
                errors,
                "Mapping retailer foreign keys",
                f"Row {row_number}: invalid retailer_id "
                f"{retailer_id}",
            )

        if distributor_id not in master_ids["distributors"]:
            add_error(
                errors,
                "Mapping distributor foreign keys",
                f"Row {row_number}: invalid distributor_id "
                f"{distributor_id}",
            )

        try:
            start_date = parse_date(
                mapping.get("effective_start_date"),
                "effective_start_date",
            )

            end_date = parse_date(
                mapping.get("effective_end_date"),
                "effective_end_date",
            )

        except ValueError as exc:
            add_error(
                errors,
                "Mapping effective dates",
                f"Row {row_number}: {exc}",
            )
            continue

        if start_date > end_date:
            add_error(
                errors,
                "Mapping effective dates",
                f"Row {row_number}: start date is after end date",
            )
            continue

        if (
            retailer_id in master_ids["retailers"]
            and distributor_id in master_ids["distributors"]
        ):
            mappings_by_retailer[retailer_id].append({
                "mapping_id": mapping_id,
                "retailer_id": retailer_id,
                "distributor_id": distributor_id,
                "effective_start_date": start_date,
                "effective_end_date": end_date,
            })

    # Check for overlapping assignments per retailer.
    for retailer_id, retailer_mappings in mappings_by_retailer.items():

        sorted_mappings = sorted(
            retailer_mappings,
            key=lambda item: item["effective_start_date"],
        )

        max_end_date = None
        max_end_mapping_id = None

        for mapping in sorted_mappings:

            start_date = mapping["effective_start_date"]
            end_date = mapping["effective_end_date"]

            if (
                max_end_date is not None
                and start_date <= max_end_date
            ):
                add_error(
                    errors,
                    "Overlapping retailer assignments",
                    (
                        f"Retailer {retailer_id}: mapping "
                        f"{mapping['mapping_id']} overlaps mapping "
                        f"{max_end_mapping_id}"
                    ),
                )

            if (
                max_end_date is None
                or end_date > max_end_date
            ):
                max_end_date = end_date
                max_end_mapping_id = mapping["mapping_id"]

    return mappings_by_retailer


# ============================================================
# ORDER FOREIGN KEY VALIDATION
# ============================================================

def validate_order_foreign_keys(
    orders: list,
    master_ids: dict,
    errors: dict,
):
    """Check that all order foreign keys exist in master datasets."""

    foreign_key_rules = {
        "retailer_id": "retailers",
        "distributor_id": "distributors",
        "sales_channel_id": "sales_channels",
    }

    for row_number, order in enumerate(orders, start=1):

        for order_field, master_name in foreign_key_rules.items():

            order_id = order.get("order_id")

            try:
                foreign_key = normalize_id(
                    order.get(order_field)
                )
            except ValueError as exc:
                add_error(
                    errors,
                    f"Order {order_field} foreign keys",
                    f"Order {order_id}, row {row_number}: {exc}",
                )
                continue

            if foreign_key is None:
                add_error(
                    errors,
                    f"Order {order_field} foreign keys",
                    f"Order {order_id}: missing {order_field}",
                )

            elif foreign_key not in master_ids[master_name]:
                add_error(
                    errors,
                    f"Order {order_field} foreign keys",
                    (
                        f"Order {order_id}: {order_field} "
                        f"{foreign_key} does not exist"
                    ),
                )


# ============================================================
# TEMPORAL MAPPING VALIDATION
# ============================================================

def validate_order_mapping(
    orders: list,
    mappings_by_retailer: dict,
    errors: dict,
):
    """
    Ensure exactly one mapping is active for the retailer
    on the order date and its distributor matches the order.
    """

    for row_number, order in enumerate(orders, start=1):

        order_id = order.get("order_id")

        try:
            retailer_id = normalize_id(order.get("retailer_id"))
            distributor_id = normalize_id(
                order.get("distributor_id")
            )

            order_date = parse_date(
                order.get("order_date"),
                "order_date",
            )

        except ValueError as exc:
            add_error(
                errors,
                "Order temporal mapping",
                f"Order {order_id}, row {row_number}: {exc}",
            )
            continue

        if retailer_id is None or distributor_id is None:
            continue

        retailer_mappings = mappings_by_retailer.get(
            retailer_id, []
        )

        active_mappings = [
            mapping
            for mapping in retailer_mappings
            if (
                mapping["effective_start_date"]
                <= order_date
                <= mapping["effective_end_date"]
            )
        ]

        if len(active_mappings) == 0:
            add_error(
                errors,
                "Order temporal mapping",
                (
                    f"Order {order_id}: no active distributor "
                    f"mapping for retailer {retailer_id} "
                    f"on {order_date}"
                ),
            )

        elif len(active_mappings) > 1:
            add_error(
                errors,
                "Order temporal mapping",
                (
                    f"Order {order_id}: multiple active mappings "
                    f"for retailer {retailer_id} on {order_date}"
                ),
            )

        else:
            active_mapping = active_mappings[0]

            if active_mapping["distributor_id"] != distributor_id:
                add_error(
                    errors,
                    "Order temporal mapping",
                    (
                        f"Order {order_id}: distributor_id "
                        f"{distributor_id} does not match active "
                        f"mapping distributor_id "
                        f"{active_mapping['distributor_id']} "
                        f"for retailer {retailer_id}"
                    ),
                )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Validate order foreign keys and "
            "temporal distributor-retailer mappings."
        )
    )

    parser.add_argument(
        "--orders-file",
        default=DEFAULT_ORDERS_FILE,
        help="Path to the generated orders CSV.",
    )

    args = parser.parse_args()

    orders_path = PROJECT_ROOT / args.orders_file

    print("=" * 65)
    print("ORDER MASTER-DATA INTEGRITY VALIDATION STARTED")
    print("=" * 65)

    errors = defaultdict(list)

    # 1. Load orders
    orders = load_orders(orders_path)

    if not orders:
        raise ValueError("Orders CSV contains no records.")

    print(f"\nLoaded orders: {len(orders):,}")

    # 2. Load approved master datasets
    datasets = load_master_datasets()

    # 3. Build primary-key lookup sets
    master_ids = build_master_id_sets(datasets)

    # 4. Validate mapping master
    mappings_by_retailer = validate_mapping_master(
        datasets["distributor_retailer_mappings"],
        master_ids,
        errors,
    )

    # 5. Validate order foreign keys
    validate_order_foreign_keys(
        orders,
        master_ids,
        errors,
    )

    # 6. Validate temporal mapping
    validate_order_mapping(
        orders,
        mappings_by_retailer,
        errors,
    )

    # 7. Print final report
    print("\n" + "=" * 65)
    print("VALIDATION SUMMARY")
    print("=" * 65)

    print(f"Orders checked: {len(orders):,}")

    total_errors = print_error_summary(errors)

    if total_errors == 0:

        print("\nPASS: All master-data integrity checks passed.")
        print("PASS: All temporal mapping checks passed.")
        print("\nORDER MASTER-DATA VALIDATION SUCCESSFUL.")

    else:

        print(f"\nFAIL: Total validation errors: {total_errors}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
