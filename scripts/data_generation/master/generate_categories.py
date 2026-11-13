
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Generate category dimension data and validate it.
"""

from scripts.common.master_data import CATEGORY_MASTER

from scripts.common.constants import (
    CATEGORY_REQUIRED_FIELDS
)

from scripts.common.validation import (
    check_required_fields,
    check_unique
)

from scripts.common.file_utils import save_json


# ============================================================
# GENERATE CATEGORY DIMENSION
# ============================================================

def generate_categories() -> list:
    """
    Generate category dimension records.
    """

    dim_category = []

    for category_id, category in enumerate(
        CATEGORY_MASTER,
        start=1
    ):

        category_record = {
            "category_id": category_id,
            **category
        }

        dim_category.append(category_record)

    return dim_category


# ============================================================
# MAIN PROCESS
# ============================================================

def main():

    categories = generate_categories()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    check_required_fields(
        categories,
        CATEGORY_REQUIRED_FIELDS
    )

    check_unique(
        categories,
        "category_id"
    )

    check_unique(
        categories,
        "category_name"
    )

    # --------------------------------------------------------
    # SAVE GENERATED DATA
    # --------------------------------------------------------

    save_json(
        categories,
        "categories",
        "generated",
        "master"
    )

    print(
        f"Category generation successful. "
        f"Total records: {len(categories)}"
    )


if __name__ == "__main__":
    main()

