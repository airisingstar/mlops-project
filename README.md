📘 This repository serves as a working MLOps blueprint for data pipelines, model lifecycle automation, and deployment — all runnable locally or in cloud environments.

# 🧠 MLOps Project

End-to-end example of a **production-grade MLOps pipeline** — from raw data ingestion to model serving and continuous monitoring.

---

## 🚀 Overview

This project demonstrates a full MLOps workflow implemented in **Python**.  
It includes automated **data cleaning**, **training**, **model promotion**, **deployment**, and **monitoring** stages.

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

## 🧠 How the Pipeline Works

This pipeline follows an **event-driven orchestration model**, where each stage is triggered automatically when the previous one completes successfully or when new data arrives.  
The goal is a **self-updating lifecycle** that moves from data ingestion to live monitoring with minimal manual effort.

---

### ⚡ Event Flow Overview

1️⃣ **Data Ingestion (Trigger Source)**  
- New raw data lands in **S3** (or `data/raw/` locally).  
- An **S3 event notification** or filesystem watcher detects the upload.  
- This event **triggers the Data Preparation job** to start cleaning and validation.

2️⃣ **Data Preparation → Processed Output**  
- `src/data_prep.py` cleans, merges, and validates schema.  
- Once complete, it emits a `_SUCCESS` marker or orchestration event (e.g., Step Functions, Airflow, or Prefect).  
- That event **triggers the Feature Engineering job**.

3️⃣ **Feature Engineering Trigger**  
- `src/feature_engineering.py` generates new derived metrics and aggregates.  
- When output is written (`data/features/*.parquet`), the orchestrator **launches the Model Training stage**.

4️⃣ **Model Training & Validation**  
- `src/train.py` trains and evaluates ML models.  
- Performance metrics are logged and compared with prior runs.  
- Upon success, the job emits a **promotion-ready event**.

5️⃣ **Model Registry & Promotion**  
- `src/register_model.py` promotes the new model to production if metrics improve.  
- Promotion automatically **triggers deployment**.

6️⃣ **Model Deployment & Serving**  
- `src/deploy_model.py` rebuilds and redeploys the FastAPI microservice.  
- The `/predict` endpoint begins serving the new model version immediately.

7️⃣ **Monitoring & Auto-Retrain Loop**  
- `src/monitor_drift.py` runs on a schedule (cron, Airflow DAG, or Lambda).  
- It monitors **data drift** and **concept drift**.  
- If drift > threshold, it **re-triggers the data prep and training pipeline**, closing the automation loop.

---

## 🔄 Event-Driven Pipeline Graph

```text
          ┌───────────────────────────┐
          │     🗂️  S3 / Raw Data     │
          │   (new upload detected)   │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ ⚙️  Data Preparation Job  │
          │ Cleans, merges, validates │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🧮 Feature Engineering     │
          │ Derived metrics, encoding │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🤖 Model Training          │
          │ Train, evaluate, validate │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🏷️  Model Registry         │
          │ Versioning & promotion    │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🚀 Deployment (FastAPI)   │
          │ Exposes /predict endpoint │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 📈 Monitoring & Drift      │
          │ Auto-retrain trigger loop │
          └───────────────────────────┘

```text

---

### 🧭 Automation

Local / Sandbox Mode: Sequential execution via make run-all or bash pipeline.sh.

Cloud Mode: Orchestration handled by AWS Step Functions, Airflow, or Prefect.

Event Communication: S3/Lambda → SNS → Step Functions → ECS/Fargate → Model Registry → FastAPI Deployment.

Self-Healing Cycle: The monitoring agent detects drift and retriggers training automatically.

🧩 Tech Stack
Layer	Tools
Language	Python 3.10+
Libraries	pandas, scikit-learn, joblib, FastAPI, uvicorn
Storage	Local /data/ (simulates S3 / Blob)
Version Control	Git + GitHub
Model Registry	MLflow
CI/CD Integration	Azure DevOps or GitHub Actions ready
⚙️ Running the Pipeline

1️⃣ Prepare environment

pip install -r requirements.txt


2️⃣ Run data preparation

python src/data_prep.py


3️⃣ Train the model

python src/train.py


4️⃣ Register model

python src/register_model.py


5️⃣ Serve the model (API)

uvicorn src.serve_app:app --host 0.0.0.0 --port 8080


6️⃣ Monitor drift

python src/drift_check.py

✅ Author & Versioning

Author: David Santana Rivera
Created: 2025-10-21
