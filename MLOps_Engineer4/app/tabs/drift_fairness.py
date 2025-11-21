import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Removed unused import

def render():
    st.title("📉 Drift & Fairness")
    
    # Add refresh and cache clear buttons
    col1, col2, col3 = st.columns([5, 1, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    with col3:
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
    
    # Auto-sync data button
    if st.button("🔄 Sync Data", help="Sync monitoring data with latest model"):
        with st.spinner("Syncing data..."):
            try:
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
                    st.error(f"❌ Sync failed: {result.get('error')}")
            except Exception as e:
                st.error(f"❌ Sync error: {e}")
    
    # Force reload monitoring data from disk (no caching)
    from pathlib import Path
    import json
    import sys
    import os
    
    base_dir = Path(__file__).resolve().parents[3]
    monitoring_dir = base_dir / "MLOps_Engineer2" / "artifacts" / "monitoring"
    
    # Load latest monitoring data directly (with file timestamp check)
    drift_metrics = {}
    fairness_data = {}
    drift_hist = {}
    
    latest_monitoring_file = monitoring_dir / "latest_monitoring.json"
    if latest_monitoring_file.exists():
        try:
            # Show file timestamp for debugging
            mtime = os.path.getmtime(latest_monitoring_file)
            from datetime import datetime
            last_update = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            st.caption(f"📊 Monitoring data last updated: {last_update}")
            
            with open(latest_monitoring_file, 'r') as f:
                latest_data = json.load(f)
                drift_metrics = latest_data.get('drift', {})
                fairness_data = latest_data.get('fairness', {})
        except Exception as e:
            st.warning(f"Could not load monitoring data: {e}")
    
    monitoring_report_file = monitoring_dir / "monitoring_report.json"
    if monitoring_report_file.exists():
        try:
            with open(monitoring_report_file, 'r') as f:
                drift_hist = json.load(f)
        except Exception as e:
            pass
    
    # If no monitoring data exists, show message
    if not drift_metrics and not fairness_data:
        st.info("ℹ️ No monitoring data available yet. Monitoring data is generated after model training.")
        st.write("The monitoring system tracks:")
        st.write("- **Drift Detection**: Compares new data against training baseline")
        st.write("- **Fairness Analysis**: Checks model performance across demographic groups")
        st.write("\nMonitoring data will appear here after you train a model.")
    
    # Drift Detection Section
    st.subheader("🔍 Data Drift Detection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        drift_status = "🚨 Detected" if drift_metrics.get('drift_detected', False) else "✅ No Drift"
        st.metric("Drift Status", drift_status)
    
    with col2:
        summary = drift_metrics.get('summary', {})
        st.metric("Drifted Features", summary.get('drifted_features', 0))
    
    with col3:
        drift_pct = summary.get('drift_percentage', 0)
        st.metric("Drift Percentage", f"{drift_pct:.1f}%")
    
    # Feature-level drift
    if 'features' in drift_metrics and drift_metrics['features']:
        st.subheader("Feature-Level Drift Analysis")
        
        feature_data = []
        for feature, metrics in drift_metrics['features'].items():
            feature_data.append({
                'Feature': feature,
                'P-Value': metrics['p_value'],
                'Drift': '🚨 Yes' if metrics['drift'] else '✅ No',
                'Statistic': metrics['statistic']
            })
        
        df_features = pd.DataFrame(feature_data)
        st.dataframe(df_features, use_container_width=True)
    
    # Drift timeline
    if drift_hist.get('drift_history'):
        st.subheader("Drift Trend Over Time")
        
        hist_data = drift_hist['drift_history']
        df_drift = pd.DataFrame(hist_data)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df_drift['date'],
            y=df_drift['p_value'],
            mode='lines+markers',
            name='P-Value',
            line=dict(color='#636EFA', width=2)
        ))
        
        # Add threshold line
        fig1.add_hline(y=0.05, line_dash="dash", line_color="red", 
                      annotation_text="Drift Threshold (p=0.05)")
        
        fig1.update_layout(
            title="Drift P-Value Over Time (90 Days)",
            xaxis_title="Date",
            yaxis_title="P-Value",
            hovermode='x unified',
            template='plotly_dark'
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    # Fairness Section
    st.subheader("⚖️ Model Fairness Analysis")
    
    if fairness_data.get('groups'):
        # Show fairness data timestamp
        if 'timestamp' in fairness_data:
            st.caption(f"⏰ Fairness analysis timestamp: {fairness_data['timestamp']}")
        
        # Fairness score
        fairness_score = fairness_data.get('fairness_score', 1.0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Fairness Score", f"{fairness_score:.3f}", 
                     help="Ratio of min/max accuracy across groups (1.0 = perfect fairness)")
        
        with col2:
            fairness_status = "✅ Fair" if fairness_score > 0.8 else "⚠️ Bias Detected"
            st.metric("Status", fairness_status)
        
        # Group-level metrics
        st.subheader("Accuracy by Demographic Group")
        
        group_data = []
        for group, metrics in fairness_data['groups'].items():
            group_data.append({
                'Group': group,
                'Accuracy': metrics['accuracy'],
                'Positive Rate': metrics['positive_prediction_rate'],
                'Sample Size': metrics['sample_size']
            })
        
        df_fair = pd.DataFrame(group_data)
        
        fig2 = px.bar(
            df_fair, 
            x='Group', 
            y='Accuracy',
            title='Model Accuracy by Demographic Group',
            color='Accuracy',
            color_continuous_scale='RdYlGn',
            text='Accuracy'
        )
        fig2.update_traces(texttemplate='%{text:.2%}', textposition='outside')
        fig2.update_layout(template='plotly_dark')
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Detailed table
        st.dataframe(df_fair, use_container_width=True)
    else:
        st.info("ℹ️ No fairness data available. Run monitoring pipeline with predictions.")
    
    # Show notes/errors
    if 'note' in drift_metrics:
        st.info(f"ℹ️ {drift_metrics['note']}")
    if 'error' in drift_metrics:
        st.warning(f"⚠️ {drift_metrics['error']}")
