"""
app.py
------
Task 7: Advanced Multi-Page Streamlit Deep Learning Application.
Main Entry Point configuring page navigation using views/ directory.
Prevents _mpa_v1 auto-discovery URL collisions on Streamlit Cloud.
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
    return ModelConnector()

connector = get_connector()

# 3. Configure Multi-Page Navigation System using views/ subfolder
pages = {
    "Navigation Menu": [
        st.Page("views/1_Overview.py", title="Executive Overview & Neural Net", icon="🏠", url_path="overview"),
        st.Page("views/2_Prediction.py", title="Single Patient Clinical Predictor", icon="🔮", url_path="prediction"),
        st.Page("views/3_Batch_Processing.py", title="Cohort CSV Ingestion & Report", icon="📁", url_path="batch-cohort"),
        st.Page("views/4_Analytics.py", title="Model Performance Dashboard", icon="📊", url_path="analytics-dashboard"),
        st.Page("views/5_System_Status.py", title="System Health & Diagnostics", icon="⚙️", url_path="system-status"),
    ]
}

# Sidebar Global Info Header
st.sidebar.title("🩺 Clinical DL System")
st.sidebar.caption("PyTorch DeepHealthRiskNet Platform")
st.sidebar.divider()

st.sidebar.subheader("🔌 Connection Engine")
st.sidebar.success("🟢 PyTorch DL Engine Active")
st.sidebar.caption("Direct in-memory neural network inference mode.")

st.sidebar.divider()
st.sidebar.info("💡 **Task 7 Multi-Page App**: Select a page from the Navigation Menu above to view Overview, Risk Prediction, Batch Cohort Ingestion, Analytics Dashboard, or System Health.")

# Run Navigation System
pg = st.navigation(pages)
pg.run()
