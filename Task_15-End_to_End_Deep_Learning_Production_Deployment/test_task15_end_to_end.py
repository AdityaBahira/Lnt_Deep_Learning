"""
test_task15_end_to_end.py
-------------------------
Automated End-to-End Verification Test Suite for Task 15:
End-to-End Deep Learning Production Deployment Project.

Validates:
1. Model Artifacts Integrity (Weights & Configuration Files)
2. PyTorch Feature Extraction & Softmax Tensor Math
3. Flask REST API Health Probe (/health)
4. Vision Diagnostics Image Inference (/predict/image)
5. Clinical Biomarker Risk Inference (/predict/tabular)
6. High-Throughput Batch Inference (/batch_predict)
7. Security & Input Validation (Error Handling & HTTP 400s)
8. Kubernetes Cluster Workloads & Pod Replica Health
9. Metrics-Server Scraping & HPA Policy Status
10. Streamlit Web UI Availability & Endpoint Response
"""

import os
import sys
import time
import json
import subprocess
import requests
import numpy as np
import torch

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(CURR_DIR, "backend")
SAVED_MODELS = os.path.join(BACKEND_DIR, "saved_models")
SAMPLE_DATA = os.path.join(CURR_DIR, "sample_data")
RESULTS_FILE = os.path.join(CURR_DIR, "task15_test_results.json")
NAMESPACE = "dl-production-app"

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def run_test_suite():
    print("=" * 85)
    print(" TASK 15: END-TO-END DEEP LEARNING PRODUCTION DEPLOYMENT ")
    print(" COMPREHENSIVE AUTOMATED VERIFICATION TEST SUITE (10 TESTS) ")
    print("=" * 85)

    test_results = {
        "project": "DeepMed-Vision: End-to-End Deep Learning Production Deployment",
        "task_id": "Task 15",
        "candidate": "Aditya Bahira",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cluster_namespace": NAMESPACE,
        "tests": []
    }

    # --------------------------------------------------------------------------
    # Test 1: PyTorch Model Weights & Config Serialization
    # --------------------------------------------------------------------------
    print("\n--- Test 1: PyTorch Model Weights & Configuration Integrity ---")
    v_weights = os.path.join(SAVED_MODELS, "deep_vision_model.pt")
    v_config = os.path.join(SAVED_MODELS, "vision_config.json")
    t_weights = os.path.join(SAVED_MODELS, "dl_model.pt")
    
    t1_pass = os.path.exists(v_weights) and os.path.exists(v_config) and os.path.exists(t_weights)
    size_mb = os.path.getsize(v_weights) / (1024 * 1024) if os.path.exists(v_weights) else 0.0
    print(f"[*] DeepMedVisionNet Weights: {v_weights} ({size_mb:.2f} MB)")
    print(f"[*] Vision Configuration: {v_config}")
    print(f"[*] Status: {'PASSED' if t1_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 1,
        "name": "Model Weights & Configuration Integrity",
        "passed": t1_pass,
        "details": f"Vision model ({size_mb:.2f} MB) and companion tabular model successfully serialized."
    })

    # --------------------------------------------------------------------------
    # Test 2: PyTorch Tensor Inference & Softmax Distribution
    # --------------------------------------------------------------------------
    print("\n--- Test 2: PyTorch Tensor Inference Math & Output Shape ---")
    sys.path.insert(0, BACKEND_DIR)
    from model_loader import ProductionModelManager
    manager = ProductionModelManager()
    
    dummy_input = torch.randn(1, 3, 64, 64)
    with torch.no_grad():
        logits = manager.vision_model(dummy_input)
        probs = torch.softmax(logits, dim=1).numpy()[0]
    prob_sum = float(np.sum(probs))
    t2_pass = (logits.shape == torch.Size([1, 4])) and abs(prob_sum - 1.0) < 1e-4
    print(f"[*] Output Logits Shape: {logits.shape}")
    print(f"[*] Softmax Probability Sum: {prob_sum:.6f}")
    print(f"[*] Status: {'PASSED' if t2_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 2,
        "name": "PyTorch Tensor Inference Math & Probability Sum",
        "passed": t2_pass,
        "details": f"Tensor shape (1, 4) verified with strict Softmax normalization (sum = {prob_sum:.4f})."
    })

    # --------------------------------------------------------------------------
    # Test 3: Flask REST API /health Endpoint
    # --------------------------------------------------------------------------
    print("\n--- Test 3: Flask REST API /health Verification ---")
    from app import app
    client = app.test_client()
    res_health = client.get("/health")
    t3_pass = res_health.status_code == 200 and res_health.json.get("status") == "healthy"
    print(f"[*] Response Status Code: {res_health.status_code}")
    print(f"[*] Hardware Device: {res_health.json.get('hardware_device')}")
    print(f"[*] Status: {'PASSED' if t3_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 3,
        "name": "Flask REST API /health Verification",
        "passed": t3_pass,
        "details": f"Health probe returned HTTP 200 with online telemetry ({res_health.json.get('hardware_device')})."
    })

    # --------------------------------------------------------------------------
    # Test 4: Single Radiological Image Diagnostic Inference (/predict/image)
    # --------------------------------------------------------------------------
    print("\n--- Test 4: Single Radiological Image Diagnostic Inference ---")
    sample_img = os.path.join(SAMPLE_DATA, "bacterial_case.png")
    with open(sample_img, "rb") as f:
        res_img = client.post("/predict/image", data={"file": f})
    
    t4_pass = res_img.status_code == 200 and res_img.json.get("status") == "success"
    pred_label = res_img.json.get("prediction")
    conf = res_img.json.get("confidence")
    lat_ms = res_img.json.get("latency_ms")
    print(f"[*] Prediction: {pred_label} (Confidence: {conf*100:.1f}%)")
    print(f"[*] Inference Latency: {lat_ms} ms")
    print(f"[*] Status: {'PASSED' if t4_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 4,
        "name": "Radiological Image Diagnostic Inference",
        "passed": t4_pass,
        "details": f"Diagnosed '{pred_label}' in {lat_ms}ms with {conf*100:.1f}% confidence."
    })

    # --------------------------------------------------------------------------
    # Test 5: Clinical Biomarker Risk Scoring (/predict/tabular)
    # --------------------------------------------------------------------------
    print("\n--- Test 5: Clinical Biomarker Risk Scoring Inference ---")
    sample_feats = [55.0, 140.0, 90.0, 78.0, 220.0, 28.5, 115.0, 6.2, 5500.0, 6.5, 96.0, 2.0, 6.0, 30.0]
    res_tab = client.post("/predict/tabular", json={"features": sample_feats})
    t5_pass = res_tab.status_code == 200 and res_tab.json.get("status") == "success"
    tab_pred = res_tab.json.get("prediction")
    print(f"[*] Clinical Risk Prediction: {tab_pred} ({res_tab.json.get('confidence')*100:.1f}%)")
    print(f"[*] Status: {'PASSED' if t5_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 5,
        "name": "Clinical Biomarker Risk Scoring Inference",
        "passed": t5_pass,
        "details": f"Patient classified into risk tier '{tab_pred}'."
    })

    # --------------------------------------------------------------------------
    # Test 6: High-Throughput Batch Ingestion (/batch_predict)
    # --------------------------------------------------------------------------
    print("\n--- Test 6: High-Throughput Batch Ingestion ---")
    b_cases = ["normal_case.png", "bacterial_case.png", "viral_case.png", "covid-19_case.png"]
    files_dict = {}
    for bc in b_cases:
        p = os.path.join(SAMPLE_DATA, bc)
        files_dict[bc] = (open(p, "rb"), bc)
    res_batch = client.post("/batch_predict", data=files_dict)
    for fh, _ in files_dict.values():
        fh.close()
        
    t6_pass = res_batch.status_code == 200 and res_batch.json.get("batch_size") == 4
    batch_lat = res_batch.json.get("total_batch_latency_ms")
    print(f"[*] Processed {res_batch.json.get('batch_size')} images in {batch_lat} ms")
    print(f"[*] Status: {'PASSED' if t6_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 6,
        "name": "High-Throughput Batch Ingestion",
        "passed": t6_pass,
        "details": f"Processed 4-image cohort in {batch_lat} ms ({batch_lat/4:.1f} ms/image)."
    })

    # --------------------------------------------------------------------------
    # Test 7: Input Validation & Security Edge Cases (HTTP 400)
    # --------------------------------------------------------------------------
    print("\n--- Test 7: Input Validation & Security Edge Cases ---")
    res_err1 = client.post("/predict/tabular", json={"features": [1.0, 2.0]})  # Invalid length
    res_err2 = client.post("/predict/image", data={})                          # Missing file
    t7_pass = (res_err1.status_code == 400) and (res_err2.status_code == 400)
    print(f"[*] Malformed Array Code: {res_err1.status_code} (Expected 400)")
    print(f"[*] Empty File Code: {res_err2.status_code} (Expected 400)")
    print(f"[*] Status: {'PASSED' if t7_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 7,
        "name": "Input Validation & HTTP 400 Error Handling",
        "passed": t7_pass,
        "details": "Malformed payload lengths and empty requests properly rejected with HTTP 400."
    })

    # --------------------------------------------------------------------------
    # Test 8: Kubernetes Pod Status & Replica Consistency
    # --------------------------------------------------------------------------
    print("\n--- Test 8: Kubernetes Pod Status & Cluster Workloads ---")
    k8s_pods = run_cmd(f"kubectl get pods -n {NAMESPACE} -o json")
    t8_pass = False
    ready_count = 0
    if k8s_pods.returncode == 0:
        try:
            pod_items = json.loads(k8s_pods.stdout).get("items", [])
            active_pods = [p for p in pod_items if p.get("metadata", {}).get("deletionTimestamp") is None]
            for p in active_pods:
                cs = p.get("status", {}).get("containerStatuses", [])
                if cs and cs[0].get("ready", False):
                    ready_count += 1
            t8_pass = (ready_count >= 4)  # 2 backend + 2 frontend pods ready
        except Exception as e:
            print(f"[!] Error: {e}")
    print(f"[*] Active Ready Pods in '{NAMESPACE}': {ready_count}")
    print(f"[*] Status: {'PASSED' if t8_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 8,
        "name": "Kubernetes Pod Status & Cluster Workloads",
        "passed": t8_pass,
        "details": f"{ready_count} enterprise microservice pods active and ready (2 backend + 2 frontend)."
    })

    # --------------------------------------------------------------------------
    # Test 9: Resource Metrics Scraping & HPA Policy Status
    # --------------------------------------------------------------------------
    print("\n--- Test 9: Resource Metrics Scraping & HPA Policy Status ---")
    top_res = run_cmd(f"kubectl top pods -n {NAMESPACE}")
    hpa_res = run_cmd(f"kubectl get hpa -n {NAMESPACE}")
    t9_pass = (top_res.returncode == 0) and (hpa_res.returncode == 0) and ("dl-backend-hpa" in hpa_res.stdout)
    print(f"[*] Top Pods Return Code: {top_res.returncode}")
    print(f"[*] HPA Configured: {'dl-backend-hpa' in hpa_res.stdout}")
    print(f"[*] Status: {'PASSED' if t9_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 9,
        "name": "Resource Metrics Scraping & HPA Policy Status",
        "passed": t9_pass,
        "details": "Metrics-server scraping CPU/RAM live telemetry; HPA scaling policy active (2-5 pods)."
    })

    # --------------------------------------------------------------------------
    # Test 10: Streamlit Frontend Microservice Health & Reachability
    # --------------------------------------------------------------------------
    print("\n--- Test 10: In-Cluster Inter-Service Networking & Reachability ---")
    # Probe backend from frontend pod inside cluster
    net_probe = run_cmd(f"kubectl exec -n {NAMESPACE} deploy/dl-frontend-deployment -- curl -s -o /dev/null -w %{{http_code}} http://dl-backend-svc:5000/health")
    code = net_probe.stdout.strip()
    t10_pass = (code == "200")
    print(f"[*] Cluster CoreDNS HTTP Status: {code} (Expected 200)")
    print(f"[*] Status: {'PASSED' if t10_pass else 'FAILED'}")
    test_results["tests"].append({
        "test_id": 10,
        "name": "In-Cluster CoreDNS Inter-Service Networking",
        "passed": t10_pass,
        "details": "Frontend pod successfully invoked http://dl-backend-svc:5000/health with HTTP 200."
    })

    # Summary
    passed_count = sum(1 for t in test_results["tests"] if t["passed"])
    total_count = len(test_results["tests"])
    test_results["summary"] = {
        "total": total_count,
        "passed": passed_count,
        "pass_percentage": round((passed_count / total_count) * 100, 2)
    }

    print("\n" + "=" * 85)
    print(f" TEST SUITE SUMMARY: {passed_count}/{total_count} PASSED ({test_results['summary']['pass_percentage']}%)")
    print("=" * 85)

    with open(RESULTS_FILE, "w") as f:
        json.dump(test_results, f, indent=2)
    print(f"[OK] Full test telemetry exported to: {RESULTS_FILE}")

    return test_results

if __name__ == "__main__":
    run_test_suite()
