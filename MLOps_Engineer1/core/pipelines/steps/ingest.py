"""Engineer-1 | Ingestion Step

Reads a small CSV into a pandas DataFrame (with a tiny synthesized fallback).
"""
from zenml.steps import step
import pandas as pd
from pathlib import Path

@step
def ingest_data() -> pd.DataFrame:
    base_dir = Path(__file__).resolve().parents[3]  # points to .../MLOps_Engineer1
    csv_path = base_dir / "data" / "adult_small.csv"
    
    if not csv_path.exists():
        df = pd.DataFrame({
            "age": [25, 45, 39, 31, 52],
            "workclass": ["Private", "Self-emp", "Private", "Private", "Gov"],
            "education_num": [13, 10, 14, 12, 9],
            "hours_per_week": [40, 60, 45, 38, 50],
            "income": [">50K", "<=50K", ">50K", "<=50K", ">50K"]
        })
        return df
    
    return pd.read_csv(csv_path)