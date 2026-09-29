"""
4_Analytics.py
--------------
Page 4: Model Performance Evaluation & Flask API Latency Analytics Dashboard.
Evaluates dataset predictions over HTTP API, calculates Confusion Matrix, ROC curves, and Latency benchmarks.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import classification_report, f1_score

from utils import (
    ModelConnector,
    compute_dataset_analytics,
    RISK_CLASSES,
    load_dataset
)

st.title("📊 Model Performance & API Latency Analytics")
st.write("Comprehensive evaluation of model accuracy, confusion matrix, multi-class ROC curves, and HTTP REST API inference benchmark.")

st.divider()

# Connection Mode Banner
conn_mode = st.session_state.get("connection_mode", "Flask REST API 🌐")
api_url = st.session_state.get("api_url", "http://127.0.0.1:5000")

@st.cache_resource
def get_connector(url):
    return ModelConnector(default_api_url=url)

connector = get_connector(api_url)

mode_arg = "API" if conn_mode.startswith("Flask") else "DIRECT"

if st.button("🚀 Run Full Model Evaluation via Flask API", type="primary", use_container_width=True):
    with st.spinner(f"🌐 Transmitting evaluation batch to Flask API ({api_url})..."):
        try:
            analytics = compute_dataset_analytics(connector, mode=mode_arg, api_url=api_url)
            
            st.session_state["cached_analytics"] = analytics
            st.success("✅ Dataset evaluation completed successfully!")
        except Exception as e:
            st.error(f"❌ Analytics Evaluation Failed: {str(e)}")

if "cached_analytics" in st.session_state:
    an = st.session_state["cached_analytics"]

    # Top Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Model Accuracy", f"{an['accuracy'] * 100:.2f}%")
    with m2:
        f1_mac = f1_score(an['y_true'], an['y_pred'], average='macro')
        st.metric("F1 Macro Score", f"{f1_mac:.4f}")
    with m3:
        st.metric("Total Batch RTT Latency", f"{an['rtt_ms']:.2f} ms")
    with m4:
        st.metric("Evaluated Patients", f"{len(an['y_true']):,} Records")

    st.divider()
    col_cm, col_roc = st.columns([1, 1])

    with col_cm:
        st.subheader("🧩 Confusion Matrix (Normalized)")
        cm = an["confusion_matrix"]
        cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        fig_cm = px.imshow(
            cm_norm,
            x=RISK_CLASSES,
            y=RISK_CLASSES,
            text_auto=".2f",
            color_continuous_scale="Blues",
            labels=dict(x="Predicted Label", y="True Target Label", color="Proportion")
        )
        fig_cm.update_layout(height=340, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_roc:
        st.subheader("📈 Multi-Class Receiver Operating Characteristic (ROC)")
        fig_roc = go.Figure()
        
        y_true_onehot = pd.get_dummies(an['y_true']).values
        y_prob = an['y_prob']

        colors = ["#28a745", "#ffc107", "#fd7e14", "#dc3545"]
        for i in range(4):
            from sklearn.metrics import roc_curve, auc
            fpr, tpr, _ = roc_curve(y_true_onehot[:, i], y_prob[:, i])
            roc_auc = auc(fpr, tpr)
            fig_roc.add_trace(go.Scatter(
                x=fpr, y=tpr,
                mode='lines',
                name=f"{RISK_CLASSES[i]} (AUC = {roc_auc:.3f})",
                line=dict(color=colors[i], width=2)
            ))

        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash', color='gray'), name='Random Chance'))
        fig_roc.update_layout(
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            height=340,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_roc, use_container_width=True)

    st.divider()
    st.subheader("⚡ Latency Benchmark: Flask API vs In-Memory PyTorch Engine")
    
    bench_df = pd.DataFrame([
        {"Component": "Flask REST API HTTP Latency", "Time (ms)": an['rtt_ms']},
        {"Component": "Backend PyTorch Engine Latency", "Time (ms)": an['backend_ms']},
        {"Component": "Estimated Network & Serialization Overhead", "Time (ms)": max(0.0, an['rtt_ms'] - an['backend_ms'])}
    ])
    
    fig_bench = px.bar(
        bench_df, x="Component", y="Time (ms)", color="Component",
        title="Latency Overhead Breakdown", text_auto=".2f",
        color_discrete_sequence=["#1E3A8A", "#2563EB", "#38BDF8"]
    )
    fig_bench.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_bench, use_container_width=True)

else:
    st.info("💡 Click the button above to execute full evaluation over Flask REST API.")
