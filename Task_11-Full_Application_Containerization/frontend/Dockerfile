# ====================================================
# Frontend Dockerfile: Streamlit Clinical Dashboard
# ====================================================
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

WORKDIR /app

# Install curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install frontend requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit application code, views, utils, and datasets
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Streamlit internal health probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Launch Streamlit server
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
