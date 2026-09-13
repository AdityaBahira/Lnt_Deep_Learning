# Health Risk Deep Learning REST API - Documentation

## Project Overview
This document provides the complete API specification for the **Flask REST API** developed for **Task 4: Developing a Flask API for Deep Learning Models**.

The API exposes a trained **PyTorch 3-Layer Deep Neural Network (`DeepHealthRiskNet`)** that performs clinical health risk classification across 4 risk categories based on 8 input physiological metrics.

- **Framework**: Flask 3.1 & PyTorch 2.12
- **Host**: `http://127.0.0.1:5000` or `http://localhost:5000`
- **Supported Content-Type**: `application/json`

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
  "timestamp": "2026-09-13T09:48:17.340Z"
}
```

---

### 2. Health & Readiness Probe Endpoint
- **URL**: `/health`
- **Method**: `GET`
- **Description**: Verifies if the Flask server is running and if the PyTorch model inference engine is loaded in memory.

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
  "feature_count": 8,
  "classes": {
    "0": "Low Risk",
    "1": "Moderate Risk",
    "2": "High Risk",
    "3": "Critical Risk"
  },
  "timestamp": "2026-09-13T09:48:17.345Z"
}
```

---

### 3. Deep Learning Prediction Endpoint
- **URL**: `/predict`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Description**: Accepts 8 numerical feature inputs per sample, preprocesses through standard scaling, executes neural network forward pass, and returns predicted class labels and softmax confidence scores.

#### Supported JSON Payload Formats

##### Format A: Single Sample Vector Array (`"features"`)
```json
{
  "features": [52.0, 28.4, 138.0, 145.0, 235.0, 80.0, 3.0, 6.5]
}
```

##### Format B: Batch Sample 2D Array (`"instances"`)
```json
{
  "instances": [
    [25.0, 21.0, 110.0, 85.0, 160.0, 65.0, 10.0, 8.0],
    [72.0, 34.5, 160.0, 195.0, 290.0, 92.0, 1.0, 5.0]
  ]
}
```

##### Format C: Key-Value Feature Mapping (`"data"`)
```json
{
  "data": {
    "age": 60,
    "bmi": 31.2,
    "blood_pressure": 145,
    "glucose_level": 165,
    "cholesterol": 250,
    "heart_rate": 84,
    "physical_activity_hours": 2,
    "sleep_hours": 6
  }
}
```

#### Example cURL Command
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [52.0, 28.4, 138.0, 145.0, 235.0, 80.0, 3.0, 6.5]
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
        "age": 52.0,
        "bmi": 28.4,
        "blood_pressure": 138.0,
        "glucose_level": 145.0,
        "cholesterol": 235.0,
        "heart_rate": 80.0,
        "physical_activity_hours": 3.0,
        "sleep_hours": 6.5
      },
      "predicted_class_id": 2,
      "predicted_label": "High Risk",
      "confidence_score": 0.8842,
      "class_probabilities": {
        "Low Risk": 0.0085,
        "Moderate Risk": 0.0941,
        "High Risk": 0.8842,
        "Critical Risk": 0.0132
      }
    }
  ],
  "latency_ms": 1.85,
  "model_name": "DeepHealthRiskNet",
  "timestamp": "2026-09-13T09:48:17.350Z"
}
```

---

## Exception & Error Handling Matrix

The API implements centralized error handlers returning standardized JSON error bodies:

```json
{
  "status": "error",
  "error_code": "ERROR_CODE_NAME",
  "message": "Detailed human-readable error description.",
  "timestamp": "2026-09-13T09:48:17.355Z"
}
```

### HTTP Error Codes Reference

| HTTP Code | Error Code | Trigger Condition | Sample Resolution |
| :--- | :--- | :--- | :--- |
| **`400`** | `MALFORMED_JSON` | Body is empty, malformed JSON, or missing `features`/`instances`/`data` key. | Provide a valid JSON payload containing `"features"`. |
| **`404`** | `NOT_FOUND` | Client requested a path that does not exist (e.g. `/api/v1/invalid`). | Verify URL path. |
| **`405`** | `METHOD_NOT_ALLOWED` | Using incorrect HTTP method (e.g., `GET /predict`). | Use `POST` method for prediction endpoint. |
| **`415`** | `UNSUPPORTED_MEDIA_TYPE` | `Content-Type` header is not `application/json`. | Set header `Content-Type: application/json`. |
| **`422`** | `UNPROCESSABLE_ENTITY` | Input feature array length $\neq 8$, or contains non-numeric strings/NaNs. | Ensure 8 numerical feature inputs per sample. |
| **`500`** | `INTERNAL_SERVER_ERROR` | Internal server or neural network execution failure. | Check server logs in `api_service.log`. |

---

## Input Features Definition

| Index | Feature Name | Description | Valid Range | Unit |
| :--- | :--- | :--- | :--- | :--- |
| 0 | `age` | Patient Age | 18 - 100 | Years |
| 1 | `bmi` | Body Mass Index | 10.0 - 50.0 | $\text{kg/m}^2$ |
| 2 | `blood_pressure` | Systolic Blood Pressure | 70 - 220 | mmHg |
| 3 | `glucose_level` | Fasting Glucose Level | 50 - 300 | mg/dL |
| 4 | `cholesterol` | Total Cholesterol Level | 100 - 400 | mg/dL |
| 5 | `heart_rate` | Resting Heart Rate | 40 - 140 | bpm |
| 6 | `physical_activity_hours` | Weekly Physical Activity | 0 - 30 | Hours/Week |
| 7 | `sleep_hours` | Daily Sleep Duration | 2 - 14 | Hours/Day |
