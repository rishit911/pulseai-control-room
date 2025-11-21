"""
Test Model Status Tab - Verify it loads correct data
"""
import sys
from pathlib import Path
import json

# Add project root to path
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

def main():
    print("🧪 Testing Model Status Tab Data Loading")
    print("=" * 60)
    
    # Test 1: Check metrics.json
    print("\n1. Testing metrics.json loading...")
    metrics_path = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
    
    if not metrics_path.exists():
        print("❌ metrics.json not found!")
        return 1
    
    try:
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        
        print("✅ metrics.json loaded successfully")
        print(f"   Model: {metrics.get('model_name', 'Unknown')}")
        print(f"   Problem type: {metrics.get('problem_type', 'Unknown')}")
        print(f"   Features: {metrics.get('features', [])}")
        print(f"   Target: {metrics.get('target', 'Unknown')}")
        
        if metrics.get('problem_type') == 'classification':
            print(f"   Accuracy: {metrics.get('accuracy', 0):.4f}")
            print(f"   Precision: {metrics.get('precision', 0):.4f}")
            print(f"   Recall: {metrics.get('recall', 0):.4f}")
        else:
            print(f"   R² Score: {metrics.get('r2_score', 0):.4f}")
            print(f"   RMSE: {metrics.get('rmse', 0):.4f}")
            print(f"   MAE: {metrics.get('mae', 0):.4f}")
    except Exception as e:
        print(f"❌ Error loading metrics: {e}")
        return 1
    
    # Test 2: Check version manager
    print("\n2. Testing version manager...")
    try:
        from MLOps_Engineer1.core.model_versioning import ModelVersionManager
        
        version_manager = ModelVersionManager()
        current_version = version_manager.get_current_version()
        
        if current_version:
            print(f"✅ Current version: {current_version}")
            
            metadata = version_manager.get_version_metadata(current_version)
            if metadata:
                print(f"   Version model: {metadata.get('model_name', 'Unknown')}")
                print(f"   Version features: {metadata.get('features', [])}")
        else:
            print("⚠️ No current version set")
    except Exception as e:
        print(f"❌ Error with version manager: {e}")
    
    # Test 3: Check if data matches
    print("\n3. Checking data consistency...")
    
    if current_version and metadata:
        metrics_model = metrics.get('model_name', '')
        version_model = metadata.get('model_name', '')
        
        if metrics_model == version_model:
            print(f"✅ Model names match: {metrics_model}")
        else:
            print(f"⚠️ Model name mismatch:")
            print(f"   metrics.json: {metrics_model}")
            print(f"   version metadata: {version_model}")
            print(f"   → Model Status will use metrics.json (source of truth)")
    
    # Test 4: Simulate what Model Status tab will show
    print("\n4. What Model Status tab will display:")
    print("-" * 60)
    
    model_info = {
        'model_type': metrics.get('model_name', 'Unknown'),
        'version': current_version if current_version else 'Unknown',
        'features': metrics.get('features', []),
        'target': metrics.get('target', 'Unknown'),
        'problem_type': metrics.get('problem_type', 'Unknown')
    }
    
    print(f"Model Type: {model_info['model_type']}")
    print(f"Version: {model_info['version']}")
    print(f"Problem Type: {model_info['problem_type']}")
    print(f"Target: {model_info['target']}")
    print(f"Features: {', '.join(model_info['features'])}")
    
    if metrics.get('problem_type') == 'classification':
        print(f"\nPerformance Metrics:")
        print(f"  Accuracy: {metrics.get('accuracy', 0):.4f}")
        print(f"  Precision: {metrics.get('precision', 0):.4f}")
        print(f"  Recall: {metrics.get('recall', 0):.4f}")
        print(f"  F1 Score: {metrics.get('f1_score', 0):.4f}")
    else:
        print(f"\nPerformance Metrics:")
        print(f"  R² Score: {metrics.get('r2_score', 0):.4f}")
        print(f"  RMSE: {metrics.get('rmse', 0):.4f}")
        print(f"  MAE: {metrics.get('mae', 0):.4f}")
        if 'mape' in metrics:
            print(f"  MAPE: {metrics.get('mape', 0):.2%}")
    
    print("\n" + "=" * 60)
    print("✅ Model Status tab should display correctly!")
    print("\n💡 If dashboard still shows old data:")
    print("   1. Click 🔄 Sync button in Model Status tab")
    print("   2. Or click 🔄 Refresh button")
    print("   3. Or restart the dashboard")
    
    return 0

if __name__ == "__main__":
    exit(main())
