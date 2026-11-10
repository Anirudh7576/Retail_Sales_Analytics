## 1. Purpose

The purpose of this data model is to define the structure, relationships, primary keys, foreign keys and modelling standards of the Snowflake data warehouse for the India FMCG Sales & Supply Chain Analytics project.

The data model is designed to support:

- Secondary sales analysis
- Distributor and retailer performance
- Product, brand and category performance
- Regional and sales-channel analysis
- Warehouse inventory monitoring
- Order fulfilment analysis
- Shipment and delivery performance
- Historical business reporting

## 2. Data Warehouse Architecture

Snowflake serves as the centralized cloud data warehouse.

The platform follows a three-layer ELT architecture:

| Layer | Purpose | Data Processing |
|---|---|---|
| RAW | Source data ingestion | Store CSV, JSON and Parquet source records with ingestion metadata |
| SILVER | Data cleansing and integration | Standardize data types, remove duplicates, validate relationships and apply business rules |
| GOLD | Business analytics | Create fact tables, dimensions and curated business metrics |

Apache Airflow orchestrates file ingestion, validation, transformation and pipeline execution.

Amazon S3 stores the original source files for auditing and reprocessing.

Power BI consumes the curated GOLD data for business reporting.

### Data Flow

```text
Synthetic Source Systems
(Python + Faker + Pandas)
          |
          v
Amazon S3 – Landing Zone
(CSV / JSON / Parquet)
          |
          v
Apache Airflow
          |
          v
Snowflake RAW
          |
          v
Snowflake SILVER
          |
          v
Snowflake GOLD
          |
          v
Power BI Dashboards
```

Airflow orchestrates the pipeline; data is transferred from S3 to Snowflake through Snowflake ingestion operations, not physically through Airflow.

## 3. Data Modelling Approach

The GOLD layer follows a **Fact Constellation (Galaxy Schema)** approach.

This design consists of multiple fact tables sharing common dimensions.

Each fact table is modelled at a clearly defined business grain.

The four primary fact tables are:

1. FACT_SALES
2. FACT_ORDERS
3. FACT_INVENTORY
4. FACT_SHIPMENTS

The shared dimensions include product, distributor, retailer, date, geography and warehouse.

The product master also uses a normalized hierarchy of category, subcategory, brand and unit of measurement. Therefore, the overall model combines fact constellation modelling with selected snowflaked dimensions.

### Why This Approach?

A single star schema is not sufficient for the project's different business processes.

Sales, orders, inventory and shipments represent different business events and cannot be combined into one fact table without introducing duplication and incorrect aggregations.

Using separate fact tables provides clearer business definitions, better data consistency and more flexible analytics.

## 4. Fact Tables

### 4.1 FACT_SALES

**Business process:** Secondary sales from distributors to retailers.

**Grain:** One SKU sold to one retailer in one invoice line.

The table contains:

- Invoice and invoice-line identifiers
- Invoice date
- Product, distributor and retailer references
- Geography and sales-channel references
- Quantity sold
- Unit selling price and unit cost
- Gross sales
- Discounts and taxes
- Net sales
- Cost and profit amounts

**Business KPIs:**

- Gross Sales
- Net Sales
- Sales Quantity
- Discount Amount
- Gross Profit
- Sales Growth
- Average Selling Price

### 4.2 FACT_ORDERS

**Business process:** Retailer orders placed with distributors.

**Grain:** One SKU in one retailer order line.

The table contains:

- Order and order-line identifiers
- Order date
- Requested delivery date
- Product, distributor and retailer references
- Ordered quantity
- Unit price
- Order amount
- Order status

**Business KPIs:**

- Total Orders
- Ordered Quantity
- Order Value
- Pending Orders
- Fulfilled Orders
- Order Fulfilment Rate

### 4.3 FACT_INVENTORY

**Business process:** Warehouse inventory management.

**Grain:** One SKU in one warehouse on one snapshot date.

The table contains:

- Inventory snapshot identifier
- Snapshot date
- Product and warehouse references
- Opening stock
- Received quantity
- Issued quantity
- Closing stock
- Damaged quantity
- Reserved quantity
- Available quantity
- Unit cost
- Inventory value

**Business KPIs:**

- Stock on Hand
- Available Stock
- Inventory Value
- Stock-out Rate
- Inventory Turnover (when supporting cost-of-goods-sold data is available)
- Days of Inventory (when supporting consumption data is available)

**Important:** Inventory is a periodic snapshot fact. Inventory balances must not be summed across multiple dates as if they were transaction quantities.

### 4.4 FACT_SHIPMENTS

**Business process:** Shipment and delivery fulfilment.

**Grain:** One SKU in one shipment line.

The table contains:

- Shipment and shipment-line identifiers
- Associated order-line identifier
- Shipment date
- Delivery date
- Product, distributor and retailer references
- Warehouse reference
- Shipped quantity
- Delivered quantity
- Shipment status
- Transporter and tracking information

**Business KPIs:**

- Shipped Quantity
- Delivered Quantity
- On-time Delivery Rate
- Average Delivery Time
- Shipment Fulfilment Rate
- Delayed Shipments

## 5. Dimension Tables

| Dimension | Description |
|---|---|
| DIM_CATEGORY | FMCG product categories |
| DIM_SUBCATEGORY | Product subcategories linked to categories |
| DIM_BRAND | Product brand information |
| DIM_UOM | Units of measurement and conversions |
| DIM_PRODUCT | SKU, packaging, MRP, cost and shelf-life attributes |
| DIM_GEOGRAPHY | India geography including region, state, district, city and PIN code |
| DIM_DISTRIBUTOR | Distributor master information |
| DIM_RETAILER | Retailer master information |
| DIM_WAREHOUSE | Warehouse master information |
| DIM_SALES_CHANNEL | Sales channel classifications |
| DIM_DATE | Calendar and Indian fiscal date attributes |

### 5.1 Product Hierarchy

The product hierarchy is:

```text
DIM_CATEGORY
     |
     v
DIM_SUBCATEGORY
     |
     v
DIM_PRODUCT
     ^
     |
DIM_BRAND

DIM_UOM ------> DIM_PRODUCT
```

One category can contain multiple subcategories.

One subcategory can contain multiple products.

One brand can contain multiple products.

One UOM can be associated with multiple products.

### 5.2 Distribution Hierarchy

The business distribution flow is:

```text
Manufacturer
     |
     v
Distributor
     |
     v
Retailer
     |
     v
End Consumer
```

The initial project captures secondary sales from distributors to retailers.

End-consumer purchases and manufacturer-to-distributor primary sales are outside the initial scope.

### 5.3 Distributor-Retailer Mapping

`BRIDGE_DISTRIBUTOR_RETAILER` maintains the relationship between distributors and retailers.

It includes effective dates to support historical assignment changes.

A retailer may move from one distributor to another over time.

Historical sales must remain attributed to the distributor responsible for the original transaction.

## 6. Primary Keys

Each GOLD dimension uses a numeric surrogate primary key, while source-system business identifiers are retained separately.

| Table | Primary Key | Business Identifier |
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
| DIM_DATE | date_key | full_date |
| BRIDGE_DISTRIBUTOR_RETAILER | mapping_key | mapping_id |
| FACT_SALES | sales_key | invoice_line_id |
| FACT_ORDERS | order_key | order_line_id |
| FACT_INVENTORY | inventory_key | inventory_snapshot_id |
| FACT_SHIPMENTS | shipment_key | shipment_line_id |

Business identifiers are generated in Python and retained in RAW and SILVER.

Surrogate keys are assigned in the Snowflake GOLD layer.

## 7. Foreign Keys

### 7.1 Dimension Relationships

| Child Table | Foreign Key | Referenced Table |
|---|---|---|
| DIM_SUBCATEGORY | category_key | DIM_CATEGORY |
| DIM_PRODUCT | category_key | DIM_CATEGORY |
| DIM_PRODUCT | subcategory_key | DIM_SUBCATEGORY |
| DIM_PRODUCT | brand_key | DIM_BRAND |
| DIM_PRODUCT | pack_uom_key | DIM_UOM |
| DIM_DISTRIBUTOR | geography_key | DIM_GEOGRAPHY |
| DIM_RETAILER | geography_key | DIM_GEOGRAPHY |
| DIM_RETAILER | sales_channel_key | DIM_SALES_CHANNEL |
| DIM_WAREHOUSE | geography_key | DIM_GEOGRAPHY |
| BRIDGE_DISTRIBUTOR_RETAILER | distributor_key | DIM_DISTRIBUTOR |
| BRIDGE_DISTRIBUTOR_RETAILER | retailer_key | DIM_RETAILER |

### 7.2 Fact Relationships

| Fact Table | Foreign Keys |
|---|---|
| FACT_SALES | invoice_date_key, product_key, distributor_key, retailer_key, geography_key, sales_channel_key |
| FACT_ORDERS | order_date_key, requested_delivery_date_key, product_key, distributor_key, retailer_key, geography_key |
| FACT_INVENTORY | snapshot_date_key, product_key, warehouse_key |
| FACT_SHIPMENTS | shipment_date_key, delivery_date_key, product_key, distributor_key, retailer_key, warehouse_key |

Date keys reference `DIM_DATE`.

Other foreign keys reference their corresponding dimensions.

Shipment records also retain `order_line_id` as a business reference to connect shipments with source orders. This is not a dimension surrogate key.

## 8. Relationships

### 8.1 Master Data Relationships

| Parent Table | Child Table | Relationship |
|---|---|---|
| DIM_CATEGORY | DIM_SUBCATEGORY | One-to-Many |
| DIM_SUBCATEGORY | DIM_PRODUCT | One-to-Many |
| DIM_BRAND | DIM_PRODUCT | One-to-Many |
| DIM_UOM | DIM_PRODUCT | One-to-Many |
| DIM_GEOGRAPHY | DIM_DISTRIBUTOR | One-to-Many |
| DIM_GEOGRAPHY | DIM_RETAILER | One-to-Many |
| DIM_GEOGRAPHY | DIM_WAREHOUSE | One-to-Many |
| DIM_SALES_CHANNEL | DIM_RETAILER | One-to-Many |
| DIM_DISTRIBUTOR | BRIDGE_DISTRIBUTOR_RETAILER | One-to-Many |
| DIM_RETAILER | BRIDGE_DISTRIBUTOR_RETAILER | One-to-Many |

### 8.2 Transaction Relationships

| Parent Table | Child Table | Relationship |
|---|---|---|
| DIM_PRODUCT | FACT_SALES | One-to-Many |
| DIM_DISTRIBUTOR | FACT_SALES | One-to-Many |
| DIM_RETAILER | FACT_SALES | One-to-Many |
| DIM_GEOGRAPHY | FACT_SALES | One-to-Many |
| DIM_SALES_CHANNEL | FACT_SALES | One-to-Many |
| DIM_DATE | FACT_SALES | One-to-Many |
| DIM_PRODUCT | FACT_ORDERS | One-to-Many |
| DIM_DISTRIBUTOR | FACT_ORDERS | One-to-Many |
| DIM_RETAILER | FACT_ORDERS | One-to-Many |
| DIM_GEOGRAPHY | FACT_ORDERS | One-to-Many |
| DIM_DATE | FACT_ORDERS | One-to-Many |
| DIM_PRODUCT | FACT_INVENTORY | One-to-Many |
| DIM_WAREHOUSE | FACT_INVENTORY | One-to-Many |
| DIM_DATE | FACT_INVENTORY | One-to-Many |
| DIM_PRODUCT | FACT_SHIPMENTS | One-to-Many |
| DIM_DISTRIBUTOR | FACT_SHIPMENTS | One-to-Many |
| DIM_RETAILER | FACT_SHIPMENTS | One-to-Many |
| DIM_WAREHOUSE | FACT_SHIPMENTS | One-to-Many |
| DIM_DATE | FACT_SHIPMENTS | One-to-Many |

## 9. Source-to-Target Mapping

| Source Dataset | Source Format | Snowflake RAW | Snowflake SILVER | Snowflake GOLD |
|---|---|---|---|---|
| Categories | JSON | RAW_CATEGORIES | STG_CATEGORIES | DIM_CATEGORY |
| Subcategories | JSON | RAW_SUBCATEGORIES | STG_SUBCATEGORIES | DIM_SUBCATEGORY |
| Brands | JSON | RAW_BRANDS | STG_BRANDS | DIM_BRAND |
| Products | JSON | RAW_PRODUCTS | STG_PRODUCTS | DIM_PRODUCT |
| UOM | JSON | RAW_UOM | STG_UOM | DIM_UOM |
| Geography | JSON | RAW_GEOGRAPHY | STG_GEOGRAPHY | DIM_GEOGRAPHY |
| Distributors | JSON | RAW_DISTRIBUTORS | STG_DISTRIBUTORS | DIM_DISTRIBUTOR |
| Retailers | JSON | RAW_RETAILERS | STG_RETAILERS | DIM_RETAILER |
| Warehouses | JSON | RAW_WAREHOUSES | STG_WAREHOUSES | DIM_WAREHOUSE |
| Sales Channels | JSON | RAW_SALES_CHANNELS | STG_SALES_CHANNELS | DIM_SALES_CHANNEL |
| Distributor-Retailer Mapping | JSON | RAW_DISTRIBUTOR_RETAILER | STG_DISTRIBUTOR_RETAILER | BRIDGE_DISTRIBUTOR_RETAILER |
| Dates | JSON | RAW_DATES | STG_DATES | DIM_DATE |
| Sales | CSV | RAW_SALES | STG_SALES | FACT_SALES |
| Orders | CSV | RAW_ORDERS | STG_ORDERS | FACT_ORDERS |
| Inventory | Parquet | RAW_INVENTORY | STG_INVENTORY | FACT_INVENTORY |
| Shipments | JSON | RAW_SHIPMENTS | STG_SHIPMENTS | FACT_SHIPMENTS |

The RAW layer preserves source business identifiers and ingestion metadata.

The SILVER layer validates, deduplicates and standardizes source records.

The GOLD layer resolves dimension surrogate keys and calculates curated business metrics.

## 10. Power BI Considerations

The GOLD model is designed for analytical reporting through Power BI.

### 10.1 Recommended Reporting Model

- Use fact tables for numeric measures and transactional metrics.
- Use dimensions for slicers, filters and descriptive attributes.
- Use one-to-many relationships from dimensions to facts.
- Prefer single-direction filtering from dimensions to facts.
- Use conformed dimensions to compare metrics across sales, orders, inventory and shipments.
- Avoid direct fact-to-fact relationships that create ambiguous filtering or duplicate measures.
- Flatten selected product hierarchy attributes into a reporting-friendly product dimension or Power BI view when appropriate.

### 10.2 Business Dashboards

**Sales Dashboard**
- Net Sales
- Sales Quantity
- Gross Profit
- Product and Brand Performance
- Regional Sales Trends

**Distribution Dashboard**
- Distributor Sales
- Active Retailers
- Retailer Coverage
- Sales by Territory

**Inventory Dashboard**
- Closing Stock
- Available Stock
- Inventory Value
- Low Stock Products

**Supply Chain Dashboard**
- Ordered Quantity
- Shipped Quantity
- Delivered Quantity
- Order Fulfilment Rate
- On-time Delivery Rate

### 10.3 Inventory Reporting Consideration

Inventory is a snapshot fact table.

Inventory quantities are additive across products and warehouses for the same snapshot date but are not additive across dates.

Power BI measures should use the latest relevant snapshot or another explicitly defined inventory aggregation method.

## 11. Data Quality and Integrity Rules

| Rule | Validation |
|---|---|
| Product integrity | Every transaction product must exist in product master data |
| Distributor integrity | Distributor references must exist in distributor master data |
| Retailer integrity | Retailer references must exist in retailer master data |
| Distributor-retailer mapping | Assignment must be valid on the business transaction date |
| Sales quantity | Must be greater than zero |
| Order quantity | Must be greater than zero |
| Sales amount | Must reconcile with quantity, price, discounts and tax |
| Shipment quantity | Must not exceed outstanding order quantity without an approved exception |
| Shipment dates | Shipment date must not precede order date |
| Inventory balance | Must satisfy the agreed stock reconciliation formula |
| Inventory availability | Available quantity must not be negative |
| Duplicate business keys | Duplicate records must be identified and handled |
| Master-data references | Invalid references must be rejected, quarantined or resolved using an approved Unknown-member rule |
| File processing | Every processed source file must have an audit record |

Snowflake standard-table primary-key and foreign-key constraints are generally informational rather than enforced. Referential integrity must therefore be validated through transformation logic and data-quality tests.

## 12. Future Enhancements

The following capabilities can be added in later releases:

1. Primary sales analytics from manufacturer to distributor.
2. Supplier and procurement analytics.
3. Product returns and reverse logistics.
4. Promotion and trade marketing analytics.
5. Payment and receivables analytics.
6. Batch-level inventory and expiry tracking.
7. Change Data Capture using Snowflake Streams and Tasks.
8. Snowpipe-based automated ingestion.
9. Advanced data-quality monitoring and alerts.
10. Role-based access control and data governance.
11. Demand forecasting and replenishment analytics.
12. GitHub Actions-based CI/CD and automated testing.

## 13. Conclusion

The redesigned data model supports a synthetic FMCG sales and supply-chain analytics platform across India.
The GOLD layer uses four fact tables, eleven dimensions and one distributor-retailer bridge table.

