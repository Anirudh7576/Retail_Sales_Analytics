
"""
Generate product-level tax configuration.

Run:
python -m scripts.data_generation.transactions.generate_product_tax_config
"""

import json

from pathlib import Path
from datetime import date

from scripts.common.file_utils import PROJECT_ROOT
from scripts.common.tax_config import (
    TAX_EFFECTIVE_START_DATE,
    TAX_EFFECTIVE_END_DATE,
    CATEGORY_TAX_RATE,
    TAX_SOURCE,
    MIN_TAX_RATE,
    MAX_TAX_RATE,
)

from scripts.validation.master_validation_config import (
    MASTER_DATA_DIR,
    MASTER_FILES,
)

from scripts.common.logger import logger


OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "config" / "product_tax_rates.json"
)


def load_master_data(dataset_name: str) -> list:
    """Load an explicitly configured approved master file."""

    file_path = (
        PROJECT_ROOT
        / MASTER_DATA_DIR
        / MASTER_FILES[dataset_name]
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Master file not found: {file_path}"
        )

    with file_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list) or not records:
        raise ValueError(
            f"Invalid or empty master dataset: {dataset_name}"
        )

    return records


def generate_product_tax_config(
    products: list,
    subcategories: list
) -> list:
    """Generate one effective tax configuration per product."""

    subcategory_category_map = {
        record["subcategory_id"]: record["category_id"]
        for record in subcategories
    }

    tax_records = []

    for tax_rate_id, product in enumerate(products, start=1):

        product_id = product["product_id"]
        subcategory_id = product["subcategory_id"]

        category_id = subcategory_category_map.get(
            subcategory_id
        )

        if category_id is None:
            raise ValueError(
                f"Category not found for product {product_id}"
            )

        tax_rate = CATEGORY_TAX_RATE.get(category_id)

        if tax_rate is None:
            raise ValueError(
                f"Tax rate not configured for category {category_id}"
            )

        tax_record = {
            "tax_rate_id": tax_rate_id,
            "product_id": product_id,
            "category_id": category_id,
            "tax_rate_pct": tax_rate,
            "effective_start_date": (
                TAX_EFFECTIVE_START_DATE.isoformat()
            ),
            "effective_end_date": (
                TAX_EFFECTIVE_END_DATE.isoformat()
            ),
            "tax_source": TAX_SOURCE,
        }

        tax_records.append(tax_record)

    return tax_records


def validate_product_tax_config(
    tax_records: list,
    products: list
) -> bool:
    """Validate product tax configuration."""

    errors = []

    required_fields = [
        "tax_rate_id",
        "product_id",
        "category_id",
        "tax_rate_pct",
        "effective_start_date",
        "effective_end_date",
        "tax_source",
    ]

    seen_tax_ids = set()
    seen_products = set()

    for index, record in enumerate(tax_records):

        # Required fields
        for field in required_fields:
            if field not in record or record[field] is None:
                errors.append(
                    f"Record {index}: Missing field {field}"
                )

        if any(
            field not in record or record[field] is None
            for field in required_fields
        ):
            continue

        # Unique tax ID
        tax_id = record["tax_rate_id"]

        if tax_id in seen_tax_ids:
            errors.append(
                f"Duplicate tax_rate_id: {tax_id}"
            )

        seen_tax_ids.add(tax_id)

        # One configuration per product in this initial version
        product_id = record["product_id"]

        if product_id in seen_products:
            errors.append(
                f"Duplicate tax configuration for product {product_id}"
            )

        seen_products.add(product_id)

        # Validate tax rate
        tax_rate = record["tax_rate_pct"]

        if (
            isinstance(tax_rate, bool)
            or not isinstance(tax_rate, (int, float))
            or not MIN_TAX_RATE <= tax_rate <= MAX_TAX_RATE
        ):
            errors.append(
                f"Invalid tax rate for product {product_id}"
            )

        # Validate effective dates
        try:
            start_date = date.fromisoformat(
                record["effective_start_date"]
            )

            end_date = date.fromisoformat(
                record["effective_end_date"]
            )

            if start_date > end_date:
                errors.append(
                    f"Invalid effective dates for product {product_id}"
                )

        except (ValueError, TypeError):
            errors.append(
                f"Invalid date format for product {product_id}"
            )

    # Validate product coverage
    expected_product_ids = {
        product["product_id"]
        for product in products
    }

    missing_products = expected_product_ids - seen_products
    unexpected_products = seen_products - expected_product_ids

    if missing_products:
        errors.append(
            f"Missing tax configurations: {len(missing_products)} products"
        )

    if unexpected_products:
        errors.append(
            f"Unknown product references: {len(unexpected_products)}"
        )

    if errors:
        for error in errors:
            logger.error(error)

        raise ValueError(
            f"Tax configuration validation failed: {len(errors)} errors"
        )

    logger.info(
        "Product tax configuration validation successful."
    )

    return True


def save_tax_config(records: list) -> None:
    """Save tax configuration as JSON."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    logger.info(
        f"Tax configuration saved: {OUTPUT_FILE}"
    )


def main():

    logger.info("Product tax configuration started.")

    products = load_master_data("products")
    subcategories = load_master_data("subcategories")

    logger.info(
        f"Loaded products: {len(products)}"
    )

    tax_records = generate_product_tax_config(
        products,
        subcategories
    )

    validate_product_tax_config(
        tax_records,
        products
    )

    save_tax_config(tax_records)

    logger.info(
        f"Generated tax records: {len(tax_records)}"
    )

    logger.info(
        "Product tax configuration completed successfully."
    )


if __name__ == "__main__":
    main()
