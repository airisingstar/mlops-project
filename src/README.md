📘 This README defines every core MLOps pipeline module, ensuring traceability from data ingestion to production monitoring.

# 📂 src/

All core pipeline logic for the MLOps project lives here.  
Each module represents a distinct stage in the ML lifecycle — from ingestion to serving.

src/
├─ data_prep.py # read, clean, and join raw data → interim + processed
├─ train.py # train model + log to MLflow or SageMaker
├─ register_model.py # promote best model version to registry
├─ feature_engineering.py# optional: generate derived features
├─ serve_app.py # FastAPI app for inference (containerized)
├─ drift_check.py # nightly drift monitoring and alerting
└─ common.py # shared utilities, schema validation, paths

yaml
Copy code

---

## 1️⃣ **data_prep.py** – Data Cleaning & Preparation

Reads `/data/raw` inputs, cleans missing values, merges transactions, and writes results into `/data/interim` and `/data/processed`.

### 🔸 Input:
data/raw/customers.csv
data/raw/transactions.json

shell
Copy code

### 🔸 Output:
data/interim/cleaned_customers.csv
data/interim/filtered_sales.csv
data/processed/train.csv
data/processed/validation.csv

bash
Copy code

### 🔸 Example Command:
```bash
python src/data_prep.py
2️⃣ train.py – Model Training & Logging
Trains machine-learning models using cleaned data and logs results to MLflow, SageMaker, or Vertex AI.

🔸 Input:
bash
Copy code
data/processed/train.csv
data/processed/validation.csv
🔸 Output:
csharp
Copy code
models/
 └─ model_v1.pkl
mlruns/
 └─ metrics, params, artifacts
🔸 Responsibilities:
Load processed data

Split features/labels

Train + evaluate model

Log metrics and artifacts (MLflow or SageMaker)

3️⃣ register_model.py – Model Registry Promotion
Selects the best model from experiments and registers it to the official registry (MLflow / SageMaker / Vertex).
Handles versioning and approval logic.

🔸 Input:
Best model artifact (.pkl, .onnx, etc.)

Evaluation metrics (from training run)

🔸 Output:
Model entry in registry (Production, Staging, Archived)

🔸 Example Command:
bash
Copy code
python src/register_model.py --stage Production
4️⃣ feature_engineering.py – Feature Generation
Optional step for teams adopting a Feature Store pattern.
Creates reusable engineered features shared across training and inference.

🔸 Input:
bash
Copy code
data/processed/train.csv
🔸 Output:
bash
Copy code
data/features/customer_features_v3.csv
🔸 Responsibilities:
Compute aggregates (e.g. avg purchase, churn score)

Save to /data/features

Optionally publish to SageMaker or Feast Feature Store

5️⃣ serve_app.py – FastAPI Inference Service
Containerized FastAPI service that loads the latest model and exposes prediction endpoints.

🔸 Endpoints:
Method	Endpoint	Description
POST	/predict	Submit customer JSON → return prediction
GET	/health	Health check for container

🔸 Example Run:
bash
Copy code
uvicorn src.serve_app:app --host 0.0.0.0 --port 8080
6️⃣ drift_check.py – Data Drift & Monitoring
Automated nightly job (cron or CI/CD) that monitors data drift between training and production datasets.

🔸 Input:
bash
Copy code
data/processed/train.csv
data/predictions/model_v5_outputs.csv
🔸 Output:
bash
Copy code
data/monitoring/drift_summary.csv
data/monitoring/input_stats_<date>.json
🔸 Responsibilities:
Compare new inputs vs. training distribution

Compute drift score

Trigger retraining if threshold exceeded

7️⃣ common.py – Shared Utilities
Contains helper functions, paths, and reusable logic imported across multiple scripts.

🔸 Typical Functions:
python
Copy code
def get_data_path(subdir):
    return os.path.join("data", subdir)

def validate_schema(df, expected_columns):
    missing = set(expected_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

✅ Summary
Script	Purpose	Inputs	Outputs
data_prep.py	Clean and prepare raw data	raw/	interim/, processed/
train.py	Train & log ML model	processed/	models/, mlruns/
register_model.py	Promote model versions	models/	registry
feature_engineering.py	Build reusable features	processed/	features/
serve_app.py	Serve model via API	models/	predictions/
drift_check.py	Monitor drift & trigger retraining	predictions/	monitoring/
common.py	Shared paths & schema utilities	n/a	n/a


Author: David Santana Rivera
Last updated: 10/21/2025