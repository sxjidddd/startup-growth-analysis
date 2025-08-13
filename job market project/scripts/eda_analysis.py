# ===== eda_analysis.py =====
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ========== Step 1: MySQL Connection ==========
db_config = {
    "host": "localhost",         # Change if using remote MySQL
    "user": "root",              # Your MySQL username
    "password": "S121001a", # Your MySQL password
    "database": "job_market"  # Your DB name
}

conn = mysql.connector.connect(**db_config)

# ========== Step 2: Load Data from MySQL ==========
query = "SELECT * FROM startup_funding"
df = pd.read_sql(query, conn)
conn.close()

print("✅ Data loaded from MySQL")
print(df.head())

# ========== Step 3: Create Output Folder ==========
output_dir = r"C:\Users\sajid\OneDrive\Desktop\job market project\output"
os.makedirs(output_dir, exist_ok=True)

# ========== Step 4: Basic EDA ==========
print("\n📊 Dataset Info:")
print(df.info())

print("\n🔍 Missing Values:")
print(df.isnull().sum())

print("\n📈 Dataset Shape:", df.shape)

# ========== Step 5: Top 10 Funded Startups ==========
top_startups = df.groupby("startup_name")["amount_usd"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_startups.values, y=top_startups.index, palette="viridis")
plt.title("Top 10 Funded Startups")
plt.xlabel("Total Funding (USD)")
plt.ylabel("Startup Name")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_10_funded_startups.png"))
plt.close()

# ========== Step 6: Top 10 Cities by Funding ==========
top_cities = df.groupby("city_location")["amount_usd"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_cities.values, y=top_cities.index, palette="magma")
plt.title("Top 10 Cities by Total Funding")
plt.xlabel("Total Funding (USD)")
plt.ylabel("City")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_10_cities.png"))
plt.close()

# ========== Step 7: Funding Trend by Year ==========
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year
yearly_funding = df.groupby("year")["amount_usd"].sum()
plt.figure(figsize=(10, 6))
sns.lineplot(x=yearly_funding.index, y=yearly_funding.values, marker="o")
plt.title("Funding Trend by Year")
plt.xlabel("Year")
plt.ylabel("Total Funding (USD)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "funding_trend_by_year.png"))
plt.close()

# ========== Step 8: Top Investors ==========
top_investors = df.groupby("investors_name")["amount_usd"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_investors.values, y=top_investors.index, palette="coolwarm")
plt.title("Top 10 Investors by Total Funding")
plt.xlabel("Total Funding (USD)")
plt.ylabel("Investor Name")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_investors.png"))
plt.close()

# ========== Step 9: Industry-Wise Funding ==========
top_industries = df.groupby("industry_vertical")["amount_usd"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_industries.values, y=top_industries.index, palette="cubehelix")
plt.title("Top 10 Industries by Total Funding")
plt.xlabel("Total Funding (USD)")
plt.ylabel("Industry")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_industries.png"))
plt.close()

print(f"\n✅ EDA complete. Charts saved in '{output_dir}'")
