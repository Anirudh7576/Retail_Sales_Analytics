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

    # Generate categories
    categories = generate_categories()

    # Create category lookup dictionary
    category_lookup = {
        category["category_name"]: category["category_id"]
        for category in categories
    }
result = generate_categories()
print(result)