'''
from fastapi import FastAPI
from datetime import datetime
from config.settings import settings

# Initialize the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Core API service for serving ML models and system metadata.",
    version=settings.VERSION
)

@app.get("/")
def root():
    """
    Root endpoint to verify the API is running.
    """
    return {
        "message": "Welcome to the AI Reliability Dashboard API Service 👋",
        "status": "running",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    """
    Health-check endpoint to verify FastAPI service status.
    """
    return {
        "service_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "status": "healthy ✅",
        "timestamp": datetime.now().isoformat()
    }
'''

from fastapi import FastAPI
from datetime import datetime
from config.settings import settings
from schemas.predict_schema import PredictRequest, PredictResponse
from utils.load_model import load_or_create_dummy_model, predict_with_dummy_model

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Core API service for AI Reliability Dashboard",
    version=settings.VERSION
)

# load dummy model at startup
model = load_or_create_dummy_model()

@app.get("/")
def root():
    return {"message": "Welcome to the AI Reliability Dashboard API 👋"}

@app.get("/health")
def health_check():
    return {
        "service_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "status": "healthy ✅",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Dummy prediction endpoint (Week 3)
    Accepts health parameters and returns a fake risk score.
    """
    features = [
        request.age,
        request.systolic_bp,
        request.diastolic_bp,
        request.cholesterol,
        request.heart_rate
    ]
    prediction, confidence = predict_with_dummy_model(model, features)
    return PredictResponse(
        prediction=round(prediction, 3),
        model_version=settings.VERSION,
        confidence=confidence
    )
