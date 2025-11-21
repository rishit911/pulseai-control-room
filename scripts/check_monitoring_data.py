"""
Check Monitoring Data - Verify drift and fairness data
"""
import json
from pathlib import Path
from datetime import datetime

def main():
    print("🔍 Checking Monitoring Data...")
    print("-" * 60)
    
    base_dir = Path(__file__).resolve().parents[1]
    monitoring_file = base_dir / "MLOps_Engineer2" / "artifacts" / "monitoring" / "latest_monitoring.json"
    
    if not monitoring_file.exists():
        print("❌ Monitoring file not found!")
        print(f"Expected location: {monitoring_file}")
        return 1
    
    # Check file timestamp
    import os
    mtime = os.path.getmtime(monitoring_file)
    last_update = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"📅 File last modified: {last_update}")
    
    # Load and display data
    with open(monitoring_file, 'r') as f:
        data = json.load(f)
    
    print(f"\n📊 Data timestamp: {data.get('timestamp', 'N/A')}")
    
    # Drift data
    drift = data.get('drift', {})
    print(f"\n🔍 Drift Detection:")
    print(f"  • Drift Detected: {drift.get('drift_detected', False)}")
    print(f"  • Features Monitored: {drift.get('summary', {}).get('total_features', 0)}")
    print(f"  • Drifted Features: {drift.get('summary', {}).get('drifted_features', 0)}")
    
    if 'features' in drift:
        print(f"\n  Feature Details:")
        for feature, metrics in drift['features'].items():
            print(f"    • {feature}: P-value={metrics['p_value']:.4f}, Drift={metrics['drift']}")
    
    # Fairness data
    fairness = data.get('fairness', {})
    print(f"\n⚖️ Fairness Analysis:")
    print(f"  • Fairness Score: {fairness.get('fairness_score', 0):.4f}")
    
    if 'groups' in fairness:
        print(f"\n  Group Accuracy:")
        for group, metrics in fairness['groups'].items():
            print(f"    • {group}: {metrics['accuracy']:.2%} (n={metrics['sample_size']})")
    
    print("\n✅ Monitoring data loaded successfully!")
    print("\n💡 If dashboard shows old data:")
    print("   1. Click 🔄 Refresh button in Drift & Fairness tab")
    print("   2. Click 🗑️ Clear Cache button")
    print("   3. Restart the dashboard")
    
    return 0

if __name__ == "__main__":
    exit(main())
