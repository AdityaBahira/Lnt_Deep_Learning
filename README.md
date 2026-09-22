# L&T Edutech Deep Learning Model Deployment & Integration
## End-to-End PyTorch Deep Health Risk Neural Network Platform

[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)](https://plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Repository Overview

This repository contains the complete implementation for the **Deep Learning Model Deployment & Integration** module. The project builds, trains, serves, and deploys a clinical decision-support platform powered by a pre-trained **PyTorch 3-Layer Deep Neural Network (`DeepHealthRiskNet`)**.

The system ingests 14 physiological and lifestyle metrics from `health_activity_data.csv` (1,002 patient records) to predict 4 clinical health risk categories (*Low Risk, Moderate Risk, High Risk, Critical Risk*).

---

### 📂 Repository Structure

```
Lnt_Deep_Learning/
├── README.md                                                  # Main Root Repository Documentation
├── Task_4_Developing_a_Flask_API_for_Deep_Learning_Models/  # Task 4: Production Flask REST API Service
│   ├── app.py                                                 # Flask Service Application & Endpoints
│   ├── model_loader.py                                        # PyTorch Model Loading Engine
│   ├── train_and_save_model.py                                # Neural Network Training Script
│   ├── health_activity_data.csv                               # 1,000-row Patient Dataset
│   ├── API_DOCUMENTATION.md                                   # REST API Specifications
│   └── saved_models/                                          # Trained Model Weights (dl_model.pt) & config.json
│
├── Task_6-Creating_a_Streamlit_User_Interface/               # Task 6: Single-Page Streamlit App
│   ├── app.py                                                 # Streamlit UI with Visual Icons & Emojis
│   ├── utils.py                                               # Dual-Mode Model Connector & Recommendations
│   ├── model_loader.py                                        # Local PyTorch Inference Engine
│   ├── requirements.txt                                       # Streamlit Dependencies
│   ├── Task_6_Streamlit_UI.ipynb                              # LMS Deliverable Notebook
│   ├── Task_6_Streamlit_UI_Report.docx                        # Technical Report (Academic Theme)
│   └── saved_models/                                          # Artifact Weights (dl_model.pt) & config.json
│
└── Task_7-Advanced_MultiPage_Streamlit_Application/           # Task 7: Multi-Page Enterprise App
    ├── app.py                                                 # Main Entry Point & st.navigation System
    ├── utils.py                                               # Multi-mode Connector & Dataset Analytics Engine
    ├── health_activity_data.csv                               # Patient Dataset (Un-modified)
    ├── model_loader.py                                        # PyTorch Model Engine
    ├── requirements.txt                                       # Dependencies Specs
    ├── build_task7_doc.py                                     # Academic Word Report Generator Script
    ├── Task_7_MultiPage_Streamlit_App.ipynb                   # LMS Submission Notebook
    ├── Task_7_MultiPage_Streamlit_UI_Report.docx              # Academic Technical Documentation
    ├── saved_models/                                          # Model Weights & Config
    └── pages/
        ├── 1_Overview.py                                      # 🏠 Executive Overview & Layer Inspector
        ├── 2_Prediction.py                                    # 🔮 Single Patient Predictor & Radar Chart
        ├── 3_Batch_Processing.py                              # 📁 Bulk Cohort Ingestion & Report Exporter
        ├── 4_Analytics.py                                     # 📊 Model Performance Dashboard (91.40% Acc)
        └── 5_System_Status.py                                 # ⚙️ REST API Health Probe & Benchmarker
```

---

### 🧠 Deep Learning Model Architecture (`DeepHealthRiskNet`)

The core neural network is a **3-Layer Artificial Neural Network** implemented in PyTorch:

```
Input Layer (14 Features) 
   │
   ▼
Linear(14 → 64) ──► BatchNorm1d(64) ──► ReLU() ──► Dropout(p=0.2)
   │
   ▼
Linear(64 → 32) ──► BatchNorm1d(32) ──► ReLU() ──► Dropout(p=0.2)
   │
   ▼
Linear(32 → 4)  ──► Softmax Activation
   │
   ▼
Output: 4 Class Probabilities [Low, Moderate, High, Critical Risk]
```

#### 📊 Input Features Schema (14 Numerical Features):
1. **Age**: Patient age in years.
2. **Height (cm)**: Patient height in centimeters.
3. **Weight (kg)**: Patient weight in kilograms.
4. **BMI**: Auto-calculated Body Mass Index ($kg/m^2$).
5. **Daily Steps**: Total step count per day.
6. **Calories Intake**: Caloric consumption ($kcal/day$).
7. **Hours of Sleep**: Sleep duration ($hours/night$).
8. **Heart Rate**: Resting heart rate ($bpm$).
9. **Systolic BP**: Systolic blood pressure ($mmHg$).
10. **Diastolic BP**: Diastolic blood pressure ($mmHg$).
11. **Exercise Hours**: Weekly exercise duration ($hours/week$).
12. **Alcohol Consumption**: Weekly alcohol intake ($units/week$).
13. **Smoker**: Binary indicator ($0 = No, 1 = Yes$).
14. **Diabetic**: Binary indicator ($0 = No, 1 = Yes$).

---

### 📊 Model Performance Summary

| Metric | Score | Details |
| :--- | :--- | :--- |
| **Overall Model Accuracy** | **91.40%** | Evaluated across 1,002 patient records in `health_activity_data.csv`. |
| **Macro Precision** | **91.80%** | High precision across all 4 risk classes. |
| **Macro Recall** | **91.20%** | Excellent sensitivity in detecting high-risk profiles. |
| **Macro F1-Score** | **91.15%** | Balanced harmonic mean performance. |
| **Inference Speed** | **< 2.0 ms** | Real-time PyTorch forward pass latency. |

---

### ⚙️ Quick Start & Running Instructions

#### 1. Running Task 6 (Single-Page App)
```bash
cd Task_6-Creating_a_Streamlit_User_Interface
pip install -r requirements.txt
python -m streamlit run app.py
```

#### 2. Running Task 7 (Multi-Page App)
```bash
cd Task_7-Advanced_MultiPage_Streamlit_Application
pip install -r requirements.txt
python -m streamlit run app.py
```

#### 3. Running Flask REST API Server (Task 4)
```bash
cd Task_4_Developing_a_Flask_API_for_Deep_Learning_Models
pip install -r requirements.txt
python app.py
```

---

### 🌐 Live Deployment Details

- **Streamlit Community Cloud Main Path**: `Task_7-Advanced_MultiPage_Streamlit_Application/app.py`
- **GitHub Repository**: [https://github.com/AdityaBahira/Lnt_Deep_Learning](https://github.com/AdityaBahira/Lnt_Deep_Learning)
