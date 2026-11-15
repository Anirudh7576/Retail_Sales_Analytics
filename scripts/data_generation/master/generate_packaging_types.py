
from scripts.common.master_data import PACKAGING_TYPE_MASTER
from scripts.common.constants import PACKAGING_TYPE_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique
)
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_packaging_types() -> list:
    packaging_records = []

    for packaging_type_id, packaging in enumerate(
        PACKAGING_TYPE_MASTER, start=1
    ):
        packaging_record = {
            "packaging_type_id": packaging_type_id,
            **packaging
        }

        packaging_records.append(packaging_record)

    return packaging_records


def validate_packaging_types(records: list) -> None:

    # Validate required fields
    check_required_fields(
        records,
        PACKAGING_TYPE_REQUIRED_FIELDS
    )

    # Validate unique packaging IDs
    check_unique(
        records,
        "packaging_type_id"
    )

    # Validate unique packaging names
    check_unique(
        records,
        "packaging_type_name"
    )

    # Validate expected record count
    if len(records) != 8:
        raise ValueError(
            f"Expected 8 packaging types, generated {len(records)}."
        )


def main():
    try:
        logger.info("Packaging type generation started.")

        packaging_records = generate_packaging_types()

        logger.info(
            "Generated %s packaging type records.",
            len(packaging_records)
        )

        # Validate generated records
        validate_packaging_types(packaging_records)

        logger.info(
            "Packaging type validation successful."
        )

        # Save generated JSON
        save_json(
            packaging_records,
            "packaging_types",
            "generated",
            "master"
        )

        logger.info(
            "Packaging type generation completed successfully."
        )

    except Exception:
        logger.exception(
            "Packaging type generation failed."
        )
        raise


if __name__ == "__main__":
    main()
