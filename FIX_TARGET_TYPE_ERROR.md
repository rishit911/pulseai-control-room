# 🔧 Fix: Target Type Error (Continuous vs Classification)

## Issue

**Error:**
```
ValueError: Unknown label type: 'continuous'
```

**What it means:**
You're trying to use a classification model (Random Forest, etc.) with a continuous numeric target variable. Classification models need discrete categories, not continuous numbers.

---

## Understanding the Problem

### Classification (✅ Supported)
**Target has discrete categories:**
- Yes/No
- A/B/C
- 0/1/2
- setosa/versicolor/virginica
- Pass/Fail

**Examples:**
```csv
# Good for classification
customer_id,age,income,will_buy
1,25,50000,Yes
2,35,75000,No
3,45,60000,Yes
```

### Regression (❌ Not Yet Supported)
**Target has continuous values:**
- House prices: $250,000, $350,000, $180,000
- Temperature: 72.5, 68.3, 75.1
- Sales: $1,234.56, $2,345.67

**Examples:**
```csv
# Not supported yet (regression)
house_id,bedrooms,sqft,price
1,3,1500,250000
2,4,2000,350000
3,2,1000,180000
```

---

## How to Fix

### Solution 1: Use Categorical Target

**If your target is naturally categorical:**
```csv
# Change from numbers to categories
Before: 0, 1, 2, 3, 4
After:  Low, Medium, High, Very High, Extreme
```

**Or keep numbers but ensure they're discrete classes:**
```csv
# Make sure it's classification
rating: 1, 2, 3, 4, 5  (only 5 unique values)
```

### Solution 2: Convert Continuous to Categories

**Bin continuous values into categories:**

```python
# Example: Convert house prices to categories
Low: < $200,000
Medium: $200,000 - $400,000
High: > $400,000
```

**In your CSV:**
```csv
Before:
house_id,price
1,250000
2,350000

After:
house_id,price_category
1,Medium
2,Medium
```

### Solution 3: Use Different Dataset

**Use one of our sample datasets:**
- ✅ Iris - Flower classification (3 categories)
- ✅ Customer Churn - Yes/No (2 categories)
- ✅ Adult Income - >50K/<=50K (2 categories)

---

## Detection in Dashboard

The dashboard now automatically detects your target type:

### ✅ Good Target (Classification)
```
✅ Categorical target (3 classes)
```
or
```
✅ Classification target (5 classes)
```

### ⚠️ Problematic Target (Regression)
```
⚠️ Continuous target (1000 unique values) - Regression not yet supported
💡 For classification, select a target with discrete categories
```

---

## Examples

### ✅ GOOD: Iris Dataset
```csv
sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
7.0,3.2,4.7,1.4,versicolor
6.3,3.3,6.0,2.5,virginica
```
**Target:** `species` (3 categories) ✅

### ✅ GOOD: Customer Churn
```csv
age,tenure,charges,churn
25,12,50.5,No
45,24,89.9,No
35,6,75.2,Yes
```
**Target:** `churn` (2 categories: Yes/No) ✅

### ❌ BAD: House Prices
```csv
bedrooms,sqft,price
3,1500,250000
4,2000,350000
2,1000,180000
```
**Target:** `price` (continuous values) ❌

**Fix:** Convert to categories:
```csv
bedrooms,sqft,price_range
3,1500,Medium
4,2000,High
2,1000,Low
```
**Target:** `price_range` (3 categories) ✅

---

## Quick Test

### Test with Iris Dataset:
1. Go to Model Training tab
2. Select "Iris (Flower Classification)"
3. Click "Load Sample Dataset"
4. Target: `species`
5. You'll see: ✅ Categorical target (3 classes)
6. Train → Works perfectly!

### Test with Your Data:
1. Upload your CSV
2. Select target column
3. Check the message:
   - ✅ Green = Good to go!
   - ⚠️ Yellow = Need to fix target

---

## Converting Continuous to Categorical

### Method 1: Manual Binning
```python
# In Excel or Python before upload
if value < 100: category = "Low"
elif value < 500: category = "Medium"
else: category = "High"
```

### Method 2: Quantile Binning
```python
# Split into equal-sized groups
Q1 (0-25%): "Low"
Q2 (25-50%): "Medium-Low"
Q3 (50-75%): "Medium-High"
Q4 (75-100%): "High"
```

### Method 3: Domain-Based
```python
# Use business logic
Temperature:
  < 60°F: "Cold"
  60-75°F: "Comfortable"
  > 75°F: "Hot"
```

---

## Future Support

**Coming Soon:**
- Regression models (Linear Regression, etc.)
- Automatic binning option
- Multi-output classification
- Time series forecasting

**For now:**
- Use classification models only
- Ensure target has discrete categories
- Maximum ~20 unique values recommended

---

## Summary

✅ **DO:**
- Use categorical targets (Yes/No, A/B/C)
- Use discrete numeric targets (1,2,3,4,5)
- Keep unique values under 20
- Use sample datasets to test

❌ **DON'T:**
- Use continuous numeric targets (prices, temperatures)
- Use targets with 100+ unique values
- Try regression problems (not supported yet)

---

**The dashboard now detects this automatically and shows helpful messages!** 🎉
