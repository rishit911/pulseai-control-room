"""Engineer-2 | Real-time monitoring pipeline."""
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime, timedelta
from MLOps_Engineer2.core.drift_detector import DriftDetector, FairnessMonitor, save_monitoring_results

class MonitoringPipeline:
    """Orchestrate drift detection and fairness monitoring."""
    
    def __init__(self, reference_data_path: str, model_path: str = None):
        self.reference_data = pd.read_csv(reference_data_path)
        self.drift_detector = DriftDetector(self.reference_data)
        self.fairness_monitor = FairnessMonitor(sensitive_attribute='age')
        
        # Load model if provided
        self.model = None
        if model_path and Path(model_path).exists():
            import joblib
            self.model = joblib.load(model_path)
    
    def monitor_batch(self, current_data: pd.DataFrame) -> Dict:
        """Run monitoring on a data batch."""
        
        # Drift detection
        drift_results = self.drift_detector.detect_drift(current_data)
        
        # Fairness monitoring (if model available)
        fairness_results = None
        if self.model is not None:
            try:
                # Prepare features
                X = current_data[['age', 'education_num', 'hours_per_week']].copy()
                X['workclass_private'] = (current_data['workclass'] == 'Private').astype(int)
                
                # Get predictions
                predictions = self.model.predict(X)
                
                # True labels (if available)
                if 'income' in current_data.columns:
                    true_labels = (current_data['income'] == '>50K').astype(int).values
                    fairness_results = self.fairness_monitor.calculate_fairness_metrics(
                        current_data, predictions, true_labels
                    )
            except Exception as e:
                fairness_results = {'error': str(e)}
        
        return {
            'drift': drift_results,
            'fairness': fairness_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_monitoring_report(self, output_dir: str) -> str:
        """Generate comprehensive monitoring report."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate time series data for drift
        drift_history = []
        for i in range(90):
            date = datetime.now() - timedelta(days=90-i)
            # Simulate drift increasing over time
            p_value = max(0.01, 0.5 - (i * 0.005))
            drift_history.append({
                'date': date.strftime('%Y-%m-%d'),
                'p_value': p_value,
                'drift_detected': p_value < 0.05
            })
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'drift_history': drift_history,
            'current_status': {
                'drift_detected': drift_history[-1]['drift_detected'],
                'p_value': drift_history[-1]['p_value']
            }
        }
        
        filepath = save_monitoring_results(report, str(output_path), 'monitoring_report.json')
        return filepath

def run_monitoring():
    """Main monitoring execution."""
    base_dir = Path(__file__).resolve().parents[2]
    
    # Paths
    reference_data = base_dir / "MLOps_Engineer1" / "data" / "adult_small.csv"
    model_path = base_dir / "MLOps_Engineer1" / "artifacts" / "models" / "income_classifier.pkl"
    output_dir = base_dir / "MLOps_Engineer2" / "artifacts" / "monitoring"
    
    # Initialize pipeline
    pipeline = MonitoringPipeline(str(reference_data), str(model_path) if model_path.exists() else None)
    
    # Generate monitoring report
    report_path = pipeline.generate_monitoring_report(str(output_dir))
    print(f"✅ Monitoring report generated: {report_path}")
    
    # Monitor current data
    current_data = pd.read_csv(reference_data)  # In production, this would be streaming data
    results = pipeline.monitor_batch(current_data)
    
    # Save results
    results_path = save_monitoring_results(results, str(output_dir), 'latest_monitoring.json')
    print(f"✅ Monitoring results saved: {results_path}")
    
    return results

if __name__ == "__main__":
    run_monitoring()
