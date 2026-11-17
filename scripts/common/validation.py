
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Common data validation functions.
"""
from scripts.common.master_data import CATEGORY_COST_FACTORS, SUBCATEGORY_MASTER

# ============================================================
# CHECK REQUIRED FIELDS
# ============================================================

def check_required_fields(
    records: list,
    required_fields: list
) -> bool:
    """
    Validate that all required fields exist
    and are not blank.
    """

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Record at index {index} must be a dictionary."
            )

        for field in required_fields:

            if field not in record:
                raise ValueError(
                    f"Missing required field '{field}'. "
                    f"Record: {record}"
                )

            value = record[field]

            if value is None:
                raise ValueError(
                    f"Null value found for '{field}'. "
                    f"Record: {record}"
                )

            if isinstance(value, str) and not value.strip():
                raise ValueError(
                    f"Blank value found for '{field}'. "
                    f"Record: {record}"
                )

    return True

# ============================================================
# CHECK UNIQUE VALUES
# ============================================================

def check_unique(
    records: list,
    field_name: str
) -> bool:
    """
    Validate uniqueness of a field.
    """

    seen_values = set()

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Record at index {index} must be a dictionary."
            )

        if field_name not in record:
            raise ValueError(
                f"Field '{field_name}' not found. "
                f"Record: {record}"
            )

        value = record[field_name]

        if value is None:
            raise ValueError(
                f"Null value found for '{field_name}'. "
                f"Record: {record}"
            )

        if isinstance(value, str) and not value.strip():
            raise ValueError(
                f"Blank value found for '{field_name}'. "
                f"Record: {record}"
            )

        try:
            if value in seen_values:
                raise ValueError(
                    f"Duplicate value found for "
                    f"'{field_name}': {value}"
                )

            seen_values.add(value)

        except TypeError:
            raise ValueError(
                f"Unhashable value found for "
                f"'{field_name}': {value}"
            )

    return True
# ============================================================
# CHECK FOREIGN KEYS
# ============================================================

def check_foreign_keys(
    fact_records: list,
    fact_field: str,
    dim_records: list,
    dim_field: str
) -> bool:
    """
    Validate that every foreign-key value in fact records
    exists in the corresponding dimension records.
    """

    # Validate dimension key uniqueness
    check_unique(
        dim_records,
        dim_field
    )

    # Build a set of valid dimension keys
    valid_values = {
        record[dim_field]
        for record in dim_records
    }

    for index, record in enumerate(fact_records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Fact record at index {index} "
                f"must be a dictionary."
            )

        if fact_field not in record:
            raise ValueError(
                f"Foreign key field '{fact_field}' "
                f"not found. Record: {record}"
            )

        value = record[fact_field]

        if value is None:
            raise ValueError(
                f"Null foreign key '{fact_field}'. "
                f"Record: {record}"
            )

        if isinstance(value, str) and not value.strip():
            raise ValueError(
                f"Blank foreign key '{fact_field}'. "
                f"Record: {record}"
            )

        if value not in valid_values:
            raise ValueError(
                f"Invalid foreign key '{fact_field}': {value}. "
                f"Record: {record}"
            )

    return True



def validate_category_cost_factors(
    products: list,
    subcategories: list
) -> None:

    # Build subcategory-to-category lookup
    subcategory_lookup = {
        item["subcategory_id"]: item["category_id"]
        for item in subcategories
    }

    for product in products:

        subcategory_id = product["subcategory_id"]
        sku = product["sku"]

        if subcategory_id not in subcategory_lookup:
            raise ValueError(
                f"Unknown subcategory ID: {subcategory_id}, "
                f"SKU: {sku}"
            )

        category_id = subcategory_lookup[subcategory_id]

        cost_factor = CATEGORY_COST_FACTORS.get(category_id)

        if cost_factor is None:
            raise ValueError(
                f"Missing cost factor for category ID: {category_id}"
            )

        expected_cost = round(
            product["mrp"] * cost_factor, 2
        )

        if product["standard_cost"] != expected_cost:
            raise ValueError(
                f"Incorrect standard cost for SKU: {sku}. "
                f"Expected: {expected_cost}, "
                f"Actual: {product['standard_cost']}"
            )

    print("Category cost factor validation successful.")


def validate_unique_ids(records, id_field, master_name):
    ids = [record.get(id_field) for record in records]

    if None in ids:
        raise ValueError(
            f"{master_name}: Missing {id_field}"
        )

    if len(ids) != len(set(ids)):
        raise ValueError(
            f"{master_name}: Duplicate {id_field}"
        )

    return set(ids)

def validate_foreign_keys(
    records,
    foreign_key,
    valid_ids,
    master_name
):
    invalid_ids = {
        record.get(foreign_key)
        for record in records
        if record.get(foreign_key) not in valid_ids
    }

    if invalid_ids:
        raise ValueError(
            f"{master_name}: Invalid {foreign_key}: "
            f"{invalid_ids}"
        )

def validate_product_master_relationships(
    products,
    subcategories,
    brands,
    uoms,
    packaging_types
):
    subcategory_ids = validate_unique_ids(
        subcategories,
        "subcategory_id",
        "Subcategory Master"
    )

    brand_ids = validate_unique_ids(
        brands,
        "brand_id",
        "Brand Master"
    )

    uom_ids = validate_unique_ids(
        uoms,
        "uom_id",
        "UOM Master"
    )

    packaging_ids = validate_unique_ids(
        packaging_types,
        "packaging_type_id",
        "Packaging Type Master"
    )

    validate_unique_ids(
        products,
        "product_id",
        "Product Master"
    )

    validate_foreign_keys(
        products, "subcategory_id",
        subcategory_ids, "Product Master"
    )

    validate_foreign_keys(
        products, "brand_id",
        brand_ids, "Product Master"
    )

    validate_foreign_keys(
        products, "uom_id",
        uom_ids, "Product Master"
    )

    validate_foreign_keys(
        products, "content_uom_id",
        uom_ids, "Product Master"
    )

    validate_foreign_keys(
        products, "packaging_type_id",
        packaging_ids, "Product Master"
    )

    print("Product master relationship validation successful.")
    # ==========================================================
