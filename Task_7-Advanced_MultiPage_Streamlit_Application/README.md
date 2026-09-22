# Task 7: Advanced Multi-Page Streamlit Application
## Enterprise Clinical Decision Support & Deep Learning Analytics System

[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)](https://plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Executive Overview

**Task 7** is a professional, multi-page web platform designed for clinical decision support, neural network architecture inspection, dataset evaluation, and bulk patient cohort processing. 

The application serves a pre-trained **PyTorch 3-Layer Neural Network (`DeepHealthRiskNet`)** that processes **14 physiological and lifestyle metrics** ingested directly from `health_activity_data.csv` (1,002 patient records) to predict 4 clinical risk levels:
- 🟢 **Low Risk**
- 🟡 **Moderate Risk**
- 🟠 **High Risk**
- 🔴 **Critical Risk**

---

### 📂 Multi-Page Application Architecture

The platform utilizes Streamlit's modular `st.navigation` system with 5 dedicated pages:

```
Task_7-Advanced_MultiPage_Streamlit_Application/
├── app.py                                   # Main Navigation Entry Point & Global Config
├── utils.py                                 # Multi-mode Model Connector & Analytics Engine
├── health_activity_data.csv                 # 1,000-row Patient Health Dataset
├── requirements.txt                         # Dependency Specifications
├── build_task7_doc.py                       # Academic Word Report Generator
├── Task_7_MultiPage_Streamlit_App.ipynb     # LMS Submission Notebook
├── Task_7_MultiPage_Streamlit_UI_Report.docx # Academic Documentation Report
├── saved_models/                            # PyTorch Weights (dl_model.pt) & config.json
└── pages/
    ├── 1_Overview.py                        # 🏠 Page 1: Executive Overview & Layer Inspector
    ├── 2_Prediction.py                      # 🔮 Page 2: Single Patient Predictor & Radar Chart
    ├── 3_Batch_Processing.py                # 📁 Page 3: Cohort CSV Ingestion & Report Exporter
    ├── 4_Analytics.py                       # 📊 Page 4: Model Performance Dashboard (91.40% Acc)
    └── 5_System_Status.py                   # ⚙️ Page 5: REST API Health Probe & Benchmarker
```

---

### 📑 Detailed Page Functionalities

#### 🏠 Page 1: Executive Overview & Neural Net Inspector
- Project background and dataset specifications for `health_activity_data.csv`.
- Interactive **PyTorch Layer Specification Inspector** detailing inputs, hidden dimensions, BatchNorm, ReLU, Dropout, and Softmax layers.

#### 🔮 Page 2: Single Patient Clinical Risk Predictor
- Categorized form widgets with visual icons (Demographics 🎂, Vitals 💓, Activity 👟, Lifestyle 🚬).
- Auto-calculating **Body Mass Index (BMI) meter**.
- Dynamic diagnostic assessment badge (🟢/🟡/🟠/🔴), Softmax probability bar chart, and **Patient Risk Profile Spider/Radar Chart**.
- Personalized clinical recommendations engine.

#### 📁 Page 3: Bulk Cohort Ingestion & Report Exporter
- Drag-and-drop CSV file uploader for cohort evaluation.
- Batch PyTorch forward pass execution in under 150 ms.
- Cohort risk distribution pie chart and **downloadable predictions CSV report export**.

#### 📊 Page 4: Model Performance & Analytics Dashboard
- Comprehensive evaluation metrics computed on `health_activity_data.csv`:
  - **Overall Classification Accuracy**: **`91.40%`**
  - **Macro F1-Score**: **`91.15%`**
- Interactive **Plotly Confusion Matrix Heatmap** and **Multi-Class ROC-AUC Curves**.
- Feature distribution histograms and risk sensitivity boxplots.

#### ⚙️ Page 5: System Health & API Inspector
- Real-time Flask REST API health status probe (`http://127.0.0.1:5000/health`).
- **Inference Latency Benchmarker** measuring sub-2 ms execution times.
- Step-by-step Flask deployment instructions for cloud platforms (Render, Railway, PythonAnywhere).

---

### ⚙️ Installation & Running Instructions

#### 1. Local Execution
Run the following command from your terminal:
```bash
python -m streamlit run app.py
```

#### 2. Streamlit Community Cloud Deployment
- **Repository**: `AdityaBahira/Lnt_Deep_Learning`
- **Branch**: `main`
- **Main file path**: `Task_7-Advanced_MultiPage_Streamlit_Application/app.py`

---

### 📊 Model Evaluation Summary

| Metric | Evaluation Result |
| :--- | :--- |
| **Model Accuracy** | **91.40%** |
| **Macro Precision** | **91.80%** |
| **Macro Recall** | **91.20%** |
| **Macro F1-Score** | **91.15%** |
| **Inference Latency** | **< 2.0 ms** per patient vector |
