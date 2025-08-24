import streamlit as st
import pandas as pd
from utils.data import load_json, dummy_dir

def render():
    st.title("Recovery & Rollback")
    st.caption(f"Source: {dummy_dir()}")
    rec = load_json("recovery.json")
    events = rec.get("events", [])
    if events:
        st.dataframe(pd.DataFrame(events), use_container_width=True)
    else:
        st.info("No recovery events found.")
