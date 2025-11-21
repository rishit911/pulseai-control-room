"""
Check what model is currently saved in artifacts
"""
from pathlib import Path
import json
import sys

base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

print("=" * 60)
print("CURRENT MODEL CHECK")
print("=" * 60)

# Check metrics
metrics_path = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
if metrics_path.exists():
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    print("\n📊 Current Metrics:")
    print(f"  Model: {metrics.get('model_name', 'N/A')}")
    print(f"  Problem Type: {metrics.get('problem_type', 'N/A')}")
    print(f"  Target: {metrics.get('target', 'N/A')}")
    print(f"  Features: {metrics.get('features', [])}")
    print(f"  Trained: {metrics.get('timestamp', 'N/A')}")
    
    if metrics.get('problem_type') == 'classification':
        print(f"\n  Accuracy: {metrics.get('accuracy', 0):.2%}")
        print(f"  Precision: {metrics.get('precision', 0):.2%}")
        print(f"  Recall: {metrics.get('recall', 0):.2%}")
        print(f"  F1 Score: {metrics.get('f1_score', 0):.2%}")
    else:
        print(f"\n  R² Score: {metrics.get('r2_score', 0):.4f}")
        print(f"  RMSE: {metrics.get('rmse', 0):.4f}")
        print(f"  MAE: {metrics.get('mae', 0):.4f}")
else:
    print("\n❌ No metrics file found!")

# Check current version
try:
    from MLOps_Engineer1.core.model_versioning import ModelVersionManager
    
    version_manager = ModelVersionManager()
    current_version = version_manager.get_current_version()
    
    print(f"\n📦 Current Version: {current_version}")
    
    if current_version:
        metadata = version_manager.get_version_metadata(current_version)
        if metadata:
            print(f"  Model: {metadata['model_name']}")
            print(f"  Target: {metadata['target']}")
            print(f"  Features: {metadata['features']}")
    
    # List all versions
    versions = version_manager.list_versions()
    print(f"\n📋 Total Versions: {len(versions)}")
    for v in versions[:5]:  # Show last 5
        print(f"  - {v['version']}: {v['model_name']} ({v['trained_at'][:19]})")

except Exception as e:
    print(f"\n❌ Error checking versions: {e}")

print("\n" + "=" * 60)
