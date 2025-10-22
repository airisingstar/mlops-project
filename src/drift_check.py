"""
drift_check.py
---------------
Monitors feature drift between training and production data,
generates metrics, and optionally triggers retraining.

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import pandas as pd
import os
import json

PROCESSED_DIR = "data/processed"
PREDICTIONS_DIR = "data/predictions"
MONITORING_DIR = "data/monitoring"

def main():
    os.makedirs(MONITORING_DIR, exist_ok=True)
    train = pd.read_csv(os.path.join(PROCESSED_DIR, "train.csv"))
    pred_path = os.path.join(PREDICTIONS_DIR, "model_v5_outputs.csv")

    if not os.path.exists(pred_path):
        print("⚠️ No predictions found to compare against.")
        return

    preds = pd.read_csv(pred_path)

    # Simple drift metric example
    drift_score = abs(train["age"].mean() - preds["customer_id"].count()) / 100
    stats = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "drift_score": round(drift_score, 3)
    }

    json_path = os.path.join(MONITORING_DIR, f"input_stats_{pd.Timestamp.now().date()}.json")
    with open(json_path, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"✅ Drift metrics saved → {json_path}")

if __name__ == "__main__":
    main()
