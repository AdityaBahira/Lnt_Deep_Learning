# Task 6: Creating a Streamlit User Interface
## Interactive Clinical Decision Support powered by Direct PyTorch Neural Network

[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?logo=plotly)](https://plotly.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python)](https://www.python.org/)

---

### 📖 Executive Overview

**Task 6** implements a Streamlit clinical user interface for real-time health risk classification. The application operates as an intuitive clinical decision-support platform powered directly by an in-memory **PyTorch 3-Layer Deep Neural Network (`DeepHealthRiskNet`)**.

The model processes **14 physiological and lifestyle metrics** to classify patient health risk into 4 clinical categories:
- 🟢 **Low Risk**: Optimal physiological metrics with minimal clinical risk factors.
- 🟡 **Moderate Risk**: Mild indicators requiring lifestyle adjustments.
- 🟠 **High Risk**: Elevated blood pressure, BMI, or lifestyle risk markers requiring medical evaluation.
- 🔴 **Critical Risk**: Severe health risk parameters requiring immediate clinical intervention.

---

### 🌟 Key Features

1. **Direct PyTorch Inference Engine**: Executes in-memory forward pass with sub-millisecond latency.
2. **Categorized Clinical Form**: 14 user inputs organized into 4 logical categories:
   - 👤 **Demographics & Body Metrics**: Age, Height, Weight, Auto BMI
   - 🏃 **Daily Activity & Nutrition**: Daily Steps, Calories Intake, Hours of Sleep
   - 🫀 **Vital Signs**: Resting Heart Rate, Systolic BP, Diastolic BP
   - 🚬 **Lifestyle & Medical Pre-conditions**: Exercise, Alcohol, Smoker Flag, Diabetic Flag
3. **Dynamic Auto-Calculated BMI Meter**: Calculates Body Mass Index live with health category feedback.
4. **Interactive Plotly Probability Distribution**: Softmax probability breakdown across all 4 risk classes.
5. **Personalized Clinical Recommendations**: Automated guidance based on specific vital sign threshold breaches.
6. **Clinical Presets**: Instant load presets for Low Risk and Critical Risk patient profiles.

---

### 📂 Directory & File Structure
```
Task_6-Creating_a_Streamlit_User_Interface/
 ├── app.py # Main Streamlit UI Entry Point
 ├── utils.py # PyTorch Model Connector & Clinical Logic
 ├── requirements.txt # Dependency specifications
 ├── build_task6_doc.py # Academic Word/PDF Report Builder
 ├── Task_6_Streamlit_UI.ipynb # Jupyter Notebook Workflow & Test Runs
 ├── Task_6_Streamlit_UI_Report.docx # Word Report Document
 └── Task_6_Streamlit_UI_Report.pdf # Submitted PDF Report
```

---

### ⚙️ Installation & Running Instructions

1. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
2. **Launch Streamlit Application**:
   ```
   python -m streamlit run app.py
   ```
3. **Access Application: Open browser at**
   ```
   http://localhost:8501
   ```
   
