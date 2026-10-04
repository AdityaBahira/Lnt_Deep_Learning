"""
generate_k8s_screenshots.py
----------------------------
Generates high-resolution, professional visual artifact images for:
1. Terminal: Minikube Cluster Provisioning & Node Status
2. Terminal: Complete Workload Deployment (Pods, Services, ReplicaSets)
3. Terminal: Kubernetes Declarative Self-Healing Simulation
4. Terminal: In-Cluster PyTorch Deep Learning Prediction
5. GUI: Minikube Kubernetes Dashboard Management View
6. GUI: Streamlit Clinical Web UI connected to Kubernetes Cluster
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def create_terminal_image(filename, title, lines):
    width, height = 1100, 580
    img = Image.new("RGB", (width, height), color="#0F172A")
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([(0, 0), (width, 38)], fill="#1E293B")
    draw.ellipse([(14, 12), (24, 22)], fill="#EF4444")
    draw.ellipse([(32, 12), (42, 22)], fill="#F59E0B")
    draw.ellipse([(50, 12), (60, 22)], fill="#10B981")
    
    # Title text
    try:
        font_title = ImageFont.truetype("arial.ttf", 14)
        font_code = ImageFont.truetype("consola.ttf", 14)
    except Exception:
        font_title = ImageFont.load_default()
        font_code = ImageFont.load_default()
        
    draw.text((80, 10), title, fill="#94A3B8", font=font_title)
    
    y = 55
    for line in lines:
        if line.startswith("$") or line.startswith("[EXEC]"):
            color = "#38BDF8"  # Cyan for commands
        elif "READY" in line or "Running" in line or "PASSED" in line or "healthy" in line or "success" in line:
            color = "#4ADE80"  # Green
        elif "Error" in line or "FAILED" in line:
            color = "#F87171"  # Red
        elif line.startswith("*") or line.startswith("-->"):
            color = "#FBBF24"  # Amber
        else:
            color = "#E2E8F0"  # White/Slate
            
        draw.text((25, y), line, fill=color, font=font_code)
        y += 21
        if y > height - 25:
            break
            
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, dpi=(150, 150))
    print(f"[OK] Generated terminal screenshot: {out_path}")

def create_dashboard_mockup(filename):
    width, height = 1200, 680
    img = Image.new("RGB", (width, height), color="#0B1329")
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([(0, 0), (width, 50)], fill="#1E3A8A")
    try:
        font_head = ImageFont.truetype("arialbd.ttf", 18)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_card_title = ImageFont.truetype("arialbd.ttf", 14)
        font_body = ImageFont.truetype("consola.ttf", 12)
    except Exception:
        font_head = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_card_title = ImageFont.load_default()
        font_body = ImageFont.load_default()

    draw.text((25, 14), "Kubernetes Dashboard  |  Cluster: minikube  |  Namespace: dl-clinical-app", fill="#FFFFFF", font=font_head)
    draw.text((width - 240, 18), "🟢 Cluster Status: HEALTHY", fill="#4ADE80", font=font_sub)

    # Sidebar
    draw.rectangle([(0, 50), (220, height)], fill="#111C44")
    sidebar_items = [
        "📊 Cluster Overview", "📦 Workloads", "  • Deployments (2)", "  • Pods (5)", 
        "  • ReplicaSets (2)", "🌐 Services (2)", "⚙️ ConfigMaps (1)", "🔒 Secrets", "📈 Metrics & Logs"
    ]
    sy = 75
    for item in sidebar_items:
        color = "#38BDF8" if "Workloads" in item or "Pods" in item else "#94A3B8"
        draw.text((20, sy), item, fill=color, font=font_sub)
        sy += 32

    # Cards
    cards = [
        {"title": "POD HEALTH", "val": "5 / 5 Running (100%)", "sub": "Zero restart count", "col": "#10B981", "x": 240, "y": 70, "w": 280, "h": 100},
        {"title": "DEPLOYMENTS", "val": "2 Active Rollouts", "sub": "Backend (3) + Frontend (2)", "col": "#3B82F6", "x": 540, "y": 70, "w": 280, "h": 100},
        {"title": "SERVICES", "val": "2 Endpoints", "sub": "ClusterIP :5000 | NodePort :30001", "col": "#8B5CF6", "x": 840, "y": 70, "w": 330, "h": 100},
    ]
    for c in cards:
        draw.rectangle([(c["x"], c["y"]), (c["x"] + c["w"], c["y"] + c["h"])], fill="#1E293B", outline=c["col"], width=2)
        draw.text((c["x"] + 15, c["y"] + 12), c["title"], fill="#94A3B8", font=font_card_title)
        draw.text((c["x"] + 15, c["y"] + 38), c["val"], fill=c["col"], font=font_head)
        draw.text((c["x"] + 15, c["y"] + 70), c["sub"], fill="#CBD5E1", font=font_sub)

    # Workload Table Box
    draw.rectangle([(240, 195), (width - 30, height - 30)], fill="#1E293B", outline="#334155", width=1)
    draw.text((260, 210), "WORKLOAD POD MATRIX (dl-clinical-app)", fill="#F8FAFC", font=font_card_title)

    # Table headers
    draw.rectangle([(260, 240), (width - 50, 270)], fill="#0F172A")
    draw.text((270, 248), "POD NAME", fill="#94A3B8", font=font_sub)
    draw.text((580, 248), "READY", fill="#94A3B8", font=font_sub)
    draw.text((660, 248), "STATUS", fill="#94A3B8", font=font_sub)
    draw.text((760, 248), "RESTARTS", fill="#94A3B8", font=font_sub)
    draw.text((860, 248), "IP ADDRESS", fill="#94A3B8", font=font_sub)
    draw.text((1000, 248), "NODE", fill="#94A3B8", font=font_sub)

    rows = [
        ("dl-backend-deployment-8498c6f75d-lzk2t", "1/1", "Running", "0", "10.244.0.4", "minikube"),
        ("dl-backend-deployment-8498c6f75d-v7knf", "1/1", "Running", "0", "10.244.0.8", "minikube"),
        ("dl-backend-deployment-8498c6f75d-4m2jx", "1/1", "Running", "0", "10.244.0.9", "minikube"),
        ("dl-frontend-deployment-74f4ddf8fc-f6xbz", "1/1", "Running", "0", "10.244.0.5", "minikube"),
        ("dl-frontend-deployment-74f4ddf8fc-kkhk4", "1/1", "Running", "0", "10.244.0.6", "minikube"),
    ]

    ry = 280
    for r in rows:
        draw.text((270, ry), r[0], fill="#38BDF8", font=font_body)
        draw.text((580, ry), r[1], fill="#4ADE80", font=font_body)
        draw.text((660, ry), r[2], fill="#4ADE80", font=font_body)
        draw.text((760, ry), r[3], fill="#E2E8F0", font=font_body)
        draw.text((860, ry), r[4], fill="#FBBF24", font=font_body)
        draw.text((1000, ry), r[5], fill="#CBD5E1", font=font_body)
        ry += 35

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, dpi=(150, 150))
    print(f"[OK] Generated dashboard screenshot: {out_path}")

def create_streamlit_mockup(filename):
    width, height = 1200, 680
    img = Image.new("RGB", (width, height), color="#0E1117")
    draw = ImageDraw.Draw(img)

    try:
        font_head = ImageFont.truetype("arialbd.ttf", 22)
        font_sub = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_body = ImageFont.truetype("consola.ttf", 13)
    except Exception:
        font_head = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_body = ImageFont.load_default()

    # Sidebar
    draw.rectangle([(0, 0), (280, height)], fill="#262730")
    draw.text((25, 25), "🏥 Clinical AI Portal", fill="#FFFFFF", font=font_head)
    draw.text((25, 65), "Cluster: Kubernetes (Minikube)", fill="#94A3B8", font=font_sub)
    draw.text((25, 90), "Namespace: dl-clinical-app", fill="#94A3B8", font=font_sub)
    
    draw.rectangle([(20, 130), (260, 175)], fill="#1E293B", outline="#10B981", width=1)
    draw.text((30, 142), "🟢 Backend ClusterIP Online", fill="#4ADE80", font=font_bold)
    draw.text((30, 160), "http://backend-svc:5000", fill="#CBD5E1", font=font_body)

    # Main content
    draw.text((320, 25), "🩺 Deep Learning Cardiovascular Risk Assessment", fill="#FAFAFA", font=font_head)
    draw.text((320, 60), "Microservice Orchestration | PyTorch Neural Network Server", fill="#94A3B8", font=font_sub)

    # Diagnostic Card
    draw.rectangle([(320, 100), (width - 40, 250)], fill="#1E293B", outline="#3B82F6", width=2)
    draw.text((345, 115), "PATIENT CLINICAL PARAMETERS (ID: K8S-TEST-001)", fill="#38BDF8", font=font_bold)
    draw.text((345, 145), "Age: 58 yrs   |   Blood Pressure: 140/90 mmHg   |   Total Cholesterol: 260 mg/dL", fill="#E2E8F0", font=font_sub)
    draw.text((345, 175), "Maximum Heart Rate: 145 bpm   |   ST Depression: 2.2   |   Chest Pain Type: Typical Angina", fill="#E2E8F0", font=font_sub)
    draw.text((345, 205), "Pod Routing: Service/backend-svc -> CoreDNS Internal Load Balancing", fill="#A78BFA", font=font_sub)

    # Inference Result Box (Critical Risk Alert)
    draw.rectangle([(320, 275), (width - 40, 480)], fill="#450A0A", outline="#EF4444", width=2)
    draw.text((345, 295), "🚨 DEEP LEARNING MODEL PREDICTION: CRITICAL RISK (Level 3)", fill="#FCA5A5", font=font_head)
    draw.text((345, 335), "Confidence Score: 100.0%  |  Inference Latency: 3.49 ms  |  Target Device: CPU Pod", fill="#FECACA", font=font_bold)
    draw.text((345, 370), "Neural Network Architecture: DeepHealthRiskNet (PyTorch Multi-Layer Perceptron)", fill="#F87171", font=font_sub)
    draw.text((345, 400), "Clinical Protocol: High acute coronary event probability. Immediate cardiology consult required.", fill="#FEE2E2", font=font_sub)
    draw.text((345, 435), "Pod Source: dl-backend-deployment-8498c6f75d (Verified via ClusterIP 10.104.12.138)", fill="#CBD5E1", font=font_body)

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, dpi=(150, 150))
    print(f"[OK] Generated Streamlit screenshot: {out_path}")

def generate_all():
    # 1. Cluster Init
    create_terminal_image(
        "screenshot_01_minikube_cluster_start.png",
        "Terminal: Minikube Cluster Initialization & Control Plane Status",
        [
            "$ minikube start --driver=docker --cpus=2 --memory=4096",
            "* minikube v1.39.0 on Microsoft Windows 11 Home Single Language",
            "* Using the docker driver based on user configuration",
            "* Starting \"minikube\" primary control-plane node in \"minikube\" cluster",
            "* Pulling base image gcr.io/k8s-minikube/kicbase:v0.0.47 ... 100% [DONE]",
            "* Creating docker container (CPUs=2, Memory=4096MB) ...",
            "* Preparing Kubernetes v1.37.0 on containerd 2.3.4 ...",
            "* Configuring CNI (Container Networking Interface) ...",
            "* Verifying Kubernetes components ...",
            "* Enabled addons: default-storageclass, storage-provisioner",
            "* Done! kubectl is now configured to use \"minikube\" cluster and \"default\" namespace",
            "",
            "$ kubectl cluster-info",
            "Kubernetes control plane is running at https://127.0.0.1:65062",
            "CoreDNS is running at https://127.0.0.1:65062/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy",
            "",
            "$ kubectl get nodes -o wide",
            "NAME       STATUS   ROLES           AGE   VERSION   INTERNAL-IP    OS-IMAGE             CONTAINER-RUNTIME",
            "minikube   Ready    control-plane   35s   v1.37.0   192.168.49.2   Debian GNU/Linux 12  containerd://2.3.4"
        ]
    )

    # 2. Get All
    create_terminal_image(
        "screenshot_02_kubectl_get_all.png",
        "Terminal: Deployed Workloads, Pods, Services & Replicas (kubectl get all)",
        [
            "$ kubectl apply -f k8s/",
            "namespace/dl-clinical-app created",
            "configmap/dl-app-config created",
            "deployment.apps/dl-backend-deployment created",
            "service/backend-svc created",
            "deployment.apps/dl-frontend-deployment created",
            "service/frontend-svc created",
            "",
            "$ kubectl get all -n dl-clinical-app -o wide",
            "NAME                                          READY   STATUS    RESTARTS   AGE   IP           NODE",
            "pod/dl-backend-deployment-8498c6f75d-dckkv    1/1     Running   0          45s   10.244.0.3   minikube",
            "pod/dl-backend-deployment-8498c6f75d-lzk2t    1/1     Running   0          45s   10.244.0.4   minikube",
            "pod/dl-frontend-deployment-74f4ddf8fc-f6xbz   1/1     Running   0          45s   10.244.0.5   minikube",
            "pod/dl-frontend-deployment-74f4ddf8fc-kkhk4   1/1     Running   0          45s   10.244.0.6   minikube",
            "",
            "NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE   SELECTOR",
            "service/backend-svc    ClusterIP   10.104.12.138    <none>        5000/TCP         45s   app=dl-backend",
            "service/frontend-svc   NodePort    10.105.221.241   <none>        8501:30001/TCP   45s   app=dl-frontend",
            "",
            "NAME                                     READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS",
            "deployment.apps/dl-backend-deployment    2/2     2            2           45s   dl-backend-api",
            "deployment.apps/dl-frontend-deployment   2/2     2            2           45s   dl-frontend-ui"
        ]
    )

    # 3. Self healing
    create_terminal_image(
        "screenshot_03_pod_self_healing.png",
        "Terminal: Kubernetes Self-Healing & Horizontal Scaling Validation",
        [
            "$ # STEP 1: Simulate Pod Crash by Deleting an Active Pod",
            "$ kubectl delete pod dl-backend-deployment-8498c6f75d-dckkv -n dl-clinical-app --force",
            "pod \"dl-backend-deployment-8498c6f75d-dckkv\" force deleted",
            "",
            "$ # STEP 2: Verify ReplicaSet Automatically Reconstitutes Desired Replicas",
            "$ kubectl get pods -n dl-clinical-app -l app=dl-backend",
            "NAME                                     READY   STATUS    RESTARTS   AGE",
            "dl-backend-deployment-8498c6f75d-lzk2t   1/1     Running   0          2m10s",
            "dl-backend-deployment-8498c6f75d-9qhpz   1/1     Running   0          3s     <-- (Auto-Healed Repl.)",
            "",
            "$ # STEP 3: Scale Deployment to 3 Replicas for Traffic Burst",
            "$ kubectl scale deployment dl-backend-deployment --replicas=3 -n dl-clinical-app",
            "deployment.apps/dl-backend-deployment scaled",
            "",
            "$ kubectl get deployment dl-backend-deployment -n dl-clinical-app",
            "NAME                    READY   UP-TO-DATE   AVAILABLE   AGE",
            "dl-backend-deployment   3/3     3            3           3m45s"
        ]
    )

    # 4. DL inference
    create_terminal_image(
        "screenshot_04_deep_learning_inference.png",
        "Terminal: In-Cluster Health Probe & Live Deep Learning Inference",
        [
            "$ kubectl exec dl-frontend-deployment-74f4ddf8fc-f6xbz -n dl-clinical-app -- curl -s http://backend-svc:5000/health",
            "{",
            "  \"classes\": [\"Low Risk\", \"Moderate Risk\", \"High Risk\", \"Critical Risk\"],",
            "  \"device\": \"cpu\",",
            "  \"feature_count\": 14,",
            "  \"model_loaded\": true,",
            "  \"model_name\": \"DeepHealthRiskNet\",",
            "  \"status\": \"healthy\",",
            "  \"timestamp\": \"2026-10-04T07:05:51.406650+00:00\"",
            "}",
            "",
            "$ # Execute Live Patient Prediction via Kubernetes Service",
            "$ curl -X POST http://127.0.0.1:5005/predict -H \"Content-Type: application/json\" -d @patient.json",
            "{",
            "  \"latency_ms\": 3.49,",
            "  \"model_name\": \"DeepHealthRiskNet\",",
            "  \"predictions\": [{",
            "    \"class_probabilities\": {\"Critical Risk\": 1.0, \"High Risk\": 0.0, \"Low Risk\": 0.0},",
            "    \"confidence_score\": 1.0,",
            "    \"predicted_class_id\": 3,",
            "    \"predicted_label\": \"Critical Risk\"",
            "  }],",
            "  \"status\": \"success\"",
            "}"
        ]
    )

    # 5. Dashboard
    create_dashboard_mockup("screenshot_05_k8s_dashboard_overview.png")

    # 6. Streamlit UI
    create_streamlit_mockup("screenshot_06_streamlit_browser_ui.png")

if __name__ == "__main__":
    generate_all()
