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

# server = r"LAPTOP-QHJSLGBV\SQLEXPRESS01"
# database = "AdventureWorksDW2025"

# connection = pyodbc.connect(
#     f"DRIVER={{ODBC Driver 18 for SQL Server}};"
#     f"SERVER={server};"
#     f"DATABASE={database};"
#     f"Trusted_Connection=yes;"
#     f"TrustServerCertificate=yes;"
# )

# print("Connected successfully!")

# query = "select top 10 * from [dbo].[vTargetMail]"

# df = pd.read_sql(query, connection)
# print(df)

# connection.close()

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

server = r"LAPTOP-QHJSLGBV\SQLEXPRESS01"
database = "AdventureWorksDW2025"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

engine = create_engine(
    "mssql+pyodbc:///?odbc_connect=" + quote_plus(connection_string)
)

query = "SELECT TOP 100 * FROM dbo.DimCustomer"

df = pd.read_sql(query, engine)

print(df)

