1. Source systems - Synthetic data generation
                    Master data (JSON):
                     Products, Brands, Categories, Subcategories, Geography, Distributors, Retailers, Warehouses, UOM, Sales Channels
                    Transactional data (Multiple formats):
                     Sales (CSV), Orders (CSV), Inventory (Parquet), Shipments (JSON)
                            |
                            |
                            V

2. AWS S3 — Data Lake

       Landing → Archive → Rejected
       purpose: Organized by master and transaction datasets    
                            |
                            |
                            V

3. Apache Airflow — Orchestration

       purpose: Scheduling, Dependencies, Retries, Monitoring, Error handling
                            |
                            |
                            V

4. Snowflake Data Warehouse
                     RAW
       Original source data and ingestion metadata

                     SILVER
       Cleaning, Standardization, Deduplication,Data quality

                     GOLD
       Business dimensions, Fact tables, Aggregations, KPIs
                            |
                            |
                            V      

5. Power BI - Business Intelligence
      purpose: Sales, Distribution, Inventory, Supply Chain dashboards