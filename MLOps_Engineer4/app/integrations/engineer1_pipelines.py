"""
Engineer 1 – Pipelines & Automation (ZenML + MLflow)
Adapter that delegates to MLOps_Engineer1 without changing UI imports.
Supports dummy mode via env var PULSEAI_USE_DUMMY=1.
Now uses real pipeline data by default with automatic sync.
"""
from typing import Dict
import os

USE_DUMMY = os.getenv("PULSEAI_USE_DUMMY", "0")  # "1" -> dummy

if USE_DUMMY == "1":
    def latest_validation_summary() -> Dict:
        return {
            "ok": False,
            "missing_issues": -1,
            "dtype_issues": -1,
            "rule_issues": -1,
            "artifact_path": None,
            "report_html_path": None,
            "note": "Dummy mode enabled (PULSEAI_USE_DUMMY=1).",
        }

    def artifact_paths() -> Dict:
        return {"json": None, "html": None}

else:
    try:
        from MLOps_Engineer1.core.integration.ui_bridge import (
            latest_validation_summary as _latest,
            artifact_paths as _paths,
        )

        def latest_validation_summary() -> Dict:
            try:
                return _latest()
            except Exception as e:
                return {
                    "ok": False,
                    "missing_issues": -1,
                    "dtype_issues": -1,
                    "rule_issues": -1,
                    "artifact_path": None,
                    "report_html_path": None,
                    "error": f"engineer1 ui_bridge error: {e}",
                }

        def artifact_paths() -> Dict:
            try:
                return _paths()
            except Exception:
                return {"json": None, "html": None}

    except Exception as e:
        def latest_validation_summary() -> Dict:
            return {
                "ok": False,
                "missing_issues": -1,
                "dtype_issues": -1,
                "rule_issues": -1,
                "artifact_path": None,
                "report_html_path": None,
                "error": f"MLOps_Engineer1 not importable: {e}",
            }

        def artifact_paths() -> Dict:
            return {"json": None, "html": None}

def sync_dashboard_data() -> Dict:
    """Manually trigger data sync from Engineer 1 to Engineer 4 dashboard"""
    try:
        from MLOps_Engineer1.core.integration.data_sync import sync_pipeline_data
        return sync_pipeline_data()
    except Exception as e:
        return {"status": "error", "error": str(e)}