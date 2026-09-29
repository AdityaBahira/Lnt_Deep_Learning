# Task 8: Integrating Streamlit Frontend with Flask REST API

## 📌 Executive Summary
Task 8 establishes seamless client-server communication between an interactive **Streamlit Multi-Page UI** (frontend) and a **Flask REST API** (backend serving a trained PyTorch `DeepHealthRiskNet` neural network model).

---

## 🏗️ System Architecture

```
+-----------------------------------+               +-----------------------------------+
|       Streamlit Frontend UI       |               |         Flask REST API            |
|       (Multi-Page Platform)       |               |     (PyTorch Inference Engine)    |
|                                   |               |                                   |
|  - 1_Overview.py                  |  HTTP POST    |  - GET / (Landing & Metadata)     |
|  - 2_Prediction.py --------------->|-------------->|  - GET /health (Status Probe)     |
|  - 3_Batch_Processing.py          | /predict JSON |  - POST /predict (Inference)      |
|  - 4_Analytics.py                 |               |                                   |
|  - 5_System_Status.py             |  JSON Resp    |  - model_loader.py                |
|                                   |<--------------|  - saved_models/dl_model.pt       |
+-----------------------------------+               +-----------------------------------+
```

---

## 📁 Directory Structure

```
Task 8/
├── saved_models/
│   ├── config.json
│   └── dl_model.pt
├── views/
│   ├── 1_Overview.py
│   ├── 2_Prediction.py
│   ├── 3_Batch_Processing.py
│   ├── 4_Analytics.py
│   └── 5_System_Status.py
├── health_activity_data.csv
├── sample_cohort_data.csv
├── model_loader.py
├── flask_api.py
├── utils.py
├── app.py
├── test_integration.py
├── Task_8_Streamlit_Flask_Integration.ipynb
├── Task_8_Streamlit_Flask_Integration_Report.pdf
├── requirements.txt
└── README.md
```

---

## 🚀 Execution Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask REST API Backend
In a terminal, execute:
```bash
python flask_api.py
```
*The server starts on `http://127.0.0.1:5000`.*

### 3. Launch the Streamlit Multi-Page Application
In a second terminal, execute:
```bash
streamlit run app.py
```
*Open `http://localhost:8501` in your browser.*

### 4. Run Automated Integration Test Suite
```bash
python test_integration.py
```

---

## 🧪 Verified REST API Endpoints

| Endpoint | Method | Payload | Description |
|---|---|---|---|
| `/` | `GET` | None | Landing info & endpoint metadata |
| `/health` | `GET` | None | Health status & PyTorch model readiness |
| `/predict` | `POST` | `{"features": [v1, ..., v14]}` | Single patient neural network inference |
| `/predict` | `POST` | `{"instances": [[...], [...]]}` | Batch cohort neural network inference |

---

## 📊 Verification & Test Results
All 11 integration test cases executed successfully:
- `TC-01`: GET / Landing Endpoint (HTTP 200 OK)
- `TC-02`: GET /health Readiness Probe (HTTP 200 OK)
- `TC-03`: POST /predict Single Patient JSON Payload (HTTP 200 OK)
- `TC-04`: POST /predict Batch Instances JSON Payload (HTTP 200 OK)
- `TC-05`: POST /predict Dictionary Payload (HTTP 200 OK)
- `TC-06`: POST /predict Non-JSON Content-Type Rejection (HTTP 415)
- `TC-07`: POST /predict Payload Structure Validation (HTTP 400)
- `TC-08`: POST /predict Dimension Mismatch Rejection (HTTP 422)
- `TC-09`: POST /predict Non-Numeric Feature Validation (HTTP 422)
- `TC-10`: Invalid Route Request (HTTP 404)
- `TC-11`: ModelConnector PyTorch Direct Fallback Mode
