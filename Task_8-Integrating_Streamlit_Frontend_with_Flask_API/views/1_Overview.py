"""
1_Overview.py
-------------
Page 1: Executive Overview, Flask REST API Integration Specs & System Architecture.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataset, FEATURE_LABELS, RISK_CLASSES, ModelConnector

st.title("🏠 Executive Overview & REST API Integration Architecture")
st.write("Welcome to **Task 8: Streamlit Frontend & Flask REST API Integration**. This application connects a multi-page interactive Streamlit UI with an enterprise Flask REST API backend for real-time deep learning inference.")

st.divider()

# Status Banner
conn_mode = st.session_state.get("connection_mode", "Flask REST API 🌐")
api_url = st.session_state.get("api_url", "http://127.0.0.1:5000")

col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    st.metric("🔌 Active Mode", conn_mode)
with col_b2:
    st.metric("🌐 Target API URL", api_url)
with col_b3:
    connector = ModelConnector(default_api_url=api_url)
    health = connector.check_api_health(api_url)
    if health.get("online"):
        st.metric("🟢 API Health", "HEALTHY (200 OK)", delta=f"{health.get('rtt_ms', 0)} ms RTT")
    else:
        st.metric("🔴 API Health", "OFFLINE / UNREACHABLE", delta="Connection Error", delta_color="inverse")

st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("🔗 System Integration Flow")
    st.info("""
    **Client-Server Decoupled Architecture:**
    1. **Streamlit UI (Frontend)**: Collects patient demographic and physiological inputs, formats request payloads, sends HTTP POST to Flask API.
    2. **Flask REST API (Backend)**: Listens on port `5000`, receives JSON payload (`/predict`), performs validation & feature scaling.
    3. **PyTorch Engine (`DeepHealthRiskNet`)**: Runs forward pass tensor math, returns softmax class probabilities.
    4. **Dynamic Output Display**: Frontend parses HTTP JSON response, calculates RTT latency, and dynamically updates UI visualizations.
    """)

    st.subheader("📋 Ingested Dataset (`health_activity_data.csv`)")
    try:
        df = load_dataset()
        st.success(f"✅ Loaded dataset with **{len(df):,} patient records**.")
        with st.expander("🔍 View Dataset Sample"):
            st.dataframe(df.head(8), use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")

with col2:
    st.header("⚡ REST API Endpoints Specification")
    
    st.markdown("""
    | Method | Endpoint | Description | Payload Format |
    |---|---|---|---|
    | `GET` | `/` | API Root Metadata | None |
    | `GET` | `/health` | Health & Readiness Probe | None |
    | `POST` | `/predict` | Deep Learning Inference | `{"features": [...]}` or `{"instances": [[...]]}` |
    """)

    st.subheader("🧠 PyTorch `DeepHealthRiskNet` Neural Network")
    st.info("""
    - **Input Layer**: 14 Scaled Features (Age, BMI, BP, Steps, Sleep, Heart Rate, etc.)
    - **Hidden Layer 1**: Linear(14 → 64) + BatchNorm1d + ReLU + Dropout(0.2)
    - **Hidden Layer 2**: Linear(64 → 32) + BatchNorm1d + ReLU + Dropout(0.2)
    - **Output Layer**: Linear(32 → 4) + Softmax Activation
    - **Target Output Classes**: Low Risk, Moderate Risk, High Risk, Critical Risk
    """)

st.divider()
st.header("📈 Cohort Demographic Overview")
try:
    df = load_dataset()
    fig = px.histogram(
        df, x="Age", color="Gender" if "Gender" in df.columns else None, 
        title="Age & Gender Distribution Across Ingested Cohort",
        barmode="overlay", color_discrete_sequence=["#1E3A8A", "#EF4444"]
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.info("Dataset visualization ready.")
