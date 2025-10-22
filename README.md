mlops-project/
├─ data/ # stores raw, processed, and monitoring data
├─ src/ # scripts for preprocessing, training, drift detection
├─ docker/ # Dockerfiles for serving and training
├─ infra/ # IaC configs (Terraform, Helm)
└─ notebooks/ # Jupyter notebooks for EDA

Workflow (Steady State Pipeline)

1️⃣ Receive new data /data/raw !> 
A new dataset lands automatically (from data team, S3 upload, SQL extract, or a manual file drop).

2️⃣ Pipeline triggers automatically > 
CI/CD or an ML orchestration tool (SageMaker Pipeline, Vertex AI, Azure ML, Jenkins, etc.) detects new data and runs the pipeline: data prep → training → validation → model registry → deploy.

3️⃣ Monitor run status > 
You check logs, metrics, or dashboards (MLflow, SageMaker Studio, Vertex Pipelines, Grafana, or App Insights).

4️⃣ New model deployed >
The CI/CD job automatically builds a new container/image or updates the production endpoint.

5️⃣ Monitor live models >!
Watch latency, accuracy drift, or cost metrics.
