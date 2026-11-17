import math

from scripts.common.master_data import (
    validate_product_family_profiles,
    build_product_master,
    BRAND_CATEGORY_MAPPING,
    validate_case_quantity_mapping
)
# from scripts.common.master_data import BRAND_CATEGORY_MAPPING

# from scripts.common.master_data import build_product_master

# from scripts.common.master_data import PRODUCT_MASTER

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


# --------------------------------------------------
# GENERATE PRODUCTS
# --------------------------------------------------

def generate_products():
    validate_case_quantity_mapping
    validate_product_family_profiles()
    products = build_product_master()
    return products

# --------------------------------------------------
# PRODUCT BUSINESS RULE VALIDATION
# --------------------------------------------------

def validate_product_business_rules(products: list) -> None:

    for product in products:

        product_id = product["product_id"]

        # Validate pack size
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

        # Validate MRP
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

        # Validate standard cost
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
                f"Standard cost cannot exceed MRP "
                f"for product_id {product_id}"
            )

        # Validate shelf life
        shelf_life = product["shelf_life_days"]

        if (
            isinstance(shelf_life, bool)
            or not isinstance(shelf_life, int)
            or shelf_life <= 0
        ):
            raise ValueError(
                f"Invalid shelf life for product_id {product_id}"
            )
        
        # Validate units per case
        units_per_case = product.get("units_per_case")

        if (
            isinstance(units_per_case, bool)
            or not isinstance(units_per_case, int)
            or units_per_case <= 0
        ):
            raise ValueError(
                f"Invalid units_per_case for product_id "
                f"{product_id}: {units_per_case}. "
                "Expected a positive integer"
            )

# --------------------------------------------------
# VALIDATE PRODUCT MASTER
# --------------------------------------------------
def validate_product_prices(products: list) -> None:

    for product in products:

        sku = product["sku"]
        mrp = product["mrp"]
        standard_cost = product["standard_cost"]

        if mrp <= 0:
            raise ValueError(
                f"Invalid MRP for SKU: {sku}"
            )

        if standard_cost <= 0:
            raise ValueError(
                f"Invalid standard cost for SKU: {sku}"
            )

        if standard_cost >= mrp:
            raise ValueError(
                f"Standard cost must be lower than MRP: {sku}"
            )

    print("Product price validation successful.")

def validate_product_pack_size(products: list) -> None:

    for product in products:

        if product["pack_size"] <= 0:
            raise ValueError(
                f"Invalid pack size for SKU: {product['sku']}"
            )

    print("Product pack size validation successful.")

def validate_product_shelf_life(products: list) -> None:

    for product in products:

        if product["shelf_life_days"] <= 0:
            raise ValueError(
                f"Invalid shelf life for SKU: {product['sku']}"
            )

    print("Product shelf life validation successful.")

def validate_product_brand_category(
    products: list,
    subcategories: list
) -> None:

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

    print("Product brand-category validation successful.")

# ===========================================================
# ===========================================================
def validate_products(
    products: list,
    subcategories: list,
    brands: list,
    uom_records: list,
    packaging_types: list
) -> None:

    # 1. Validate required fields
    check_required_fields(
        products,
        PRODUCT_REQUIRED_FIELDS
    )

    # 2. Validate unique product identifiers
    check_unique(products, "product_id")

    # 3. Validate unique SKUs
    check_unique(products, "sku")

    # 4. Validate unique product names
    check_unique(products, "product_name")

    # 5. Validate subcategory foreign keys
    check_foreign_keys(
        products,
        "subcategory_id",
        subcategories,
        "subcategory_id"
    )

    # 6. Validate brand foreign keys
    check_foreign_keys(
        products,
        "brand_id",
        brands,
        "brand_id"
    )

    # 7. Validate selling UOM foreign keys
    check_foreign_keys(
        products,
        "uom_id",
        uom_records,
        "uom_id"
    )

    # 8. Validate content UOM foreign keys
    check_foreign_keys(
        products,
        "content_uom_id",
        uom_records,
        "uom_id"
    )

    # 9. Validate packaging type foreign keys
    check_foreign_keys(
        products,
        "packaging_type_id",
        packaging_types,
        "packaging_type_id"
    )

    validate_category_cost_factors(
    products,
    subcategories
    )


    validate_product_brand_category(
            products,
            subcategories
    )

    validate_product_business_rules(products)

    # # 10. Validate product prices
    # validate_product_prices(products)

    # # 11. Validate product pack size
    # validate_product_pack_size(products)

    # # 12. Validate product shelf life
    # validate_product_shelf_life(products)

    # 13. Validate brand-category relationship
    
    print("Product validation successful.")


    # Validate business rules
    # validate_product_business_rules(products)

    # if len(products) != EXPECTED_PRODUCT_COUNT:
    #     raise ValueError(
    #         f"Expected {EXPECTED_PRODUCT_COUNT} products, "
    #         f"generated {len(products)}"
    #     )


# --------------------------------------------------
# MAIN
# --------------------------------------------------


def main():

    try:

        logger.info("Product generation started.")

        # 1. Load latest master datasets
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

        # 2. Generate products
        products = generate_products()

        logger.info(
            "Generated %s product records.",
            len(products)
        )

        # 3. Validate products
        validate_products(
            products,
            subcategories,
            brands,
            uom_records,
            packaging_types
        )

        logger.info("Product validation successful.")

        # 4. Save product master data
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


# validate_case_quantity_mapping()
# validate_product_family_profiles()

# products = build_product_master()

# validate_product_business_rules(products)

# print("Total products:", len(products))