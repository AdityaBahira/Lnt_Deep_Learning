# 🏥 Task 5: Deep Learning API Testing & Validation (Postman & cURL)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.12-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-v11-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Build Status](https://img.shields.io/badge/Tests-12%2F12%20PASSED-22c55e?style=for-the-badge)

---

## 📌 Project Overview

This repository contains the complete testing suite, Postman collection, cURL verification scripts, and documentation for **Task 5: API Testing and Validation of the Health Risk Deep Learning Prediction API**.

The system under test is a production-ready **Flask REST API** wrapping a pre-trained **PyTorch 3-Layer Neural Network (`DeepHealthRiskNet`)**. The model evaluates **14 physiological and lifestyle metrics** per patient and classifies them into one of **4 clinical risk categories**:
- `0: Low Risk`
- `1: Moderate Risk`
- `2: High Risk`
- `3: Critical Risk`

---

## 🎯 Objectives Pursued

- 🟢 **Health & Readiness Verification**: Confirm server startup and PyTorch inference engine pre-loading (`GET /health`).
- 🟢 **Schema & Format Validation**: Validate predictions across 3 JSON request formats (Single Vector, Batch Matrix, Dict Mapping).
- 🟢 **Systematic Negative Testing**: Probe failure boundaries for missing inputs, unprocessable entity dimensions, non-numeric values, and invalid HTTP routes/methods.
- 🟢 **Automated Postman Assertions**: Execute 25 automated JavaScript test assertions (`pm.test`) via Postman Collection Runner.
- 🟢 **Status Code Accuracy**: Verify strict REST status code mapping (`200 OK`, `400 Bad Request`, `404 Not Found`, `405 Method Not Allowed`, `415 Unsupported Media Type`, `422 Unprocessable Entity`).

---

## 🚀 Endpoint Summary

| HTTP Method | Endpoint | Description | Expected Request Body | Success Status |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | API Landing & Metadata | None | `200 OK` |
| `GET` | `/health` | Server Health & PyTorch Model Readiness Probe | None | `200 OK` |
| `POST` | `/predict` | Deep Learning Inference Endpoint | JSON Object (Format A/B/C) | `200 OK` |
| `GET` | `/docs` | Interactive HTML Documentation Page | None | `200 OK` |

---

## 📥 Supported Input Formats (`POST /predict`)

### 1️⃣ Format A: Single Sample Vector Array (`"features"`)
```json
{
  "features": [56.0, 164.0, 81.0, 30.72, 5134.0, 1796.0, 8.6, 102.0, 137.0, 72.0, 8.1, 7.0, 0.0, 0.0]
}
```

### 2️⃣ Format B: Batch 2D Matrix Array (`"instances"`)
```json
{
  "instances": [
    [25.0, 199.0, 85.0, 31.14, 5131.0, 3256.0, 6.5, 104.0, 106.0, 79.0, 3.6, 7.0, 0.0, 0.0],
    [78.0, 172.0, 72.0, 32.46, 19532.0, 2216.0, 9.6, 95.0, 96.0, 86.0, 8.3, 2.0, 1.0, 1.0]
  ]
}
```

### 3️⃣ Format C: Key-Value Feature Dict (`"data"`)
```json
{
  "data": {
    "age": 60, "height_cm": 157, "weight_kg": 63, "bmi": 29.37,
    "daily_steps": 17351, "calories_intake": 2556, "hours_of_sleep": 5.1,
    "heart_rate": 111, "systolic_bp": 100, "diastolic_bp": 64,
    "exercise_hours_per_week": 8.5, "alcohol_consumption_per_week": 8,
    "smoker": 1, "diabetic": 0
  }
}
```

---

## 📊 Test Case Execution Matrix

| Test ID | Scenario Description | Method & Endpoint | Input Payload / Header | Expected Status | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Root API Metadata Check | `GET /` | None | `200 OK` | `PASS` |
| **TC-02** | Health Readiness Probe | `GET /health` | None | `200 OK` | `PASS` |
| **TC-03** | Single Patient Vector (Format A) | `POST /predict` | 14-feature float array | `200 OK` | `PASS` |
| **TC-04** | Batch Patients Matrix (Format B) | `POST /predict` | 2D float matrix (2 samples) | `200 OK` | `PASS` |
| **TC-05** | Dict Feature Mapping (Format C) | `POST /predict` | Feature key-value dictionary | `200 OK` | `PASS` |
| **TC-06** | Unsupported Media Type | `POST /predict` | Header `Content-Type: text/plain` | `415 Unsupported Media Type` | `PASS` |
| **TC-07** | Missing Request Body | `POST /predict` | Empty `{}` body | `400 Bad Request` | `PASS` |
| **TC-08** | Missing Required Key | `POST /predict` | `{"invalid_key": [1,2,3]}` | `400 Bad Request` | `PASS` |
| **TC-09** | Feature Dimension Mismatch | `POST /predict` | 4 features instead of 14 | `422 Unprocessable Entity` | `PASS` |
| **TC-10** | Non-numeric Feature Value | `POST /predict` | `{"features": [56, "invalid", ...]}` | `422 Unprocessable Entity` | `PASS` |
| **TC-11** | Disallowed HTTP Method | `GET /predict` | None | `405 Method Not Allowed` | `PASS` |
| **TC-12** | Non-existent URL Path | `GET /api/v2/unknown`| None | `404 Not Found` | `PASS` |

---

## 💻 How to Run & Verify

### 1. Launch the Flask API Server
```bash
# Clone the repository
git clone https://github.com/aps31012005-prog/Task_5_API_testing-.git
cd Task_5_API_testing-

# Install dependencies
pip install -r requirements.txt

# Launch Flask API server
python app.py
```
*(Server will start on `http://127.0.0.1:5000` with `DeepHealthRiskNet` model pre-loaded).*

---

### 2. Run Automated Postman Collection
1. Open **Postman Desktop Client**.
2. Press **`Ctrl + O`** and select `Task_5_Health_Risk_DL_API.postman_collection.json`.
3. Hover over the collection name -> Click **`...`** -> **Run collection**.
4. Click **Run Task 5 - Health Risk Deep Learning API Tests**.
5. All **12 requests & 25 test assertions** will execute with **100% PASS** in green!

---

### 3. Quick Terminal cURL Verification

#### System Health Probe:
```bash
curl -s -X GET http://127.0.0.1:5000/health
```

#### Clinical Prediction Request:
```bash
curl -s -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [56.0, 164.0, 81.0, 30.72, 5134.0, 1796.0, 8.6, 102.0, 137.0, 72.0, 8.1, 7.0, 0.0, 0.0]}'
```

---

## 📁 Repository Structure

```text
Task_5_API_Testing/
├── README.md                                       # Main repository documentation & guide
├── Task_5_Health_Risk_DL_API.postman_collection.json # Exported Postman Collection JSON (v2.1)
├── Task_5_API_Testing_and_Validation_Report.docx  # Complete Word document report
├── app.py                                          # Flask REST API server source code
├── model_loader.py                                 # PyTorch DeepHealthRiskNet inference engine
├── requirements.txt                                # Python dependencies list
├── test_client.py                                  # Automated Python test client script
├── sample_outputs.json                             # Recorded test execution output log
├── saved_models/                                   # Trained model artifacts folder
│   ├── dl_model.pt                                 # PyTorch weights state dictionary
│   └── config.json                                 # Scaler mean/std & class configuration
└── screenshots/                                    # Captured test execution screenshots
    ├── 01_flask_server_startup.png
    ├── 02_root_endpoint_tc01.png
    ├── 03_health_probe_tc02.png
    ├── 04_single_prediction_tc03.png
    ├── 05_batch_prediction_tc04.png
    ├── 06_dict_prediction_tc05.png
    ├── 07_unsupported_media_tc06.png
    ├── 08_missing_payload_tc07_tc08.png
    ├── 09_dimension_mismatch_tc09.png
    ├── 10_non_numeric_tc10.png
    ├── 11_method_not_allowed_tc11.png
    ├── 12_not_found_tc12.png
    └── 13_postman_runner_summary.png
```

---

## 👤 Author Information

- **Name**: Aryan Pravin Shetty / [Your Student Name]
- **Student ID**: 5626748 / [Your Student ID]
- **Roll No**: 34 / [Your Roll No]
- **Subject**: Deep Learning from Production to Deployment
- **Platform**: L&T Edutech LMS Platform
