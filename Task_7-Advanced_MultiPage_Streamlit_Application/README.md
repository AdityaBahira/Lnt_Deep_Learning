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
