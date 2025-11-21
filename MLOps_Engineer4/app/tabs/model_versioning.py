"""
Model Versioning Tab - View and manage model versions
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import plotly.graph_objects as go
import plotly.express as px

# Add base dir to path
base_dir = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(base_dir))

from MLOps_Engineer1.core.model_versioning import ModelVersionManager

def render():
    st.title("📦 Model Versioning")
    st.write("View, compare, and manage all trained model versions")
    
    # Initialize version manager
    version_manager = ModelVersionManager()
    
    # Get version stats
    stats = version_manager.get_version_stats()
    
    # Display stats
    st.header("📊 Version Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Versions", stats.get('total_versions', 0))
    with col2:
        st.metric("Current Version", stats.get('current_version', 'None'))
    with col3:
        st.metric("Latest Version", stats.get('latest_version', 'None'))
    with col4:
        st.metric("Models Trained", stats.get('total_models_trained', 0))
    
    # List all versions
    st.header("📋 All Model Versions")
    
    versions = version_manager.list_versions()
    
    if not versions:
        st.info("ℹ️ No model versions found. Train a model to create the first version!")
        return
    
    # Create DataFrame for display
    version_data = []
    current_version = version_manager.get_current_version()
    
    for v in versions:
        is_current = v['version'] == current_version
        
        # Get primary metric based on problem type
        problem_type = v['metrics'].get('problem_type', 'classification')
        if problem_type == 'classification':
            primary_metric = f"{v['metrics'].get('accuracy', 0):.2%}"
            metric_name = "Accuracy"
        else:
            primary_metric = f"{v['metrics'].get('r2_score', 0):.4f}"
            metric_name = "R² Score"
        
        version_data.append({
            'Version': v['version'],
            'Status': '🟢 Current' if is_current else '⚪ Archived',
            'Model': v['model_name'],
            'Type': problem_type.title(),
            metric_name: primary_metric,
            'Features': len(v['features']),
            'Target': v['target'],
            'Trained': v['trained_at'][:19].replace('T', ' ')
        })
    
    df = pd.DataFrame(version_data)
    
    # Display table
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Version Details
    st.header("🔍 Version Details")
    
    selected_version = st.selectbox(
        "Select version to view details",
        options=[v['version'] for v in versions],
        index=0
    )
    
    if selected_version:
        metadata = version_manager.get_version_metadata(selected_version)
        
        if metadata:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Model Information")
                st.write(f"**Version:** {metadata['version']}")
                st.write(f"**Model Type:** {metadata['model_name']}")
                st.write(f"**Problem Type:** {metadata['metrics'].get('problem_type', 'classification')}")
                st.write(f"**Status:** {'🟢 Current' if metadata['version'] == current_version else '⚪ Archived'}")
                st.write(f"**Trained:** {metadata['trained_at'][:19].replace('T', ' ')}")
                
                st.subheader("🎯 Features & Target")
                st.write(f"**Target:** {metadata['target']}")
                st.write(f"**Features ({len(metadata['features'])}):**")
                for feat in metadata['features']:
                    st.write(f"  • {feat}")
            
            with col2:
                st.subheader("📊 Performance Metrics")
                
                problem_type = metadata['metrics'].get('problem_type', 'classification')
                
                if problem_type == 'classification':
                    metrics_to_show = ['accuracy', 'precision', 'recall', 'f1_score']
                    for metric in metrics_to_show:
                        if metric in metadata['metrics']:
                            value = metadata['metrics'][metric]
                            st.metric(metric.replace('_', ' ').title(), f"{value:.2%}")
                else:
                    metrics_to_show = ['r2_score', 'rmse', 'mae', 'mape']
                    for metric in metrics_to_show:
                        if metric in metadata['metrics']:
                            value = metadata['metrics'][metric]
                            if metric == 'mape':
                                st.metric(metric.upper(), f"{value:.2%}" if value > 0 else "N/A")
                            else:
                                st.metric(metric.upper().replace('_', ' '), f"{value:.4f}")
                
                # Feature Importance
                if metadata.get('feature_importance'):
                    st.subheader("🎯 Feature Importance")
                    imp_df = pd.DataFrame([
                        {'Feature': k, 'Importance': v}
                        for k, v in sorted(metadata['feature_importance'].items(), 
                                         key=lambda x: x[1], reverse=True)
                    ])
                    
                    fig = px.bar(imp_df, x='Importance', y='Feature', orientation='h',
                               title='Feature Importance')
                    st.plotly_chart(fig, use_container_width=True)
    
    # Version Comparison
    st.header("⚖️ Compare Versions")
    
    if len(versions) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            version1 = st.selectbox(
                "Select first version",
                options=[v['version'] for v in versions],
                key='compare_v1'
            )
        
        with col2:
            version2 = st.selectbox(
                "Select second version",
                options=[v['version'] for v in versions],
                index=min(1, len(versions)-1),
                key='compare_v2'
            )
        
        if st.button("🔍 Compare Versions"):
            comparison = version_manager.compare_versions(version1, version2)
            
            if comparison:
                st.subheader(f"Comparison: {version1} vs {version2}")
                
                # Model comparison
                st.write(f"**{version1}:** {comparison['model_comparison']['version1_model']}")
                st.write(f"**{version2}:** {comparison['model_comparison']['version2_model']}")
                
                # Metrics comparison
                if comparison['metrics_comparison']:
                    st.subheader("📊 Metrics Comparison")
                    
                    comp_data = []
                    for metric, values in comparison['metrics_comparison'].items():
                        comp_data.append({
                            'Metric': metric.replace('_', ' ').title(),
                            version1: f"{values['version1']:.4f}",
                            version2: f"{values['version2']:.4f}",
                            'Difference': f"{values['difference']:+.4f}",
                            'Change %': f"{values['percent_change']:+.2f}%"
                        })
                    
                    comp_df = pd.DataFrame(comp_data)
                    st.dataframe(comp_df, use_container_width=True, hide_index=True)
                    
                    # Visualization
                    fig = go.Figure()
                    
                    metrics = list(comparison['metrics_comparison'].keys())
                    v1_values = [comparison['metrics_comparison'][m]['version1'] for m in metrics]
                    v2_values = [comparison['metrics_comparison'][m]['version2'] for m in metrics]
                    
                    fig.add_trace(go.Bar(name=version1, x=metrics, y=v1_values))
                    fig.add_trace(go.Bar(name=version2, x=metrics, y=v2_values))
                    
                    fig.update_layout(
                        title='Metrics Comparison',
                        barmode='group',
                        template='plotly_dark'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Train at least 2 models to compare versions")
    
    # Version Management
    st.header("🔧 Version Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔄 Rollback to Version")
        
        rollback_version = st.selectbox(
            "Select version to rollback to",
            options=[v['version'] for v in versions if v['version'] != current_version],
            key='rollback_version'
        )
        
        if st.button("🔄 Rollback", type="primary"):
            if rollback_version:
                with st.spinner(f"Rolling back to {rollback_version}..."):
                    success = version_manager.rollback_to_version(rollback_version)
                    
                    if success:
                        st.success(f"✅ Successfully rolled back to {rollback_version}!")
                        st.info("🔄 Refresh the page to see changes")
                        st.balloons()
                    else:
                        st.error("❌ Rollback failed")
    
    with col2:
        st.subheader("🗑️ Delete Version")
        
        delete_version = st.selectbox(
            "Select version to delete",
            options=[v['version'] for v in versions if v['version'] != current_version],
            key='delete_version'
        )
        
        if st.button("🗑️ Delete", type="secondary"):
            if delete_version:
                if st.session_state.get('confirm_delete') != delete_version:
                    st.session_state.confirm_delete = delete_version
                    st.warning(f"⚠️ Click again to confirm deletion of {delete_version}")
                else:
                    success = version_manager.delete_version(delete_version)
                    
                    if success:
                        st.success(f"✅ Deleted {delete_version}")
                        st.session_state.confirm_delete = None
                        st.rerun()
                    else:
                        st.error("❌ Cannot delete current version")
    
    # Version Timeline
    st.header("📅 Version Timeline")
    
    if versions:
        timeline_data = []
        for v in reversed(versions):  # Oldest first
            problem_type = v['metrics'].get('problem_type', 'classification')
            if problem_type == 'classification':
                metric_val = v['metrics'].get('accuracy', 0)
            else:
                metric_val = v['metrics'].get('r2_score', 0)
            
            timeline_data.append({
                'Version': v['version'],
                'Date': v['trained_at'][:10],
                'Metric': metric_val,
                'Model': v['model_name']
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        
        fig = px.line(
            timeline_df,
            x='Version',
            y='Metric',
            title='Model Performance Over Versions',
            markers=True,
            hover_data=['Model', 'Date']
        )
        
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
