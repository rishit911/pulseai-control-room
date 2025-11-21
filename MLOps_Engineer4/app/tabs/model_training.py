"""
Model Training Tab - Allow users to upload data and train custom models
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import joblib
import io

# ML Models - Classification
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

# ML Models - Regression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

from sklearn.model_selection import train_test_split

# Metrics - Classification
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# Metrics - Regression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

def save_model_artifacts(model, metrics, feature_importance, model_name, features, target):
    """Save model and metrics with versioning."""
    base_dir = Path(__file__).resolve().parents[3]
    
    # Import versioning system
    import sys
    sys.path.insert(0, str(base_dir))
    from MLOps_Engineer1.core.model_versioning import ModelVersionManager
    
    # Initialize version manager
    version_manager = ModelVersionManager()
    
    # Save with versioning
    version = version_manager.save_model_version(
        model=model,
        metrics=metrics,
        feature_importance=feature_importance,
        model_name=model_name,
        features=features,
        target=target
    )
    
    # Return version info
    model_dir = base_dir / "MLOps_Engineer1" / "artifacts" / "models"
    return str(model_dir / "income_classifier.pkl"), version

def get_model_instance(model_name, params, is_classification=True):
    """Get model instance based on selection and problem type."""
    if is_classification:
        # Classification models
        if model_name == 'Random Forest':
            return RandomForestClassifier(**params, random_state=42)
        elif model_name == 'Gradient Boosting':
            return GradientBoostingClassifier(**params, random_state=42)
        elif model_name == 'Logistic Regression':
            return LogisticRegression(**params, random_state=42, max_iter=1000)
        elif model_name == 'Support Vector Machine':
            return SVC(**params, random_state=42, probability=True)
        elif model_name == 'Decision Tree':
            return DecisionTreeClassifier(**params, random_state=42)
        elif model_name == 'K-Nearest Neighbors':
            return KNeighborsClassifier(**params)
        elif model_name == 'Naive Bayes':
            return GaussianNB()
    else:
        # Regression models
        if model_name == 'Random Forest':
            return RandomForestRegressor(**params, random_state=42)
        elif model_name == 'Gradient Boosting':
            return GradientBoostingRegressor(**params, random_state=42)
        elif model_name == 'Linear Regression':
            return LinearRegression(**params)
        elif model_name == 'Ridge Regression':
            return Ridge(**params, random_state=42)
        elif model_name == 'Lasso Regression':
            return Lasso(**params, random_state=42)
        elif model_name == 'ElasticNet':
            return ElasticNet(**params, random_state=42)
        elif model_name == 'Support Vector Machine':
            return SVR(**params)
        elif model_name == 'Decision Tree':
            return DecisionTreeRegressor(**params, random_state=42)
        elif model_name == 'K-Nearest Neighbors':
            return KNeighborsRegressor(**params)
    
    return None

def render():
    st.title("🤖 Model Training Studio")
    st.write("Upload your data, configure your model, and train in real-time!")
    
    # Initialize session state
    if 'training_data' not in st.session_state:
        st.session_state.training_data = None
    if 'trained_model' not in st.session_state:
        st.session_state.trained_model = None
    
    # Step 1: Data Upload
    st.header("📊 Step 1: Upload Training Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file with your training data"
        )
    
    with col2:
        st.info("💡 **Data Requirements:**\n- CSV format\n- Include target column\n- No missing values in target")
    
    # Alternative: Load sample datasets
    st.subheader("Or use a sample dataset:")
    sample_choice = st.selectbox(
        "Select sample dataset",
        ["None", 
         "Iris (Flower Classification)", 
         "Customer Churn (Classification)", 
         "House Prices (Regression)",
         "Current adult_small.csv"],
        help="Quick start with pre-loaded datasets"
    )
    
    if sample_choice != "None" and st.button("Load Sample Dataset"):
        try:
            base_dir = Path(__file__).resolve().parents[3]
            
            if sample_choice == "Iris (Flower Classification)":
                sample_path = base_dir / "sample_datasets" / "iris_sample.csv"
            elif sample_choice == "Customer Churn (Classification)":
                sample_path = base_dir / "sample_datasets" / "customer_churn.csv"
            elif sample_choice == "House Prices (Regression)":
                sample_path = base_dir / "sample_datasets" / "house_prices.csv"
            else:  # adult_small.csv
                sample_path = base_dir / "MLOps_Engineer1" / "data" / "adult_small.csv"
            
            if sample_path.exists():
                df = pd.read_csv(sample_path)
                st.session_state.training_data = df
                st.success(f"✅ Sample data loaded! Shape: {df.shape}")
                st.rerun()
            else:
                st.error(f"❌ Sample file not found: {sample_path}")
        except Exception as e:
            st.error(f"❌ Error loading sample: {e}")
    
    if uploaded_file is not None:
        try:
            # Reset file pointer to beginning
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            
            # Validate data
            if df.empty:
                st.error("❌ The uploaded file is empty")
                return
            
            if df.shape[0] < 10:
                st.warning("⚠️ Dataset is very small (< 10 rows). Results may not be reliable.")
            
            st.session_state.training_data = df
            
            st.success(f"✅ Data loaded successfully! Shape: {df.shape}")
            
            # Show data preview
            with st.expander("📋 Data Preview", expanded=True):
                st.dataframe(df.head(10), use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rows", df.shape[0])
                with col2:
                    st.metric("Columns", df.shape[1])
                with col3:
                    st.metric("Missing Values", df.isnull().sum().sum())
            
            # Data info
            with st.expander("ℹ️ Data Information"):
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())
        
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.info("💡 Please ensure your file is a valid CSV with proper headers")
            return
    
    # Step 2: Feature Selection
    if st.session_state.training_data is not None:
        df = st.session_state.training_data
        
        st.header("🎯 Step 2: Select Features & Target")
        
        col1, col2 = st.columns(2)
        
        with col1:
            target_column = st.selectbox(
                "Select Target Column",
                options=df.columns.tolist(),
                help="The column you want to predict"
            )
            
            # Show target info and detect problem type
            if target_column:
                target_series = df[target_column]
                unique_count = target_series.nunique()
                
                # Store problem type in session state
                if target_series.dtype == 'object':
                    st.session_state.problem_type = 'classification'
                    st.success(f"✅ Classification - Categorical target ({unique_count} classes)")
                elif unique_count <= 20:
                    st.session_state.problem_type = 'classification'
                    st.success(f"✅ Classification - Discrete target ({unique_count} classes)")
                else:
                    st.session_state.problem_type = 'regression'
                    st.info(f"📊 Regression - Continuous target ({unique_count} unique values)")
        
        with col2:
            # Auto-detect numeric columns for features
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # Remove target from options
            available_features = [col for col in df.columns if col != target_column]
            
            feature_columns = st.multiselect(
                "Select Feature Columns",
                options=available_features,
                default=[col for col in numeric_cols if col != target_column][:5],
                help="Columns to use for prediction"
            )
        
        if len(feature_columns) == 0:
            st.warning("⚠️ Please select at least one feature column")
            return
        
        # Show feature statistics
        with st.expander("📊 Feature Statistics"):
            st.dataframe(df[feature_columns].describe(), use_container_width=True)
        
        # Step 3: Model Selection
        st.header("🔧 Step 3: Configure Model")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Get problem type
            problem_type = st.session_state.get('problem_type', 'classification')
            
            # Show different models based on problem type
            if problem_type == 'classification':
                model_options = [
                    'Random Forest',
                    'Gradient Boosting',
                    'Logistic Regression',
                    'Support Vector Machine',
                    'Decision Tree',
                    'K-Nearest Neighbors',
                    'Naive Bayes'
                ]
                help_text = "Choose the classification algorithm"
            else:  # regression
                model_options = [
                    'Random Forest',
                    'Gradient Boosting',
                    'Linear Regression',
                    'Ridge Regression',
                    'Lasso Regression',
                    'ElasticNet',
                    'Support Vector Machine',
                    'Decision Tree',
                    'K-Nearest Neighbors'
                ]
                help_text = "Choose the regression algorithm"
            
            model_name = st.selectbox(
                "Select Model Type",
                options=model_options,
                help=help_text
            )
        
        with col2:
            test_size = st.slider(
                "Test Set Size (%)",
                min_value=10,
                max_value=50,
                value=20,
                step=5,
                help="Percentage of data to use for testing"
            ) / 100
        
        # Model-specific parameters
        st.subheader("⚙️ Model Parameters")
        
        params = {}
        
        if model_name == 'Random Forest':
            col1, col2, col3 = st.columns(3)
            with col1:
                params['n_estimators'] = st.number_input("Number of Trees", 10, 500, 100, 10)
            with col2:
                params['max_depth'] = st.number_input("Max Depth", 1, 50, 10, 1)
            with col3:
                params['min_samples_split'] = st.number_input("Min Samples Split", 2, 20, 2, 1)
        
        elif model_name == 'Gradient Boosting':
            col1, col2, col3 = st.columns(3)
            with col1:
                params['n_estimators'] = st.number_input("Number of Estimators", 10, 500, 100, 10)
            with col2:
                params['learning_rate'] = st.number_input("Learning Rate", 0.01, 1.0, 0.1, 0.01)
            with col3:
                params['max_depth'] = st.number_input("Max Depth", 1, 20, 3, 1)
        
        elif model_name == 'Logistic Regression':
            col1, col2 = st.columns(2)
            with col1:
                params['C'] = st.number_input("Regularization (C)", 0.01, 10.0, 1.0, 0.1)
            with col2:
                penalty = st.selectbox("Penalty", ['l2', 'none'])
                params['penalty'] = penalty
                # Set appropriate solver based on penalty
                if penalty == 'l2':
                    params['solver'] = 'lbfgs'
                elif penalty == 'none':
                    params['solver'] = 'lbfgs'
        
        elif model_name == 'Support Vector Machine':
            col1, col2, col3 = st.columns(3)
            with col1:
                params['C'] = st.number_input("C Parameter", 0.1, 10.0, 1.0, 0.1)
            with col2:
                params['kernel'] = st.selectbox("Kernel", ['rbf', 'linear', 'poly', 'sigmoid'])
            with col3:
                params['gamma'] = st.selectbox("Gamma", ['scale', 'auto'])
        
        elif model_name == 'Decision Tree':
            col1, col2 = st.columns(2)
            with col1:
                params['max_depth'] = st.number_input("Max Depth", 1, 50, 10, 1)
            with col2:
                params['min_samples_split'] = st.number_input("Min Samples Split", 2, 20, 2, 1)
        
        elif model_name == 'K-Nearest Neighbors':
            col1, col2 = st.columns(2)
            with col1:
                params['n_neighbors'] = st.number_input("Number of Neighbors", 1, 50, 5, 1)
            with col2:
                params['weights'] = st.selectbox("Weights", ['uniform', 'distance'])
        
        elif model_name == 'Naive Bayes':
            st.info("ℹ️ Naive Bayes has no hyperparameters to tune. It will use default settings.")
            params = {}  # No parameters needed
        
        # Regression-specific models
        elif model_name == 'Linear Regression':
            st.info("ℹ️ Linear Regression has no hyperparameters to tune. It will use default settings.")
            params = {}
        
        elif model_name == 'Ridge Regression':
            col1, col2 = st.columns(2)
            with col1:
                params['alpha'] = st.number_input("Alpha (Regularization)", 0.01, 10.0, 1.0, 0.1,
                                                 help="Higher values = more regularization")
            with col2:
                params['solver'] = st.selectbox("Solver", ['auto', 'svd', 'cholesky', 'lsqr'])
        
        elif model_name == 'Lasso Regression':
            col1, col2 = st.columns(2)
            with col1:
                params['alpha'] = st.number_input("Alpha (Regularization)", 0.01, 10.0, 1.0, 0.1,
                                                 help="Higher values = more regularization")
            with col2:
                params['max_iter'] = st.number_input("Max Iterations", 100, 10000, 1000, 100)
        
        elif model_name == 'ElasticNet':
            col1, col2, col3 = st.columns(3)
            with col1:
                params['alpha'] = st.number_input("Alpha", 0.01, 10.0, 1.0, 0.1)
            with col2:
                params['l1_ratio'] = st.number_input("L1 Ratio", 0.0, 1.0, 0.5, 0.1,
                                                    help="0=Ridge, 1=Lasso")
            with col3:
                params['max_iter'] = st.number_input("Max Iterations", 100, 10000, 1000, 100)
        
        # Step 4: Train Model
        st.header("🚀 Step 4: Train Model")
        
        if st.button("🎯 Train Model", type="primary", use_container_width=True):
            with st.spinner(f"Training {model_name}..."):
                try:
                    # Prepare data
                    X = df[feature_columns].copy()
                    
                    # Handle categorical features
                    for col in X.columns:
                        if X[col].dtype == 'object':
                            X[col] = pd.Categorical(X[col]).codes
                    
                    # Prepare target - detect problem type
                    y = df[target_column].copy()
                    
                    # Determine if classification or regression
                    is_classification = False
                    if y.dtype == 'object':
                        # Categorical target - classification
                        is_classification = True
                        y = pd.Categorical(y).codes
                    elif y.nunique() <= 20:
                        # Numeric but few unique values - likely classification
                        is_classification = True
                        y = y.astype(int)
                    else:
                        # Many unique numeric values - regression
                        is_classification = False
                        # Keep y as is for regression
                    
                    # Split data
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=test_size, random_state=42
                    )
                    
                    # Train model
                    model = get_model_instance(model_name, params, is_classification)
                    model.fit(X_train, y_train)
                    
                    # Predictions
                    y_pred = model.predict(X_test)
                    
                    # Calculate metrics based on problem type
                    if is_classification:
                        metrics = {
                            'problem_type': 'classification',
                            'accuracy': float(accuracy_score(y_test, y_pred)),
                            'precision': float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
                            'recall': float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
                            'f1_score': float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
                            'train_size': len(X_train),
                            'test_size': len(X_test),
                            'timestamp': datetime.now().isoformat(),
                            'model_name': model_name,
                            'features': feature_columns,
                            'target': target_column
                        }
                    else:  # regression
                        mse = mean_squared_error(y_test, y_pred)
                        rmse = np.sqrt(mse)
                        mae = mean_absolute_error(y_test, y_pred)
                        r2 = r2_score(y_test, y_pred)
                        
                        # Calculate MAPE safely
                        try:
                            mape = mean_absolute_percentage_error(y_test, y_pred)
                        except:
                            mape = 0.0
                        
                        metrics = {
                            'problem_type': 'regression',
                            'rmse': float(rmse),
                            'mae': float(mae),
                            'r2_score': float(r2),
                            'mse': float(mse),
                            'mape': float(mape),
                            'train_size': len(X_train),
                            'test_size': len(X_test),
                            'timestamp': datetime.now().isoformat(),
                            'model_name': model_name,
                            'features': feature_columns,
                            'target': target_column
                        }
                    
                    # Feature importance
                    feature_importance = {}
                    if hasattr(model, 'feature_importances_'):
                        for feat, imp in zip(feature_columns, model.feature_importances_):
                            feature_importance[feat] = float(imp)
                    elif hasattr(model, 'coef_'):
                        for feat, imp in zip(feature_columns, abs(model.coef_[0])):
                            feature_importance[feat] = float(imp)
                    else:
                        # Default equal importance
                        for feat in feature_columns:
                            feature_importance[feat] = 1.0 / len(feature_columns)
                    
                    # Save artifacts with versioning
                    model_path, version = save_model_artifacts(
                        model, metrics, feature_importance, model_name, 
                        feature_columns, target_column
                    )
                    
                    # Sync all dashboard data with latest training info
                    try:
                        import sys
                        base_dir = Path(__file__).resolve().parents[3]
                        sys.path.insert(0, str(base_dir))
                        from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer
                        
                        syncer = DataSynchronizer()
                        result = syncer.sync_all_data()
                        if result.get('status') == 'success':
                            st.success("✅ All dashboard data synced!")
                        else:
                            st.warning(f"⚠️ Sync warning: {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.warning(f"⚠️ Could not sync dashboard data: {e}")
                    
                    # Auto-update monitoring
                    monitoring_updated = False
                    try:
                        import subprocess
                        import sys
                        base_dir = Path(__file__).resolve().parents[3]
                        script_path = base_dir / "scripts" / "auto_update_monitoring.py"
                        
                        if script_path.exists():
                            result = subprocess.run(
                                [sys.executable, str(script_path)], 
                                capture_output=True, 
                                text=True,
                                timeout=10
                            )
                            if result.returncode == 0:
                                monitoring_updated = True
                                st.success("✅ Monitoring data updated!")
                            else:
                                st.info("ℹ️ Monitoring update skipped")
                        else:
                            st.info("ℹ️ Monitoring will be available after first use")
                    except Exception as e:
                        # Monitoring update is optional
                        st.info("ℹ️ Monitoring data will be generated on next refresh")
                    
                    st.session_state.trained_model = {
                        'model': model,
                        'metrics': metrics,
                        'feature_importance': feature_importance,
                        'X_test': X_test,
                        'y_test': y_test,
                        'y_pred': y_pred
                    }
                    
                    st.success(f"✅ Model trained successfully!")
                    st.balloons()
                    
                    # Display results
                    st.header("📊 Training Results")
                    
                    if is_classification:
                        # Classification metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Accuracy", f"{metrics['accuracy']:.2%}")
                        with col2:
                            st.metric("Precision", f"{metrics['precision']:.2%}")
                        with col3:
                            st.metric("Recall", f"{metrics['recall']:.2%}")
                        with col4:
                            st.metric("F1 Score", f"{metrics['f1_score']:.2%}")
                        
                        # Confusion Matrix
                        st.subheader("🎯 Confusion Matrix")
                        cm = confusion_matrix(y_test, y_pred)
                        st.dataframe(pd.DataFrame(cm), use_container_width=True)
                        
                        # Classification Report
                        st.subheader("📋 Classification Report")
                        report = classification_report(y_test, y_pred, output_dict=True)
                        st.json(report)
                    
                    else:
                        # Regression metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("R² Score", f"{metrics['r2_score']:.4f}",
                                    help="1.0 = perfect, 0.0 = baseline")
                        with col2:
                            st.metric("RMSE", f"{metrics['rmse']:.4f}",
                                    help="Root Mean Squared Error")
                        with col3:
                            st.metric("MAE", f"{metrics['mae']:.4f}",
                                    help="Mean Absolute Error")
                        with col4:
                            st.metric("MAPE", f"{metrics['mape']:.2%}" if metrics['mape'] > 0 else "N/A",
                                    help="Mean Absolute Percentage Error")
                        
                        # Prediction vs Actual Plot
                        st.subheader("📈 Predictions vs Actual Values")
                        import plotly.graph_objects as go
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=y_test,
                            y=y_pred,
                            mode='markers',
                            name='Predictions',
                            marker=dict(size=8, opacity=0.6)
                        ))
                        
                        # Add perfect prediction line
                        min_val = min(y_test.min(), y_pred.min())
                        max_val = max(y_test.max(), y_pred.max())
                        fig.add_trace(go.Scatter(
                            x=[min_val, max_val],
                            y=[min_val, max_val],
                            mode='lines',
                            name='Perfect Prediction',
                            line=dict(color='red', dash='dash')
                        ))
                        
                        fig.update_layout(
                            xaxis_title='Actual Values',
                            yaxis_title='Predicted Values',
                            title='Prediction Quality',
                            template='plotly_dark'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Residuals Plot
                        st.subheader("📉 Residuals Distribution")
                        residuals = y_test - y_pred
                        
                        import plotly.express as px
                        fig2 = px.histogram(
                            x=residuals,
                            nbins=30,
                            title='Residuals (Actual - Predicted)',
                            labels={'x': 'Residual', 'y': 'Count'}
                        )
                        fig2.update_layout(template='plotly_dark')
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    # Feature Importance
                    if feature_importance:
                        st.subheader("🎯 Feature Importance")
                        import plotly.express as px
                        imp_df = pd.DataFrame([
                            {'Feature': k, 'Importance': v}
                            for k, v in sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
                        ])
                        fig = px.bar(imp_df, x='Importance', y='Feature', orientation='h',
                                   title='Feature Importance')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.success(f"📦 Model Version: **{version}**")
                    st.info(f"💾 Model saved to: {model_path}")
                    
                    # Show update instructions
                    st.success("✅ Model deployed successfully!")
                    st.info("🔄 **To see updates in other tabs:**")
                    st.write("1. **Model Status & Explainability**: Click 🔄 Refresh or press R")
                    st.write("2. **Drift & Fairness**: " + ("Updated automatically!" if monitoring_updated else "Click 🔄 Refresh"))
                    st.write("3. **Or press R** in your browser to reload everything")
                    
                    # Show version info
                    with st.expander("📋 Version Information"):
                        st.write(f"**Version:** {version}")
                        st.write(f"**Model Type:** {model_name}")
                        st.write(f"**Problem Type:** {metrics.get('problem_type', 'classification')}")
                        st.write(f"**Trained:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        st.write(f"**Features:** {', '.join(feature_columns)}")
                        st.write(f"**Target:** {target_column}")
                    
                except Exception as e:
                    st.error(f"❌ Training failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
    
    else:
        st.info("👆 Please upload a CSV file to get started")
