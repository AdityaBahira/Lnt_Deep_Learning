# Task 4: Developing a Flask API for Deep Learning Models

## Objective
To expose a trained Deep Learning PyTorch model as a production-grade REST API using the Flask framework, complete with JSON request-response handling, input schema validation, HTTP exception handling, automated testing, and LMS submission deliverables.

---

## Directory Structure
```text
e:/Rest_Api/
├── app.py                             # Flask REST API Server
├── model_loader.py                    # Thread-safe PyTorch Inference Engine
├── train_and_save_model.py            # Deep Learning Model Training & Serialization Script
├── test_client.py                     # Automated HTTP Test Suite (13/13 Tests)
├── generate_pdf.py                    # PDF Report Generator
├── task4_flask_dl_api.ipynb           # Executable Jupyter Notebook Deliverable
├── API_DOCUMENTATION.md               # OpenAPI / Markdown API Specification
├── Task_4_Flask_API_DL_Submission.pdf # Submission PDF Report for LMS Platform
├── sample_outputs.json                # Verified Test Outputs & Response Logs
├── requirements.txt                   # Python Dependencies
├── README.md                          # Project Documentation
└── saved_models/
    ├── dl_model.pt                    # PyTorch Saved Weights StateDict
    └── config.json                    # Feature Normalization Metrics & Metadata
```

---

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train & Save PyTorch Deep Learning Model
```bash
python train_and_save_model.py
```

### 3. Launch Flask REST API Server
```bash
python app.py
```
The server will start on `http://127.0.0.1:5000`.

### 4. Run Automated API Test Suite
In a separate terminal:
```bash
python test_client.py
```

### 5. Access Interactive API Documentation
Open your web browser and navigate to:
`http://127.0.0.1:5000/docs`

---

## API Endpoints Overview

| Method | Route | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Root Metadata & System Status |
| `GET` | `/health` | Health Check & PyTorch Model Readiness Probe |
| `POST` | `/predict` | Deep Learning Inference Endpoint (Single/Batch JSON) |
| `GET` | `/docs` | Interactive HTML API Documentation |

---

## Deliverables Summary for LMS Platform Submission
1. **Source Code**: Python modules (`app.py`, `model_loader.py`, `train_and_save_model.py`, `test_client.py`).
2. **Jupyter Notebook**: `task4_flask_dl_api.ipynb` containing training, API execution, and plots.
3. **API Documentation**: `API_DOCUMENTATION.md` and interactive web UI at `/docs`.
4. **Submission PDF**: `Task_4_Flask_API_DL_Submission.pdf` containing full source code, test results, outputs, and observations ready to upload on the L&T Edutech LMS Platform.
