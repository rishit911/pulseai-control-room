import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

def render():
    st.title("🧠 Model Explainability")
    
    # Add refresh button
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Always load the latest feature importance from trained model
    base_dir = Path(__file__).resolve().parents[3]
    importance_file = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "feature_importance.json"
    
    # Force reload by checking file modification time
    if importance_file.exists():
        with open(importance_file, 'r') as f:
            feature_importance = json.load(f)
        
        st.subheader("📊 Feature Importance")
        st.write("Understanding which features drive model predictions:")
        
        # Create DataFrame
        importance_df = pd.DataFrame([
            {'Feature': k, 'Importance': v}
            for k, v in feature_importance.items()
        ]).sort_values('Importance', ascending=False)
        
        # Visualization
        fig = px.bar(
            importance_df,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Feature Importance (Random Forest)',
            color='Importance',
            color_continuous_scale='Viridis',
            text='Importance'
        )
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(
            template='plotly_dark',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature descriptions
        st.subheader("📝 Feature Importance Details")
        
        for idx, row in importance_df.iterrows():
            feature_name = row['Feature']
            feature_importance_val = row['Importance']
            
            with st.expander(f"**{feature_name}** (Importance: {feature_importance_val:.3f})"):
                # Show relative importance
                pct = (feature_importance_val / importance_df['Importance'].sum()) * 100
                st.progress(min(1.0, feature_importance_val))
                st.caption(f"Contributes {pct:.1f}% to model decisions")
                st.write(f"Feature: `{feature_name}`")
        
        # Plain English Summary
        st.subheader("💡 Model Summary")
        
        top_feature = importance_df.iloc[0]['Feature']
        top_importance = importance_df.iloc[0]['Importance']
        
        # Load model metadata for accurate info
        metrics_file = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
        model_type = "Model"
        target = "target"
        
        if metrics_file.exists():
            with open(metrics_file, 'r') as f:
                metrics = json.load(f)
                model_type = metrics.get('model_name', 'Model')
                target = metrics.get('target', 'target')
        
        summary = f"""
        The **{model_type}** uses **{len(feature_importance)} features** to predict **{target}**.
        
        **Key Insights:**
        - **{top_feature}** is the most important feature (importance: {top_importance:.3f})
        - Feature importance shows which inputs have the most influence on predictions
        - Higher importance = greater impact on model decisions
        
        **How to interpret:**
        - Features are ranked by their contribution to prediction accuracy
        - The model considers all features but weighs them differently
        - This helps identify which data points are most critical
        """
        
        st.markdown(summary)
        
        # Model insights
        st.subheader("🔍 Model Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Features", len(feature_importance))
            st.metric("Top Feature", top_feature)
        
        with col2:
            st.metric("Model Type", "Random Forest")
            st.metric("Importance Range", f"{importance_df['Importance'].min():.3f} - {importance_df['Importance'].max():.3f}")
        
    else:
        st.warning("⚠️ Feature importance data not available. Train the model first.")
        st.info("💡 Run: `python -m MLOps_Engineer1.core.pipelines.run_training`")