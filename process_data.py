import pandas as pd
from pathlib import Path

# =============================
# 1. Paths
# =============================
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "processed_sales.csv"

# =============================
# 2. Load CSV files
# =============================
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("❌ No CSV files found in data/ directory")

print(f"📂 Found {len(csv_files)} CSV files")

dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    print(f"\n📄 Loaded: {file.name}")
    print("Columns:", df.columns.tolist())
    dfs.append(df)

# =============================
# 3. Combine all data
# =============================
combined_df = pd.concat(dfs, ignore_index=True)
combined_df.columns = combined_df.columns.str.lower()

print("\n🔗 Combined shape:", combined_df.shape)

# =============================
# 4. Validate required columns
# =============================
required_cols = {"product", "quantity", "price", "date", "region"}
missing = required_cols - set(combined_df.columns)

if missing:
    raise ValueError(f"❌ Missing required columns: {missing}")

# =============================
# 5. Clean product names
# =============================
combined_df["product"] = (
    combined_df["product"]
    .astype(str)
    .str.strip()
    .str.lower()
)

print("\n🧾 Unique products:")
print(combined_df["product"].unique())

# =============================
# 6. Filter Pink Morsel
# =============================
pink_df = combined_df[combined_df["product"] == "pink morsel"].copy()

print("\n🎯 Pink Morsel rows:", len(pink_df))

if pink_df.empty:
    raise ValueError("❌ No Pink Morsel data found")

# =============================
# 7. FIX DATA TYPES (CRITICAL)
# =============================

# Clean price: "$3.00" -> 3.00
pink_df["price"] = (
    pink_df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .astype(float)
)

# Quantity to numeric
pink_df["quantity"] = pd.to_numeric(pink_df["quantity"], errors="raise")

# =============================
# 8. Calculate Sales
# =============================
pink_df["sales"] = pink_df["quantity"] * pink_df["price"]

# =============================
# 9. Final Output DataFrame
# =============================
final_df = pink_df[["sales", "date", "region"]].rename(
    columns={
        "sales": "Sales",
        "date": "Date",
        "region": "Region"
    }
)

print("\n✅ Final preview:")
print(final_df.head())
print("\n📊 Final shape:", final_df.shape)

# =============================
# 10. Save CSV
# =============================
final_df.to_csv(OUTPUT_FILE, index=False)

print(f"\n💾 Output saved to {OUTPUT_FILE}")
