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
Frontend/task 7/
├── app.py                                   # Main Navigation Entry Point & Global Config
├── utils.py                                 # Multi-mode Model Connector & Analytics Engine
├── requirements.txt                         # Dependency Specifications
├── build_task7_doc.py                       # Academic Word Report Generator
├── Task_7_MultiPage_Streamlit_App.ipynb     # LMS Submission Notebook
├── Task_7_MultiPage_Streamlit_UI_Report.docx # Academic Documentation Report
└── pages/
    ├── 1_Overview.py                        # 🏠 Page 1: Executive Overview & Layer Inspector
    ├── 2_Prediction.py                      # 🔮 Page 2: Single Patient Predictor & Radar Chart
    ├── 3_Batch_Processing.py                # 📁 Page 3: Cohort CSV Ingestion & Report Exporter
    ├── 4_Analytics.py                       # 📊 Page 4: Model Performance Dashboard (91.40% Acc)
    └── 5_System_Status.py                   # ⚙️ Page 5: REST API Health Probe & Benchmarker
```

---

### ⚙️ Installation & Running Instructions

#### Local Execution
Run the following command from your terminal:
```bash
python -m streamlit run "Frontend/task 7/app.py"
```
