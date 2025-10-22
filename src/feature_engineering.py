"""
feature_engineering.py
----------------------
Computes engineered features (aggregations, ratios, scores)
and saves them to /data/features for reuse.

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import os
import pandas as pd

PROCESSED_DIR = "data/processed"
FEATURES_DIR = "data/features"

def main():
    os.makedirs(FEATURES_DIR, exist_ok=True)
    train_path = os.path.join(PROCESSED_DIR, "train.csv")

    if not os.path.exists(train_path):
        print("⚠️ Processed train.csv not found. Run data_prep.py first.")
        return

    df = pd.read_csv(train_path)
    print("🧮 Generating features...")
    df["age_bucket"] = pd.cut(df["age"], bins=[0, 25, 35, 45, 60], labels=["GenZ", "Millennial", "GenX", "Boomer"])
    df["loyalty_normalized"] = df["loyalty_points"] / df["loyalty_points"].max()

    feature_path = os.path.join(FEATURES_DIR, "customer_features_v3.csv")
    df.to_csv(feature_path, index=False)
    print(f"✅ Features saved → {feature_path}")

if __name__ == "__main__":
    main()
