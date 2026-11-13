
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Generate subcategory dimension data and validate it.
"""

from scripts.common.master_data import SUBCATEGORY_MASTER

from scripts.common.constants import (
    SUBCATEGORY_REQUIRED_FIELDS
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


# ============================================================
# GENERATE SUBCATEGORY DIMENSION
# ============================================================

def generate_subcategories() -> list:
    """
    Generate subcategory dimension records.

    category_id is retrieved from the latest category JSON.
    """

    # Read latest category records
    categories = get_latest_json(
        "master/categories",
        "categories"
    )

    # Create category name-to-ID mapping
    category_mapping = {
        category["category_name"]: category["category_id"]
        for category in categories
    }

    dim_subcategory = []

    for subcategory_id, subcategory in enumerate(
        SUBCATEGORY_MASTER,
        start=1
    ):

        category_name = subcategory["category_name"]

        if category_name not in category_mapping:
            raise ValueError(
                f"Category '{category_name}' not found "
                f"in category master data."
            )

        subcategory_record = {
            "subcategory_id": subcategory_id,
            "category_id": category_mapping[category_name],
            "subcategory_name": subcategory["subcategory_name"],
            "subcategory_description": subcategory[
                "subcategory_description"
            ]
        }

        dim_subcategory.append(subcategory_record)

    return dim_subcategory


# ============================================================
# MAIN PROCESS
# ============================================================

def main():

    try:

        logger.info("Subcategory generation started.")

        subcategories = generate_subcategories()

        logger.info(
            "Generated %s subcategory records.",
            len(subcategories)
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        check_required_fields(
            subcategories,
            SUBCATEGORY_REQUIRED_FIELDS
        )

        check_unique(
            subcategories,
            "subcategory_id"
        )

        # Subcategory names must be unique within a category.
        # Check the category + subcategory combination.
        unique_subcategories = [
            {
                "category_subcategory": (
                    record["category_id"],
                    record["subcategory_name"].strip().casefold()
                )
            }
            for record in subcategories
        ]

        check_unique(
            unique_subcategories,
            "category_subcategory"
        )

        # Validate category foreign keys
        categories = get_latest_json(
            "master/categories",
            "categories"
        )

        check_foreign_keys(
            subcategories,
            "category_id",
            categories,
            "category_id"
        )

        logger.info("Subcategory validation successful.")

        # ----------------------------------------------------
        # SAVE GENERATED DATA
        # ----------------------------------------------------

        save_json(
            subcategories,
            "subcategories",
            "generated",
            "master"
        )

        logger.info(
            "Subcategory generation completed successfully."
        )

    except Exception:
        logger.exception("Subcategory generation failed.")
        raise


if __name__ == "__main__":
    main()
