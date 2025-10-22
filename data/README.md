📘 *This README defines every data stage in the MLOps lifecycle — enabling full traceability from raw ingestion to model monitoring.*

# 📂 data/

Central repository for all datasets used throughout the ML pipeline.  
Each subfolder represents a different stage of data maturity — from raw uploads to monitored model outputs.

```
data/
├─ raw/               # untouched incoming data
├─ interim/           # cleaned or partially processed
├─ processed/         # ready for model training
├─ features/          # extracted feature tables
├─ validation/        # schema or test data samples
├─ predictions/       # model outputs for QA or audit
└─ monitoring/        # drift metrics, logs, performance snapshots
```
---

______________________________________________________________________

SUBFOLDERS

## 1️⃣ **raw/** – Incoming Data

Direct dumps from upstream systems or user uploads.  
May include duplicates, missing values, or mixed formats.
Starting point for data processing and ML pipeline.

### 🔸 Triggered by
ETL, cron job, or API feed
### 🔸 Triggers
`src/data_prep.py`

### 🔸 Module
*(none)*
### 🔸 Command
```bash
aws s3 cp ./new_customer_data.csv s3://mybucket/data/raw/   # AWS example
```

### 🔸 Example files uploaded
```
data/raw/customers.csv
data/raw/transactions.json
```

---

## 2️⃣ **interim/** – Cleaned, Still Volatile

After initial cleaning but before feature engineering.  
Used for quick inspections or debugging preprocessing steps.
Works in memory Pandas Dataframe.
Creates only requested/specified data by pandas module to create new .parquet files

### 🔸 Triggered by
`src/data_prep.py`
### 🔸 Triggers
`src/train.py`

### 🔸 Module
```python
df = pd.read_csv("data/raw/customers.csv")  # read raw
df = df.dropna(subset=["email", "age"]) # clean in memory
df.to_parquet("data/interim/cleaned_customers.parquet") # write clean version
```
### 🔸 Command
*(none — runs automatically in pipeline)*

### 🔸 Example files created
```
data/interim/cleaned_customers.parquet
data/interim/filtered_sales.csv
```

---

## 3️⃣ **processed/** – Final Training Data

Fully transformed datasets, ready for training. Contains the datasets directly used for model training and evaluation.
Used by training and experimentation pipelines.

### 🔸 Triggered by
`data/interim/cleaned_customers.parquet`
### 🔸 Triggers
`src/train.py` (model training)

### 🔸 Module
```python
train_df = pd.read_parquet("data/interim/cleaned_customers.parquet") # Read interim
```

### 🔸 Example files created
```
data/processed/train.parquet
data/processed/validation.parquet
```

---

## 4️⃣ **features/** – Engineered Feature Tables

Optional, used when applying a Feature Store pattern.  
Contains reusable engineered features across models.
Central repository of computed features for training/inference parity.

### 🔸 Triggered by
`src/train.py` or `src/feature_engineering.py` (if implemented)
### 🔸 Triggers
Model training and inference that consume shared features MLflow, another pandas script or SageMaker Feature Store

### 🔸 Module
```python
df = create_feature_table(train_df)
df.to_parquet("data/features/customer_features_v3.parquet")
```

### 🔸 Example files created
```
data/features/customer_features_v3.parquet
```

---

## 5️⃣ **validation/** – Holdout or QA Data

Used to verify pipeline outputs or validate retraining consistency.  
Includes golden datasets for regression and schema testing.
Ensures data quality, schema consistency, and reproducibility.

### 🔸 Triggered by
CI/CD validation or schema check (e.g., `great_expectations`, `pytest`)
### 🔸 Triggers
Retraining approval or QA validation jobs, schema checks, or unit tests

### 🔸 Example files created
```
data/validation/golden_test_set.csv
data/validation/schema_test_sample.json
```

---

## 6️⃣ **predictions/** – Model Outputs (QA or Audit)

Stores generated predictions from deployed models for manual review, audit, or monitoring.
Provides traceability for inference results; supports model audits and post-deployment checks.

### 🔸 Triggered by
`src/serve_app.py` or batch inference scripts
### 🔸 Triggers
QA or audit pipelines, QA dashboards, monitoring jobs, or compliance tools

### 🔸 Example files created
```
data/predictions/model_v5_outputs.csv
```

---

## 7️⃣ **monitoring/** – Drift Metrics, Logs, Performance Snapshots

Contains logs and metrics for data drift, performance, and system health.
Tracks drift and performance trends over time; ensures deployed models stay reliable and compliant.

### 🔸 Triggered by
`src/drift_check.py` or CI/CD scheduled monitor
### 🔸 Triggers
Retraining pipeline or alert notifications. pandas (metrics parsing), dashboards, alert systems

### 🔸 Module
```python
if drift_score > 0.05:
    trigger_retrain_pipeline()
```

### 🔸 Example files created
```
data/monitoring/input_stats_2025_10_21.json
data/monitoring/drift_summary.csv
```

---

### ✅ **Summary**

| Stage | Input From | Created By | Ingested By | Triggers |
|--------|-------------|-------------|--------------|-----------|
| `raw/` | Upstream | External source | `data_prep.py` | Data cleaning |
| `interim/` | `data_prep.py` | `data_prep.py` | pandas memory | Training step |
| `processed/` | `data_prep.py` | CI/CD | `train.py` | Training & registry |
| `features/` | Training data | Feature job | Model pipeline | Inference |
| `validation/` | CI/CD | Validator | QA tools | Retraining |
| `predictions/` | Inference jobs | Model API | QA dashboards | Monitoring |
| `monitoring/` | Drift monitor | `drift_check.py` | Dashboards | Retraining trigger |

---

Stage	Format Used	Why
data/raw/	.csv, .json, .xlsx	Human-readable / manual upload
data/interim/	.parquet	Faster intermediate read/write
data/processed/	.parquet	Consistent model input format
data/monitoring/	.csv, .json	Easy for metrics dashboard

__________________________________________________________________________________________

---

## 📘 Example: Converting CSV → Parquet with `data_prep.py` (pandas)

```python
import pandas as pd

# Load raw CSV
df = pd.read_csv("data/raw/customers.csv")

# Clean and filter
df = df.dropna(subset=["email", "age"])

# Save as Parquet
df.to_parquet("data/interim/cleaned_customers.parquet", index=False)

🧠 About .parquet Files

A .parquet file is a binary, columnar data format designed for big data and ML pipelines.

It’s used instead of .csv because it’s:

⚡ Much faster to read/write

🗜️ Compressed (saves cloud storage)

📊 Column-oriented (great for analytics and training data)

🧩 Schema-aware (preserves data types)

Parquet stores each column separately (columnar layout).
This allows efficient reads for selected columns only:

pd.read_parquet("cleaned_customers.parquet", columns=["age", "region"])


It’s the standard format used by tools like Spark, Arrow, Athena, BigQuery, SageMaker, and Azure ML.

Author: David Santana Rivera
Last updated: 10/10/2025