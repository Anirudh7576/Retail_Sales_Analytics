                  Source Systems
       (CRM, Website, POS, Mobile App)
                     │
                     ▼
      Python Data Generator (Project Simulation)
                     │
                     ▼
              Upload Files to Amazon S3
                     │
                     ▼
          Airflow Scheduled ELT Pipeline
                     │
                     ▼
       Load Source Data into Snowflake RAW
                     │
                     ▼
      Data Validation & Quality Checks
             │                     │
             │                     ▼
             │           Rejected Records
             │          (Error Table / Log)
             ▼
 Transform RAW → SILVER (Data Cleansing)
                     │
                     ▼
 Transform SILVER → GOLD
 (Business Rules & Aggregations)
                     │
                     ▼
        Refresh Power BI Dataset
                     │
                     ▼
        Business Dashboards & Reports