"""
2_Prediction.py
---------------
Page 2: Interactive Single-Patient Clinical Risk Predictor over Flask REST API.
Demonstrates HTTP POST request transfer, real-time response parsing, dynamic rendering, and RTT latency tracking.
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

st.title("🔮 Single Patient Clinical Risk Predictor (Flask API)")
st.write("Input patient physiological parameters to transfer HTTP API requests and receive real-time neural network predictions from the Flask backend.")

st.divider()

# Connection Mode Banner
conn_mode = st.session_state.get("connection_mode", "Flask REST API 🌐")
api_url = st.session_state.get("api_url", "http://127.0.0.1:5000")

@st.cache_resource
def get_connector(url):
    return ModelConnector(default_api_url=url)

connector = get_connector(api_url)

# Preset Loaders in Top Bar
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
        st.subheader("👤 Demographics & Body Metrics")
        age = st.number_input("🎂 Age (years)", min_value=1, max_value=120, value=int(init["age"]))
        height_cm = st.number_input("📏 Height (cm)", min_value=50.0, max_value=250.0, value=float(init["h"]), step=0.5)
        weight_kg = st.number_input("⚖️ Weight (kg)", min_value=10.0, max_value=300.0, value=float(init["w"]), step=0.5)
        
        current_bmi = calculate_bmi(weight_kg, height_cm)
        st.metric("🧮 Calculated BMI", f"{current_bmi:.2f} kg/m²", 
                  delta="Normal" if 18.5 <= current_bmi <= 24.9 else ("Overweight" if current_bmi >= 25 else "Underweight"),
                  delta_color="normal" if 18.5 <= current_bmi <= 24.9 else "inverse")

        st.subheader("🏃 Daily Activity & Nutrition")
        daily_steps = st.number_input("👟 Daily Steps", min_value=0, max_value=50000, value=int(init["steps"]), step=500)
        calories = st.number_input("🍎 Calories Intake (kcal)", min_value=500, max_value=10000, value=int(init["cal"]), step=50)
        sleep_hrs = st.slider("💤 Hours of Sleep", min_value=0.0, max_value=16.0, value=float(init["sleep"]), step=0.1)

    with col2:
        st.subheader("🫀 Vital Signs")
        heart_rate = st.number_input("💓 Heart Rate (bpm)", min_value=30, max_value=220, value=int(init["hr"]))
        sys_bp = st.number_input("🩸 Systolic BP (mmHg)", min_value=60, max_value=240, value=int(init["sys"]))
        dia_bp = st.number_input("🩺 Diastolic BP (mmHg)", min_value=30, max_value=160, value=int(init["dia"]))

        st.subheader("🚬 Lifestyle & Pre-conditions")
        exercise_hrs = st.slider("🏋️ Exercise (hours/week)", min_value=0.0, max_value=40.0, value=float(init["ex"]), step=0.5)
        alcohol_units = st.number_input("🍷 Alcohol (units/week)", min_value=0, max_value=100, value=int(init["alc"]))
        
        smoker = st.checkbox("🚬 Active Smoker", value=bool(init["smk"]))
        diabetic = st.checkbox("🩹 Diagnosed Diabetic", value=bool(init["diab"]))

    st.divider()
    btn = st.form_submit_button("⚡ Send HTTP API Request & Predict", use_container_width=True, type="primary")

if btn:
    feature_dict = {
        "age": float(age), "height_cm": float(height_cm), "weight_kg": float(weight_kg), "bmi": float(current_bmi),
        "daily_steps": float(daily_steps), "calories_intake": float(calories), "hours_of_sleep": float(sleep_hrs),
        "heart_rate": float(heart_rate), "systolic_bp": float(sys_bp), "diastolic_bp": float(dia_bp),
        "exercise_hours_per_week": float(exercise_hrs), "alcohol_consumption_per_week": float(alcohol_units),
        "smoker": 1.0 if smoker else 0.0, "diabetic": 1.0 if diabetic else 0.0
    }
    feature_vector = [feature_dict[k] for k in FEATURE_NAMES]

    mode_arg = "API" if conn_mode.startswith("Flask") else "DIRECT"

    st.divider()
    with st.spinner(f"🌐 Transmitting HTTP POST payload to `{api_url}/predict`..."):
        try:
            res = connector.predict_single(feature_vector, mode=mode_arg, api_url=api_url)
            pred_label = res.get("predicted_label", "Low Risk")
            confidence = res.get("confidence_score", 0.0)
            probs = res.get("class_probabilities", {})
            rtt_ms = res.get("rtt_ms", 0.0)
            backend_ms = res.get("backend_latency_ms", 0.0)
            active_mode_str = res.get("mode", "Flask API")

            meta = RISK_METADATA.get(pred_label, RISK_METADATA["Low Risk"])

            st.subheader("🎯 Real-Time Inference Results")
            
            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            with res_col1:
                st.metric("Predicted Health Risk", meta["badge"])
            with res_col2:
                st.metric("Model Confidence", f"{confidence * 100:.1f}%")
            with res_col3:
                st.metric("Network RTT Latency", f"{rtt_ms:.2f} ms")
            with res_col4:
                st.metric("Inference Engine Mode", active_mode_str)

            st.caption(f"**Clinical Description**: {meta['desc']}")

            # Dynamic Bar Chart for Softmax Probabilities
            prob_df = pd.DataFrame([
                {"Risk Class": k, "Probability (%)": v * 100} for k, v in probs.items()
            ])
            
            fig = px.bar(
                prob_df, x="Risk Class", y="Probability (%)",
                color="Risk Class",
                color_discrete_map={
                    "Low Risk": "#28a745", "Moderate Risk": "#ffc107",
                    "High Risk": "#fd7e14", "Critical Risk": "#dc3545"
                },
                title="Neural Network Softmax Class Probability Distribution",
                text_auto=".1f"
            )
            fig.update_layout(height=320, showlegend=False, yaxis_range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)

            # Recommendations & API Details
            st.divider()
            rec_col1, rec_col2 = st.columns([1, 1])

            with rec_col1:
                st.subheader("💡 Dynamic Clinical Recommendations")
                recs = generate_recommendations(feature_dict, pred_label)
                for r in recs:
                    st.markdown(f"- {r}")

            with rec_col2:
                st.subheader("📡 HTTP API Transmission Log")
                st.json({
                    "endpoint": f"{api_url}/predict",
                    "method": "POST",
                    "http_status": res.get("http_status", 200),
                    "total_rtt_latency_ms": rtt_ms,
                    "backend_inference_latency_ms": backend_ms,
                    "request_payload": {"features": feature_vector},
                    "response_summary": {
                        "predicted_label": pred_label,
                        "confidence_score": confidence
                    }
                })

        except Exception as e:
            st.error(f"❌ Real-time Prediction Error: {str(e)}")
            st.info("💡 Make sure the Flask API server is running (`python flask_api.py`) or switch to Direct PyTorch Engine in the sidebar.")
