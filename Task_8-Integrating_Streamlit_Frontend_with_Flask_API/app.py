"""
app.py
------
Task 8: Streamlit Frontend integrated with Flask REST API Backend.
Main entry point configuring multi-page navigation and global Flask API connection controls.
"""

import streamlit as st
from utils import ModelConnector

# 1. Configure Global Page Specs
st.set_page_config(
    page_title="Clinical DL Platform | Task 8 Integration",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Session State Initialization for Connection Controls
if "connection_mode" not in st.session_state:
    st.session_state.connection_mode = "Flask REST API 🌐"

if "api_url" not in st.session_state:
    st.session_state.api_url = "http://127.0.0.1:5000"

# 3. Global Connector Cache
@st.cache_resource
def get_connector(url):
    return ModelConnector(default_api_url=url)

connector = get_connector(st.session_state.api_url)

# 4. Sidebar Connection Engine Control Panel
st.sidebar.title("🩺 Clinical DL Platform")
st.sidebar.caption("Task 8: Streamlit + Flask REST API Integration")
st.sidebar.divider()

st.sidebar.subheader("🔌 Backend Connection Control")

conn_choice = st.sidebar.radio(
    "Select Inference Backend:",
    ["Flask REST API 🌐", "Direct PyTorch Engine 🧠"],
    index=0 if st.session_state.connection_mode.startswith("Flask") else 1,
    help="Choose whether to route predictions through HTTP requests to Flask REST API or directly execute PyTorch in-memory."
)
st.session_state.connection_mode = conn_choice

if conn_choice.startswith("Flask"):
    api_url_input = st.sidebar.text_input(
        "Flask API Base URL:",
        value=st.session_state.api_url,
        help="Target URL of the running Flask REST API service."
    )
    st.session_state.api_url = api_url_input

    # Probe Health
    health = connector.check_api_health(st.session_state.api_url)
    if health.get("online"):
        st.sidebar.success(f"🟢 **Flask API Online** ({health.get('rtt_ms', 0)} ms)")
        st.sidebar.caption(f"Device: `{health.get('device', 'cpu')}` | Model: `{health.get('model_name', 'DeepHealthRiskNet')}`")
    else:
        st.sidebar.error("🔴 **Flask API Offline**")
        st.sidebar.caption(f"Reason: {health.get('message', 'Connection failed')}")
        st.sidebar.warning("⚠️ Please start Flask API (`python flask_api.py`) or switch to Direct PyTorch Engine above.")

else:
    st.sidebar.info("🧠 **Direct In-Memory Engine Active**")
    st.sidebar.caption("PyTorch forward pass executed directly in Streamlit process.")

st.sidebar.divider()
st.sidebar.info("💡 **Task 8 Navigation**: Select a page from the menu above to execute single patient inference, cohort batch API evaluation, analytics, or API diagnostics.")

# 5. Configure Multi-Page Navigation System using views/ subfolder
pages = {
    "Navigation Menu": [
        st.Page("views/1_Overview.py", title="Executive Overview & Architecture", icon="🏠", url_path="overview"),
        st.Page("views/2_Prediction.py", title="Single Patient API Predictor", icon="🔮", url_path="prediction"),
        st.Page("views/3_Batch_Processing.py", title="Cohort CSV Batch API Ingestion", icon="📁", url_path="batch-cohort"),
        st.Page("views/4_Analytics.py", title="Model & API Latency Analytics", icon="📊", url_path="analytics-dashboard"),
        st.Page("views/5_System_Status.py", title="Flask API Health Diagnostics", icon="⚙️", url_path="system-status"),
    ]
}

pg = st.navigation(pages)
pg.run()
