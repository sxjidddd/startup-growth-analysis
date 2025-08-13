import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# File paths
input_file = r"C:\Users\sajid\OneDrive\Desktop\job market project\data\emerging_startups_2025_clean.csv"
output_dir = r"C:\Users\sajid\OneDrive\Desktop\job market project\output"

# Load dataset
df = pd.read_csv(input_file)

# Rename columns to snake_case for easy access
df.rename(columns={
    "Sr No": "sr_no",
    "Date dd/mm/yyyy": "date",
    "Startup Name": "startup_name",
    "Industry Vertical": "industry_vertical",
    "SubVertical": "sub_vertical",
    "City  Location": "city_location",
    "Investors Name": "investors_name",
    "InvestmentnType": "investment_type",
    "Amount in USD": "amount_usd"
}, inplace=True)

# Convert amount_usd to numeric
df["amount_usd"] = (
    df["amount_usd"].replace({",": "", r"\$": ""}, regex=True).astype(float)
)

# 1️⃣ Total funding by city
city_funding = df.groupby("city_location")["amount_usd"].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
sns.barplot(x=city_funding.values, y=city_funding.index, palette="viridis")
plt.title("Total Funding by City")
plt.xlabel("Total Funding (USD)")
plt.ylabel("City")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "total_funding_by_city.png"))
plt.close()

# 2️⃣ Top 10 investors by total investment
investor_funding = df.groupby("investors_name")["amount_usd"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=investor_funding.values, y=investor_funding.index, palette="coolwarm")
plt.title("Top 10 Investors by Total Investment")
plt.xlabel("Total Investment (USD)")
plt.ylabel("Investor")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "top_investors.png"))
plt.close()

# 3️⃣ Funding distribution by industry
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="industry_vertical", y="amount_usd")
plt.xticks(rotation=90)
plt.title("Funding Distribution by Industry")
plt.ylabel("Funding Amount (USD)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "funding_distribution_by_industry.png"))
plt.close()

# 4️⃣ Summary statistics
summary = df.describe(include="all")
summary.to_csv(os.path.join(output_dir, "summary_statistics.csv"))

print("✅ Advanced EDA completed. Charts and summary saved.")
