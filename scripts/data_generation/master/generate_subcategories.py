
"""
Project : FMCG Sales and Supply Chain Analytics
Purpose : Generate and validate subcategory master data.
"""

from scripts.common.master_data import SUBCATEGORY_MASTER
from scripts.common.constants import SUBCATEGORY_REQUIRED_FIELDS

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


def generate_subcategories(categories: list) -> list:
    """
    Generate subcategories using the supplied category records.
    """

    category_mapping = {
        category["category_name"]: category["category_id"]
        for category in categories
    }

    subcategories = []

    for subcategory_id, subcategory in enumerate(
        SUBCATEGORY_MASTER,
        start=1
    ):

        category_name = subcategory["category_name"]

        if category_name not in category_mapping:
            raise ValueError(
                f"Category not found: {category_name}"
            )

        record = {
            "subcategory_id": subcategory_id,
            "category_id": category_mapping[category_name],
            "subcategory_name": subcategory["subcategory_name"],
            "subcategory_description": subcategory[
                "subcategory_description"
            ]
        }

        subcategories.append(record)

    return subcategories


def validate_subcategories(
    subcategories: list,
    categories: list
) -> None:

    check_required_fields(
        subcategories,
        SUBCATEGORY_REQUIRED_FIELDS
    )

    check_unique(
        subcategories,
        "subcategory_id"
    )

    unique_combinations = [
        {
            "category_subcategory": (
                record["category_id"],
                record["subcategory_name"].strip().casefold()
            )
        }
        for record in subcategories
    ]

    check_unique(
        unique_combinations,
        "category_subcategory"
    )

    check_foreign_keys(
        subcategories,
        "category_id",
        categories,
        "category_id"
    )


def main():
    try:
        logger.info("Subcategory generation started.")

        # Load category data only once.
        categories = get_latest_json(
            "master/categories",
            "categories"
        )

        subcategories = generate_subcategories(categories)

        validate_subcategories(
            subcategories,
            categories
        )

        save_json(
            subcategories,
            "subcategories",
            "generated",
            "master"
        )

        logger.info(
            "Subcategory generation completed. Records: %s",
            len(subcategories)
        )

    except Exception:
        logger.exception("Subcategory generation failed.")
        raise


if __name__ == "__main__":
    main()
