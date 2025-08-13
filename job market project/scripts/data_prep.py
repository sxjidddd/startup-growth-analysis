import pandas as pd
import os

# ===== File Paths =====
raw_file = r"C:\Users\sajid\OneDrive\Desktop\job market project\data\startup_funding(in).csv"
clean_file = r"C:\Users\sajid\OneDrive\Desktop\job market project\data\emerging_startups_2025_clean.csv"

# ===== Step 1: Check if file exists =====
if not os.path.exists(raw_file):
    raise FileNotFoundError(f"❌ File not found: {raw_file}")

# ===== Step 2: Load CSV (handle Excel encoding) =====
try:
    data = pd.read_csv(raw_file, encoding="windows-1252")
    print("✅ Data loaded successfully with 'windows-1252' encoding.")
except UnicodeDecodeError:
    data = pd.read_csv(raw_file, encoding="latin1")
    print("✅ Data loaded successfully with 'latin1' encoding.")

# ===== Step 3: Overview before cleaning =====
print(f"\n📊 Shape before cleaning: {data.shape}")
print("\nColumn names before cleaning:", data.columns.tolist())

# ===== Step 4: Strip spaces from column names only (no renaming) =====
data.columns = data.columns.str.strip()

# ===== Step 5: Drop rows where key fields are missing =====
data = data.dropna(subset=["Startup Name", "Amount in USD"])

# ===== Step 6: Fill other missing values with 'Unknown' =====
data = data.fillna("Unknown")

# ===== Step 7: Clean 'Amount in USD' column =====
def clean_amount(value):
    if isinstance(value, str):
        value = value.replace(",", "").replace("$", "").strip()
    try:
        return float(value)
    except ValueError:
        return None

data["Amount in USD"] = data["Amount in USD"].apply(clean_amount)

# Drop rows where amount is invalid
data = data.dropna(subset=["Amount in USD"])

# ===== Step 8: Standardize text columns =====
text_columns = [
    "Startup Name",
    "Industry Vertical",
    "SubVertical",
    "City  Location",  # note: double space from Excel
    "Investors Name",
    "InvestmentnType"
]

for col in text_columns:
    if col in data.columns:
        data[col] = data[col].astype(str).str.strip().str.title()

# ===== Step 9: Convert date column to datetime =====
if "Date dd/mm/yyyy" in data.columns:
    data["Date dd/mm/yyyy"] = pd.to_datetime(data["Date dd/mm/yyyy"], errors="coerce", dayfirst=True)

# ===== Step 10: Final overview =====
print(f"📊 Shape after cleaning: {data.shape}")
print("\nSample cleaned data:\n", data.head())

# ===== Step 11: Save cleaned data =====
os.makedirs(os.path.dirname(clean_file), exist_ok=True)
data.to_csv(clean_file, index=False, encoding="utf-8-sig")

print(f"\n💾 Cleaned data saved to: {clean_file}")
print("✅ Data preparation complete!")
