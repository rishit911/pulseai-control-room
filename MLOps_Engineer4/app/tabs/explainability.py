import streamlit as st # type: ignore
import pandas as pd
import plotly.express as px # type: ignore
from utils.data import load_json, dummy_dir

def render():
    st.title("Explainability")
    st.caption(f"Source: {dummy_dir()}")

    # ✅ load the JSON first (this was missing)
    exp = load_json("explainability.json")

    st.subheader("Plain-English Summary")
    st.write(exp.get("summary", "No summary available."))

    # --- Feature importance (safe against length mismatches) ---
    st.subheader("Feature importance (SHAP)")
    features = list(exp.get("shap_top_features", []))

    if not features:
        st.info("No feature importances available.")
        return

    n = len(features)
    # Build a decreasing series of importances of length n
    if n == 1:
        importances = [0.4]
    else:
        hi, lo = 0.45, 0.08
        step = (hi - lo) / (n - 1)
        importances = [round(hi - i * step, 3) for i in range(n)]

    feats = pd.DataFrame({"feature": features, "importance": importances})
    fig = px.bar(feats, x="feature", y="importance", title="Top Features")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Note:** Feature importance values are illustrative and do not reflect actual model outputs.")