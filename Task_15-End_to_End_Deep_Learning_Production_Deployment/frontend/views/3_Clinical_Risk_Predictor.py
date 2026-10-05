"""
views/3_Clinical_Risk_Predictor.py
----------------------------------
Clinical Biomarker Multi-Condition Risk Predictor using DeepHealthRiskNet.
Features:
- Preset patient sample selector (Healthy, Moderate, Severe, Custom)
- Live auto-calculating BMI indicator
- 4 categorized clinical biomarker inputs (14 physiological features)
- Color-coded risk tier banner and Plotly probability distribution
- Personalized clinical and lifestyle recommendations
"""

import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import predict_tabular, create_radar_chart

st.title("🩺 Clinical Biomarker Risk Predictor")
st.markdown("Assess patient cardiovascular and metabolic health risk across 14 physiological biomarkers using `DeepHealthRiskNet`.")

# ----------------------------------------------------
# 1. Preset Selector
# ----------------------------------------------------
st.subheader("1. Clinical Preset Profile")
preset = st.selectbox(
    "Load Clinical Preset Profile:",
    [
        "🟢 Healthy / Low Risk Patient",
        "🟡 Moderate Risk Patient",
        "🔴 Severe / Critical Risk Patient",
        "Default / Custom Patient"
    ]
)

if preset == "🟢 Healthy / Low Risk Patient":
    p_vals = {
        "age": 28, "height": 175.0, "weight": 68.0,
        "steps": 10500, "calories": 2100, "sleep": 7.8,
        "hr": 68, "sys_bp": 115, "dia_bp": 75,
        "exercise": 5.5, "alcohol": 1,
        "smoker": False, "diabetic": False
    }
elif preset == "🟡 Moderate Risk Patient":
    p_vals = {
        "age": 45, "height": 170.0, "weight": 78.0,
        "steps": 7000, "calories": 2400, "sleep": 6.5,
        "hr": 80, "sys_bp": 125, "dia_bp": 82,
        "exercise": 3.0, "alcohol": 4,
        "smoker": False, "diabetic": False
    }
elif preset == "🔴 Severe / Critical Risk Patient":
    p_vals = {
        "age": 65, "height": 165.0, "weight": 98.0,
        "steps": 2000, "calories": 3200, "sleep": 5.0,
        "hr": 105, "sys_bp": 160, "dia_bp": 100,
        "exercise": 0.5, "alcohol": 15,
        "smoker": True, "diabetic": True
    }
else:
    p_vals = {
        "age": 50, "height": 172.0, "weight": 80.0,
        "steps": 6500, "calories": 2300, "sleep": 6.8,
        "hr": 78, "sys_bp": 128, "dia_bp": 82,
        "exercise": 2.5, "alcohol": 3,
        "smoker": False, "diabetic": False
    }

st.markdown("---")

# ----------------------------------------------------
# 2. Form Input Widgets Grouped by 4 Categories
# ----------------------------------------------------
st.subheader("2. Patient Physiological Biomarkers")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 👤 Category 1: Demographics & Body Metrics")
    age = st.number_input("🎂 Age (Years)", min_value=18, max_value=100, value=int(p_vals["age"]), step=1)
    height_cm = st.number_input("📏 Height (cm)", min_value=120.0, max_value=220.0, value=float(p_vals["height"]), step=0.5)
    weight_kg = st.number_input("⚖️ Weight (kg)", min_value=35.0, max_value=200.0, value=float(p_vals["weight"]), step=0.5)
    
    # Auto-calculated BMI
    bmi = weight_kg / ((height_cm / 100.0) ** 2)
    if bmi < 18.5:
        bmi_status = "Underweight"
        bmi_color = "#38BDF8"
    elif bmi < 25.0:
        bmi_status = "Normal Weight"
        bmi_color = "#10B981"
    elif bmi < 30.0:
        bmi_status = "Overweight"
        bmi_color = "#F59E0B"
    else:
        bmi_status = "Obese"
        bmi_color = "#EF4444"
        
    st.markdown(f"""
    <div style="background-color: #1E293B; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; border: 1px solid #334155;">
        <span style="color: #94A3B8; font-size: 13px;">Auto-Calculated BMI:</span>
        <b style="color: #F8FAFC; font-size: 16px; margin-left: 8px;">{bmi:.2f} kg/m²</b>
        <span style="color: {bmi_color}; font-weight: bold; margin-left: 10px;">({bmi_status})</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🏃 Category 2: Daily Activity & Nutrition")
    daily_steps = st.number_input("👟 Daily Steps (steps/day)", min_value=500, max_value=35000, value=int(p_vals["steps"]), step=500)
    calories_intake = st.number_input("🍎 Caloric Intake (kcal/day)", min_value=1000, max_value=6000, value=int(p_vals["calories"]), step=50)
    hours_of_sleep = st.slider("💤 Sleep Duration (hours/night)", min_value=3.0, max_value=12.0, value=float(p_vals["sleep"]), step=0.5)

with col2:
    st.markdown("#### 🫀 Category 3: Vital Signs & Cardiovascular")
    heart_rate = st.number_input("💓 Resting Heart Rate (bpm)", min_value=40, max_value=160, value=int(p_vals["hr"]), step=1)
    systolic_bp = st.number_input("🩸 Systolic Blood Pressure (mmHg)", min_value=80, max_value=220, value=int(p_vals["sys_bp"]), step=1)
    diastolic_bp = st.number_input("🩺 Diastolic Blood Pressure (mmHg)", min_value=50, max_value=140, value=int(p_vals["dia_bp"]), step=1)

    st.markdown("#### 🚬 Category 4: Lifestyle & Medical Conditions")
    exercise_hours = st.slider("🏋️ Physical Exercise (hours/week)", min_value=0.0, max_value=25.0, value=float(p_vals["exercise"]), step=0.5)
    alcohol_units = st.number_input("🍷 Alcohol Consumption (units/week)", min_value=0, max_value=50, value=int(p_vals["alcohol"]), step=1)
    
    st.write("🏥 Pre-Existing Clinical Risk Indicators:")
    smoker_flag = st.checkbox("🚬 Active Tobacco Smoker", value=bool(p_vals["smoker"]))
    diabetic_flag = st.checkbox("🩹 Diagnosed Type-2 Diabetic", value=bool(p_vals["diabetic"]))

# 14-Feature Input Vector in exact training order:
# [age, height_cm, weight_kg, bmi, daily_steps, calories_intake, hours_of_sleep,
#  heart_rate, systolic_bp, diastolic_bp, exercise_hours_per_week, alcohol_consumption_per_week, smoker, diabetic]
features_vector = [
    float(age),
    float(height_cm),
    float(weight_kg),
    float(bmi),
    float(daily_steps),
    float(calories_intake),
    float(hours_of_sleep),
    float(heart_rate),
    float(systolic_bp),
    float(diastolic_bp),
    float(exercise_hours),
    float(alcohol_units),
    1.0 if smoker_flag else 0.0,
    1.0 if diabetic_flag else 0.0
]

st.markdown("---")

# ----------------------------------------------------
# 3. Execution & Clinical Output
# ----------------------------------------------------
st.subheader("3. Neural Network Risk Evaluation")

if st.button("🔮 Calculate Deep Learning Clinical Risk", type="primary"):
    with st.spinner("Executing DeepHealthRiskNet forward inference..."):
        res = predict_tabular(features_vector, base_url=st.session_state.get("backend_url"))
        
    if res.get("status") == "success":
        pred = res.get("prediction", "Unknown")
        conf = res.get("confidence", 0.0) * 100.0
        lat = res.get("latency_ms", 0.0)
        probs = res.get("probabilities", {})
        
        # Color coding
        if "Low" in pred:
            badge_color = "#10B981"
            rec_text = "Patient demonstrates optimal cardiovascular indicators. Maintain balanced nutrition, daily 8,000+ steps, and regular sleep schedule."
        elif "Moderate" in pred:
            badge_color = "#3B82F6"
            rec_text = "Borderline clinical metrics detected. Recommend reducing dietary sodium, increasing weekly aerobic exercise to 4+ hours, and monitoring blood pressure."
        elif "High" in pred:
            badge_color = "#F59E0B"
            rec_text = "Elevated cardiovascular and metabolic strain. Physician consultation recommended for lipid profile review and structured hypertension management."
        else:
            badge_color = "#EF4444"
            rec_text = "CRITICAL RISK: Significant multi-condition warning signs (elevated BP, metabolic risk, smoking/diabetic indicators). Immediate clinical evaluation recommended."
            
        c_res, c_chart = st.columns([1, 1.2])
        
        with c_res:
            st.markdown(f"""
            <div style="background-color: {badge_color}22; border-left: 6px solid {badge_color}; padding: 18px; border-radius: 8px; margin-bottom: 16px;">
                <span style="color: #94A3B8; font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">DIAGNOSTIC FINDING</span>
                <h2 style="margin: 4px 0 0 0; color: {badge_color};">{pred.upper()}</h2>
                <p style="margin: 6px 0 0 0; font-size: 15px; color: #F1F5F9;">
                    Model Confidence: <b>{conf:.1f}%</b> | Latency: <b>{lat:.1f} ms</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 📋 Clinical Recommendations")
            st.info(rec_text)
            
        with c_chart:
            # Horizontal bar chart of probabilities
            labels = list(probs.keys())
            vals = [probs[k] * 100.0 for k in labels]
            colors = ["#10B981", "#3B82F6", "#F59E0B", "#EF4444"]
            
            fig = go.Figure(go.Bar(
                x=vals,
                y=labels,
                orientation='h',
                marker=dict(color=colors, line=dict(color='#38BDF8', width=1.2)),
                text=[f"{v:.1f}%" for v in vals],
                textposition='outside'
            ))
            fig.update_layout(
                title="Class Probability Distribution",
                xaxis_title="Confidence Probability (%)",
                xaxis=dict(range=[0, 115]),
                yaxis_title="",
                template="plotly_dark",
                height=260,
                margin=dict(l=20, r=20, t=35, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Radar chart of vital metrics
            radar_data = {
                "Systolic BP": min(systolic_bp / 1.8, 100.0),
                "Heart Rate": min(heart_rate / 1.3, 100.0),
                "BMI": min(bmi * 2.8, 100.0),
                "Caloric Intake": min(calories_intake / 35.0, 100.0),
                "Alcohol Load": min(alcohol_units * 6.5, 100.0)
            }
            fig_radar = create_radar_chart(radar_data)
            st.plotly_chart(fig_radar, use_container_width=True)
            
    else:
        st.error(f"Inference error: {res.get('message', 'Failed to evaluate model')}")
