
from scripts.common.master_data import DISTRIBUTOR_MASTER
from scripts.common.constants import DISTRIBUTOR_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique,
    check_foreign_keys
)
from scripts.common.file_utils import save_json, get_latest_json
from scripts.common.logger import logger


def generate_distributors() -> list:
    distributor_records = []

    for distributor_id, distributor in enumerate(
        DISTRIBUTOR_MASTER, start=1
    ):
        distributor_record = {
            "distributor_id": distributor_id,
            **distributor
        }

        distributor_records.append(distributor_record)

    return distributor_records


def validate_distributors(
    distributors: list,
    geography: list
) -> None:

    # Validate required fields
    check_required_fields(
        distributors,
        DISTRIBUTOR_REQUIRED_FIELDS
    )

    # Validate unique distributor IDs
    check_unique(distributors, "distributor_id")

    # Validate unique distributor names
    check_unique(distributors, "distributor_name")

    # Validate geography foreign keys
    check_foreign_keys(
        distributors,
        "geography_id",
        geography,
        "geography_id"
    )


def main():
    try:
        logger.info("Distributor generation started.")

        # Read the latest geography master data
        geography = get_latest_json(
            "master/geography",
            "geography"
        )

        distributors = generate_distributors()

        logger.info(
            "Generated %s distributor records.",
            len(distributors)
        )

        validate_distributors(
            distributors,
            geography
        )

        logger.info("Distributor validation successful.")

        save_json(
            distributors,
            "distributors",
            "generated",
            "master"
        )

        logger.info(
            "Distributor generation completed successfully."
        )

    except Exception:
        logger.exception("Distributor generation failed.")
        raise


if __name__ == "__main__":
    main()
