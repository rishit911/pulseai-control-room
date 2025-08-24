# PulseAI — AI Reliability Control Room 

A stylish, production-ready **SaaS dashboard** for AI reliability and observability.

- 🔐 **Login** (Single User Default)
- 🧭 **Left icon navigation**
- 🏠 **Control Room**: KPIs, **radial gauge** (“Time to completion”), parameter **sparklines**, **SPC** with UCL/LCL, **donut** & **histogram**
- 📊 **Model Status**: Accuracy / Precision / Recall (90-day)
- 📉 **Drift & Fairness**: drift **p-value** trend, **accuracy by group**
- 🧪 **Data Health**: missing values
- 🧠 **Explainability**: feature importance (length-safe)
- 📄 **PDF Report**: KPIs + charts only (not a printed web page)
- 🧩 **Integration stubs** for Engineer 1/2/3 (pipelines, monitoring, serving)

**Key Metrics Will Be Updated Later As per Pipelines Data**

---

## Tech Stack

<p align="left">
  <img alt="Python"        src="https://cdn.simpleicons.org/python"            width="48" />
  <img alt="Streamlit"     src="https://cdn.simpleicons.org/streamlit"         width="48" />
  <img alt="Plotly"        src="https://cdn.simpleicons.org/plotly"            width="48" />
  <img alt="Pandas"        src="https://cdn.simpleicons.org/pandas"            width="48" />
  <img alt="NumPy"         src="https://cdn.simpleicons.org/numpy"             width="48" />
  <img alt="FastAPI"       src="https://cdn.simpleicons.org/fastapi"           width="48" />
  <img alt="MLflow"        src="https://cdn.simpleicons.org/mlflow"            width="48" />
  <img alt="Apache Airflow"src="https://cdn.simpleicons.org/apacheairflow"     width="48" />
  <img alt="Prefect"       src="https://cdn.simpleicons.org/prefect"           width="48" />
  <img alt="Jupyter"       src="https://cdn.simpleicons.org/jupyter"           width="48" />
  <img alt="OpenAPI"       src="https://cdn.simpleicons.org/openapiinitiative" width="48" />
  <img alt="Docker"        src="https://cdn.simpleicons.org/docker"            width="48" />
  <img alt="Kubernetes"    src="https://cdn.simpleicons.org/kubernetes"        width="48" />
  <img alt="GitHub"        src="https://cdn.simpleicons.org/github"            width="48" />
</p>

## Quickstart

### Requirements
- Python 3.10+
- VS Code (or any terminal)
- Windows CMD / macOS / Linux

### Setup (VS Code Terminal → **Command Prompt** profile)
```bat
# 1) clone
git clone <your-repo-url> pulseai-control-room
cd pulseai-control-room

# 2) venv
python -m venv .venv
.\.venv\Scripts\activate.bat

# 3) install
pip install -U pip
pip install -r requirements.txt

# 4) run
python -m streamlit run app\main.py
```

## Login credentials
- **Username:** `Devanjan123`
- **Password:** `Dev123`

---

## What’s Done

### UI/UX
- Full-screen **hero login**, **left-half card** (glass effect), rounded inputs with icons, remember/forgot row, white pill submit.
- Sticky gradient **top bar** with role & org badges.
- **Left icon nav** (styled sidebar radio).
- Smooth animations, **dark theme** (glass cards, soft shadows).

### Analytics  (Based On DUMMY DATA)

#### Control Room
- **KPI tiles:** Operator ID, Batches Today, Drift Alerts (24h), OOC%, Queue.
- **Radial gauge** for “Time to completion”.
- **Parameter rows:** sparkline mini-charts + OOC% progress + pass/fail.
- **SPC chart** with mean/UCL/LCL lines.
- **OOC donut** + **value histogram**.

#### Other Tabs
- **Model Status:** KPIs + Accuracy/Precision/Recall timeline (90 days).
- **Drift & Fairness:** Drift p-value timeline; fairness bar by subgroup.
- **Data Health:** Missing values by column.
- **Explainability:** Feature importance chart (safe to variable list length).
- **PDF Report:** A4 multi-page PDF (KPI cover + charts), using Plotly → Kaleido and ReportLab.

---

## Project Structure
<img width="520" height="747" alt="image" src="https://github.com/user-attachments/assets/0e51244e-dedb-4887-9b96-3672aec60ddc" />

## Integration Plan (Engineer 1/2/3)

### Where to plug in

Add real clients in:
- `app/integrations/engineer1_pipelines.py`
- `app/integrations/engineer2_monitoring.py`
- `app/integrations/engineer3_api.py`

Un-comment their imports & (future) tabs in `app/main.py`.

> **IMPORTANT:** **ALL THESE ARE TRAINED ON DUMMY DATA.**  
> Once E1/E2/E3 publish REST endpoints or storage locations (S3/Parquet), replace `utils/data.py` loaders with API calls and bind auth (API keys/JWT) via environment variables.

---

## Roadmap

- **E1 integration:** run/retrain triggers, pipeline status, registry pulls.  
- **E2 integration:** live drift/fairness dashboards, alert banners, thresholds.  
- **E3 integration:** deploy/rollback from the UI, A/B split controls, live `/status`.  
- **Role-based views** (Business vs Eng).  
- **Notebook Runner** (Papermill/Jupytext) to execute training/eval notebooks from inside the app.

---


