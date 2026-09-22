"""
1_Overview.py
-------------
Page 1: Executive Overview, Dataset Specifications & PyTorch Model Architecture Inspector.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_dataset, FEATURE_LABELS, RISK_CLASSES

st.markdown("## 🏠 Executive Overview & Model Architecture")
st.markdown("Welcome to **Task 7: Advanced Multi-Page Clinical Decision Platform**. This application serves pre-trained PyTorch Deep Neural Networks for clinical health risk assessment.")

st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Dataset Specifications & Features")
    st.write("The system processes **14 physiological and lifestyle features** ingested directly from the dataset (`Backend/health_activity_data.csv`).")
    
    try:
        df = load_dataset()
        st.success(f"✅ Ingested **`health_activity_data.csv`** successfully ({len(df):,} total patient records).")
        
        with st.expander("🔍 View Raw Dataset Sample"):
            st.dataframe(df.head(10), use_container_width=True)

        st.markdown("#### Feature Summary Table")
        feat_df = pd.DataFrame([
            {"Feature Key": k, "Label": v} for k, v in FEATURE_LABELS.items()
        ])
        st.dataframe(feat_df, use_container_width=True, height=250)

    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")

with col2:
    st.subheader("🧠 PyTorch Neural Network Architecture")
    st.write("The underlying model **`DeepHealthRiskNet`** is a 3-Layer Artificial Neural Network trained in PyTorch.")

    # Architecture Visual Box
    st.info("""
    **`DeepHealthRiskNet` Layer Specification:**
    - **Input Layer**: 14 Nodes (Standard Scaled Feature Vector)
    - **Hidden Layer 1**: Linear(14 → 64) → BatchNorm1d(64) → ReLU() → Dropout(p=0.2)
    - **Hidden Layer 2**: Linear(64 → 32) → BatchNorm1d(32) → ReLU() → Dropout(p=0.2)
    - **Output Layer**: Linear(32 → 4) → Softmax Activation
    - **Target Output Classes (4)**: Low Risk, Moderate Risk, High Risk, Critical Risk
    """)

    st.markdown("#### Clinical Target Class Categories")
    for cls in RISK_CLASSES:
        if cls == "Low Risk":
            st.markdown("- 🟢 **Low Risk**: Optimal physiological metrics and low cardiovascular risk.")
        elif cls == "Moderate Risk":
            st.markdown("- 🟡 **Moderate Risk**: Mild risk factors requiring routine lifestyle adjustments.")
        elif cls == "High Risk":
            st.markdown("- 🟠 **High Risk**: Elevated blood pressure, BMI, or lifestyle risks requiring medical evaluation.")
        elif cls == "Critical Risk":
            st.markdown("- 🔴 **Critical Risk**: Severe health risk parameters requiring immediate clinical checkup.")

st.markdown("---")
st.markdown("### 📈 Dataset Distribution Quick Overview")
try:
    df = load_dataset()
    fig = px.histogram(df, x="Age", color="Gender" if "Gender" in df.columns else None, 
                       title="Age Distribution Across Patient Dataset",
                       barmode="overlay", color_discrete_sequence=["#1E3A8A", "#EF4444"])
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.info("Dataset visualization ready.")
