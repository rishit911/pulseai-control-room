"""Engineer-1 | UI bridge for potential Streamlit integration.

NOTE: This file is READY to import but this prompt does NOT modify any files under MLOps_Engineer4/.
If/when Engineer 4 chooses, they can import:
    from MLOps_Engineer1.core.integration.ui_bridge import latest_validation_summary, artifact_paths
"""
from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[3]  # .../pulseai-control-room
ART_DIR = BASE / "MLOps_Engineer1" / "artifacts" / "validation"
JSON_FILE = ART_DIR / "validation_results.json"
HTML_FILE = ART_DIR / "validation_report.html"

def latest_validation_summary() -> dict:
    if JSON_FILE.exists():
        data = json.loads(JSON_FILE.read_text())
        return {
            "ok": data.get("ok", False),
            "missing_issues": len(data.get("missing", {})),
            "dtype_issues": len(data.get("dtypes", {})),
            "rule_issues": len(data.get("rules", {})),
            "artifact_path": str(JSON_FILE),
            "report_html_path": str(HTML_FILE) if HTML_FILE.exists() else None
        }
    return {"ok": False, "missing_issues": -1, "dtype_issues": -1, "rule_issues": -1}

def artifact_paths() -> dict:
    return {"json": str(JSON_FILE), "html": str(HTML_FILE)}