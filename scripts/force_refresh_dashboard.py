"""
Force Refresh Dashboard - Sync data and clear cache
"""
import sys
from pathlib import Path

# Add project root to path
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

def main():
    print("🔄 Force Refreshing Dashboard Data...")
    print("=" * 60)
    
    # 1. Sync all data
    print("\n1. Syncing all data...")
    try:
        from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer
        syncer = DataSynchronizer()
        result = syncer.sync_all_data()
        
        if result.get('status') == 'success':
            print("✅ Data synced successfully!")
        else:
            print(f"❌ Sync failed: {result.get('error')}")
            return 1
    except Exception as e:
        print(f"❌ Sync error: {e}")
        return 1
    
    # 2. Show current model info
    print("\n2. Current model info:")
    try:
        from MLOps_Engineer1.core.model_versioning import ModelVersionManager
        version_manager = ModelVersionManager()
        current_version = version_manager.get_current_version()
        
        if current_version:
            print(f"✅ Current version: {current_version}")
            
            metadata = version_manager.get_version_metadata(current_version)
            if metadata:
                print(f"   Model: {metadata.get('model_name', 'Unknown')}")
                print(f"   Features: {metadata.get('features', [])}")
                print(f"   Target: {metadata.get('target', 'Unknown')}")
        else:
            print("⚠️ No current version found")
    except Exception as e:
        print(f"⚠️ Error getting version: {e}")
    
    # 3. Check metrics file
    print("\n3. Checking metrics file...")
    metrics_file = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "metrics.json"
    
    if metrics_file.exists():
        import json
        import os
        from datetime import datetime
        
        mtime = os.path.getmtime(metrics_file)
        last_modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
        
        print(f"✅ Metrics file exists")
        print(f"   Last modified: {last_modified}")
        print(f"   Model: {metrics.get('model_name', 'Unknown')}")
        print(f"   Problem type: {metrics.get('problem_type', 'Unknown')}")
        
        if metrics.get('problem_type') == 'classification':
            print(f"   Accuracy: {metrics.get('accuracy', 0):.4f}")
        else:
            print(f"   R² Score: {metrics.get('r2_score', 0):.4f}")
    else:
        print("❌ Metrics file not found")
    
    print("\n" + "=" * 60)
    print("✅ Refresh complete!")
    print("\n💡 Next steps:")
    print("   1. Go to Model Status tab in dashboard")
    print("   2. Click 🔄 Refresh or 🔄 Sync button")
    print("   3. Should show latest model data")
    
    return 0

if __name__ == "__main__":
    exit(main())
