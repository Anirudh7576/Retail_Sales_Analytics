1. Business cases:

   | Business Case                      | Business Impact                    | ELT Solution                                                              |
   | ---------------------------------- | ---------------------------------- | ------------------------------------------------------------------------- |
   | Duplicate sales records            | Incorrect revenue reports          | Remove duplicates in the SILVER layer using business keys.                |
   | Missing product information        | Incomplete sales analysis          | Reject invalid records and log them for investigation.                    |
   | Late-arriving files                | Delayed dashboards                 | Airflow detects late files and processes them automatically.              |
   | Incorrect payment methods          | Finance reconciliation issues      | Validate payment methods against the payment dimension.                   |
   | Missing geography                  | Regional reports become inaccurate | Load unknown values into a default "Unknown" geography and log the issue. |
   | Negative quantity                  | Incorrect inventory and revenue    | Reject invalid records during data quality validation.                    |
   | Null order date                    | Time-based reports fail            | Move records to a rejected area for business review.                      |
   | Duplicate customer records         | Incorrect customer analytics       | Deduplicate customer records during transformation.                       |
   | Data arrives from multiple sources | Inconsistent reporting             | Standardize and integrate data in the SILVER layer.                       |
   | Manual report preparation          | High operational effort            | Automate the pipeline using Airflow and scheduled ELT jobs.               |

2. Business benefits:

   a) Faster decision-making.
   b) Improved data quality.
   c) Reduced manual effort.
   d) Consistent reporting across departments.
   e) Historical data available for trend analysis.
   f) Better dashboard performance.
   g) Improved business confidence in reports.

 3. Technical Mapping

   | Business Problem    | Technology Used |                       Why                             |
   | ------------------- | --------------- | ----------------------------------------------------- |
   | Data quality        | Snowflake       | Validate and clean data in the SILVER layer.          |
   | Workflow automation | Airflow         | Schedule and monitor ELT jobs.                        |
   | Historical storage  | Amazon S3       | Store raw source files for auditing and reprocessing. |
   | Fast analytics      | Snowflake       | Separate compute and storage for scalable analytics.  |
   | Reporting           | Power BI        | Interactive dashboards for business users.            |
 
