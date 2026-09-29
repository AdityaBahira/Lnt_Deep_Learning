"""
3_Batch_Processing.py
---------------------
Page 3: Cohort CSV Batch Ingestion & Real-Time REST API Processing.
Demonstrates batch payload HTTP requests over Flask API, throughput metrics, and report export.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from utils import (
    ModelConnector,
    FEATURE_NAMES,
    FEATURE_LABELS,
    RISK_METADATA,
    calculate_bmi
)

st.title("📁 Cohort CSV Ingestion & Batch API Processing")
st.write("Ingest patient cohort CSV datasets and execute high-throughput batch predictions over the Flask REST API (`POST /predict`).")

st.divider()

# Connection Mode Banner
conn_mode = st.session_state.get("connection_mode", "Flask REST API 🌐")
api_url = st.session_state.get("api_url", "http://127.0.0.1:5000")

@st.cache_resource
def get_connector(url):
    return ModelConnector(default_api_url=url)

connector = get_connector(api_url)

# Data Ingestion Source
source = st.radio("Choose Ingestion Source:", ["Use Pre-loaded Sample Cohort (`sample_cohort_data.csv`)", "Upload Custom Cohort CSV File"], horizontal=True)

df_raw = None
if "Sample Cohort" in source:
    sample_path = os.path.join(os.path.dirname(__file__), "../sample_cohort_data.csv")
    if os.path.exists(sample_path):
        df_raw = pd.read_csv(sample_path)
        st.success(f"✅ Pre-loaded sample cohort dataset with **{len(df_raw)} records**.")
    else:
        st.error(f"Sample cohort file '{sample_path}' not found.")
else:
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])
    if uploaded_file is not None:
        df_raw = pd.read_csv(uploaded_file)
        st.success(f"✅ Uploaded custom cohort with **{len(df_raw)} records**.")

if df_raw is not None:
    st.subheader("📋 Ingested Cohort Data Preview")
    st.dataframe(df_raw.head(10), use_container_width=True)

    if st.button("⚡ Process Cohort via Flask REST API", type="primary", use_container_width=True):
        # Extract features for each row
        feature_matrix = []
        for idx, row in df_raw.iterrows():
            bp_str = str(row.get("Blood_Pressure", "120/80"))
            sys_bp, dia_bp = map(float, bp_str.split("/")) if "/" in bp_str else (120.0, 80.0)
                
            smoker_val = 1.0 if str(row.get("Smoker", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
            diabetic_val = 1.0 if str(row.get("Diabetic", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
            
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
            feature_matrix.append(vec)

        mode_arg = "API" if conn_mode.startswith("Flask") else "DIRECT"

        with st.spinner(f"🌐 Transmitting batch request ({len(feature_matrix)} samples) to Flask API..."):
            try:
                results, rtt_ms, backend_ms = connector.predict_batch(feature_matrix, mode=mode_arg, api_url=api_url)

                st.divider()
                st.subheader("📊 Batch Inference Metrics & Execution Summary")
                
                b_col1, b_col2, b_col3, b_col4 = st.columns(4)
                with b_col1:
                    st.metric("Total Cohort Size", f"{len(results)} Patients")
                with b_col2:
                    st.metric("Total RTT Latency", f"{rtt_ms:.2f} ms")
                with b_col3:
                    st.metric("Avg Latency per Sample", f"{rtt_ms / max(len(results), 1):.2f} ms")
                with b_col4:
                    st.metric("Throughput", f"{int(len(results) / (rtt_ms / 1000.0 + 1e-6)):,} samples/sec")

                # Attach predictions to DataFrame
                df_out = df_raw.copy()
                df_out["Predicted_Risk_Class"] = [r["predicted_label"] for r in results]
                df_out["Confidence_Score"] = [r["confidence_score"] for r in results]

                col_chart1, col_chart2 = st.columns([1, 1])
                
                with col_chart1:
                    st.subheader("Cohort Health Risk Breakdown")
                    risk_counts = df_out["Predicted_Risk_Class"].value_counts().reset_index()
                    risk_counts.columns = ["Risk Class", "Patient Count"]
                    
                    fig_pie = px.pie(
                        risk_counts, names="Risk Class", values="Patient Count",
                        color="Risk Class",
                        color_discrete_map={
                            "Low Risk": "#28a745", "Moderate Risk": "#ffc107",
                            "High Risk": "#fd7e14", "Critical Risk": "#dc3545"
                        },
                        hole=0.4
                    )
                    fig_pie.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col_chart2:
                    st.subheader("Patient Count by Risk Category")
                    fig_bar = px.bar(
                        risk_counts, x="Risk Class", y="Patient Count",
                        color="Risk Class",
                        color_discrete_map={
                            "Low Risk": "#28a745", "Moderate Risk": "#ffc107",
                            "High Risk": "#fd7e14", "Critical Risk": "#dc3545"
                        },
                        text_auto=True
                    )
                    fig_bar.update_layout(height=320, showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)

                st.divider()
                st.subheader("📋 Complete Inferred Patient Cohort Table")
                st.dataframe(df_out, use_container_width=True)

                # Export CSV
                csv_bytes = df_out.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Inferred Cohort CSV Report",
                    data=csv_bytes,
                    file_name="cohort_predictions_task8.csv",
                    mime="text/csv",
                    type="primary"
                )

            except Exception as e:
                st.error(f"❌ Batch Inference Error: {str(e)}")
                st.info("💡 Verify that Flask API is online (`python flask_api.py`) or switch connection mode.")
