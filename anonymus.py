# local
import csv

# path = r"sales_table.csv"

# with open(path, "r") as data:
#     reader = csv.reader(data)

#     for row in reader:
#         print(row)
# ========================================================================
# online csv url
import pandas as pd

path = r"https://raw.githubusercontent.com/softhints/Pandas-Exercises-Projects/refs/heads/main/data/europe_pop.csv"

data = pd.read_csv(path)
print(data)



