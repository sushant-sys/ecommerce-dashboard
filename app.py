import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# =========================
# CUSTOM CSS (PREMIUM UI)
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #141e30, #243b55);
}

h1 {
    text-align: center;
    color: #00ffe1;
    font-size: 40px;
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    transition: 0.3s;
}
.card:hover {
    transform: scale(1.08);
}

.section {
    margin-top: 20px;
}

section[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.5);
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    conn = sqlite3.connect("backend/db.sqlite3")
    df = pd.read_sql_query("SELECT * FROM orders_order", conn)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

# =========================
# SIDEBAR - UPLOAD CSV
# =========================
st.sidebar.title("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    new_df = pd.read_csv(uploaded_file)
    new_df.columns = new_df.columns.str.strip().str.replace(" ", "_")

    conn = sqlite3.connect("backend/db.sqlite3")
    new_df.to_sql("orders_order", conn, if_exists="append", index=False)

    st.sidebar.success("Data Uploaded Successfully 🚀")

# =========================
# FILTERS
# =========================
st.sidebar.title("🎛 Filters")

city_filter = st.sidebar.multiselect("City", df["city"].unique(), default=df["city"].unique())
category_filter = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())

df = df[(df["city"].isin(city_filter)) & (df["category"].isin(category_filter))]

# =========================
# TITLE
# =========================
st.markdown("<h1>🚀 Advanced E-commerce Dashboard</h1>", unsafe_allow_html=True)

# =========================
# KPI SECTION
# =========================
total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
total_orders = df["order_id"].nunique()

col1, col2, col3 = st.columns(3)

col1.markdown(f'<div class="card"><h3>💰 Sales</h3><h2>{int(total_sales)}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card"><h3>📈 Profit</h3><h2>{int(total_profit)}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card"><h3>🛒 Orders</h3><h2>{total_orders}</h2></div>', unsafe_allow_html=True)

# =========================
# SECTION 1: CITY SALES
# =========================
st.subheader("🏙️ City-wise Sales")

city_df = df.groupby("city")["sales"].sum().reset_index()
fig1 = px.bar(city_df, x="city", y="sales", color="sales")
st.plotly_chart(fig1, use_container_width=True)

# =========================
# SECTION 2: CATEGORY PIE
# =========================
st.subheader("📦 Category Distribution")

cat_df = df.groupby("category")["sales"].sum().reset_index()
fig2 = px.pie(cat_df, names="category", values="sales")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# SECTION 3: MONTHLY TREND
# =========================
st.subheader("📈 Monthly Sales Trend")

df["month"] = df["order_date"].dt.to_period("M").astype(str)
monthly = df.groupby("month")["sales"].sum().reset_index()

fig3 = px.line(monthly, x="month", y="sales", markers=True)
st.plotly_chart(fig3, use_container_width=True)

# =========================
# SECTION 4: TOP PRODUCTS
# =========================
st.subheader("🔥 Top Products")

top_products = df.groupby("product_name")["sales"].sum().reset_index()
top_products = top_products.sort_values(by="sales", ascending=False).head(10)

fig4 = px.bar(top_products, x="product_name", y="sales", color="sales")
st.plotly_chart(fig4, use_container_width=True)

# =========================
# SECTION 5: LOSS ANALYSIS
# =========================
st.subheader("⚠️ Loss Making Products")

loss_df = df.groupby("product_name")["profit"].sum().reset_index()
loss_df = loss_df.sort_values(by="profit").head(10)

fig5 = px.bar(loss_df, x="product_name", y="profit", color="profit")
st.plotly_chart(fig5, use_container_width=True)

# =========================
# SECTION 6: INSIGHTS
# =========================
st.subheader("💡 Business Insights")

top_city = city_df.sort_values(by="sales", ascending=False).iloc[0]["city"]
top_category = cat_df.sort_values(by="sales", ascending=False).iloc[0]["category"]

st.success(f"Top City: {top_city}")
st.info(f"Best Category: {top_category}")

if df["profit"].sum() > 0:
    st.success("Overall business is profitable 🚀")
else:
    st.error("Business is in loss ❌")

# =========================
# SECTION 7: DATA PREVIEW
# =========================
st.subheader("📊 Raw Data Preview")
st.dataframe(df)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<h4 style='text-align:center; color:white;'>✨ Designed by Sushant ✨</h4>",
    unsafe_allow_html=True
)