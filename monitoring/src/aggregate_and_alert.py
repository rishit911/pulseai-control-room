import os
from .utils import write_json, ensure_dir, timestamp


def aggregate_and_write(drift_res, fairness_res, validation_res, config, out_latest, out_history_root):
    summary = {
        "drift": drift_res,
        "fairness": fairness_res,
        "validation": validation_res,
        "timestamp": timestamp(),
    }
    ensure_dir(out_latest)
    latest_path = os.path.join(out_latest, "summary.json")
    write_json(latest_path, summary)

    # history
    ts = summary["timestamp"].replace(":", "-")
    hist_dir = os.path.join(out_history_root, ts)
    ensure_dir(hist_dir)
    write_json(os.path.join(hist_dir, "summary.json"), summary)
    # also write sub-artifacts
    if drift_res is not None:
        write_json(os.path.join(out_latest, "drift.json"), drift_res)
        write_json(os.path.join(hist_dir, "drift.json"), drift_res)
    if fairness_res is not None:
        write_json(os.path.join(out_latest, "fairness.json"), fairness_res)
        write_json(os.path.join(hist_dir, "fairness.json"), fairness_res)
    if validation_res is not None:
        write_json(os.path.join(out_latest, "validation.json"), validation_res)
        write_json(os.path.join(hist_dir, "validation.json"), validation_res)

    # simple alert logic
    alerts = []
    drift_threshold = config.get("metrics", {}).get("drift_threshold_mean_diff", None)
    fairness_threshold = config.get("metrics", {}).get("fairness_disparity_threshold", None)
    max_drift = drift_res.get("max") if drift_res else None
    if max_drift is not None and drift_threshold is not None and max_drift > drift_threshold:
        alerts.append({"type": "drift", "value": max_drift, "threshold": drift_threshold})
    disparity = fairness_res.get("disparity") if fairness_res else None
    if disparity is not None and fairness_threshold is not None and disparity > fairness_threshold:
        alerts.append({"type": "fairness", "value": disparity, "threshold": fairness_threshold})

    write_json(os.path.join(out_latest, "alerts.json"), alerts)
    write_json(os.path.join(hist_dir, "alerts.json"), alerts)
    return {"summary_path": latest_path, "alerts": alerts}
