#!/usr/bin/env bash
set -euo pipefail
# One-click: setup venv, install deps, init ZenML, run pipeline, launch Streamlit (Unix/macOS)

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt

# Init ZenML + MLflow tracker (idempotent)
zenml init
zenml experiment-tracker register mlflow_tracker --flavor=mlflow || true
zenml stack register engineer1_stack -o default -a default -e mlflow_tracker || true
zenml stack set engineer1_stack || true

# Run pipeline and smoke test
python -m MLOps_Engineer1.core.pipelines.run_ingestion_validation
python MLOps_Engineer1/smoke_test.py

# Launch Streamlit UI (Ctrl+C to stop)
python -m streamlit run MLOps_Engineer4/app/main.py