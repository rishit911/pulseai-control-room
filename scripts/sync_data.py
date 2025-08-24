#!/usr/bin/env python3
"""
Data Synchronization Script
Syncs real pipeline data from Engineer 1 to Engineer 4 dashboard
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    try:
        from MLOps_Engineer1.core.integration.data_sync import sync_pipeline_data
        
        print("🔄 Syncing pipeline data to dashboard...")
        result = sync_pipeline_data()
        
        if result.get("status") == "success":
            print("✅ Data sync completed successfully!")
            print(f"   - Validation data: {'✅' if 'validation' in result else '❌'}")
            print(f"   - Control metadata: {'✅' if 'control_meta' in result else '❌'}")
            print(f"   - Sync timestamp: {result.get('sync_timestamp', 'N/A')}")
        else:
            print(f"❌ Data sync failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"❌ Data sync error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())