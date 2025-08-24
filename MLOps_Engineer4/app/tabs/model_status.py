import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data import load_json, dummy_dir

def render():
    st.title("Model Status")
    st.caption(f"Source: {dummy_dir()}")
    ms = load_json("model_status.json")
    ts = load_json("metrics_timeseries.json")

    cols = st.columns(4)
    cols[0].metric("Active Version", ms.get("active_model", "-"))
    cols[1].metric("Accuracy", f"{ms.get('accuracy', 0):.2f}")
    cols[2].metric("Precision", f"{ms.get('precision', 0):.2f}")
    cols[3].metric("Recall", f"{ms.get('recall', 0):.2f}")

    st.subheader("Performance over time")
    df = pd.DataFrame({
        "date": ts["dates"],
        "accuracy": ts["accuracy"],
        "precision": ts["precision"],
        "recall": ts["recall"],
    })
    df = df.melt(id_vars="date", var_name="metric", value_name="value")
    fig = px.line(df, x="date", y="value", color="metric", markers=True,
                  title="Accuracy / Precision / Recall Timeline")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Rollback History")
    st.write(ms.get("rollback_history", []))
    st.caption(f"Last Trained: {ms.get('last_trained', 'N/A')}")
