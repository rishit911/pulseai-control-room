import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data import load_json, dummy_dir

def render():
    st.title("Data Health")
    st.caption(f"Source: {dummy_dir()}")
    data = load_json("validation.json")
    mv = pd.DataFrame(list(data.get("missing_values", {}).items()),
                      columns=["column", "missing_count"])
    st.metric("Rows", data.get("row_count", 0))
    st.subheader("Missing values by column")
    fig = px.bar(mv, x="column", y="missing_count", title="Missing Values")
    st.plotly_chart(fig, use_container_width=True)
