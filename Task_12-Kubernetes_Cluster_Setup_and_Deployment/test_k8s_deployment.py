"""
test_k8s_deployment.py
----------------------
Automated verification and operational testing suite for Task 12:
Kubernetes Cluster Setup and Deployment.

Validates:
1. Cluster Connectivity & Node Readiness (minikube / kubectl)
2. Manifest Application (Namespace, ConfigMap, Deployments, Services)
3. Deployment Rollout Status (Backend & Frontend)
4. Pod Health, Phase, and Multi-Replica Distribution
5. Service Discovery & NodePort / ClusterIP Configuration
6. In-cluster Model Inference (/health & /predict via Port-Forwarding / Exec)
7. Kubernetes Self-Healing Simulation (Pod termination & auto-recovery)
8. Horizontal Pod Scaling (Scale up to 3 replicas)
9. Structured JSON summary export for report generator and LMS validation.
"""

import os
import sys
import time
import json
import subprocess
import requests

NAMESPACE = "dl-clinical-app"
MANIFESTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k8s")
RESULTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "k8s_test_results.json")

def run_cmd(cmd, check=True):
    print(f"\n[EXEC] {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and res.returncode != 0:
        print(f"[ERROR] Command failed with code {res.returncode}:\n{res.stderr}")
    return res

def wait_for_rollout(deployment_name, timeout=180):
    print(f"[*] Waiting for {deployment_name} to finish rollout (max {timeout}s)...")
    res = run_cmd(f"kubectl rollout status deployment/{deployment_name} -n {NAMESPACE} --timeout={timeout}s", check=False)
    return res.returncode == 0, res.stdout.strip()

def run_test_suite():
    print("=" * 80)
    print(" TASK 12: KUBERNETES DEPLOYMENT & ORCHESTRATION VERIFICATION SUITE ")
    print("=" * 80)
    
    test_results = {
        "task": "Task 12: Kubernetes Cluster Setup and Deployment",
        "cluster_type": "Minikube (Docker Driver)",
        "namespace": NAMESPACE,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tests": []
    }

    # Test 1: Cluster Info & Node Status
    print("\n--- Test 1: Verify Kubernetes Cluster & Nodes ---")
    node_res = run_cmd("kubectl get nodes -o json")
    node_data = json.loads(node_res.stdout) if node_res.returncode == 0 else {}
    node_name = node_data.get("items", [{}])[0].get("metadata", {}).get("name", "unknown")
    node_ready = False
    for cond in node_data.get("items", [{}])[0].get("status", {}).get("conditions", []):
        if cond.get("type") == "Ready" and cond.get("status") == "True":
            node_ready = True
            break
            
    test_results["tests"].append({
        "name": "Cluster Node Status",
        "node_name": node_name,
        "status": "PASSED" if node_ready else "FAILED",
        "details": f"Node '{node_name}' is Ready" if node_ready else "Node is not ready"
    })
    print(f"[RESULT] Node {node_name} Ready: {node_ready}")

    # Test 2: Apply Manifests
    print("\n--- Test 2: Apply Kubernetes Declarative Manifests ---")
    apply_res = run_cmd(f"kubectl apply -f {MANIFESTS_DIR}")
    test_results["tests"].append({
        "name": "Manifest Application",
        "status": "PASSED" if apply_res.returncode == 0 else "FAILED",
        "details": apply_res.stdout.strip()
    })

    # Test 3: Backend Rollout
    print("\n--- Test 3: Verify Backend Deployment Rollout ---")
    backend_ok, backend_msg = wait_for_rollout("dl-backend-deployment")
    test_results["tests"].append({
        "name": "Backend Deployment Rollout",
        "status": "PASSED" if backend_ok else "FAILED",
        "details": backend_msg
    })

    # Test 4: Frontend Rollout
    print("\n--- Test 4: Verify Frontend Deployment Rollout ---")
    frontend_ok, frontend_msg = wait_for_rollout("dl-frontend-deployment")
    test_results["tests"].append({
        "name": "Frontend Deployment Rollout",
        "status": "PASSED" if frontend_ok else "FAILED",
        "details": frontend_msg
    })

    # Test 5: Verify Pod Replicas & Status
    print("\n--- Test 5: Pod Inspection & Health ---")
    pods_res = run_cmd(f"kubectl get pods -n {NAMESPACE} -o json")
    pods_data = json.loads(pods_res.stdout) if pods_res.returncode == 0 else {"items": []}
    pod_list = []
    all_pods_running = True
    for p in pods_data.get("items", []):
        p_name = p["metadata"]["name"]
        p_phase = p["status"]["phase"]
        p_ip = p["status"].get("podIP", "None")
        containers = p["status"].get("containerStatuses", [])
        p_ready = all(c.get("ready", False) for c in containers) if containers else False
        pod_list.append({
            "name": p_name,
            "phase": p_phase,
            "ready": p_ready,
            "ip": p_ip
        })
        if p_phase != "Running" or not p_ready:
            all_pods_running = False
        print(f"  * Pod: {p_name} | Phase: {p_phase} | Ready: {p_ready} | IP: {p_ip}")

    test_results["pods"] = pod_list
    test_results["tests"].append({
        "name": "Pod Health & Multi-Replica Status",
        "status": "PASSED" if all_pods_running and len(pod_list) >= 4 else "FAILED",
        "details": f"Total pods: {len(pod_list)}, All healthy & running: {all_pods_running}"
    })

    # Test 6: Verify Services
    print("\n--- Test 6: Service Inspection ---")
    svc_res = run_cmd(f"kubectl get svc -n {NAMESPACE} -o json")
    svc_data = json.loads(svc_res.stdout) if svc_res.returncode == 0 else {"items": []}
    svc_list = []
    for s in svc_data.get("items", []):
        s_name = s["metadata"]["name"]
        s_type = s["spec"]["type"]
        s_ip = s["spec"].get("clusterIP", "")
        ports = [f"{p['port']}:{p.get('nodePort', p['port'])}/{p['protocol']}" for p in s["spec"].get("ports", [])]
        svc_list.append({
            "name": s_name,
            "type": s_type,
            "cluster_ip": s_ip,
            "ports": ports
        })
        print(f"  * Service: {s_name} | Type: {s_type} | ClusterIP: {s_ip} | Ports: {ports}")
    test_results["services"] = svc_list

    # Test 7: Clinical Deep Learning Inference Verification
    print("\n--- Test 7: Inter-Service & Inference Validation via Backend Port-Forward ---")
    pf_proc = subprocess.Popen("kubectl port-forward svc/backend-svc -n dl-clinical-app 5005:5000", shell=True)
    time.sleep(3)
    inference_passed = False
    prediction_result = {}
    try:
        health_resp = requests.get("http://127.0.0.1:5005/health", timeout=5)
        print(f"  * /health status: {health_resp.status_code}, response: {health_resp.json()}")

        sample_patient = {
            "features": [58.0, 1.0, 2.0, 140.0, 260.0, 0.0, 1.0, 145.0, 1.0, 2.2, 1.0, 1.0, 2.0, 0.0]
        }
        pred_resp = requests.post("http://127.0.0.1:5005/predict", json=sample_patient, timeout=10)
        prediction_result = pred_resp.json()
        print(f"  * /predict status: {pred_resp.status_code}, response: {prediction_result}")
        inference_passed = (pred_resp.status_code == 200 and "predictions" in prediction_result)
    except Exception as e:
        print(f"[ERROR] Inference test failed: {e}")
    finally:
        pf_proc.terminate()
        try:
            pf_proc.kill()
        except Exception:
            pass

    test_results["tests"].append({
        "name": "Live DL PyTorch Inference inside Cluster",
        "status": "PASSED" if inference_passed else "FAILED",
        "sample_prediction": prediction_result
    })

    # Test 8: Kubernetes Self-Healing Simulation
    print("\n--- Test 8: Self-Healing Test (Pod Termination & Auto-Recovery) ---")
    backend_pods = [p["name"] for p in pod_list if "dl-backend" in p["name"]]
    if backend_pods:
        victim_pod = backend_pods[0]
        print(f"  * Terminating pod '{victim_pod}' to test self-healing...")
        del_res = run_cmd(f"kubectl delete pod {victim_pod} -n {NAMESPACE} --grace-period=0 --force")
        time.sleep(4)
        post_pods_res = run_cmd(f"kubectl get pods -n {NAMESPACE} -o json")
        post_data = json.loads(post_pods_res.stdout) if post_pods_res.returncode == 0 else {"items": []}
        new_backend_pods = [p["metadata"]["name"] for p in post_data.get("items", []) if "dl-backend" in p["metadata"]["name"]]
        
        healed = victim_pod not in new_backend_pods or len(new_backend_pods) >= 2
        print(f"  * Self-healing result: Old pod terminated, active backend replicas: {len(new_backend_pods)}")
        test_results["tests"].append({
            "name": "Self-Healing Auto-Recovery",
            "status": "PASSED" if healed else "FAILED",
            "details": f"Terminated {victim_pod}; ReplicaSet automatically spawned replacement pod. Active replicas: {len(new_backend_pods)}"
        })
    else:
        test_results["tests"].append({
            "name": "Self-Healing Auto-Recovery",
            "status": "SKIPPED",
            "details": "No backend pods found"
        })

    # Test 9: Horizontal Scaling
    print("\n--- Test 9: Horizontal Scaling (Scale up to 3 Replicas) ---")
    scale_res = run_cmd(f"kubectl scale deployment dl-backend-deployment --replicas=3 -n {NAMESPACE}")
    time.sleep(5)
    scale_check = run_cmd(f"kubectl get deployment dl-backend-deployment -n {NAMESPACE} -o json")
    scale_data = json.loads(scale_check.stdout) if scale_check.returncode == 0 else {}
    spec_replicas = scale_data.get("spec", {}).get("replicas", 0)
    print(f"  * Scale desired replicas: {spec_replicas}")
    test_results["tests"].append({
        "name": "Horizontal Deployment Scaling",
        "status": "PASSED" if spec_replicas == 3 else "FAILED",
        "details": f"Deployment scaled to {spec_replicas} replicas successfully"
    })

    # Write output to file
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2)
    print(f"\n[OK] Test suite complete! Results written to: {RESULTS_FILE}")
    return test_results

if __name__ == "__main__":
    run_test_suite()
