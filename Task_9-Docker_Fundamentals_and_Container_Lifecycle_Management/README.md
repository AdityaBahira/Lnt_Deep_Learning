# Task 9: Docker Fundamentals and Container Lifecycle Management

## 📌 Project Overview
This task demonstrates Docker architecture, container lifecycle management, storage volumes, and bridge networking using an official **lightweight image** (`python:3.10-slim`, **~125 MB**, far less than 1GB) pulled directly from **Docker Hub Registry**.

---

## 🚀 Complete Command Execution Steps

### Phase A: Environment & Architecture Check
```bash
docker --version
docker info
```

### Phase B: Pull & Explore Lightweight Image from Docker Hub (~125 MB)
```bash
# Pull official lightweight Python 3.10 image from Docker Hub
docker pull python:3.10-slim

# List local image cache
docker images

# Inspect image metadata & layer architecture
docker inspect python:3.10-slim

# Tag image for local runtime alias
docker tag python:3.10-slim my_dl_runtime:v1
```

### Phase C: Storage & Networking Setup
```bash
# Create persistent storage volume
docker volume create dl_storage_vol
docker volume ls

# Create isolated bridge network
docker network create dl_bridge_net
docker network ls
```

### Phase D: Container Lifecycle Operations
```bash
# Run container in detached mode using lightweight image
docker run -d --name dl_runtime_container -v dl_storage_vol:/workspace --network dl_bridge_net python:3.10-slim python -c "import time, sys; print('Lightweight Deep Learning Runtime Initialized'); sys.stdout.flush(); time.sleep(3600)"

# List active containers
docker ps

# Execute command inside container
docker exec dl_runtime_container python -c "import sys, platform; print('Python Version:', sys.version.split()[0]); print('Platform:', platform.platform())"

# Read container logs
docker logs dl_runtime_container

# Pause & Unpause container
docker pause dl_runtime_container
docker ps
docker unpause dl_runtime_container

# Monitor live resource stats
docker stats dl_runtime_container --no-stream

# Stop, Start & Restart container
docker stop dl_runtime_container
docker ps -a
docker start dl_runtime_container
docker restart dl_runtime_container
```

### Phase E: Cleanup Operations
```bash
docker stop dl_runtime_container
docker rm dl_runtime_container
docker volume rm dl_storage_vol
docker network rm dl_bridge_net
docker rmi my_dl_runtime:v1
```
