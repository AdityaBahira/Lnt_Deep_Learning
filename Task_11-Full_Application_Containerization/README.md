# Task 11: Full Application Containerization & Docker Hub Deployment

## 🩺 Clinical Deep Learning Platform (DeepHealthRiskNet)

This directory contains the production-grade containerization setup for the complete Clinical Deep Learning system, decoupling the **Flask REST API (PyTorch Inference Engine)** and **Streamlit Clinical UI (Frontend)** into isolated, network-orchestrated microservices.

---

## 📁 Directory Structure

```text
Task_11_Deployment/
├── backend/
│   ├── flask_api.py            # Flask REST API endpoints (/health, /predict, /predict/batch)
│   ├── model_loader.py         # PyTorch DeepHealthRiskNet inference engine
│   ├── saved_models/
│   │   ├── config.json         # Feature scaling and training metadata
│   │   └── dl_model.pt         # Saved neural network model weights
│   ├── requirements.txt        # Backend dependencies (PyTorch CPU, Flask, scikit-learn)
│   └── Dockerfile              # Backend container build specification
├── frontend/
│   ├── app.py                  # Streamlit main entrypoint & navigation
│   ├── views/                  # Multi-page clinical dashboards
│   │   ├── 1_Overview.py
│   │   ├── 2_Prediction.py
│   │   ├── 3_Batch_Processing.py
│   │   ├── 4_Analytics.py
│   │   └── 5_System_Status.py
│   ├── utils.py                # ModelConnector & data handling utilities
│   ├── health_activity_data.csv # Cohort analytics dataset
│   ├── sample_cohort_data.csv  # Batch testing sample dataset
│   ├── requirements.txt        # Frontend dependencies (Streamlit, Plotly, Pandas)
│   └── Dockerfile              # Frontend container build specification
├── docker-compose.yml          # Multi-container orchestration (recommended)
├── Dockerfile.allinone         # Optional single-container unified deployment
├── supervisord.conf            # Process manager for single-container option
├── .dockerignore               # Build optimization exclusions
└── README.md                   # Complete deployment & execution guide
```

---

## 🚀 Quick Start Instructions

### Option A: Multi-Container Setup with Docker Compose (Recommended)

1. **Navigate to the deployment directory:**
   ```bash
   cd "E:\DL_deploy\Task_11_Deployment"
   ```

2. **Build and start services locally:**
   ```bash
   docker compose build
   docker compose up -d
   ```

3. **Verify running containers:**
   ```bash
   docker ps
   ```

4. **Verify Health and UI:**
   - **Flask API Health:** Open [http://localhost:5000/health](http://localhost:5000/health) or run `curl http://localhost:5000/health`
   - **Streamlit Web Dashboard:** Open [http://localhost:8501](http://localhost:8501) in your browser

5. **Stop containers when needed:**
   ```bash
   docker compose down
   ```

---

## 🐳 Pushing to Docker Hub

1. **Login to Docker Hub in your terminal:**
   ```bash
   docker login -u <your_dockerhub_username>
   ```

2. **Tag the images for Docker Hub:**
   ```bash
   docker tag dl_clinical_backend:v1.0 <your_dockerhub_username>/dl-clinical-backend:v1.0
   docker tag dl_clinical_frontend:v1.0 <your_dockerhub_username>/dl-clinical-frontend:v1.0
   ```
   *(Or set `$env:DOCKER_USERNAME="<your_dockerhub_username>"` before running `docker compose build`)*

3. **Push both images to Docker Hub:**
   ```bash
   docker push <your_dockerhub_username>/dl-clinical-backend:v1.0
   docker push <your_dockerhub_username>/dl-clinical-frontend:v1.0
   ```

4. **Public Verification:**
   Ensure repositories on [Docker Hub](https://hub.docker.com/) are set to **Public** for evaluation.

---

### Option B: Optional Single-Container Deployment (All-in-One)

If your evaluator specifically requests a single Docker image:
```bash
docker build -f Dockerfile.allinone -t <your_dockerhub_username>/dl-clinical-allinone:v1.0 .
docker run -d -p 5000:5000 -p 8501:8501 --name clinical_allinone <your_dockerhub_username>/dl-clinical-allinone:v1.0
```
