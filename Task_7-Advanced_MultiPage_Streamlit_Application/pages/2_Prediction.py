"""
2_Prediction.py
---------------
Page 2: Interactive Single-Patient Clinical Risk Predictor with Icons, Dynamic BMI Meter,
Plotly Probability Distribution, and Patient Metric Radar Chart.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils import (
    ModelConnector,
    FEATURE_NAMES,
    FEATURE_LABELS,
    RISK_METADATA,
    calculate_bmi,
    generate_recommendations
)

st.markdown("## 🔮 Single Patient Clinical Risk Predictor")
st.markdown("Input patient physiological parameters to run real-time forward pass inference on `DeepHealthRiskNet`.")

st.markdown("---")

# Retrieve Model Connector
@st.cache_resource
def get_connector():
    return ModelConnector(api_url="http://127.0.0.1:5000")

connector = get_connector()
conn_mode = st.session_state.get("conn_mode", "🧠 Direct PyTorch Engine")

# Preset Loaders in Sidebar / Top
preset = st.selectbox(
    "📋 Quick Clinical Presets:",
    ["Custom / Manual Input", "🟢 Healthy / Low Risk Patient", "🟡 Moderate Risk Patient", "🔴 Critical Risk Patient"]
)

if preset == "🟢 Healthy / Low Risk Patient":
    init = {"age": 26, "h": 176.0, "w": 68.0, "steps": 11200, "cal": 2100, "sleep": 8.0, "hr": 64, "sys": 114, "dia": 74, "ex": 6.0, "alc": 1, "smk": False, "diab": False}
elif preset == "🟡 Moderate Risk Patient":
    init = {"age": 48, "h": 168.0, "w": 79.0, "steps": 5800, "cal": 2450, "sleep": 6.5, "hr": 78, "sys": 129, "dia": 83, "ex": 2.5, "alc": 4, "smk": False, "diab": False}
elif preset == "🔴 Critical Risk Patient":
    init = {"age": 64, "h": 162.0, "w": 96.0, "steps": 2100, "cal": 3200, "sleep": 5.0, "hr": 104, "sys": 162, "dia": 98, "ex": 0.5, "alc": 12, "smk": True, "diab": True}
else:
    init = {"age": 45, "h": 170.0, "w": 75.0, "steps": 6500, "cal": 2400, "sleep": 6.8, "hr": 78, "sys": 128, "dia": 82, "ex": 2.5, "alc": 4, "smk": False, "diab": False}

# Categorized Form
with st.form("single_pred_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Demographics & Body Measurements")
        age = st.number_input("🎂 Age (years)", min_value=1, max_value=120, value=int(init["age"]))
        height_cm = st.number_input("📏 Height (cm)", min_value=50.0, max_value=250.0, value=float(init["h"]), step=0.5)
        weight_kg = st.number_input("⚖️ Weight (kg)", min_value=10.0, max_value=300.0, value=float(init["w"]), step=0.5)
        
        current_bmi = calculate_bmi(weight_kg, height_cm)
        st.metric("🧮 Calculated BMI", f"{current_bmi:.2f} kg/m²", 
                  delta="Normal" if 18.5 <= current_bmi <= 24.9 else ("Overweight" if current_bmi >= 25 else "Underweight"),
                  delta_color="normal" if 18.5 <= current_bmi <= 24.9 else "inverse")

        st.markdown("#### 🏃 Daily Activity & Nutrition")
        daily_steps = st.number_input("👟 Daily Steps", min_value=0, max_value=50000, value=int(init["steps"]), step=500)
        calories = st.number_input("🍎 Calories Intake (kcal)", min_value=500, max_value=10000, value=int(init["cal"]), step=50)
        sleep_hrs = st.slider("💤 Hours of Sleep", min_value=0.0, max_value=16.0, value=float(init["sleep"]), step=0.1)

    with col2:
        st.markdown("#### 🫀 Vital Signs")
        heart_rate = st.number_input("💓 Heart Rate (bpm)", min_value=30, max_value=220, value=int(init["hr"]))
        sys_bp = st.number_input("🩸 Systolic BP (mmHg)", min_value=60, max_value=240, value=int(init["sys"]))
        dia_bp = st.number_input("🩺 Diastolic BP (mmHg)", min_value=30, max_value=160, value=int(init["dia"]))

        st.markdown("#### 🚬 Lifestyle & Pre-conditions")
        exercise_hrs = st.slider("🏋️ Exercise (hours/week)", min_value=0.0, max_value=40.0, value=float(init["ex"]), step=0.5)
        alcohol_units = st.number_input("🍷 Alcohol (units/week)", min_value=0, max_value=100, value=int(init["alc"]))
        
        smoker = st.checkbox("🚬 Active Smoker", value=bool(init["smk"]))
        diabetic = st.checkbox("🩹 Diagnosed Diabetic", value=bool(init["diab"]))

    st.markdown("---")
    btn = st.form_submit_button("⚡ Run Neural Network Inference")

if btn:
    feature_dict = {
        "age": float(age), "height_cm": float(height_cm), "weight_kg": float(weight_kg), "bmi": float(current_bmi),
        "daily_steps": float(daily_steps), "calories_intake": float(calories), "hours_of_sleep": float(sleep_hrs),
        "heart_rate": float(heart_rate), "systolic_bp": float(sys_bp), "diastolic_bp": float(dia_bp),
        "exercise_hours_per_week": float(exercise_hrs), "alcohol_consumption_per_week": float(alcohol_units),
        "smoker": 1.0 if smoker else 0.0, "diabetic": 1.0 if diabetic else 0.0
    }
    feature_vector = [feature_dict[k] for k in FEATURE_NAMES]

    st.markdown("---")
    with st.spinner("🧠 Executing PyTorch Forward Pass..."):
        try:
            if "Direct" in conn_mode:
                res = connector.predict_direct(feature_vector)
            else:
                healthy, _ = connector.check_api_health()
                if not healthy:
                    st.warning("⚠️ Flask API offline. Using Direct PyTorch Engine fallback.")
                    res = connector.predict_direct(feature_vector)
                else:
                    res = connector.predict_api(feature_vector)

            pred_label = res.get("predicted_label", "Low Risk")
            confidence = res.get("confidence_score", 0.0)
            probabilities = res.get("class_probabilities", {})
            latency = res.get("latency_ms", 0.0)
            mode_used = res.get("mode", conn_mode)

            meta = RISK_METADATA.get(pred_label, RISK_METADATA["Low Risk"])

            # Diagnostic Output Banner
            c1, c2, c3 = st.columns([2, 1, 1])
            with c1:
                st.markdown(f"### Assessment: {meta['badge']}")
                st.write(meta["desc"])
            with c2:
                st.metric("🎯 Confidence", f"{confidence*100:.1f}%")
            with c3:
                st.metric("⏱️ Latency", f"{latency} ms", delta=mode_used.split()[0])

            # Visualizations Row
            v1, v2 = st.columns(2)

            with v1:
                st.markdown("#### 📊 Softmax Class Probabilities")
                df_prob = pd.DataFrame({
                    "Risk Category": list(probabilities.keys()),
                    "Probability (%)": [v * 100 for v in probabilities.values()]
                })
                cmap = {"Low Risk": "#28a745", "Moderate Risk": "#ffc107", "High Risk": "#fd7e14", "Critical Risk": "#dc3545"}
                fig_bar = px.bar(df_prob, x="Risk Category", y="Probability (%)", color="Risk Category",
                                 color_discrete_map=cmap, text_auto=".1f")
                fig_bar.update_layout(yaxis_range=[0, 100], height=320, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)

            with v2:
                st.markdown("#### 🕸️ Patient Risk Profile Spider Chart")
                # Normalized metrics for spider plot
                radar_categories = ["BMI", "Systolic BP", "Heart Rate", "Calories", "Steps (Inv)", "Sleep (Inv)"]
                radar_vals = [
                    min(current_bmi / 40.0 * 100, 100),
                    min(sys_bp / 180.0 * 100, 100),
                    min(heart_rate / 140.0 * 100, 100),
                    min(calories / 4000.0 * 100, 100),
                    max((10000 - daily_steps) / 10000.0 * 100, 0),
                    max((8.0 - sleep_hrs) / 8.0 * 100, 0)
                ]
                fig_radar = go.Figure(data=go.Scatterpolar(r=radar_vals, theta=radar_categories, fill='toself', line_color='#1E3A8A'))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=320, showlegend=False)
                st.plotly_chart(fig_radar, use_container_width=True)

            # Clinical Recommendations
            st.markdown("#### 💡 Clinical Recommendations")
            recs = generate_recommendations(feature_dict, pred_label)
            for r in recs:
                st.write(f"- {r}")

        except Exception as e:
            st.error(f"❌ Error during inference: {str(e)}")
