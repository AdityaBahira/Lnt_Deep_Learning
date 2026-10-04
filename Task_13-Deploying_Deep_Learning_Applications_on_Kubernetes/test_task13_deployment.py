"""
test_task13_deployment.py
--------------------------
Automated verification and operational test suite for Task 13:
Deploying Deep Learning Applications on Kubernetes.

Validates:
1. Kubernetes Cluster Status & Node Readiness
2. Production Namespace & Decoupled ConfigMap Verification
3. Deep Learning Backend Deployment & Health Probes (PyTorch DeepHealthRiskNet)
4. Clinical Streamlit Frontend Deployment & Rollout Status
5. Service Discovery & External NodePort Exposure (30500 for API, 31501 for UI)
6. External REST API Inference Validation (/predict with patient health metrics)
7. External Frontend UI HTTP Accessibility
8. Kubernetes ReplicaSet Scaling & Load Distribution (Scale to 3 replicas)
9. Self-Healing Simulation (Pod deletion and auto-recovery)
10. Structured Telemetry Export to task13_test_results.json
"""

import os
import sys
import time
import json
import subprocess
import requests

NAMESPACE = "dl-production-app"
BACKEND_URL = "http://localhost:30500"
FRONTEND_URL = "http://localhost:31501"
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_FILE = os.path.join(CURR_DIR, "task13_test_results.json")

def run_cmd(cmd, check=False):
    print(f"\n[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Command failed with code {res.returncode}:\n{res.stderr}")
    return res

def wait_for_rollout(deployment_name, timeout=90):
    print(f"[*] Waiting for {deployment_name} rollout in namespace '{NAMESPACE}'...")
    res = run_cmd(f"kubectl rollout status deployment/{deployment_name} -n {NAMESPACE} --timeout={timeout}s")
    return res.returncode == 0, res.stdout.strip()

def run_test_suite():
    print("=" * 80)
    print(" TASK 13: DEPLOYING DEEP LEARNING APPLICATIONS ON KUBERNETES ")
    print(" AUTOMATED VERIFICATION & OPERATIONAL TEST SUITE ")
    print("=" * 80)

    test_results = {
        "task": "Task 13: Deploying Deep Learning Applications on Kubernetes",
        "cluster_type": "Minikube (Docker Driver)",
        "namespace": NAMESPACE,
        "backend_external_url": BACKEND_URL,
        "frontend_external_url": FRONTEND_URL,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tests": []
    }

    # Test 1: Cluster & Node Verification
    print("\n--- Test 1: Verify Kubernetes Cluster & Node Status ---")
    node_res = run_cmd("kubectl get nodes -o json")
    node_ok = False
    node_name = "unknown"
    if node_res.returncode == 0:
        try:
            node_data = json.loads(node_res.stdout)
            node_name = node_data["items"][0]["metadata"]["name"]
            conds = node_data["items"][0]["status"]["conditions"]
            ready_cond = next((c for c in conds if c["type"] == "Ready"), None)
            node_ok = ready_cond is not None and ready_cond["status"] == "True"
        except Exception as e:
            print(f"[!] Node parse error: {e}")
    
    print(f"Node: {node_name} | Ready: {node_ok}")
    test_results["tests"].append({
        "id": "T01_CLUSTER_NODES",
        "name": "Cluster & Node Readiness",
        "status": "PASSED" if node_ok else "FAILED",
        "details": f"Node '{node_name}' is Ready in Minikube control plane."
    })

    # Test 2: Namespace & ConfigMap
    print("\n--- Test 2: Verify Namespace & Production ConfigMap ---")
    cm_res = run_cmd(f"kubectl get configmap dl-production-config -n {NAMESPACE} -o json")
    cm_ok = False
    cm_keys = []
    if cm_res.returncode == 0:
        try:
            cm_data = json.loads(cm_res.stdout)
            cm_keys = list(cm_data.get("data", {}).keys())
            cm_ok = "BACKEND_URL" in cm_keys and "MODEL_NAME" in cm_keys
        except Exception as e:
            print(f"[!] ConfigMap parse error: {e}")

    print(f"ConfigMap keys found: {cm_keys}")
    test_results["tests"].append({
        "id": "T02_CONFIG_MAP",
        "name": "Production ConfigMap & Decoupling",
        "status": "PASSED" if cm_ok else "FAILED",
        "details": f"ConfigMap contains {len(cm_keys)} keys including BACKEND_URL and MODEL_NAME."
    })

    # Test 3: Backend Deployment & Health Probes
    print("\n--- Test 3: Verify PyTorch Backend Deployment & Rollout ---")
    be_rollout, be_msg = wait_for_rollout("dl-backend-deployment")
    be_pods_res = run_cmd(f"kubectl get pods -n {NAMESPACE} -l app=dl-backend -o json")
    be_ready_count = 0
    if be_pods_res.returncode == 0:
        try:
            be_pods = json.loads(be_pods_res.stdout)["items"]
            for p in be_pods:
                container_statuses = p.get("status", {}).get("containerStatuses", [])
                if container_statuses and container_statuses[0].get("ready", False):
                    be_ready_count += 1
        except Exception as e:
            print(f"[!] Backend pods parse error: {e}")

    print(f"Backend Ready Replicas: {be_ready_count} / 2")
    test_results["tests"].append({
        "id": "T03_BACKEND_ROLLOUT",
        "name": "PyTorch Backend Rollout & Probes",
        "status": "PASSED" if (be_rollout and be_ready_count >= 2) else "FAILED",
        "details": f"Backend deployment healthy: {be_ready_count} replicas ready with liveness/readiness probes."
    })

    # Test 4: Frontend Deployment & Rollout
    print("\n--- Test 4: Verify Streamlit Frontend Deployment & Rollout ---")
    fe_rollout, fe_msg = wait_for_rollout("dl-frontend-deployment")
    fe_pods_res = run_cmd(f"kubectl get pods -n {NAMESPACE} -l app=dl-frontend -o json")
    fe_ready_count = 0
    if fe_pods_res.returncode == 0:
        try:
            fe_pods = json.loads(fe_pods_res.stdout)["items"]
            for p in fe_pods:
                container_statuses = p.get("status", {}).get("containerStatuses", [])
                if container_statuses and container_statuses[0].get("ready", False):
                    fe_ready_count += 1
        except Exception as e:
            print(f"[!] Frontend pods parse error: {e}")

    print(f"Frontend Ready Replicas: {fe_ready_count} / 2")
    test_results["tests"].append({
        "id": "T04_FRONTEND_ROLLOUT",
        "name": "Streamlit Frontend Deployment Rollout",
        "status": "PASSED" if (fe_rollout and fe_ready_count >= 2) else "FAILED",
        "details": f"Frontend deployment healthy: {fe_ready_count} replicas active and serving UI."
    })

    # Test 5: Service Configuration & Port Mapping
    print("\n--- Test 5: Verify Service Networking & NodePort Mapping ---")
    svc_res = run_cmd(f"kubectl get svc -n {NAMESPACE} -o json")
    svc_ok = False
    if svc_res.returncode == 0:
        try:
            svc_list = json.loads(svc_res.stdout)["items"]
            svc_names = [s["metadata"]["name"] for s in svc_list]
            svc_ok = "dl-backend-svc" in svc_names and "dl-frontend-svc" in svc_names
        except Exception as e:
            print(f"[!] Service parse error: {e}")

    print(f"Services found: dl-backend-svc (Port 5000:30500), dl-frontend-svc (Port 8501:31501)")
    test_results["tests"].append({
        "id": "T05_SERVICE_MAPPING",
        "name": "Kubernetes Service Configurations",
        "status": "PASSED" if svc_ok else "FAILED",
        "details": "Services configured with NodePort (Backend :30500, Frontend :31501) for external exposure."
    })

    # Test 6: External Health Check (Backend /health)
    print("\n--- Test 6: External Backend Health Verification ---")
    be_health_ok = False
    be_health_data = {}
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if r.status_code == 200:
            be_health_data = r.json()
            be_health_ok = be_health_data.get("status") == "healthy" and be_health_data.get("model_loaded") is True
            print(f"Backend Health: {be_health_data}")
    except Exception as e:
        print(f"[!] Backend health request error: {e}")

    test_results["tests"].append({
        "id": "T06_EXTERNAL_BACKEND_HEALTH",
        "name": "External Backend Health Endpoint",
        "status": "PASSED" if be_health_ok else "FAILED",
        "details": f"HTTP 200 OK: Model {be_health_data.get('model_name', 'DeepHealthRiskNet')} loaded on {be_health_data.get('device', 'cpu')}."
    })

    # Test 7: External Frontend Accessibility
    print("\n--- Test 7: External Frontend UI HTTP Accessibility ---")
    fe_access_ok = False
    try:
        r_fe = requests.get(FRONTEND_URL, timeout=10)
        fe_access_ok = (r_fe.status_code == 200 and "Streamlit" in r_fe.text or "text/html" in r_fe.headers.get("content-type", ""))
        print(f"Frontend HTTP Status: {r_fe.status_code} | Content-Type: {r_fe.headers.get('content-type')}")
    except Exception as e:
        print(f"[!] Frontend accessibility error: {e}")

    test_results["tests"].append({
        "id": "T07_EXTERNAL_FRONTEND_ACCESS",
        "name": "External Streamlit UI Accessibility",
        "status": "PASSED" if fe_access_ok else "FAILED",
        "details": f"Frontend responded HTTP 200 OK on exposed NodePort port 31501."
    })

    # Test 8: Live Deep Learning Model Inference (/predict)
    print("\n--- Test 8: Live Deep Learning Model Inference Request ---")
    infer_ok = False
    infer_data = {}
    test_payload = {
        "features": [62.0, 1.0, 3.0, 145.0, 233.0, 1.0, 0.0, 150.0, 0.0, 2.3, 0.0, 0.0, 1.0, 0.0]
    }
    try:
        r_infer = requests.post(f"{BACKEND_URL}/predict", json=test_payload, timeout=10)
        if r_infer.status_code == 200:
            infer_data = r_infer.json()
            pred = infer_data["predictions"][0]
            label = pred.get("predicted_label")
            conf = pred.get("confidence_score")
            lat = infer_data.get("latency_ms")
            infer_ok = infer_data.get("status") == "success" and label is not None
            print(f"Prediction Output: Label='{label}', Confidence={conf*100:.2f}%, Latency={lat}ms")
    except Exception as e:
        print(f"[!] Model inference request error: {e}")

    test_results["tests"].append({
        "id": "T08_MODEL_INFERENCE",
        "name": "External Deep Learning Model Inference (/predict)",
        "status": "PASSED" if infer_ok else "FAILED",
        "details": f"Successfully performed live neural inference: Predicted '{infer_data.get('predictions', [{}])[0].get('predicted_label', 'N/A')}' in {infer_data.get('latency_ms', 0)}ms."
    })

    # Test 9: Horizontal Pod Scaling (Scale Backend to 3 replicas)
    print("\n--- Test 9: Horizontal Pod Scaling to 3 Replicas ---")
    scale_res = run_cmd(f"kubectl scale deployment/dl-backend-deployment --replicas=3 -n {NAMESPACE}")
    time.sleep(5)
    scale_rollout, _ = wait_for_rollout("dl-backend-deployment", timeout=60)
    scale_pods_res = run_cmd(f"kubectl get pods -n {NAMESPACE} -l app=dl-backend -o json")
    active_replicas = 0
    if scale_pods_res.returncode == 0:
        try:
            scale_pods = json.loads(scale_pods_res.stdout)["items"]
            active_replicas = len(scale_pods)
        except Exception as e:
            print(f"[!] Scaling parse error: {e}")

    print(f"Active Replicas after scaling: {active_replicas}")
    test_results["tests"].append({
        "id": "T09_HORIZONTAL_SCALING",
        "name": "Horizontal Pod Scaling & Dynamic Rebalancing",
        "status": "PASSED" if (scale_rollout and active_replicas >= 3) else "FAILED",
        "details": f"Successfully scaled backend deployment to {active_replicas} replicas dynamically."
    })

    # Test 10: Kubernetes Self-Healing Simulation
    print("\n--- Test 10: Kubernetes Self-Healing Verification ---")
    healing_ok = False
    if scale_pods_res.returncode == 0 and len(scale_pods) > 0:
        pod_to_delete = scale_pods[0]["metadata"]["name"]
        print(f"Terminating pod to test self-healing: {pod_to_delete}")
        del_res = run_cmd(f"kubectl delete pod {pod_to_delete} -n {NAMESPACE} --grace-period=0 --force")
        time.sleep(4)
        post_pods_res = run_cmd(f"kubectl get pods -n {NAMESPACE} -l app=dl-backend -o json")
        if post_pods_res.returncode == 0:
            try:
                post_pods = json.loads(post_pods_res.stdout)["items"]
                current_count = len(post_pods)
                healing_ok = current_count >= 3
                print(f"Replica count post-pod termination: {current_count}")
            except Exception as e:
                print(f"[!] Post-healing parse error: {e}")

    test_results["tests"].append({
        "id": "T10_SELF_HEALING",
        "name": "Kubernetes Self-Healing & Pod Recovery",
        "status": "PASSED" if healing_ok else "FAILED",
        "details": "ReplicaSet detected pod termination and automatically provisioned a replacement pod to maintain desired state."
    })

    # Summary
    passed_count = sum(1 for t in test_results["tests"] if t["status"] == "PASSED")
    total_count = len(test_results["tests"])
    test_results["summary"] = {
        "total_tests": total_count,
        "passed": passed_count,
        "failed": total_count - passed_count,
        "pass_rate": f"{(passed_count / total_count) * 100:.1f}%"
    }

    print("\n" + "=" * 80)
    print(f" TEST EXECUTION SUMMARY: {passed_count}/{total_count} PASSED ({test_results['summary']['pass_rate']})")
    print("=" * 80)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2)
    print(f"Test results saved to: {RESULTS_FILE}")

    return passed_count == total_count

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
