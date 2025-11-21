# 🎉 NEW: Regression Support Added!

## Overview

The Model Training Studio now supports **both Classification AND Regression**! Train models to predict continuous values like prices, temperatures, sales, etc.

---

## 🆕 What's New

### Regression Models Added:
1. **Random Forest Regressor** - Ensemble method, robust
2. **Gradient Boosting Regressor** - High accuracy
3. **Linear Regression** - Simple, interpretable
4. **Ridge Regression** - Linear with L2 regularization
5. **Lasso Regression** - Linear with L1 regularization (feature selection)
6. **ElasticNet** - Combines Ridge and Lasso
7. **Support Vector Regressor (SVR)** - Non-linear patterns
8. **Decision Tree Regressor** - Interpretable
9. **K-Nearest Neighbors Regressor** - Simple patterns

### Regression Metrics:
- **R² Score** - Model fit quality (1.0 = perfect)
- **RMSE** - Root Mean Squared Error
- **MAE** - Mean Absolute Error
- **MAPE** - Mean Absolute Percentage Error

### Visualizations:
- **Predictions vs Actual** scatter plot
- **Residuals distribution** histogram
- **Feature importance** (for tree-based models)

---

## 📊 Problem Type Detection

The dashboard automatically detects whether your problem is classification or regression:

### Classification (Discrete Categories)
```
Target: species → setosa, versicolor, virginica
Result: ✅ Classification - Categorical target (3 classes)
Models: Random Forest, Logistic Regression, etc.
```

### Regression (Continuous Values)
```
Target: price → 250000, 350000, 180000
Result: 📊 Regression - Continuous target (20 unique values)
Models: Random Forest Regressor, Linear Regression, etc.
```

---

## 🚀 Quick Start - Regression

### Example: House Price Prediction

1. **Load Sample Data**
   - Select "House Prices (Regression)"
   - Click "Load Sample Dataset"

2. **Configure**
   - Target: `price`
   - Features: `bedrooms`, `bathrooms`, `sqft`, `age_years`, `garage`

3. **Select Model**
   - Choose "Random Forest" (automatically uses Regressor)
   - Or try "Linear Regression" for simplicity

4. **Train**
   - Click "Train Model"
   - See regression metrics!

5. **Results**
   - R² Score: How well model fits (higher = better)
   - RMSE: Average prediction error
   - Predictions vs Actual plot
   - Residuals distribution

---

## 📈 Regression Models Guide

### 1. Random Forest Regressor
**Best for:** General purpose, robust predictions

**Parameters:**
- Number of Trees: 10-500 (default: 100)
- Max Depth: 1-50 (default: 10)
- Min Samples Split: 2-20 (default: 2)

**Use when:** You want reliable predictions without much tuning

---

### 2. Gradient Boosting Regressor
**Best for:** Maximum accuracy, complex patterns

**Parameters:**
- Number of Estimators: 10-500 (default: 100)
- Learning Rate: 0.01-1.0 (default: 0.1)
- Max Depth: 1-20 (default: 3)

**Use when:** You need the best possible predictions

---

### 3. Linear Regression
**Best for:** Simple relationships, interpretability

**Parameters:** None (uses defaults)

**Use when:** You want to understand feature relationships

---

### 4. Ridge Regression
**Best for:** Linear relationships with regularization

**Parameters:**
- Alpha: 0.01-10.0 (default: 1.0) - Higher = more regularization
- Solver: auto, svd, cholesky, lsqr

**Use when:** You have multicollinearity in features

---

### 5. Lasso Regression
**Best for:** Feature selection, sparse models

**Parameters:**
- Alpha: 0.01-10.0 (default: 1.0)
- Max Iterations: 100-10000 (default: 1000)

**Use when:** You want automatic feature selection

---

### 6. ElasticNet
**Best for:** Combines Ridge and Lasso benefits

**Parameters:**
- Alpha: 0.01-10.0 (default: 1.0)
- L1 Ratio: 0.0-1.0 (default: 0.5) - 0=Ridge, 1=Lasso
- Max Iterations: 100-10000 (default: 1000)

**Use when:** You want both regularization and feature selection

---

### 7. Support Vector Regressor (SVR)
**Best for:** Non-linear patterns, small datasets

**Parameters:**
- C: 0.1-10.0 (default: 1.0)
- Kernel: rbf, linear, poly, sigmoid
- Gamma: scale, auto

**Use when:** You have complex non-linear relationships

---

### 8. Decision Tree Regressor
**Best for:** Interpretable predictions

**Parameters:**
- Max Depth: 1-50 (default: 10)
- Min Samples Split: 2-20 (default: 2)

**Use when:** You need explainable predictions

---

### 9. K-Nearest Neighbors Regressor
**Best for:** Simple patterns, local predictions

**Parameters:**
- Number of Neighbors: 1-50 (default: 5)
- Weights: uniform, distance

**Use when:** Similar instances have similar values

---

## 📊 Understanding Regression Metrics

### R² Score (Coefficient of Determination)
- **Range:** -∞ to 1.0
- **Interpretation:**
  - 1.0 = Perfect predictions
  - 0.8-0.9 = Very good
  - 0.6-0.8 = Good
  - 0.4-0.6 = Moderate
  - < 0.4 = Poor
  - < 0.0 = Worse than baseline

### RMSE (Root Mean Squared Error)
- **Range:** 0 to ∞
- **Interpretation:**
  - Lower is better
  - Same units as target variable
  - Penalizes large errors more
  - Example: RMSE of $50,000 for house prices

### MAE (Mean Absolute Error)
- **Range:** 0 to ∞
- **Interpretation:**
  - Lower is better
  - Average absolute error
  - More robust to outliers than RMSE
  - Example: MAE of $30,000 for house prices

### MAPE (Mean Absolute Percentage Error)
- **Range:** 0% to ∞
- **Interpretation:**
  - Lower is better
  - Percentage error
  - Easy to understand
  - Example: MAPE of 10% = predictions off by 10% on average

---

## 🎯 Use Cases

### House Price Prediction
```csv
Features: bedrooms, bathrooms, sqft, age, location
Target: price
Model: Random Forest Regressor or Gradient Boosting
```

### Sales Forecasting
```csv
Features: marketing_spend, season, day_of_week, promotions
Target: sales_amount
Model: Gradient Boosting Regressor
```

### Temperature Prediction
```csv
Features: humidity, pressure, wind_speed, time_of_day
Target: temperature
Model: Random Forest Regressor
```

### Stock Price Prediction
```csv
Features: volume, open, high, low, indicators
Target: close_price
Model: Gradient Boosting Regressor
```

### Energy Consumption
```csv
Features: temperature, hour, day_type, occupancy
Target: kwh_consumed
Model: Random Forest Regressor
```

---

## 📝 Example Workflow

### Predicting House Prices:

1. **Load Data**
   ```
   Select: "House Prices (Regression)"
   Click: "Load Sample Dataset"
   ```

2. **Explore**
   ```
   Check data preview
   View statistics
   Verify target is continuous
   ```

3. **Configure**
   ```
   Target: price
   Features: bedrooms, bathrooms, sqft, age_years, garage
   ```

4. **Select Model**
   ```
   Model: Random Forest
   Parameters: Default (100 trees, depth 10)
   Test Size: 20%
   ```

5. **Train**
   ```
   Click: "Train Model"
   Wait: ~5 seconds
   ```

6. **Analyze Results**
   ```
   R² Score: 0.85 (Good fit!)
   RMSE: $45,000 (Average error)
   MAE: $32,000 (Typical error)
   MAPE: 12% (12% off on average)
   ```

7. **Visualize**
   ```
   Predictions vs Actual: Points near diagonal = good
   Residuals: Centered at 0 = unbiased
   Feature Importance: sqft most important
   ```

8. **Deploy**
   ```
   Model auto-saved
   API auto-reloaded
   Ready for predictions!
   ```

---

## 🔄 Classification vs Regression

| Aspect | Classification | Regression |
|--------|---------------|------------|
| **Target** | Categories | Continuous numbers |
| **Examples** | Yes/No, A/B/C | Prices, temperatures |
| **Models** | Logistic, Naive Bayes | Linear, Ridge |
| **Metrics** | Accuracy, Precision | R², RMSE, MAE |
| **Output** | Class label | Numeric value |
| **Visualization** | Confusion matrix | Scatter plot |

---

## 💡 Tips for Regression

### Data Preparation
1. **Scale features** if using Linear/Ridge/Lasso
2. **Remove outliers** that skew predictions
3. **Handle missing values** appropriately
4. **Create interaction features** for better fit

### Model Selection
1. **Start simple:** Try Linear Regression first
2. **Add complexity:** Move to Random Forest
3. **Optimize:** Try Gradient Boosting
4. **Compare:** Check R² and RMSE

### Improving Performance
1. **Feature engineering:** Create new features
2. **Hyperparameter tuning:** Adjust parameters
3. **More data:** Collect additional samples
4. **Ensemble:** Combine multiple models

---

## 🎉 Summary

✅ **9 Regression Models** added
✅ **4 Regression Metrics** displayed
✅ **2 Visualizations** for analysis
✅ **Auto-detection** of problem type
✅ **Sample dataset** included
✅ **Full integration** with dashboard

**You can now train both classification AND regression models!** 🚀

---

**Try it now with the House Prices dataset!**
