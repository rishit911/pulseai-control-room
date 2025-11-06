# Monitoring

Small monitoring engine for data validation, drift detection, fairness checks and artifact emission.

Quick start

1. Create a virtual environment and install dependencies from `requirements.txt`:

   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

2. Update `config/monitor_config.yaml` to point to your data files (by default sample CSVs are provided).

3. Run the monitor:

   python -m monitoring.src.**main**

Outputs are written to `artifacts/latest/` and `artifacts/history/<timestamp>/`.
