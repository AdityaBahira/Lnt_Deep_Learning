"""
views/5_MLOps_Monitoring.py
---------------------------
Kubernetes Cluster Health, Latency Benchmarking, and MLOps Performance Monitoring.
"""

import time
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import check_backend_health

st.title("⚙️ Kubernetes & Cluster Telemetry")
st.markdown("Monitor cloud-native cluster health, latency variance, and pod availability.")

st.subheader("1. Real-Time Microservice Health Probe")
url = st.session_state.get("backend_url", "http://localhost:5000")

col1, col2 = st.columns([1, 2])
with col1:
    st.write(f"**Target Host:** `{url}`")
    ping_btn = st.button("🔄 Probe Service Latency", type="primary")

with col2:
    is_up, payload, rtt = check_backend_health(url)
    if is_up:
        st.success(f"🟢 **Service Available** — RTT: `{rtt:.1f} ms`")
        st.json(payload)
    else:
        st.error(f"🔴 **Service Unreachable** — Details: `{payload.get('error')}`")

st.markdown("---")
st.subheader("2. Real-Time Latency Benchmark")
st.markdown("Execute 10 consecutive requests to measure API stability and round-trip consistency.")

if st.button("📊 Run 10-Request Latency Profiler"):
    latencies = []
    statuses = []
    
    prog = st.progress(0.0)
    for i in range(10):
        t0 = time.time()
        try:
            r = requests.get(f"{url}/health", timeout=2.0)
            ms = (time.time() - t0) * 1000.0
            latencies.append(ms)
            statuses.append(r.status_code)
        except Exception:
            latencies.append(0.0)
            statuses.append(503)
        prog.progress((i + 1) / 10.0)
        time.sleep(0.05)
        
    df_lat = pd.DataFrame({
        "Request Iteration": list(range(1, 11)),
        "Round-Trip Time (ms)": latencies,
        "HTTP Status": statuses
    })
    
    avg_l = sum(latencies) / len(latencies)
    min_l = min(latencies)
    max_l = max(latencies)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Average Latency", f"{avg_l:.1f} ms")
    c2.metric("Min Latency", f"{min_l:.1f} ms")
    c3.metric("Max Latency", f"{max_l:.1f} ms")
    
    theme = st.session_state.get("theme_mode", "light")
    fig = px.line(
        df_lat,
        x="Request Iteration",
        y="Round-Trip Time (ms)",
        markers=True,
        title="Microservice Response Latency Profile (10 Trials)",
        template="plotly_dark" if theme == "dark" else "plotly_white"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("3. Production Kubernetes Cluster Specifications")

st.markdown("""
| Component | Kubernetes Object | Configuration | Status |
| :--- | :--- | :--- | :--- |
| **Namespace** | `Namespace` | `dl-production-app` | Active |
| **Backend Microservice** | `Deployment` | 2 Replicas, Requests: 100m / 256Mi, Limits: 500m / 768Mi | High Availability |
| **Backend Internal Service** | `Service` (ClusterIP / NodePort) | Internal Port: 5000, NodePort: 30500 | CoreDNS Routing |
| **Frontend Web Interface** | `Deployment` | 2 Replicas, Requests: 100m / 256Mi | Redundant |
| **Frontend External Service** | `Service` (NodePort) | Internal Port: 8501, NodePort: 31501 | Public Node Exposure |
| **Autoscaling Policy** | `HorizontalPodAutoscaler` | Min: 2, Max: 5, Target CPU: 60% | Active Metrics-Server |
""")
