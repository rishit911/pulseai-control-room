@echo off
SETLOCAL
REM One-click: setup venv, install deps, init ZenML, run pipeline, launch Streamlit (Windows)

IF NOT EXIST .venv (
  python -m venv .venv
)
call .venv\Scripts\activate

pip install -U pip
pip install -r requirements.txt

REM Init ZenML + MLflow tracker (idempotent)
zenml init
zenml experiment-tracker register mlflow_tracker --flavor=mlflow 2> NUL || echo tracker exists
zenml stack register engineer1_stack -o default -a default -e mlflow_tracker 2> NUL || echo stack exists
zenml stack set engineer1_stack 2> NUL || echo stack set

REM Run pipeline and smoke test
python -m MLOps_Engineer1.core.pipelines.run_ingestion_validation
python MLOps_Engineer1\smoke_test.py

REM Sync real pipeline data to dashboard
echo 🔄 Syncing real pipeline data to dashboard...
python scripts\sync_data.py

REM Launch Streamlit UI with real data (Ctrl+C to stop)
echo 🚀 Starting Streamlit UI with real data...
python -m streamlit run MLOps_Engineer4\app\main.py
ENDLOCAL