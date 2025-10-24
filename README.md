📘 This repository serves as a working MLOps blueprint for data pipelines, model lifecycle automation, and deployment — all runnable locally or in cloud environments.

# 🧠 MLOps Project

End-to-end example of a production-grade MLOps pipeline — from raw data ingestion to model serving and monitoring.

## 🚀 **Overview**

This project demonstrates a full MLOps workflow implemented in Python.  
It includes automated data cleaning, training, model promotion, deployment, and monitoring stages.

| Stage | Folder | Owner Script | Description |
|--------|---------|--------------|--------------|
| 🧩 Raw Data | `data/raw` | — | Manual or ETL uploads raw data |
| 🧹 Data Prep | `data/interim`, `data/processed` | `src/data_prep.py` | Cleans + joins data for training |
| 🧮 Feature Engineering | `data/features` | `src/feature_engineering.py` | Creates derived fields for ML |
| 🤖 Model Training | `models/` | `src/train.py` | Builds and evaluates model |
| 📦 Model Registry | `model_registry/` | `src/register_model.py` | Stores promoted models |
| 🌐 Inference | — | `src/serve_app.py` | Exposes REST API for predictions |
| 📊 Monitoring | `data/monitoring/` | `src/drift_check.py` | Detects drift and triggers retraining |

---

## 🧠 **How the Pipeline Works**

### 1️⃣ **Raw → Interim**
- Input: `data/raw/customers.csv`, `data/raw/transactions.json`  
- Script: `src/data_prep.py`
- Cleans missing values, merges tables, and saves:
data/interim/cleaned_customers.csv
data/interim/filtered_sales.csv

markdown
Copy code

### 2️⃣ **Interim → Processed**
- Splits cleaned dataset into `train.csv` and `validation.csv`
- Output path: `data/processed/`

### 3️⃣ **Feature Engineering**
- Optional advanced step for derived metrics:
data/features/customer_features_v3.csv

markdown
Copy code

### 4️⃣ **Training**
- Trains ML model (`RandomForestClassifier` placeholder)
- Saves artifact to:
models/model_v1.pkl

markdown
Copy code

### 5️⃣ **Model Registry Promotion**
- Promotes best model to:
model_registry/model_production.pkl

markdown
Copy code

### 6️⃣ **Serving**
- FastAPI app (`src/serve_app.py`)
- Exposes `/predict` endpoint for real-time inference

### 7️⃣ **Monitoring**
- Drift metrics saved automatically:
data/monitoring/input_stats_<date>.json
data/monitoring/drift_summary.csv

yaml
Copy code

---

## 🧩 **Tech Stack**

| Layer | Tools |
|--------|--------|
| **Language** | Python 3.10+ |
| **Libraries** | pandas, scikit-learn, joblib, FastAPI, uvicorn |
| **Storage** | Local `/data/` (simulates S3 / Blob) |
| **Versioning** | Git + GitHub |
| **Model Registry** | MLflow |
| **CI/CD Integration** | Azure DevOps or GitHub Actions ready |

---

## ⚙️ **Running the Pipeline**

1️⃣ **Prepare environment**
```bash
pip install -r requirements.txt
2️⃣ Run data preparation

bash
Copy code
python src/data_prep.py
3️⃣ Train the model

bash
Copy code
python src/train.py
4️⃣ Register model

bash
Copy code
python src/register_model.py
5️⃣ Serve the model (API)

bash
Copy code
uvicorn src.serve_app:app --host 0.0.0.0 --port 8080
6️⃣ Monitor drift

bash
Copy code
python src/drift_check.py
✅ Author & Versioning
Author: David Santana Rivera

Created: 2025-10-21

Version: v1.0 – Full baseline MLOps repo structure

License: MIT (customize as needed)
