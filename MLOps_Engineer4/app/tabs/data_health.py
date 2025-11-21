import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data import load_json

def render():
    st.title("🧪 Data Health")
    
    # Add refresh button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Get validation data
    validation_summary = load_json("validation.json")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = "✅ Passed" if validation_summary.get('ok', False) else "❌ Failed"
        st.metric("Validation Status", status)
    
    with col2:
        st.metric("Missing Issues", validation_summary.get('missing_issues', 0))
    
    with col3:
        st.metric("Data Type Issues", validation_summary.get('dtype_issues', 0))
    
    with col4:
        st.metric("Rule Violations", validation_summary.get('rule_issues', 0))
    
    # Show validation details
    st.subheader("Validation Summary")
    
    if validation_summary.get('ok'):
        st.success("✅ All validation checks passed!")
    else:
        st.error("❌ Validation failed. Please check the issues below.")
    
    # Display artifact paths
    if validation_summary.get('artifact_path'):
        st.info(f"📄 Validation results: `{validation_summary['artifact_path']}`")
    
    if validation_summary.get('report_html_path'):
        st.info(f"📊 HTML report: `{validation_summary['report_html_path']}`")
    
    # Show error if any
    if 'error' in validation_summary:
        st.warning(f"⚠️ {validation_summary['error']}")
    
    # Sync button
    st.subheader("Data Sync")
    if st.button("🔄 Sync Data"):
        with st.spinner("Syncing data..."):
            try:
                from pathlib import Path
                import sys
                base_dir = Path(__file__).resolve().parents[3]
                sys.path.insert(0, str(base_dir))
                from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer
                
                syncer = DataSynchronizer()
                result = syncer.sync_all_data()
                if result.get('status') == 'success':
                    st.success("✅ Data synced successfully!")
                    st.rerun()
                else:
                    st.error("❌ Sync failed")
            except Exception as e:
                st.error(f"❌ Error: {e}")
