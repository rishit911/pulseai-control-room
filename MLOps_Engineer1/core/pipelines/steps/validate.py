"""Engineer-1 | Validation Step

Validates dtypes & nulls against configs/schema.yaml, writes artifacts,
and logs validation_ok metric and artifacts to MLflow.
"""
from zenml.steps import step
import pandas as pd
from pathlib import Path
import yaml, json
import mlflow

def _dtype_name(series: pd.Series) -> str:
    return str(series.dtype)

@step(enable_cache=False)  # Disable cache to always run fresh validation
def validate_data(df: pd.DataFrame, schema_rel=None) -> str:
    base_dir = Path(__file__).resolve().parents[3]  # .../MLOps_Engineer1
    schema_path = base_dir / "configs" / "schema.yaml"
    schema = yaml.safe_load(schema_path.read_text())
    
    issues = {"missing": {}, "dtypes": {}, "rules": {}, "ok": True}
    
    for col in schema["columns"]:
        name = col["name"]; want = col["dtype"]; allow_null = col["allow_null"]
        
        if name not in df.columns:
            issues["dtypes"][name] = "missing column"; issues["ok"] = False; continue
        
        got = _dtype_name(df[name])
        if want not in got:
            issues["dtypes"][name] = f"expected {want}, got {got}"; issues["ok"] = False
        
        null_frac = df[name].isna().mean()
        if not allow_null and null_frac > 0:
            issues["missing"][name] = f"{null_frac:.2%} nulls (not allowed)"; issues["ok"] = False
    
    max_null_fraction = float(schema["rules"]["max_null_fraction"])
    global_null_frac = df.isna().mean().mean()
    if global_null_frac > max_null_fraction:
        issues["rules"]["max_null_fraction"] = f"{global_null_frac:.2%} > {max_null_fraction:.2%}"
        issues["ok"] = False
    
    art_dir = base_dir / "artifacts" / "validation"
    art_dir.mkdir(parents=True, exist_ok=True)
    
    json_path = art_dir / "validation_results.json"
    html_path = art_dir / "validation_report.html"
    
    json_path.write_text(json.dumps(issues, indent=2))
    html_path.write_text(f"<html><body><h2>Data Validation Report</h2><pre>{json.dumps(issues, indent=2)}</pre></body></html>")
    
    with mlflow.start_run(run_name="validation"):
        mlflow.log_artifact(str(json_path), artifact_path="validation")
        mlflow.log_artifact(str(html_path), artifact_path="validation")
        mlflow.log_dict(issues, "validation/validation_results.json")
        mlflow.log_metric("validation_ok", 1.0 if issues["ok"] else 0.0)
    
    # Sync data to Engineer 4 dashboard
    try:
        from MLOps_Engineer1.core.integration.data_sync import sync_pipeline_data
        sync_result = sync_pipeline_data()
        print(f"✅ Data synced to Engineer 4 dashboard: {sync_result.get('status', 'unknown')}")
    except Exception as e:
        print(f"⚠️ Data sync failed: {e}")
    
    return str(json_path)