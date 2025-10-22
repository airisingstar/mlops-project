"""
data_prep.py
-------------
Reads raw customer and transaction data, performs basic cleaning and joins,
and writes cleaned/intermediate/processed datasets for ML training.

Input:
  - data/raw/customers.csv
  - data/raw/transactions.json

Output:
  - data/interim/cleaned_customers.csv
  - data/interim/filtered_sales.csv
  - data/processed/train.csv
  - data/processed/validation.csv

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from common import load_environment, get_env_var, get_data_path

# ---------- Load Environment ----------
load_environment()

RAW_DIR = get_data_path("raw")
INTERIM_DIR = get_data_path("interim")
PROCESSED_DIR = get_data_path("processed")

os.makedirs(INTERIM_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# ---------- 1️⃣ Load Raw Data ----------
print("📥 Loading raw data...")

# Pull paths from environment file
customers_path = get_env_var("DATA_PATH", os.path.join(RAW_DIR, "customers.csv"))
transactions_path = get_env_var("TRANSACTIONS_PATH", os.path.join(RAW_DIR, "transactions.json"))

customers = pd.read_csv(customers_path)
transactions = pd.read_json(transactions_path)

# ---------- 2️⃣ Clean Customer Data ----------
print("🧹 Cleaning customer data...")
customers["email"] = customers["email"].replace("", pd.NA)
customers["age"] = pd.to_numeric(customers["age"], errors="coerce")

# Drop rows missing both email and age
cleaned_customers = customers.dropna(subset=["email", "age"]).copy()

# ---------- 3️⃣ Join Transactions ----------
print("🔗 Joining with transaction data...")
merged = transactions.merge(cleaned_customers, on="customer_id", how="left")

# ---------- 4️⃣ Derived Fields ----------
merged["amount_usd"] = merged["amount"]
merged["transaction_year"] = pd.to_datetime(merged["timestamp"]).dt.year

# ---------- 5️⃣ Write Interim Files ----------
print("💾 Writing interim files...")
cleaned_customers.to_csv(os.path.join(INTERIM_DIR, "cleaned_customers.csv"), index=False)

merged[
    ["transaction_id", "customer_id", "amount_usd", "transaction_year", "region"]
].to_csv(os.path.join(INTERIM_DIR, "filtered_sales.csv"), index=False)

# ---------- 6️⃣ Train/Validation Split ----------
print("📊 Creating train/validation splits...")
train_df, val_df = train_test_split(cleaned_customers, test_size=0.25, random_state=42)

train_df.to_csv(os.path.join(PROCESSED_DIR, "train.csv"), index=False)
val_df.to_csv(os.path.join(PROCESSED_DIR, "validation.csv"), index=False)

print("✅ Data prep completed successfully!")
print(f" - {len(cleaned_customers)} cleaned customer records")
print(f" - {len(merged)} transactions joined")
print(f" - Train set: {len(train_df)}, Validation set: {len(val_df)}")
