📘 This repository serves as a working MLOps blueprint for data pipelines, model lifecycle automation, and deployment — all runnable locally or in cloud environments.

# 🧠 MLOps Project

End-to-end example of a **production-grade MLOps pipeline** — from raw data ingestion to model serving and continuous monitoring.

---

## 💼 Scenario

**MyAiToolset LLC** provides managed **AI automation and chatbot software** solutions designed for small to mid-sized businesses.  
The company targets a diverse range of industries including **Medical, Dental, Legal, Home Services, Real Estate, Fitness, Education, Ecommerce, Automotive,** and **Restaurant** sectors.

Currently, MyAiToolset offers **four subscription packages**, each tailored to the level of automation, update frequency, and support required by the client:

| Package | Monthly Price | Description |
|----------|----------------|--------------|
| **Business** | $150 | Standard plan for small businesses that need reliable chatbot automation with monthly updates and maintenance. |
| **Elite** | $250 | Includes faster content updates, priority support, and weekly optimization refreshes. |
| **MVP** | $350 | Designed for high-traffic or seasonal businesses needing frequent updates and 2–4 hour response time. |
| **Now** | $500 | Premium tier with real-time monitoring, live deployment updates, and near-instant support. |

Each package also requires a **one-time setup fee of $399**, which covers onboarding, chatbot customization, and initial content training.

---

## 🚀 Overview

This project operationalizes **lead prediction** and **sales intelligence** for MyAiToolset by connecting:

- 📨 **Formspree** → Website form submissions (leads)  
- 💳 **Stripe** → Payment and plan purchase data  
- 🧹 **ETL + Feature Engineering** → Transform lead + payment data into model-ready datasets  
- 🤖 **Model Training + Registry** → Predict plan tier likelihood  
- 🌐 **FastAPI Deployment** → Serve real-time predictions for new leads  
- 📈 **Monitoring** → Track accuracy and drift as new customers arrive  

The entire system forms a **data-driven sales forecasting loop** that continuously improves as the business grows.

---

## 🎯 Model Goal / Objective

Using form submissions collected through **Formspree** (customers.csv) and **Stripe** (transactions.json), the goal is to:
- **Predict which plan tier** a new lead is most likely to purchase, based on their **Business Type** and **Business Size**.  
- Enable **lead scoring and targeted offers** by analyzing historical customer purchase patterns.  
- Automatically update the model as new sign-ups and transactions flow in through the production system via automated ETL.

---

### 🧩 Data Sources

This model uses two primary data sources:

| Source File | Description |
|--------------|-------------|
| `customers.csv` | Contains static information about each customer such as age, region, signup date, and loyalty points. |
| `transactions.json` | Contains dynamic purchase data including transaction amount, timestamp, and payment method. |

---

### 🧠 What the Model Learns
The model classifies each new lead into one of four **MyAiToolset packages**:

| Label | Package | Monthly Price |
|--------|----------|----------------|
| 0 | Business | $150 |
| 1 | Elite | $250 |
| 2 | MVP | $350 |
| 3 | Now | $500 |

After combining website form submissions with payment records:
1. Encodes categorical features (business_type, business_size).
2. Learns correlations between customer demographics and purchased plan tier.
3. Predicts the most likely package for future leads.

Example:

{
  "business_type": "Dental",
  "business_size": "10-25"
}
→ Predicted: "MVP ($350/mo)"

---

### ⚙️ Model Workflow

1. **Detect new data** in `data/raw/` — new leads arrive via **Formspree** (`customers.csv`) and payment data via **Stripe** (`transactions.json`).  
2. **Clean and join datasets** — ETL pipeline merges both sources to produce a unified `data/processed/train.csv` dataset.  
3. **Train a RandomForestClassifier** to predict which **plan tier** (Business, Elite, MVP, Now) a new lead is most likely to purchase.  
4. **Register and deploy the model** via FastAPI for real-time inference.  
   - **Input Example:** `{ "business_type": "Dental", "business_size": "10-25" }`  
   - **Output Example:** `{ "predicted_package": "MVP", "probability": 0.82 }`  
5. **Monitor model drift** and automatically retrain when the distribution of business types, sizes, or package selections shifts over time.

---

The end-to-end goal is to create a **self-updating, data-driven system** that helps identify which customers are most likely to make large purchases — enabling smarter marketing, retention, and sales strategies.

## 🧠 How the Pipeline Works
This pipeline follows an **event-driven orchestration model**, where each stage runs automatically when new data arrives or the previous job completes successfully.

---

### ⚡ Event Flow Overview

1️⃣ **Data Ingestion**  
- Formspree emails parsed into `data/raw/customers.csv`.  
- Stripe payment exports synced to `data/raw/transactions.json`.  
- ETL pipeline triggered via scheduled job or webhook.

2️⃣ **Data Preparation**  
- `src/data_prep.py` cleans and merges lead and transaction data.  
- Produces unified `train.csv` with encoded `business_type` and `business_size`.

3️⃣ **Feature Engineering**  
- `src/feature_engineering.py` converts categorical values to numerical features.  
- Adds label column `package_tier`.

4️⃣ **Model Training & Validation**  
- `src/train.py` trains a **RandomForestClassifier** to predict `package_tier`.  
- Logs accuracy and model version.

5️⃣ **Model Registry & Promotion**  
- `src/register_model.py` stores the trained model if performance exceeds prior baseline.  
- Triggers deployment.

6️⃣ **Model Deployment & Serving**  
- `src/deploy_model.py` rebuilds the FastAPI container exposing `/predict`.  
- Input: `{ "business_type": "Dental", "business_size": "10-25" }`  
- Output: `{ "predicted_package": "MVP", "probability": 0.82 }`

7️⃣ **Monitoring & Retraining Loop**  
- `src/monitor_drift.py` detects changes in business distribution or conversion patterns.  
- Retrains model automatically when drift exceeds threshold.

---

## 🔄 Event-Driven Pipeline Graph

```text
          ┌───────────────────────────┐
          │  📨 Formspree Leads       │
          │  (customers.csv)          │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 💳 Stripe Transactions     │
          │ (transactions.json)        │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ ⚙️  Data Preparation Job  │
          │ Merge & Clean Datasets    │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🧮 Feature Engineering     │
          │ Encode Type & Size        │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🤖 Model Training          │
          │ Predict Plan Tier          │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🏷️  Model Registry         │
          │ Version & Promotion       │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 🚀 Deployment (FastAPI)   │
          │ Exposes /predict Endpoint │
          └──────────────┬────────────┘
                         │
                         ▼
          ┌───────────────────────────┐
          │ 📈 Monitoring & Drift      │
          │ Auto-Retrain Trigger Loop │
          └───────────────────────────┘
```

### 🧭 Automation
Local / Sandbox Mode: Sequential execution via make run-all or bash pipeline.sh.

Cloud Mode: Orchestrated by Prefect, Airflow, or AWS Step Functions.

Triggers:
- Formspree → new lead CSV
- Stripe → new transaction JSON
- Scheduler → nightly retrain job

Self-Healing Loop: Model retrains when drift or prediction confidence drops below threshold.

### 🧩 Tech Stack
| Layer                   | Tools                                          |
| ----------------------- | ---------------------------------------------- |
| 💻 **Language**         | Python 3.10+                                   |
| 📚 **Libraries**        | pandas, scikit-learn, joblib, FastAPI, uvicorn |
| 💾 **Storage**          | Local `/data/` (simulated Formspree + Stripe)  |
| 🔄 **Orchestration**    | Prefect / Airflow / AWS Step Functions         |
| 🧾 **Model Registry**   | MLflow                                         |
| 💳 **Integration APIs** | Formspree, Stripe                              |
| 🚀 **Deployment**       | FastAPI on Render                              |
| 📈 **Monitoring**       | Drift metrics, accuracy tracking               |

### ⚙️ Running the Pipeline

1️⃣ **Prepare environment**
```bash
pip install -r requirements.txt
```

2️⃣ Run data preparation
```bash
python src/data_prep.py
```

3️⃣ Generate Features
```bash
python src/feature_engineering.py
```

4️⃣ Train the model
```bash
python src/train.py
```

4️⃣ Register model
```bash
python src/register_model.py
```

5️⃣ Register and Deploy model
```bash
python src/register_model.py && python src/deploy_model.py
```

6️⃣ Monitor drift and Retrain model
```bash
python src/drift_check.py
```

### ✅ Author & Versioning
Author: David Santana Rivera

Updated: 10-24-2025
