## 1. Purpose

The purpose of this document is to define how data moves from source files stored in Amazon S3 into Snowflake RAW, SILVER and GOLD schemas.

It documents:

- Source datasets and file formats.
- Source-to-target table mappings.
- Column-level mappings.
- Data transformation rules.
- Data quality validations.
- Surrogate key generation.
- Fact and dimension loading dependencies.

This document ensures consistent data integration and traceability throughout the ELT pipeline.

## 2. Source System Overview

The project simulates data from multiple FMCG business domains.

| Source Dataset | Business Domain | File Format | Frequency |
|---|---|---|---|
| Categories | Product Master | JSON | Initial / On Change |
| Subcategories | Product Master | JSON | Initial / On Change |
| Brands | Product Master | JSON | Initial / On Change |
| Products | Product Master | JSON | Initial / On Change |
| UOM | Product Master | JSON | Initial / On Change |
| Geography | Location Master | JSON | Initial / On Change |
| Distributors | Distribution | JSON | Initial / On Change |
| Retailers | Distribution | JSON | Initial / On Change |
| Warehouses | Inventory | JSON | Initial / On Change |
| Sales Channels | Sales | JSON | Initial / On Change |
| Distributor-Retailer Mapping | Distribution | JSON | Initial / On Change |
| Dates | Reference Data | JSON | Initial / Annual |
| Sales | Sales | CSV | Daily |
| Orders | Order Management | CSV | Daily |
| Inventory | Inventory Management | Parquet | Daily |
| Shipments | Logistics | JSON | Daily |

All data is synthetically generated using Python, Faker and Pandas.

## 3. Amazon S3 Source Structure

Source files are organized in the S3 landing zone.

bucket/
│
├── landing/
│   ├── master/
│   │   ├── categories/
│   │   ├── subcategories/
│   │   ├── brands/
│   │   ├── products/
│   │   ├── uom/
│   │   ├── geography/
│   │   ├── distributors/
│   │   ├── retailers/
│   │   ├── warehouses/
│   │   ├── sales_channels/
│   │   ├── distributor_retailer_mapping/
│   │   └── dates/
│   │
│   └── transactions/
│       ├── sales/
│       ├── orders/
│       ├── inventory/
│       └── shipments/
│
├── archive/
│   ├── master/
│   └── transactions/
│
└── rejected/
    ├── master/
    └── transactions/
```

## 4. Snowflake Schema Overview

The Snowflake database will contain the following schemas:

| Schema | Purpose |
|---|---|
| RAW_SCHEMA | Source-level data ingestion |
| SILVER_SCHEMA | Cleaned, standardized and validated data |
| GOLD_SCHEMA | Curated dimensions and fact tables |
| AUDIT_SCHEMA | File tracking, pipeline logs and data-quality results |

### 4.1 RAW Schema

The RAW schema stores source data with ingestion metadata.

Recommended metadata columns:

| Column | Description |
|---|---|
| source_file_name | Original file name |
| source_file_path | S3 source path |
| file_row_number | Record position in the source file, where available |
| load_timestamp | Ingestion timestamp |
| pipeline_run_id | Airflow pipeline run identifier |
| record_hash | Optional record fingerprint |

The original source fields must be preserved wherever practical.

### 4.2 SILVER Schema

The SILVER schema contains:

- Standardized column names.
- Corrected data types.
- Cleaned records.
- Deduplicated business identifiers.
- Validated foreign-key relationships.
- Standardized dates and financial values.
- Data-quality status and rejection information.

### 4.3 GOLD Schema

The GOLD schema contains:

**Dimensions**

DIM_CATEGORY, DIM_SUBCATEGORY, DIM_BRAND, DIM_UOM, DIM_PRODUCT, DIM_GEOGRAPHY, DIM_DISTRIBUTOR, DIM_RETAILER, DIM_WAREHOUSE, DIM_SALES_CHANNEL and DIM_DATE.

**Bridge**

BRIDGE_DISTRIBUTOR_RETAILER.

**Facts**

FACT_SALES, FACT_ORDERS, FACT_INVENTORY and FACT_SHIPMENTS.

## 5. Dataset-Level Source-to-Target Mapping

| Source File | RAW Table | SILVER Table | GOLD Table |
|---|---|---|---|
| categories.json | RAW_CATEGORIES | STG_CATEGORIES | DIM_CATEGORY |
| subcategories.json | RAW_SUBCATEGORIES | STG_SUBCATEGORIES | DIM_SUBCATEGORY |
| brands.json | RAW_BRANDS | STG_BRANDS | DIM_BRAND |
| products.json | RAW_PRODUCTS | STG_PRODUCTS | DIM_PRODUCT |
| uom.json | RAW_UOM | STG_UOM | DIM_UOM |
| geography.json | RAW_GEOGRAPHY | STG_GEOGRAPHY | DIM_GEOGRAPHY |
| distributors.json | RAW_DISTRIBUTORS | STG_DISTRIBUTORS | DIM_DISTRIBUTOR |
| retailers.json | RAW_RETAILERS | STG_RETAILERS | DIM_RETAILER |
| warehouses.json | RAW_WAREHOUSES | STG_WAREHOUSES | DIM_WAREHOUSE |
| sales_channels.json | RAW_SALES_CHANNELS | STG_SALES_CHANNELS | DIM_SALES_CHANNEL |
| distributor_retailer_mapping.json | RAW_DISTRIBUTOR_RETAILER | STG_DISTRIBUTOR_RETAILER | BRIDGE_DISTRIBUTOR_RETAILER |
| dates.json | RAW_DATES | STG_DATES | DIM_DATE |
| sales.csv | RAW_SALES | STG_SALES | FACT_SALES |
| orders.csv | RAW_ORDERS | STG_ORDERS | FACT_ORDERS |
| inventory.parquet | RAW_INVENTORY | STG_INVENTORY | FACT_INVENTORY |
| shipments.json | RAW_SHIPMENTS | STG_SHIPMENTS | FACT_SHIPMENTS |

Note: The `STG_` naming convention refers to cleaned SILVER-layer staging tables, not a separate warehouse layer.

## 6. Master Data Transformation Mapping

### 6.1 Product Master

| Source Column | Target Column | Transformation |
|---|---|---|
| category_id | category_id | Preserve business ID |
| category_name | category_name | Trim spaces and standardize |
| subcategory_id | subcategory_id | Preserve business ID |
| category_id | category_key | Resolve from DIM_CATEGORY |
| brand_id | brand_id | Preserve business ID |
| brand_name | brand_name | Standardize |
| product_id | product_id | Preserve business ID |
| sku_code | sku_code | Trim and validate uniqueness |
| product_name | product_name | Trim spaces |
| brand_id | brand_key | Lookup DIM_BRAND |
| category_id | category_key | Lookup DIM_CATEGORY |
| subcategory_id | subcategory_key | Lookup DIM_SUBCATEGORY |
| pack_uom_id | pack_uom_key | Lookup DIM_UOM |
| mrp | mrp | Convert to NUMBER(12,2) |
| standard_cost | standard_cost | Convert to NUMBER(12,2) |
| shelf_life_days | shelf_life_days | Validate positive integer |

### 6.2 Distributor and Retailer Master

| Source Column | Target Column | Transformation |
|---|---|---|
| distributor_id | distributor_id | Preserve business ID |
| distributor_code | distributor_code | Trim and standardize |
| distributor_name | distributor_name | Trim spaces |
| geography_id | geography_key | Lookup DIM_GEOGRAPHY |
| retailer_id | retailer_id | Preserve business ID |
| retailer_code | retailer_code | Trim and standardize |
| retailer_name | retailer_name | Trim spaces |
| geography_id | geography_key | Lookup DIM_GEOGRAPHY |
| sales_channel_id | sales_channel_key | Lookup DIM_SALES_CHANNEL |

### 6.3 Geography

| Source Column | Target Column | Transformation |
|---|---|---|
| geography_id | geography_id | Preserve business ID |
| country_code | country_code | Standardize to IN |
| country_name | country_name | Standardize to India |
| sales_region | sales_region | Validate against approved regions |
| state_name | state_name | Standardize state name |
| district_name | district_name | Trim spaces |
| city_name | city_name | Trim spaces |
| pincode | pincode | Store as VARCHAR(10) |

PIN codes must be stored as strings to preserve formatting and leading zeros where applicable.

## 7. Transactional Source-to-Target Mapping

### 7.1 FACT_SALES

**Source:** sales.csv

**Target:** GOLD_SCHEMA.FACT_SALES

**Grain:** One product sold to one retailer in one invoice line.

| Source Column | Target Column | Transformation |
|---|---|---|
| invoice_line_id | invoice_line_id | Validate uniqueness |
| invoice_id | invoice_id | Preserve business ID |
| invoice_date | invoice_date_key | Lookup DIM_DATE |
| product_id | product_key | Lookup DIM_PRODUCT |
| distributor_id | distributor_key | Lookup DIM_DISTRIBUTOR |
| retailer_id | retailer_key | Lookup DIM_RETAILER |
| geography_id | geography_key | Lookup DIM_GEOGRAPHY |
| sales_channel_id | sales_channel_key | Lookup DIM_SALES_CHANNEL |
| quantity | quantity | Validate greater than zero |
| unit_selling_price | unit_selling_price | Convert to NUMBER(12,2) |
| unit_cost | unit_cost | Convert to NUMBER(12,2) |
| quantity × unit_selling_price | gross_sales_amount | Calculate |
| discount_amount | discount_amount | Validate non-negative and within gross sales |
| tax_amount | tax_amount | Validate non-negative |
| gross_sales_amount - discount_amount + tax_amount | net_sales_amount | Calculate under the agreed tax-inclusive definition |
| quantity × unit_cost | cost_amount | Calculate |
| gross_sales_amount - discount_amount - cost_amount | profit_amount | Calculate excluding tax |

The financial formula must be applied consistently across all records.

### 7.2 FACT_ORDERS

**Source:** orders.csv

**Target:** GOLD_SCHEMA.FACT_ORDERS

**Grain:** One SKU in one retailer order line.

| Source Column | Target Column | Transformation |
|---|---|---|
| order_line_id | order_line_id | Validate uniqueness |
| order_id | order_id | Preserve business ID |
| order_date | order_date_key | Lookup DIM_DATE |
| requested_delivery_date | requested_delivery_date_key | Lookup DIM_DATE |
| product_id | product_key | Lookup DIM_PRODUCT |
| distributor_id | distributor_key | Lookup DIM_DISTRIBUTOR |
| retailer_id | retailer_key | Lookup DIM_RETAILER |
| geography_id | geography_key | Lookup DIM_GEOGRAPHY |
| ordered_quantity | ordered_quantity | Validate greater than zero |
| unit_price | unit_price | Convert to NUMBER(12,2) |
| ordered_quantity × unit_price | order_amount | Calculate or reconcile |
| order_status | order_status | Validate approved status |

### 7.3 FACT_INVENTORY

**Source:** inventory.parquet

**Target:** GOLD_SCHEMA.FACT_INVENTORY

**Grain:** One SKU in one warehouse on one snapshot date.

| Source Column | Target Column | Transformation |
|---|---|---|
| inventory_snapshot_id | inventory_snapshot_id | Validate uniqueness |
| snapshot_date | snapshot_date_key | Lookup DIM_DATE |
| product_id | product_key | Lookup DIM_PRODUCT |
| warehouse_id | warehouse_key | Lookup DIM_WAREHOUSE |
| opening_stock_quantity | opening_stock_quantity | Validate non-negative |
| received_quantity | received_quantity | Validate non-negative |
| issued_quantity | issued_quantity | Validate non-negative |
| closing_stock_quantity | closing_stock_quantity | Reconcile stock movement |
| damaged_quantity | damaged_quantity | Validate non-negative |
| reserved_quantity | reserved_quantity | Validate non-negative |
| available_quantity | available_quantity | Calculate or reconcile |
| unit_cost | unit_cost | Convert to NUMBER(12,2) |
| closing_stock_quantity × unit_cost | inventory_value | Calculate using agreed valuation method |

### 7.4 FACT_SHIPMENTS

**Source:** shipments.json

**Target:** GOLD_SCHEMA.FACT_SHIPMENTS

**Grain:** One SKU in one shipment line.

| Source Column | Target Column | Transformation |
|---|---|---|
| shipment_line_id | shipment_line_id | Validate uniqueness |
| shipment_id | shipment_id | Preserve business ID |
| order_line_id | order_line_id | Validate against order-line business ID |
| shipment_date | shipment_date_key | Lookup DIM_DATE |
| delivery_date | delivery_date_key | Lookup DIM_DATE |
| product_id | product_key | Lookup DIM_PRODUCT |
| distributor_id | distributor_key | Lookup DIM_DISTRIBUTOR |
| retailer_id | retailer_key | Lookup DIM_RETAILER |
| warehouse_id | warehouse_key | Lookup DIM_WAREHOUSE |
| shipped_quantity | shipped_quantity | Validate positive quantity |
| delivered_quantity | delivered_quantity | Validate non-negative and not greater than shipped quantity |
| shipment_status | shipment_status | Validate approved status |
| transporter_name | transporter_name | Standardize text |
| tracking_number | tracking_number | Preserve reference |

## 8. Surrogate Key Generation

Surrogate keys will be generated in the GOLD layer.

| Dimension | Surrogate Key | Business Key |
|---|---|---|
| DIM_CATEGORY | category_key | category_id |
| DIM_SUBCATEGORY | subcategory_key | subcategory_id |
| DIM_BRAND | brand_key | brand_id |
| DIM_UOM | uom_key | uom_id |
| DIM_PRODUCT | product_key | product_id |
| DIM_GEOGRAPHY | geography_key | geography_id |
| DIM_DISTRIBUTOR | distributor_key | distributor_id |
| DIM_RETAILER | retailer_key | retailer_id |
| DIM_WAREHOUSE | warehouse_key | warehouse_id |
| DIM_SALES_CHANNEL | sales_channel_key | sales_channel_id |

Surrogate keys should remain stable across incremental loads.

Dimension lookups must use business identifiers and, for SCD Type 2 dimensions, the appropriate effective-date range.

## 9. Data Quality and Reconciliation

Before records are loaded into GOLD, the following validations must pass.

| Validation | Expected Result |
|---|---|
| Required business keys | No missing mandatory identifiers |
| Duplicate transaction IDs | No duplicate invoice, order or shipment line keys |
| Product references | All accepted references resolve |
| Distributor references | All accepted references resolve |
| Retailer references | All accepted references resolve |
| Geography references | Valid geography or approved Unknown-member handling |
| Sales calculations | Amounts reconcile to the approved formula |
| Inventory calculations | Stock balances reconcile |
| Shipment calculations | Delivered quantity does not exceed shipped quantity |
| Record counts | Source, accepted, rejected and loaded counts reconcile |

### 9.1 Record Count Reconciliation

For each source file:

Total Source Records = Accepted Records + Rejected Records

After deduplication, duplicate records must be separately accounted for so that the audit process can distinguish invalid records from intentionally discarded duplicates.

### 9.2 File-Level Tracking

Every processed file must be tracked using:

- Source file name.
- Source file path.
- Dataset name.
- File size.
- File checksum, where available.
- Pipeline run ID.
- Processing timestamp.
- Source record count.
- Accepted record count.
- Rejected record count.
- Processing status.

## 10. Loading Dependencies

Master data must be loaded before dependent transactional data.

Recommended dependency sequence:

```text
DIM_CATEGORY
      |
      v
DIM_SUBCATEGORY
      |
      v
DIM_BRAND + DIM_UOM
      |
      v
DIM_PRODUCT

DIM_GEOGRAPHY
      |
      +------> DIM_DISTRIBUTOR
      |
      +------> DIM_RETAILER
      |
      +------> DIM_WAREHOUSE

DIM_SALES_CHANNEL
      |
      v
DIM_RETAILER

DIM_DISTRIBUTOR + DIM_RETAILER
      |
      v
BRIDGE_DISTRIBUTOR_RETAILER

DIM_DATE

All Required Dimensions
      |
      +------> FACT_SALES
      |
      +------> FACT_ORDERS
      |
      +------> FACT_INVENTORY
      |
      +------> FACT_SHIPMENTS
```
