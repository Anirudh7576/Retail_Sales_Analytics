
"""
Project : FMCG Sales and Supply Chain Analytics
Purpose : Generate and validate brand master data.
"""

from scripts.common.master_data import BRAND_MASTER
from scripts.common.constants import BRAND_REQUIRED_FIELDS
from scripts.common.validation import check_required_fields, check_unique
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_brands() -> list:
    """Generate brand records using configured brand IDs."""

    return [dict(brand) for brand in BRAND_MASTER]


def validate_brands(brands: list) -> None:
    check_required_fields(brands, BRAND_REQUIRED_FIELDS)
    check_unique(brands, "brand_id")
    check_unique(brands, "brand_name")


def main():
    try:
        logger.info("Brand generation started.")

        brands = generate_brands()
        validate_brands(brands)

        save_json(
            brands,
            "brands",
            "generated",
            "master"
        )

        logger.info(
            "Brand generation completed. Records: %s",
            len(brands)
        )

    except Exception:
        logger.exception("Brand generation failed.")
        raise


if __name__ == "__main__":
    main()
