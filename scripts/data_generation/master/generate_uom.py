
from scripts.common.master_data import UOM_MASTER
from scripts.common.constants import UOM_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique
)
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_uom() -> list:
    uom_records = []

    for uom_id, uom in enumerate(UOM_MASTER, start=1):
        uom_record = {
            "uom_id": uom_id,
            **uom
        }

        uom_records.append(uom_record)

    return uom_records


def main():
    try:
        logger.info("UOM generation started.")

        uom_records = generate_uom()

        logger.info(
            "Generated %s UOM records.",
            len(uom_records)
        )

        # Validate required fields
        check_required_fields(
            uom_records,
            UOM_REQUIRED_FIELDS
        )

        # Validate unique identifiers and names
        check_unique(uom_records, "uom_id")
        check_unique(uom_records, "uom_name")

        logger.info("UOM validation successful.")

        # Save generated records
        save_json(
            uom_records,
            "uom",
            "generated",
            "master"
        )

        logger.info("UOM generation completed successfully.")

    except Exception:
        logger.exception("UOM generation failed.")
        raise


if __name__ == "__main__":
    main()
