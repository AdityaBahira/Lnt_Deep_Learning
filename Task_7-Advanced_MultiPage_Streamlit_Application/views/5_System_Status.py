"""
5_System_Status.py
------------------
Page 5: System Health Inspector, Model Diagnostics, and Latency Benchmarker.
"""

import time
import streamlit as st
import pandas as pd

from utils import ModelConnector

st.title("⚙️ System Health & Neural Net Diagnostics")
st.write("Monitor in-memory PyTorch model status, verify model readiness, benchmark forward-pass latency, and inspect architectural specifications.")

st.divider()

@st.cache_resource
def get_connector():
    return ModelConnector()

connector = get_connector()

col1, col2 = st.columns(2)

with col1:
    st.header("🧠 Direct PyTorch Model Engine Health")
    st.write("Engine Status: `DeepHealthRiskNet` (PyTorch 2.x Neural Network)")
    
    if st.button("🔄 Check Model Engine Health", use_container_width=True):
        if connector.direct_engine and connector.direct_engine._initialized:
            st.success("🟢 **PyTorch Model Engine is ONLINE and Healthy!**")
            st.json({
                "model_name": connector.direct_engine.config["model_name"],
                "initialized": connector.direct_engine._initialized,
                "input_dimension": connector.direct_engine.input_dim,
                "output_classes": connector.direct_engine.class_labels,
                "device": str(connector.direct_engine.device)
            })
        else:
            st.error("🔴 **PyTorch Model Engine is Offline or Not Initialized.**")

with col2:
    st.header("⏱️ Real-Time Inference Latency Benchmarker")
    st.write("Measures in-memory PyTorch forward-pass execution latency across 10 sample iterations.")
    if st.button("⚡ Run Latency Benchmark (10 Inferences)", use_container_width=True, type="primary"):
        test_vec = [45.0, 170.0, 75.0, 25.95, 6500.0, 2400.0, 6.8, 78.0, 128.0, 82.0, 2.5, 4.0, 0.0, 0.0]
        latencies = []
        for _ in range(10):
            t0 = time.time()
            connector.predict_direct(test_vec)
            latencies.append((time.time() - t0) * 1000)
        
        avg_lat = sum(latencies) / len(latencies)
        st.metric("⚡ Average Latency (10 runs)", f"{avg_lat:.2f} ms")
        st.caption(f"Min: {min(latencies):.2f} ms | Max: {max(latencies):.2f} ms")

st.divider()
st.header("📖 PyTorch Model Architecture Specifications")
specs_df = pd.DataFrame([
    {"Component": "Neural Net Model", "Specification": "3-Layer DeepHealthRiskNet (Linear -> BatchNorm -> ReLU -> Dropout)"},
    {"Component": "Input Dimension", "Specification": "14 Numerical Features (StandardScaler normalized)"},
    {"Component": "Hidden Layers", "Specification": "Layer 1: 14 -> 64 | Layer 2: 64 -> 32 (Dropout p=0.2)"},
    {"Component": "Output Layer", "Specification": "32 -> 4 (Softmax Probability Distribution over 4 Risk Tiers)"},
    {"Component": "Execution Engine", "Specification": "Direct In-Memory PyTorch Forward Pass (Sub-millisecond Latency)"}
])
st.dataframe(specs_df, use_container_width=True)
