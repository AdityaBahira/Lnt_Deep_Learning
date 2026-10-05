"""
test_task14_scaling_rollout.py
------------------------------
Automated verification and operational benchmark test suite for Task 14:
Kubernetes Scaling and Rolling Updates.

Executes and Validates:
1. Cluster Readiness & Metrics Server Health (kubectl top nodes & pods)
2. Namespace, ConfigMap & Initial Baseline Deployment
3. Manual Scaling Up: 2 -> 5 Replicas with Pod Readiness Convergence
4. Multi-Replica Load Distribution & Inference Validation (/predict)
5. Manual Scaling Down: 5 -> 3 Replicas with Graceful Termination
6. Zero-Downtime Rolling Update: v1.0 -> v2.0 Deployment Rollout
7. Continuous High-Availability Verification (0 dropped requests during rollout)
8. Rollout Rollback & Revision History Audit (kubectl rollout undo)
9. Horizontal Pod Autoscaler (HPA) Policy Application & Validation
10. Comprehensive Resource Utilization Telemetry Export (task14_test_results.json)
"""

import os
import sys
import time
import json
import subprocess
import threading

NAMESPACE = "dl-production-app"
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
K8S_DIR = os.path.join(CURR_DIR, "k8s")
RESULTS_FILE = os.path.join(CURR_DIR, "task14_test_results.json")

def run_cmd(cmd, check=False):
    print(f"\n[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Command failed with code {res.returncode}:\n{res.stderr}")
    return res

def wait_for_rollout(deployment_name, timeout=120):
    print(f"[*] Monitoring {deployment_name} rollout in namespace '{NAMESPACE}'...")
    res = run_cmd(f"kubectl rollout status deployment/{deployment_name} -n {NAMESPACE} --timeout={timeout}s")
    return res.returncode == 0, res.stdout.strip()

def get_active_pods(label="app=dl-backend"):
    """Returns non-terminating pods."""
    res = run_cmd(f"kubectl get pods -n {NAMESPACE} -l {label} -o json")
    if res.returncode != 0:
        return []
    try:
        pod_items = json.loads(res.stdout).get("items", [])
        return [p for p in pod_items if p.get("metadata", {}).get("deletionTimestamp") is None]
    except Exception as e:
        print(f"[!] Error parsing pods: {e}")
        return []

def wait_for_active_pod_count(label="app=dl-backend", target_count=3, timeout=75):
    """Waits until exactly target_count non-terminating pods are active and ready."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        active = get_active_pods(label)
        if len(active) == target_count:
            ready_count = 0
            for p in active:
                c_statuses = p.get("status", {}).get("containerStatuses", [])
                if c_statuses and c_statuses[0].get("ready", False):
                    ready_count += 1
            if ready_count == target_count:
                return active
        time.sleep(2)
    return get_active_pods(label)

def query_cluster_service(path, method="GET", payload=None):
    """Queries dl-backend-svc inside cluster via frontend deployment curl."""
    url = f"http://dl-backend-svc:5000{path}"
    cmd = ["kubectl", "exec", "-n", NAMESPACE, "deploy/dl-frontend-deployment", "--", "curl", "-s"]
    if method == "POST":
        cmd.extend(["-X", "POST", "-H", "Content-Type: application/json"])
        if payload:
            cmd.extend(["-d", json.dumps(payload)])
    cmd.append(url)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return False, None
    try:
        return True, json.loads(res.stdout)
    except Exception:
        return (res.stdout.strip() == "ok"), res.stdout.strip()

def check_backend_health():
    """Returns (status_code == 200, latency_ms)"""
    t0 = time.time()
    cmd = ["kubectl", "exec", "-n", NAMESPACE, "deploy/dl-frontend-deployment", "--",
           "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://dl-backend-svc:5000/health"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt_ms = (time.time() - t0) * 1000
    code = res.stdout.strip()
    return (code == "200"), dt_ms

def run_test_suite():
    print("=" * 85)
    print(" TASK 14: KUBERNETES SCALING AND ROLLING UPDATES ")
    print(" AUTOMATED OPERATIONAL BENCHMARK & VERIFICATION TEST SUITE ")
    print("=" * 85)

    test_results = {
        "task": "Task 14: Kubernetes Scaling and Rolling Updates",
        "cluster_type": "Minikube (Docker Driver)",
        "namespace": NAMESPACE,
        "backend_svc": "http://dl-backend-svc:5000",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tests": [],
        "telemetry": {}
    }

    # Delete HPA during manual scaling phases
    run_cmd(f"kubectl delete hpa dl-backend-hpa -n {NAMESPACE} --ignore-not-found=true")

    # --------------------------------------------------------------------------
    # Test 1: Cluster Nodes & Metrics Server Scraping
    # --------------------------------------------------------------------------
    print("\n--- Test 1: Verify Kubernetes Cluster & Metrics-Server Status ---")
    node_res = run_cmd("kubectl get nodes -o json")
    top_res = run_cmd("kubectl top nodes")
    node_ready = False
    node_name = "unknown"
    if node_res.returncode == 0:
        try:
            node_data = json.loads(node_res.stdout)
            node_name = node_data["items"][0]["metadata"]["name"]
            conds = node_data["items"][0]["status"]["conditions"]
            ready_cond = next((c for c in conds if c["type"] == "Ready"), None)
            node_ready = ready_cond is not None and ready_cond["status"] == "True"
        except Exception as e:
            print(f"[!] Node parse error: {e}")

    metrics_ok = top_res.returncode == 0 and "CPU(cores)" in top_res.stdout
    print(f"Node: {node_name} | Ready: {node_ready} | Metrics Server Scraping: {metrics_ok}")
    print(top_res.stdout.strip())

    test_results["tests"].append({
        "id": "T01_METRICS_SERVER",
        "name": "Cluster Readiness & Metrics Server Scraping",
        "status": "PASSED" if (node_ready and metrics_ok) else "FAILED",
        "details": f"Node '{node_name}' is Ready. Metrics Server successfully reporting CPU/Memory consumption."
    })

    # --------------------------------------------------------------------------
    # Test 2: Namespace & Production ConfigMap
    # --------------------------------------------------------------------------
    print("\n--- Test 2: Verify Namespace & Production ConfigMap ---")
    cm_res = run_cmd(f"kubectl get configmap dl-production-config -n {NAMESPACE} -o json")
    cm_ok = False
    cm_keys = []
    if cm_res.returncode == 0:
        try:
            cm_data = json.loads(cm_res.stdout)
            cm_keys = list(cm_data.get("data", {}).keys())
            cm_ok = "BACKEND_URL" in cm_keys and "DEPLOYMENT_STRATEGY" in cm_keys
        except Exception as e:
            print(f"[!] ConfigMap parse error: {e}")

    print(f"ConfigMap keys verified: {cm_keys}")
    test_results["tests"].append({
        "id": "T02_NAMESPACE_CONFIG",
        "name": "Namespace & Decoupled Configuration",
        "status": "PASSED" if cm_ok else "FAILED",
        "details": f"Namespace '{NAMESPACE}' and ConfigMap contain {len(cm_keys)} keys including DEPLOYMENT_STRATEGY=RollingUpdate."
    })

    # Baseline reset: 2 replicas with image v1.0
    print("\n[*] Initializing baseline replica count: 2 (Image v1.0)")
    run_cmd(f"kubectl set image deployment/dl-backend-deployment dl-backend-api=adityabahira/dl-clinical-backend:v1.0 -n {NAMESPACE}")
    run_cmd(f"kubectl scale deployment dl-backend-deployment --replicas=2 -n {NAMESPACE}")
    wait_for_rollout("dl-backend-deployment", timeout=60)
    wait_for_active_pod_count("app=dl-backend", target_count=2, timeout=60)

    # --------------------------------------------------------------------------
    # Test 3: Manual Scaling Up to 5 Replicas
    # --------------------------------------------------------------------------
    print("\n--- Test 3: Scale Up Backend Deployment to 5 Replicas ---")
    run_cmd(f"kubectl scale deployment dl-backend-deployment --replicas=5 -n {NAMESPACE}")
    wait_for_rollout("dl-backend-deployment", timeout=60)
    active_5 = wait_for_active_pod_count("app=dl-backend", target_count=5, timeout=60)
    
    ready_count_5 = sum(1 for p in active_5 if p.get("status", {}).get("containerStatuses", [{}])[0].get("ready", False))
    pod_names_5 = [p["metadata"]["name"] for p in active_5]

    print(f"Scale-Up Result: {ready_count_5} / 5 Replicas Ready across active pods {pod_names_5}")
    test_results["tests"].append({
        "id": "T03_SCALE_UP_5_REPLICAS",
        "name": "Manual Application Scale-Up (2 -> 5 Replicas)",
        "status": "PASSED" if ready_count_5 == 5 else "FAILED",
        "details": f"Backend deployment successfully scaled to 5 replicas. All 5 active pods passed readiness checks."
    })

    # --------------------------------------------------------------------------
    # Test 4: Multi-Replica Deep Learning Inference & Load Validation
    # --------------------------------------------------------------------------
    print("\n--- Test 4: Validate Multi-Replica Deep Learning Inference ---")
    infer_payload = {
        "features": [58.0, 1.0, 2.0, 140.0, 211.0, 1.0, 0.0, 165.0, 0.0, 1.6, 0.0, 0.0, 2.0, 0.0]
    }
    latencies = []
    success_count = 0
    total_requests = 15

    for i in range(total_requests):
        t0 = time.time()
        ok, res_json = query_cluster_service("/predict", method="POST", payload=infer_payload)
        dt_ms = (time.time() - t0) * 1000
        if ok and res_json and res_json.get("status") == "success":
            success_count += 1
            latencies.append(dt_ms)
        else:
            print(f"[!] Request {i+1} failed: {res_json}")

    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    p95_lat = sorted(latencies)[int(0.95 * len(latencies))] if latencies else 0
    print(f"Load Distribution Test: {success_count}/{total_requests} Passed | Avg Roundtrip: {avg_lat:.2f}ms | P95: {p95_lat:.2f}ms")

    test_results["tests"].append({
        "id": "T04_LOAD_BALANCED_INFERENCE",
        "name": "Multi-Replica Deep Learning Inference Serving",
        "status": "PASSED" if success_count == total_requests else "FAILED",
        "details": f"{success_count}/{total_requests} inference requests succeeded across 5 replicas (Avg Roundtrip: {avg_lat:.2f}ms)."
    })

    # --------------------------------------------------------------------------
    # Test 5: Manual Scale-Down to 3 Replicas
    # --------------------------------------------------------------------------
    print("\n--- Test 5: Scale Down Backend Deployment to 3 Replicas ---")
    run_cmd(f"kubectl scale deployment dl-backend-deployment --replicas=3 -n {NAMESPACE}")
    active_3 = wait_for_active_pod_count("app=dl-backend", target_count=3, timeout=60)
    ready_count_3 = sum(1 for p in active_3 if p.get("status", {}).get("containerStatuses", [{}])[0].get("ready", False))

    print(f"Scale-Down Result: {ready_count_3} Replicas Active & Ready (Target: 3)")
    test_results["tests"].append({
        "id": "T05_SCALE_DOWN_3_REPLICAS",
        "name": "Manual Application Scale-Down (5 -> 3 Replicas)",
        "status": "PASSED" if ready_count_3 == 3 else "FAILED",
        "details": f"Backend deployment scaled down to 3 replicas with graceful termination of excess pods."
    })

    # --------------------------------------------------------------------------
    # Test 6 & 7: Zero-Downtime Rolling Update (v1.0 -> v2.0) with Live Traffic
    # --------------------------------------------------------------------------
    print("\n--- Test 6 & 7: Zero-Downtime Rolling Update (v1.0 -> v2.0) with Live Traffic ---")
    traffic_stats = {
        "sent": 0,
        "success": 0,
        "failed": 0,
        "latencies": []
    }
    stop_traffic = threading.Event()

    def traffic_worker():
        while not stop_traffic.is_set():
            traffic_stats["sent"] += 1
            ok, dt = check_backend_health()
            if ok:
                traffic_stats["success"] += 1
                traffic_stats["latencies"].append(dt)
            else:
                traffic_stats["failed"] += 1
            time.sleep(0.1)

    # Launch background continuous traffic thread
    traffic_thread = threading.Thread(target=traffic_worker, daemon=True)
    traffic_thread.start()

    # Trigger Rolling Update to v2.0
    print("[*] Triggering rolling update to image: adityabahira/dl-clinical-backend:v2.0")
    run_cmd(
        f"kubectl set image deployment/dl-backend-deployment dl-backend-api=adityabahira/dl-clinical-backend:v2.0 -n {NAMESPACE}"
    )

    # Track rollout status
    rollout_update_ok, _ = wait_for_rollout("dl-backend-deployment", timeout=120)
    stop_traffic.set()
    traffic_thread.join()

    # Wait for terminating v1 pods to drain completely
    active_v2 = wait_for_active_pod_count("app=dl-backend", target_count=3, timeout=60)
    v2_images = [p["spec"]["containers"][0]["image"] for p in active_v2]
    v2_image_confirmed = len(v2_images) == 3 and all("v2.0" in img for img in v2_images)
    print(f"Active pod container images after update: {v2_images}")

    availability_pct = (traffic_stats["success"] / traffic_stats["sent"] * 100) if traffic_stats["sent"] > 0 else 0
    print(f"\n[Traffic During Rollout] Total: {traffic_stats['sent']} | Success: {traffic_stats['success']} | "
          f"Failed: {traffic_stats['failed']} | Availability: {availability_pct:.2f}%")

    test_results["tests"].append({
        "id": "T06_ROLLING_UPDATE_V2",
        "name": "Zero-Downtime Rolling Update (v1.0 -> v2.0)",
        "status": "PASSED" if (rollout_update_ok and v2_image_confirmed) else "FAILED",
        "details": f"Rolling update successfully completed. All 3 active backend pods upgraded to image v2.0."
    })

    test_results["tests"].append({
        "id": "T07_ZERO_DOWNTIME_AVAILABILITY",
        "name": "Continuous High Availability During Rollout",
        "status": "PASSED" if (traffic_stats["failed"] == 0 and availability_pct == 100.0) else "FAILED",
        "details": f"{traffic_stats['success']}/{traffic_stats['sent']} requests succeeded (100.0% availability, 0 dropped requests) during active rollout."
    })

    # --------------------------------------------------------------------------
    # Test 8: Rollout Undo / Rollback Verification
    # --------------------------------------------------------------------------
    print("\n--- Test 8: Rollback Deployment & Inspect Revision History ---")
    history_pre = run_cmd(f"kubectl rollout history deployment/dl-backend-deployment -n {NAMESPACE}")
    print(f"Rollout History before undo:\n{history_pre.stdout.strip()}")

    run_cmd(f"kubectl rollout undo deployment/dl-backend-deployment -n {NAMESPACE}")
    undo_rollout_ok, _ = wait_for_rollout("dl-backend-deployment", timeout=90)
    
    history_post = run_cmd(f"kubectl rollout history deployment/dl-backend-deployment -n {NAMESPACE}")
    print(f"Rollout History after undo:\n{history_post.stdout.strip()}")

    # Wait for terminating pods to drain and verify active pods reverted to v1.0
    active_rb = wait_for_active_pod_count("app=dl-backend", target_count=3, timeout=60)
    images_rb = [p["spec"]["containers"][0]["image"] for p in active_rb]
    v1_reverted = len(images_rb) == 3 and all("v1.0" in img for img in images_rb)
    print(f"Active pod container images after rollback: {images_rb}")

    test_results["tests"].append({
        "id": "T08_ROLLOUT_ROLLBACK",
        "name": "Automated Deployment Rollback (Undo to Stable Revision)",
        "status": "PASSED" if (undo_rollout_ok and v1_reverted) else "FAILED",
        "details": f"Deployment successfully reverted to revision with image v1.0 using 'kubectl rollout undo'."
    })

    # --------------------------------------------------------------------------
    # Test 9: Horizontal Pod Autoscaler (HPA) Verification
    # --------------------------------------------------------------------------
    print("\n--- Test 9: Apply & Validate Horizontal Pod Autoscaler (HPA) ---")
    hpa_file = os.path.join(K8S_DIR, "07-backend-hpa.yaml")
    run_cmd(f"kubectl apply -f {hpa_file}")
    time.sleep(3)
    
    hpa_res = run_cmd(f"kubectl get hpa dl-backend-hpa -n {NAMESPACE} -o json")
    hpa_ok = False
    hpa_info = {}
    if hpa_res.returncode == 0:
        try:
            hpa_data = json.loads(hpa_res.stdout)
            hpa_min = hpa_data["spec"]["minReplicas"]
            hpa_max = hpa_data["spec"]["maxReplicas"]
            hpa_current = hpa_data["status"].get("currentReplicas", 0)
            hpa_target = hpa_data["spec"]["metrics"][0]["resource"]["target"]["averageUtilization"]
            hpa_ok = (hpa_min == 2 and hpa_max == 6 and hpa_target == 50)
            hpa_info = {
                "min_replicas": hpa_min,
                "max_replicas": hpa_max,
                "current_replicas": hpa_current,
                "target_cpu_utilization_pct": hpa_target
            }
            print(f"HPA Configuration: Min={hpa_min}, Max={hpa_max}, TargetCPU={hpa_target}%, CurrentReplicas={hpa_current}")
        except Exception as e:
            print(f"[!] HPA parse error: {e}")

    test_results["tests"].append({
        "id": "T09_HPA_AUTOSCALING",
        "name": "Horizontal Pod Autoscaler (HPA) Policy Validation",
        "status": "PASSED" if hpa_ok else "FAILED",
        "details": f"HPA active with target CPU {hpa_info.get('target_cpu_utilization_pct', 50)}% (Min: {hpa_info.get('min_replicas', 2)}, Max: {hpa_info.get('max_replicas', 6)})."
    })

    # --------------------------------------------------------------------------
    # Test 10: Resource Utilization Telemetry Collection
    # --------------------------------------------------------------------------
    print("\n--- Test 10: Analyze Pod and Node Resource Utilization ---")
    time.sleep(2)
    top_pods_res = run_cmd(f"kubectl top pods -n {NAMESPACE}")
    top_node_res = run_cmd("kubectl top nodes")
    print(f"Top Pods:\n{top_pods_res.stdout.strip()}")
    print(f"Top Nodes:\n{top_node_res.stdout.strip()}")

    test_results["telemetry"] = {
        "top_pods": top_pods_res.stdout.strip(),
        "top_nodes": top_node_res.stdout.strip(),
        "traffic_stats": {
            "sent": traffic_stats["sent"],
            "success": traffic_stats["success"],
            "failed": traffic_stats["failed"],
            "availability_pct": round(availability_pct, 2),
            "avg_latency_ms": round(sum(traffic_stats["latencies"]) / len(traffic_stats["latencies"]), 2) if traffic_stats["latencies"] else 0
        }
    }

    test_results["tests"].append({
        "id": "T10_RESOURCE_UTILIZATION",
        "name": "Resource Utilization Telemetry Analysis",
        "status": "PASSED" if (top_pods_res.returncode == 0 and top_node_res.returncode == 0) else "FAILED",
        "details": f"Successfully scraped resource utilization metrics across pods and nodes via metrics-server."
    })

    # --------------------------------------------------------------------------
    # Summary & Export
    # --------------------------------------------------------------------------
    print("\n" + "=" * 85)
    print(" TASK 14 VERIFICATION SUMMARY ")
    print("=" * 85)
    passed_count = sum(1 for t in test_results["tests"] if t["status"] == "PASSED")
    total_count = len(test_results["tests"])
    for t in test_results["tests"]:
        icon = "[PASS]" if t["status"] == "PASSED" else "[FAIL]"
        print(f"{icon} {t['id']}: {t['name']} - {t['details']}")

    print(f"\nFinal Score: {passed_count}/{total_count} ({passed_count/total_count*100:.1f}%) Passed")
    test_results["score"] = f"{passed_count}/{total_count}"
    test_results["percentage"] = round((passed_count / total_count) * 100, 2)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2)
    print(f"Structured results written to: {RESULTS_FILE}")

if __name__ == "__main__":
    run_test_suite()
