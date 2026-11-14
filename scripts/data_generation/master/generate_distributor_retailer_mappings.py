
from datetime import date

from scripts.common.master_data import (
    DISTRIBUTOR_RETAILER_MAPPING_MASTER
)
from scripts.common.constants import (
    DISTRIBUTOR_RETAILER_MAPPING_REQUIRED_FIELDS
)
from scripts.common.validation import (
    check_required_fields,
    check_unique,
    check_foreign_keys
)
from scripts.common.file_utils import (
    save_json,
    get_latest_json
)
from scripts.common.logger import logger


def generate_distributor_retailer_mappings() -> list:
    mapping_records = []

    for mapping_id, mapping in enumerate(
        DISTRIBUTOR_RETAILER_MAPPING_MASTER,
        start=1
    ):
        mapping_record = {
            "mapping_id": mapping_id,
            **mapping
        }

        mapping_records.append(mapping_record)

    return mapping_records


def validate_mapping_dates(records: list) -> None:
    retailer_assignments = {}

    for record in records:
        retailer_id = record["retailer_id"]

        try:
            start_date = date.fromisoformat(
                record["effective_start_date"]
            )
            end_date = date.fromisoformat(
                record["effective_end_date"]
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Invalid effective date for retailer {retailer_id}"
            ) from exc

        if end_date < start_date:
            raise ValueError(
                f"Effective end date is before start date "
                f"for retailer {retailer_id}"
            )

        retailer_assignments.setdefault(
            retailer_id, []
        ).append((start_date, end_date))

    # Check for overlapping assignments for each retailer
    for retailer_id, periods in retailer_assignments.items():

        periods.sort(key=lambda period: period[0])

        for index in range(1, len(periods)):
            previous_end = periods[index - 1][1]
            current_start = periods[index][0]

            if current_start <= previous_end:
                raise ValueError(
                    f"Overlapping distributor assignments found "
                    f"for retailer_id {retailer_id}"
                )


def validate_distributor_retailer_mappings(
    mappings: list,
    distributors: list,
    retailers: list
) -> None:

    # Validate required fields
    check_required_fields(
        mappings,
        DISTRIBUTOR_RETAILER_MAPPING_REQUIRED_FIELDS
    )

    # Validate unique mapping IDs
    check_unique(mappings, "mapping_id")

    # Validate distributor foreign keys
    check_foreign_keys(
        mappings,
        "distributor_id",
        distributors,
        "distributor_id"
    )

    # Validate retailer foreign keys
    check_foreign_keys(
        mappings,
        "retailer_id",
        retailers,
        "retailer_id"
    )

    # Validate unique distributor-retailer-date combinations
    mapping_keys = [
        (
            record["distributor_id"],
            record["retailer_id"],
            record["effective_start_date"],
            record["effective_end_date"]
        )
        for record in mappings
    ]

    if len(mapping_keys) != len(set(mapping_keys)):
        raise ValueError(
            "Duplicate distributor-retailer mapping found."
        )

    # Validate effective dates and overlapping assignments
    validate_mapping_dates(mappings)


def main():
    try:
        logger.info(
            "Distributor-retailer mapping generation started."
        )

        # Load latest distributor master
        distributors = get_latest_json(
            "master/distributors",
            "distributors"
        )

        # Load latest retailer master
        retailers = get_latest_json(
            "master/retailers",
            "retailers"
        )

        # Generate mapping records
        mappings = generate_distributor_retailer_mappings()

        logger.info(
            "Generated %s distributor-retailer mapping records.",
            len(mappings)
        )

        # Validate generated records
        validate_distributor_retailer_mappings(
            mappings,
            distributors,
            retailers
        )

        logger.info(
            "Distributor-retailer mapping validation successful."
        )

        # Save mapping data
        save_json(
            mappings,
            "distributor_retailer_mappings",
            "generated",
            "master"
        )

        logger.info(
            "Distributor-retailer mapping generation completed successfully."
        )

    except Exception:
        logger.exception(
            "Distributor-retailer mapping generation failed."
        )
        raise


if __name__ == "__main__":
    main()
