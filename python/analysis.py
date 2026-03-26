import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("../data/orders.csv", encoding='latin1')

# =========================
# 2. CLEAN COLUMNS
# =========================
df.columns = df.columns.str.strip().str.replace(" ", "_")

print("Columns:\n", df.columns)

# =========================
# 3. BASIC INFO
# =========================
print("\nFirst 5 Rows:\n", df.head())

# =========================
# 4. TOTAL SALES & PROFIT
# =========================
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()

print("\nTotal Sales:", total_sales)
print("Total Profit:", total_profit)

# =========================
# 5. TOP CITIES
# =========================
city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False)

print("\nTop 10 Cities by Sales:\n", city_sales.head(10))

# =========================
# 6. TOP PRODUCTS
# =========================
product_sales = df.groupby("Product_Name")["Sales"].sum().sort_values(ascending=False)

print("\nTop 10 Products:\n", product_sales.head(10))

# =========================
# 7. LOSS MAKING PRODUCTS
# =========================
loss_products = df.groupby("Product_Name")["Profit"].sum().sort_values().head(5)

print("\nTop Loss Making Products:\n", loss_products)

# =========================
# 8. VISUALIZATION
# =========================

# Top Cities Graph
city_sales.head(10).plot(kind='bar')
plt.title("Top 10 Cities by Sales")
plt.xlabel("City")
plt.ylabel("Sales")
plt.show()

# Top Products Graph
product_sales.head(10).plot(kind='bar')
plt.title("Top 10 Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.show()