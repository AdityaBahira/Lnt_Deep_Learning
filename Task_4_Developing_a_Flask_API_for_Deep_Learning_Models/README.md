# Deep Learning REST API Backend (`DL_deploy/Backend`)

## Overview
This backend service exposes a pre-trained **PyTorch Deep Neural Network (`DeepHealthRiskNet`)** as a production-ready **Flask REST API**. It loads serialized model weights (`saved_models/dl_model.pt`) and normalization parameters (`saved_models/config.json`), preprocesses 14 clinical and lifestyle feature inputs using standard scaling, executes neural network forward pass inference, and returns predicted health risk classifications with softmax confidence scores.

---

## 📁 Directory Structure
```text
e:/DL_deploy/Backend/
├── app.py                             # Main Flask REST API Server
├── model_loader.py                    # Thread-safe PyTorch Inference Engine & Model Import Wrapper
├── test_client.py                     # Automated HTTP Test Suite
├── API_DOCUMENTATION.md               # Complete API Specification for Frontend Integration
├── Task_4_Flask_API_DL_Submission.pdf # Assignment Submission Report
├── requirements.txt                   # Python Dependencies
├── README.md                          # Project Documentation
├── sample_outputs.json                # API Output Test Results Log
├── health_activity_data.csv           # Clinical Health Dataset (1,000 Records)
└── saved_models/                      # Serialized Pre-Trained Model Artifacts
    ├── dl_model.pt                    # PyTorch Weights State Dictionary
    └── config.json                    # Feature Means, Standard Deviations & Class Labels
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup
Navigate to the `Backend` directory and install dependencies:

```bash
cd e:\DL_deploy\Backend
pip install -r requirements.txt
```

### 2. Model Importing & Initialization
The API automatically imports pre-trained model weights and feature configuration upon server startup via `model_loader.py`:
* **Model State Dict**: `saved_models/dl_model.pt`
* **Configuration & Normalization Stats**: `saved_models/config.json`

### 3. Start the Flask REST API Server
Launch the backend API server:

```bash
python app.py
```
The API server will run locally at **`http://127.0.0.1:5000`**.

### 4. Run Automated Test Suite
In a separate terminal window:

```bash
python test_client.py
```

---

## 🌐 API Endpoints Reference

| Method | Endpoint | Description | Content-Type |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | System Metadata & API Info | `application/json` |
| `GET` | `/health` | Server & Model Readiness Probe | `application/json` |
| `POST` | `/predict` | Deep Learning Model Inference Endpoint | `application/json` |
| `GET` | `/docs` | Interactive Web Documentation Interface | `text/html` |

---

## 💻 Sample Payload & Request Format (`POST /predict`)

### Request Body Format (14 Features):
```json
{
  "features": [56.0, 164.0, 81.0, 30.72, 5134.0, 1796.0, 8.6, 102.0, 137.0, 72.0, 8.1, 7.0, 0.0, 0.0]
}
```

### Response Body Format (HTTP 200 OK):
```json
{
  "status": "success",
  "predictions_count": 1,
  "predictions": [
    {
      "sample_index": 0,
      "input_features": {
        "age": 56.0,
        "height_cm": 164.0,
        "weight_kg": 81.0,
        "bmi": 30.72,
        "daily_steps": 5134.0,
        "calories_intake": 1796.0,
        "hours_of_sleep": 8.6,
        "heart_rate": 102.0,
        "systolic_bp": 137.0,
        "diastolic_bp": 72.0,
        "exercise_hours_per_week": 8.1,
        "alcohol_consumption_per_week": 7.0,
        "smoker": 0.0,
        "diabetic": 0.0
      },
      "predicted_class_id": 1,
      "predicted_label": "Moderate Risk",
      "confidence_score": 0.8942,
      "class_probabilities": {
        "Low Risk": 0.0215,
        "Moderate Risk": 0.8942,
        "High Risk": 0.0712,
        "Critical Risk": 0.0131
      }
    }
  ],
  "latency_ms": 2.15,
  "model_name": "DeepHealthRiskNet",
  "timestamp": "2026-09-18T19:30:00Z"
}
```

---

## 📄 Documentation Reference for Frontend Development
For full specification of status codes (`400`, `404`, `405`, `415`, `422`, `500`) and payload integration guidelines, refer to **[API_DOCUMENTATION.md](file:///e:/DL_deploy/Backend/API_DOCUMENTATION.md)**.
