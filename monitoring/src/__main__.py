"""Simple orchestrator to run validation, drift and fairness in sequence."""
import os
import json
import logging

from .utils import load_yaml, ensure_dir, write_json, timestamp
from .dataloaders import load_csv
from .validators import validate_config_schema
from .drift_runner import run_drift
from .fairness_runner import run_fairness
from .aggregate_and_alert import aggregate_and_write
from .emit_contracts import emit_contracts


LOG = logging.getLogger("monitor")


def run_monitor():
    here = os.path.dirname(__file__)
    # pkg_root points to the `monitoring` package folder (one level up from src)
    pkg_root = os.path.abspath(os.path.join(here, os.pardir))
    cfg_path = os.path.join(pkg_root, "config", "monitor_config.yaml")
    config = load_yaml(cfg_path)

    # load data (paths are relative to the monitoring package root)
    ref_path = os.path.join(pkg_root, config["data"]["reference"]) if "data" in config else None
    cur_path = os.path.join(pkg_root, config["data"]["current"]) if "data" in config else None
    validation_res = {"config_exists": os.path.exists(cfg_path)}
    if not ref_path or not os.path.exists(ref_path):
        validation_res["reference_exists"] = False
        ref_df = None
    else:
        validation_res["reference_exists"] = True
        ref_df = load_csv(ref_path)
    if not cur_path or not os.path.exists(cur_path):
        validation_res["current_exists"] = False
        cur_df = None
    else:
        validation_res["current_exists"] = True
        cur_df = load_csv(cur_path)

    # run drift & fairness if data present
    drift_res = run_drift(ref_df, cur_df) if ref_df is not None and cur_df is not None else None
    fairness_res = None
    if cur_df is not None:
        sensitive = config.get("sensitive_feature")
        prediction = config.get("prediction")
        label = config.get("label")
        if sensitive and prediction and sensitive in cur_df.columns and prediction in cur_df.columns:
            fairness_res = run_fairness(ref_df, cur_df, sensitive, prediction, label)

    artifacts_latest = os.path.join(pkg_root, "artifacts", "latest")
    artifacts_history = os.path.join(pkg_root, "artifacts", "history")
    ensure_dir(artifacts_latest)
    ensure_dir(artifacts_history)

    # write artifacts and alerts
    aggr = aggregate_and_write(drift_res, fairness_res, validation_res, config, artifacts_latest, artifacts_history)

    # emit contracts
    emit_contracts(artifacts_latest)

    LOG.info("Monitor run completed. Summary: %s", aggr)
    print(json.dumps({"status": "done", "summary": aggr}, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_monitor()
