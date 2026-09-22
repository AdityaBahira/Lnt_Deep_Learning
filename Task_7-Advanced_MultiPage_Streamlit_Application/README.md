# Task 7: Advanced Multi-Page Streamlit Application
## Enterprise Clinical Decision Support & Deep Learning Analytics System

[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.1-F7931E?logo=scikitlearn)](https://scikit-learn.org/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Executive Overview

**Task 7** is an enterprise-grade multi-page web application designed for clinical decision support, PyTorch model architecture inspection, dataset performance analytics, and bulk cohort processing. 

The application serves a pre-trained **PyTorch 3-Layer Neural Network (`DeepHealthRiskNet`)** that processes **14 physiological and lifestyle metrics** ingested directly from `health_activity_data.csv` (1,002 patient records) to predict 4 clinical risk categories:
- 🟢 **Low Risk**
- 🟡 **Moderate Risk**
- 🟠 **High Risk**
- 🔴 **Critical Risk**

---

### 📂 Repository & Application Structure

```
Task_7-Advanced_MultiPage_Streamlit_Application/
├── README.md                                  # Task 7 Comprehensive Documentation
├── app.py                                     # Main Entry Point & st.navigation Multi-Page Config
├── utils.py                                   # Multi-mode Model Connector & Dataset Analytics Engine
├── health_activity_data.csv                   # Patient Dataset (1,002 records - Un-modified)
├── model_loader.py                            # PyTorch Inference Engine Singleton
├── requirements.txt                           # Dependency Specifications
├── build_task7_doc.py                         # Academic Word Report Generator Script
├── Task_7_MultiPage_Streamlit_App.ipynb       # LMS Submission Jupyter Notebook
├── Task_7_MultiPage_Streamlit_UI_Report.docx  # Technical Documentation (Academic Slate Navy Theme)
├── saved_models/                              # PyTorch Model Weights (dl_model.pt) & config.json
└── views/
    ├── 1_Overview.py                          # 🏠 Page 1: Executive Overview & Layer Inspector
    ├── 2_Prediction.py                        # 🔮 Page 2: Single Patient Predictor & Radar Chart
    ├── 3_Batch_Processing.py                  # 📁 Page 3: Cohort CSV Ingestion & Report Exporter
    ├── 4_Analytics.py                         # 📊 Page 4: Model Performance Dashboard (91.40% Acc)
    └── 5_System_Status.py                     # ⚙️ Page 5: REST API Health Probe & Benchmarker
```

---

### 📑 Modular Views Specifications

#### 🏠 Page 1: Executive Overview & Layer Inspector (`views/1_Overview.py`)
- Project background and dataset specs for `health_activity_data.csv`.
- Interactive **PyTorch Layer Specification Inspector** detailing input dimensions, linear layers, BatchNorm1d, ReLU, Dropout (0.2), and Softmax.

#### 🔮 Page 2: Single Patient Clinical Risk Predictor (`views/2_Prediction.py`)
- Categorized form widgets with visual icons (Demographics 🎂, Vitals 💓, Activity 👟, Lifestyle 🚬).
- Auto-calculating **BMI meter**.
- Diagnostic assessment badge (🟢/🟡/🟠/🔴), Softmax probability bar chart, and **Patient Risk Profile Spider/Radar Chart**.

#### 📁 Page 3: Cohort CSV Ingestion & Report Exporter (`views/3_Batch_Processing.py`)
- Drag-and-drop CSV file uploader for cohort evaluation.
- Batch PyTorch forward pass execution in under 150 ms.
- Summary risk distribution pie chart and **downloadable predictions CSV report export**.

#### 📊 Page 4: Model Performance Dashboard (`views/4_Analytics.py`)
- Comprehensive dataset evaluation metrics computed on `health_activity_data.csv`:
  - **Overall Classification Accuracy**: **`91.40%`**
  - **Macro F1-Score**: **`91.15%`**
- Interactive **Plotly Confusion Matrix Heatmap** and **Multi-Class ROC-AUC Curves**.
- Feature distribution histograms and risk sensitivity boxplots.

#### ⚙️ Page 5: System Health & API Inspector (`views/5_System_Status.py`)
- Real-time Flask REST API health probe (`http://127.0.0.1:5000/health`).
- **Inference Latency Benchmarker** measuring sub-2 ms execution times.
- Step-by-step REST API documentation table.

---

### 📊 Model Performance Metrics

| Metric | Score | Details |
| :--- | :--- | :--- |
| **Classification Accuracy** | **91.40%** | Measured across all 1,002 patient records in `health_activity_data.csv`. |
| **Macro Precision** | **91.80%** | High precision across all 4 risk classes. |
| **Macro Recall** | **91.20%** | High sensitivity in detecting critical profiles. |
| **Macro F1-Score** | **91.15%** | Balanced harmonic mean performance. |
| **Inference Latency** | **< 2.0 ms** | Real-time PyTorch forward pass execution speed. |

---

### ⚙️ Installation & Deployment Instructions

#### 1. Local Setup
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

#### 2. Deploying to Streamlit Community Cloud
- **Repository**: `AdityaBahira/Lnt_Deep_Learning`
- **Branch**: `main`
- **Main file path**: `Task_7-Advanced_MultiPage_Streamlit_Application/app.py`
