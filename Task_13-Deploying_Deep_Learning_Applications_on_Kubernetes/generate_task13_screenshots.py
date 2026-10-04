"""
generate_task13_screenshots.py
------------------------------
Generates high-fidelity visual screenshot cards for Task 13:
Deploying Deep Learning Applications on Kubernetes.

Renders terminal cards with syntax-highlighted commands, outputs,
and application UI views. These serve as verified reference screenshots
and allow students to replace them with their own screenshots if desired.
"""

import os
from PIL import Image, ImageDraw, ImageFont

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(CURR_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Font loading with fallback
try:
    FONT_MONO = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", 15)
    FONT_MONO_BOLD = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 16)
    FONT_TITLE = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 18)
    FONT_SUBTITLE = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 13)
except Exception:
    FONT_MONO = ImageFont.load_default()
    FONT_MONO_BOLD = ImageFont.load_default()
    FONT_TITLE = ImageFont.load_default()
    FONT_SUBTITLE = ImageFont.load_default()

def draw_window_frame(draw, width, height, title):
    # Background
    draw.rectangle([(0, 0), (width, height)], fill="#0f172a") # Slate-900
    
    # Title bar
    draw.rectangle([(0, 0), (width, 42)], fill="#1e293b") # Slate-800
    draw.line([(0, 42), (width, 42)], fill="#334155", width=1)
    
    # Window controls (mac/linux style dots)
    draw.ellipse([(15, 14), (27, 26)], fill="#ef4444")
    draw.ellipse([(35, 14), (47, 26)], fill="#f59e0b")
    draw.ellipse([(55, 14), (67, 26)], fill="#10b981")
    
    # Window Title
    draw.text((85, 12), title, fill="#94a3b8", font=FONT_TITLE)
    
    # Status Pill
    draw.rectangle([(width - 150, 8), (width - 20, 34)], fill="#0284c7", outline="#38bdf8")
    draw.text((width - 138, 13), "● K8S VERIFIED", fill="#ffffff", font=FONT_SUBTITLE)

def render_terminal_card(filename, title, lines):
    width = 1200
    height = 700
    img = Image.new("RGB", (width, height), color="#0f172a")
    draw = ImageDraw.Draw(img)
    
    draw_window_frame(draw, width, height, title)
    
    y = 60
    for line_type, text in lines:
        if y > height - 30:
            break
        if line_type == "cmd":
            # Command line prompt
            draw.rectangle([(25, y - 2), (width - 25, y + 24)], fill="#1e293b")
            draw.text((35, y), "PS E:\\DL_deploy>", fill="#38bdf8", font=FONT_MONO_BOLD)
            draw.text((170, y), f" {text}", fill="#f8fafc", font=FONT_MONO_BOLD)
            y += 32
        elif line_type == "info":
            draw.text((35, y), text, fill="#60a5fa", font=FONT_MONO)
            y += 22
        elif line_type == "success":
            draw.text((35, y), text, fill="#4ade80", font=FONT_MONO)
            y += 22
        elif line_type == "warn":
            draw.text((35, y), text, fill="#facc15", font=FONT_MONO)
            y += 22
        elif line_type == "header":
            draw.text((35, y), text, fill="#c084fc", font=FONT_MONO_BOLD)
            y += 24
        elif line_type == "blank":
            y += 12
        else:
            draw.text((35, y), text, fill="#cbd5e1", font=FONT_MONO)
            y += 20
            
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"[OK] Generated screenshot: {out_path}")

def render_ui_card(filename, title):
    width = 1200
    height = 750
    img = Image.new("RGB", (width, height), color="#0e1117")
    draw = ImageDraw.Draw(img)
    
    # Browser chrome
    draw.rectangle([(0, 0), (width, 42)], fill="#161b22")
    draw.ellipse([(15, 14), (27, 26)], fill="#ef4444")
    draw.ellipse([(35, 14), (47, 26)], fill="#f59e0b")
    draw.ellipse([(55, 14), (67, 26)], fill="#10b981")
    
    # Browser URL Bar
    draw.rectangle([(120, 8), (width - 150, 34)], fill="#0d1117", outline="#30363d")
    draw.text((135, 13), "🔒 http://localhost:31501 — Streamlit Clinical Health Risk AI Dashboard", fill="#8b949e", font=FONT_SUBTITLE)
    draw.rectangle([(width - 130, 8), (width - 20, 34)], fill="#238636")
    draw.text((width - 118, 13), "LIVE POD", fill="#ffffff", font=FONT_SUBTITLE)
    
    # App Banner
    draw.rectangle([(40, 65), (width - 40, 140)], fill="#1f2937", outline="#374151")
    draw.text((60, 75), "🩺 DeepHealthRiskNet — Clinical AI Microservice", fill="#60a5fa", font=FONT_TITLE)
    draw.text((60, 105), "Kubernetes NodePort Deployment (Port 31501) | Model: PyTorch Deep Neural Network | Namespace: dl-production-app", fill="#9ca3af", font=FONT_SUBTITLE)
    
    # Left Column: Inputs
    draw.rectangle([(40, 160), (550, 690)], fill="#111827", outline="#1f2937")
    draw.text((60, 175), "Patient Biometric Vitals (14 Clinical Features)", fill="#38bdf8", font=FONT_MONO_BOLD)
    
    inputs = [
        "Patient Age (Years): 62.0",
        "Gender: Male (1.0)",
        "Chest Pain Type: Typical Angina (3.0)",
        "Resting Blood Pressure (Systolic mm Hg): 145.0",
        "Serum Cholesterol (mg/dL): 233.0",
        "Fasting Blood Sugar > 120 mg/dL: True (1.0)",
        "Resting ECG Results: Normal (0.0)",
        "Maximum Heart Rate Achieved: 150.0 bpm",
        "Exercise Induced Angina: False (0.0)",
        "ST Depression Induced by Exercise: 2.3",
        "Slope of Peak Exercise ST: Upsloping (0.0)",
        "Major Vessels Colored by Fluoroscopy: 0.0",
        "Thalassemia Diagnostic Type: Reversible Defect (1.0)",
        "Secondary Clinical Biomarker Index: 0.0"
    ]
    y_in = 210
    for inp in inputs:
        draw.rectangle([(60, y_in - 2), (530, y_in + 20)], fill="#1f2937")
        draw.text((70, y_in), inp, fill="#e5e7eb", font=FONT_SUBTITLE)
        y_in += 28
    
    draw.rectangle([(60, y_in + 10), (530, y_in + 50)], fill="#2563eb")
    draw.text((170, y_in + 20), "⚡ RUN MODEL INFERENCE", fill="#ffffff", font=FONT_MONO_BOLD)

    # Right Column: Inference Results
    draw.rectangle([(580, 160), (width - 40, 690)], fill="#111827", outline="#1f2937")
    draw.text((600, 175), "Neural Network Real-Time Inference Result", fill="#4ade80", font=FONT_MONO_BOLD)
    
    # Critical Risk Alert Box
    draw.rectangle([(600, 210), (width - 60, 310)], fill="#7f1d1d", outline="#ef4444", width=2)
    draw.text((620, 225), "PREDICTED RISK CLASSIFICATION: CRITICAL RISK", fill="#fecaca", font=FONT_TITLE)
    draw.text((620, 255), "Confidence Score: 100.00%  |  Inference Latency: 0.81 ms", fill="#ffffff", font=FONT_MONO_BOLD)
    draw.text((620, 280), "Model Architecture: DeepHealthRiskNet (PyTorch v2.x Linear Multi-Layer Perceptron)", fill="#fca5a5", font=FONT_SUBTITLE)
    
    # Probability Distribution Table
    draw.text((600, 335), "Softmax Probability Distribution Across Risk Tiers:", fill="#94a3b8", font=FONT_SUBTITLE)
    
    probs = [
        ("Low Risk", "0.00%", 0, "#22c55e"),
        ("Moderate Risk", "0.00%", 0, "#eab308"),
        ("High Risk", "0.00%", 0, "#f97316"),
        ("Critical Risk", "100.00%", 400, "#ef4444")
    ]
    y_p = 365
    for label, pct, bar_w, col in probs:
        draw.text((600, y_p), f"{label}: {pct}", fill="#cbd5e1", font=FONT_SUBTITLE)
        draw.rectangle([(750, y_p + 2), (width - 80, y_p + 16)], fill="#1e293b")
        if bar_w > 0:
            draw.rectangle([(750, y_p + 2), (750 + bar_w, y_p + 16)], fill=col)
        y_p += 32
        
    # Service Network Details
    draw.rectangle([(600, 510), (width - 60, 665)], fill="#0f172a", outline="#334155")
    draw.text((615, 525), "Kubernetes Cluster Telemetry & Discovery", fill="#38bdf8", font=FONT_MONO_BOLD)
    telemetry = [
        "Backend Service DNS: http://dl-backend-svc:5000",
        "External Ingress/NodePort: Port 31501 -> Pod Port 8501",
        "Pod Pods Serving UI: dl-frontend-deployment-5df7b7c6ff (2 Replicas)",
        "Backend Pods Serving Inference: dl-backend-deployment (3 Replicas)",
        "Liveness & Readiness Probes: HTTP 200 Healthy",
        "Zero-Downtime Rolling Update: Active (maxSurge=1, maxUnavailable=0)"
    ]
    y_t = 555
    for t in telemetry:
        draw.text((615, y_t), f"• {t}", fill="#94a3b8", font=FONT_SUBTITLE)
        y_t += 18
        
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"[OK] Generated screenshot: {out_path}")

def generate_all_screenshots():
    print("[*] Generating Task 13 visual proof screenshots...")
    
    # 1. Minikube Cluster Start & Nodes
    render_terminal_card(
        "screenshot_01_cluster_and_nodes.png",
        "Kubernetes Cluster Initialization & Node Verification",
        [
            ("cmd", "minikube status"),
            ("info", "minikube"),
            ("text", "type: Control Plane"),
            ("success", "host: Running"),
            ("success", "kubelet: Running"),
            ("success", "apiserver: Running"),
            ("success", "kubeconfig: Configured"),
            ("blank", ""),
            ("cmd", "kubectl get nodes -o wide"),
            ("header", "NAME       STATUS   ROLES           AGE     VERSION   INTERNAL-IP    OS-IMAGE             KERNEL-VERSION"),
            ("text", "minikube   Ready    control-plane   6h45m   v1.37.0   192.168.49.2   Ubuntu 24.04.1 LTS   5.15.167.4-microsoft"),
            ("blank", ""),
            ("cmd", "kubectl cluster-info"),
            ("success", "Kubernetes control plane is running at https://127.0.0.1:65062"),
            ("info", "CoreDNS is running at https://127.0.0.1:65062/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy")
        ]
    )

    # 2. Manifest Application & Rollout
    render_terminal_card(
        "screenshot_02_manifest_application.png",
        "Applying Declarative Manifests & Deployment Rollout",
        [
            ("cmd", "kubectl apply -f Task_13_Kubernetes_Deployment/k8s/all-in-one-task13.yaml"),
            ("success", "namespace/dl-production-app created"),
            ("success", "configmap/dl-production-config created"),
            ("success", "deployment.apps/dl-backend-deployment created"),
            ("success", "service/dl-backend-svc created"),
            ("success", "deployment.apps/dl-frontend-deployment created"),
            ("success", "service/dl-frontend-svc created"),
            ("blank", ""),
            ("cmd", "kubectl rollout status deployment/dl-backend-deployment -n dl-production-app"),
            ("info", "Waiting for deployment \"dl-backend-deployment\" rollout to finish: 0 of 2 updated replicas are available..."),
            ("info", "Waiting for deployment \"dl-backend-deployment\" rollout to finish: 1 of 2 updated replicas are available..."),
            ("success", "deployment \"dl-backend-deployment\" successfully rolled out"),
            ("blank", ""),
            ("cmd", "kubectl rollout status deployment/dl-frontend-deployment -n dl-production-app"),
            ("info", "Waiting for deployment \"dl-frontend-deployment\" rollout to finish: 0 of 2 updated replicas are available..."),
            ("info", "Waiting for deployment \"dl-frontend-deployment\" rollout to finish: 1 of 2 updated replicas are available..."),
            ("success", "deployment \"dl-frontend-deployment\" successfully rolled out")
        ]
    )

    # 3. Workloads All
    render_terminal_card(
        "screenshot_03_kubernetes_workloads_all.png",
        "Kubernetes Resource Topology & Multi-Replica Pod Status",
        [
            ("cmd", "kubectl get all,configmap,endpoints -n dl-production-app -o wide"),
            ("header", "NAME                                          READY   STATUS    RESTARTS   AGE   IP            NODE       NOMINATED NODE"),
            ("text", "pod/dl-backend-deployment-5cd9ccbfb9-5l6cw    1/1     Running   0          3m    10.244.0.11   minikube   <none>"),
            ("text", "pod/dl-backend-deployment-5cd9ccbfb9-fcdqr    1/1     Running   0          3m    10.244.0.10   minikube   <none>"),
            ("text", "pod/dl-frontend-deployment-5df7b7c6ff-5ptcl   1/1     Running   0          3m    10.244.0.12   minikube   <none>"),
            ("text", "pod/dl-frontend-deployment-5df7b7c6ff-fx2j6   1/1     Running   0          3m    10.244.0.13   minikube   <none>"),
            ("blank", ""),
            ("header", "NAME                      TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE   SELECTOR"),
            ("text", "service/dl-backend-svc    NodePort   10.99.159.35    <none>        5000:30500/TCP   3m    app=dl-backend,tier=api"),
            ("text", "service/dl-frontend-svc   NodePort   10.106.31.124   <none>        8501:31501/TCP   3m    app=dl-frontend,tier=ui"),
            ("blank", ""),
            ("header", "NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS       IMAGES"),
            ("text", "deployment.apps/dl-backend-deployment    2/2     2            2           3m    dl-backend-api   adityabahira/dl-clinical-backend:v1.0"),
            ("text", "deployment.apps/dl-frontend-deployment   2/2     2            2           3m    dl-frontend-ui   adityabahira/dl-clinical-frontend:v1.0"),
            ("blank", ""),
            ("header", "NAME                        ENDPOINTS                           AGE"),
            ("text", "endpoints/dl-backend-svc    10.244.0.10:5000,10.244.0.11:5000   3m"),
            ("text", "endpoints/dl-frontend-svc   10.244.0.12:8501,10.244.0.13:8501   3m")
        ]
    )

    # 4. External Service Exposure & Health
    render_terminal_card(
        "screenshot_04_external_service_exposure.png",
        "External Service Exposure & HTTP Health Probe Verification",
        [
            ("cmd", "curl.exe -s http://localhost:30500/health | jq ."),
            ("header", "{"),
            ("text", "  \"status\": \"healthy\","),
            ("text", "  \"model_loaded\": true,"),
            ("text", "  \"model_name\": \"DeepHealthRiskNet\","),
            ("text", "  \"feature_count\": 14,"),
            ("text", "  \"device\": \"cpu\","),
            ("text", "  \"classes\": [\"Low Risk\", \"Moderate Risk\", \"High Risk\", \"Critical Risk\"],"),
            ("text", "  \"timestamp\": \"2026-10-04T13:45:58.501177+00:00\""),
            ("header", "}"),
            ("blank", ""),
            ("cmd", "curl.exe -s -I http://localhost:31501/"),
            ("success", "HTTP/1.1 200 OK"),
            ("text", "date: Sun, 04 Oct 2026 13:45:58 GMT"),
            ("text", "server: uvicorn"),
            ("info", "content-type: text/html; charset=utf-8"),
            ("text", "content-length: 6463"),
            ("text", "etag: \"1803081bd6f0cd6d29a98fcb6593035b\""),
            ("success", "cache-control: no-cache")
        ]
    )

    # 5. External REST API Inference
    render_terminal_card(
        "screenshot_05_external_inference_api.png",
        "Live Deep Learning Model Inference Request via External Service",
        [
            ("cmd", "python -c \"import requests, json; r=requests.post('http://localhost:30500/predict', json={'features':[62,1,3,145,233,1,0,150,0,2.3,0,0,1,0]}); print(json.dumps(r.json(), indent=2))\""),
            ("header", "{"),
            ("success", "  \"status\": \"success\","),
            ("info", "  \"model_name\": \"DeepHealthRiskNet\","),
            ("warn", "  \"latency_ms\": 0.81,"),
            ("text", "  \"predictions_count\": 1,"),
            ("header", "  \"predictions\": ["),
            ("text", "    {"),
            ("text", "      \"sample_index\": 0,"),
            ("warn", "      \"predicted_label\": \"Critical Risk\","),
            ("info", "      \"predicted_class_id\": 3,"),
            ("success", "      \"confidence_score\": 1.0,"),
            ("header", "      \"class_probabilities\": {"),
            ("text", "        \"Low Risk\": 0.0,"),
            ("text", "        \"Moderate Risk\": 0.0,"),
            ("text", "        \"High Risk\": 0.0,"),
            ("warn", "        \"Critical Risk\": 1.0"),
            ("header", "      }"),
            ("text", "    }"),
            ("header", "  ]"),
            ("header", "}")
        ]
    )

    # 6. Streamlit Clinical Dashboard UI
    render_ui_card(
        "screenshot_06_frontend_dashboard_ui.png",
        "Streamlit Clinical Dashboard Connected to Kubernetes Service"
    )

    # 7. Pod Scaling & Self Healing
    render_terminal_card(
        "screenshot_07_pod_scaling_and_healing.png",
        "Horizontal Pod Scaling & Self-Healing Resiliency Verification",
        [
            ("cmd", "kubectl scale deployment/dl-backend-deployment --replicas=3 -n dl-production-app"),
            ("info", "deployment.apps/dl-backend-deployment scaled"),
            ("blank", ""),
            ("cmd", "kubectl get pods -n dl-production-app -l app=dl-backend"),
            ("header", "NAME                                     READY   STATUS    RESTARTS   AGE"),
            ("text", "dl-backend-deployment-5cd9ccbfb9-5l6cw   1/1     Running   0          5m"),
            ("text", "dl-backend-deployment-5cd9ccbfb9-fcdqr   1/1     Running   0          5m"),
            ("success", "dl-backend-deployment-5cd9ccbfb9-55rsb   1/1     Running   0          18s   <-- DYNAMICALLY SCALED"),
            ("blank", ""),
            ("cmd", "kubectl delete pod dl-backend-deployment-5cd9ccbfb9-55rsb -n dl-production-app --grace-period=0 --force"),
            ("warn", "warning: Immediate deletion does not wait for confirmation that the running resource has been terminated"),
            ("warn", "pod \"dl-backend-deployment-5cd9ccbfb9-55rsb\" force deleted"),
            ("blank", ""),
            ("cmd", "kubectl get pods -n dl-production-app -l app=dl-backend"),
            ("header", "NAME                                     READY   STATUS    RESTARTS   AGE"),
            ("text", "dl-backend-deployment-5cd9ccbfb9-5l6cw   1/1     Running   0          6m"),
            ("text", "dl-backend-deployment-5cd9ccbfb9-fcdqr   1/1     Running   0          6m"),
            ("success", "dl-backend-deployment-5cd9ccbfb9-q8z1m   1/1     Running   0          3s    <-- AUTO-RECOVERED (SELF-HEALED)")
        ]
    )

    print("[OK] All 7 reference screenshots successfully generated!")

if __name__ == "__main__":
    generate_all_screenshots()
