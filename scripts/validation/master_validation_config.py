
"""
Configuration for consolidated master-data validation.
Only explicitly selected files are included.
"""

MASTER_DATA_DIR = "data/generated/master"

MASTER_FILES = {
    "categories": "categories/categories_20261117_120935_773817.json",
    "brands": "brands/brands_20261117_120946_414956.json",
    "subcategories": "subcategories/subcategories_20261117_121026_894659.json",
    "uom": "uom/uom_20261117_120956_389234.json",
    "packaging_types": "packaging_types/packaging_types_20261117_121015_918155.json",
    "products": "products/products_20261117_121046_696071.json",
    "geography": "geography/geography_20261113_185511_064526.json",
    "distributors": "distributors/distributors_20261113_190154_088841.json",
    "retailers": "retailers/retailers_20261114_094359_702908.json",
    "warehouses": "warehouses/warehouses_20261114_094830_788172.json",
    "sales_channels": "sales_channels/sales_channels_20261114_100412_690844.json",
    "distributor_retailer_mappings": (
        "distributor_retailer_mappings/"
        "distributor_retailer_mappings_20261114_100538_045964.json"
    ),
    "dates": "dates/dates_20261114_102722_852077.json",
}

# Required fields for every dataset.
REQUIRED_FIELDS = {
    "categories": [
        "category_id", "category_name", "category_description"
    ],
    "brands": [
        "brand_id", "brand_name", "brand_description"
    ],
    "subcategories": [
        "subcategory_id", "category_id",
        "subcategory_name", "subcategory_description"
    ],
    "uom": [
        "uom_id", "uom_code", "uom_name", "uom_description"
    ],
    "packaging_types": [
        "packaging_type_id", "packaging_type_name"
    ],
    "products": [
        "product_id", "subcategory_id", "brand_id",
        "product_name", "sku", "uom_id",
        "packaging_type_id", "pack_size", "content_uom_id",
        "mrp", "standard_cost", "shelf_life_days",
        "units_per_case"
    ],
    "geography": [
        "geography_id", "city", "district", "state",
        "region", "country", "postal_code"
    ],
    "distributors": [
        "distributor_id", "distributor_name", "geography_id"
    ],
    "retailers": [
        "retailer_id", "retailer_name",
        "retailer_type", "geography_id"
    ],
    "warehouses": [
        "warehouse_id", "warehouse_name", "geography_id"
    ],
    "sales_channels": [
        "sales_channel_id", "sales_channel_name",
        "sales_channel_description"
    ],
    "distributor_retailer_mappings": [
        "mapping_id", "distributor_id", "retailer_id",
        "effective_start_date", "effective_end_date"
    ],
    "dates": [
        "date_id", "full_date", "day", "day_name",
        "week", "month", "month_name", "quarter", "year",
        "fiscal_year", "fiscal_quarter"
    ],
}

# Primary key for each dataset.
PRIMARY_KEYS = {
    "categories": "category_id",
    "brands": "brand_id",
    "subcategories": "subcategory_id",
    "uom": "uom_id",
    "packaging_types": "packaging_type_id",
    "products": "product_id",
    "geography": "geography_id",
    "distributors": "distributor_id",
    "retailers": "retailer_id",
    "warehouses": "warehouse_id",
    "sales_channels": "sales_channel_id",
    "distributor_retailer_mappings": "mapping_id",
    "dates": "date_id",
}

# Foreign-key relationships:
# dataset: (foreign key field, referenced dataset, referenced primary key)
FOREIGN_KEYS = {
    "subcategories": [
        ("category_id", "categories", "category_id"),
    ],
    "distributors": [
        ("geography_id", "geography", "geography_id"),
    ],
    "retailers": [
        ("geography_id", "geography", "geography_id"),
    ],
    "warehouses": [
        ("geography_id", "geography", "geography_id"),
    ],
    "products": [
        ("subcategory_id", "subcategories", "subcategory_id"),
        ("brand_id", "brands", "brand_id"),
        ("uom_id", "uom", "uom_id"),
        ("content_uom_id", "uom", "uom_id"),
        ("packaging_type_id", "packaging_types", "packaging_type_id"),
    ],
    "distributor_retailer_mappings": [
        ("distributor_id", "distributors", "distributor_id"),
        ("retailer_id", "retailers", "retailer_id"),
    ],
}

# Business-key uniqueness checks.
UNIQUE_FIELDS = {
    "categories": ["category_name"],
    "brands": ["brand_name"],
    "uom": ["uom_code", "uom_name"],
    "packaging_types": ["packaging_type_name"],
    "products": ["sku", "product_name"],
    "sales_channels": ["sales_channel_name"],
}

# Composite business keys.
COMPOSITE_UNIQUE_FIELDS = {
    "subcategories": ["category_id", "subcategory_name"],
}
