"""
serve_app.py
-------------
FastAPI inference service for real-time predictions.

Author: David Santana Rivera
Last updated: 10/21/2025
"""

from fastapi import FastAPI
import joblib
import pandas as pd
import os

app = FastAPI(title="Customer Churn Predictor")

MODEL_PATH = "models/model_v1.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    if model is None:
        return {"error": "Model not loaded"}
    df = pd.DataFrame([payload])
    prediction = model.predict(df.select_dtypes(include=["int64", "float64"]))[0]
    return {"prediction": float(prediction)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
