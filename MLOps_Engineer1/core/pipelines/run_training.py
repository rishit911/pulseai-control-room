"""Run the full training pipeline."""
from MLOps_Engineer1.core.pipelines.training_pipeline import training_pipeline

if __name__ == "__main__":
    pipeline = training_pipeline()
    pipeline.run()
    print("✅ Training pipeline completed successfully!")
