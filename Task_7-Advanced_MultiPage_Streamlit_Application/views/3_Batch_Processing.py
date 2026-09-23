"""
4_Batch_Processing.py
---------------------
Page 4: Cohort Batch Ingestion, Batch Neural Network Inference & Downloadable CSV Report Exporter.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from utils import (
    ModelConnector,
    calculate_bmi,
    RISK_METADATA,
    FEATURE_NAMES
)

st.title("📁 Bulk Batch Ingestion & Cohort Report Generator")
st.write("Upload bulk patient CSV datasets to execute batch PyTorch forward-pass inferences and generate exportable clinical reports.")

st.divider()

@st.cache_resource
def get_connector():
    return ModelConnector()

connector = get_connector()

uploaded_file = st.file_uploader("📥 Upload Patient Cohort CSV File:", type=["csv"])

use_sample = st.checkbox("💡 Or click here to run batch inference on Backend/health_activity_data.csv sample (First 20 patients)", value=False)

if uploaded_file is not None or use_sample:
    try:
        if uploaded_file is not None:
            df_in = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded uploaded dataset containing **{len(df_in):,} patient records**.")
        else:
            from utils import load_dataset
            df_in = load_dataset().head(20)
            st.info("ℹ️ Using sample cohort from `Backend/health_activity_data.csv` (First 20 records).")

        with st.expander("🔍 Preview Input Data"):
            st.dataframe(df_in.head(10), use_container_width=True)

        if st.button("⚡ Execute Batch Inferences", use_container_width=True, type="primary"):
            with st.spinner(f"🧠 Running batch PyTorch forward passes on {len(df_in)} records..."):
                features_list = []
                for idx, row in df_in.iterrows():
                    bp_str = str(row.get("Blood_Pressure", "120/80"))
                    sys_bp, dia_bp = map(float, bp_str.split("/")) if "/" in bp_str else (120.0, 80.0)
                    
                    smk = 1.0 if str(row.get("Smoker", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
                    diab = 1.0 if str(row.get("Diabetic", "No")).strip().lower() in ["yes", "1", "true"] else 0.0
                    
                    h_cm = float(row.get("Height_cm", 170.0))
                    w_kg = float(row.get("Weight_kg", 70.0))
                    bmi_val = float(row.get("BMI", calculate_bmi(w_kg, h_cm)))

                    vec = [
                        float(row.get("Age", 45)), h_cm, w_kg, bmi_val,
                        float(row.get("Daily_Steps", 5000)), float(row.get("Calories_Intake", 2000)), float(row.get("Hours_of_Sleep", 7.0)),
                        float(row.get("Heart_Rate", 75)), sys_bp, dia_bp,
                        float(row.get("Exercise_Hours_per_Week", 2.0)), float(row.get("Alcohol_Consumption_per_Week", 0.0)),
                        smk, diab
                    ]
                    features_list.append(vec)

                results, latency_ms = connector.predict_batch_direct(features_list)

                # Format Output Dataframe
                out_rows = []
                for idx, res in enumerate(results):
                    out_rows.append({
                        "Patient_ID": df_in.iloc[idx].get("ID", idx+1),
                        "Age": features_list[idx][0],
                        "BMI": features_list[idx][3],
                        "Systolic_BP": features_list[idx][8],
                        "Diastolic_BP": features_list[idx][9],
                        "Predicted_Risk_Class": res["predicted_label"],
                        "Confidence_Score": f"{res['confidence_score']*100:.1f}%",
                        "Low_Risk_Prob": f"{res['class_probabilities']['Low Risk']*100:.1f}%",
                        "Moderate_Risk_Prob": f"{res['class_probabilities']['Moderate Risk']*100:.1f}%",
                        "High_Risk_Prob": f"{res['class_probabilities']['High Risk']*100:.1f}%",
                        "Critical_Risk_Prob": f"{res['class_probabilities']['Critical Risk']*100:.1f}%"
                    })
                df_out = pd.DataFrame(out_rows)

                st.divider()
                st.header("🎯 Batch Inference Summary")
                
                b1, b2, b3 = st.columns(3)
                b1.metric("📊 Total Patients Assessed", f"{len(df_out):,}")
                b2.metric("⏱️ Batch Processing Latency", f"{latency_ms:.2f} ms")
                high_risk_count = len(df_out[df_out["Predicted_Risk_Class"].isin(["High Risk", "Critical Risk"])])
                b3.metric("🚨 High/Critical Risk Patients", f"{high_risk_count}", delta=f"{high_risk_count/len(df_out)*100:.1f}% of cohort", delta_color="inverse")

                # Visual Summary Pie Chart
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.subheader("🥧 Cohort Risk Distribution Breakdown")
                    risk_counts = df_out["Predicted_Risk_Class"].value_counts().reset_index()
                    risk_counts.columns = ["Risk Class", "Count"]
                    cmap = {"Low Risk": "#28a745", "Moderate Risk": "#ffc107", "High Risk": "#fd7e14", "Critical Risk": "#dc3545"}
                    fig_pie = px.pie(risk_counts, values="Count", names="Risk Class", color="Risk Class", color_discrete_map=cmap, hole=0.4)
                    fig_pie.update_layout(height=320)
                    st.plotly_chart(fig_pie, use_container_width=True)

                with c2:
                    st.subheader("📥 Download Clinical Prediction Report")
                    st.write("Click below to export the batch predictions CSV file:")
                    csv_bytes = df_out.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="💾 Download Predictions CSV Report",
                        data=csv_bytes,
                        file_name="cohort_health_risk_predictions.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

                st.subheader("📋 Detailed Predictions Table")
                st.dataframe(df_out, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Batch Processing Error: {str(e)}")
