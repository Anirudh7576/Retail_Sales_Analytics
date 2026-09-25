# local
# import csv

# path = r"sales_table.csv"

# with open(path, "r") as data:
#     reader = csv.reader(data)

#     for row in reader:
#         print(row)
# ========================================================================
# csv for data analysis

# import pandas as pd

# path = r"https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv"

# data = pd.read_csv(path)
# print(data)

# =========================================================================
# csv by requests

# import requests as requests
# from pathlib import Path

# path = "https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv"

# response = requests.get(path)

# print(response)
# ==========================================================================
# import requests as requests
# from pathlib import Path

# path = "https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv"

# response = requests.get(path)

# with open(response, "w") as file:
# print(response)
# ============================================================================
# for read from online and load it to local folder
# import csv
# import requests
# from io import StringIO

# url = "https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv"

# response = requests.get(url)
# response.raise_for_status()

# reader = csv.reader(StringIO(response.text))
# output_path = r"C:/Users/Anirudh Gogikar/Downloads/csv_file_loading.csv"

# with open(output_path, "w", newline= "", encoding= "utf-8") as file:
#     writer = csv.writer(file)

#     for row in reader:
#         writer.writerow(row)
# print(row)
# ------------------------------------------
# with open(output_path, "wb") as file:
#     file.write(response.content)
# print(file)
# ===========================================
# import requests

# url = "https://dummyjson.com/products"

# response = requests.get(url=url)
# response.raise_for_status()
 
# data = response.json()

# for row in data["products"]:
#     print(row)
# ======================================================
# import json

# data = {
#     "name": "Anirudh",
#     "age": 35
# }

# json_string = json.dumps(data, indent=4)

# print(json_string)

# import json

# json_string = '{"name": "Anirudh", "age": 35}'

# data = json.loads(json_string)

# print(data)
# print(data["name"])

# import requests

# url = "https://dummyjson.com/products"

# output_path = r"C:/Users/Anirudh Gogikar/Downloads/products.json"

# response = requests.get(url, timeout=30)
# response.raise_for_status()

# with open(output_path, "wb") as file:
#     file.write(response.content)

# print("JSON file downloaded successfully")

# import json

# data = {
#     "name": "Anirudh",
#     "age": 35
# }

# json_string = json.dumps(data, indent=4)

# print(json_string)

# import json

# json_string = '{"name": "Anirudh", "age": 35}'

# data = json.loads(json_string)

# print(data)
# print(data["name"])
# ==============================================

    

# import pandas as pd
# from pathlib import Path

# folder_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/kaggle")
# archive_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/archive")

# for file_path in folder_path.glob("*.csv"):
#     df = pd.read_csv(file_path)
#     print(file_path.name)
# =====================================================================
# import pandas as pd
# from pathlib import Path
# import shutil

# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/kaggle")
# archive_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/archive")

# archive_path.mkdir(parents= True, exist_ok = True)

# for file_path in source_path.iterdir():

#     if file_path.is_file():

#         try:

#             destination = archive_path/file_path.name

#             shutil.move(file_path, destination)

#             print(f"move file {file_path.name}")

#         except:

#             print("file does not exist")
# ==================================================
# import pandas as pd
# from pathlib import Path
# import shutil
# from datetime import datetime

# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/kaggle")
# archive_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/archive")

# archive_path.mkdir(parents = True , exist_ok = True)
            
# for file_path in source_path.iterdir():

#     if file_path.is_file():

#         try:

#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#             destination = archive_path/f"{file_path.stem}_{timestamp}{file_path.suffix}"

#             shutil.move(file_path, destination)

#             print(f"moved file: {file_path.name}")

#         except Exception as e:
#             print(f"no file found {file_path.name}, {e}")
# ====================================================================
# import pandas as pd
# from pathlib import Path
# import shutil
# from datetime import datetime

# destination_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/kaggle")
# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/archive")

# destination_path.mkdir(parents = True , exist_ok = True)
            
# for file_path in source_path.iterdir():

#     if (file_path.is_file() and file_path.name.startswith("csv_file_loading")):


#         try:

#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#             destination = destination_path/f"{file_path.stem}_{timestamp}{file_path.suffix}"

#             shutil.move(file_path, destination)

#             print(f"moved file: {file_path.name}")

#         except Exception as e:
#             print(f"no file found {file_path.name}, {e}")
# ==============================================================
# from pathlib import Path
# import pandas as pd

# destination_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/kaggle/csv_file_loading_20260902_163008.csv")

# df = pd.read_csv(destination_path)
# print(len(df))
# =============================================================
# import pandas as pd
# from pathlib import Path

# destination_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/kaggle/csv_file_loading_20260902_163008.csv")

# df = pd.read_csv(destination_path)
# df = df.drop_duplicates()

# print(len(df))
# =============================================================
# from pathlib import Path
# import pandas as pd

# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/archive")
# destination_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/merged.csv")

# dataframes = []

# for file_path in source_path.glob("*csv"):
#     df = pd.read_csv(file_path)
#     dataframes.append(df)

# merged_df = pd.concat(dataframes, ignore_index = True)
# merged_df.to_csv(destination_path, index = False)
# ==============================================================
# Handle missing file exception
# from pathlib import Path

# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/archive")

# def handle_missing_file():
#     try:
#         for file_name in source_path.iterdir():

#             if (file_name.is_file() and file_name.name.startswith("csv_file_loading")):

#                 print(f"file found {file_name.name}")

#     except FileNotFoundError:
#         print("file not found")

#     except PermissionError:
#         print("permissions are not found")

#     except Exception as error:

#         print(f"Error file name: {file_name.name}")

# ===============================================================
# import pyodbc
# import pandas as pd

# server = r"LAPTOP-QHJSLGBV\SQLEXPRESS012"
# database = "AdventureWorksDW2025"

# connection = pyodbc.connect(
#             f"DRIVER={{ODBC Driver 18 for SQL Server}};"
#             f"SERVER={server};"
#             f"DATABASE={database};"
#             f"Trusted_Connection=yes;"
#             f"TrustServerCertificate=yes;"
#         )

# print("Connected successfully!")

# query = "select top 10 * from [dbo].[vTargetMail]"

# df = pd.read_sql(query, connection)
# print(df)

# connection.close()        
# =======================================================

# import pandas as pd
# from sqlalchemy import create_engine
# from urllib.parse import quote_plus

# server = r"LAPTOP-QHJSLGBV\SQLEXPRESS01"
# database = "AdventureWorksDW2025"

# connection_string = (
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     f"SERVER={server};"
#     f"DATABASE={database};"
#     "Trusted_Connection=yes;"
#     "TrustServerCertificate=yes;"
# )

# engine = create_engine(
#     "mssql+pyodbc:///?odbc_connect=" + quote_plus(connection_string)
# )

# query = "SELECT TOP 100 * FROM dbo.DimCustomer"

# df = pd.read_sql(query, engine)

# print(df)
# ========================================================================

# import pandas as pd
# from sqlalchemy import create_engine
# from urllib.parse import quote_plus
# from pathlib import Path

# # --------------------------------------------------
# # 1. SQL Server connection
# # --------------------------------------------------

# server = r"LAPTOP-QHJSLGBV\SQLEXPRESS01"
# database = "AdventureWorksDW2025"

# connection_string = (
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     f"SERVER={server};"
#     f"DATABASE={database};"
#     "Trusted_Connection=yes;"
#     "TrustServerCertificate=yes;"
# )

# engine = create_engine(
#     "mssql+pyodbc:///?odbc_connect="
#     + quote_plus(connection_string)
# )

# # --------------------------------------------------
# # 2. Last successfully processed ID
# # --------------------------------------------------

# watermark_file = Path("last_processed_id.txt")

# if watermark_file.exists():
#     last_processed_id = int(
#         watermark_file.read_text().strip()
#     )
# else:
#     last_processed_id = 0

# print(f"Last processed SalesID: {last_processed_id}")

# # --------------------------------------------------
# # 3. Incremental query
# # --------------------------------------------------

# query = """
# SELECT
#     SalesID,
#     CustomerID,
#     ProductID,
#     SalesDate,
#     Quantity,
#     SalesAmount
# FROM dbo.FactSales
# WHERE SalesID > %(last_id)s
# ORDER BY SalesID
# """
# # --------------------------------------------------
# # 4. Read data in chunks
# # --------------------------------------------------

# total_processed = 0
# max_processed_id = last_processed_id

# for chunk in pd.read_sql(
#     query,
#     engine,
#     params={"last_id": last_processed_id},
#     chunksize=100_000
# ):

#     print(f"Received {len(chunk)} rows")

#     # --------------------------------------------------
#     # 5. Transform / validate
#     # --------------------------------------------------

#     chunk["SalesAmount"] = chunk["SalesAmount"].fillna(0)

#     chunk = chunk.drop_duplicates(
#         subset=["SalesID"]
#     )

#     # --------------------------------------------------
#     # 6. Process the chunk
#     # --------------------------------------------------

#     # Example:
#     # chunk.to_csv(...)
#     # upload to S3
#     # insert into Snowflake
#     # etc.

#     print(
#         f"Processing SalesID "
#         f"{chunk['SalesID'].min()} "
#         f"to "
#         f"{chunk['SalesID'].max()}"
#     )

#     # --------------------------------------------------
#     # 7. Update watermark
#     # --------------------------------------------------

#     max_processed_id = max(
#         max_processed_id,
#         chunk["SalesID"].max()
#     )

#     total_processed += len(chunk)


# # --------------------------------------------------
# # 8. Save watermark
# # --------------------------------------------------

# if max_processed_id > last_processed_id:

#     watermark_file.write_text(
#         str(max_processed_id)
#     )

# print("--------------------------------")
# print(f"Rows processed: {total_processed}")
# print(f"New watermark : {max_processed_id}")
# print("--------------------------------")

# engine.dispose()

# # ===========================================
# 1. Daily file processing at 8:00 AM

# from datetime import datetime
# from airflow import DAG
# from airflow.provides.standard.operators.python import PythonOperator
# from airflow.provides.standard.operators.empty import EmptyOperator

# # check the file
# def check_file():
#     import os

#     source_path = ""

#     if os.path.exists(source_path):
#         print("source file exist")

#     else:
#         raise FileNotFoundError (
#             print(f"source file not exist in : {source_path} ")
#         )

# # process the file
# def process_file():

#     import pandas as pd

#     df = pd.read_csv(source_path)

#     print("file processing starting")

#     print(f"number of rows are : {len(df)}")

#     df["total"] = df["amount"] - df["discount"]

#     print(df)

# #  load the file in datalake
# def load_file():
#     import pandas as pd
#     destination_path = ""
#     df = pd.write_csv(destination_path)

#     print("files are loaded")

# #  create a DAG
# with DAG (
#     task_id = "sales_file",
#     shedule = "* 8 0 0 0",
#     start_date = datetime(2026,9,11),
#     catchup = False,
#     tags = ["sales", "total"]
# ) as dag:

#     start = EmptyOperator(
#         task_id = "start"
#     )

#     file_check_task = PythonOperator(
#         task_id = "check file exist",
#         python_callable = check_file
#     )

#     process_file_task = PythonOperator(
#         task_id = "process file",
#         python_callable = process_file
#     )

#     load_file_destination_task = PythonOperator(
#         take_id = "load_file",
#         python_callable = load_file
#     )

#     end = PythonOperator(
#         task_id = "end"
#     )

# start >> file_check_task
# file_check_task >> process_file_task
# process_file_task >> load_file_destination_task
# load_file_destination_task >> end

# ======================================================================
# define task dependencies 
# from datetime import datetime
# from airflow import DAG
# from airflow.providers.standard.operators.python import PythonOperator
# from airflow.providers.standard.operators.empty import EmptyOperator
# from airflow.providers.standard.operators.python import PythonSensor

# def check_file():
#     s3_path = "s3/folders/orders/orders.csv"
#     latest_file = max(s3_path)

#     import os

#     os.path.exists(latest_file)

#     print(f"latest file : {latest_file}")

# def validate_file():

#     import pandas as pd
#     s3_path = "s3/folders/orders/orders.csv"
#     latest_file = max(s3_path)

#     df= pd.read_csv(latest_file)
#     total_rows = len(df)

#     if total_rows == 0:
#         raise ValueError (
#             print("File does not exist rows")
#         )

# def snowflake_load():
#     import pandas as pd
#     snowflake_path = "snowflake/fact_orders"

#     df = pd.write_csv(snowflake_path)

#     print(f"data loaded into : {snowflake_path}")

# with DAG(
#     task_id = "read_validate_load",
#     start_date = datetime(2026,9,11),
#     catchup = False,
#     tags = ["read", "validate", "load"]
# ) as dag:

#     start = EmptyOperator(
#         task_id = "start"
#     )

#     read_task = PythonSensor(
#         task_id = "read the latest file",
#         python_callable = check_file
#     )

#     validate_task = PythonOperator(
#         task_id = "validate file",
#         python_callable = validate_file
#     )

#     load_file_task = PythonOperator(
#         task_id = "load file",
#         python_callable = snowflake_load
#     )

#     end = PythonOperator(
#         task_id = "end"
#     )

# start >> read_task
# read_task >> validate_task
# validate_task >> load_file_task
# load_file_task >> end
# ==================================================
# Retry failed operation

# import requests
# import time

# url = "https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv."

# max_attempts = 3

# try:

#     for attempt in range(1, max_attempts + 1):

#         print(f"For a attempts : {attempt}/{max_attempts}")

#         response = requests.get(url,
#                                 timeout = 10)

#         response.raise_for_status()

#         print("file downloaded successfully")
#         print(f"HTTP status is : {response.status_code}")

#         break

# except requests.exceptions.RequestException as error:

#     print(f"request failed :{error}")

#     if attempt == max_attempts:
#         print("Reached to max attempts")
#         raise

#     print("wait for 5 sec")
#     time.sleep(5)
# =============================================================================

# import requests
# import time

# url = "https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv"

# max_retries = 3

# for attempt in range(1, max_retries + 1):

#     try:
#         print(f"Downloading file - Attempt {attempt}/{max_retries}")

#         response = requests.get(
#             url,
#             timeout=10
#         )

#         if response.status_code == 404:
#             raise FileNotFoundError(
#                 f"File does not exist: {url}"
#             )

#         response.raise_for_status()

#         print("File downloaded successfully")

#         # Process the file here
#         with open("europe_pop.csv", "wb") as file:
#             file.write(response.content)

#         print("File saved successfully")

#         break

#     except FileNotFoundError as error:

#         print(f"Permanent error: {error}")
#         raise

#     except requests.exceptions.RequestException as error:

#         print(f"Network error: {error}")

#         if attempt == max_retries:
#             print("Maximum retry attempts reached")
#             raise

#         wait_time = 5 * attempt

#         print(
#             f"Retrying after {wait_time} seconds..."
#         )

#         time.sleep(wait_time)
# =============================================================
#  Handle API requests

# if response.status_code == 400:
#     raise ValueError("Bad API request")

# if response.status_code == 401:
#     raise ValueError("Unatherized - check API credentials")

# if response.status_code == 404:
#     raise ValueError("API endpoint not found")
# =============================================================
#  Handle timeout exceptions

# import requests
# import time

# url = "https://api.example.com/customers"

# max_retries = 3

# for attempt in range(1, max_retries + 1):

#     try:
#         print(f"API request - Attempt {attempt}/{max_retries}")

#         response = requests.get(
#             url,
#             timeout=10
#         )

#         response.raise_for_status()

#         data = response.json()

#         print("API request successful")
#         print(data)

#         break

#     except requests.exceptions.Timeout as error:

#         print("API is not responding within 10 seconds")

#         if attempt == max_retries:
#             print("Maximum retry attempts reached")
#             raise

#         print("Retrying in 5 seconds...")
#         time.sleep(5)

#     except requests.exceptions.RequestException as error:

#         print(f"API request failed: {error}")

#         if attempt == max_retries:
#             print("Maximum retry attempts reached")
#             raise

#         print("Retrying in 5 seconds...")
#         time.sleep(5)
# ==========================================================
# Handle authentication failure

# headers = "BEARER token"

# response = requests.get(url,
#                         headers,
#                         timeout = 5)

# if response.status_code == 401:
#     print("Authentication error : {headers}")

#     raise PermissionError("API authentication error")
# ============================================================
# Handle invalid json
# my logic => check for record => if it is starts with certain prefix then and is json => else except FileNotFoundError

# from pathlib import Path
# import json
# url = Path("https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv")

# for file in url.iterdir():

#     try:
#         if (
#             file.is_file() and 
#             file.name.starswith() == "customer" and 
#             file.suffix.lower() == ".json"):

#             with file.open("r", encoding= "utf-8") as json_data:
#                 data= json.load(json_data)

#             print("load file successfully")

#     except json.JSONDecoderError as error:

#         print(f"invalid JSON file :{file.name}")
#         print(f"JSON error: {error}")

#     except FileNotFoundError:

#         print(f"file is not found: {file}")

# ========================================================================
# skip bad record while processing
# import json

# with open("r", "customers.csv", encoding = "utf-8") as file:
#     records = json.load(file)


#     for row in records:
#         try:

#             row["customer_id"] = int(row["customer_id"])
#             row["name"] = str(row["name"])

#             print("file loaded succesfully")

#         except (KeyError, ValueError) as error:

#             print(f"data is invalid : {error}")

#             continue
# =======================================================================
# log failed records

# import json
# import logging

# logging.basicConfig(
#     filename="failed_records.log",
#     level=logging.ERROR,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# records = [
#     {"customer_id": 101, "name": "Anirudh"},
#     {"customer_id": "ABC", "name": "Rahul"},
#     {"name": "John"},
#     {"customer_id": 104, "name": "David"}
# ]

# for record in records:
#     try:
#         customer_id = int(record["customer_id"])
#         customer_name = record["name"]

#         print(f"Processing customer: {customer_id} - {customer_name}")

#     except (ValueError, KeyError) as error:
#         logging.error(
#             f"Failed record: {record} | Reason: {error}"
#         )

#         continue
# =========================================
# rollback database transaction

# import pyodbc

# connection = pyodbc.connect(
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     r"SERVER=LAPTOP-QHJSLGBV\SQLEXPRESS01;"
#     "DATABASE=AdventureWorksDW2025;"
#     "Trusted_Connection=yes;"
#     "TrustServerCertificate=yes;"

# )

# cusror = connection.cursor()

# try:

#     # process the data
#     cusror.commit()

# except Exception as error:

#     cusror.rollback()

# finally:
#     cusror.close()
#     connection.close()
# ===========================================
#  Raise custom exception

# try:
#     number = int("ABC")

# except Exception as error:
#     raise ValueError(f"Failed to convert value: {error}")
# =============================================
# Global exception handler

# import sys
# import logging

# logging.basicConfig(
#     filename = "global_exception.log",
#     level = logging.ERROR,
#     format = "%(asctime)s - %(levelname)s - %(messages)s"
# )

# def global_exception_handler(exception_type, excetion_value, traceback):

#     logging.error(

#         "Unhandled error",

#         exc_info= (exception_type, excetion_value, traceback)
#     )


#     print("unexpected file error found, please check log file")


# sys.excepthook = global_exception_handler
# ======================================================
# Handle missing file exception

# import pandas as pd
# from pathlib import Path

# url = Path(r"C:/Users/Anirudh Gogikar/Downloads/customer")

# try:

#     for file in url.iterdir():

#         if (file.is_file() and file.name.startswith("..")):

#             # with open(file, "r") as data:
#             #     df = pd.read_csv(data)

#             print(f"file name: {file.name}")

# except FileNotFoundError as error:

#     print(f"file missing : {error}")

# from pathlib import Path

# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/customer")

# file_path = source_path/"erged.csv"

# try:

#     if not source_path.exists():
#         raise FileNotFoundError(
#         f"file does not exist: {source_path}")
   

#     if not file_path.exists:
#         raise FileNotFoundError(
#         f"file does not exist: {file_path}")
    

# except FileNotFoundError as error:
#     print(f"File does not exist : {error}")

# except PermissionError as error:
#     print(f"Authentication issue : {error}")

# except Exception as error:
#     print(f"Unexcepted error : {error}")
# ==============================================================
# from pathlib import Path
# import pandas as pd
# import shutil
# import logging

# source_path = Path(r"C:/Users/Anirudh Gogikar/Downloads/customer")

# failed_path = source_path / "check invalid data"
# failed_path.mkdir(parents=True, exist_ok=True)

# logging.basicConfig(
#     filename="csv_validation.log",
#     level=logging.ERROR,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# expected_columns = ["date","year", "month", "week"]

# for file_path in source_path.glob("*.csv"):

#     try:
#         print(f"Processing: {file_path.name}")

#         # Read CSV
#         df = pd.read_csv(file_path)

#         if list(df.columns) != expected_columns:
#             raise ValueError(
#                 f"Invalid CSV header. Expected: {expected_columns}, "
#                 f"Found: {list(df.columns)}"
#             )

#         print("CSV is valid")
#         print(df)


#     except pd.errors.ParserError as error:

#         logging.error(
#             f"Invalid CSV format: {file_path.name} | Reason: {error}"
#         )

#         # Move invalid file to failed folder
#         destination = failed_path / file_path.name

#         shutil.move(file_path, destination)

#         print(
#             f"Invalid CSV format: {file_path.name}"
#         )
#         print(
#             f"Moved to failed folder: {destination}"
#         )

#     except FileNotFoundError:

#         logging.error(
#             f"File not found: {file_path}"
#         )

#         print(f"File not found: {file_path}")

#     except PermissionError:

#         logging.error(
#             f"Permission denied: {file_path}"
#         )

#         print(f"Permission denied: {file_path}")

#     except Exception as error:

#         logging.error(
#             f"Unexpected error: {file_path.name} | "
#             f"Reason: {error}"
#         )

#         print(
#             f"Unexpected error: {file_path.name}"
#         )




















# from pathlib import Path
# import pandas as pd
# import logging

# source_path1 = ""

# logging.basicConfig(
#     filename= "invalid_details_file.csv",
#     level = logging.ERROR,
#     format = "%(asctime)s - %(error)s - %(message)s"
# )

# failed_path1 =  source_path1/"failed"
# Path.mkdir(parents = True, exist_ok= True)

# existed_columns = ["day", "year", "week","month"]

# for file_name in source_path1.glob("*.csv"):

# try:

#         df = pd.read_csv(file_name)

#         print("File processing started")

#         if list(df.columns) != existed_columns:
#              raise ValueError(
#                   print(f"file name : {file_name.name}")
#              )

#         print(f"")

# ===================================================================
# create reusable ETL function

# logic >> extract data from AWS S3 (intiate credentials)/ sql server >> transform the data >> load it into snowflake.

# import boto3
# import pandas as pd
# from io import BytesIO

# s3 = boto3.client("s3")

# bucket_name = "retail-sales-analytics-898565151550-us-east-1-an"
# s3_key = "landing/sales/sales_20260829_203556.json"

# response = s3.get_object(
#     Bucket = bucket_name,
#     Key = s3_key
# )

# df = pd.read_json(
#         BytesIO(response["Body"].read())
# )

# df["absolute_amount"] = abs(df["profit_amount"])
# df = df.drop_duplicates()
# print(df)

# =================================================================================
