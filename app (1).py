
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="🍬",
    layout="wide"
)

st.title("🍬 Nassau Candy Sales Dashboard")
st.markdown("---")

# Load Dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert Dates
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# Create Year Column
df["Year"] = df["Order Date"].dt.year

# ---------------- Sidebar ---------------- #

st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Select Year",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

division = st.sidebar.multiselect(
    "Select Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["Region"].isin(region)) &
    (df["Division"].isin(division))
]

# ---------------- KPI Cards ---------------- #

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${total_sales:,.2f}")
c2.metric("💵 Total Profit", f"${total_profit:,.2f}")
c3.metric("📦 Orders", total_orders)
c4.metric("👥 Customers", total_customers)

st.markdown("---")

#---------monthly sales trend----#

st.subheader("📈 Monthly Sales Trend")

filtered_df["Month"] = filtered_df["Order Date"].dt.month_name()

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reindex(month_order)
)

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(monthly_sales.index, monthly_sales.values, marker="o")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
plt.xticks(rotation=45)

st.pyplot(fig)

#----------Sales by Division----------#

st.subheader("🍫 Sales by Division")

division_sales = filtered_df.groupby("Division")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8,4))
division_sales.plot(kind="bar", ax=ax)
ax.set_ylabel("Sales")

st.pyplot(fig)

#--------- Sales by Region------------#

st.subheader("🌍 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum()

fig, ax = plt.subplots(figsize=(8,4))
region_sales.plot(kind="bar", ax=ax)
ax.set_ylabel("Sales")

st.pyplot(fig)

# ===============================
# Top 10 Products by Sales
# ===============================

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))
top_products.plot(kind="bar", ax=ax)

ax.set_xlabel("Product")
ax.set_ylabel("Sales")
plt.xticks(rotation=45, ha="right")

st.pyplot(fig)

# ===============================
# Top 10 Cities by Sales
# ===============================

st.subheader("🏙 Top 10 Cities by Sales")

top_cities = (
    filtered_df.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))
top_cities.plot(kind="bar", ax=ax)

ax.set_xlabel("City")
ax.set_ylabel("Sales")
plt.xticks(rotation=45)

st.pyplot(fig)

# ===============================
# Ship Mode Analysis
# ===============================

st.subheader("🚚 Orders by Ship Mode")

ship_mode = filtered_df["Ship Mode"].value_counts()

fig, ax = plt.subplots(figsize=(7,4))
ship_mode.plot(kind="bar", ax=ax)

ax.set_xlabel("Ship Mode")
ax.set_ylabel("Number of Orders")

st.pyplot(fig)

# ===============================
# Sales vs Cost
# ===============================

st.subheader("💰 Sales vs Cost")

fig, ax = plt.subplots(figsize=(8,5))

ax.scatter(
    filtered_df["Cost"],
    filtered_df["Sales"],
    alpha=0.6
)

ax.set_xlabel("Cost")
ax.set_ylabel("Sales")

st.pyplot(fig)

# ===============================
# Correlation Heatmap
# ===============================

st.subheader("🔥 Correlation Heatmap")

corr = filtered_df[["Sales","Cost","Gross Profit","Units"]].corr()

fig, ax = plt.subplots(figsize=(6,4))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)

# ===============================
# Distribution of Sales
# ===============================

st.subheader("📊 Distribution of Sales")

fig, ax = plt.subplots(figsize=(8,4))

ax.hist(
    filtered_df["Sales"],
    bins=30
)

ax.set_xlabel("Sales")
ax.set_ylabel("Frequency")

st.pyplot(fig)
