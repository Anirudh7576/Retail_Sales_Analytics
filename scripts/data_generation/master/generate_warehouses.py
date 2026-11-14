
from scripts.common.master_data import WAREHOUSE_MASTER
from scripts.common.constants import WAREHOUSE_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique,
    check_foreign_keys
)
from scripts.common.file_utils import save_json, get_latest_json
from scripts.common.logger import logger


def generate_warehouses() -> list:
    warehouse_records = []

    for warehouse_id, warehouse in enumerate(
        WAREHOUSE_MASTER, start=1
    ):
        warehouse_record = {
            "warehouse_id": warehouse_id,
            **warehouse
        }

        warehouse_records.append(warehouse_record)

    return warehouse_records


def validate_warehouses(
    warehouses: list,
    geography: list
) -> None:

    # Validate required fields
    check_required_fields(
        warehouses,
        WAREHOUSE_REQUIRED_FIELDS
    )

    # Validate unique warehouse IDs
    check_unique(warehouses, "warehouse_id")

    # Validate unique warehouse names
    check_unique(warehouses, "warehouse_name")

    # Validate geography foreign keys
    check_foreign_keys(
        warehouses,
        "geography_id",
        geography,
        "geography_id"
    )


def main():
    try:
        logger.info("Warehouse generation started.")

        # Load geography master data
        geography = get_latest_json(
            "master/geography",
            "geography"
        )

        warehouses = generate_warehouses()

        logger.info(
            "Generated %s warehouse records.",
            len(warehouses)
        )

        # Validate warehouse records
        validate_warehouses(
            warehouses,
            geography
        )

        logger.info("Warehouse validation successful.")

        # Save warehouse master data
        save_json(
            warehouses,
            "warehouses",
            "generated",
            "master"
        )

        logger.info(
            "Warehouse generation completed successfully."
        )

    except Exception:
        logger.exception("Warehouse generation failed.")
        raise


if __name__ == "__main__":
    main()
