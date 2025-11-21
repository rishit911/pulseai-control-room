"""
Model Versioning System
Tracks all trained models with versions, timestamps, and metadata
"""
import json
from pathlib import Path
from datetime import datetime
import shutil
import joblib
from typing import Dict, List, Optional

class ModelVersionManager:
    """Manage model versions with metadata tracking."""
    
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).resolve().parents[2] / "artifacts" / "models"
        
        self.versions_dir = self.base_dir / "versions"
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        
        self.registry_file = self.base_dir / "model_registry.json"
        self.current_version_file = self.base_dir / "current_version.txt"
    
    def get_next_version(self) -> str:
        """Get the next version number."""
        registry = self.load_registry()
        if not registry:
            return "v1.0.0"
        
        # Get latest version
        versions = [v['version'] for v in registry]
        if not versions:
            return "v1.0.0"
        
        # Parse latest version (format: v1.0.0)
        latest = sorted(versions)[-1]
        major, minor, patch = latest[1:].split('.')
        
        # Increment patch version
        new_patch = int(patch) + 1
        return f"v{major}.{minor}.{new_patch}"
    
    def save_model_version(
        self,
        model,
        metrics: Dict,
        feature_importance: Dict,
        model_name: str,
        features: List[str],
        target: str,
        version: str = None
    ) -> str:
        """Save a new model version with metadata."""
        
        # Get version number
        if version is None:
            version = self.get_next_version()
        
        # Create version directory
        version_dir = self.versions_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # Save model
        model_path = version_dir / "model.pkl"
        joblib.dump(model, model_path)
        
        # Save metrics
        metrics_path = version_dir / "metrics.json"
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Save feature importance
        importance_path = version_dir / "feature_importance.json"
        with open(importance_path, 'w') as f:
            json.dump(feature_importance, f, indent=2)
        
        # Create metadata
        metadata = {
            'version': version,
            'model_name': model_name,
            'features': features,
            'target': target,
            'metrics': metrics,
            'feature_importance': feature_importance,
            'trained_at': datetime.now().isoformat(),
            'model_path': str(model_path),
            'status': 'active'
        }
        
        # Save metadata
        metadata_path = version_dir / "metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update registry
        self.add_to_registry(metadata)
        
        # Set as current version
        self.set_current_version(version)
        
        # Also save to main location for backward compatibility
        self._save_to_main_location(model, metrics, feature_importance)
        
        return version
    
    def _save_to_main_location(self, model, metrics, feature_importance):
        """Save to main location for backward compatibility."""
        import joblib
        
        joblib.dump(model, self.base_dir / "income_classifier.pkl")
        
        with open(self.base_dir / "metrics.json", 'w') as f:
            json.dump(metrics, f, indent=2)
        
        with open(self.base_dir / "feature_importance.json", 'w') as f:
            json.dump(feature_importance, f, indent=2)
    
    def load_registry(self) -> List[Dict]:
        """Load the model registry."""
        if self.registry_file.exists():
            with open(self.registry_file, 'r') as f:
                return json.load(f)
        return []
    
    def add_to_registry(self, metadata: Dict):
        """Add a model version to the registry."""
        registry = self.load_registry()
        
        # Check if version already exists
        existing = [m for m in registry if m['version'] == metadata['version']]
        if existing:
            # Update existing
            for i, m in enumerate(registry):
                if m['version'] == metadata['version']:
                    registry[i] = metadata
        else:
            # Add new
            registry.append(metadata)
        
        # Save registry
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def get_current_version(self) -> Optional[str]:
        """Get the current active version."""
        if self.current_version_file.exists():
            return self.current_version_file.read_text().strip()
        return None
    
    def set_current_version(self, version: str):
        """Set the current active version."""
        self.current_version_file.write_text(version)
    
    def get_version_metadata(self, version: str) -> Optional[Dict]:
        """Get metadata for a specific version."""
        registry = self.load_registry()
        for metadata in registry:
            if metadata['version'] == version:
                return metadata
        return None
    
    def list_versions(self) -> List[Dict]:
        """List all model versions."""
        registry = self.load_registry()
        # Sort by trained_at descending
        return sorted(registry, key=lambda x: x['trained_at'], reverse=True)
    
    def load_model_version(self, version: str):
        """Load a specific model version."""
        version_dir = self.versions_dir / version
        model_path = version_dir / "model.pkl"
        
        if model_path.exists():
            return joblib.load(model_path)
        return None
    
    def rollback_to_version(self, version: str) -> bool:
        """Rollback to a specific version."""
        metadata = self.get_version_metadata(version)
        if not metadata:
            return False
        
        # Load the model
        model = self.load_model_version(version)
        if model is None:
            return False
        
        # Load metrics and feature importance
        version_dir = self.versions_dir / version
        
        with open(version_dir / "metrics.json", 'r') as f:
            metrics = json.load(f)
        
        with open(version_dir / "feature_importance.json", 'r') as f:
            feature_importance = json.load(f)
        
        # Save to main location
        self._save_to_main_location(model, metrics, feature_importance)
        
        # Set as current version
        self.set_current_version(version)
        
        return True
    
    def compare_versions(self, version1: str, version2: str) -> Dict:
        """Compare two model versions."""
        meta1 = self.get_version_metadata(version1)
        meta2 = self.get_version_metadata(version2)
        
        if not meta1 or not meta2:
            return {}
        
        comparison = {
            'version1': version1,
            'version2': version2,
            'metrics_comparison': {},
            'model_comparison': {
                'version1_model': meta1['model_name'],
                'version2_model': meta2['model_name']
            }
        }
        
        # Compare metrics
        for metric in meta1['metrics']:
            if metric in meta2['metrics']:
                v1_val = meta1['metrics'][metric]
                v2_val = meta2['metrics'][metric]
                
                if isinstance(v1_val, (int, float)) and isinstance(v2_val, (int, float)):
                    diff = v2_val - v1_val
                    pct_change = (diff / v1_val * 100) if v1_val != 0 else 0
                    
                    comparison['metrics_comparison'][metric] = {
                        'version1': v1_val,
                        'version2': v2_val,
                        'difference': diff,
                        'percent_change': pct_change
                    }
        
        return comparison
    
    def delete_version(self, version: str) -> bool:
        """Delete a model version (except current)."""
        current = self.get_current_version()
        if version == current:
            return False  # Cannot delete current version
        
        # Remove from registry
        registry = self.load_registry()
        registry = [m for m in registry if m['version'] != version]
        
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
        
        # Delete version directory
        version_dir = self.versions_dir / version
        if version_dir.exists():
            shutil.rmtree(version_dir)
        
        return True
    
    def get_version_stats(self) -> Dict:
        """Get statistics about model versions."""
        registry = self.load_registry()
        
        if not registry:
            return {
                'total_versions': 0,
                'current_version': None,
                'latest_version': None
            }
        
        return {
            'total_versions': len(registry),
            'current_version': self.get_current_version(),
            'latest_version': sorted([m['version'] for m in registry])[-1],
            'oldest_version': sorted([m['version'] for m in registry])[0],
            'total_models_trained': len(registry)
        }
