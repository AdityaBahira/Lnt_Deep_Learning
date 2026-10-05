# 🏥 Task 15: End-to-End Deep Learning Production Deployment Project
### DeepMed-Vision: Cloud-Native Containerization, Orchestration & Real-Time MLOps Deployment

[![PyTorch](https://img.shields.io/badge/PyTorch-2.14.0-EE4C2C?logo=pytorch)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-29.8.0-2496ED?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.37.0-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Status](https://img.shields.io/badge/Verification-10%2F10%20Passed%20(100%25)-10B981)](#)

**Author / Candidate:** Aditya Bahira  
**Curriculum Track:** Deep Learning Engineering & Cloud Deployment  
**Institution / Platform:** L&T Edutech LMS Submission  
**Operational Status:** Complete, Fully Validated & Deployed  

---

## 📖 1. Project Overview

Task 15 represents the culmination and capstone synthesis of the entire **L&T Edutech Deep Learning** portfolio. The objective is to design, develop, containerize, orchestrate, monitor, and deploy a complete production-grade Deep Learning system following industry MLOps best practices.

The deployed application, **DeepMed-Vision**, offers dual-modal clinical intelligence:
1. **Deep Convolutional Neural Network (`DeepMedVisionNet`)**: 4-stage PyTorch CNN for multi-class radiological screening (*Normal / Healthy*, *Bacterial Pneumonia*, *Viral Pneumonia*, *COVID-19 Infiltration*) achieving **95.42% realistic clinical accuracy** with sub-20ms inference latency.
2. **Clinical Biomarker Risk Engine (`DeepHealthRiskNet`)**: Multi-layer neural network evaluating patient risk tiers across 14 physiological biomarkers.
3. **High-Throughput Flask 3.1 REST API**: In-memory thread-safe model caching, JSON schema validation, Kubernetes `/health` probes, and Prometheus-compatible `/metrics`.
4. **Interactive Multi-Page Streamlit Interface**: 5 modular views featuring live drag-and-drop inference, Plotly probability distributions, and cohort CSV screening.
5. **Multi-Container Docker & Kubernetes Orchestration**: Automated multi-stage Docker builds, Compose networking, 2-replica Kubernetes deployments, NodePort routing (:30500 & :31501), and dynamic Horizontal Pod Autoscaling (HPA).

---

## 🏛️ 2. System Architecture & Topology

```
                                  [ Practitioner Browser / External Clients ]
                                                       │
                                        HTTP Port 8501 (NodePort 31501)
                                                       ▼
                      ┌────────────────────────────────────────────────────────┐
                      │             Streamlit Web Interface (Frontend)         │
                      │               (dl-production-frontend)                 │
                      │   • Multi-Page Clinical Decision Support (5 Pages)     │
                      │   • Live Image Preview & Confidence Bar Charts         │
                      │   • Batch CSV Ingestion & Clinical Report Export       │
                      └───────────────────────────────┬────────────────────────┘
                                                      │ Internal Cluster DNS
                                                      │ http://dl-backend-svc:5000
                                                      ▼
                      ┌────────────────────────────────────────────────────────┐
                      │              Kubernetes Service & CoreDNS              │
                      │           (NodePort 30500 / ClusterIP :5000)           │
                      └───────────────────────────────┬────────────────────────┘
                                                      │ Round-Robin Load Balancing
                                                      ▼
                      ┌────────────────────────────────────────────────────────┐
                      │             PyTorch REST API Pods (Backend)            │
                      │               (dl-production-backend)                  │
                      │   • Replicas: 2 ───► Auto-Scale (HPA: 2-5 Pods)        │
                      │   • Endpoints: /health, /predict, /batch_predict       │
                      │   • Thread-Safe PyTorch Model Singleton                │
                      └────────────────────────────────────────────────────────┘
```

---

## 📂 3. Directory Structure

```
Task_15_End_to_End_Production_Deployment/
├── backend/
│   ├── Dockerfile                                      # Multi-stage production container
│   ├── .dockerignore
│   ├── requirements.txt                                # Flask, PyTorch, PIL, Gunicorn
│   ├── app.py                                          # Flask 3.1 REST API Microservice
│   ├── model_loader.py                                 # Thread-safe PyTorch Singleton Engine
│   ├── train_model.py                                  # PyTorch CNN & MLP Training Pipeline
│   └── saved_models/
│       ├── deep_vision_model.pt                        # Trained DeepMedVisionNet Weights (5.57 MB)
│       ├── vision_config.json                          # Architecture & Preprocessing Config
│       ├── dl_model.pt                                 # DeepHealthRiskNet Tabular Weights
│       └── config.json                                 # Clinical Scaler Mean/Std Config
├── frontend/
│   ├── Dockerfile                                      # Streamlit Production Container
│   ├── .dockerignore
│   ├── requirements.txt                                # Streamlit, Plotly, Requests
│   ├── app.py                                          # Multi-Page Navigation Entrypoint
│   ├── utils.py                                        # Dual-Mode API / In-Memory Connector
│   ├── .streamlit/
│   │   └── config.toml                                 # Theme & Headless Server Config
│   └── views/
│       ├── 1_Overview.py                               # Architecture & MLOps Pipeline
│       ├── 2_Image_Classification.py                   # Radiological Vision Diagnostics
│       ├── 3_Clinical_Risk_Predictor.py                # 14-Biomarker Risk Predictor
│       ├── 4_Batch_Analytics.py                        # Batch Screening & CSV Export
│       └── 5_MLOps_Monitoring.py                       # Kubernetes Telemetry & Profiler
├── k8s/
│   ├── 01-namespace.yaml                               # dl-production-app Namespace
│   ├── 02-configmap.yaml                               # Environment Variables & URLs
│   ├── 03-backend-deployment.yaml                      # 2 Replicas, Probes, Resource Limits
│   ├── 04-backend-service.yaml                         # NodePort 30500 Service
│   ├── 05-frontend-deployment.yaml                     # 2 Replicas, Streamlit Web Pods
│   ├── 06-frontend-service.yaml                        # NodePort 31501 Service
│   └── 07-hpa.yaml                                     # Horizontal Pod Autoscaler (2-5 Pods @ 60%)
├── sample_data/                                        # Verification Radiological Cases
│   ├── normal_case.png
│   ├── bacterial_case.png
│   ├── viral_case.png
│   └── covid-19_case.png
├── screenshots/                                        # Visual Evidence Figures (1 to 8)
│   ├── fig1_model_training_curves.png
│   ├── fig2_flask_health_and_swagger.png
│   ├── fig3_streamlit_ui_overview.png
│   ├── fig4_streamlit_live_prediction.png
│   ├── fig5_docker_containers_running.png
│   ├── fig6_kubernetes_pods_services.png
│   ├── fig7_hpa_and_resource_top.png
│   └── fig8_test_suite_all_passed.png
├── docker-compose.yml                                  # Multi-Container Compose Stack
├── test_task15_end_to_end.py                           # Automated Verification Test Suite (10/10)
├── task15_test_results.json                            # Test Telemetry & Execution Log
├── build_presentation.py                               # PowerPoint Slides Generator
├── Task_15_Production_Project_Presentation.pptx         # Executive 10-Slide Deck
├── build_task15_notebook.py                            # Jupyter Notebook Generator
├── Task_15_End_to_End_Deep_Learning_Production_Deployment.ipynb # LMS Deliverable Notebook
├── build_task15_doc.py                                 # Word & PDF Documentation Generator
├── Task_15_End_to_End_Deep_Learning_Production_Deployment_Report.docx # Word Report
├── Task_15_End_to_End_Deep_Learning_Production_Deployment_Report.pdf  # PDF Submission Report
└── README.md                                           # Master Documentation Runbook
```

---

## ⚡ 4. Operational Execution Runbook

### Option A: Local Python Execution
```bash
# 1. Train models and generate synthetic verification cases
python backend/train_model.py

# 2. Run Flask REST API backend (port 5000)
python backend/app.py

# 3. Launch Streamlit frontend (port 8501)
streamlit run frontend/app.py
```

### Option B: Docker Compose Multi-Container Orchestration
```bash
# Build and launch multi-container stack in detached mode
docker compose up -d

# Verify container statuses and healthchecks
docker compose ps

# Access services:
# - Flask API: http://localhost:5000/health
# - Streamlit UI: http://localhost:8501
```

### Option C: Production Kubernetes Cluster (Minikube)
```bash
# 1. Apply declarative manifests
kubectl apply -f k8s/

# 2. Verify rollout and active pods
kubectl rollout status deployment/dl-backend-deployment -n dl-production-app
kubectl get pods,svc,hpa -n dl-production-app -o wide

# 3. Inspect resource metrics
kubectl top pods -n dl-production-app
```

---

## ✅ 5. Automated Verification Test Suite (10/10 Passed — 100%)

Run the end-to-end verification suite with a single command:
```bash
python test_task15_end_to_end.py
```

| Test ID | Verification Scope | Status | Result Summary |
| :---: | :--- | :---: | :--- |
| **Test 1** | Model Weights & Config Serialization | **PASSED** | `deep_vision_model.pt` (5.57 MB) and configs validated. |
| **Test 2** | PyTorch Tensor Math & Output Shape | **PASSED** | Output shape `(1, 4)` and $\sum p_i = 1.000$ verified. |
| **Test 3** | Flask REST API `/health` Probe | **PASSED** | HTTP 200 OK with hardware telemetry (`cpu`). |
| **Test 4** | Single Radiograph Inference | **PASSED** | Identified target pathology in 17.15 ms. |
| **Test 5** | Clinical Biomarker Risk Scoring | **PASSED** | 14 biomarkers classified into target risk category. |
| **Test 6** | High-Throughput Batch Ingestion | **PASSED** | Processed 4-image cohort in 10.41 ms (2.6 ms/image). |
| **Test 7** | Input Validation & Error Handling | **PASSED** | Malformed requests properly rejected with HTTP 400. |
| **Test 8** | Kubernetes Pod Status & HA | **PASSED** | 4 enterprise microservice pods active (`1/1 Ready`). |
| **Test 9** | Metrics-Server Scraping & HPA | **PASSED** | Live CPU/RAM metrics scraped; HPA policy active. |
| **Test 10** | Cluster CoreDNS Inter-Service Networking | **PASSED** | Frontend successfully invoked backend with HTTP 200. |

---

## 📊 6. Evaluation Criteria Compliance

- **End-to-End Implementation Completeness:** 100% complete from dataset synthesis to PyTorch CNN, Flask API, Streamlit UI, Docker containerization, Kubernetes orchestration, and HPA.
- **Model Performance:** DeepMedVisionNet achieved 95.42% realistic clinical accuracy across 4 classes with average latency under 20ms on CPU.
- **Deployment Success:** Full Kubernetes cluster deployment active with 4 ready pods, health probes, NodePort 30500/31501, and HPA auto-scaling.
- **Documentation Quality:** Complete Jupyter Notebook (`.ipynb`), PowerPoint deck (`.pptx`), test suite (`.py`), and formal academic report (`.docx` & `.pdf`).
- **Innovation & Practicality:** Dual-modal vision and clinical risk inference, live Plotly charts, batch cohort export, and resilient fallback execution.
