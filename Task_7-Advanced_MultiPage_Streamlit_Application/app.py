"""
app.py
------
Task 7: Advanced Multi-Page Streamlit Deep Learning Application.
Main Entry Point configuring page navigation, theme customization, and global model engine status.
"""

import streamlit as st
from utils import ModelConnector

# 1. Configure Global Page & Theme Specs
st.set_page_config(
    page_title="🩺 Clinical DL Platform | Task 7",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for Multi-Page Navigation
st.markdown("""
    <style>
    .stAppViewContainer {
        background-color: #FAFAFA;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1E3A8A;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Shared Connector Resource
@st.cache_resource
def get_connector():
    return ModelConnector(api_url="http://127.0.0.1:5000")

connector = get_connector()

# 3. Configure Multi-Page Navigation System
pages = {
    "Navigation Menu": [
        st.Page("pages/1_Overview.py", title="Executive Overview & Neural Net", icon="🏠"),
        st.Page("pages/2_Prediction.py", title="Single Patient Clinical Predictor", icon="🔮"),
        st.Page("pages/3_Analytics.py", title="Model Performance Dashboard", icon="📊"),
        st.Page("pages/4_Batch_Processing.py", title="Cohort CSV Ingestion & Report", icon="📁"),
        st.Page("pages/5_System_Status.py", title="System Health & API Inspector", icon="⚙️"),
    ]
}

# Sidebar Global Info Header
st.sidebar.image("https://img.icons8.com/color/96/000000/medical-heart.png", width=65)
st.sidebar.markdown('<div class="sidebar-header">🩺 Clinical DL System</div>', unsafe_allow_html=True)
st.sidebar.caption("PyTorch DeepHealthRiskNet Platform")
st.sidebar.markdown("---")

# Execution Mode Selector (Shared state)
if "conn_mode" not in st.session_state:
    st.session_state["conn_mode"] = "🧠 Direct PyTorch Engine"

st.sidebar.subheader("🔌 Model Connection Engine")
selected_mode = st.sidebar.radio(
    "Inference Engine Mode:",
    ["🧠 Direct PyTorch Engine", "🌐 Flask REST API Endpoint"],
    index=0 if "Direct" in st.session_state["conn_mode"] else 1
)
st.session_state["conn_mode"] = selected_mode

st.sidebar.markdown("---")
# Quick API Health Indicator in Sidebar
api_healthy, health_info = connector.check_api_health()
if api_healthy:
    st.sidebar.success("🟢 Flask REST API Online")
else:
    st.sidebar.warning("🔴 Flask REST API Offline (Direct Fallback Active)")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Task 7 Multi-Page App**: Use the navigation menu above to switch between Overview, Risk Prediction, Analytics Dashboard, Batch Processing, and System Status.")

# Run Navigation System
pg = st.navigation(pages)
pg.run()
