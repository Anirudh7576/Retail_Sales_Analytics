
"""
Project : FMCG Sales and Supply Chain Analytics
Purpose : Generate and validate UOM master data.
"""

from scripts.common.master_data import UOM_MASTER
from scripts.common.constants import UOM_REQUIRED_FIELDS

from scripts.common.validation import (
    check_required_fields,
    check_unique
)

from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_uom() -> list:
    """Generate UOM records using configured IDs."""

    return [dict(uom) for uom in UOM_MASTER]


def validate_uom(records: list) -> None:

    check_required_fields(
        records,
        UOM_REQUIRED_FIELDS
    )

    check_unique(records, "uom_id")
    check_unique(records, "uom_code")
    check_unique(records, "uom_name")


def main():
    try:
        logger.info("UOM generation started.")

        uom_records = generate_uom()
        validate_uom(uom_records)

        save_json(
            uom_records,
            "uom",
            "generated",
            "master"
        )

        logger.info(
            "UOM generation completed. Records: %s",
            len(uom_records)
        )

    except Exception:
        logger.exception("UOM generation failed.")
        raise


if __name__ == "__main__":
    main()
