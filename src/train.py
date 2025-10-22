"""
train.py
---------
Trains and evaluates ML model using processed data.
Logs metrics and artifacts to MLflow or local directory.

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

PROCESSED_DIR = "data/processed"
MODELS_DIR = "models"

def main():
    os.makedirs(MODELS_DIR, exist_ok=True)
    print("📥 Loading training data...")
    train_df = pd.read_csv(os.path.join(PROCESSED_DIR, "train.csv"))

    # Example placeholder: assume a target column called 'loyalty_points'
    X = train_df.drop(columns=["loyalty_points"], errors="ignore")
    y = train_df["loyalty_points"] if "loyalty_points" in train_df.columns else None

    if y is None:
        print("⚠️ No target column found. Skipping model training.")
        return

    print("🚀 Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X.select_dtypes(include=["int64", "float64"]), y)

    preds = model.predict(X.select_dtypes(include=["int64", "float64"]))
    acc = accuracy_score(y, preds)
    print(f"✅ Training complete. Accuracy: {acc:.3f}")

    joblib.dump(model, os.path.join(MODELS_DIR, "model_v1.pkl"))
    print("💾 Model saved to models/model_v1.pkl")

if __name__ == "__main__":
    main()
