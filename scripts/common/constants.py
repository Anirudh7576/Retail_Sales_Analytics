
# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_NAME = "ABC Consumer Products India Pvt. Ltd."

COUNTRY = "India"
CURRENCY = "INR"

DATE_START = "2025-01-01"
DATE_END = "2026-12-31"

# Financial precision
DECIMAL_PLACES = 2


# ============================================================
# DATA GENERATION VOLUMES
# ============================================================

DATA_VOLUME = {
    "categories": 4,
    "subcategories": 20,
    "brands": 20,
    "products": 300,
    "uom": 10,
    "geography": 1000,
    "distributors": 100,
    "retailers": 20000,
    "warehouses": 50,
    "sales_channels": 5,
    "distributor_retailer_mappings": 25000,
    "sales": 1000000,
    "orders": 250000,
    "inventory": 500000,
    "shipments": 200000
}


# ============================================================
# MASTER DATA REQUIRED FIELDS
# ============================================================

CATEGORY_REQUIRED_FIELDS = [
    "category_id",
    "category_name",
    "category_description"
]

SUBCATEGORY_REQUIRED_FIELDS = [
    "subcategory_id",
    "category_id",
    "subcategory_name",
    "subcategory_description"
]

BRAND_REQUIRED_FIELDS = [
    "brand_id",
    "brand_name",
    "brand_description"
]

PRODUCT_REQUIRED_FIELDS = [
    "product_id",
    "subcategory_id",
    "brand_id",
    "product_name",
    "sku",
    "uom_id",
    "mrp",
    "standard_cost",
    "shelf_life_days"
]

UOM_REQUIRED_FIELDS = [
    "uom_id",
    "uom_name",
    "uom_description"
]

GEOGRAPHY_REQUIRED_FIELDS = [
    "geography_id",
    "city",
    "district",
    "state",
    "region",
    "country",
    "postal_code"
]

DISTRIBUTOR_REQUIRED_FIELDS = [
    "distributor_id",
    "distributor_name",
    "geography_id"
]

RETAILER_REQUIRED_FIELDS = [
    "retailer_id",
    "retailer_name",
    "retailer_type",
    "geography_id"
]

WAREHOUSE_REQUIRED_FIELDS = [
    "warehouse_id",
    "warehouse_name",
    "geography_id"
]

SALES_CHANNEL_REQUIRED_FIELDS = [
    "sales_channel_id",
    "sales_channel_name",
    "sales_channel_description"
]

DISTRIBUTOR_RETAILER_MAPPING_REQUIRED_FIELDS = [
    "mapping_id",
    "distributor_id",
    "retailer_id",
    "effective_start_date",
    "effective_end_date"
]

# ============================================================
# DATE DIMENSION REQUIRED FIELDS
# ============================================================

DATE_REQUIRED_FIELDS = [
    "date_id",
    "full_date",
    "day",
    "day_name",
    "week",
    "month",
    "month_name",
    "quarter",
    "year",
    "fiscal_year",
    "fiscal_quarter"
]


# ============================================================
# FACT SALES REQUIRED FIELDS
# ============================================================

FACT_SALES_REQUIRED_FIELDS = [
    "sales_key",
    "invoice_id",
    "invoice_line_id",
    "date_id",
    "product_id",
    "distributor_id",
    "retailer_id",
    "geography_id",
    "sales_channel_id",
    "quantity",
    "unit_price",
    "unit_cost",
    "gross_sales_amount",
    "discount_amount",
    "net_sales_amount",
    "tax_amount",
    "invoice_amount",
    "cost_of_goods_sold",
    "profit_amount"
]

DATE_START = "2025-01-01"
DATE_END = "2026-12-31"
# ============================================================
# FACT ORDERS REQUIRED FIELDS
# ============================================================

FACT_ORDERS_REQUIRED_FIELDS = [
    "order_line_id",
    "order_id",
    "date_id",
    "product_id",
    "distributor_id",
    "retailer_id",
    "sales_channel_id",
    "order_quantity",
    "unit_price",
    "discount_amount",
    "order_line_amount"
]


# ============================================================
# FACT INVENTORY REQUIRED FIELDS
# ============================================================

FACT_INVENTORY_REQUIRED_FIELDS = [
    "inventory_snapshot_id",
    "date_id",
    "product_id",
    "warehouse_id",
    "opening_quantity",
    "receipts_quantity",
    "issues_quantity",
    "adjustment_quantity",
    "closing_quantity"
]


# ============================================================
# FACT SHIPMENTS REQUIRED FIELDS
# ============================================================

FACT_SHIPMENTS_REQUIRED_FIELDS = [
    "shipment_line_id",
    "shipment_id",
    "order_line_id",
    "date_id",
    "product_id",
    "distributor_id",
    "retailer_id",
    "warehouse_id",
    "shipped_quantity"
]
