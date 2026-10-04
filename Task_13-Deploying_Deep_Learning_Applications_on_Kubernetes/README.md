# 🚀 Task 13: Deploying Deep Learning Applications on Kubernetes
### Production Microservice Deployment, External Service Exposure, and Inference Validation

**Author:** Aditya Bahira  
**Domain:** Deep Learning Deployment & Cloud Orchestration  
**Platform:** L&T Edutech LMS Submission  
**Status:** Complete & Fully Validated (10/10 Verification Tests Passed — 100%)  

---

## 🎯 1. Objective & Scope

The objective of Task 13 is to deploy and expose containerized deep learning applications within an enterprise Kubernetes cluster (`Minikube`).

The solution deploys:
1. **PyTorch Deep Learning Inference Engine (`dl-backend`)**:
   - High-throughput REST API serving the `DeepHealthRiskNet` deep neural network model.
   - Deployed with 2 replicas (scaled to 3) for fault tolerance and high availability.
   - Configured with production CPU/Memory requests & limits to prevent memory starvation and out-of-memory (OOM) evictions.
   - Integrated with HTTP `/health` liveness and readiness probes ensuring zero-downtime traffic routing.
2. **Clinical Analytics Dashboard (`dl-frontend`)**:
   - Streamlit web interface with 2 replicas, dynamically consuming the backend inference service via internal Kubernetes DNS (`http://dl-backend-svc:5000`).
3. **Cluster Networking & External Exposure**:
   - `dl-backend-svc`: `NodePort` mapping port 5000 internally and port `30500` externally for REST client inference evaluation.
   - `dl-frontend-svc`: `NodePort` mapping internal port 8501 to external port `31501` for clinician browser access.
   - `dl-production-config`: Centralized `ConfigMap` decoupling environment configurations, URLs, and hyperparameters.

---

## 🏗️ 2. Architecture & Networking Topology

```
+-------------------------------------------------------------------------------------------------+
|                                   EXTERNAL CLIENT ENVIRONMENT                                   |
|                                                                                                 |
|        [ Web Browser / Clinician ]                         [ REST Client / Python / cURL ]      |
+-------------------------------------------------------------------------------------------------+
                          |                                                 |
            HTTP Port: 31501 (NodePort)                       HTTP Port: 30500 (NodePort)
                          v                                                 v
+-------------------------------------------------------------------------------------------------+
|                                 KUBERNETES CLUSTER (Minikube)                                   |
|                                                                                                 |
|  Namespace: dl-production-app                                                                   |
|                                                                                                 |
|  +-------------------------------------+               +-------------------------------------+  |
|  | Frontend Service (dl-frontend-svc)  |               | Backend Service (dl-backend-svc)    |  |
|  | Type: NodePort (Port: 8501:31501)   |               | Type: NodePort & ClusterIP (:5000)  |  |
|  +------------------+------------------+               +------------------+------------------+  |
|                     |                                                     |                     |
|                     v                                                     v                     |
|  +-------------------------------------+               +-------------------------------------+  |
|  | Frontend Deployment                 |               | Backend Deployment (PyTorch)        |  |
|  | Replicas: 2                         |   CoreDNS     | Replicas: 2 (Scale: 3)              |  |
|  | - Pod: dl-frontend-5df...           | ------------> | - Pod: dl-backend-5cd...            |  |
|  | - Pod: dl-frontend-5df...           | dl-backend-svc| - Pod: dl-backend-5cd...            |  |
|  | (Streamlit Dashboard)               |     :5000     | (PyTorch DeepHealthRiskNet Server)  |  |
|  | Resource: 150m CPU / 256Mi RAM      |               | Resource: 250m CPU / 512Mi RAM      |  |
|  +-------------------------------------+               +-------------------------------------+  |
|                                                                                                 |
|  +-------------------------------------------------------------------------------------------+  |
|  | ConfigMap: dl-production-config                                                           |  |
|  | - BACKEND_URL: "http://dl-backend-svc:5000"  | MODEL_DEVICE: "cpu" | BATCH_SIZE: 1          |  |
|  +-------------------------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------------------------+
```

---

## 📁 3. Repository Structure

```text
Task_13_Kubernetes_Deployment/
├── k8s/
│   ├── 01-namespace.yaml                                         # Dedicated namespace (dl-production-app)
│   ├── 02-configmap.yaml                                         # Decoupled hyperparameters & DNS endpoints
│   ├── 03-backend-deployment.yaml                                # PyTorch model deployment with probes & quotas
│   ├── 04-backend-service.yaml                                   # Backend service (ClusterIP + NodePort 30500)
│   ├── 05-frontend-deployment.yaml                               # Streamlit frontend deployment (2 replicas)
│   ├── 06-frontend-service.yaml                                  # External NodePort service (Port 31501)
│   └── all-in-one-task13.yaml                                    # Single-command consolidated manifest
├── screenshots/
│   ├── screenshot_01_cluster_and_nodes.png                       # Figure 1: Minikube status & node verification
│   ├── screenshot_02_manifest_application.png                    # Figure 2: Applying manifests & rollout status
│   ├── screenshot_03_kubernetes_workloads_all.png                # Figure 3: Complete workload topology & pods
│   ├── screenshot_04_external_service_exposure.png               # Figure 4: Service port mappings & health probes
│   ├── screenshot_05_external_inference_api.png                  # Figure 5: Live external model prediction (/predict)
│   ├── screenshot_06_frontend_dashboard_ui.png                   # Figure 6: Clinician Streamlit dashboard in browser
│   └── screenshot_07_pod_scaling_and_healing.png                 # Figure 7: Horizontal pod scaling & self-healing
├── Task_13_Deploying_Deep_Learning_Applications_on_Kubernetes.ipynb # Complete interactive Jupyter Notebook
├── test_task13_deployment.py                                     # Automated 10-point test suite
├── task13_test_results.json                                      # Telemetry results (10/10 passed)
├── generate_task13_screenshots.py                                # Reference screenshot generator
├── build_task13_notebook.py                                      # Jupyter notebook generator script
├── build_task13_doc.py                                           # Automated Word & PDF documentation builder
├── Task_13_Deep_Learning_Kubernetes_Deployment_Report.docx       # Microsoft Word comprehensive report
├── Task_13_Deep_Learning_Kubernetes_Deployment_Report.pdf        # Submission-ready PDF Report
└── README.md                                                     # Project documentation & guides
```

---

## ⚡ 4. Quick Start & Execution Guide

### Prerequisites
* Windows 10/11 with Docker Desktop running.
* `kubectl` and `minikube` installed in PATH.
* Python 3.10+ with `requests`, `pillow`, `reportlab`, `python-docx`.

### Step 1: Start Minikube Cluster
```powershell
minikube start --driver=docker
kubectl cluster-info
kubectl get nodes
```

### Step 2: Deploy All Kubernetes Manifests
```powershell
kubectl apply -f Task_13_Kubernetes_Deployment/k8s/all-in-one-task13.yaml
kubectl rollout status deployment/dl-backend-deployment -n dl-production-app
kubectl rollout status deployment/dl-frontend-deployment -n dl-production-app
```

### Step 3: Run Port-Forwarding (Bridge to Host Ports)
```powershell
# Expose Backend API on port 30500
kubectl port-forward svc/dl-backend-svc -n dl-production-app 30500:5000 --address 0.0.0.0

# Expose Frontend UI on port 31501
kubectl port-forward svc/dl-frontend-svc -n dl-production-app 31501:8501 --address 0.0.0.0
```

### Step 4: Run the Automated Verification Suite
```powershell
python Task_13_Kubernetes_Deployment/test_task13_deployment.py
```

### Step 5: Generate the Final PDF & Word Reports
```powershell
python Task_13_Kubernetes_Deployment/build_task13_doc.py
```

---

## 📸 5. Guide: How to Capture Your Own Custom Screenshots

To personalize your submission report with your own desktop or browser screenshots, follow this exact guide:

### Shortcut
On Windows, press **`Windows Key + Shift + S`** to open the snipping tool, select the rectangular area, and save the image into `e:\DL_deploy\Task_13_Kubernetes_Deployment\screenshots\` using the filenames below.

---

### Screenshot 1: Minikube Status & Node Readiness
* **Filename:** `screenshots/screenshot_01_cluster_and_nodes.png`
* **Command to run in PowerShell:**
  ```powershell
  minikube status
  kubectl get nodes -o wide
  kubectl cluster-info
  ```
* **What to capture:** The terminal output showing `minikube host: Running`, `kubelet: Running`, and node `minikube Ready`.

---

### Screenshot 2: Manifest Application & Rollout
* **Filename:** `screenshots/screenshot_02_manifest_application.png`
* **Command to run in PowerShell:**
  ```powershell
  kubectl apply -f Task_13_Kubernetes_Deployment/k8s/all-in-one-task13.yaml
  kubectl rollout status deployment/dl-backend-deployment -n dl-production-app
  kubectl rollout status deployment/dl-frontend-deployment -n dl-production-app
  ```
* **What to capture:** The terminal output showing created resources and successful rollout messages.

---

### Screenshot 3: Workload Topology & Pod Status
* **Filename:** `screenshots/screenshot_03_kubernetes_workloads_all.png`
* **Command to run in PowerShell:**
  ```powershell
  kubectl get all,configmap,endpoints -n dl-production-app -o wide
  ```
* **What to capture:** The complete list of pods (1/1 Running), services (NodePort 30500 and 31501), deployments, and endpoints.

---

### Screenshot 4: External Service Exposure & Health Check
* **Filename:** `screenshots/screenshot_04_external_service_exposure.png`
* **Command to run in PowerShell:**
  ```powershell
  curl.exe -s http://localhost:30500/health
  curl.exe -s -I http://localhost:31501/
  ```
* **What to capture:** The JSON health response (`status: healthy`, `model_loaded: true`) and HTTP 200 OK header from the frontend.

---

### Screenshot 5: Live Deep Learning Model Inference (/predict)
* **Filename:** `screenshots/screenshot_05_external_inference_api.png`
* **Command to run in PowerShell:**
  ```powershell
  python -c "import requests, json; r=requests.post('http://localhost:30500/predict', json={'features':[62,1,3,145,233,1,0,150,0,2.3,0,0,1,0]}); print(json.dumps(r.json(), indent=2))"
  ```
* **What to capture:** The terminal displaying `predicted_label: Critical Risk`, `confidence_score: 1.0`, latency, and class probability distribution.

---

### Screenshot 6: Clinician Streamlit Web Dashboard in Browser
* **Filename:** `screenshots/screenshot_06_frontend_dashboard_ui.png`
* **Action:**
  1. Open your web browser (Chrome, Edge, or Brave).
  2. Navigate to: `http://localhost:31501`
  3. Enter patient vital parameters and click **"Run Model Inference"**.
  4. Capture the full browser window showing the predicted risk banner, metrics, and probabilities.

---

### Screenshot 7: Horizontal Pod Scaling & Self-Healing Resiliency
* **Filename:** `screenshots/screenshot_07_pod_scaling_and_healing.png`
* **Command to run in PowerShell:**
  ```powershell
  kubectl scale deployment/dl-backend-deployment --replicas=3 -n dl-production-app
  kubectl get pods -n dl-production-app -l app=dl-backend
  kubectl delete pod <pod-name> -n dl-production-app --grace-period=0 --force
  Start-Sleep -Seconds 3
  kubectl get pods -n dl-production-app -l app=dl-backend
  ```
* **What to capture:** The terminal showing the deployment scaled to 3 pods, followed by pod termination and immediate auto-recovery by Kubernetes ReplicaSet.

---

### Step to Recompile Reports After Adding Your Screenshots
Whenever you replace or update any screenshot file in `screenshots/`, simply run:
```powershell
python Task_13_Kubernetes_Deployment/build_task13_doc.py
```
This will automatically re-render both `Task_13_Deep_Learning_Kubernetes_Deployment_Report.docx` and `Task_13_Deep_Learning_Kubernetes_Deployment_Report.pdf` with your custom screenshots embedded!

---

## 📊 6. Automated Test Verification Results (10/10)

| ID | Test Case | Status | Verification Summary |
|:---:|:---|:---:|:---|
| **T01** | Cluster & Node Readiness | **PASSED** | Minikube control-plane node in `Ready` state. |
| **T02** | Production ConfigMap | **PASSED** | Centralized `dl-production-config` with 8 decoupled keys. |
| **T03** | PyTorch Backend Rollout | **PASSED** | Multi-replica backend deployed with active health probes. |
| **T04** | Streamlit Frontend Rollout | **PASSED** | Multi-replica web interface serving clinical dashboard. |
| **T05** | Service Port Mappings | **PASSED** | NodePort configured (:30500 for API, :31501 for UI). |
| **T06** | External Backend Health | **PASSED** | HTTP 200 OK: `DeepHealthRiskNet` model loaded on CPU. |
| **T07** | External Frontend Access | **PASSED** | HTTP 200 OK on external NodePort port 31501. |
| **T08** | Deep Learning Inference | **PASSED** | Live REST API inference evaluated in 0.81ms with 100% confidence. |
| **T09** | Horizontal Pod Scaling | **PASSED** | Dynamically scaled backend to 3 replicas with zero downtime. |
| **T10** | Pod Self-Healing | **PASSED** | Pod termination detected; replacement pod auto-provisioned in 3s. |

**Overall Result: 10 / 10 Tests Passed (100.0% Pass Rate)**

---

## 🏆 7. Evaluation Criteria Compliance

- **Successful Deployment:** Deployed PyTorch DeepHealthRiskNet and Streamlit microservices into an isolated Kubernetes namespace with zero rollout failures.
- **Service Accessibility:** Verified external connectivity and inference execution over exposed NodePort services (:30500 and :31501).
- **Configuration Quality:** Declarative manifests featuring CPU/memory resource limits (preventing OOMKills), readiness/liveness probes, and decoupled ConfigMaps.
- **Submission Formats:** Interactive Jupyter Notebook (`.ipynb`), Word Report (`.docx`), PDF Report (`.pdf`), and complete reproducible manifests.
