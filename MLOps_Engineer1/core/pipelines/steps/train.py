"""Engineer-1 | Training step with MLflow logging."""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from zenml.steps import step, Output
import mlflow
import mlflow.sklearn
from pathlib import Path
import json
from datetime import datetime

@step(enable_cache=False)
def train_model(df: pd.DataFrame) -> Output(model_path=str, metrics=dict):
    """Train a Random Forest model and log to MLflow."""
    
    # Prepare features
    X = df[['age', 'education_num', 'hours_per_week']].copy()
    X['workclass_private'] = (df['workclass'] == 'Private').astype(int)
    y = (df['income'] == '>50K').astype(int)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'recall': float(recall_score(y_test, y_pred, zero_division=0)),
        'f1_score': float(f1_score(y_test, y_pred, zero_division=0)),
        'train_size': len(X_train),
        'test_size': len(X_test),
        'timestamp': datetime.now().isoformat()
    }
    
    # MLflow logging
    with mlflow.start_run(run_name="income_classifier"):
        mlflow.log_params({
            'n_estimators': 100,
            'max_depth': 5,
            'test_size': 0.2
        })
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, "model")
    
    # Save model locally
    model_dir = Path(__file__).resolve().parents[3] / "artifacts" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = str(model_dir / "income_classifier.pkl")
    import joblib
    joblib.dump(model, model_path)
    
    # Save metrics
    metrics_path = model_dir / "metrics.json"
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    # Save feature importance
    feature_names = ['age', 'education_num', 'hours_per_week', 'workclass_private']
    importance = {
        name: float(imp) 
        for name, imp in zip(feature_names, model.feature_importances_)
    }
    importance_path = model_dir / "feature_importance.json"
    with open(importance_path, 'w') as f:
        json.dump(importance, f, indent=2)
    
    # Sync data to dashboard after training
    try:
        import sys
        base_dir = Path(__file__).resolve().parents[3]
        sys.path.insert(0, str(base_dir))
        from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer
        
        syncer = DataSynchronizer()
        syncer.sync_all_data()
        print("✅ Dashboard data synced successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not sync dashboard data: {e}")
    
    return model_path, metrics
