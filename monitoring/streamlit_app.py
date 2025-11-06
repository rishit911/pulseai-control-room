"""Streamlit viewer for the monitoring artifacts.

Run with:
  python -m streamlit run monitoring\streamlit_app.py

This app reads `monitoring/artifacts/latest` and `monitoring/artifacts/history`.
"""
import os
import json
import streamlit as st
import pandas as pd


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def list_history_dirs(history_root):
    if not os.path.isdir(history_root):
        return []
    entries = [d for d in os.listdir(history_root) if os.path.isdir(os.path.join(history_root, d))]
    entries.sort(reverse=True)
    return entries


pkg_root = os.path.dirname(__file__)
art_latest = os.path.join(pkg_root, "artifacts", "latest")
art_history = os.path.join(pkg_root, "artifacts", "history")

st.set_page_config(page_title="AI Reliability Dashboard", layout="wide")

st.title("AI Reliability Dashboard — Monitor Viewer")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Latest run")
    summary = load_json(os.path.join(art_latest, "summary.json"))
    drift = load_json(os.path.join(art_latest, "drift.json"))
    fairness = load_json(os.path.join(art_latest, "fairness.json"))
    validation = load_json(os.path.join(art_latest, "validation.json"))
    alerts = load_json(os.path.join(art_latest, "alerts.json"))

    if summary is None:
        st.warning("No latest summary found — run the monitor first.")
    else:
        st.subheader("Summary")
        st.json(summary)

    if drift:
        st.subheader("Drift — per-column")
        per_col = drift.get("per_column", {})
        df_drift = pd.DataFrame(list(per_col.items()), columns=["column", "score"]).set_index("column")
        st.dataframe(df_drift)
        if not df_drift.empty:
            st.bar_chart(df_drift)

    if fairness:
        st.subheader("Fairness")
        st.json(fairness)
        per_group = fairness.get("per_group_positive_rate") or {}
        if per_group:
            df_fg = pd.DataFrame(list(per_group.items()), columns=["group", "positive_rate"]).set_index("group")
            st.dataframe(df_fg)
            st.bar_chart(df_fg)

    if alerts:
        st.subheader("Alerts")
        st.write(alerts)

with col2:
    st.header("History")
    runs = list_history_dirs(art_history)
    sel = st.selectbox("Select historical run", options=["(none)"] + runs, index=0)
    if sel and sel != "(none)":
        hist_dir = os.path.join(art_history, sel)
        st.subheader(f"Artifacts for {sel}")
        hist_drift = load_json(os.path.join(hist_dir, "drift.json"))
        hist_fair = load_json(os.path.join(hist_dir, "fairness.json"))
        hist_val = load_json(os.path.join(hist_dir, "validation.json"))
        hist_summary = load_json(os.path.join(hist_dir, "summary.json"))
        st.json({"summary": hist_summary})
        if hist_drift:
            st.write("Drift per column")
            df = pd.DataFrame(list(hist_drift.get("per_column", {}).items()), columns=["column", "score"]).set_index("column")
            st.dataframe(df)
            st.bar_chart(df)
        if hist_fair:
            st.write("Fairness")
            st.json(hist_fair)

st.markdown("---")
st.caption("This viewer reads artifacts written by the monitoring engine (JSON files under `monitoring/artifacts`).")
