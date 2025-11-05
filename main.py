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
