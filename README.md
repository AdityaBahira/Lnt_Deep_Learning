# L&T Edutech Deep Learning Project Portfolio
## End-to-End Deep Learning, Computer Vision, REST APIs & Streamlit Platform

[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)](https://plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Repository Overview

This repository contains the complete 7-task portfolio for the **L&T Edutech Deep Learning** curriculum. The project spans custom Convolutional Neural Networks (CNNs), transfer learning with ResNet, dataset preprocessing, production Flask REST API development, Postman API validation, single-page Streamlit interfaces, and advanced multi-page clinical decision platforms.

---

### 📂 Repository Structure & Tasks Overview

```
Lnt_Deep_Learning/
├── README.md                                                     # Master Repository Documentation & Task Index
│
├── Task 1: Building an Image Classification Model using CNN/     # Task 1: Custom CNN Architecture
│
├── Task 2: Transfer Learning using ResNet/                       # Task 2: Pre-trained ResNet Transfer Learning
│
├── Task 3: Dataset Preparation and Preprocessing for Deep Learning/ # Task 3: Data Ingestion & Scaling Pipelines
│
├── Task_4_Developing_a_Flask_API_for_Deep_Learning_Models/     # Task 4: PyTorch Flask REST API Service
│   ├── app.py                                                    # Production Flask API Server
│   ├── model_loader.py                                           # Model Inference Engine
│   ├── train_and_save_model.py                                   # DeepHealthRiskNet Training Pipeline
│   ├── health_activity_data.csv                                  # Patient Clinical Dataset (1,002 rows)
│   ├── API_DOCUMENTATION.md                                      # REST API Endpoint Specifications
│   └── saved_models/                                             # PyTorch Weights (dl_model.pt) & config.json
│
├── Task 5: API Testing and Validation using Postman_Curl/        # Task 5: Automated REST API Validation
│   ├── Task_5_Health_Risk_DL_API.postman_collection.json         # Postman Test Suite
│   ├── test_client.py                                            # Python Automated Test Runner
│   ├── Task_5_API_Testing_and_Validation_Report.pdf             # Validation Test Report
│   └── screenshots/                                              # Postman Execution Proof Screenshots
│
├── Task_6-Creating_a_Streamlit_User_Interface/                  # Task 6: Streamlit Interactive UI
│   ├── app.py                                                    # Icon-Rich Streamlit App with Live BMI
│   ├── utils.py                                                  # Dual-Mode Model Connector & Recommendations
│   ├── model_loader.py                                           # In-Memory PyTorch Engine
│   ├── Task_6_Streamlit_UI.ipynb                                 # LMS Deliverable Notebook
│   ├── Task_6_Streamlit_UI_Report.docx                           # Technical Documentation Report
│   └── saved_models/                                             # PyTorch Model Weights & Config
│
└── Task_7-Advanced_MultiPage_Streamlit_Application/              # Task 7: Multi-Page Enterprise App
    ├── app.py                                                    # st.navigation Entry Point & Global Config
    ├── utils.py                                                  # Multi-mode Connector & Analytics Engine
    ├── health_activity_data.csv                                  # Patient Master Dataset (Un-modified)
    ├── sample_cohort_data.csv                                    # Sample 50-Patient CSV for Batch Testing
    ├── model_loader.py                                           # PyTorch Model Engine
    ├── Task_7_MultiPage_Streamlit_App.ipynb                      # LMS Submission Notebook
    ├── Task_7_MultiPage_Streamlit_UI_Report.docx                 # Academic Documentation Report (91.40% Acc)
    ├── saved_models/                                             # PyTorch Model Artifacts
    └── views/
        ├── 1_Overview.py                                         # 🏠 Page 1: Overview & Layer Inspector
        ├── 2_Prediction.py                                       # 🔮 Page 2: Single Patient Predictor & Radar Chart
        ├── 3_Batch_Processing.py                                 # 📁 Page 3: Cohort CSV Ingestion & Report
        ├── 4_Analytics.py                                        # 📊 Page 4: Model Performance Dashboard
        └── 5_System_Status.py                                    # ⚙️ Page 5: REST API Health Probe & Benchmarker
```

---

### 📋 Complete Curriculum Tasks Table

| Task ID | Task Title | Key Focus & Technologies | Primary Artifacts |
| :--- | :--- | :--- | :--- |
| **Task 1** | **Building an Image Classification Model using CNN** | Custom Convolutional Neural Network, Feature Maps, Softmax | Jupyter Notebook & Training Code |
| **Task 2** | **Transfer Learning using ResNet** | Pre-trained ResNet Backbones, Feature Extraction, Fine-tuning | Transfer Learning Notebook & Evaluation |
| **Task 3** | **Dataset Preparation & Preprocessing** | Data Cleaning, Standard Scaling, Normalization Pipelines | Preprocessing Scripts & Processed Data |
| **Task 4** | **Developing a Flask API for DL Models** | Flask 3.1 REST API, PyTorch Model Serving, Gunicorn | `app.py`, `model_loader.py`, `config.json` |
| **Task 5** | **API Testing & Validation using Postman/cURL** | Postman Runner, HTTP Status Verification, Edge-Case Auditing | `.postman_collection.json`, Test Report |
| **Task 6** | **Creating a Streamlit User Interface** | Streamlit 1.64, Dual Engine (Direct/API), Live BMI, Emojis | `app.py`, `utils.py`, `Task_6_Report.docx` |
| **Task 7** | **Advanced Multi-Page Streamlit Application** | `st.navigation`, Confusion Matrix, ROC-AUC, 91.40% Accuracy | `views/`, `sample_cohort_data.csv`, `Task_7_Report.docx` |

---

### 🌐 Cloud Deployment Configuration
- **Streamlit Community Cloud Main File**: `Task_7-Advanced_MultiPage_Streamlit_Application/app.py`
- **GitHub Repository**: [https://github.com/AdityaBahira/Lnt_Deep_Learning](https://github.com/AdityaBahira/Lnt_Deep_Learning)
