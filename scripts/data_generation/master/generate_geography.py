
from scripts.common.master_data import GEOGRAPHY_MASTER
from scripts.common.constants import GEOGRAPHY_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique
)
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_geography() -> list:
    geography_records = []

    for geography_id, geography in enumerate(
        GEOGRAPHY_MASTER, start=1
    ):
        geography_record = {
            "geography_id": geography_id,
            **geography
        }

        geography_records.append(geography_record)

    return geography_records


def validate_geography(records: list) -> None:
    # Validate required fields
    check_required_fields(
        records,
        GEOGRAPHY_REQUIRED_FIELDS
    )

    # Validate unique geography IDs
    check_unique(records, "geography_id")

    # Validate unique city, district, state and PIN combinations
    location_keys = [
        (
            record["city"].strip().lower(),
            record["district"].strip().lower(),
            record["state"].strip().lower(),
            record["postal_code"].strip()
        )
        for record in records
    ]

    if len(location_keys) != len(set(location_keys)):
        raise ValueError(
            "Duplicate city, district, state and postal code combination found."
        )


def main():
    try:
        logger.info("Geography generation started.")

        geography_records = generate_geography()

        logger.info(
            "Generated %s geography records.",
            len(geography_records)
        )

        validate_geography(geography_records)

        logger.info("Geography validation successful.")

        save_json(
            geography_records,
            "geography",
            "generated",
            "master"
        )

        logger.info(
            "Geography generation completed successfully."
        )

    except Exception:
        logger.exception("Geography generation failed.")
        raise


if __name__ == "__main__":
    main()
