import pandas as pd
from pathlib import Path

file_path = Path(
    "data/generated/transactions/orders/"
    "orders_20261118_120729_181778.csv"
)

df = pd.read_csv(file_path)

# Convert columns to datetime
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["requested_delivery_date"] = pd.to_datetime(
    df["requested_delivery_date"], errors="coerce"
)
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")

checks = {
    "Order dates within 2026": (
        df["order_date"].between("2026-01-01", "2026-12-31").all()
    ),
    "Delivery date >= order date": (
        (df["requested_delivery_date"] >= df["order_date"]).all()
    ),
    "Created timestamp <= updated timestamp": (
        (df["created_at"] <= df["updated_at"]).all()
    ),
    "Created date matches order date": (
        (df["created_at"].dt.date == df["order_date"].dt.date).all()
    ),
    "No invalid datetime values": (
        df[[
            "order_date",
            "requested_delivery_date",
            "created_at",
            "updated_at",
        ]].notna().all().all()
    ),
}

for check_name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {check_name}")

if not all(checks.values()):
    raise ValueError("Order business-rule validation failed.")

print("\nAll order date and timestamp checks passed.")