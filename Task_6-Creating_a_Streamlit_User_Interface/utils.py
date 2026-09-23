"""
utils.py
--------
Helper functions for Streamlit UI:
1. PyTorch Model loading & inference engine connection (Direct PyTorch vs REST API mode).
2. Data preprocessing & feature array building.
3. Clinical recommendations and icon mapping.
"""

import os
import sys
import time
import numpy as np

# Dynamically add Backend to sys.path to enable importing model_loader
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

FEATURE_NAMES = [
    "age", "height_cm", "weight_kg", "bmi",
    "daily_steps", "calories_intake", "hours_of_sleep",
    "heart_rate", "systolic_bp", "diastolic_bp",
    "exercise_hours_per_week", "alcohol_consumption_per_week",
    "smoker", "diabetic"
]

FEATURE_LABELS = {
    "age": "🎂 Age (years)",
    "height_cm": "📏 Height (cm)",
    "weight_kg": "⚖️ Weight (kg)",
    "bmi": "🧮 Body Mass Index (BMI)",
    "daily_steps": "👟 Daily Steps",
    "calories_intake": "🍎 Calories Intake (kcal)",
    "hours_of_sleep": "💤 Sleep (hours/night)",
    "heart_rate": "💓 Heart Rate (bpm)",
    "systolic_bp": "🩸 Systolic BP (mmHg)",
    "diastolic_bp": "🩺 Diastolic BP (mmHg)",
    "exercise_hours_per_week": "🏋️ Exercise (hours/week)",
    "alcohol_consumption_per_week": "🍷 Alcohol (units/week)",
    "smoker": "🚬 Smoker",
    "diabetic": "🩹 Diabetic"
}

RISK_METADATA = {
    "Low Risk": {
        "badge": "🟢 Low Risk",
        "color": "#28a745",
        "icon": "🟢",
        "alert_type": "success",
        "description": "Patient exhibits optimal physiological metrics and minimal clinical risk factors."
    },
    "Moderate Risk": {
        "badge": "🟡 Moderate Risk",
        "color": "#ffc107",
        "icon": "🟡",
        "alert_type": "warning",
        "description": "Patient displays mild indicators requiring preventative lifestyle adjustments."
    },
    "High Risk": {
        "badge": "🟠 High Risk",
        "color": "#fd7e14",
        "icon": "🟠",
        "alert_type": "warning",
        "description": "Significant clinical risk markers detected. Medical evaluation recommended."
    },
    "Critical Risk": {
        "badge": "🔴 Critical Risk",
        "color": "#dc3545",
        "icon": "🔴",
        "alert_type": "error",
        "description": "Severe health risk parameters identified. Immediate clinical intervention required."
    }
}

class ModelConnector:
    """Handles direct PyTorch Deep Neural Network model loading and inference."""

    def __init__(self):
        self.direct_engine = None
        self._init_direct_engine()

    def _init_direct_engine(self):
        """Attempts to initialize direct PyTorch inference engine from Backend."""
        try:
            from model_loader import get_model_engine
            self.direct_engine = get_model_engine()
        except Exception as e:
            self.direct_engine = None

    def predict(self, feature_vector):
        """Runs inference directly using in-memory PyTorch model engine."""
        if not self.direct_engine:
            self._init_direct_engine()
        if not self.direct_engine:
            raise RuntimeError("Direct PyTorch Model Engine is not available.")
        
        start_time = time.time()
        results = self.direct_engine.predict([feature_vector])
        latency_ms = round((time.time() - start_time) * 1000, 2)
        res_data = results[0]
        res_data["latency_ms"] = latency_ms
        res_data["mode"] = "Direct PyTorch Engine 🧠"
        return res_data

def calculate_bmi(weight_kg, height_cm):
    """Calculates Body Mass Index (BMI)."""
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)

def generate_recommendations(inputs, risk_label):
    """Generates personalized clinical recommendations based on inputs & risk."""
    recs = []
    bmi = inputs.get("bmi", 0)
    sys_bp = inputs.get("systolic_bp", 120)
    dia_bp = inputs.get("diastolic_bp", 80)
    steps = inputs.get("daily_steps", 5000)
    sleep = inputs.get("hours_of_sleep", 7.0)
    smoker = inputs.get("smoker", 0)

    if risk_label in ["High Risk", "Critical Risk"]:
        recs.append("🚨 **Immediate Action**: Schedule a formal clinical checkup with a physician for comprehensive diagnostic evaluation.")
    
    if sys_bp >= 130 or dia_bp >= 85:
        recs.append(f"🩸 **Blood Pressure Warning**: Elevated blood pressure ({sys_bp}/{dia_bp} mmHg). Reduce sodium intake and monitor daily.")
    else:
        recs.append("💚 **Blood Pressure**: Vital signs are within optimal resting ranges.")

    if bmi >= 25.0:
        recs.append(f"⚖️ **Weight & BMI**: Current BMI is {bmi:.1f} (Overweight category). Aim for a balanced caloric restriction diet.")
    elif bmi < 18.5:
        recs.append(f"⚖️ **Weight & BMI**: Current BMI is {bmi:.1f} (Underweight category). Ensure adequate nutrient intake.")

    if steps < 7000:
        recs.append(f"🏃 **Physical Activity**: Daily step count ({steps:,} steps) is below recommended levels. Target 8,000–10,000 daily steps.")
    else:
        recs.append("👟 **Physical Activity**: Excellent step count activity maintained.")

    if sleep < 6.0:
        recs.append(f"💤 **Sleep Hygiene**: Sleep duration ({sleep} hrs) is insufficient. Aim for 7–8 hours of restful sleep nightly.")

    if smoker == 1:
        recs.append("🚬 **Smoking Cessation**: Active smoking significantly inflates cardiovascular and overall health risk score.")

    return recs
