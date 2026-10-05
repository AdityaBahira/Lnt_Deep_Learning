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
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "light"

# 3. Sidebar Header & Global Status
st.sidebar.title("🏥 DeepMed-Vision")
st.sidebar.caption("L&T Edutech Capstone — Task 15 Production Deployment")
st.sidebar.markdown("---")

# Theme Toggle
st.sidebar.subheader("🎨 Appearance")
theme_choice = st.sidebar.radio(
    "Theme Display Mode:",
    ["☀️ Light Mode", "🌙 Dark Mode"],
    index=0 if st.session_state.theme_mode == "light" else 1,
    horizontal=True,
    help="Toggle between Clean Clinical Light Mode and Dark Mode."
)
selected_theme = "light" if "Light" in theme_choice else "dark"
if selected_theme != st.session_state.theme_mode:
    st.session_state.theme_mode = selected_theme
    st.rerun()

# Dynamic Theme CSS Injection
if st.session_state.theme_mode == "light":
    st.markdown("""
    <style>
    /* =========================================================================
       CLINICAL LIGHT MODE
       ========================================================================= */
    :root {
        --text-color: #0F172A !important;
        --background-color: #FFFFFF !important;
        --secondary-background-color: #F8FAFC !important;
    }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
    }
    [data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }
    
    /* Typography & Letters */
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    p, span, label, li, strong, b, em {
        color: #1E293B !important;
    }
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong {
        color: #1E293B !important;
    }
    
    /* Markdown Tables & Formatted Tables */
    table, [data-testid="stTable"] table, [data-testid="stMarkdownContainer"] table {
        width: 100% !important;
        border-collapse: collapse !important;
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        margin: 16px 0 !important;
    }
    thead tr, [data-testid="stMarkdownContainer"] thead tr {
        background-color: #F1F5F9 !important;
        border-bottom: 2px solid #CBD5E1 !important;
    }
    th, [data-testid="stMarkdownContainer"] th {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        border: 1px solid #CBD5E1 !important;
        text-align: left !important;
    }
    tbody tr, [data-testid="stMarkdownContainer"] tbody tr {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }
    tbody tr:nth-of-type(even), [data-testid="stMarkdownContainer"] tbody tr:nth-of-type(even) {
        background-color: #F8FAFC !important;
    }
    tbody tr:hover, [data-testid="stMarkdownContainer"] tbody tr:hover {
        background-color: #EFF6FF !important;
    }
    td, [data-testid="stMarkdownContainer"] td {
        color: #1E293B !important;
        padding: 12px 16px !important;
        border: 1px solid #E2E8F0 !important;
    }
    td strong, td b, th strong, th b {
        color: #1D4ED8 !important;
    }
    
    /* Code Blocks & Architecture Diagrams */
    pre, code, [data-testid="stCodeBlock"], [data-testid="stCodeBlock"] pre {
        background-color: #F8FAFC !important;
        color: #0369A1 !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }
    code {
        color: #1D4ED8 !important;
        background-color: #EFF6FF !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #0F172A !important;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
    }
    [data-testid="stMetricLabel"] * {
        color: #64748B !important;
    }
    [data-testid="stMetricValue"] * {
        color: #0F172A !important;
        font-weight: 700 !important;
    }
    
    /* Widget Labels & Controls */
    [data-testid="stWidgetLabel"] *,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        color: #0F172A !important;
        font-weight: 600 !important;
    }
    [data-testid="stRadio"] label, [data-testid="stRadio"] span, [data-testid="stRadio"] p,
    [data-testid="stCheckbox"] label, [data-testid="stCheckbox"] span, [data-testid="stCheckbox"] p {
        color: #1E293B !important;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] {
        color: #64748B !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB !important;
        border-bottom-color: #2563EB !important;
    }
    
    /* Alerts */
    [data-testid="stAlert"] p, [data-testid="stAlert"] span {
        color: #0F172A !important;
    }
    
    hr {
        border-color: #E2E8F0 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #64748B !important;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    /* =========================================================================
       HIGH-CONTRAST DARK MODE (Crisp Letters & Table Visibility)
       ========================================================================= */
    :root {
        --text-color: #F8FAFC !important;
        --background-color: #0E1117 !important;
        --secondary-background-color: #1E293B !important;
    }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0E1117 !important;
        color: #F8FAFC !important;
    }
    [data-testid="stHeader"] {
        background-color: #0E1117 !important;
    }
    
    /* Typography & Letters - Bright High Contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    p, span, label, li, strong, b, em {
        color: #F1F5F9 !important;
    }
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong {
        color: #F1F5F9 !important;
    }
    
    /* Markdown Tables & Formatted Tables - Crystal Clear in Dark Mode */
    table, [data-testid="stTable"] table, [data-testid="stMarkdownContainer"] table {
        width: 100% !important;
        border-collapse: collapse !important;
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        margin: 16px 0 !important;
    }
    thead tr, [data-testid="stMarkdownContainer"] thead tr {
        background-color: #334155 !important;
        border-bottom: 2px solid #475569 !important;
    }
    th, [data-testid="stMarkdownContainer"] th {
        background-color: #334155 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        border: 1px solid #475569 !important;
        text-align: left !important;
    }
    tbody tr, [data-testid="stMarkdownContainer"] tbody tr {
        background-color: #1E293B !important;
        border-bottom: 1px solid #334155 !important;
    }
    tbody tr:nth-of-type(even), [data-testid="stMarkdownContainer"] tbody tr:nth-of-type(even) {
        background-color: #16202E !important;
    }
    tbody tr:hover, [data-testid="stMarkdownContainer"] tbody tr:hover {
        background-color: #273549 !important;
    }
    td, [data-testid="stMarkdownContainer"] td {
        color: #E2E8F0 !important;
        padding: 12px 16px !important;
        border: 1px solid #334155 !important;
    }
    td strong, td b, th strong, th b {
        color: #60A5FA !important;
    }
    
    /* Code Blocks & Architecture Diagrams */
    pre, code, [data-testid="stCodeBlock"], [data-testid="stCodeBlock"] pre {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }
    code {
        color: #60A5FA !important;
        background-color: #1E293B !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] caption {
        color: #F3F4F6 !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1E293B !important;
        padding: 14px 18px !important;
        border-radius: 8px !important;
        border: 1px solid #334155 !important;
    }
    [data-testid="stMetricLabel"] * {
        color: #94A3B8 !important;
    }
    [data-testid="stMetricValue"] * {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* Widget Labels & Controls */
    [data-testid="stWidgetLabel"] *,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }
    [data-testid="stRadio"] label, [data-testid="stRadio"] span, [data-testid="stRadio"] p,
    [data-testid="stCheckbox"] label, [data-testid="stCheckbox"] span, [data-testid="stCheckbox"] p {
        color: #F1F5F9 !important;
    }
    
    /* Input Fields */
    input[type="text"], input[type="number"], div[data-baseweb="input"] input {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-color: #334155 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-color: #334155 !important;
    }
    div[data-baseweb="select"] span {
        color: #F8FAFC !important;
    }
    div[data-testid="stSlider"] div {
        color: #F8FAFC !important;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
        background-color: transparent !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #60A5FA !important;
        border-bottom-color: #60A5FA !important;
    }
    
    /* Alerts */
    [data-testid="stAlert"] p, [data-testid="stAlert"] span {
        color: #F8FAFC !important;
    }
    
    /* JSON Telemetry Viewer */
    [data-testid="stJson"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    [data-testid="stJson"] * {
        color: #38BDF8 !important;
    }
    
    hr {
        border-color: #334155 !important;
    }
    .stCaption, [data-testid="stCaptionContainer"] p {
        color: #94A3B8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
