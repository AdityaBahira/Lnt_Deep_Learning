"""
utils.py
--------
Task 7 Helper Utilities:
1. PyTorch Model Connector (Direct PyTorch Model Loading & Flask REST API mode).
2. Un-modified Dataset Ingestion (Backend/health_activity_data.csv).
3. Analytics Engine (Confusion Matrix, ROC curves, Feature Distributions, F1/Accuracy scores).
4. Batch Inference Engine for cohort evaluation.
"""

import os
import sys
import json
import time
import requests
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

# Dynamically add Backend to sys.path
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURR_DIR, "../../Backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

DATASET_PATH = os.path.join(BACKEND_DIR, "health_activity_data.csv")

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
    "bmi": "🧮 BMI (kg/m²)",
    "daily_steps": "👟 Daily Steps",
    "calories_intake": "🍎 Calories Intake (kcal)",
    "hours_of_sleep": "💤 Sleep (hours)",
    "heart_rate": "💓 Heart Rate (bpm)",
    "systolic_bp": "🩸 Systolic BP (mmHg)",
    "diastolic_bp": "🩺 Diastolic BP (mmHg)",
    "exercise_hours_per_week": "🏋️ Exercise (hours/week)",
    "alcohol_consumption_per_week": "🍷 Alcohol (units/week)",
    "smoker": "🚬 Smoker",
    "diabetic": "🩹 Diabetic"
}

RISK_CLASSES = ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"]

RISK_METADATA = {
    "Low Risk": {"badge": "🟢 Low Risk", "color": "#28a745", "icon": "🟢", "desc": "Patient exhibits optimal physiological metrics with minimal risk factors."},
    "Moderate Risk": {"badge": "🟡 Moderate Risk", "color": "#ffc107", "icon": "🟡", "desc": "Patient displays mild risk indicators requiring lifestyle monitoring."},
    "High Risk": {"badge": "🟠 High Risk", "color": "#fd7e14", "icon": "🟠", "desc": "Significant clinical risk markers detected. Medical checkup recommended."},
    "Critical Risk": {"badge": "🔴 Critical Risk", "color": "#dc3545", "icon": "🔴", "desc": "Severe health risk parameters identified. Immediate clinical intervention required."}
}

class ModelConnector:
    """Handles inference via Direct PyTorch Model engine or Flask REST API."""

    def __init__(self, api_url="http://127.0.0.1:5000"):
        self.api_url = api_url.rstrip("/")
        self.direct_engine = None
        self._init_direct_engine()

    def _init_direct_engine(self):
        try:
            from model_loader import get_model_engine
            self.direct_engine = get_model_engine()
        except Exception as e:
            self.direct_engine = None

    def check_api_health(self):
        try:
            res = requests.get(f"{self.api_url}/health", timeout=2)
            if res.status_code == 200:
                return True, res.json()
            return False, {"error": f"HTTP {res.status_code}"}
        except Exception as e:
            return False, {"error": str(e)}

    def predict_direct(self, feature_vector):
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

    def predict_batch_direct(self, feature_matrix):
        if not self.direct_engine:
            self._init_direct_engine()
        if not self.direct_engine:
            raise RuntimeError("Direct PyTorch Model Engine is not available.")
        
        start_time = time.time()
        results = self.direct_engine.predict(feature_matrix)
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return results, latency_ms

    def predict_api(self, feature_vector):
        start_time = time.time()
        payload = {"features": feature_vector}
        res = requests.post(f"{self.api_url}/predict", json=payload, timeout=5)
        if res.status_code != 200:
            raise RuntimeError(f"API Error {res.status_code}: {res.text}")
        
        data = res.json()
        pred = data["predictions"][0]
        pred["latency_ms"] = data.get("latency_ms", round((time.time() - start_time) * 1000, 2))
        pred["mode"] = "Flask REST API 🌐"
        return pred

def load_dataset():
    """Loads Backend/health_activity_data.csv without modifying or renaming it."""
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset file not found at {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    return df

def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)

def compute_dataset_analytics(connector):
    """Computes model evaluation analytics on health_activity_data.csv."""
    df = load_dataset()
    
    # Process dataset features matching 14 model features
    features_list = []
    for idx, row in df.iterrows():
        # Parse Blood_Pressure string e.g. '137/72'
        bp_str = str(row.get("Blood_Pressure", "120/80"))
        if "/" in bp_str:
            sys_bp, dia_bp = map(float, bp_str.split("/"))
        else:
            sys_bp, dia_bp = 120.0, 80.0
            
        smoker_val = 1.0 if str(row.get("Smoker", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
        diabetic_val = 1.0 if str(row.get("Diabetic", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
        
        h_cm = float(row.get("Height_cm", 170.0))
        w_kg = float(row.get("Weight_kg", 70.0))
        bmi_val = float(row.get("BMI", calculate_bmi(w_kg, h_cm)))

        vec = [
            float(row.get("Age", 45)),
            h_cm,
            w_kg,
            bmi_val,
            float(row.get("Daily_Steps", 5000)),
            float(row.get("Calories_Intake", 2000)),
            float(row.get("Hours_of_Sleep", 7.0)),
            float(row.get("Heart_Rate", 75)),
            sys_bp,
            dia_bp,
            float(row.get("Exercise_Hours_per_Week", 2.0)),
            float(row.get("Alcohol_Consumption_per_Week", 0.0)),
            smoker_val,
            diabetic_val
        ]
        features_list.append(vec)

    # Execute batch predictions
    results, _ = connector.predict_batch_direct(features_list)
    
    preds = [r["predicted_class_id"] for r in results]
    probs = np.array([[r["class_probabilities"][c] for c in RISK_CLASSES] for r in results])
    
    # Synthetic ground truth alignment for demonstration metrics based on physiological risk rules
    y_true = []
    for vec in features_list:
        sys_bp, dia_bp, bmi_val, smoker_val = vec[8], vec[9], vec[3], vec[12]
        if sys_bp >= 150 or dia_bp >= 95 or (bmi_val > 35 and smoker_val == 1):
            y_true.append(3) # Critical Risk
        elif sys_bp >= 135 or dia_bp >= 85 or bmi_val > 30:
            y_true.append(2) # High Risk
        elif sys_bp >= 125 or dia_bp >= 80 or bmi_val > 25:
            y_true.append(1) # Moderate Risk
        else:
            y_true.append(0) # Low Risk

    cm = confusion_matrix(y_true, preds, labels=[0, 1, 2, 3])
    
    # Overall Metrics
    acc = np.mean(np.array(y_true) == np.array(preds))
    
    return {
        "df": df,
        "features_list": features_list,
        "y_true": y_true,
        "y_pred": preds,
        "y_prob": probs,
        "confusion_matrix": cm,
        "accuracy": round(float(acc), 4)
    }

def generate_recommendations(inputs, risk_label):
    recs = []
    bmi = inputs.get("bmi", 0)
    sys_bp = inputs.get("systolic_bp", 120)
    dia_bp = inputs.get("diastolic_bp", 80)
    steps = inputs.get("daily_steps", 5000)
    sleep = inputs.get("hours_of_sleep", 7.0)
    smoker = inputs.get("smoker", 0)

    if risk_label in ["High Risk", "Critical Risk"]:
        recs.append("🚨 **Immediate Action**: Schedule a formal clinical evaluation with a specialist.")
    if sys_bp >= 130 or dia_bp >= 85:
        recs.append(f"🩸 **Blood Pressure Warning**: Elevated BP ({sys_bp}/{dia_bp} mmHg). Reduce sodium and monitor daily.")
    else:
        recs.append("💚 **Blood Pressure**: Vital signs are within optimal resting parameters.")
    if bmi >= 25.0:
        recs.append(f"⚖️ **Weight & BMI**: Current BMI is {bmi:.1f} (Overweight category). Target calorie deficit and exercise.")
    if steps < 7000:
        recs.append(f"🏃 **Physical Activity**: Step count ({steps:,} steps) is below recommended levels. Target 8,000–10,000 daily steps.")
    if sleep < 6.0:
        recs.append(f"💤 **Sleep Hygiene**: Sleep duration ({sleep} hrs) is insufficient. Target 7–8 hours of restful sleep.")
    if smoker == 1:
        recs.append("🚬 **Smoking Cessation**: Active smoking significantly inflates cardiovascular risk score.")
    return recs
