"""
app.py
------
Task 6: Streamlit User Interface for Deep Health Risk Neural Network Model.
Features:
- Categorized visual widgets with health icons & emojis.
- Auto-calculating BMI indicator.
- Dynamic dual-mode connection (Direct PyTorch Model vs Flask REST API).
- Interactive Plotly probability distribution visualization.
- Personalized clinical recommendations.
"""

import streamlit as st
import numpy as np
import pandas as pd
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

# ----------------------------------------------------
# 1. Page Configuration & Custom Styling
# ----------------------------------------------------
st.set_page_config(
    page_title="🩺 Health Risk DL Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS for visual polishing
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #E5E7EB;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        padding: 0.6rem 1rem;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. Initialize Model Connector
# ----------------------------------------------------
# ----------------------------------------------------
# 2. Initialize Model Connector
# ----------------------------------------------------
@st.cache_resource
def get_connector():
    return ModelConnector()

connector = get_connector()

# ----------------------------------------------------
# 3. Sidebar Controls & Model Status
# ----------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/000000/medical-heart.png", width=70)
st.sidebar.title("🩺 Control Panel")
st.sidebar.markdown("---")

st.sidebar.subheader("🔌 Model Engine")
st.sidebar.success("🟢 Direct PyTorch Engine Active")
st.sidebar.caption("In-memory `DeepHealthRiskNet` model loader initialized.")

st.sidebar.markdown("---")
st.sidebar.subheader("📋 Preset Sample Inputs")
sample_preset = st.sidebar.selectbox(
    "Load Clinical Preset Sample:",
    ["Default / Custom", "🟢 Healthy / Low Risk Preset", "🔴 Severe / High Risk Preset"]
)

# Preset Values Configuration
if sample_preset == "🟢 Healthy / Low Risk Preset":
    init_val = {
        "age": 28, "height_cm": 175.0, "weight_kg": 68.0,
        "daily_steps": 10500, "calories_intake": 2100, "hours_of_sleep": 7.8,
        "heart_rate": 68, "systolic_bp": 115, "diastolic_bp": 75,
        "exercise_hours_per_week": 5.5, "alcohol_consumption_per_week": 1,
        "smoker": False, "diabetic": False
    }
elif sample_preset == "🔴 Severe / High Risk Preset":
    init_val = {
        "age": 62, "height_cm": 165.0, "weight_kg": 95.0,
        "daily_steps": 2500, "calories_intake": 3200, "hours_of_sleep": 5.2,
        "heart_rate": 105, "systolic_bp": 155, "diastolic_bp": 98,
        "exercise_hours_per_week": 0.5, "alcohol_consumption_per_week": 12,
        "smoker": True, "diabetic": True
    }
else:
    init_val = {
        "age": 45, "height_cm": 170.0, "weight_kg": 75.0,
        "daily_steps": 6500, "calories_intake": 2400, "hours_of_sleep": 6.8,
        "heart_rate": 78, "systolic_bp": 128, "diastolic_bp": 82,
        "exercise_hours_per_week": 2.5, "alcohol_consumption_per_week": 4,
        "smoker": False, "diabetic": False
    }

# ----------------------------------------------------
# 4. Main Body UI Header
# ----------------------------------------------------
st.markdown('<div class="main-header">🩺 Deep Learning Health Risk Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Clinical Decision Support powered by PyTorch 3-Layer Neural Network (<code>DeepHealthRiskNet</code>)</div>', unsafe_allow_html=True)

st.info("💡 **Instructions**: Adjust the 14 patient physiological and lifestyle metrics below, then click **⚡ Run Inference** to compute clinical health risk probabilities.")

# ----------------------------------------------------
# 5. Form Input Widgets Grouped by Categories
# ----------------------------------------------------
with st.form("clinical_form"):
    st.subheader("📋 Patient Clinical Assessment Form")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 👤 Category 1: Demographics & Body Metrics")
        age = st.number_input("🎂 Age (years)", min_value=1, max_value=120, value=int(init_val["age"]), step=1)
        height_cm = st.number_input("📏 Height (cm)", min_value=50.0, max_value=250.0, value=float(init_val["height_cm"]), step=0.5)
        weight_kg = st.number_input("⚖️ Weight (kg)", min_value=10.0, max_value=300.0, value=float(init_val["weight_kg"]), step=0.5)
        
        # Dynamic live BMI calculation display
        current_bmi = calculate_bmi(weight_kg, height_cm)
        st.metric("🧮 Auto-Calculated BMI", f"{current_bmi:.2f} kg/m²", 
                  delta="Normal" if 18.5 <= current_bmi <= 24.9 else ("Overweight" if current_bmi >= 25 else "Underweight"),
                  delta_color="normal" if 18.5 <= current_bmi <= 24.9 else "inverse")

        st.markdown("#### 🏃 Category 2: Daily Activity & Nutrition")
        daily_steps = st.number_input("👟 Daily Steps", min_value=0, max_value=50000, value=int(init_val["daily_steps"]), step=500)
        calories_intake = st.number_input("🍎 Calories Intake (kcal/day)", min_value=500, max_value=10000, value=int(init_val["calories_intake"]), step=50)
        hours_of_sleep = st.slider("💤 Hours of Sleep per Night", min_value=0.0, max_value=16.0, value=float(init_val["hours_of_sleep"]), step=0.1)

    with col2:
        st.markdown("#### 🫀 Category 3: Vital Signs & Cardiovascular")
        heart_rate = st.number_input("💓 Resting Heart Rate (bpm)", min_value=30, max_value=220, value=int(init_val["heart_rate"]), step=1)
        systolic_bp = st.number_input("🩸 Systolic Blood Pressure (mmHg)", min_value=60, max_value=240, value=int(init_val["systolic_bp"]), step=1)
        diastolic_bp = st.number_input("🩺 Diastolic Blood Pressure (mmHg)", min_value=30, max_value=160, value=int(init_val["diastolic_bp"]), step=1)

        st.markdown("#### 🚬 Category 4: Lifestyle & Medical Conditions")
        exercise_hours = st.slider("🏋️ Exercise (hours/week)", min_value=0.0, max_value=40.0, value=float(init_val["exercise_hours_per_week"]), step=0.5)
        alcohol_units = st.number_input("🍷 Alcohol Consumption (units/week)", min_value=0, max_value=100, value=int(init_val["alcohol_consumption_per_week"]), step=1)
        
        st.write("🏥 Risk Pre-conditions:")
        smoker_flag = st.checkbox("🚬 Active Smoker", value=bool(init_val["smoker"]))
        diabetic_flag = st.checkbox("🩹 Diagnosed Diabetic", value=bool(init_val["diabetic"]))

    st.markdown("---")
    submit_btn = st.form_submit_button("⚡ Run Neural Network Inference")

# ----------------------------------------------------
# 6. Inference Execution & Output Visualizations
# ----------------------------------------------------
if submit_btn:
    # Feature vector construction (exact 14 features matching PyTorch model schema)
    feature_dict = {
        "age": float(age),
        "height_cm": float(height_cm),
        "weight_kg": float(weight_kg),
        "bmi": float(current_bmi),
        "daily_steps": float(daily_steps),
        "calories_intake": float(calories_intake),
        "hours_of_sleep": float(hours_of_sleep),
        "heart_rate": float(heart_rate),
        "systolic_bp": float(systolic_bp),
        "diastolic_bp": float(diastolic_bp),
        "exercise_hours_per_week": float(exercise_hours),
        "alcohol_consumption_per_week": float(alcohol_units),
        "smoker": 1.0 if smoker_flag else 0.0,
        "diabetic": 1.0 if diabetic_flag else 0.0
    }
    
    feature_vector = [feature_dict[name] for name in FEATURE_NAMES]

    st.markdown("---")
    st.subheader("🎯 Neural Network Prediction Results")

    with st.spinner("🧠 Executing PyTorch forward pass & computing softmax probabilities..."):
        try:
            result = connector.predict(feature_vector)
            pred_label = result.get("predicted_label", "Low Risk")
            confidence = result.get("confidence_score", 0.0)
            probabilities = result.get("class_probabilities", {})
            latency = result.get("latency_ms", 0.0)
            mode_used = result.get("mode", "Direct PyTorch Engine 🧠")

            meta = RISK_METADATA.get(pred_label, RISK_METADATA["Low Risk"])

            # Render Result Banner & Metrics
            res_col1, res_col2, res_col3, res_col4 = st.columns([2, 1, 1, 1])
            
            with res_col1:
                st.markdown(f"### Diagnostic Assessment: {meta['badge']}")
                st.write(meta["description"])
            
            with res_col2:
                st.metric("🎯 Confidence Score", f"{confidence * 100:.1f}%")

            with res_col3:
                st.metric("⏱️ Inference Latency", f"{latency} ms")

            with res_col4:
                st.metric("⚙️ Execution Engine", mode_used.split()[0])

            # Class Probability Bar Chart (Plotly)
            st.markdown("#### 📊 Risk Class Probability Distribution")
            df_probs = pd.DataFrame({
                "Risk Category": list(probabilities.keys()),
                "Probability (%)": [v * 100 for v in probabilities.values()]
            })

            color_map = {
                "Low Risk": "#28a745",
                "Moderate Risk": "#ffc107",
                "High Risk": "#fd7e14",
                "Critical Risk": "#dc3545"
            }
            df_probs["Color"] = df_probs["Risk Category"].map(color_map)

            fig = px.bar(
                df_probs,
                x="Risk Category",
                y="Probability (%)",
                color="Risk Category",
                color_discrete_map=color_map,
                text_auto=".1f",
                title="Model Softmax Probability Breakdown"
            )
            fig.update_layout(
                yaxis_range=[0, 100],
                showlegend=False,
                height=350,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)

            # Personalized Clinical Recommendations
            st.markdown("#### 💡 Clinical Guidance & Recommendations")
            recs = generate_recommendations(feature_dict, pred_label)
            for r in recs:
                st.write(f"- {r}")

            # Developer Payload Expander
            with st.expander("🛠️ View Full JSON Prediction Payload"):
                st.json(result)

        except Exception as e:
            st.error(f"❌ Prediction Error: {str(e)}")
