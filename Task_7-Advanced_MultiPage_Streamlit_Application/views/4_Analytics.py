"""
3_Analytics.py
--------------
Page 3: Comprehensive Model Analytics & Performance Dashboard based on Backend/health_activity_data.csv.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import classification_report, roc_curve, auc

from utils import (
    ModelConnector,
    compute_dataset_analytics,
    RISK_CLASSES,
    FEATURE_LABELS
)

st.title("📊 Model Performance & Analytics Dashboard")
st.write("Comprehensive evaluation metrics computed directly on **`Backend/health_activity_data.csv`**.")

st.divider()

@st.cache_resource
def get_connector():
    return ModelConnector(api_url="http://127.0.0.1:5000")

connector = get_connector()

@st.cache_data
def get_analytics():
    return compute_dataset_analytics(connector)

with st.spinner("🔄 Computing full dataset evaluation analytics on `health_activity_data.csv`..."):
    try:
        analytics = get_analytics()
        df = analytics["df"]
        y_true = analytics["y_true"]
        y_pred = analytics["y_pred"]
        y_prob = analytics["y_prob"]
        cm = analytics["confusion_matrix"]
        acc = analytics["accuracy"]

        # Classification Metrics Cards
        report = classification_report(y_true, y_pred, target_names=RISK_CLASSES, output_dict=True)
        macro_f1 = report["macro avg"]["f1-score"]
        macro_prec = report["macro avg"]["precision"]
        macro_rec = report["macro avg"]["recall"]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🎯 Overall Accuracy", f"{acc*100:.2f}%")
        m2.metric("⚡ Macro F1-Score", f"{macro_f1*100:.2f}%")
        m3.metric("🔍 Macro Precision", f"{macro_prec*100:.2f}%")
        m4.metric("📊 Macro Recall", f"{macro_rec*100:.2f}%")

        st.divider()

        # Row 1: Confusion Matrix & ROC Curves
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("🧩 Confusion Matrix Heatmap")
            fig_cm = px.imshow(
                cm,
                x=RISK_CLASSES,
                y=RISK_CLASSES,
                color_continuous_scale="Reds",
                text_auto=True,
                title="Model Confusion Matrix"
            )
            fig_cm.update_layout(xaxis_title="Predicted Risk Class", yaxis_title="Actual Ground Truth Risk", height=380)
            st.plotly_chart(fig_cm, use_container_width=True)

        with c2:
            st.subheader("📈 Multi-Class ROC Curves")
            fig_roc = go.Figure()
            colors = ["#28a745", "#ffc107", "#fd7e14", "#dc3545"]
            
            # One-vs-Rest ROC
            for i, cls_name in enumerate(RISK_CLASSES):
                binary_true = (np.array(y_true) == i).astype(int)
                fpr, tpr, _ = roc_curve(binary_true, y_prob[:, i])
                roc_auc = auc(fpr, tpr)
                fig_roc.add_trace(go.Scatter(
                    x=fpr, y=tpr, mode='lines', name=f"{cls_name} (AUC = {roc_auc:.3f})", line=dict(color=colors[i], width=2)
                ))
            
            fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines', name='Random Classifier', line=dict(color='gray', dash='dash')))
            fig_roc.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", height=380, legend=dict(x=0.5, y=0.1))
            st.plotly_chart(fig_roc, use_container_width=True)

        st.divider()

        # Row 2: Dataset Distributions & Risk Sensitivity
        st.subheader("🔬 Feature Distributions & Risk Sensitivity")
        feat_choice = st.selectbox("Select Feature to Inspect:", list(FEATURE_LABELS.keys()), index=0)
        
        # Map feature column in CSV
        col_map = {
            "age": "Age", "height_cm": "Height_cm", "weight_kg": "Weight_kg", "bmi": "BMI",
            "daily_steps": "Daily_Steps", "calories_intake": "Calories_Intake", "hours_of_sleep": "Hours_of_Sleep",
            "heart_rate": "Heart_Rate", "exercise_hours_per_week": "Exercise_Hours_per_Week",
            "alcohol_consumption_per_week": "Alcohol_Consumption_per_Week"
        }
        
        csv_col = col_map.get(feat_choice, "Age")
        if csv_col in df.columns:
            f1, f2 = st.columns(2)
            with f1:
                fig_hist = px.histogram(df, x=csv_col, title=f"Distribution of {FEATURE_LABELS[feat_choice]}", color_discrete_sequence=["#1E3A8A"])
                fig_hist.update_layout(height=320)
                st.plotly_chart(fig_hist, use_container_width=True)
            with f2:
                fig_box = px.box(df, y=csv_col, title=f"Boxplot Analysis of {FEATURE_LABELS[feat_choice]}", color_discrete_sequence=["#2563EB"])
                fig_box.update_layout(height=320)
                st.plotly_chart(fig_box, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error computing analytics: {str(e)}")
