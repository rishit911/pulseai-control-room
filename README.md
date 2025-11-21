# MLOps Control Room Platform

A complete MLOps platform for model training, monitoring, and deployment with real-time dashboard integration.

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

## 📊 Key Features

- ✅ **16 ML Algorithms** (Classification & Regression)
- ✅ **Real-time Dashboard** with 9 integrated sections
- ✅ **Automatic Data Sync** across all components
- ✅ **Model Versioning** with rollback capability
- ✅ **Drift Detection** and fairness monitoring
- ✅ **API Serving** with health monitoring
- ✅ **Interactive Training** with custom data upload

## 🎯 What's Included

### Dashboard Sections
- **Control Room**: Real-time performance metrics
- **Model Training**: Upload data & train custom models
- **Model Versioning**: Manage model versions
- **Model Status**: Current model info & API health
- **Drift & Fairness**: Monitor model drift & bias
- **Data Health**: Data quality monitoring
- **Recovery**: Deployment history
- **Explainability**: Feature importance
- **Reports**: Performance analytics

### Complete Integration
- All 13 JSON data files sync automatically
- Dashboard updates in real-time after training
- API serves latest trained models
- Monitoring tracks actual model features
- No manual data management needed

## 📚 Documentation

- **📖 [COMPLETE_MLOPS_GUIDE.md](COMPLETE_MLOPS_GUIDE.md)** - Complete user guide
- **📁 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Clean project structure

## 🎉 Success Status

```
✅ Dashboard Integration: 100% Complete
✅ Auto-sync System: Fully Functional
✅ Model Training: 16 Algorithms Supported
✅ API Integration: Real-time Serving
✅ Monitoring: Drift & Fairness Tracking
✅ Documentation: Comprehensive Guide
```

## 🔧 System Requirements

- Python 3.8+
- Required packages (auto-installed)
- 2 terminal windows for full system
- Web browser for dashboard access

## 🚨 Quick Troubleshooting

### Dashboard Shows Old Data
**Solution**: Click **🗑️ Clear Cache** button in any tab

### Data Upload Issues
**Solution**: Ensure CSV has headers and valid format

### API Not Responding
**Solution**: Start API with `python MLOps_Engineer3/api/serve.py`

### Manual Data Sync
**Solution**: Run `python scripts/sync_control_room.py`

---

**🚀 Ready to use! Follow the Quick Start above and see the complete guide for detailed instructions.**

## Tech Stack

<p align="left">
  <img alt="Python"        src="https://cdn.simpleicons.org/python"            width="48" />
  <img alt="Streamlit"     src="https://cdn.simpleicons.org/streamlit"         width="48" />
  <img alt="Plotly"        src="https://cdn.simpleicons.org/plotly"            width="48" />
  <img alt="Pandas"        src="https://cdn.simpleicons.org/pandas"            width="48" />
  <img alt="NumPy"         src="https://cdn.simpleicons.org/numpy"             width="48" />
  <img alt="FastAPI"       src="https://cdn.simpleicons.org/fastapi"           width="48" />
  <img alt="MLflow"        src="https://cdn.simpleicons.org/mlflow"            width="48" />
  <img alt="Scikit-learn"  src="https://cdn.simpleicons.org/scikitlearn"       width="48" />
</p>