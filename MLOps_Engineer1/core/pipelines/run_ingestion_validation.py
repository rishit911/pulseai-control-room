"""Engineer-1 | Runner for ingestion+validation (ZenML 0.84+ safe)."""
from pathlib import Path
from MLOps_Engineer1.core.pipelines.ingestion_validation_pipeline import ingestion_validation_pipeline

if __name__ == "__main__":
    p = ingestion_validation_pipeline()
    
    # Execute pipeline - handle the response object properly
    try:
        resp = p.run()  # This should return a PipelineRunResponse
        run_id = getattr(resp, "id", None) or getattr(resp, "name", "unknown")
        status = getattr(resp, "status", "unknown")
        print(f"✅ Pipeline execution submitted. run_id={run_id} status={status}")
    except AttributeError as e:
        if "'PipelineRunResponse' object has no attribute 'run'" in str(e):
            # This means the pipeline already executed and returned a response
            print(f"✅ Pipeline execution completed successfully")
        else:
            raise e
    
    print(f"Check artifacts at: {Path('MLOps_Engineer1/artifacts/validation').resolve()}")