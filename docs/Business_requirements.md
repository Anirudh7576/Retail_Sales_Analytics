## 1. Project Overview

ABC Consumer Products India Pvt. Ltd. is a fictional FMCG company inspired by the operating model of large consumer goods organizations. The company manufactures and distributes consumer products across multiple regions in India through a network of distributors and retailers.

The business manages multiple product categories, brands, SKUs, distributors, retailers, warehouses and sales channels. It generates business data from sales transactions, customer orders, inventory snapshots and shipment operations.

To support business growth and data-driven decision-making, the company requires a modern cloud-based data engineering platform that can efficiently ingest, process, validate, transform and analyze data from multiple business domains.

The proposed solution uses Python for synthetic data generation, Amazon S3 for data storage, Apache Airflow for workflow orchestration, Snowflake for cloud data warehousing and Power BI for business intelligence.

The platform will initially focus on secondary sales analytics, distributor and retailer performance, inventory visibility, order fulfilment and shipment tracking.

## 2. Business Problems

The company faces the following business challenges:

a. **Delayed sales reporting:** Business users do not receive timely sales reports, affecting decision-making.

b. **Manual data preparation:** Data engineering and business teams spend significant time collecting, cleaning and preparing data from different sources.

c. **Inconsistent business data:** Product, distributor, retailer and geography information may be incomplete, duplicated or inconsistent across source systems.

d. **Inaccurate sales reporting:** Duplicate transactions, incorrect product references and invalid quantities can result in incorrect revenue and sales volume calculations.

e. **Limited distributor visibility:** Management cannot easily compare distributor performance across states, regions and sales territories.

f. **Limited retailer coverage analysis:** The company needs better visibility into retailer coverage, active outlets and distributor-retailer relationships.

g. **Poor inventory visibility:** Stock discrepancies, low inventory levels and potential stock-outs make replenishment decisions difficult.

h. **Limited order fulfilment visibility:** The business needs to identify pending orders, delayed shipments and fulfilment issues.

i. **Historical data challenges:** Historical sales, inventory, order and shipment information is difficult to integrate and analyze consistently.

j. **Inconsistent departmental reporting:** Sales, distribution and supply-chain teams may use different calculations and reporting definitions.

## 3. Business Objectives

The primary objectives are:

a. Develop a centralized cloud-based data platform for FMCG sales and supply-chain analytics.

b. Automate data ingestion, validation and transformation using Apache Airflow and Snowflake.

c. Improve data quality by identifying duplicate, missing, invalid and inconsistent records.

d. Provide accurate sales performance analysis by product, brand, category, distributor, retailer, region and sales channel.

e. Improve distributor and retailer performance visibility.

f. Enable better inventory monitoring and identify potential stock-out and excess-stock situations.

g. Improve order fulfilment and shipment tracking.

h. Maintain historical business data to support trend analysis and comparisons.

i. Improve dashboard performance and provide consistent business metrics.

j. Reduce manual reporting effort through automated data pipelines and scheduled dashboard refreshes.

k. Build a scalable and maintainable architecture that can accommodate additional business domains and increasing data volumes.

## 4. Stakeholders

The proposed platform will support the following stakeholders:

a. **Sales Team:** Monitor sales revenue, sales quantity, product performance and regional sales trends.

b. **Distribution Team:** Analyze distributor performance, retailer coverage and territory-level sales.

c. **Supply Chain Team:** Monitor inventory availability, stock movement and supply-chain efficiency.

d. **Warehouse Team:** Track inventory levels, warehouse stock availability and shipment operations.

e. **Finance Team:** Analyze sales value, discounts and revenue-related metrics.

f. **Marketing Team:** Analyze brand, category and product performance across sales channels.

g. **Management:** Monitor business performance and identify opportunities for growth and operational improvement.

h. **Data Engineering Team:** Develop, maintain and monitor ingestion, transformation and orchestration pipelines.

i. **QA / Data Quality Team:** Validate source data, business rules, data reconciliation and pipeline outputs.

j. **Executive Leadership:** Review consolidated business performance through executive dashboards.

## 5. Data Sources

The initial project will simulate data from the following business domains.

### 5.1 Master Data

| Dataset | Description | Format |
|---|---|---|
| Categories | FMCG product categories | JSON |
| Subcategories | Product subcategories | JSON |
| Brands | Product brand information | JSON |
| Products | SKU and product details | JSON |
| Units of Measurement | Product measurement and packaging units | JSON |
| Geography | Country, state, district and city information | JSON |
| Distributors | Distributor master information | JSON |
| Retailers | Retailer master information | JSON |
| Warehouses | Warehouse master information | JSON |
| Sales Channels | General Trade, Modern Trade, Pharmacy, E-commerce and Institutional | JSON |
| Distributor-Retailer Mapping | Distributor-to-retailer territory relationships | JSON |
| Date Dimension | Calendar and financial date information | JSON |

### 5.2 Transactional Data

| Dataset | Description | Format |
|---|---|---|
| Sales | Secondary sales transactions from distributors to retailers | CSV |
| Orders | Retailer orders placed with distributors | CSV |
| Inventory | Product and warehouse inventory snapshots | Parquet |
| Shipments | Shipment and order fulfilment details | JSON |

### 5.3 Data Generation and Storage

- Python, Faker and Pandas will generate synthetic master and transactional datasets.
- CSV, JSON and Parquet formats will represent different source-system extraction patterns.
- Amazon S3 will store generated files in organized landing, archive and rejected zones.
- Snowflake will access source files through external stages and storage integrations.

## 6. Expected Outputs

### 6.1 Data Warehouse Outputs

**RAW Schema**
- Source-level master and transactional data.
- Ingestion metadata and file tracking information.

**SILVER Schema**
- Cleaned and standardized master data.
- Deduplicated and validated transactions.
- Standardized business keys and data types.
- Data-quality exceptions and rejected records.

**GOLD Schema**

Dimension tables:
- DIM_PRODUCT
- DIM_BRAND
- DIM_CATEGORY
- DIM_SUBCATEGORY
- DIM_DISTRIBUTOR
- DIM_RETAILER
- DIM_GEOGRAPHY
- DIM_WAREHOUSE
- DIM_SALES_CHANNEL
- DIM_DATE

Fact tables:
- FACT_SALES
- FACT_ORDERS
- FACT_INVENTORY
- FACT_SHIPMENTS

### 6.2 Business Reports and Dashboards

a. **Sales Performance Dashboard:** Revenue, sales quantity, discounts, product performance and sales trends.

b. **Distributor Performance Dashboard:** Distributor-level sales, regional performance and retailer coverage.

c. **Retailer Analytics Dashboard:** Retailer-level purchases, sales contribution and channel performance.

d. **Inventory Dashboard:** Stock availability, inventory value, stock-outs and inventory ageing where supporting data is available.

e. **Order Fulfilment Dashboard:** Total orders, pending orders, fulfilled quantities and fulfilment rates.

f. **Shipment Performance Dashboard:** Shipment volumes, delivery delays and on-time delivery performance.

g. **Executive Dashboard:** Consolidated business KPIs covering sales, distribution, inventory and supply chain.

### 6.3 Operational Outputs

- Daily pipeline execution reports.
- File ingestion and processing audit logs.
- Data-quality validation reports.
- Rejected-record reports.
- Pipeline failure and retry logs.


## 7. Project Data Volume

The initial project will use medium-scale synthetic data to demonstrate scalable data engineering practices.

| Dataset | Approximate Volume |
|---|---:|
| Categories | 4 |
| Subcategories | 20 |
| Brands | 20 |
| Products | 300 |
| Distributors | 100 |
| Retailers | 20,000 |
| Warehouses | 50 |
| Geography records | 1,000 |
| Sales transactions | 1,000,000 |
| Orders | 200,000–300,000 |
| Inventory snapshots | 500,000–1,000,000 |
| Shipments | 150,000–250,000 |

---

**Final Project Goal:** Build a production-style, synthetic India FMCG data engineering platform that integrates sales, distribution, inventory, order and shipment data into a centralized Snowflake analytical environment, enabling reliable and consistent business reporting through Power BI.