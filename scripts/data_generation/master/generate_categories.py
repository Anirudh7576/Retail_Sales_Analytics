
"""
Project : FMCG Sales and Supply Chain Analytics
Purpose : Generate and validate category master data.
"""

from scripts.common.master_data import CATEGORY_MASTER
from scripts.common.constants import CATEGORY_REQUIRED_FIELDS
from scripts.common.validation import check_required_fields, check_unique
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_categories() -> list:
    """Generate category records with sequential IDs."""

    categories = []

    for category_id, category in enumerate(
        CATEGORY_MASTER,
        start=1
    ):
        category_record = {
            "category_id": category_id,
            **category
        }

        categories.append(category_record)

    return categories


def validate_categories(categories: list) -> None:
    check_required_fields(
        categories,
        CATEGORY_REQUIRED_FIELDS
    )

    check_unique(categories, "category_id")
    check_unique(categories, "category_name")


def main():
    try:
        logger.info("Category generation started.")

        categories = generate_categories()
        validate_categories(categories)

        save_json(
            categories,
            "categories",
            "generated",
            "master"
        )

        logger.info(
            "Category generation completed. Records: %s",
            len(categories)
        )

    except Exception:
        logger.exception("Category generation failed.")
        raise


if __name__ == "__main__":
    main()
