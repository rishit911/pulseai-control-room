"""
Engineer 3 – Model Serving API Integration
Connect to FastAPI serving endpoint.
"""
from typing import Dict, List
import os
import requests
from datetime import datetime

API_URL = os.getenv("MODEL_API_URL", "http://localhost:8000")

def get_api_status() -> Dict:
    """Check if the model API is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "unhealthy", "error": f"Status code: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"status": "offline", "error": "Cannot connect to API"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_model_info() -> Dict:
    """Get model information from API."""
    try:
        response = requests.get(f"{API_URL}/model/info", timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_model_metrics() -> Dict:
    """Get model performance metrics from API."""
    try:
        response = requests.get(f"{API_URL}/model/metrics", timeout=2)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Metrics not available"}
    except Exception as e:
        return {"error": str(e)}

def make_prediction(age: int, workclass: str, education_num: int, hours_per_week: int) -> Dict:
    """Make a single prediction via API."""
    try:
        payload = {
            "age": age,
            "workclass": workclass,
            "education_num": education_num,
            "hours_per_week": hours_per_week
        }
        response = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Prediction failed: HTTP {response.status_code}. Is the API running?"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Please start: python MLOps_Engineer3/api/serve.py"}
    except Exception as e:
        return {"error": str(e)}

def make_batch_prediction(instances: List[Dict]) -> Dict:
    """Make batch predictions via API."""
    try:
        payload = {"instances": instances}
        response = requests.post(f"{API_URL}/predict/batch", json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Batch prediction failed: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
