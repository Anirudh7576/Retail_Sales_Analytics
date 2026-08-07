"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Subcategory Dimension data and save it as JSON.
"""

from scripts.common.constants import (
    SUBCATEGORY_MASTER,
    SUBCATEGORY_REQUIRED_FIELDS,
)

from scripts.common.validation import (
    check_required_fields,
    check_unique,
)

from scripts.common.file_utils import save_json

from scripts.data_generation.generate_categories import generate_categories


# ==========================================================
# Generate Subcategory Dimension
# ==========================================================

def generate_subcategories() -> list:
    """
    Generate subcategory dimension data.
    """

    # Generate category dimension
    categories = generate_categories()

    # Build category lookup dictionary
    category_lookup = {
        category["category_name"]: category["category_id"]
        for category in categories
    }

    dim_subcategory = []

    for subcategory_id, subcategory in enumerate(
        SUBCATEGORY_MASTER,
        start=101
    ):

        # Create a copy of the master record
        subcategory_record = subcategory.copy()

        # Add generated primary key
        subcategory_record["subcategory_id"] = subcategory_id

        # Add foreign key
        subcategory_record["category_id"] = category_lookup[
            subcategory_record["category_name"]
        ]

        # Remove helper column
        subcategory_record.pop("category_name")

        dim_subcategory.append(subcategory_record)

    return dim_subcategory

# ==========================================================
# Main
# ==========================================================

def main():

    try:

        subcategories = generate_subcategories()

        # Validation
        check_required_fields(
            subcategories,
            SUBCATEGORY_REQUIRED_FIELDS
        )

        check_unique(
            subcategories,
            "subcategory_id"
        )

        check_unique(
            subcategories,
            "subcategory_name"
        )

        # Save JSON
        save_json(
            records=subcategories,
            file_prefix="subcategories"
        )

        print("\nGenerated Subcategory Records\n")

        for record in subcategories:
            print(record)

        print("\nSubcategory generation completed successfully.")

    except Exception as error:

        print(f"\nProcess failed : {error}")


if __name__ == "__main__":
    main()