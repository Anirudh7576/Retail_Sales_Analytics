# 1. File arrives every day at 8:00 am in s3 (csv) >> snowflake raw  >> snowflake_silver >> snowflake_gold >> power BI

from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator

def check_file():

    print(f"latest file is available at {datetime.now()}")

def validate_file():
    # is it empty
    # it has all required columns in seq
    # all datatypes are corrected
    print("validation completed")

def load_to_snowflakeRAW():

    print("files are loaded")

def transform_data_silver():

    # remove duplicate rows
    # remove null rows
    # remove withspaces in stirgs
    # rename columns
    # select columns
    # chage datatypes
    # validate values
    print("transformation completed")

def load_to_datawarehouse():
    # by using stage/task perform incremetal data loading

    print("data loaded into warehouse")

def refresh_powrerbi():
    print("power BI refresh completed")

# =====================================================

with DAG(

    dag_id     = "fact_sales_file",
    start_date = datetime(2026,10,1),
    schedule   = "0 8 * * *",
    catchup    = False,
    tags       = ["sales","snowflake", "powerbi","raw"]

) as dag:

    start = EmptyOperator(
        task_id = "start"
    )

    check_file_task= PythonOperator(
        task_id = "check",
        python_callable = check_file
    )

    valid_s3_file_taks= PythonOperator(
        task_id = "extact",
        python_callable = validate_file
    )

    raw_snowflake_task = PythonOperator(
        task_id = "raw",
        python_callable = load_to_snowflakeRAW
    )

    silver_snowflake_task = PythonOperator(
        task_id = "silver",
        python_callable = transform_data_silver
    )

    datawarehouse_task = PythonOperator(
        task_id = "datawarehouse",
        python_callable = load_to_datawarehouse
    )

    powerbi_task = PythonOperator(
        task_id = "powerbi refresh",
        python_callable = refresh_powrerbi
    )

    end = EmptyOperator(
        task_id = "End"
    )

start >> check_file_task >> valid_s3_file_taks >> raw_snowflake_task >> silver_snowflake_task >> datawarehouse_task >> powerbi_task >> end 

# ======================
# A DAG with parallel tasks

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonBrachOperator


with DAG(

    dag_id = "executing parallel tasks",
    start_date = datetime(2026,10,1),
    shedule = "0 8 * * *",
    catchup = False,
    tags = ["parallel", "dag", "empty"]

) as dag:

    start = EmptyOperator(
        task_id = "start"
    )

    task_2 = PythonOperator(
        task_id = "check_file",
        python_Callable = "check_file_function"
    )

    task_3 = PythonBrachOperator(
        task_id = "valid_file",
        python_Callable = "check_valid_file_function"
    )

    task_4 = PythonBrachOperator(
        task_id = "invalid file",
        python_Callable = "check_invalid_file_function"
    )

    end = EmptyOperator(
        task_id = "end"
    )

start >> task_2

task_2 >> task_3
task_2 >> task_4

task_3 >> end
task_4 >> end

