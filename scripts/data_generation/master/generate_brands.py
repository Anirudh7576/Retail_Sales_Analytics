
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Generate brand dimension data and validate it.
"""

from scripts.common.master_data import BRAND_MASTER

from scripts.common.constants import (
    BRAND_REQUIRED_FIELDS
)

from scripts.common.validation import (
    check_required_fields,
    check_unique
)

from scripts.common.file_utils import save_json

from scripts.common.logger import logger


# ============================================================
# GENERATE BRAND DIMENSION
# ============================================================

def generate_brands() -> list:
    """
    Generate brand dimension records.
    """

    dim_brand = []

    for brand_id, brand in enumerate(
        BRAND_MASTER,
        start=1
    ):

        brand_record = {
            "brand_id": brand_id,
            **brand
        }

        dim_brand.append(brand_record)

    return dim_brand


# ============================================================
# MAIN PROCESS
# ============================================================

def main():

    try:

        logger.info("Brand generation started.")

        brands = generate_brands()

        logger.info(
            "Generated %s brand records.",
            len(brands)
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        check_required_fields(
            brands,
            BRAND_REQUIRED_FIELDS
        )

        check_unique(
            brands,
            "brand_id"
        )

        check_unique(
            brands,
            "brand_name"
        )

        logger.info("Brand validation successful.")

        # ----------------------------------------------------
        # SAVE GENERATED DATA
        # ----------------------------------------------------

        save_json(
            brands,
            "brands",
            "generated",
            "master"
        )

        logger.info("Brand generation completed successfully.")

    except Exception:
        logger.exception("Brand generation failed.")
        raise


if __name__ == "__main__":
    main()
