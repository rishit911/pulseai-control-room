# 🔄 Dashboard Refresh Guide

## How Updates Work

When you train a new model, the dashboard tabs need to be refreshed to show the new data.

---

## ✅ What Gets Updated Automatically

### Immediate Updates (No Refresh Needed)
- ✅ Model Training tab - Shows results immediately
- ✅ Model Versions tab - New version appears instantly
- ✅ Model artifacts saved to disk

### Requires Refresh
- 🔄 Model Status - Needs refresh to load new metrics
- 🔄 Explainability - Needs refresh to load new feature importance
- 🔄 Drift & Fairness - Needs refresh to load new monitoring data
- 🔄 Data Health - Needs refresh to load new validation data

---

## 🔄 How to Refresh

### Method 1: Use Refresh Button (Recommended)
```
1. Go to any tab (Model Status, Explainability, etc.)
2. Look for 🔄 Refresh button in top-right
3. Click it
4. Tab reloads with new data
```

### Method 2: Browser Refresh
```
1. Press R key in browser
2. Or press F5
3. Or click browser refresh button
4. Entire app reloads
```

### Method 3: Navigate Away and Back
```
1. Click on different tab
2. Click back to original tab
3. Data refreshes
```

---

## 📊 What You'll See After Refresh

### Model Status Tab
**Before Refresh:**
- Old metrics (0.00% or previous model)
- Old version number

**After Refresh:**
- ✅ New metrics from latest model
- ✅ Current version number
- ✅ Updated performance charts
- ✅ New timestamp

### Explainability Tab
**Before Refresh:**
- Old feature importance

**After Refresh:**
- ✅ New feature importance
- ✅ Updated features list
- ✅ New importance values

### Drift & Fairness Tab
**Before Refresh:**
- Old monitoring data

**After Refresh:**
- ✅ Reset drift baseline
- ✅ New fairness metrics
- ✅ Updated trends

---

## 🧪 Test the Refresh

### Quick Test:
```
1. Note current metrics in Model Status
2. Go to Model Training
3. Train a new model (different algorithm)
4. Go back to Model Status
5. Click 🔄 Refresh
6. See new metrics!
```

### Example:
```
Before Training:
- Model Status: Accuracy 95% (Random Forest)
- Version: v1.0.0

Train New Model:
- Logistic Regression
- Gets version v1.0.1

After Refresh:
- Model Status: Accuracy 92% (Logistic Regression)
- Version: v1.0.1
```

---

## 💡 Why Manual Refresh?

### Design Choice
- Prevents unnecessary reloads
- Gives you control
- Saves resources
- Allows comparison before switching

### Alternative (Auto-Refresh)
If you want automatic refresh, you can:
1. Use browser auto-refresh extension
2. Set refresh interval (e.g., every 30 seconds)
3. Or press R manually when needed

---

## 🔧 Troubleshooting

### "Still showing old data after refresh"
**Solution:**
1. Try browser refresh (F5 or R)
2. Check if model training completed successfully
3. Verify artifacts were saved
4. Check file timestamps

### "Refresh button not working"
**Solution:**
1. Use browser refresh (F5)
2. Navigate to different tab and back
3. Restart Streamlit app if needed

### "Metrics show 0.00%"
**Solution:**
1. Train a model first
2. Wait for training to complete
3. Refresh the tab
4. Check artifacts exist

---

## 📁 Behind the Scenes

### What Happens When You Refresh

**Model Status Tab:**
```
1. Checks API for model info
2. Falls back to local artifacts
3. Loads metrics.json
4. Displays current version
5. Shows performance charts
```

**Explainability Tab:**
```
1. Reads feature_importance.json
2. Loads from artifacts directory
3. Displays importance chart
4. Shows feature details
```

**Other Tabs:**
```
1. Read their respective data files
2. Load from artifacts
3. Display updated information
```

---

## 🎯 Best Practices

### After Training
1. ✅ Wait for "Model trained successfully!" message
2. ✅ Note the version number
3. ✅ Go to Model Status tab
4. ✅ Click Refresh
5. ✅ Verify new metrics
6. ✅ Check Explainability tab
7. ✅ Click Refresh there too

### Regular Workflow
1. Train model
2. Refresh Model Status
3. Check metrics
4. Refresh Explainability
5. Check features
6. Compare with previous version
7. Decide to keep or rollback

---

## 🚀 Quick Reference

| Tab | Refresh Needed? | How to Refresh |
|-----|----------------|----------------|
| Model Training | ❌ No | Auto-updates |
| Model Versions | ❌ No | Auto-updates |
| Model Status | ✅ Yes | Click 🔄 button |
| Explainability | ✅ Yes | Click 🔄 button |
| Drift & Fairness | ✅ Yes | Click 🔄 button |
| Data Health | ✅ Yes | Click 🔄 button |
| Control Room | ⚠️ Maybe | Depends on data |
| Reports | ⚠️ Maybe | Depends on data |

---

## 💡 Pro Tips

1. **Bookmark Workflow:**
   - Train → Refresh Model Status → Refresh Explainability

2. **Use Browser Shortcuts:**
   - R key = Quick refresh
   - Ctrl+R = Force refresh

3. **Check Version:**
   - Model Status shows current version
   - Model Versions shows all versions

4. **Compare Before/After:**
   - Note metrics before training
   - Refresh after training
   - Compare the difference

---

## 🎉 Summary

✅ **Refresh buttons added** to all tabs
✅ **Clear instructions** after training
✅ **Version tracking** shows current model
✅ **Multiple refresh methods** available
✅ **Automatic fallback** to local files

**Just click 🔄 Refresh after training to see updates!**
