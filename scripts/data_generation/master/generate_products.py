
import math

from scripts.common.master_data import PRODUCT_MASTER
from scripts.common.constants import PRODUCT_REQUIRED_FIELDS
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


def generate_products() -> list:
    product_records = []

    for product_id, product in enumerate(
        PRODUCT_MASTER, start=1
    ):
        product_record = {
            "product_id": product_id,
            **product
        }

        product_records.append(product_record)

    return product_records


def validate_product_business_rules(products: list) -> None:

    for product in products:
        product_id = product["product_id"]

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

        if standard_cost > mrp:
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


def validate_products(
    products: list,
    subcategories: list,
    brands: list,
    uom_records: list
) -> None:

    # Validate required fields
    check_required_fields(
        products,
        PRODUCT_REQUIRED_FIELDS
    )

    # Validate unique product identifiers
    check_unique(products, "product_id")

    # Validate unique SKUs
    check_unique(products, "sku")

    # Validate product names
    check_unique(products, "product_name")

    # Validate subcategory foreign keys
    check_foreign_keys(
        products,
        "subcategory_id",
        subcategories,
        "subcategory_id"
    )

    # Validate brand foreign keys
    check_foreign_keys(
        products,
        "brand_id",
        brands,
        "brand_id"
    )

    # Validate UOM foreign keys
    check_foreign_keys(
        products,
        "uom_id",
        uom_records,
        "uom_id"
    )

    # Validate product business rules
    validate_product_business_rules(products)

    # Validate expected record count
    if len(products) != 300:
        raise ValueError(
            f"Expected 300 products, generated {len(products)}"
        )


def main():
    try:
        logger.info("Product generation started.")

        # Load latest master datasets
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

        # Generate product records
        products = generate_products()

        logger.info(
            "Generated %s product records.",
            len(products)
        )

        # Validate generated products
        validate_products(
            products,
            subcategories,
            brands,
            uom_records
        )

        logger.info("Product validation successful.")

        # Save product master data
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
