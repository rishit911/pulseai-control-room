# 📦 Model Versioning Guide

## Overview

Your MLOps platform now has **complete model versioning**! Every trained model is automatically versioned, tracked, and can be compared or rolled back.

---

## ✨ Features

### Automatic Versioning
- ✅ Every trained model gets a unique version (v1.0.0, v1.0.1, etc.)
- ✅ Metadata tracked (model type, features, metrics, timestamp)
- ✅ Full model artifacts saved per version
- ✅ Version registry maintained

### Version Management
- ✅ View all versions
- ✅ Compare any two versions
- ✅ Rollback to previous versions
- ✅ Delete old versions
- ✅ Track current version

### Visualizations
- ✅ Version timeline
- ✅ Performance comparison charts
- ✅ Feature importance per version
- ✅ Metrics trends

---

## 🧪 How to Test Versioning

### Test 1: Train Multiple Models

**Step 1: Train First Model**
```
1. Go to Model Training tab
2. Load "Iris (Flower Classification)"
3. Target: species
4. Features: all numeric
5. Model: Random Forest
6. Train
7. Note the version: v1.0.0
```

**Step 2: Train Second Model**
```
1. Stay in Model Training tab
2. Keep same data
3. Change Model: Logistic Regression
4. Train
5. Note the version: v1.0.1
```

**Step 3: Train Third Model**
```
1. Load "House Prices (Regression)"
2. Target: price
3. Features: all
4. Model: Random Forest
5. Train
6. Note the version: v1.0.2
```

**Result:** You now have 3 versions!

---

### Test 2: View All Versions

**Go to Model Versions Tab**
```
1. Click "📦 Model Versions" in sidebar
2. See statistics:
   - Total Versions: 3
   - Current Version: v1.0.2
   - Latest Version: v1.0.2
3. See table with all versions
4. Current version marked with 🟢
```

**What You'll See:**
- Version numbers
- Model types
- Performance metrics
- Training timestamps
- Status (Current/Archived)

---

### Test 3: View Version Details

**In Model Versions Tab:**
```
1. Select a version from dropdown
2. See detailed information:
   - Model type
   - Problem type
   - Features used
   - Target variable
   - All metrics
   - Feature importance chart
```

**Try Different Versions:**
- Select v1.0.0 → See Random Forest (Classification)
- Select v1.0.1 → See Logistic Regression
- Select v1.0.2 → See Random Forest (Regression)

---

### Test 4: Compare Versions

**Compare Two Models:**
```
1. In Model Versions tab
2. Scroll to "Compare Versions"
3. Select v1.0.0 (Random Forest)
4. Select v1.0.1 (Logistic Regression)
5. Click "Compare Versions"
```

**What You'll See:**
- Side-by-side metrics
- Difference calculations
- Percentage changes
- Comparison chart

**Example Output:**
```
Accuracy:
  v1.0.0: 0.9500
  v1.0.1: 0.9200
  Difference: -0.0300
  Change: -3.16%
```

---

### Test 5: Rollback to Previous Version

**Rollback Test:**
```
1. Current version: v1.0.2 (Regression)
2. In Model Versions tab
3. Go to "Rollback to Version"
4. Select v1.0.0 (Random Forest Classification)
5. Click "Rollback"
6. See success message
7. Refresh page
8. Current version now: v1.0.0
```

**Verify Rollback:**
```
1. Go to Model Status tab
2. Check metrics match v1.0.0
3. Go to Explainability tab
4. Check features match v1.0.0
```

---

### Test 6: Delete Old Version

**Delete Test:**
```
1. In Model Versions tab
2. Go to "Delete Version"
3. Select v1.0.1 (not current)
4. Click "Delete"
5. Click again to confirm
6. Version removed from list
```

**Note:** Cannot delete current version!

---

### Test 7: Version Timeline

**View Performance Over Time:**
```
1. In Model Versions tab
2. Scroll to "Version Timeline"
3. See line chart showing:
   - All versions on X-axis
   - Performance metric on Y-axis
   - Trend over time
```

**Interpretation:**
- Upward trend = improving models
- Downward = need to investigate
- Flat = consistent performance

---

## 📁 Where Versions Are Stored

### Directory Structure
```
MLOps_Engineer1/artifacts/models/
├── versions/
│   ├── v1.0.0/
│   │   ├── model.pkl
│   │   ├── metrics.json
│   │   ├── feature_importance.json
│   │   └── metadata.json
│   ├── v1.0.1/
│   │   ├── model.pkl
│   │   ├── metrics.json
│   │   ├── feature_importance.json
│   │   └── metadata.json
│   └── v1.0.2/
│       ├── model.pkl
│       ├── metrics.json
│       ├── feature_importance.json
│       └── metadata.json
├── model_registry.json
├── current_version.txt
├── income_classifier.pkl  (current version)
├── metrics.json           (current version)
└── feature_importance.json (current version)
```

---

## 🔍 Check Versioning Files

### Via Command Line

**Check Registry:**
```bash
type MLOps_Engineer1\artifacts\models\model_registry.json
```

**Check Current Version:**
```bash
type MLOps_Engineer1\artifacts\models\current_version.txt
```

**List All Versions:**
```bash
dir MLOps_Engineer1\artifacts\models\versions
```

**Check Specific Version:**
```bash
type MLOps_Engineer1\artifacts\models\versions\v1.0.0\metadata.json
```

---

## 📊 Version Metadata

Each version stores:

```json
{
  "version": "v1.0.0",
  "model_name": "Random Forest",
  "features": ["sepal_length", "sepal_width", ...],
  "target": "species",
  "metrics": {
    "accuracy": 0.95,
    "precision": 0.94,
    ...
  },
  "feature_importance": {
    "sepal_length": 0.35,
    ...
  },
  "trained_at": "2025-11-07T15:30:00",
  "model_path": "...",
  "status": "active"
}
```

---

## 🎯 Use Cases

### Development Workflow
1. Train baseline model → v1.0.0
2. Try different features → v1.0.1
3. Try different algorithm → v1.0.2
4. Compare all versions
5. Deploy best performing

### Production Workflow
1. Current model in production → v1.0.5
2. Train new model → v1.0.6
3. Compare v1.0.5 vs v1.0.6
4. If better, keep v1.0.6
5. If worse, rollback to v1.0.5

### Experimentation
1. Train multiple models
2. Compare all versions
3. Identify best features
4. Identify best algorithm
5. Retrain with best config

---

## 💡 Best Practices

### Version Management
- ✅ Keep at least 3-5 recent versions
- ✅ Delete very old versions to save space
- ✅ Document major version changes
- ✅ Test before rolling back
- ✅ Compare before deploying

### Naming Convention
- Automatic: v1.0.0, v1.0.1, v1.0.2...
- Patch increments for each new model
- Can be extended for major/minor versions

### Monitoring
- Track version performance over time
- Set up alerts for degradation
- Regular version audits
- Keep version changelog

---

## 🔧 Troubleshooting

### "No versions found"
**Solution:** Train at least one model first

### "Cannot delete current version"
**Solution:** Rollback to different version first, then delete

### "Rollback failed"
**Solution:** Check if version exists in versions directory

### "Version not found"
**Solution:** Check model_registry.json for available versions

---

## 📈 Version Comparison Metrics

### Classification
- Accuracy difference
- Precision difference
- Recall difference
- F1 Score difference

### Regression
- R² Score difference
- RMSE difference
- MAE difference
- MAPE difference

---

## 🎉 Summary

Your versioning system provides:

✅ **Automatic tracking** of all models
✅ **Complete metadata** for each version
✅ **Easy comparison** between versions
✅ **Quick rollback** to any version
✅ **Version timeline** visualization
✅ **Safe deletion** of old versions
✅ **Current version** tracking
✅ **Full integration** with dashboard

---

## 🚀 Quick Test Sequence

```
1. Train 3 different models
2. Go to Model Versions tab
3. See all 3 versions listed
4. Compare first two versions
5. Rollback to first version
6. Verify rollback worked
7. Delete middle version
8. View timeline chart
```

**Time:** 5-10 minutes
**Result:** Full understanding of versioning!

---

**Your MLOps platform now has enterprise-grade model versioning! 🎊**
