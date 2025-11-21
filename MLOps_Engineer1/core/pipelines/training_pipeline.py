"""Engineer-1 | Full training pipeline: ingest -> validate -> train."""
from zenml.pipelines import pipeline
from MLOps_Engineer1.core.pipelines.steps.ingest import ingest_data
from MLOps_Engineer1.core.pipelines.steps.validate import validate_data
from MLOps_Engineer1.core.pipelines.steps.train import train_model

@pipeline
def training_pipeline():
    """Complete ML pipeline with validation and training."""
    df = ingest_data()
    validation_result = validate_data(df)
    model_path, metrics = train_model(df)
