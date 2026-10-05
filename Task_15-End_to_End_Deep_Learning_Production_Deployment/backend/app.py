"""
app.py
------
Task 15: Production-grade Flask REST API Microservice for Deep Learning Inference.
Serves both DeepMedVisionNet (Image Diagnostics) and DeepHealthRiskNet (Biomarker Analytics).
Integrated with Kubernetes health probes (/health), Prometheus-style metrics (/metrics),
and flexible batch/single inference endpoints.
"""

import os
import io
import time
import base64
import logging
from flask import Flask, request, jsonify, make_response
from model_loader import ProductionModelManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FlaskAPI")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max payload

# Initialize Model Manager Singleton
manager = ProductionModelManager()

# Middleware: Add CORS headers and request timing
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "DeepMed-Vision & Clinical Risk Production Inference API",
        "version": "1.0.0",
        "framework": "Flask 3.1 & PyTorch 2.14",
        "status": "online",
        "documentation": {
            "GET /health": "Cluster liveness/readiness probe & model inventory",
            "POST /predict/image": "Single radiological image inference (multipart or base64)",
            "POST /predict": "Unified multi-modal inference endpoint (image or biomarker array)",
            "POST /predict/tabular": "Clinical biomarker inference (14 features)",
            "POST /batch_predict": "Batch inference for images or patient cohorts",
            "GET /metrics": "Performance metrics, throughput & latency statistics"
        }
    }), 200

@app.route("/health", methods=["GET"])
def health():
    """
    Kubernetes Liveness & Readiness Probe.
    Returns 200 OK with system telemetry and loaded model details.
    """
    telemetry = manager.get_system_telemetry()
    status_code = 200 if (telemetry["vision_model"]["loaded"] or telemetry["tabular_model"]["loaded"]) else 503
    return jsonify(telemetry), status_code

@app.route("/predict/image", methods=["POST"])
def predict_image_endpoint():
    """Predicts diagnostic class from an uploaded medical image."""
    try:
        image_bytes = None
        # 1. Check for file upload (multipart/form-data)
        if "file" in request.files:
            uploaded_file = request.files["file"]
            if uploaded_file.filename == "":
                return jsonify({"status": "error", "message": "No file selected."}), 400
            image_bytes = uploaded_file.read()
        elif "image" in request.files:
            uploaded_file = request.files["image"]
            image_bytes = uploaded_file.read()
            
        # 2. Check for JSON with base64 image
        elif request.is_json:
            data = request.get_json()
            if "image_base64" in data:
                b64_str = data["image_base64"]
                if "," in b64_str:
                    b64_str = b64_str.split(",")[1]
                image_bytes = base64.b64decode(b64_str)
                
        if image_bytes is None or len(image_bytes) == 0:
            return jsonify({
                "status": "error",
                "message": "Missing image input. Provide multipart 'file' or JSON 'image_base64'."
            }), 400
            
        result = manager.predict_image(image_bytes)
        return jsonify({"status": "success", **result}), 200
        
    except Exception as e:
        logger.error(f"Inference error in /predict/image: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/predict/tabular", methods=["POST"])
def predict_tabular_endpoint():
    """Predicts clinical risk level from 14 physiological biomarkers."""
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"status": "error", "message": "Request payload must be valid JSON."}), 400
            
        features = data.get("features", None)
        if features is None and isinstance(data, list):
            features = data
            
        if not features or len(features) != 14:
            return jsonify({
                "status": "error",
                "message": f"Expected 'features' array of length 14, received: {len(features) if features else 0}"
            }), 400
            
        result = manager.predict_tabular(features)
        return jsonify({"status": "success", **result}), 200
        
    except Exception as e:
        logger.error(f"Inference error in /predict/tabular: {e}")
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/predict", methods=["POST"])
def unified_predict():
    """
    Unified multi-modal endpoint.
    Automatically detects whether input is an Image (multipart/file)
    or Tabular Biomarkers (JSON 'features' array).
    """
    if "file" in request.files or "image" in request.files:
        return predict_image_endpoint()
        
    if request.is_json:
        data = request.get_json(silent=True) or {}
        if "image_base64" in data:
            return predict_image_endpoint()
        elif "features" in data or isinstance(data, list):
            return predict_tabular_endpoint()
            
    return jsonify({
        "status": "error",
        "message": "Unrecognized request format. Submit image file or 14 biomarker features."
    }), 400

@app.route("/batch_predict", methods=["POST"])
def batch_predict():
    """Executes bulk inference over multiple items."""
    t0 = time.time()
    try:
        # Batch images (multipart multiple files)
        if "files" in request.files or len(request.files) > 1:
            files_list = request.files.getlist("files") or list(request.files.values())
            results = []
            for f in files_list:
                b = f.read()
                try:
                    res = manager.predict_image(b)
                    results.append({"filename": f.filename, "status": "success", **res})
                except Exception as ex:
                    results.append({"filename": f.filename, "status": "error", "message": str(ex)})
            return jsonify({
                "status": "success",
                "batch_size": len(results),
                "total_batch_latency_ms": round((time.time() - t0) * 1000.0, 2),
                "results": results
            }), 200
            
        # Batch tabular cohorts
        if request.is_json:
            data = request.get_json()
            cohort = data.get("cohort", [])
            results = []
            for item in cohort:
                feats = item if isinstance(item, list) else item.get("features", [])
                try:
                    res = manager.predict_tabular(feats)
                    results.append({"status": "success", **res})
                except Exception as ex:
                    results.append({"status": "error", "message": str(ex)})
            return jsonify({
                "status": "success",
                "batch_size": len(results),
                "total_batch_latency_ms": round((time.time() - t0) * 1000.0, 2),
                "results": results
            }), 200
            
        return jsonify({"status": "error", "message": "No batch files or cohort JSON provided."}), 400
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/metrics", methods=["GET"])
def metrics():
    """Prometheus-compatible and JSON operational metrics."""
    telemetry = manager.get_system_telemetry()
    return jsonify(telemetry["telemetry"]), 200

# Error Handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"status": "error", "error_code": 400, "message": "Bad Request: " + str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "error_code": 404, "message": "Endpoint not found."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"status": "error", "error_code": 405, "message": "Method Not Allowed."}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "error_code": 500, "message": "Internal Server Error."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Production Flask API on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
