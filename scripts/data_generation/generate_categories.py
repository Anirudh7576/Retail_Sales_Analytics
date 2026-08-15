"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Category Dimension data and validate it.
"""

from scripts.common.constants import (
    CATEGORY_MASTER, 
    CATEGORY_REQUIRED_FIELDS,
)

from scripts.common.validation import (
    check_required_fields,
    check_unique,
)

from scripts.common.file_utils import save_json

# ===================================
# Generate Category Dimension
# ===================================

def generate_categories() -> list:
    """
    Generate category dimension records.
    """

    dim_category = []

    for category_id, category in enumerate(CATEGORY_MASTER, start=1):

        category_record = {
            "category_id": category_id,
            **category
        }

        dim_category.append(category_record)

    return dim_category

def main():

    try:

        categories = generate_categories()

        # Validation
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

       # Save
        save_json(
                   categories,
                   "categories",
                   "generated"
               )
       
    except Exception as error:
        print(
                   f"\n dimension categories process failed: {error}"
               )
       
    # --------------------------------------------------
    # Save rejected data ONLY if generation succeeded
    # --------------------------------------------------
       
        if categories is not None:
            save_json(
                categories,
                "categories",
                "rejected")
        
        
        print(
                f"\nFACT_SALES process failed: "
                f"{error}"
                    )
       
if __name__ == "__main__":
           main()