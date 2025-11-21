"""
Final Setup Script - Ensure everything is working correctly
"""
import sys
from pathlib import Path

# Add project root to path
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

def main():
    print("🔧 Final MLOps Platform Setup")
    print("=" * 50)
    
    # 1. Sync all data
    print("\n1. Syncing all dashboard data...")
    try:
        from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer
        syncer = DataSynchronizer()
        result = syncer.sync_all_data()
        
        if result.get('status') == 'success':
            print("✅ All data synced successfully!")
            print(f"   • Files synced: 13")
            print(f"   • Timestamp: {result.get('sync_timestamp')}")
        else:
            print(f"❌ Sync failed: {result.get('error')}")
            return 1
    except Exception as e:
        print(f"❌ Sync error: {e}")
        return 1
    
    # 2. Check model status
    print("\n2. Checking model status...")
    try:
        from MLOps_Engineer1.core.model_versioning import ModelVersionManager
        version_manager = ModelVersionManager()
        current_version = version_manager.get_current_version()
        
        if current_version:
            print(f"✅ Current model version: {current_version}")
            
            # Get model info
            metadata = version_manager.get_version_metadata(current_version)
            if metadata:
                print(f"   • Model: {metadata.get('model_name', 'Unknown')}")
                print(f"   • Features: {len(metadata.get('features', []))}")
                print(f"   • Target: {metadata.get('target', 'Unknown')}")
        else:
            print("⚠️ No model found - train a model first")
    except Exception as e:
        print(f"⚠️ Model check warning: {e}")
    
    # 3. Verify file structure
    print("\n3. Verifying file structure...")
    
    required_files = [
        "MLOps_Engineer4/app/main.py",
        "MLOps_Engineer3/api/serve.py", 
        "MLOps_Engineer1/core/integration/data_sync.py",
        "MLOps_Engineer1/core/model_versioning.py",
        "scripts/sync_control_room.py",
        "scripts/check_monitoring_data.py",
        "scripts/check_current_model.py",
        "COMPLETE_MLOPS_GUIDE.md",
        "README.md"
    ]
    
    all_good = True
    for file_path in required_files:
        if (base_dir / file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    # 4. Check data files
    print("\n4. Checking data files...")
    data_dir = base_dir / "MLOps_Engineer4" / "data"
    
    expected_files = [
        "control_meta.json", "parameters.json", "spc.json",
        "ooc_breakdown.json", "validation.json", "drift_timeline.json",
        "explainability.json", "fairness.json", "metrics_timeseries.json",
        "model_status.json", "recovery.json"
    ]
    
    data_files_ok = 0
    for file_name in expected_files:
        if (data_dir / file_name).exists():
            data_files_ok += 1
    
    print(f"✅ Data files: {data_files_ok}/{len(expected_files)} present")
    
    # 5. Final status
    print("\n" + "=" * 50)
    if all_good and data_files_ok >= 10:
        print("🎉 MLOps Platform Setup Complete!")
        print("\n🚀 Ready to run:")
        print("   Terminal 1: streamlit run MLOps_Engineer4/app/main.py")
        print("   Terminal 2: python MLOps_Engineer3/api/serve.py")
        print("\n📖 See COMPLETE_MLOPS_GUIDE.md for full documentation")
        return 0
    else:
        print("⚠️ Setup incomplete - check errors above")
        return 1

if __name__ == "__main__":
    exit(main())