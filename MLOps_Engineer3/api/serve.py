"""Engineer-3 | FastAPI model serving endpoint."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
from typing import List, Dict

app = FastAPI(title="Income Prediction API", version="1.0.0")

# Model path
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "MLOps_Engineer1" / "artifacts" / "models" / "income_classifier.pkl"
METRICS_PATH = BASE_DIR / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"

# Load model
model = None
model_metrics = {}

def load_model():
    """Load the trained model."""
    global model, model_metrics
    try:
        if MODEL_PATH.exists():
            import warnings
            # Suppress sklearn version warnings
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                try:
                    model = joblib.load(MODEL_PATH)
                    print(f"✅ Model loaded from {MODEL_PATH}")
                except Exception as load_error:
                    print(f"⚠️  Model loading failed: {load_error}")
                    print(f"💡 This may be due to scikit-learn version mismatch.")
                    print(f"💡 Please retrain the model to fix this issue.")
                    model = None
            
            if METRICS_PATH.exists():
                with open(METRICS_PATH, 'r') as f:
                    model_metrics = json.load(f)
        else:
            print(f"⚠️  Model not found at {MODEL_PATH}")
            print(f"💡 Train a model first using the Model Training tab")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None

# Load model on startup
load_model()

# Dynamic prediction - no fixed schema needed

@app.get("/")
def root():
    """API root endpoint."""
    return {
        "service": "Income Prediction API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "model_info": "/model/info",
            "metrics": "/model/metrics"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint."""
    status_info = {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }
    
    if model is None and MODEL_PATH.exists():
        status_info["warning"] = "Model file exists but failed to load. May need retraining due to version mismatch."
    elif model is None:
        status_info["warning"] = "No model found. Train a model first."
    
    return status_info

@app.post("/predict")
def predict(data: dict):
    """Make a single prediction with dynamic features."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Load model metadata to get expected features
        if METRICS_PATH.exists():
            with open(METRICS_PATH, 'r') as f:
                metrics = json.load(f)
                expected_features = metrics.get('features', [])
        else:
            # Fallback: try to get features from model
            expected_features = getattr(model, 'feature_names_in_', None)
            if expected_features is None:
                raise HTTPException(status_code=500, detail="Cannot determine model features")
        
        # Prepare features from request data
        features = pd.DataFrame([{feat: data.get(feat, 0) for feat in expected_features}])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Try to get probability if available (classification models)
        try:
            probability = float(model.predict_proba(features)[0][1])
        except:
            probability = float(prediction)  # For regression
        
        return {
            "prediction": float(prediction),
            "probability": probability,
            "timestamp": datetime.now().isoformat(),
            "features_used": expected_features
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/batch")
def batch_predict(data: dict):
    """Make batch predictions with dynamic features."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Load model metadata
        if METRICS_PATH.exists():
            with open(METRICS_PATH, 'r') as f:
                metrics = json.load(f)
                expected_features = metrics.get('features', [])
        else:
            expected_features = getattr(model, 'feature_names_in_', None)
            if expected_features is None:
                raise HTTPException(status_code=500, detail="Cannot determine model features")
        
        # Get instances from request
        instances = data.get('instances', [])
        if not instances:
            raise HTTPException(status_code=400, detail="No instances provided")
        
        # Prepare features
        features = pd.DataFrame([{feat: inst.get(feat, 0) for feat in expected_features} for inst in instances])
        
        # Make predictions
        predictions = model.predict(features)
        
        # Try to get probabilities if available
        try:
            probabilities = model.predict_proba(features)[:, 1]
        except:
            probabilities = predictions  # For regression
        
        results = []
        for pred, prob in zip(predictions, probabilities):
            results.append({
                "prediction": float(pred),
                "probability": float(prob)
            })
        
        return {
            "predictions": results,
            "count": len(results),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

@app.get("/model/info")
def model_info():
    """Get model information."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(model).__name__,
        "model_path": str(MODEL_PATH),
        "features": ['age', 'education_num', 'hours_per_week', 'workclass_private'],
        "target": "income",
        "version": "1.0.0",
        "loaded_at": datetime.now().isoformat()
    }

@app.get("/model/metrics")
def model_metrics_endpoint():
    """Get model performance metrics."""
    # Check if model file has been updated
    if MODEL_PATH.exists():
        current_mtime = MODEL_PATH.stat().st_mtime
        if not hasattr(model_metrics_endpoint, 'last_check') or current_mtime > model_metrics_endpoint.last_check:
            load_model()
            model_metrics_endpoint.last_check = current_mtime
    
    if not model_metrics:
        raise HTTPException(status_code=404, detail="Metrics not available")
    
    return model_metrics

@app.post("/model/reload")
def reload_model():
    """Reload the model from disk."""
    load_model()
    return {
        "status": "success" if model is not None else "failed",
        "message": "Model reloaded",
        "model_loaded": model is not None,
        "metrics": model_metrics if model_metrics else {},
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model/auto-reload")
def auto_reload_check():
    """Check if model needs reloading based on file modification time."""
    global model
    
    if MODEL_PATH.exists():
        current_mtime = MODEL_PATH.stat().st_mtime
        
        # Store last load time in a simple way
        if not hasattr(auto_reload_check, 'last_mtime'):
            auto_reload_check.last_mtime = current_mtime
            return {"needs_reload": False, "current_model": type(model).__name__ if model else None}
        
        if current_mtime > auto_reload_check.last_mtime:
            load_model()
            auto_reload_check.last_mtime = current_mtime
            return {
                "needs_reload": True,
                "reloaded": True,
                "current_model": type(model).__name__ if model else None,
                "timestamp": datetime.now().isoformat()
            }
        
        return {"needs_reload": False, "current_model": type(model).__name__ if model else None}
    
    return {"needs_reload": False, "model_exists": False}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Income Prediction API...")
    print(f"📊 Model path: {MODEL_PATH}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
