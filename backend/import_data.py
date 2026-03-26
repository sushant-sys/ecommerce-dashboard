import os
import django
import pandas as pd

# Django setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from orders.models import Order

# Load CSV
df = pd.read_csv("../data/orders.csv", encoding="latin1")

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Convert date format
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors='coerce')

# Drop invalid dates
df = df.dropna(subset=["Order_Date"])

# Insert data
for _, row in df.iterrows():
    Order.objects.create(
        order_id=row["Order_ID"],
        product_name=row["Product_Name"],
        category=row["Category"],
        sales=row["Sales"],
        profit=row["Profit"],
        city=row["City"],
        order_date=row["Order_Date"].date()
    )

print("Data imported successfully 🔥")