"""Engineer-2 | Drift detection using statistical tests."""
import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, List

class DriftDetector:
    """Detect data drift using Kolmogorov-Smirnov test."""
    
    def __init__(self, reference_data: pd.DataFrame):
        self.reference_data = reference_data
        self.numeric_cols = reference_data.select_dtypes(include=[np.number]).columns.tolist()
    
    def detect_drift(self, current_data: pd.DataFrame, threshold: float = 0.05) -> Dict:
        """
        Detect drift using KS test.
        Returns dict with drift status and p-values for each feature.
        """
        results = {
            'timestamp': datetime.now().isoformat(),
            'drift_detected': False,
            'features': {},
            'summary': {}
        }
        
        drift_count = 0
        
        for col in self.numeric_cols:
            if col in current_data.columns:
                # Kolmogorov-Smirnov test
                statistic, p_value = stats.ks_2samp(
                    self.reference_data[col].dropna(),
                    current_data[col].dropna()
                )
                
                has_drift = p_value < threshold
                if has_drift:
                    drift_count += 1
                
                results['features'][col] = {
                    'p_value': float(p_value),
                    'statistic': float(statistic),
                    'drift': has_drift,
                    'threshold': threshold
                }
        
        results['drift_detected'] = drift_count > 0
        results['summary'] = {
            'total_features': len(self.numeric_cols),
            'drifted_features': drift_count,
            'drift_percentage': (drift_count / len(self.numeric_cols)) * 100 if self.numeric_cols else 0
        }
        
        return results
    
    def calculate_psi(self, reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
        """Calculate Population Stability Index (PSI)."""
        # Create bins based on reference data
        _, bin_edges = np.histogram(reference.dropna(), bins=bins)
        
        # Calculate distributions
        ref_dist, _ = np.histogram(reference.dropna(), bins=bin_edges)
        cur_dist, _ = np.histogram(current.dropna(), bins=bin_edges)
        
        # Normalize
        ref_dist = ref_dist / len(reference) + 1e-10
        cur_dist = cur_dist / len(current) + 1e-10
        
        # Calculate PSI
        psi = np.sum((cur_dist - ref_dist) * np.log(cur_dist / ref_dist))
        
        return float(psi)

class FairnessMonitor:
    """Monitor model fairness across demographic groups."""
    
    def __init__(self, sensitive_attribute: str = 'age'):
        self.sensitive_attribute = sensitive_attribute
    
    def calculate_fairness_metrics(
        self, 
        data: pd.DataFrame, 
        predictions: np.ndarray, 
        true_labels: np.ndarray
    ) -> Dict:
        """Calculate fairness metrics by demographic groups."""
        
        # Create age groups
        if self.sensitive_attribute == 'age':
            data['age_group'] = pd.cut(
                data['age'], 
                bins=[0, 30, 45, 100], 
                labels=['Young', 'Middle', 'Senior']
            )
            groups = data['age_group']
        else:
            groups = data[self.sensitive_attribute]
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'groups': {}
        }
        
        for group in groups.unique():
            if pd.isna(group):
                continue
            
            mask = groups == group
            group_preds = predictions[mask]
            group_true = true_labels[mask]
            
            if len(group_preds) > 0:
                accuracy = np.mean(group_preds == group_true)
                positive_rate = np.mean(group_preds == 1)
                
                results['groups'][str(group)] = {
                    'accuracy': float(accuracy),
                    'positive_prediction_rate': float(positive_rate),
                    'sample_size': int(np.sum(mask))
                }
        
        # Calculate disparate impact
        if len(results['groups']) >= 2:
            accuracies = [g['accuracy'] for g in results['groups'].values()]
            results['fairness_score'] = float(min(accuracies) / max(accuracies)) if max(accuracies) > 0 else 1.0
        else:
            results['fairness_score'] = 1.0
        
        return results

def save_monitoring_results(results: Dict, output_dir: str, filename: str):
    """Save monitoring results to JSON."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
    
    return str(filepath)
