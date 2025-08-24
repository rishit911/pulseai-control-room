# MLOps_Engineer1 – Pipelines & Automation

This module contains ZenML pipelines, validation configs, and artifacts for Engineer 1.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt

zenml init
zenml experiment-tracker register mlflow_tracker --flavor=mlflow || true
zenml stack register engineer1_stack -o default -a default -e mlflow_tracker
zenml stack set engineer1_stack

python -m MLOps_Engineer1.core.pipelines.run_ingestion_validation

# Or run the comprehensive smoke test
python MLOps_Engineer1/smoke_test.py
```

Artifacts land in `MLOps_Engineer1/artifacts/validation/`.

## Optional: View tracking UIs

```bash
# MLflow experiment tracking
mlflow ui  # http://127.0.0.1:5000

# ZenML dashboard  
zenml login --local  # web UI for pipelines and runs
```
