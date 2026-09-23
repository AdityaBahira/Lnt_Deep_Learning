# Task 7: Advanced Multi-Page Streamlit Application
## Enterprise Clinical Decision Support, Cohort Batch Processing & Model Diagnostics

[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?logo=plotly)](https://plotly.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2%2B-F7931E?logo=scikit-learn)](https://scikit-learn.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Executive Overview

**Task 7** expands the clinical decision support platform into a full-scale, multi-page application using Streamlit's `st.navigation` architecture. 

The platform ingests un-modified patient records directly from `health_activity_data.csv` (1,002 patient records) and evaluates the pre-trained **PyTorch 3-Layer Deep Neural Network (`DeepHealthRiskNet`)** across single-patient predictions, batch cohort processing, model analytics, and neural net diagnostics.

---

### 📂 Multi-Page Application Architecture

The application is structured into 5 modular pages configured via `views/`:
```
Task_7-Advanced_MultiPage_Streamlit_Application/
  ├── app.py # Main Navigation Entry Point & Sidebar Config
  ├── utils.py # Direct Model Connector & Analytics Engine
  ├── sample_cohort_data.csv # Sample CSV dataset for batch upload testing
  ├── requirements.txt # Dependency specifications ├── build_task7_doc.py # Academic Word/PDF Report Generator
  ├── Task_7_MultiPage_Streamlit_App.ipynb # Jupyter Notebook Implementation
  ├── Task_7_MultiPage_Streamlit_UI_Report.pdf # Submitted PDF Report
  └── views/
        ├── 1_Overview.py # 🏠 Page 1: Executive Overview & Layer Inspector
        ├── 2_Prediction.py # 🔮 Page 2: Single Patient Predictor & Radar Chart
        ├── 3_Batch_Processing.py # 📁 Page 3: Cohort CSV Ingestion & Report Exporter
        ├── 4_Analytics.py # 📊 Page 4: Model Performance Dashboard (91.40% Acc)
        └── 5_System_Status.py # ⚙️ Page 5: PyTorch Model Health & Diagnostics
```

---

### 📄 Summary of Pages

1. **Page 1 (Executive Overview & Neural Net)**: Overview of dataset feature specifications (14 features) and layer-by-layer specification of `DeepHealthRiskNet`.
2. **Page 2 (Single Patient Clinical Predictor)**: Interactive form widgets with dynamic BMI calculation, Plotly softmax probability bar chart, metric spider chart, and personalized clinical recommendations.
3. **Page 3 (Cohort CSV Ingestion & Report)**: Drag-and-drop CSV uploader for batch cohort inference, high-risk patient flags, summary risk distribution pie charts, and downloadable CSV reports.
4. **Page 4 (Model Performance Dashboard)**: Comprehensive evaluation dashboard displaying confusion matrix heatmap, multi-class ROC-AUC curves, feature histograms, and overall 91.40% classification accuracy.
5. **Page 5 (System Health & Diagnostics)**: In-memory PyTorch model health probe, latency benchmarker across 10 sample iterations, and neural network specification tables.

---

### ⚙️ Installation & Running Instructions

1. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
2. **Launch Multi-Page Streamlit Application**:
   ```
   python -m streamlit run app.py
   ```
3. Access Application: Open browser at `http://localhost:8501` and navigate using the sidebar menu
