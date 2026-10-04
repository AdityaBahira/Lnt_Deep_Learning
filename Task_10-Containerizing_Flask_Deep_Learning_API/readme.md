# Task 10 – Containerizing Flask Deep Learning API

## Project Overview

This project demonstrates the containerization and deployment of a Flask-based Deep Learning API using Docker.

The application loads a trained deep learning model and provides REST API endpoints for health monitoring, prediction, and API documentation.

The Dockerized application can be built locally, tested through REST APIs, and distributed through Docker Hub.

## Objective

The objective of this task is to package a Flask-based deep learning application into a Docker container and verify its deployment locally.

### Main Objectives

- Create a Dockerfile for the Flask application
- Configure application dependencies
- Build a Docker image
- Run the application inside a Docker container
- Test the REST API
- Monitor the running container
- Perform Docker image inspection and optimization
- Make the Docker image available through Docker Hub

## Technologies Used

- Python
- Flask
- PyTorch
- NumPy
- Docker
- Docker Desktop
- REST API
- Docker Hub

## Project Structure

    Task-10-Containerizing-Flask-Deep-Learning-API/
    │
    ├── app.py
    ├── model_loader.py
    ├── test_client.py
    ├── requirements.txt
    ├── Dockerfile
    ├── .dockerignore
    │
    ├── saved_models/
    │   └── trained model files
    │
    └── report/
        └── Task_10_Containerizing_Flask_Deep_Learning_API_Report.pdf

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Displays API/service information |
| GET | `/health` | Checks API and model health |
| POST | `/predict` | Generates a prediction |
| GET | `/docs` | Displays API documentation |

# Docker Setup

## 1. Build Docker Image

Navigate to the project directory and build the Docker image:

    docker build -t health-risk-flask-api:1.0 .

Check the image:

    docker images

## 2. Run Docker Container

    docker run -d --name health-risk-api -p 5000:5000 health-risk-flask-api:1.0

Check the running container:

    docker ps

## 3. View Container Logs

    docker logs health-risk-api

For live logs:

    docker logs -f health-risk-api

# API Testing

## Root Endpoint

    curl http://localhost:5000/

## Health Endpoint

    curl http://localhost:5000/health

The health endpoint verifies that the Flask application and deep learning model are loaded correctly.

## Prediction Endpoint

The `/predict` endpoint accepts feature values in JSON format.

### PowerShell

    curl.exe -X POST "http://localhost:5000/predict" -H "Content-Type: application/json" -d '{"features":[55.0,29.4,135.0,140.0,240.0,82.0,2.5,6.0]}'

The API returns the prediction result in JSON format.

## API Documentation

Open the following URL in a web browser:

http://localhost:5000/docs

# Container Monitoring

Monitor CPU, memory, network, and other resource usage:

    docker stats health-risk-api --no-stream

# Container Lifecycle

## Stop Container

    docker stop health-risk-api

## Start Container

    docker start health-risk-api

## Restart Container

    docker restart health-risk-api

## Remove Container

    docker rm -f health-risk-api

# Docker Image Inspection and Optimization

View image layers:

    docker history health-risk-flask-api:1.0

Inspect image configuration:

    docker inspect health-risk-flask-api:1.0

Check Docker disk usage:

    docker system df

These commands help inspect the Docker image structure and identify Docker storage usage.

# Docker Hub

The Docker image is available on Docker Hub for distribution and deployment.

## Pull the Docker Image

Anyone with Docker installed can download the image using:

    docker pull YOUR_USERNAME/health-risk-flask-api:1.0

## Run the Docker Image

After pulling the image, run the application using:

    docker run -d --name health-risk-api -p 5000:5000 YOUR_USERNAME/health-risk-flask-api:1.0

## Check the Running Container

    docker ps

## Check API Health

    curl http://localhost:5000/health

## Open API Documentation

Open the following URL in a web browser:

http://localhost:5000/docs

## Test Prediction

    curl.exe -X POST "http://localhost:5000/predict" -H "Content-Type: application/json" -d '{"features":[55.0,29.4,135.0,140.0,240.0,82.0,2.5,6.0]}'

## Docker Hub Image

**Image:** `YOUR_USERNAME/health-risk-flask-api:1.0`

Replace `YOUR_USERNAME` with the Docker Hub username that owns the repository.

# Results

The Flask-based deep learning API was successfully containerized using Docker.

The application was tested through its REST API endpoints, including:

- Root endpoint
- Health endpoint
- Prediction endpoint
- API documentation endpoint

The Docker image is also available through Docker Hub for container distribution and deployment.

# Observations

- Docker provides an isolated environment for the Flask application.
- Application dependencies are packaged inside the Docker image.
- The Flask API can be accessed through the exposed port `5000`.
- Docker commands allow the application container to be started, stopped, restarted, and monitored.
- Docker image layers can be inspected using Docker commands.
- Docker Hub provides a convenient way to distribute and deploy the containerized application.

# Author

**Aditya Bahira**

MSc Data Science & Big Data Analytics

## Academic Practical

**L&T Edutech – Deep Learning Deployment**

**Task 10: Containerizing Flask Deep Learning API**
