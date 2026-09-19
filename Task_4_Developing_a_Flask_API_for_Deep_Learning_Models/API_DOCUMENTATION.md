# Health Risk Deep Learning REST API - Documentation

## Project Overview
This document provides the complete API specification for the **Flask REST API** developed for **Task 4: Developing a Flask API for Deep Learning Models**.

The API imports and serves a pre-trained **PyTorch 3-Layer Deep Neural Network (`DeepHealthRiskNet`)** that performs clinical health risk classification across 4 risk categories based on 14 physiological and lifestyle metrics.

- **Framework**: Flask 3.1 & PyTorch 2.12
- **Host**: `http://127.0.0.1:5000` or `http://localhost:5000`
- **Supported Content-Type**: `application/json`
- **Pre-trained Model Artifacts**: `saved_models/dl_model.pt` & `saved_models/config.json`

---

## Endpoint Summary Table

| Method | Endpoint | Description | Request Body | Auth Required |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Root Info & Metadata | None | No |
| `GET` | `/health` | Server Health & Model Readiness | None | No |
| `POST` | `/predict` | Deep Learning Inference Endpoint | JSON Object | No |
| `GET` | `/docs` | Interactive HTML Documentation Page | None | No |

---

## Endpoint Specifications

### 1. Root Information Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns API service information, framework versions, and list of available endpoints.

#### Example Request
```bash
curl -X GET http://127.0.0.1:5000/
```

#### Example Response (200 OK)
```json
{
  "status": "success",
  "service_name": "Health Risk Deep Learning REST API",
  "version": "1.0.0",
  "framework": "Flask 3.1 & PyTorch 2.12",
  "description": "REST API exposing a trained PyTorch Deep Neural Network for clinical risk prediction.",
  "endpoints": {
    "GET /": "API Landing and System Info",
    "GET /health": "Server and Model Health Status",
    "POST /predict": "Deep Learning Inference Endpoint",
    "GET /docs": "Interactive HTML Documentation"
  },
  "timestamp": "2026-09-18T19:30:00.000Z"
}
```

---

### 2. Health & Readiness Probe Endpoint
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Verifies if the Flask server is running and if the PyTorch model inference engine is imported and loaded into memory.

#### Example Request
```bash
curl -X GET http://127.0.0.1:5000/health
```

#### Example Response (200 OK)
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "DeepHealthRiskNet",
  "device": "cpu",
  "feature_count": 14,
  "classes": {
    "0": "Low Risk",
    "1": "Moderate Risk",
    "2": "High Risk",
    "3": "Critical Risk"
  },
  "timestamp": "2026-09-18T19:30:00.000Z"
}
```

---

### 3. Deep Learning Prediction Endpoint
- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Description**: Accepts 14 numerical feature inputs per sample, preprocesses through standard scaling, executes neural network forward pass, and returns predicted class labels and softmax confidence scores.

#### Supported JSON Payload Formats

##### Format A: Single Sample Vector Array (`"features"`)
```json
{
  "features": [56.0, 164.0, 81.0, 30.72, 5134.0, 1796.0, 8.6, 102.0, 137.0, 72.0, 8.1, 7.0, 0.0, 0.0]
}
```

##### Format B: Batch Sample 2D Array (`"instances"`)
```json
{
  "instances": [
    [25.0, 199.0, 85.0, 31.14, 5131.0, 3256.0, 6.5, 104.0, 106.0, 79.0, 3.6, 7.0, 0.0, 0.0],
    [78.0, 172.0, 72.0, 32.46, 19532.0, 2216.0, 9.6, 95.0, 96.0, 86.0, 8.3, 2.0, 1.0, 1.0]
  ]
}
```

##### Format C: Key-Value Feature Mapping (`"data"`)
```json
{
  "data": {
    "age": 60,
    "height_cm": 157,
    "weight_kg": 63,
    "bmi": 29.37,
    "daily_steps": 17351,
    "calories_intake": 2556,
    "hours_of_sleep": 5.1,
    "heart_rate": 111,
    "systolic_bp": 100,
    "diastolic_bp": 64,
    "exercise_hours_per_week": 8.5,
    "alcohol_consumption_per_week": 8,
    "smoker": 1,
    "diabetic": 0
  }
}
```

#### Example cURL Command
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [56.0, 164.0, 81.0, 30.72, 5134.0, 1796.0, 8.6, 102.0, 137.0, 72.0, 8.1, 7.0, 0.0, 0.0]
  }'
```

#### Example Successful Response (200 OK)
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
  "timestamp": "2026-09-18T19:30:00.000Z"
}
```

---

## Model Importing Architecture

The Flask application imports pre-trained model artifacts dynamically via **`model_loader.py`**:
1. **`saved_models/dl_model.pt`**: Contains PyTorch model weights state dictionary.
2. **`saved_models/config.json`**: Contains feature input dimensions (`14`), class labels, mean array ($\mu$), and standard deviation array ($\sigma$).

### Model Engine Initialization (`model_loader.py`):
```python
from model_loader import get_model_engine

# Initialize singleton inference engine
engine = get_model_engine()
results = engine.predict([[56.0, 164.0, 81.0, 30.72, 5134.0, 1796.0, 8.6, 102.0, 137.0, 72.0, 8.1, 7.0, 0.0, 0.0]])
```
