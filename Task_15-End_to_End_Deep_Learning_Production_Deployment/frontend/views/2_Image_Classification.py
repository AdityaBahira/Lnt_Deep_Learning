"""
views/2_Image_Classification.py
-------------------------------
Radiological Vision Diagnostics with Sample Gallery, Live File Upload,
and Plotly Probability Distribution.
"""

import os
import streamlit as st
from PIL import Image
from utils import predict_image, create_probability_bar_chart

st.title("🩻 Radiological Vision Diagnostics")
st.markdown("Analyze chest radiographs in real-time using the trained **DeepMedVisionNet** model.")

# Sample Gallery Selection
# Sample Gallery Selection (Real Kaggle Radiographs)
sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sample_data")
sample_cases = {
    "COVID-19 Infiltration": "covid_case.png",
    "Lung Opacity / Bacterial": "lung_opacity_case.png",
    "Normal / Healthy": "normal_case.png",
    "Viral Pneumonia": "viral_case.png"
}

st.subheader("1. Select Diagnostic Sample or Upload Radiograph")
tab_sample, tab_upload = st.tabs(["📁 Sample Radiograph Gallery", "⬆️ Custom File Upload"])

selected_image_data = None
selected_label = None

with tab_sample:
    col_a, col_b, col_c, col_d = st.columns(4)
    cols = [col_a, col_b, col_c, col_d]
    
    for idx, (label, fname) in enumerate(sample_cases.items()):
        fpath = os.path.join(sample_dir, fname)
        with cols[idx]:
            if os.path.exists(fpath):
                img_prev = Image.open(fpath)
                st.image(img_prev, caption=label, use_container_width=True)
                if st.button(f"Load {label.split('/')[0]}", key=f"btn_{idx}"):
                    selected_image_data = fpath
                    selected_label = label
                    st.session_state["current_img"] = fpath
                    st.session_state["current_label"] = label

with tab_upload:
    uploaded = st.file_uploader("Upload Chest X-Ray or CT Scan (JPEG / PNG)", type=["png", "jpg", "jpeg"])
    if uploaded is not None:
        selected_image_data = uploaded.read()
        selected_label = uploaded.name
        st.session_state["current_img"] = selected_image_data
        st.session_state["current_label"] = selected_label

# Use persisted session state if present
if "current_img" in st.session_state:
    selected_image_data = st.session_state["current_img"]
    selected_label = st.session_state["current_label"]

st.markdown("---")

# Prediction and Results Section
if selected_image_data is not None:
    st.subheader("2. Diagnostic Analysis & Inference")
    col_img, col_res = st.columns([1, 1.4])
    
    with col_img:
        st.markdown("**Selected Radiograph Preview**")
        if isinstance(selected_image_data, str):
            display_img = Image.open(selected_image_data)
        else:
            import io
            display_img = Image.open(io.BytesIO(selected_image_data))
        st.image(display_img, caption=f"Active Input: {selected_label}", width=320)
        
        run_btn = st.button("🚀 Run Deep Learning Diagnostic Inference", type="primary", use_container_width=True)
        
    with col_res:
        if run_btn or "last_prediction" in st.session_state:
            with st.spinner("Executing PyTorch Forward Pass..."):
                if run_btn or "last_prediction" not in st.session_state:
                    res = predict_image(selected_image_data, base_url=st.session_state.get("backend_url"))
                    st.session_state["last_prediction"] = res
                else:
                    res = st.session_state["last_prediction"]
                    
            if res.get("status") == "success":
                pred = res.get("prediction", "Unknown")
                conf = res.get("confidence", 0.0) * 100.0
                latency = res.get("latency_ms", 0.0)
                probs = res.get("probabilities", {})
                
                # Badge color logic
                if "Normal" in pred:
                    badge_color = "#10B981"
                    status_text = "NEGATIVE FOR PATHOLOGY"
                elif "Lung_Opacity" in pred or "Opacity" in pred:
                    badge_color = "#F59E0B"
                    status_text = "LUNG OPACITY / INFILTRATE DETECTED"
                elif "Viral" in pred:
                    badge_color = "#8B5CF6"
                    status_text = "INTERSTITIAL VIRAL PATTERN"
                else:
                    badge_color = "#EF4444"
                    status_text = "COVID-19 INFILTRATION DETECTED"
                    
                is_light = st.session_state.get("theme_mode", "light") == "light"
                sub_text_color = "#334155" if is_light else "#E2E8F0"
                bg_opacity = "18" if is_light else "28"

                st.markdown(f"""
                <div style="background-color: {badge_color}{bg_opacity}; border-left: 6px solid {badge_color}; padding: 14px; border-radius: 6px; margin-bottom: 12px;">
                    <h3 style="margin: 0; color: {badge_color};">Predicted: {pred}</h3>
                    <p style="margin: 4px 0 0 0; font-weight: bold; color: {sub_text_color};">{status_text} | Confidence: {conf:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Class Confidence", f"{conf:.1f}%")
                m2.metric("Inference Latency", f"{latency:.1f} ms")
                m3.metric("Serving Device", res.get("device", "CPU").upper())
                
                # Plotly Chart
                if probs:
                    chart = create_probability_bar_chart(probs)
                    st.plotly_chart(chart, use_container_width=True)
            else:
                st.error(f"Inference Failure: {res.get('message', 'Unknown Error')}")
else:
    st.info("👆 Please select a sample case above or upload an image to begin diagnostic inference.")
