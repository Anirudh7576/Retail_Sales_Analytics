## 1. End-to-End Project Workflow

```text
                 SYNTHETIC FMCG SOURCE SYSTEMS
              (India – Sales & Supply Chain)
                             |
          +------------------+------------------+
          |                  |                  |
          v                  v                  v
    MASTER DATA         TRANSACTION DATA    INVENTORY DATA
       (JSON)             (CSV / JSON)        (PARQUET)
          |                  |                  |
          |                  |                  |
    Categories           Sales (CSV)       Inventory
    Subcategories        Orders (CSV)      Snapshots
    Brands               Shipments (JSON)
    Products
    UOM
    Geography
    Distributors
    Retailers
    Warehouses
    Sales Channels
    Distributor-Retailer Mapping
    Dates
          |                  |                  |
          +------------------+------------------+
                             |
                             v
                 PYTHON DATA GENERATION
                  (Faker + Pandas)
                             |
                             v
               SOURCE DATA VALIDATION
             (Schema, Business Keys, FK)
                    |             |
                 Valid          Invalid
                    |             |
                    |             v
                    |       Local Error Logs
                    v
                 AMAZON S3
               (LANDING ZONE)
                             |
                             v
                 APACHE AIRFLOW
              (Scheduled Batch ELT)
                             |
                             v
                 SNOWFLAKE RAW
              (Source Data Ingestion)
                             |
                             v
             DATA QUALITY & VALIDATION
          (Duplicates, Nulls, Types, FK)
                    |             |
                  Valid         Invalid
                    |             |
                    |             v
                    |      AUDIT / REJECTED
                    |        RECORDS
                    v
                 SNOWFLAKE SILVER
           (Cleaned & Standardized Data)
                             |
                             v
                 SNOWFLAKE GOLD
             (Dimensional Data Model)
                             |
           +-----------------+-----------------+
           |                 |                 |
           v                 v                 v
      FACT TABLES       DIMENSIONS         BUSINESS KPIs
           |                 |                 |
      FACT_SALES        DIM_PRODUCT        Net Sales
      FACT_ORDERS       DIM_BRAND          Gross Profit
      FACT_INVENTORY    DIM_CATEGORY       Stock on Hand
      FACT_SHIPMENTS    DIM_DISTRIBUTOR    Order Fulfilment
                        DIM_RETAILER       Delivery Performance
                        DIM_GEOGRAPHY
                        DIM_WAREHOUSE
                        DIM_DATE
                        Other Dimensions
           |                 |                 |
           +-----------------+-----------------+
                             |
                             v
                    POWER BI REFRESH
                             |
                             v
                 BUSINESS DASHBOARDS
                             |
           +-----------------+-----------------+
           |                 |                 |
           v                 v                 v
      SALES ANALYTICS   DISTRIBUTION     SUPPLY CHAIN
                        ANALYTICS         ANALYTICS
           |                 |                 |
      Sales Revenue     Distributor Sales  Inventory Levels
      Product Sales     Retailer Coverage  Stock Availability
      Brand Sales       Regional Sales     Order Fulfilment
      Sales Trends      Channel Sales      Shipment Performance
```

## 2. Workflow Stages

| Step | Component | Responsibility |
|---|---|---|
| 1 | Synthetic Source Systems | Simulate FMCG master, sales, orders, inventory and shipment data |
| 2 | Python Data Generator | Generate realistic data using Faker and Pandas |
| 3 | Source Validation | Validate schemas, required fields, business keys and relationships |
| 4 | Amazon S3 | Store CSV, JSON and Parquet files in the landing zone |
| 5 | Apache Airflow | Schedule and orchestrate ingestion and transformation workflows |
| 6 | Snowflake RAW | Ingest source records with file and load metadata |
| 7 | Data Quality Checks | Detect duplicates, invalid references, missing values and business-rule violations |
| 8 | Rejected Records / Audit | Track failed validations, rejected records and pipeline execution details |
| 9 | Snowflake SILVER | Clean, deduplicate, standardize and integrate source data |
| 10 | Snowflake GOLD | Build dimensions, facts and business metrics |
| 11 | Power BI Refresh | Refresh the analytical semantic model after successful GOLD processing |
| 12 | Business Dashboards | Present sales, distribution, inventory and supply-chain KPIs |

## 3. Data Formats

| Dataset Category | Format | Storage |
|---|---|---|
| Master Data | JSON | Amazon S3 |
| Sales Transactions | CSV | Amazon S3 |
| Orders | CSV | Amazon S3 |
| Inventory Snapshots | Parquet | Amazon S3 |
| Shipments | JSON | Amazon S3 |

## 4. Workflow Execution Rules

1. Master data must be loaded and validated before dependent transaction data is published to GOLD.
2. Files must be tracked using unique file identifiers or file paths and processing status.
3. Failed pipeline tasks must support controlled retries without duplicating previously processed data.
4. Invalid records must be quarantined or rejected according to defined business rules.
5. All pipeline executions must be logged for monitoring and troubleshooting.
6. SILVER transformations must enforce data types, deduplication and referential integrity.
7. GOLD fact tables must use valid dimension surrogate keys.
8. Power BI refresh must run only after required GOLD transformations and validation checks succeed.
9. Source files must be retained or archived according to the defined retention policy.
10. The initial implementation will use scheduled batch processing. Incremental and event-driven processing can be introduced later.

## 5. Monitoring and Error Handling

The platform should maintain operational audit tables:

| Audit Table | Purpose |
|---|---|
| FILE_LOAD_AUDIT | Tracks source-file processing and load status |
| PIPELINE_RUN_LOG | Tracks pipeline executions, duration and failures |
| DATA_QUALITY_RESULTS | Stores validation results and rule failures |
| REJECTED_RECORDS | Stores rejected record references, reasons and source metadata |

Airflow handles orchestration retries and failure notifications. Snowflake audit tables record ingestion and transformation results.

## 6. Business Outcome

The completed platform will provide:

- Automated batch ingestion of multiple source formats.
- Reliable and traceable data processing.
- Validated master and transactional data.
- Consistent sales and supply-chain metrics.
- Historical analytical data.
- Power BI dashboards for business decision-making.
