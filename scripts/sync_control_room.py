"""
Sync Control Room Data with Latest Model Training
This script updates the Control Room dashboard with data from the latest trained model.
"""
import sys
from pathlib import Path

# Add project root to path
base_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(base_dir))

from MLOps_Engineer1.core.integration.data_sync import DataSynchronizer

def main():
    print("🔄 Syncing Control Room data with latest model training...")
    print("-" * 60)
    
    syncer = DataSynchronizer()
    result = syncer.sync_all_data()
    
    if result.get('status') == 'success':
        print("\n✅ All dashboard data synced successfully!")
        print(f"📊 Sync timestamp: {result.get('sync_timestamp')}")
        print("\n📁 Updated data files (MLOps_Engineer4/data/):")
        print("  • control_meta.json - Control room metadata")
        print("  • parameters.json - Feature parameters")
        print("  • spc.json - Statistical process control data")
        print("  • ooc_breakdown.json - Out-of-control breakdown")
        print("  • validation.json - Data validation results")
        print("  • drift_timeline.json - 90-day drift history")
        print("  • explainability.json - Feature importance & summary")
        print("  • fairness.json - Group-level fairness metrics")
        print("  • metrics_timeseries.json - Performance over time")
        print("  • model_status.json - Current model status")
        print("  • recovery.json - Deployment history")
        
        print("\n📁 Updated monitoring files (MLOps_Engineer2/artifacts/monitoring/):")
        print("  • latest_monitoring.json - Current drift & fairness")
        print("  • monitoring_report.json - Historical drift data")
        
        # Show key metrics
        if 'control_meta' in result:
            meta = result['control_meta']
            print(f"\n📈 Model Performance:")
            print(f"  • Success Rate: {meta.get('success_rate', 0):.2f}%")
            print(f"  • Total Processed: {meta.get('total_processed', 0)} records")
            print(f"  • Status: {meta.get('status', 'unknown')}")
            print(f"  • Alerts: {meta.get('alerts', 0)}")
        
        # Show monitoring metrics
        if 'monitoring' in result:
            monitoring = result['monitoring']
            drift = monitoring.get('drift', {})
            fairness = monitoring.get('fairness', {})
            
            print(f"\n🔍 Drift & Fairness:")
            print(f"  • Drift Detected: {'Yes' if drift.get('drift_detected') else 'No'}")
            print(f"  • Drifted Features: {drift.get('summary', {}).get('drifted_features', 0)}")
            print(f"  • Fairness Score: {fairness.get('fairness_score', 0):.3f}")
        
        # Show model status
        if 'model_status' in result:
            status = result['model_status']
            print(f"\n📦 Model Version:")
            print(f"  • Active Model: {status.get('active_model', 'N/A')}")
            print(f"  • Last Trained: {status.get('last_trained', 'N/A')}")
        
        print(f"\n✨ Total files synced: 13")
    else:
        print(f"\n❌ Error syncing data: {result.get('error')}")
        return 1
    
    print("\n💡 Tip: Refresh your dashboard to see the updated data!")
    return 0

if __name__ == "__main__":
    exit(main())
