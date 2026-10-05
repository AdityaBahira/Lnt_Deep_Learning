"""
views/4_Batch_Analytics.py
--------------------------
Batch Screening & Cohort Processing with CSV Report Export.
"""

import os
import io
import time
import pandas as pd
import streamlit as st
from utils import predict_image

st.title("📁 Batch Screening & Cohort Export")
st.markdown("High-throughput clinical screening for multi-image radiological cohorts.")

sample_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sample_data")

st.subheader("1. Ingestion Mode")
mode = st.radio("Choose Batch Source:", ["Standard Test Cohort (Preloaded)", "Upload Multiple Radiographs (Batch)"])

batch_items = []

if mode.startswith("Standard"):
    st.info("Loaded 4 standard clinical cases from system verification dataset.")
    cases = ["normal_case.png", "bacterial_case.png", "viral_case.png", "covid-19_case.png"]
    for c in cases:
        p = os.path.join(sample_dir, c)
        if os.path.exists(p):
            with open(p, "rb") as f:
                batch_items.append({"filename": c, "bytes": f.read()})
else:
    uploaded_files = st.file_uploader("Upload batch images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        for uf in uploaded_files:
            batch_items.append({"filename": uf.name, "bytes": uf.read()})

if batch_items:
    st.write(f"**Total Cases in Batch:** {len(batch_items)}")
    
    if st.button("⚡ Process Full Batch Ingestion", type="primary"):
        results = []
        progress_bar = st.progress(0.0)
        t0 = time.time()
        
        for idx, item in enumerate(batch_items):
            res = predict_image(item["bytes"], base_url=st.session_state.get("backend_url"))
            pred = res.get("prediction", "Unknown")
            conf = res.get("confidence", 0.0)
            lat = res.get("latency_ms", 0.0)
            
            results.append({
                "Sample Identifier": item["filename"],
                "Diagnostic Finding": pred,
                "Model Confidence": f"{conf*100:.1f}%",
                "Inference Latency (ms)": lat,
                "Status": "COMPLETED"
            })
            progress_bar.progress((idx + 1) / len(batch_items))
            
        total_time = (time.time() - t0) * 1000.0
        df = pd.DataFrame(results)
        
        st.success(f"✅ Processed {len(results)} cases in {total_time:.1f} ms ({total_time/len(results):.1f} ms/case avg).")
        st.dataframe(df, use_container_width=True)
        
        # CSV Export
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Clinical Screening Report (CSV)",
            data=csv_data,
            file_name="DeepMed_Vision_Batch_Report.csv",
            mime="text/csv"
        )
else:
    st.warning("Please upload files or select standard cohort.")
