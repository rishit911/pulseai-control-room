"""
Retrain Model - Fix scikit-learn version compatibility
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to path
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

def main():
    print("🔄 Retraining Model with Current scikit-learn Version")
    print("=" * 60)
    
    # Check scikit-learn version
    try:
        import sklearn
        print(f"✅ scikit-learn version: {sklearn.__version__}")
    except ImportError:
        print("❌ scikit-learn not installed!")
        return 1
    
    # Load the iris data (or whatever data was used)
    print("\n📊 Loading training data...")
    data_file = base_dir / "MLOps_Engineer1" / "data" / "adult_small.csv"
    
    if not data_file.exists():
        print(f"❌ Data file not found: {data_file}")
        print("💡 Use the Model Training tab in the dashboard to train a new model")
        return 1
    
    try:
        df = pd.read_csv(data_file)
        print(f"✅ Data loaded: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return 1
    
    # Check what features to use based on metrics.json
    metrics_file = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
    
    if metrics_file.exists():
        import json
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
        
        features = metrics.get('features', [])
        target = metrics.get('target', '')
        model_name = metrics.get('model_name', 'Random Forest')
        problem_type = metrics.get('problem_type', 'regression')
        
        print(f"\n🎯 Previous model configuration:")
        print(f"   Model: {model_name}")
        print(f"   Type: {problem_type}")
        print(f"   Features: {features}")
        print(f"   Target: {target}")
        
        # Check if we have these columns
        missing_cols = [col for col in features + [target] if col not in df.columns]
        
        if missing_cols:
            print(f"\n⚠️  Missing columns in data: {missing_cols}")
            print(f"💡 Available columns: {list(df.columns)}")
            print(f"\n💡 Solution: Use the Model Training tab to train with available data")
            return 1
        
        print(f"\n✅ All required columns present in data")
        print(f"\n💡 To retrain with current scikit-learn version:")
        print(f"   1. Go to Model Training tab in dashboard")
        print(f"   2. Upload your data (or use sample data)")
        print(f"   3. Select features: {', '.join(features)}")
        print(f"   4. Select target: {target}")
        print(f"   5. Choose algorithm: {model_name}")
        print(f"   6. Click 'Train Model'")
        print(f"\n   This will create a new model compatible with scikit-learn {sklearn.__version__}")
        
    else:
        print("\n💡 No previous model configuration found")
        print("   Use the Model Training tab to train a new model")
    
    print("\n" + "=" * 60)
    print("✅ Ready to retrain!")
    print("\n🚀 Quick Start:")
    print("   1. Open dashboard: http://localhost:8501")
    print("   2. Go to Model Training tab")
    print("   3. Train a new model")
    print("   4. New model will be compatible with current scikit-learn version")
    
    return 0

if __name__ == "__main__":
    exit(main())
