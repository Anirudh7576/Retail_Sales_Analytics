
from scripts.common.master_data import RETAILER_MASTER
from scripts.common.constants import RETAILER_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique,
    check_foreign_keys
)
from scripts.common.file_utils import save_json, get_latest_json
from scripts.common.logger import logger


def generate_retailers() -> list:
    retailer_records = []

    for retailer_id, retailer in enumerate(
        RETAILER_MASTER, start=1
    ):
        retailer_record = {
            "retailer_id": retailer_id,
            **retailer
        }

        retailer_records.append(retailer_record)

    return retailer_records


def validate_retailers(
    retailers: list,
    geography: list
) -> None:

    # Validate required fields
    check_required_fields(
        retailers,
        RETAILER_REQUIRED_FIELDS
    )

    # Validate unique retailer IDs
    check_unique(retailers, "retailer_id")

    # Validate unique retailer names
    check_unique(retailers, "retailer_name")

    # Validate retailer geography foreign keys
    check_foreign_keys(
        retailers,
        "geography_id",
        geography,
        "geography_id"
    )


def main():
    try:
        logger.info("Retailer generation started.")

        # Load the latest geography master data
        geography = get_latest_json(
            "master/geography",
            "geography"
        )

        retailers = generate_retailers()

        logger.info(
            "Generated %s retailer records.",
            len(retailers)
        )

        # Validate generated records
        validate_retailers(
            retailers,
            geography
        )

        logger.info("Retailer validation successful.")

        # Save retailer master data
        save_json(
            retailers,
            "retailers",
            "generated",
            "master"
        )

        logger.info(
            "Retailer generation completed successfully."
        )

    except Exception:
        logger.exception("Retailer generation failed.")
        raise


if __name__ == "__main__":
    main()
