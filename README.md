📘 This repository serves as a working MLOps blueprint for data pipelines, model lifecycle automation, and deployment — all runnable locally or in cloud environments.

# 🧠 MLOps Project

End-to-end example of a **production-grade MLOps pipeline** — from raw data ingestion to model serving and continuous monitoring.

---

## 🎯 Model Goal

The objective of this project is to **predict which customer groups are most likely to make a large future purchase** based on their demographics, transaction behavior, and loyalty attributes.

This model uses two primary data sources:

| Source File | Description |
|--------------|-------------|
| `customers.csv` | Contains static information about each customer such as age, region, signup date, and loyalty points. |
| `transactions.json` | Contains dynamic purchase data including transaction amount, timestamp, and payment method. |

---

### 🧠 What the Model Learns
After merging customers with their transactions using `customer_id`, the model:
1. **Aggregates purchase behavior** — average spend, total completed transactions, most recent purchase amount.  
2. **Combines demographic and loyalty features** — age, region, signup date, and loyalty points.  
3. **Predicts** whether a customer is a **high-value buyer**, defined as someone likely to make a purchase above a given threshold (e.g., `$300`).  

---

### ⚙️ Model Workflow
1. Detect new data in `data/raw/` (e.g., S3 upload or local ingestion).  
2. Clean and join datasets → produce `data/processed/train.csv`.  
3. Train a **RandomForestClassifier** to predict high-value buyers.  
4. Register and deploy the model via FastAPI for real-time inference.  
   - **Input Example:** `{ "age": 35, "region": "East", "loyalty_points": 1200 }`  
   - **Output Example:** `{ "large_purchase_probability": 0.87 }`  
5. Monitor model drift and retrain automatically as customer patterns evolve.

---

The end-to-end goal is to create a **self-updating, data-driven system** that helps identify which customers are most likely to make large purchases — enabling smarter marketing, retention, and sales strategies.

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
```

### 🧭 Automation
Local / Sandbox Mode: Sequential execution via make run-all or bash pipeline.sh.

Cloud Mode: Orchestration handled by AWS Step Functions, Airflow, or Prefect.

Event Communication: S3/Lambda → SNS → Step Functions → ECS/Fargate → Model Registry → FastAPI Deployment.

Self-Healing Cycle: The monitoring agent detects drift and retriggers training automatically.

### 🧩 Tech Stack

| Layer | Tools |
|--------|--------|
| **Language** | Python 3.10+ |
| **Libraries** | pandas, scikit-learn, joblib, FastAPI, uvicorn |
| **Storage** | Local `/data/` (simulates S3 / Blob) |
| **Version Control** | Git + GitHub |
| **Model Registry** | MLflow |
| **CI/CD Integration** | Azure DevOps or GitHub Actions ready |


### ⚙️ Running the Pipeline

### ⚙️ Running the Pipeline

1️⃣ **Prepare environment**
```bash
pip install -r requirements.txt
```

2️⃣ Run data preparation
```bash
python src/data_prep.py
```

3️⃣ Train the model
```bash
python src/train.py
```

4️⃣ Register model
```bash
python src/register_model.py
```

5️⃣ Serve the model (API)
```bash
uvicorn src.serve_app:app --host 0.0.0.0 --port 8080
```

6️⃣ Monitor drift
```bash
python src/drift_check.py
```

### ✅ Author & Versioning
Author: David Santana Rivera

Updated: 10-10-2025
