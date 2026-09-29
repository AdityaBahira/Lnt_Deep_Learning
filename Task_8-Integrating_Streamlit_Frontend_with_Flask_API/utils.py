"""
utils.py
--------
Task 8 Helper Utilities:
1. Flask API & PyTorch Model Connector (HTTP REST API Client & Direct Fallback Engine).
2. Dataset Ingestion (health_activity_data.csv).
3. Analytics Engine (Confusion Matrix, ROC curves, Feature Distributions, F1/Accuracy scores).
4. Real-time Batch Inference Engine for cohort evaluation.
"""

import os
import sys
import json
import time
import requests
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

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
    """
    Connects Streamlit Frontend with Flask REST API (and provides Direct PyTorch Fallback).
    """

    def __init__(self, default_api_url="http://127.0.0.1:5000"):
        self.default_api_url = default_api_url.rstrip("/")
        self.direct_engine = None

    def _get_direct_engine(self):
        if self.direct_engine is None:
            try:
                from model_loader import get_model_engine
                self.direct_engine = get_model_engine()
            except Exception as e:
                self.direct_engine = None
        return self.direct_engine

    def check_api_health(self, api_url=None):
        """Probes GET /health endpoint of the Flask REST API."""
        url = (api_url or self.default_api_url).rstrip("/") + "/health"
        try:
            start = time.time()
            resp = requests.get(url, timeout=3.0)
            latency = round((time.time() - start) * 1000, 2)
            if resp.status_code == 200:
                data = resp.json()
                data["online"] = True
                data["rtt_ms"] = latency
                return data
            else:
                return {
                    "online": False,
                    "status_code": resp.status_code,
                    "rtt_ms": latency,
                    "message": f"Flask API returned status code {resp.status_code}"
                }
        except requests.exceptions.RequestException as req_err:
            return {
                "online": False,
                "error": str(req_err),
                "message": f"Could not connect to Flask API at {url}. Ensure server is running."
            }

    def predict_single(self, feature_vector, mode="API", api_url=None):
        """
        Runs single sample prediction either via Flask API (HTTP POST /predict)
        or via Direct PyTorch Model Engine.
        """
        target_url = (api_url or self.default_api_url).rstrip("/")
        
        if mode.upper() == "API":
            endpoint = f"{target_url}/predict"
            payload = {"features": feature_vector}
            start_time = time.time()
            try:
                response = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=5.0)
                rtt_ms = round((time.time() - start_time) * 1000, 2)
                
                if response.status_code == 200:
                    json_resp = response.json()
                    preds = json_resp.get("predictions", [])
                    if preds:
                        res_data = preds[0]
                        res_data["rtt_ms"] = rtt_ms
                        res_data["backend_latency_ms"] = json_resp.get("latency_ms", 0.0)
                        res_data["mode"] = "Flask REST API 🌐"
                        res_data["http_status"] = 200
                        return res_data
                    else:
                        raise RuntimeError("Flask API returned empty predictions array.")
                else:
                    err_msg = response.json().get("message", response.text) if response.headers.get("content-type") == "application/json" else response.text
                    raise RuntimeError(f"HTTP {response.status_code} from Flask API: {err_msg}")
            except requests.exceptions.RequestException as req_err:
                raise RuntimeError(f"Failed to communicate with Flask API at {endpoint}: {str(req_err)}")

        # Fallback / Direct Mode
        engine = self._get_direct_engine()
        if not engine:
            raise RuntimeError("Direct PyTorch Model Engine is not available.")
        
        start_time = time.time()
        results = engine.predict([feature_vector])
        rtt_ms = round((time.time() - start_time) * 1000, 2)
        res_data = results[0]
        res_data["rtt_ms"] = rtt_ms
        res_data["backend_latency_ms"] = rtt_ms
        res_data["mode"] = "Direct PyTorch Engine 🧠"
        res_data["http_status"] = 200
        return res_data

    def predict_batch(self, feature_matrix, mode="API", api_url=None):
        """
        Runs batch predictions either via Flask API (HTTP POST /predict)
        or via Direct PyTorch Engine.
        """
        target_url = (api_url or self.default_api_url).rstrip("/")
        
        if mode.upper() == "API":
            endpoint = f"{target_url}/predict"
            payload = {"instances": feature_matrix}
            start_time = time.time()
            try:
                response = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=30.0)
                rtt_ms = round((time.time() - start_time) * 1000, 2)
                
                if response.status_code == 200:
                    json_resp = response.json()
                    preds = json_resp.get("predictions", [])
                    backend_ms = json_resp.get("latency_ms", 0.0)
                    return preds, rtt_ms, backend_ms
                else:
                    err_msg = response.json().get("message", response.text) if response.headers.get("content-type") == "application/json" else response.text
                    raise RuntimeError(f"HTTP {response.status_code} from Flask API: {err_msg}")
            except requests.exceptions.RequestException as req_err:
                raise RuntimeError(f"Failed to communicate with Flask API at {endpoint}: {str(req_err)}")

        # Fallback / Direct Mode
        engine = self._get_direct_engine()
        if not engine:
            raise RuntimeError("Direct PyTorch Model Engine is not available.")
        
        start_time = time.time()
        results = engine.predict(feature_matrix)
        rtt_ms = round((time.time() - start_time) * 1000, 2)
        return results, rtt_ms, rtt_ms

def load_dataset():
    """Robustly loads health_activity_data.csv from Task 8 directory or fallback paths."""
    possible_paths = [
        os.path.join(CURR_DIR, "health_activity_data.csv"),
        os.path.abspath("health_activity_data.csv"),
        os.path.abspath("Task 8/health_activity_data.csv"),
        os.path.abspath("../Backend/health_activity_data.csv")
    ]
    for p in possible_paths:
        if os.path.exists(p):
            return pd.read_csv(p)
    raise FileNotFoundError(f"Dataset file 'health_activity_data.csv' not found. Checked: {possible_paths}")

def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0:
        return 0.0
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)

def compute_dataset_analytics(connector, mode="API", api_url=None):
    """Computes full model evaluation analytics on health_activity_data.csv."""
    df = load_dataset()
    
    features_list = []
    scores = []
    
    for idx, row in df.iterrows():
        bp_str = str(row.get("Blood_Pressure", "120/80"))
        sys_bp, dia_bp = map(float, bp_str.split("/")) if "/" in bp_str else (120.0, 80.0)
            
        smoker_val = 1.0 if str(row.get("Smoker", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
        diabetic_val = 1.0 if str(row.get("Diabetic", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
        heart_disease_val = 1.0 if str(row.get("Heart_Disease", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
        
        age_val = float(row.get("Age", 45))
        h_cm = float(row.get("Height_cm", 170.0))
        w_kg = float(row.get("Weight_kg", 70.0))
        bmi_val = float(row.get("BMI", calculate_bmi(w_kg, h_cm)))
        steps_val = float(row.get("Daily_Steps", 5000))
        cal_val = float(row.get("Calories_Intake", 2000))
        sleep_val = float(row.get("Hours_of_Sleep", 7.0))
        hr_val = float(row.get("Heart_Rate", 75))
        ex_val = float(row.get("Exercise_Hours_per_Week", 2.0))
        alc_val = float(row.get("Alcohol_Consumption_per_Week", 0.0))

        vec = [
            age_val, h_cm, w_kg, bmi_val, steps_val, cal_val, sleep_val,
            hr_val, sys_bp, dia_bp, ex_val, alc_val, smoker_val, diabetic_val
        ]
        features_list.append(vec)

        # Multi-Condition Clinical Health Risk Score formula
        score = (
            0.03 * age_val +
            0.04 * (sys_bp - 120.0) +
            0.02 * (dia_bp - 80.0) +
            0.05 * (bmi_val - 22.0) +
            0.02 * (hr_val - 70.0) +
            1.5 * smoker_val +
            1.8 * diabetic_val +
            2.2 * heart_disease_val +
            0.15 * alc_val -
            0.10 * ex_val -
            0.0001 * steps_val
        )
        scores.append(score)

    scores = np.array(scores)
    q25, q50, q75 = np.percentile(scores, [25, 50, 75])
    y_true = np.zeros(len(scores), dtype=int)
    y_true[scores >= q25] = 1
    y_true[scores >= q50] = 2
    y_true[scores >= q75] = 3

    # Execute batch predictions via connector (API or Direct)
    results, rtt_ms, backend_ms = connector.predict_batch(features_list, mode=mode, api_url=api_url)
    
    preds = [r["predicted_class_id"] for r in results]
    probs = np.array([[r["class_probabilities"][c] for c in RISK_CLASSES] for r in results])
    
    cm = confusion_matrix(y_true, preds, labels=[0, 1, 2, 3])
    acc = np.mean(np.array(y_true) == np.array(preds))
    
    return {
        "df": df,
        "features_list": features_list,
        "y_true": y_true,
        "y_pred": preds,
        "y_prob": probs,
        "confusion_matrix": cm,
        "accuracy": round(float(acc), 4),
        "rtt_ms": rtt_ms,
        "backend_ms": backend_ms
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
