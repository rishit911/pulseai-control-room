from pydantic import BaseModel

class PredictRequest(BaseModel):
    age: int
    systolic_bp: float
    diastolic_bp: float
    cholesterol: float
    heart_rate: float

class PredictResponse(BaseModel):
    prediction: float
    model_version: str
    confidence: float
