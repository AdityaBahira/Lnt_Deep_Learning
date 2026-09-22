"""
5_System_Status.py
------------------
Page 5: System Health Inspector, Model Diagnostics, Latency Benchmarker, and REST API Specifications.
"""

import time
import streamlit as st
import pandas as pd

from utils import ModelConnector

st.title("⚙️ System Health & API Inspector")
st.write("Monitor backend service status, ping REST endpoints, benchmark forward-pass latency, and inspect API specifications.")

st.divider()

@st.cache_resource
def get_connector():
    return ModelConnector(api_url="http://127.0.0.1:5000")

connector = get_connector()

col1, col2 = st.columns(2)

with col1:
    st.header("🖥️ REST API Server Health Probe")
    st.write("Target Endpoint: `http://127.0.0.1:5000/health`")
    
    if st.button("🔄 Ping Flask REST API Server", use_container_width=True):
        is_healthy, info = connector.check_api_health()
        if is_healthy:
            st.success("🟢 **Flask REST API is ONLINE and Healthy!**")
            st.json(info)
        else:
            st.warning("🔴 **Flask REST API is OFFLINE** (Direct PyTorch Engine is active).")
            st.json(info)

with col2:
    st.header("⏱️ Real-Time Inference Latency Benchmarker")
    st.write("Measures in-memory PyTorch forward-pass execution latency across 10 sample iterations.")
    if st.button("⚡ Run Latency Benchmark (10 Inferences)", use_container_width=True, type="primary"):
        test_vec = [45.0, 170.0, 75.0, 25.95, 6500.0, 2400.0, 6.8, 78.0, 128.0, 82.0, 2.5, 4.0, 0.0, 0.0]
        latencies = []
        for _ in range(10):
            t0 = time.time()
            connector.predict_direct(test_vec)
            latencies.append((time.time() - t0) * 1000)
        
        avg_lat = sum(latencies) / len(latencies)
        st.metric("⚡ Average Latency (10 runs)", f"{avg_lat:.2f} ms")
        st.caption(f"Min: {min(latencies):.2f} ms | Max: {max(latencies):.2f} ms")

st.divider()
st.header("📖 REST API Endpoints Specification")
endpoints_df = pd.DataFrame([
    {"Method": "GET", "Endpoint": "/", "Description": "Returns service status, version, and API landing details."},
    {"Method": "GET", "Endpoint": "/health", "Description": "Server readiness probe checking if PyTorch model is loaded."},
    {"Method": "POST", "Endpoint": "/predict", "Description": "Inference endpoint accepting 14-feature vector JSON payloads."},
    {"Method": "GET", "Endpoint": "/docs", "Description": "Interactive HTML Swagger documentation page."}
])
st.dataframe(endpoints_df, use_container_width=True)
