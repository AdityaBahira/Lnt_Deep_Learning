"""
5_System_Status.py
------------------
Page 5: System Health Inspector, Flask REST API Probe, Latency Benchmarker, and Cloud Deployment Guide.
"""

import time
import streamlit as st
import requests

from utils import ModelConnector

st.markdown("## ⚙️ System Health & API Inspector")
st.markdown("Monitor backend service status, ping endpoints, benchmark forward-pass latency, and inspect API documentation.")

st.markdown("---")

@st.cache_resource
def get_connector():
    return ModelConnector(api_url="http://127.0.0.1:5000")

connector = get_connector()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🖥️ Local Flask REST API Probe")
    st.write("Target Endpoint: `http://127.0.0.1:5000/health`")
    
    if st.button("🔄 Ping Flask REST API Server"):
        is_healthy, info = connector.check_api_health()
        if is_healthy:
            st.success("🟢 **Flask REST API is ONLINE and Healthy!**")
            st.json(info)
        else:
            st.warning("🔴 **Flask REST API is OFFLINE** (Direct PyTorch Engine is active).")
            st.json(info)

    st.markdown("---")
    st.subheader("⏱️ Real-Time Inference Latency Benchmarker")
    if st.button("⚡ Run Latency Benchmark (10 Inferences)"):
        test_vec = [45.0, 170.0, 75.0, 25.95, 6500.0, 2400.0, 6.8, 78.0, 128.0, 82.0, 2.5, 4.0, 0.0, 0.0]
        latencies = []
        for _ in range(10):
            t0 = time.time()
            connector.predict_direct(test_vec)
            latencies.append((time.time() - t0) * 1000)
        
        avg_lat = sum(latencies) / len(latencies)
        st.metric("⚡ Average Latency (10 runs)", f"{avg_lat:.2f} ms")
        st.caption(f"Min: {min(latencies):.2f} ms | Max: {max(latencies):.2f} ms")

with col2:
    st.subheader("☁️ Flask Cloud Deployment Guide")
    st.info("""
    **To host your Flask API on a free cloud platform (e.g. Render, Railway, or PythonAnywhere):**
    
    1. **Render.com Deployment**:
       - Connect your GitHub repo (`AdityaBahira/Lnt_Deep_Learning`).
       - Set Root Directory to `Backend/` or `Task_4_Developing_a_Flask_API_for_Deep_Learning_Models/`.
       - Build Command: `pip install -r requirements.txt`
       - Start Command: `python app.py` or `gunicorn app:app`
       
    2. **Connect Cloud URL to Streamlit**:
       - Update `api_url` in `utils.py` to point to your deployed URL (e.g. `https://your-flask-api.onrender.com`).
    """)

st.markdown("---")
st.subheader("📖 REST API Endpoints Specification")
endpoints_df = [
    {"Method": "GET", "Endpoint": "/", "Description": "Returns service status, version, and API landing details."},
    {"Method": "GET", "Endpoint": "/health", "Description": "Server readiness probe checking if PyTorch model is loaded."},
    {"Method": "POST", "Endpoint": "/predict", "Description": "Inference endpoint accepting 14-feature vector JSON payloads."},
    {"Method": "GET", "Endpoint": "/docs", "Description": "Interactive HTML Swagger documentation page."}
]
st.table(endpoints_df)
