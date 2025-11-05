import os
import joblib
import numpy as np
from sklearn.dummy import DummyRegressor

MODEL_PATH = os.path.join("model", "dummy_model.pkl")

def load_or_create_dummy_model():
    # If model file exists, load it
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    # Otherwise create a simple DummyRegressor model
    X = np.random.rand(100, 5)
    y = np.random.rand(100)
    dummy_model = DummyRegressor(strategy="mean")
    dummy_model.fit(X, y)
    os.makedirs("model", exist_ok=True)
    joblib.dump(dummy_model, MODEL_PATH)
    return dummy_model

def predict_with_dummy_model(model, features):
    # For demonstration, predict a single random value
    prediction = float(model.predict([features])[0])
    confidence = 0.85  # placeholder
    return prediction, confidence
