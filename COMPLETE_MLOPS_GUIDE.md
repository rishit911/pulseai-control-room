# Complete MLOps Platform - User Guide

## 🚀 Quick Start

### 1. Run the System
```bash
# Terminal 1: Start Dashboard
streamlit run MLOps_Engineer4/app/main.py

# Terminal 2: Start API
python MLOps_Engineer3/api/serve.py
```

### 2. Access the Platform
- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000

### 3. Train Your First Model
1. Go to **Model Training** tab
2. Upload your CSV file
3. Select features and target
4. Click **Train Model**
5. All dashboard sections update automatically ✨

## 📊 Platform Overview

### Complete MLOps Pipeline
```
Data Upload → Feature Selection → Model Training → Auto-Sync → Dashboard Updates
     ↓              ↓                  ↓             ↓            ↓
   CSV File    Choose Features    16 Algorithms   All JSON     Real-time
   Validation   & Target Type    Classification   Files        Monitoring
                                 & Regression     Updated
```

### Dashboard Sections
- **🏠 Control Room**: Real-time performance metrics
- **🤖 Model Training**: Upload data & train custom models
- **📦 Model Versioning**: Manage model versions
- **📊 Model Status**: Current model info & API health
- **📉 Drift & Fairness**: Monitor model drift & bias
- **🏥 Data Health**: Data quality monitoring
- **🔄 Recovery**: Deployment history
- **🔍 Explainability**: Feature importance
- **📈 Reports**: Performance analytics

## 🎯 Key Features

### ✅ Automatic Data Sync
- All 13 JSON files update after training
- No manual intervention needed
- Real-time dashboard updates

### ✅ Multi-Model Support
**Classification (7 algorithms):**
- Random Forest, Gradient Boosting
- Logistic Regression, SVM
- Decision Tree, K-Nearest Neighbors
- Naive Bayes

**Regression (9 algorithms):**
- Random Forest, Gradient Boosting
- Linear, Ridge, Lasso, ElasticNet
- SVM, Decision Tree, K-Nearest Neighbors

### ✅ Complete Integration
- Dashboard ↔ Model Training
- API ↔ Model Serving
- Monitoring ↔ Drift Detection
- Versioning ↔ Model Management

## 📋 Step-by-Step Usage

### Training a Model

#### Step 1: Upload Data
1. Go to **Model Training** tab
2. Click **Browse files** or drag & drop CSV
3. Data preview appears automatically
4. Verify data quality metrics

#### Step 2: Configure Training
1. **Select Target**: Choose column to predict
2. **Problem Type**: Auto-detected (classification/regression)
3. **Select Features**: Choose input columns
4. **Algorithm**: Pick from 16 available models
5. **Parameters**: Adjust hyperparameters (optional)

#### Step 3: Train & Deploy
1. Click **Train Model**
2. Watch training progress
3. View results and metrics
4. Model auto-deploys to API
5. Dashboard updates automatically

### Monitoring Your Model

#### Control Room
- **Success Rate**: Model performance (accuracy/R²)
- **Total Processed**: Training data size
- **System Health**: Performance-based status
- **Alerts**: Issue count

#### Drift & Fairness
- **Drift Detection**: Statistical tests on features
- **Feature Monitoring**: P-values and trends
- **Fairness Analysis**: Group-level performance
- **90-Day History**: Drift trends over time

#### Model Status
- **Current Version**: Active model info
- **Performance**: Latest metrics
- **API Health**: Serving status
- **Test Predictions**: Interactive testing

## 🔧 Troubleshooting

### Dashboard Shows Old Data
**Solution**: Click **🗑️ Clear Cache** button in any tab

### Data Upload Issues
**Common fixes**:
- Ensure CSV has headers
- Check for special characters
- Verify file isn't corrupted
- Try smaller file first

### Training Fails
**Check**:
- Target column has valid values
- Features are numeric (or will be encoded)
- Dataset has enough rows (>10 recommended)
- No excessive missing values

### API Not Responding
**Steps**:
1. Check if API is running (http://localhost:8000)
2. Restart API: `python MLOps_Engineer3/api/serve.py`
3. Check Model Status tab for connection

### Sync Issues
**Manual sync**: Run `python scripts/sync_control_room.py`

## 📊 Data Requirements

### File Format
- **Type**: CSV files only
- **Headers**: Required in first row
- **Encoding**: UTF-8 recommended
- **Size**: No strict limit (larger files take longer)

### Data Structure
- **Minimum**: 2 columns (1 feature + 1 target)
- **Recommended**: 10+ rows for reliable results
- **Features**: Numeric preferred (categorical auto-encoded)
- **Target**: Any type (auto-detected as classification/regression)

### Example Data Formats

#### Classification Example
```csv
age,income,education,target
25,50000,Bachelor,Yes
30,60000,Master,No
35,70000,PhD,Yes
```

#### Regression Example
```csv
size,bedrooms,location,price
1200,2,Urban,250000
1500,3,Suburban,300000
2000,4,Rural,350000
```

## 🎛️ Advanced Features

### Model Versioning
- Automatic version assignment
- Version comparison
- Rollback capability
- Metadata tracking

### API Integration
- RESTful endpoints
- Batch predictions
- Model reloading
- Health monitoring

### Monitoring Pipeline
- Drift detection algorithms
- Fairness analysis
- Performance tracking
- Alert generation

## 📈 Performance Metrics

### Classification Metrics
- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1 Score**: Harmonic mean of precision and recall

### Regression Metrics
- **R² Score**: Coefficient of determination
- **RMSE**: Root Mean Square Error
- **MAE**: Mean Absolute Error
- **MAPE**: Mean Absolute Percentage Error

## 🔄 System Architecture

### Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboard     │    │   Training      │    │   API Server    │
│   (Streamlit)   │◄──►│   Pipeline      │◄──►│   (FastAPI)     │
│   Port 8501     │    │   (MLOps_E1)    │    │   Port 8000     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sync     │    │   Monitoring    │    │   Model Store   │
│   (13 JSON)     │    │   (Drift/Fair)  │    │   (Artifacts)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow
1. **Upload**: CSV → Training Pipeline
2. **Process**: Feature selection → Model training
3. **Store**: Model → Artifacts + Versioning
4. **Sync**: Metrics → 13 JSON files
5. **Serve**: Model → API endpoints
6. **Monitor**: Performance → Drift detection
7. **Display**: Data → Dashboard tabs

## 🛠️ Development

### Project Structure
```
├── MLOps_Engineer1/          # Training Pipeline
│   ├── core/
│   │   ├── integration/      # Data sync system
│   │   ├── model_versioning.py
│   │   └── pipelines/
│   ├── artifacts/            # Model storage
│   └── data/
├── MLOps_Engineer2/          # Monitoring
│   ├── core/
│   └── artifacts/
├── MLOps_Engineer3/          # API Server
│   └── api/serve.py
├── MLOps_Engineer4/          # Dashboard
│   ├── app/
│   │   ├── tabs/            # Dashboard sections
│   │   └── main.py
│   └── data/                # JSON data files
└── scripts/                 # Utility scripts
```

### Key Files
- `MLOps_Engineer4/app/main.py` - Dashboard entry point
- `MLOps_Engineer3/api/serve.py` - API server
- `MLOps_Engineer1/core/integration/data_sync.py` - Sync system
- `MLOps_Engineer4/app/tabs/model_training.py` - Training interface

## 🎯 Best Practices

### Data Preparation
- Clean data before upload
- Handle missing values
- Ensure consistent formatting
- Use meaningful column names

### Model Training
- Start with simple algorithms
- Validate results make sense
- Check for overfitting
- Monitor performance metrics

### Production Usage
- Regular model retraining
- Monitor drift continuously
- Set up performance alerts
- Maintain model versions

## 🚨 Common Issues & Solutions

### Issue: "Model not found"
**Solution**: Train a model first using Model Training tab

### Issue: "API connection failed"
**Solution**: Start API server: `python MLOps_Engineer3/api/serve.py`

### Issue: "Data sync failed"
**Solution**: Run manual sync: `python scripts/sync_control_room.py`

### Issue: "Dashboard shows cached data"
**Solution**: Click 🗑️ Clear Cache button

### Issue: "File upload error"
**Solution**: Check CSV format, headers, and encoding

## 📞 Quick Commands

```bash
# Start dashboard
streamlit run MLOps_Engineer4/app/main.py

# Start API
python MLOps_Engineer3/api/serve.py

# Manual sync
python scripts/sync_control_room.py

# Check current model
python scripts/check_current_model.py

# Verify monitoring data
python scripts/check_monitoring_data.py
```

## 🎉 Success Checklist

### ✅ System Running
- [ ] Dashboard accessible at http://localhost:8501
- [ ] API accessible at http://localhost:8000
- [ ] Both services show no errors

### ✅ Model Training
- [ ] Can upload CSV files
- [ ] Feature selection works
- [ ] Model training completes
- [ ] Results display correctly

### ✅ Dashboard Integration
- [ ] Control Room shows real metrics
- [ ] Drift & Fairness monitors actual features
- [ ] Model Status displays current info
- [ ] All tabs load without errors

### ✅ API Integration
- [ ] Model Status shows "API Healthy"
- [ ] Test predictions work
- [ ] API endpoints respond

---

## 🎯 Summary

This MLOps platform provides:
- **Complete model lifecycle management**
- **Real-time monitoring and drift detection**
- **Automated data synchronization**
- **Production-ready API serving**
- **Interactive dashboard interface**

**Quick Start**: Upload CSV → Select features → Train model → Monitor performance

**Support**: All issues auto-resolve with cache clearing and data sync

**Status**: Production-ready ✅

---

*Last Updated: 2025-11-07*  
*Version: Complete Integration*