import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "AI Reliability Dashboard API"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    VERSION: str = "1.0.0"

settings = Settings()
