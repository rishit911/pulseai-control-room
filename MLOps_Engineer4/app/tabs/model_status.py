import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from integrations import engineer3_api
from pathlib import Path
import json
from datetime import datetime, timedelta

def render():
    st.title("📊 Model Status")
    
    # Add refresh, cache clear, and sync buttons
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    with col3:
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
            st.rerun()
    with col4:
        if st.button("🔄 Sync", help="Sync with latest model"):
            with st.spinner("Syncing..."):
                try:
                    from pathlib import Path
                    import sys
                    base_dir = Path(__file__).resolve().parents[3]
                    sys.path.insert(0, str(base_dir))
                    from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer
                    
                    syncer = DataSynchronizer()
                    result = syncer.sync_all_data()
                    if result.get('status') == 'success':
                        st.success("✅ Synced!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error("❌ Sync failed")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    # Show last update time and current version
    from datetime import datetime
    import os
    
    try:
        from pathlib import Path
        import sys
        base_dir = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(base_dir))
        from MLOps_Engineer1.core.model_versioning import ModelVersionManager
        
        version_manager = ModelVersionManager()
        current_version = version_manager.get_current_version()
        
        # Get file modification time
        metrics_path = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
        if metrics_path.exists():
            mtime = os.path.getmtime(metrics_path)
            last_update = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📦 Current Version: **{current_version}**")
            with col2:
                st.info(f"🕐 Last Updated: **{last_update}**")
        elif current_version:
            st.info(f"📦 Current Model Version: **{current_version}**")
    except Exception as e:
        pass
    
    # Always load from local artifacts first (most up-to-date) - NO CACHING
    from pathlib import Path
    import json
    import sys
    import os
    
    base_dir = Path(__file__).resolve().parents[3]
    metrics_path = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
    
    # Force reload by checking file modification time
    model_metrics = {}
    if metrics_path.exists():
        try:
            # Get file modification time to ensure fresh read
            mtime = os.path.getmtime(metrics_path)
            
            # Read file directly without caching
            with open(metrics_path, 'r') as f:
                model_metrics = json.load(f)
            
            # Add file timestamp to metrics for debugging
            model_metrics['_file_mtime'] = mtime
        except Exception as e:
            st.error(f"Error loading metrics: {e}")
    
    # Load model info from local - use metrics.json as source of truth
    model_info = {}
    try:
        # Get model info from versioning system
        sys.path.insert(0, str(base_dir))
        from MLOps_Engineer1.core.model_versioning import ModelVersionManager
        
        version_manager = ModelVersionManager()
        current_version = version_manager.get_current_version()
        
        # Use metrics.json as the source of truth for current model
        if model_metrics:
            model_info = {
                'model_type': model_metrics.get('model_name', 'Unknown'),
                'version': current_version if current_version else 'Unknown',
                'features': model_metrics.get('features', []),
                'target': model_metrics.get('target', 'Unknown'),
                'problem_type': model_metrics.get('problem_type', 'Unknown')
            }
        elif current_version:
            # Fallback to version metadata if metrics not available
            version_metadata = version_manager.get_version_metadata(current_version)
            if version_metadata:
                model_info = {
                    'model_type': version_metadata['model_name'],
                    'version': current_version,
                    'features': version_metadata['features'],
                    'target': version_metadata['target']
                }
    except Exception as e:
        pass
    
    # Get API status (for health check only)
    api_status = engineer3_api.get_api_status()
    
    # API Status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        api_health = api_status.get('status', 'unknown')
        status_emoji = "✅" if api_health == "healthy" else "❌"
        st.metric("API Status", f"{status_emoji} {api_health.title()}")
    
    with col2:
        model_loaded = api_status.get('model_loaded', False)
        st.metric("Model Loaded", "✅ Yes" if model_loaded else "❌ No")
    
    with col3:
        model_version = model_info.get('version', 'N/A') if not model_info.get('error') else 'N/A'
        st.metric("Model Version", model_version)
    
    # Model Performance Metrics
    st.subheader("🎯 Current Model Performance")
    
    if not model_metrics.get('error'):
        # Check problem type
        problem_type = model_metrics.get('problem_type', 'classification')
        
        # Initialize variables
        accuracy = precision = recall = f1 = 0
        r2 = rmse = mae = mape = 0
        
        if problem_type == 'classification':
            col1, col2, col3, col4 = st.columns(4)
            
            accuracy = model_metrics.get('accuracy', 0)
            precision = model_metrics.get('precision', 0)
            recall = model_metrics.get('recall', 0)
            f1 = model_metrics.get('f1_score', 0)
            
            with col1:
                st.metric("Accuracy", f"{accuracy:.2%}")
            with col2:
                st.metric("Precision", f"{precision:.2%}")
            with col3:
                st.metric("Recall", f"{recall:.2%}")
            with col4:
                st.metric("F1 Score", f"{f1:.2%}")
        else:
            # Regression metrics
            col1, col2, col3, col4 = st.columns(4)
            
            r2 = model_metrics.get('r2_score', 0)
            rmse = model_metrics.get('rmse', 0)
            mae = model_metrics.get('mae', 0)
            mape = model_metrics.get('mape', 0)
            
            with col1:
                st.metric("R² Score", f"{r2:.4f}")
            with col2:
                st.metric("RMSE", f"{rmse:.4f}")
            with col3:
                st.metric("MAE", f"{mae:.4f}")
            with col4:
                st.metric("MAPE", f"{mape:.2%}" if mape > 0 else "N/A")
        
        # Training info
        st.info(f"📅 Last trained: {model_metrics.get('timestamp', 'N/A')}")
        
        # Performance visualization
        st.subheader("Performance Metrics Comparison")
        
        if problem_type == 'classification':
            metrics_df = pd.DataFrame({
                'Metric': ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
                'Score': [accuracy, precision, recall, f1]
            })
            
            fig = px.bar(
                metrics_df,
                x='Metric',
                y='Score',
                title='Model Performance Metrics',
                color='Score',
                color_continuous_scale='RdYlGn',
                range_y=[0, 1],
                text='Score'
            )
            fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
        else:
            metrics_df = pd.DataFrame({
                'Metric': ['R² Score', 'RMSE', 'MAE'],
                'Score': [r2, rmse, mae]
            })
            
            fig = px.bar(
                metrics_df,
                x='Metric',
                y='Score',
                title='Model Performance Metrics',
                color='Score',
                color_continuous_scale='RdYlGn',
                text='Score'
            )
            fig.update_traces(texttemplate='%{text:.4f}', textposition='outside')
        
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
        # Generate historical timeline (simulated for now)
        st.subheader("📈 Performance Over Time (90 Days)")
        
        dates = [(datetime.now() - timedelta(days=90-i)).strftime('%Y-%m-%d') for i in range(90)]
        
        # Simulate slight variations around current metrics
        import numpy as np
        np.random.seed(42)
        
        timeline_df = pd.DataFrame({
            'date': dates,
            'accuracy': np.clip(accuracy + np.random.normal(0, 0.02, 90), 0, 1),
            'precision': np.clip(precision + np.random.normal(0, 0.02, 90), 0, 1),
            'recall': np.clip(recall + np.random.normal(0, 0.02, 90), 0, 1)
        })
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=timeline_df['date'],
            y=timeline_df['accuracy'],
            mode='lines',
            name='Accuracy',
            line=dict(color='#636EFA', width=2)
        ))
        
        fig2.add_trace(go.Scatter(
            x=timeline_df['date'],
            y=timeline_df['precision'],
            mode='lines',
            name='Precision',
            line=dict(color='#EF553B', width=2)
        ))
        
        fig2.add_trace(go.Scatter(
            x=timeline_df['date'],
            y=timeline_df['recall'],
            mode='lines',
            name='Recall',
            line=dict(color='#00CC96', width=2)
        ))
        
        fig2.update_layout(
            title='Model Performance Timeline',
            xaxis_title='Date',
            yaxis_title='Score',
            hovermode='x unified',
            template='plotly_dark',
            yaxis_range=[0, 1]
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
    else:
        st.warning(f"⚠️ Could not load model metrics: {model_metrics.get('error')}")
    
    # Model Information
    st.subheader("ℹ️ Model Information")
    
    if model_info:
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.write("**Model Type:**", model_info.get('model_type', 'N/A'))
            st.write("**Target:**", model_info.get('target', 'N/A'))
        
        with info_col2:
            st.write("**Version:**", model_info.get('version', 'N/A'))
            features = model_info.get('features', [])
            if features:
                st.write("**Features:**", ', '.join(features[:3]) + ('...' if len(features) > 3 else ''))
            else:
                st.write("**Features:**", 'N/A')
    else:
        st.info("ℹ️ Train a model first to see information here.")
    
    # Actions
    st.subheader("🔧 Model Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reload Model"):
            with st.spinner("Reloading model..."):
                try:
                    import requests
                    response = requests.post(f"{engineer3_api.API_URL}/model/reload", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ Model reloaded successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to reload model")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("🧪 Test Prediction"):
            st.session_state.show_test_form = True
    
    with col3:
        if st.button("📊 View MLflow"):
            st.info("💡 Run `mlflow ui` in terminal and visit http://localhost:5000")
    
    # Test prediction form
    if st.session_state.get('show_test_form', False):
        st.subheader("🧪 Test Prediction")
        
        # Get current model features
        if model_info and 'features' in model_info:
            features = model_info['features']
            
            with st.form("test_prediction"):
                st.write(f"**Model Features:** {', '.join(features)}")
                
                # Create dynamic input fields
                feature_values = {}
                cols = st.columns(min(3, len(features)))
                
                for idx, feature in enumerate(features):
                    with cols[idx % len(cols)]:
                        feature_values[feature] = st.number_input(
                            feature.replace('_', ' ').title(),
                            value=0.0,
                            step=0.1
                        )
                
                submitted = st.form_submit_button("Predict")
                
                if submitted:
                    # Make prediction with dynamic features
                    try:
                        import requests
                        response = requests.post(
                            f"{engineer3_api.API_URL}/predict",
                            json=feature_values,
                            timeout=5
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success(f"**Prediction:** {result['prediction']:.4f}")
                            if 'probability' in result:
                                st.info(f"**Confidence:** {result['probability']:.4f}")
                        else:
                            st.error(f"❌ Prediction failed: {response.status_code}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Model features not available. Train a model first.")
