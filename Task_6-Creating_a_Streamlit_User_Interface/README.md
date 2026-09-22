# Task 6: Creating a Streamlit User Interface
## Clinical Health Risk Deep Learning Platform

[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)](https://plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Executive Overview

**Task 6** implements a user-friendly Streamlit web application for real-time clinical health risk classification. The platform connects to a pre-trained **PyTorch 3-Layer Neural Network (`DeepHealthRiskNet`)** and converts 14 patient physiological and lifestyle metrics into risk classifications, confidence scores, probability breakdown charts, and clinical guidance.

---

### 📂 Directory & Repository Structure

```
Task_6-Creating_a_Streamlit_User_Interface/
├── README.md                                  # Task 6 Documentation
├── app.py                                     # Main Streamlit UI with Visual Icons & Widgets
├── utils.py                                   # Dual-Mode Model Connector & Recommendations
├── model_loader.py                            # PyTorch Inference Engine Singleton
├── requirements.txt                           # Dependency Specifications
├── Task_6_Streamlit_UI.ipynb                  # LMS Deliverable Notebook
├── Task_6_Streamlit_UI_Report.docx            # Technical Documentation Report (Academic Theme)
└── saved_models/
    ├── dl_model.pt                            # PyTorch State Dict Model Weights
    └── config.json                            # Model Metadata, Labels & Normalization Stats
```

---

### ✨ Key Application Features

1. **Categorized Input Form Widgets with Emojis**:
   - 👤 **Demographics & Body Metrics**: Age 🎂, Height 📏, Weight ⚖️, Auto-calculating BMI Meter 🧮.
   - 🏃 **Daily Activity & Nutrition**: Daily Steps 👟, Calories 🍎, Sleep 💤.
   - 🫀 **Vital Signs**: Heart Rate 💓, Systolic BP 🩸, Diastolic BP 🩺.
   - 🚬 **Lifestyle & Medical**: Exercise 🏋️, Alcohol 🍷, Smoker 🚬, Diabetic 🩹.

2. **Dual Model Execution Engine**:
   - 🧠 **Direct PyTorch Engine**: In-memory PyTorch forward pass execution via `model_loader.py` without needing an external web server.
   - 🌐 **Flask REST API Mode**: Endpoint connection (`http://127.0.0.1:5000/predict`) with server health monitoring.

3. **Output Visualizations & Recommendations**:
   - Dynamic Risk Badges: 🟢 **Low Risk**, 🟡 **Moderate Risk**, 🟠 **High Risk**, 🔴 **Critical Risk**.
   - Interactive **Plotly Softmax Probability Distribution Bar Chart**.
   - Personalized **Clinical Guidance & Recommendations List**.

---

### 🧠 PyTorch Model Architecture Specs

```
Input Layer (14 Features) ──► Linear(14→64) ──► BatchNorm1d ──► ReLU ──► Dropout(0.2)
                           ──► Linear(64→32) ──► BatchNorm1d ──► ReLU ──► Dropout(0.2)
                           ──► Linear(32→4)  ──► Softmax ──► 4 Risk Classes
```

---

### ⚙️ Installation & Local Setup

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Launch Streamlit Application
```bash
python -m streamlit run app.py
```
