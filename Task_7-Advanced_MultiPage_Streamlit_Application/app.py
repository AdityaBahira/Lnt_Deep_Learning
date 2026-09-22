"""
app.py
------
Task 7: Advanced Multi-Page Streamlit Deep Learning Application.
Main Entry Point configuring page navigation with explicit unique url_path attributes.
"""

import streamlit as st
from utils import ModelConnector

# 1. Configure Global Page Specs
st.set_page_config(
    page_title="Clinical DL Platform | Task 7",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Shared Connector Resource
@st.cache_resource
def get_connector():
    return ModelConnector(api_url="http://127.0.0.1:5000")

connector = get_connector()

# 3. Configure Multi-Page Navigation System with Explicit Unique URL Pathnames
pages = {
    "Navigation Menu": [
        st.Page("pages/1_Overview.py", title="Executive Overview & Neural Net", icon="🏠", url_path="overview"),
        st.Page("pages/2_Prediction.py", title="Single Patient Clinical Predictor", icon="🔮", url_path="prediction"),
        st.Page("pages/3_Batch_Processing.py", title="Cohort CSV Ingestion & Report", icon="📁", url_path="batch-cohort"),
        st.Page("pages/4_Analytics.py", title="Model Performance Dashboard", icon="📊", url_path="analytics"),
        st.Page("pages/5_System_Status.py", title="System Health & API Inspector", icon="⚙️", url_path="system-status"),
    ]
}

# Sidebar Global Info Header
st.sidebar.title("🩺 Clinical DL System")
st.sidebar.caption("PyTorch DeepHealthRiskNet Platform")
st.sidebar.divider()

# Execution Mode Selector (Shared state)
if "conn_mode" not in st.session_state:
    st.session_state["conn_mode"] = "🧠 Direct PyTorch Engine"

st.sidebar.subheader("🔌 Connection Engine")
selected_mode = st.sidebar.radio(
    "Inference Engine Mode:",
    ["🧠 Direct PyTorch Engine", "🌐 Flask REST API Endpoint"],
    index=0 if "Direct" in st.session_state["conn_mode"] else 1
)
st.session_state["conn_mode"] = selected_mode

st.sidebar.divider()
# Quick API Health Indicator in Sidebar
api_healthy, health_info = connector.check_api_health()
if api_healthy:
    st.sidebar.success("🟢 Flask REST API Online")
else:
    st.sidebar.warning("🔴 Flask REST API Offline (Direct Fallback Active)")

st.sidebar.divider()
st.sidebar.info("💡 **Task 7 Multi-Page App**: Select a page from the Navigation Menu above to view Overview, Risk Prediction, Batch Cohort Ingestion, Analytics Dashboard, or System Health.")

# Run Navigation System
pg = st.navigation(pages)
pg.run()
