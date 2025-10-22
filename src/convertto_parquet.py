"""
convertto_parquet.py
--------------------
Converts all sandbox CSV example files into Parquet format for faster processing.

Usage:
    python src/convertto_parquet.py

Requirements:
    pip install pyarrow

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import os
import pandas as pd

# --- Directories ---
DATA_DIRS = [
    "data/interim",
    "data/processed",
    "data/features",
]

# --- Helper function ---
def convert_csv_to_parquet(csv_path):
    """Convert a CSV file to Parquet with the same name."""
    parquet_path = csv_path.replace(".csv", ".parquet")
    try:
        df = pd.read_csv(csv_path)
        df.to_parquet(parquet_path, index=False)
        print(f"✅ Converted: {csv_path} → {parquet_path}")
    except Exception as e:
        print(f"⚠️ Skipped {csv_path}: {e}")

# --- Conversion loop ---
for folder in DATA_DIRS:
    if not os.path.exists(folder):
        print(f"⚠️ Folder not found: {folder}")
        continue

    for file in os.listdir(folder):
        if file.endswith("_example.csv"):
            csv_path = os.path.join(folder, file)
            convert_csv_to_parquet(csv_path)

print("\n🎯 Conversion complete! All *_example.csv files converted to Parquet where possible.")
