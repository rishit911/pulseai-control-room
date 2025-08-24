"""Engineer-1 | Pipeline: ingestion -> validation (ZenML)."""
from zenml.pipelines import pipeline
from MLOps_Engineer1.core.pipelines.steps.ingest import ingest_data
from MLOps_Engineer1.core.pipelines.steps.validate import validate_data

@pipeline
def ingestion_validation_pipeline():
    df = ingest_data()
    _ = validate_data(df)