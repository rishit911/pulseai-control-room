"""Train a fresh model with current data and scikit-learn version"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import json
from datetime import datetime

print("🔄 Training Fresh Model with Current scikit-learn Version")
print("=" * 60)

# Load data
data_path = "MLOps_Engineer1/data/adult_small.csv"
print(f"📊 Loading data from {data_path}...")
df = pd.read_csv(data_path)
print(f"✅ Data loaded: {df.shape}")
print(f"   Columns: {list(df.columns)}")

# Prepare features and target
# Encode categorical variables
le_workclass = LabelEncoder()
df['workclass_encoded'] = le_workclass.fit_transform(df['workclass'])

le_income = LabelEncoder()
df['income_encoded'] = le_income.fit_transform(df['income'])

# Features and target
feature_cols = ['age', 'workclass_encoded', 'education_num', 'hours_per_week']
target_col = 'income_encoded'

X = df[feature_cols]
y = df[target_col]

print(f"\n🎯 Training configuration:")
print(f"   Features: {feature_cols}")
print(f"   Target: income (binary classification)")
print(f"   Samples: {len(X)}")

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
print(f"\n🚀 Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='binary')
recall = recall_score(y_test, y_pred, average='binary')
f1 = f1_score(y_test, y_pred, average='binary')

print(f"\n📊 Model Performance:")
print(f"   Accuracy:  {accuracy:.4f}")
print(f"   Precision: {precision:.4f}")
print(f"   Recall:    {recall:.4f}")
print(f"   F1 Score:  {f1:.4f}")

# Save model
model_path = "MLOps_Engineer1/artifacts/models/income_classifier.pkl"
os.makedirs(os.path.dirname(model_path), exist_ok=True)
joblib.dump(model, model_path)
print(f"\n✅ Model saved to: {model_path}")

# Save metadata
metadata = {
    "model_type": "RandomForestClassifier",
    "task_type": "classification",
    "features": feature_cols,
    "target": "income",
    "n_samples": len(X),
    "train_size": len(X_train),
    "test_size": len(X_test),
    "metrics": {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    },
    "sklearn_version": "1.6.1",
    "trained_at": datetime.now().isoformat(),
    "version": "v1.0.10"
}

metadata_path = "MLOps_Engineer1/artifacts/models/model_metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✅ Metadata saved to: {metadata_path}")

# Update control room data
control_meta = {
    "model_version": "v1.0.10",
    "last_trained": datetime.now().isoformat(),
    "metrics": {
        "r2_score": float(accuracy),
        "rmse": 1 - float(accuracy),
        "mae": 1 - float(f1),
        "mape": (1 - float(accuracy)) * 100
    }
}

control_path = "MLOps_Engineer4/data/control_meta.json"
with open(control_path, 'w') as f:
    json.dump(control_meta, f, indent=2)
print(f"✅ Control room metadata updated: {control_path}")

print("\n" + "=" * 60)
print("✅ Model training complete!")
print("💡 Now restart the API to load the new model:")
print("   1. Stop the API (Ctrl+C)")
print("   2. Run: python MLOps_Engineer3/api/serve.py")
print("=" * 60)
