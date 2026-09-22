# Task 6: Creating a Streamlit User Interface
## Clinical Health Risk Deep Learning Platform

[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Plotly](https://img.shields.io/badge/Plotly-7.1.0-3F4F75?logo=plotly)](https://plotly.com/)

---

### 📖 Overview

**Task 6** provides a user-friendly Streamlit web application for real-time health risk classification powered by a pre-trained **PyTorch 3-Layer Neural Network (`DeepHealthRiskNet`)**.

The interface converts 14 patient metrics into risk assessments, confidence scores, probability breakdown charts, and clinical guidance.

---

### ✨ Key Features

- **Categorized Form Widgets with Icons**:
  - 👤 **Demographics**: Age 🎂, Height 📏, Weight ⚖️, Auto-calculating BMI Meter 🧮.
  - 🏃 **Daily Activity**: Steps 👟, Calories 🍎, Sleep 💤.
  - 🫀 **Vital Signs**: Heart Rate 💓, Systolic BP 🩸, Diastolic BP 🩺.
  - 🚬 **Lifestyle & Medical**: Exercise 🏋️, Alcohol 🍷, Smoker 🚬, Diabetic 🩹.
- **Dual Execution Engine**:
  - 🧠 **Direct PyTorch Engine**: Instant in-memory model loading (`dl_model.pt`).
  - 🌐 **Flask REST API Mode**: Endpoint querying (`http://127.0.0.1:5000/predict`).
- **Data Visualizations & Guidance**:
  - Dynamic risk badges (🟢 Low Risk, 🟡 Moderate Risk, 🟠 High Risk, 🔴 Critical Risk).
  - Interactive Plotly Softmax probability distribution bar chart.
  - Personalized clinical recommendations list.

---

### 🚀 Running the App

```bash
python -m streamlit run app.py
```
