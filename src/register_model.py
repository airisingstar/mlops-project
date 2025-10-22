"""
register_model.py
------------------
Registers trained models into MLflow or a local model registry.
Promotes the latest successful version to Production.

Author: David Santana Rivera
Last updated: 10/21/2025
"""

import os
import shutil

MODELS_DIR = "models"
REGISTRY_DIR = "model_registry"

def main(stage="Production"):
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    src_model = os.path.join(MODELS_DIR, "model_v1.pkl")
    dst_model = os.path.join(REGISTRY_DIR, f"model_{stage.lower()}.pkl")

    if not os.path.exists(src_model):
        print("⚠️ No trained model found. Run train.py first.")
        return

    shutil.copy2(src_model, dst_model)
    print(f"✅ Model promoted to registry → {dst_model}")

if __name__ == "__main__":
    main()
