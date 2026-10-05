"""
views/3_Clinical_Risk_Predictor.py
----------------------------------
Clinical Biomarker Multi-Condition Risk Predictor using DeepHealthRiskNet.
"""

import streamlit as st
import numpy as np
from utils import predict_tabular, create_radar_chart

st.title("🩺 Clinical Biomarker Risk Predictor")
st.markdown("Assess patient cardiovascular and metabolic health risk using 14 physiological biomarkers.")

st.subheader("1. Patient Clinical Biomarkers")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Cardiovascular Profile")
    age = st.slider("Age (Years)", 18, 90, 52)
    systolic_bp = st.slider("Systolic BP (mmHg)", 90, 200, 135)
    diastolic_bp = st.slider("Diastolic BP (mmHg)", 60, 120, 85)
    resting_hr = st.slider("Resting Heart Rate (BPM)", 45, 130, 74)
    cholesterol = st.slider("Total Cholesterol (mg/dL)", 120, 340, 215)

with col2:
    st.markdown("#### Metabolic & Physical")
    bmi = st.slider("Body Mass Index (BMI)", 15.0, 48.0, 27.4, step=0.1)
    fasting_glucose = st.slider("Fasting Blood Sugar (mg/dL)", 70, 260, 110)
    hba1c = st.slider("HbA1c Level (%)", 4.0, 12.0, 5.8, step=0.1)
    daily_steps = st.slider("Daily Physical Steps", 1000, 22000, 6500, step=500)
    sleep_hours = st.slider("Sleep Duration (Hours)", 3.0, 11.0, 7.0, step=0.5)

with col3:
    st.markdown("#### Lifestyle & Vitals")
    oxygen_sat = st.slider("Blood Oxygen (SpO2 %)", 85, 100, 97)
    water_intake = st.slider("Water Intake (Liters/Day)", 0.5, 5.0, 2.2, step=0.1)
    stress_level = st.slider("Reported Stress Index (1-10)", 1, 10, 5)
    active_minutes = st.slider("Active Minutes / Day", 5, 180, 45)

features_vector = [
    float(age), float(systolic_bp), float(diastolic_bp), float(resting_hr), float(cholesterol),
    float(bmi), float(fasting_glucose), float(hba1c), float(daily_steps), float(sleep_hours),
    float(oxygen_sat), float(water_intake), float(stress_level), float(active_minutes)
]

st.markdown("---")
st.subheader("2. Multi-Condition Health Risk Evaluation")

if st.button("🔮 Calculate Deep Learning Clinical Risk", type="primary"):
    with st.spinner("Evaluating multi-condition risk model..."):
        res = predict_tabular(features_vector, base_url=st.session_state.get("backend_url"))
        
    if res.get("status") == "success":
        pred = res.get("prediction", "Unknown")
        conf = res.get("confidence", 0.0) * 100.0
        lat = res.get("latency_ms", 0.0)
        probs = res.get("probabilities", {})
        
        # Risk color
        if "Low" in pred:
            color = "#10B981"
        elif "Moderate" in pred:
            color = "#3B82F6"
        elif "High" in pred:
            color = "#F59E0B"
        else:
            color = "#EF4444"
            
        c_res, c_radar = st.columns([1, 1.2])
        with c_res:
            st.markdown(f"""
            <div style="background-color: {color}22; border-left: 6px solid {color}; padding: 16px; border-radius: 6px;">
                <h2 style="margin: 0; color: {color};">{pred.upper()}</h2>
                <p style="margin: 6px 0 0 0; font-size: 16px; color: #F1F5F9;">
                    Confidence Score: <b>{conf:.1f}%</b> | Latency: <b>{lat:.1f} ms</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Risk Distribution Breakdown")
            for c_name, p_val in probs.items():
                st.write(f"**{c_name}**: {p_val*100:.1f}%")
                st.progress(float(p_val))
                
        with c_radar:
            radar_dict = {
                "BP Ratio": min(systolic_bp / 2.0, 100),
                "BMI": min(bmi * 2.5, 100),
                "Glucose": min(fasting_glucose / 2.5, 100),
                "Cholesterol": min(cholesterol / 3.4, 100),
                "Stress": stress_level * 10
            }
            chart = create_radar_chart(radar_dict)
            st.plotly_chart(chart, use_container_width=True)
    else:
        st.error(f"Prediction failed: {res.get('message')}")
