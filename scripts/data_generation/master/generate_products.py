
"""
Project : FMCG Sales and Supply Chain Analytics
Purpose : Generate and validate product master data.
"""

import math

from scripts.common.master_data import (
    build_product_master,
    BRAND_CATEGORY_MAPPING,
    validate_product_family_profiles,
    validate_case_quantity_mapping
)

from scripts.common.constants import PRODUCT_REQUIRED_FIELDS

from scripts.common.validation import (
    check_required_fields,
    check_unique,
    check_foreign_keys,
    validate_category_cost_factors
)

from scripts.common.file_utils import (
    save_json,
    get_latest_json
)

from scripts.common.logger import logger


# ============================================================
# GENERATE PRODUCTS
# ============================================================

def generate_products() -> list:
    """Validate product configuration and generate products."""

    validate_case_quantity_mapping()
    validate_product_family_profiles()

    return build_product_master()


# ============================================================
# PRODUCT BUSINESS RULE VALIDATION
# ============================================================

def validate_product_business_rules(products: list) -> None:
    """Validate product pricing, pack size and shelf life."""

    for product in products:

        product_id = product["product_id"]

        # Pack size
        pack_size = product["pack_size"]

        if (
            isinstance(pack_size, bool)
            or not isinstance(pack_size, (int, float))
            or not math.isfinite(pack_size)
            or pack_size <= 0
        ):
            raise ValueError(
                f"Invalid pack size for product_id {product_id}"
            )

        # MRP
        mrp = product["mrp"]

        if (
            isinstance(mrp, bool)
            or not isinstance(mrp, (int, float))
            or not math.isfinite(mrp)
            or mrp <= 0
        ):
            raise ValueError(
                f"Invalid MRP for product_id {product_id}"
            )

        # Standard cost
        standard_cost = product["standard_cost"]

        if (
            isinstance(standard_cost, bool)
            or not isinstance(standard_cost, (int, float))
            or not math.isfinite(standard_cost)
            or standard_cost <= 0
        ):
            raise ValueError(
                f"Invalid standard cost for product_id {product_id}"
            )

        if standard_cost >= mrp:
            raise ValueError(
                f"Standard cost must be lower than MRP. "
                f"Product ID: {product_id}"
            )

        # Shelf life
        shelf_life = product["shelf_life_days"]

        if (
            isinstance(shelf_life, bool)
            or not isinstance(shelf_life, int)
            or shelf_life <= 0
        ):
            raise ValueError(
                f"Invalid shelf life for product_id {product_id}"
            )

        # Units per case
        units_per_case = product["units_per_case"]

        if (
            isinstance(units_per_case, bool)
            or not isinstance(units_per_case, int)
            or units_per_case <= 0
        ):
            raise ValueError(
                f"Invalid units_per_case for product_id {product_id}"
            )


# ============================================================
# PRODUCT BRAND-CATEGORY VALIDATION
# ============================================================

def validate_product_brand_category(
    products: list,
    subcategories: list
) -> None:
    """Ensure each brand sells only permitted categories."""

    subcategory_lookup = {
        item["subcategory_id"]: item["category_id"]
        for item in subcategories
    }

    for product in products:

        subcategory_id = product["subcategory_id"]
        brand_id = product["brand_id"]
        sku = product["sku"]

        if subcategory_id not in subcategory_lookup:
            raise ValueError(
                f"Unknown subcategory ID: {subcategory_id}, SKU: {sku}"
            )

        category_id = subcategory_lookup[subcategory_id]

        allowed_categories = BRAND_CATEGORY_MAPPING.get(brand_id)

        if allowed_categories is None:
            raise ValueError(
                f"Unknown brand ID: {brand_id}, SKU: {sku}"
            )

        if category_id not in allowed_categories:
            raise ValueError(
                f"Invalid brand-category combination: "
                f"SKU={sku}, Brand ID={brand_id}, "
                f"Category ID={category_id}"
            )


# ============================================================
# VALIDATE PRODUCT MASTER
# ============================================================

def validate_products(
    products: list,
    subcategories: list,
    brands: list,
    uom_records: list,
    packaging_types: list
) -> None:
    """Run all product master validations."""

    # 1. Required fields
    check_required_fields(
        products,
        PRODUCT_REQUIRED_FIELDS
    )

    # 2. Unique product identifiers
    check_unique(products, "product_id")
    check_unique(products, "sku")
    check_unique(products, "product_name")

    # 3. Foreign-key validation
    check_foreign_keys(
        products,
        "subcategory_id",
        subcategories,
        "subcategory_id"
    )

    check_foreign_keys(
        products,
        "brand_id",
        brands,
        "brand_id"
    )

    check_foreign_keys(
        products,
        "uom_id",
        uom_records,
        "uom_id"
    )

    check_foreign_keys(
        products,
        "content_uom_id",
        uom_records,
        "uom_id"
    )

    check_foreign_keys(
        products,
        "packaging_type_id",
        packaging_types,
        "packaging_type_id"
    )

    # 4. Category-based standard cost
    validate_category_cost_factors(
        products,
        subcategories
    )

    # 5. Brand-category applicability
    validate_product_brand_category(
        products,
        subcategories
    )

    # 6. Product business rules
    validate_product_business_rules(products)


# ============================================================
# MAIN PROCESS
# ============================================================

def main():

    try:

        logger.info("Product generation started.")

        # Load dependent master datasets
        subcategories = get_latest_json(
            "master/subcategories",
            "subcategories"
        )

        brands = get_latest_json(
            "master/brands",
            "brands"
        )

        uom_records = get_latest_json(
            "master/uom",
            "uom"
        )

        packaging_types = get_latest_json(
            "master/packaging_types",
            "packaging_types"
        )

        # Generate products
        products = generate_products()

        logger.info(
            "Generated %s product records.",
            len(products)
        )

        # Validate products
        validate_products(
            products,
            subcategories,
            brands,
            uom_records,
            packaging_types
        )

        logger.info("Product validation successful.")

        # Save generated products
        save_json(
            products,
            "products",
            "generated",
            "master"
        )

        logger.info(
            "Product generation completed successfully."
        )

    except Exception:
        logger.exception("Product generation failed.")
        raise


if __name__ == "__main__":
    main()
