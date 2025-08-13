import pandas as pd
import mysql.connector
import os

# ===== File Path =====
clean_file = r"C:\Users\sajid\OneDrive\Desktop\job market project\data\emerging_startups_2025_clean.csv"

# ===== MySQL Connection =====
db = mysql.connector.connect(
    host="localhost",       # Change if remote
    user="root",            # Your MySQL username
    password="S121001a", # Your MySQL password
    database="Job_market"
)

cursor = db.cursor()

# ===== Read CSV =====
data = pd.read_csv(clean_file)

# ===== Insert Data =====
for _, row in data.iterrows():
    cursor.execute("""
        INSERT INTO startup_funding 
        (date, startup_name, industry_vertical, sub_vertical, city_location, investors_name, investment_type, amount_usd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["Date dd/mm/yyyy"] if not pd.isna(row["Date dd/mm/yyyy"]) else None,
        row["Startup Name"],
        row["Industry Vertical"],
        row["SubVertical"],
        row["City  Location"],
        row["Investors Name"],
        row["InvestmentnType"],
        row["Amount in USD"]
    ))

db.commit()
print("✅ Data imported successfully into MySQL.")

cursor.close()
db.close()
