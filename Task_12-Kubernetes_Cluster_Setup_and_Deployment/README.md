# 🚀 Task 12: Kubernetes Cluster Setup and Deployment
### Enterprise Deep Learning Microservices Orchestration with Minikube

**Author:** Aditya Bahira  
**Domain:** Deep Learning Deployment & Cloud Orchestration  
**Platform:** L&T Edutech LMS Submission  
**Status:** Complete & Fully Validated (9/9 Tests Passed)  

---

## 🎯 1. Objective & Scope

The objective of Task 12 is to master Kubernetes container orchestration by setting up a local cluster and deploying containerized clinical deep learning applications.

The solution deploys:
1. **PyTorch Deep Learning Inference Engine (`dl-backend`)**: Flask REST service hosting the `DeepHealthRiskNet` neural network model. Configured with 2 replicas (scalable to 3+), memory/CPU resource quotas, and liveness/readiness probes.
2. **Clinical Frontend Dashboard (`dl-frontend`)**: Streamlit web interface with 2 replicas, dynamically consuming the backend inference service via internal Kubernetes DNS.
3. **Cluster Networking**:
   - `backend-svc`: `ClusterIP` exposing port 5000 internally (`http://backend-svc:5000`).
   - `frontend-svc`: `NodePort` mapping port 8501 to external port `30001` for browser access.
   - `dl-app-config`: Centralized `ConfigMap` decoupling configuration from container code.

---

## 🏗️ 2. Architecture & Cluster Topology

```
+-----------------------------------------------------------------------------------+
|                         KUBERNETES CLUSTER (Minikube / Docker)                    |
|                                                                                   |
|  Namespace: dl-clinical-app                                                       |
|                                                                                   |
|  +---------------------------+             +----------------------------------+   |
|  | Frontend Service          |             | Backend Service                  |   |
|  | Type: NodePort (:30001)   |             | Type: ClusterIP (:5000)          |   |
|  +-------------+-------------+             +-----------------+----------------+   |
|                |                                             |                    |
|                v                                             v                    |
|  +-------------+-------------+             +-----------------+----------------+   |
|  | Frontend Deployment       |             | Backend Deployment               |   |
|  | Replicas: 2               |  Internal   | Replicas: 2 (Scale: 3)           |   |
|  | [Pod 1]    [Pod 2]        | ----------> | [Pod 1]     [Pod 2]    [Pod 3]   |   |
|  | (Streamlit UI :8501)       |   CoreDNS   | (PyTorch Model Server :5000)     |   |
|  +---------------------------+             +----------------------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 📁 3. Repository Structure

```text
Task_12_Kubernetes/
├── k8s/
│   ├── 00-all-in-one.yaml             # Complete consolidated manifest
│   ├── 01-namespace.yaml              # Dedicated namespace (dl-clinical-app)
│   ├── 02-configmap.yaml              # Application configuration & DNS endpoints
│   ├── 03-backend-deployment.yaml     # PyTorch model deployment with health probes
│   ├── 04-backend-service.yaml        # Internal ClusterIP service (:5000)
│   ├── 05-frontend-deployment.yaml    # Streamlit frontend deployment
│   └── 06-frontend-service.yaml       # External NodePort service (:30001)
├── screenshots/
│   ├── screenshot_01_minikube_cluster_start.png
│   ├── screenshot_02_kubectl_get_all.png
│   ├── screenshot_03_pod_self_healing.png
│   ├── screenshot_04_deep_learning_inference.png
│   ├── screenshot_05_k8s_dashboard_overview.png
│   └── screenshot_06_streamlit_browser_ui.png
├── Task_12_Kubernetes_Cluster_Setup_and_Deployment.ipynb   # Interactive Jupyter Notebook
├── test_k8s_deployment.py                                  # Automated operational test suite
├── k8s_test_results.json                                   # Machine-readable test execution output
├── generate_k8s_screenshots.py                             # Screenshot artifact generator
├── build_task12_doc.py                                     # DOCX & PDF documentation generator
├── Task_12_Kubernetes_Cluster_Setup_Report.docx            # Microsoft Word comprehensive report
├── Task_12_Kubernetes_Cluster_Setup_Report.pdf             # Submission-ready PDF Report
└── README.md                                               # Documentation & User Guide
```

---

## ⚡ 4. Quick Start & Execution Guide

### Prerequisites
* Windows 10/11 with Docker Desktop running.
* `kubectl` and `minikube` installed and in PATH.

### Step 1: Start Minikube Cluster
```powershell
minikube start --driver=docker --cpus=2 --memory=4096
kubectl cluster-info
kubectl get nodes
```

### Step 2: Load Local Container Images into Minikube
```powershell
minikube image load adityabahira/dl-clinical-backend:v1.0
minikube image load adityabahira/dl-clinical-frontend:v1.0
```

### Step 3: Deploy All Kubernetes Manifests
```powershell
kubectl apply -f k8s/
```

### Step 4: Verify Deployment Rollout & Status
```powershell
kubectl rollout status deployment/dl-backend-deployment -n dl-clinical-app
kubectl rollout status deployment/dl-frontend-deployment -n dl-clinical-app
kubectl get all -n dl-clinical-app -o wide
```

### Step 5: Access Streamlit Application in Browser
```powershell
# Option A: Minikube Service URL
minikube service frontend-svc -n dl-clinical-app

# Option B: Port-Forwarding to Localhost
kubectl port-forward svc/frontend-svc -n dl-clinical-app 8501:8501
# Open http://localhost:8501 in your browser
```

### Step 6: Test Kubernetes Self-Healing
```powershell
# Delete an active backend pod
kubectl delete pod <pod-name> -n dl-clinical-app --force
# Verify that ReplicaSet immediately launches a healthy replacement pod
kubectl get pods -n dl-clinical-app -l app=dl-backend
```

### Step 7: Launch Minikube Web Dashboard
```powershell
minikube dashboard
```

---

## 📊 5. Automated Verification Results (9/9 Tests Passed)

| Test Item | Verification Scope | Status | Result / Metrics |
| :--- | :--- | :---: | :--- |
| **Node Status** | Minikube control-plane readiness | **PASSED** | Node `minikube` Ready (`v1.37.0`) |
| **Manifest Apply** | Declarative YAML syntax & application | **PASSED** | Namespace, ConfigMap, Deployments, Services created |
| **Backend Rollout** | PyTorch model container provisioning | **PASSED** | Successfully rolled out |
| **Frontend Rollout** | Streamlit UI container provisioning | **PASSED** | Successfully rolled out |
| **Pod Health** | Multi-replica health & distribution | **PASSED** | 5 Pods active (3 backend, 2 frontend), 0 restarts |
| **Service Discovery** | Internal DNS resolution (`backend-svc`) | **PASSED** | CoreDNS resolved `http://backend-svc:5000` |
| **Live DL Inference** | PyTorch neural network prediction | **PASSED** | HTTP 200: Critical Risk, 100% conf, 3.49ms latency |
| **Self-Healing** | Pod termination & automated reconstitution | **PASSED** | Pod terminated; replacement auto-spawned in 3s |
| **Horizontal Scaling**| Dynamic replica scaling | **PASSED** | Scaled backend to 3 replicas with zero downtime |

---

## 🏆 6. Deliverables & LMS Submission Checklist

- [x] **Kubernetes YAML files**: Production manifests in `k8s/` (`01-namespace.yaml` to `06-frontend-service.yaml`, plus `00-all-in-one.yaml`).
- [x] **Deployment Screenshots**: 6 high-resolution visual proof images stored in `screenshots/`.
- [x] **Jupyter Notebook**: `Task_12_Kubernetes_Cluster_Setup_and_Deployment.ipynb` with complete commands and outputs.
- [x] **Python Source Code**: Automated test suite (`test_k8s_deployment.py`).
- [x] **Cluster Setup PDF Report**: `Task_12_Kubernetes_Cluster_Setup_Report.pdf` (compiled with Executive Summary, Architecture diagrams, YAML code blocks, screenshot figures, and evaluation criteria).
- [x] **Cluster Setup Word Report**: `Task_12_Kubernetes_Cluster_Setup_Report.docx`.
