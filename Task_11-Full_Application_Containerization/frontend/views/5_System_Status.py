"""
5_System_Status.py
------------------
Page 5: System Health Diagnostics & Real-Time Flask REST API Probe.
Probes server availability, displays environment specs, and simulates REST API HTTP calls.
"""

import streamlit as st
import requests
import time
import json
from utils import ModelConnector

st.title("⚙️ System Health & Flask REST API Diagnostics")
st.write("Monitor Flask REST API readiness, probe HTTP health status, and simulate raw JSON payloads.")

st.divider()

api_url = st.session_state.get("api_url", "http://127.0.0.1:5000")

@st.cache_resource
def get_connector(url):
    return ModelConnector(default_api_url=url)

connector = get_connector(api_url)

st.subheader("🔌 Flask API Server Probe")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"**Target Flask Base URL**: `{api_url}`")
    if st.button("🔄 Execute Health & Readiness Probe", type="primary", use_container_width=True):
        st.rerun()

    health = connector.check_api_health(api_url)
    
    if health.get("online"):
        st.success(f"🟢 **Status: HEALTHY (HTTP 200 OK)**")
        st.metric("Round-Trip Time (RTT)", f"{health.get('rtt_ms', 0)} ms")
        
        st.subheader("🖥️ Backend System Specs")
        spec_df = {
            "Model Name": health.get("model_name", "N/A"),
            "PyTorch Execution Device": health.get("device", "N/A"),
            "Input Feature Count": health.get("feature_count", 14),
            "Target Risk Classes": ", ".join(health.get("classes", []))
        }
        for k, v in spec_df.items():
            st.markdown(f"- **{k}**: `{v}`")

    else:
        st.error("🔴 **Status: OFFLINE / UNREACHABLE**")
        st.warning(f"Error Details: {health.get('message', 'Failed to connect')}")
        st.info("💡 Make sure Flask API is running: `python flask_api.py`")

with col2:
    st.subheader("📡 Endpoint Probe Inspection (`GET /health`)")
    try:
        resp = requests.get(f"{api_url}/health", timeout=3.0)
        st.markdown(f"**HTTP Response Code**: `{resp.status_code} {resp.reason}`")
        st.json(resp.json())
    except Exception as e:
        st.error(f"Failed to probe GET /health: {str(e)}")

st.divider()
st.header("🧪 Interactive API Request Simulator")
st.write("Simulate raw HTTP requests to test Flask API endpoints directly from Streamlit UI.")

sim_endpoint = st.selectbox("Select Target Endpoint:", ["GET /", "GET /health", "POST /predict"])

if sim_endpoint == "GET /":
    if st.button("Send GET / Request"):
        try:
            r = requests.get(f"{api_url}/")
            st.markdown(f"**Status Code**: `{r.status_code}`")
            st.json(r.json())
        except Exception as e:
            st.error(str(e))

elif sim_endpoint == "GET /health":
    if st.button("Send GET /health Request"):
        try:
            r = requests.get(f"{api_url}/health")
            st.markdown(f"**Status Code**: `{r.status_code}`")
            st.json(r.json())
        except Exception as e:
            st.error(str(e))

elif sim_endpoint == "POST /predict":
    raw_json_input = st.text_area(
        "Enter Raw JSON Request Payload:",
        value=json.dumps({
            "features": [45.0, 170.0, 75.0, 25.95, 6500.0, 2400.0, 6.8, 78.0, 128.0, 82.0, 2.5, 4.0, 0.0, 0.0]
        }, indent=2),
        height=180
    )
    if st.button("Send POST /predict Request"):
        try:
            payload = json.loads(raw_json_input)
            r = requests.post(f"{api_url}/predict", json=payload, headers={"Content-Type": "application/json"})
            st.markdown(f"**Status Code**: `{r.status_code}`")
            st.json(r.json())
        except Exception as e:
            st.error(f"Error executing request: {str(e)}")
