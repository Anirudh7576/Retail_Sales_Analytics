
"""
Project : FMCG Sales and Supply Chain Analytics
Purpose : Generate and validate packaging type master data.
"""

from scripts.common.master_data import PACKAGING_TYPE_MASTER
from scripts.common.constants import PACKAGING_TYPE_REQUIRED_FIELDS

from scripts.common.validation import (
    check_required_fields,
    check_unique
)

from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_packaging_types() -> list:
    """Generate packaging records with sequential IDs."""

    return [
        {
            "packaging_type_id": packaging_type_id,
            **packaging
        }
        for packaging_type_id, packaging in enumerate(
            PACKAGING_TYPE_MASTER,
            start=1
        )
    ]


def validate_packaging_types(records: list) -> None:

    check_required_fields(
        records,
        PACKAGING_TYPE_REQUIRED_FIELDS
    )

    check_unique(records, "packaging_type_id")
    check_unique(records, "packaging_type_name")

    if len(records) != len(PACKAGING_TYPE_MASTER):
        raise ValueError(
            "Packaging record count does not match configuration."
        )


def main():
    try:
        logger.info("Packaging type generation started.")

        records = generate_packaging_types()
        validate_packaging_types(records)

        save_json(
            records,
            "packaging_types",
            "generated",
            "master"
        )

        logger.info(
            "Packaging type generation completed. Records: %s",
            len(records)
        )

    except Exception:
        logger.exception("Packaging type generation failed.")
        raise


if __name__ == "__main__":
    main()
