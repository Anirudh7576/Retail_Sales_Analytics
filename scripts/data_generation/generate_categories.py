"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Category Dimension data and validate it.
"""

# ==============================
# Category Master Data
# ==============================

CATEGORY_MASTER = [
    {
        "category_name": "Electronics",
        "category_description": "Electronic devices and accessories"
    },
    {
        "category_name": "Clothing",
        "category_description": "Men's, women's and children's apparel"
    },
    {
        "category_name": "Furniture",
        "category_description": "Home and office furniture"
    },
    {
        "category_name": "Sports",
        "category_description": "Sports equipment and fitness accessories"
    },
    {
        "category_name": "Books",
        "category_description": "Educational, fiction and non-fiction books"
    },
    {
        "category_name": "Beauty",
        "category_description": "Beauty and personal care products"
    },
    {
        "category_name": "Grocery",
        "category_description": "Daily grocery and household essentials"
    },
    {
        "category_name": "Toys",
        "category_description": "Toys and games for children"
    },
    {
        "category_name": "Automotive",
        "category_description": "Vehicle accessories and spare parts"
    },
    {
        "category_name": "Home & Kitchen",
        "category_description": "Kitchen appliances and home essentials"
    }
]

# ===================================
# Validation Configuration
# ===================================

CATEGORY_REQUIRED_FIELDS = [
    "category_id",
    "category_name",
    "category_description"
]
from scripts.common.validation import (
    check_required_fields,
    check_unique,
)

from scripts.common.file_utils import save_json

from scripts.common.constants import CATEGORY_MASTER, CATEGORY_REQUIRED_FIELDS
from datetime import timedelta
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


# ===================================
# Generic Validation Functions
# ===================================

# def check_required_fields(records: list,
#                           required_fields: list) -> bool:
#     """
#     Validate that all required fields exist
#     and are not blank.
#     """

#     for record in records:

#         for field in required_fields:

#             if field not in record:
#                 raise ValueError(
#                     f"Missing required field '{field}'. "
#                     f"Record: {record}"
#                 )

#             if record[field] in (None, ""):
#                 raise ValueError(
#                     f"Blank value found for '{field}'. "
#                     f"Record: {record}"
#                 )

#     return True


# def check_unique(records: list,
#                  field_name: str) -> bool:
#     """
#     Validate uniqueness of a field.
#     """

#     seen_values = set()

#     for record in records:

#         value = record[field_name]

#         if value in seen_values:
#             raise ValueError(
#                 f"Duplicate value found for "
#                 f"'{field_name}': {value}"
#             )

#         seen_values.add(value)

#     return True
# #====================================
# # Save file
# #====================================

# import json
# from pathlib import Path
# from datetime import datetime


# def save_file(dim_category: list) -> None:
#     """
#     Save category data as a JSON file with a timestamp.
#     """

#     # Project root
#     project_root = Path(__file__).resolve().parents[2]

#     # Target directory
#     target_path = project_root / "data" / "generated"

#     # Create directory if it doesn't exist
#     target_path.mkdir(parents=True, exist_ok=True)

#     # Generate filename
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#     file_name = f"categories_{timestamp}.json"

#     file_path = target_path / file_name

#     # Save JSON
#     with open(file_path, "w", encoding="utf-8") as file:
#         json.dump(dim_category, file, indent=4)

#     print(f"File saved successfully: {file_path}")

# ===================================
# Main
# ===================================

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

        # Save JSON
        save_json(
            records=categories,
            file_prefix="categories"
        )

        print("\nGenerated category Records\n")

        for record in categories:
            print(record)

        print("\ncategory generation completed successfully.")

    except Exception as error:

        print(f"\nProcess failed : {error}")


if __name__ == "__main__":
    main()