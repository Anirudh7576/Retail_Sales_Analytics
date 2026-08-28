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

import json

data = {
    "name": "Anirudh",
    "age": 35
}

json_string = json.dumps(data, indent=4)

print(json_string)

import json

json_string = '{"name": "Anirudh", "age": 35}'

data = json.loads(json_string)

print(data)
print(data["name"])