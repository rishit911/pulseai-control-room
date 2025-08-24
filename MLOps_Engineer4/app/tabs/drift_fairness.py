import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data import load_json, dummy_dir

def render():
    st.title("Drift & Fairness")
    st.caption(f"Source: {dummy_dir()}")

    drift = load_json("drift_timeline.json")
    df_drift = pd.DataFrame({"date": drift["dates"], "p_value": drift["p_value"]})
    st.subheader("Data drift p-value over time")
    fig1 = px.line(df_drift, x="date", y="p_value", markers=True,
                   title="Drift p-value (lower means more drift)")
    st.plotly_chart(fig1, use_container_width=True)

    fair = load_json("fairness.json")
    df_fair = pd.DataFrame(fair)
    st.subheader("Group fairness — accuracy by subgroup")
    fig2 = px.bar(df_fair, x="group", y="accuracy", title="Accuracy by Group")
    st.plotly_chart(fig2, use_container_width=True)
