## 1. Purpose

The purpose of this document is to define data quality standards, validation rules and error-handling procedures for the India FMCG Sales & Supply Chain Analytics project.

These rules ensure that master and transactional data is accurate, complete, consistent, valid and reliable before it is used for business reporting.

The validation framework covers:

- Master data validation
- Transactional data validation
- Data type and schema validation
- Referential integrity
- Business rule validation
- Duplicate detection
- Financial reconciliation
- Inventory reconciliation
- Data pipeline validation

All datasets in this project are synthetically generated and simulate FMCG business operations in India.

## 2. Data Quality Dimensions

The project follows six major data quality dimensions.

| Data Quality Dimension | Description | Example |
|---|---|---|
| Completeness | Required fields must contain valid values | Every sales record must have a product ID |
| Accuracy | Values must represent valid business information | Sales amount must be calculated correctly |
| Consistency | Related datasets must follow common business definitions | Product category must match the product hierarchy |
| Validity | Data must follow defined formats and business rules | Sales quantity must be greater than zero |
| Uniqueness | Business identifiers must not have unintended duplicates | Invoice line ID must be unique |
| Timeliness | Data must arrive and be processed within expected schedules | Daily sales files must be available before the agreed cutoff |

## 3. Validation Layers

Data quality checks will be performed at different stages of the ELT pipeline.

| Layer | Validation Activity | Action |
|---|---|---|
| Python Data Generation | Validate generated records and relationships | Prevent invalid files from being published |
| Amazon S3 Landing | Validate file presence, format and naming conventions | Reject or quarantine invalid files |
| Snowflake RAW | Validate ingestion status, source schema and file metadata | Record ingestion errors |
| Snowflake SILVER | Validate mandatory fields, data types, duplicates and business rules | Clean, quarantine or reject invalid records |
| Snowflake GOLD | Validate surrogate keys, referential integrity and business metrics | Prevent invalid data from reaching reporting |
| Power BI | Validate KPI definitions and report-level aggregations | Ensure consistent business reporting |

## 4. Master Data Quality Rules

### 4.1 DIM_CATEGORY

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| CAT001 | category_id | Must not be NULL | Reject |
| CAT002 | category_id | Must be unique | Reject duplicate |
| CAT003 | category_name | Must not be NULL or blank | Reject |
| CAT004 | category_name | Must follow the approved category list | Reject or flag |
| CAT005 | is_active | Must contain TRUE or FALSE | Reject |

### 4.2 DIM_SUBCATEGORY

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| SUB001 | subcategory_id | Must not be NULL | Reject |
| SUB002 | subcategory_id | Must be unique | Reject duplicate |
| SUB003 | category_id | Must exist in DIM_CATEGORY | Reject or quarantine |
| SUB004 | subcategory_name | Must not be NULL or blank | Reject |
| SUB005 | is_active | Must contain TRUE or FALSE | Reject |

### 4.3 DIM_BRAND

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| BRD001 | brand_id | Must not be NULL | Reject |
| BRD002 | brand_id | Must be unique | Reject duplicate |
| BRD003 | brand_name | Must not be NULL or blank | Reject |
| BRD004 | is_active | Must contain TRUE or FALSE | Reject |

### 4.4 DIM_UOM

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| UOM001 | uom_id | Must not be NULL and must be unique | Reject |
| UOM002 | uom_code | Must belong to the approved UOM list | Reject |
| UOM003 | measurement_type | Must be Volume, Weight or Count | Reject |
| UOM004 | conversion_to_base | Must be greater than zero | Reject |

### 4.5 DIM_PRODUCT

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| PRD001 | product_id | Must not be NULL | Reject |
| PRD002 | product_id | Must be unique | Reject duplicate |
| PRD003 | sku_code | Must be unique | Reject duplicate |
| PRD004 | product_name | Must not be NULL or blank | Reject |
| PRD005 | brand_id | Must exist in DIM_BRAND | Reject or quarantine |
| PRD006 | category_id | Must exist in DIM_CATEGORY | Reject or quarantine |
| PRD007 | subcategory_id | Must exist in DIM_SUBCATEGORY | Reject or quarantine |
| PRD008 | category_id and subcategory_id | Must represent a valid parent-child relationship | Reject or quarantine |
| PRD009 | pack_size | Must be greater than zero | Reject |
| PRD010 | units_per_case | Must be greater than zero | Reject |
| PRD011 | mrp | Must be greater than or equal to zero | Reject |
| PRD012 | standard_cost | Must be greater than or equal to zero | Reject |
| PRD013 | shelf_life_days | Must be greater than zero | Reject |
| PRD014 | product_status | Must be Active or Discontinued | Reject |

### 4.6 DIM_GEOGRAPHY

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| GEO001 | geography_id | Must not be NULL and must be unique | Reject |
| GEO002 | country_code | Must be IN | Reject |
| GEO003 | country_name | Must be India | Reject |
| GEO004 | sales_region | Must belong to the approved Indian sales-region list | Reject |
| GEO005 | state_name | Must be a valid Indian state or Union Territory | Reject |
| GEO006 | district_name | Must not be NULL or blank | Reject |
| GEO007 | city_name | Must not be NULL or blank | Reject |
| GEO008 | pincode | Must contain exactly six numeric digits | Reject |
| GEO009 | state and PIN code | Must represent a valid geographical combination | Reject or quarantine |

### 4.7 DIM_DISTRIBUTOR

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| DIS001 | distributor_id | Must not be NULL and must be unique | Reject |
| DIS002 | distributor_code | Must be unique | Reject duplicate |
| DIS003 | distributor_name | Must not be NULL or blank | Reject |
| DIS004 | geography_id | Must exist in DIM_GEOGRAPHY | Reject or quarantine |
| DIS005 | contact_email | Must follow valid email format when provided | Reject or flag |
| DIS006 | contact_phone | Must follow the agreed Indian phone-number format when provided | Reject or flag |
| DIS007 | credit_limit | Must be greater than or equal to zero | Reject |
| DIS008 | payment_terms_days | Must be greater than or equal to zero | Reject |

### 4.8 DIM_RETAILER

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| RET001 | retailer_id | Must not be NULL and must be unique | Reject |
| RET002 | retailer_code | Must be unique | Reject duplicate |
| RET003 | retailer_name | Must not be NULL or blank | Reject |
| RET004 | geography_id | Must exist in DIM_GEOGRAPHY | Reject or quarantine |
| RET005 | sales_channel_id | Must exist in DIM_SALES_CHANNEL | Reject or quarantine |
| RET006 | retailer_type | Must belong to the approved retailer-type list | Reject |
| RET007 | credit_limit | Must be greater than or equal to zero | Reject |
| RET008 | payment_terms_days | Must be greater than or equal to zero | Reject |

### 4.9 DIM_WAREHOUSE

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| WAR001 | warehouse_id | Must not be NULL and must be unique | Reject |
| WAR002 | warehouse_code | Must be unique | Reject duplicate |
| WAR003 | warehouse_name | Must not be NULL or blank | Reject |
| WAR004 | geography_id | Must exist in DIM_GEOGRAPHY | Reject or quarantine |
| WAR005 | capacity_units | Must be greater than zero | Reject |
| WAR006 | is_active | Must contain TRUE or FALSE | Reject |

### 4.10 DIM_SALES_CHANNEL

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| CHN001 | sales_channel_id | Must not be NULL and must be unique | Reject |
| CHN002 | channel_code | Must be unique | Reject duplicate |
| CHN003 | channel_name | Must not be NULL or blank | Reject |
| CHN004 | channel_name | Must belong to the approved channel list | Reject |

### 4.11 BRIDGE_DISTRIBUTOR_RETAILER

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| MAP001 | mapping_id | Must not be NULL and must be unique | Reject |
| MAP002 | distributor_id | Must exist in DIM_DISTRIBUTOR | Reject |
| MAP003 | retailer_id | Must exist in DIM_RETAILER | Reject |
| MAP004 | effective_from | Must not be NULL | Reject |
| MAP005 | effective_to | Must be greater than or equal to effective_from when populated | Reject |
| MAP006 | distributor_id, retailer_id and effective dates | Must not create overlapping assignments unless explicitly permitted | Reject or flag |
| MAP007 | is_active | Must agree with the mapping's effective period and current status | Reject or flag |

## 5. Transactional Data Quality Rules

### 5.1 FACT_SALES

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| SAL001 | invoice_line_id | Must not be NULL and must be unique | Reject duplicate |
| SAL002 | invoice_id | Must not be NULL | Reject |
| SAL003 | invoice_date | Must not be NULL and must be valid | Reject |
| SAL004 | product_id | Must exist in DIM_PRODUCT | Reject or quarantine |
| SAL005 | distributor_id | Must exist in DIM_DISTRIBUTOR | Reject or quarantine |
| SAL006 | retailer_id | Must exist in DIM_RETAILER | Reject or quarantine |
| SAL007 | geography_id | Must exist in DIM_GEOGRAPHY or follow approved Unknown-member handling | Reject or map |
| SAL008 | sales_channel_id | Must exist in DIM_SALES_CHANNEL | Reject or quarantine |
| SAL009 | quantity | Must be greater than zero | Reject |
| SAL010 | unit_selling_price | Must be greater than or equal to zero | Reject |
| SAL011 | unit_cost | Must be greater than or equal to zero | Reject |
| SAL012 | discount_amount | Must be greater than or equal to zero and not exceed gross sales | Reject |
| SAL013 | tax_amount | Must be greater than or equal to zero | Reject |
| SAL014 | gross_sales_amount | Must reconcile with quantity multiplied by unit selling price | Reject or flag |
| SAL015 | net_sales_amount | Must reconcile with the approved gross sales, discount and tax formula | Reject or flag |
| SAL016 | profit_amount | Must reconcile with net sales excluding tax less cost amount | Reject or flag |
| SAL017 | distributor-retailer mapping | Must be valid on invoice date | Reject or quarantine |

### 5.2 FACT_ORDERS

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| ORD001 | order_line_id | Must not be NULL and must be unique | Reject duplicate |
| ORD002 | order_id | Must not be NULL | Reject |
| ORD003 | order_date | Must not be NULL | Reject |
| ORD004 | product_id | Must exist in DIM_PRODUCT | Reject |
| ORD005 | distributor_id | Must exist in DIM_DISTRIBUTOR | Reject |
| ORD006 | retailer_id | Must exist in DIM_RETAILER | Reject |
| ORD007 | ordered_quantity | Must be greater than zero | Reject |
| ORD008 | unit_price | Must be greater than or equal to zero | Reject |
| ORD009 | order_amount | Must reconcile with quantity and price under the agreed pricing formula | Reject or flag |
| ORD010 | requested_delivery_date | Must not precede order_date | Reject |
| ORD011 | order_status | Must belong to the approved order-status list | Reject |

### 5.3 FACT_INVENTORY

| Rule ID | Column | Validation Rule | Action |
|---|---|---|---|
| INV001 | inventory_snapshot_id | Must not be NULL and must be unique | Reject duplicate |
| INV002 | snapshot_date | Must not be NULL | Reject |
| INV003 | product_id | Must exist in DIM_PRODUCT | Reject |
| INV004 | warehouse_id | Must exist in DIM_WAREHOUSE | Reject |
| INV005 | opening_stock_quantity | Must be greater than or equal to zero | Reject |
| INV006 | received_quantity | Must be greater than or equal to zero | Reject |
| INV007 | issued_quantity | Must be greater than or equal to zero | Reject |
| INV008 | closing_stock_quantity | Must be greater than or equal to zero | Reject |
| INV009 | damaged_quantity | Must be greater than or equal to zero | Reject |
| INV010 | reserved_quantity | Must be greater than or equal to zero | Reject |
| INV011 | available_quantity | Must be greater than or equal to zero and not exceed closing stock | Reject |
| INV012 | inventory_value | Must reconcile