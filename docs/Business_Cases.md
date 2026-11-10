## 1. Business Cases

The project simulates an FMCG company's sales and supply-chain operations across India. It focuses on secondary sales, distributor and retailer relationships, order fulfilment, inventory management and shipment tracking.

| Business Case | Business Impact | ELT Solution |
|---|---|---|
| Duplicate sales transactions | Inflated sales revenue and incorrect business reports | Identify duplicate invoice lines using business keys and deduplicate records in the SILVER layer. |
| Missing product information | Incomplete product and category-level sales analysis | Validate product references against product master data and quarantine invalid records. |
| Invalid product-category relationships | Incorrect product hierarchy and category reporting | Validate product-to-subcategory and subcategory-to-category relationships during transformation. |
| Duplicate product master records | Inconsistent SKU-level reporting | Identify duplicate product business keys and maintain a single valid product record. |
| Missing distributor information | Incorrect distributor performance and sales attribution | Validate distributor references against the distributor master and route invalid records for investigation. |
| Missing retailer information | Inaccurate retailer-level sales analysis | Validate retailer identifiers and maintain an unknown or rejected-record strategy based on business rules. |
| Incorrect distributor-retailer mapping | Sales attributed to the wrong distributor or territory | Validate effective-dated distributor-retailer relationships against the transaction date. |
| Missing or invalid geography | Inaccurate regional and state-level sales reports | Standardize geography using the geography master and assign an Unknown member where permitted. Log unresolved records. |
| Negative or zero sales quantity | Incorrect sales volume and revenue calculations | Reject records that violate sales quantity rules during SILVER-layer validation. |
| Incorrect sales amount or discount | Inaccurate revenue and profitability reporting | Recalculate gross sales, discounts and net sales using validated quantities and prices. |
| Late-arriving sales files | Delayed sales dashboards and business decisions | Use Airflow sensors or scheduled file checks to detect late files and process them through controlled retries. |
| Missing order dates | Incorrect order ageing and fulfilment analysis | Reject or quarantine records with missing mandatory order dates. |
| Orders not fulfilled on time | Poor retailer service levels and potential lost sales | Compare order dates with shipment and delivery dates to calculate order fulfilment performance. |
| Shipment quantity exceeds ordered quantity | Incorrect fulfilment reporting and inventory discrepancies | Validate shipped quantities against outstanding order quantities and flag exceptions. |
| Inventory below zero | Incorrect stock availability and replenishment decisions | Apply inventory validation rules and investigate invalid stock balances or movements. |
| Inventory stock discrepancies | Unreliable inventory visibility and stock valuation | Reconcile opening stock, receipts, issues and closing stock using inventory movement records. |
| Product expiry and shelf-life risks | Product wastage and potential financial losses | Track product shelf-life information and identify inventory approaching expiry where batch-level data is available. |
| Duplicate distributor or retailer records | Incorrect customer and distribution analytics | Deduplicate master records using business identifiers and apply controlled master-data updates. |
| Data received in different formats | Inconsistent data processing across source systems | Ingest CSV, JSON and Parquet files into Snowflake RAW and standardize schemas in SILVER. |
| Data arrives from multiple source systems | Inconsistent reporting across business functions | Integrate sales, orders, inventory and shipment data using common business keys and conformed dimensions. |
| Historical master-data changes | Incorrect historical sales attribution | Maintain effective-dated master records and use Slowly Changing Dimensions (SCD Type 2) where historical analysis requires them. |
| Manual report preparation | High operational effort and delayed reporting | Automate ingestion, transformation and data-quality workflows using Airflow and Snowflake. |
| Pipeline failures or incomplete loads | Missing or duplicated data in business reports | Implement retries, idempotent processing, file-level audit tracking and pipeline failure notifications. |

## 2. Business Benefits

The proposed data engineering platform provides the following business benefits:

a. **Faster decision-making:** Provide timely visibility into sales, distribution, inventory and shipment performance.

b. **Improved data quality:** Identify duplicate, incomplete, inconsistent and invalid records before they reach analytical reporting.

c. **Better sales visibility:** Analyse sales performance by product, brand, category, distributor, retailer, geography and sales channel.

d. **Improved distribution effectiveness:** Identify high-performing distributors, retailer coverage gaps and regional sales opportunities.

e. **Better inventory management:** Monitor stock availability, inventory ageing and potential stock-out situations.

f. **Improved order fulfilment:** Track pending orders, shipment quantities, fulfilment rates and delivery delays.

g. **Reduced operational effort:** Automate repetitive data ingestion, validation, transformation and reporting activities.

h. **Consistent business reporting:** Provide standardized metrics across sales, distribution and supply-chain functions.

i. **Historical trend analysis:** Maintain historical sales, inventory, order and shipment data for business comparisons and forecasting.

j. **Scalable data processing:** Support increasing data volumes and additional source systems through a modular ELT architecture.

k. **Improved business confidence:** Provide traceability, reconciliation and data-quality monitoring for analytical outputs.

## 3. Technical Mapping

| Business Requirement / Problem | Technology Used | Why |
|---|---|---|
| Synthetic master and transaction data generation | Python, Faker, Pandas | Generate realistic FMCG master and transactional datasets with controlled volumes and relationships. |
| Multiple source file formats | Python, Pandas, PyArrow | Generate and process CSV, JSON and Parquet files. |
| Historical source-file storage | Amazon S3 | Retain original files for auditing, recovery and reprocessing. |
| Data ingestion from S3 | Snowflake External Stages, Storage Integration | Securely access files stored in Amazon S3 without embedding AWS access keys in pipeline code. |
| Workflow automation | Apache Airflow | Schedule, orchestrate, monitor and retry data engineering workflows. |
| Raw data ingestion | Snowflake RAW Schema | Store source data with ingestion metadata while preserving source-level traceability. |
| Data cleansing and standardization | Snowflake SILVER Schema, SQL | Remove duplicates, standardize data types, validate relationships and handle invalid records. |
| Master-data history | Snowflake, SCD Type 2 | Maintain historical changes to selected business dimensions. |
| Analytical data modelling | Snowflake GOLD Schema | Build dimensional models containing fact and dimension tables for business reporting. |
| Incremental data processing | Snowflake Streams and Tasks | Capture and process changes incrementally where appropriate. |
| Data-quality monitoring | Python, Snowflake SQL, Audit Tables | Validate business rules, record failures and monitor data-quality metrics. |
| Pipeline execution tracking | Airflow, Snowflake Audit Tables | Track pipeline runs, file processing status, record counts and failures. |
| Scalable analytical processing | Snowflake | Use independent virtual warehouses and scalable compute for analytical workloads. |
| Business intelligence and reporting | Power BI | Build interactive dashboards for sales, distribution, inventory and supply-chain analysis. |
| Source-code management | Git and GitHub | Maintain version control, collaborate and track project changes. |
| Automated testing and deployment | GitHub Actions | Run code quality checks, tests and deployment workflows through CI/CD. |

## 4. Business Analytics Scope

The platform will initially support four major analytical areas.

| Analytics Area | Key Business Questions | Example KPIs |
|---|---|---|
| Sales Analytics | Which products, brands, distributors and regions generate the highest sales? | Net Sales, Gross Sales, Sales Quantity, Average Selling Price, Sales Growth |
| Distribution Analytics | Which distributors perform best, and how effectively are retailers covered? | Distributor Sales, Active Retailers, Retailer Coverage, Sales per Distributor |
| Inventory Analytics | Which products have low stock or excess inventory? | Stock on Hand, Inventory Value, Days of Inventory, Stock-out Rate |
| Supply Chain Analytics | How efficiently are orders fulfilled and shipments delivered? | Order Fulfilment Rate, Pending Orders, On-time Delivery Rate, Average Delivery Time |

## 5. Project Scope and Assumptions

1. The project uses synthetic data inspired by FMCG business operations in India.
2. The initial sales model represents secondary sales: distributor-to-retailer transactions.
3. Distributor, retailer, product, geography and warehouse information are maintained as master data.
4. The initial ingestion approach uses batch processing from Amazon S3 orchestrated by Apache Airflow.
5. CSV is used for sales and order transactions, JSON for master data and shipment events, and Parquet for inventory snapshots.
6. Snowflake follows a RAW → SILVER → GOLD architecture.
7. Payment analytics, primary sales, returns, promotions and procurement can be introduced in subsequent releases.
8. All business metrics and KPIs will be calculated using documented business definitions and validated data.

