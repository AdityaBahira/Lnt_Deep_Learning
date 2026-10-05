"""
app.py
------
Task 15: Master Streamlit Production Web Interface.
Orchestrates multi-page clinical diagnostics, vision inference, biomarker analytics,
and real-time Kubernetes cluster monitoring.
"""

import os
import streamlit as st
from utils import get_active_backend_url, check_backend_health

# 1. Global Page Configuration
st.set_page_config(
    page_title="DeepMed-Vision | Production Deep Learning Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Session State Initialization
if "backend_url" not in st.session_state:
    st.session_state.backend_url = get_active_backend_url()

# 3. Sidebar Header & Global Status
st.sidebar.title("🏥 DeepMed-Vision")
st.sidebar.caption("L&T Edutech Capstone — Task 15 Production Deployment")
st.sidebar.markdown("---")

st.sidebar.subheader("🔌 Backend Connection")
backend_input = st.sidebar.text_input(
    "REST API Endpoint:",
    value=st.session_state.backend_url,
    help="Target URL of the containerized Flask inference microservice."
)
st.session_state.backend_url = backend_input

is_healthy, health_data, latency_ms = check_backend_health(st.session_state.backend_url)
if is_healthy:
    st.sidebar.success(f"🟢 **API Online** ({latency_ms:.1f} ms)")
    v_name = health_data.get("vision_model", {}).get("name", "DeepMedVisionNet")
    st.sidebar.caption(f"Hardware: `{health_data.get('hardware_device', 'cpu')}` | Model: `{v_name}`")
else:
    st.sidebar.warning("🟡 **Standalone Mode** (Using Direct PyTorch Fallback)")
    st.sidebar.caption("Backend unreachable; local engine active.")

st.sidebar.markdown("---")
st.sidebar.info("""
**Candidate:** Aditya Bahira  
**Curriculum:** Deep Learning & MLOps  
**Cluster:** Kubernetes / Minikube  
""")

# 4. Multi-Page Navigation via st.navigation
pages = {
    "Diagnostics": [
        st.Page("views/1_Overview.py", title="Overview & Architecture", icon="🏛️"),
        st.Page("views/2_Image_Classification.py", title="Radiological Vision Diagnostics", icon="🩻"),
        st.Page("views/3_Clinical_Risk_Predictor.py", title="Biomarker Risk Predictor", icon="🩺"),
    ],
    "Operations": [
        st.Page("views/4_Batch_Analytics.py", title="Batch Screening & Export", icon="📁"),
        st.Page("views/5_MLOps_Monitoring.py", title="Kubernetes & Cluster Telemetry", icon="⚙️"),
    ]
}

nav = st.navigation(pages)
nav.run()
