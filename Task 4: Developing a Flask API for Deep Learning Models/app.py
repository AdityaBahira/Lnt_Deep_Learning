"""
app.py
------
Production-ready Flask REST API service for serving PyTorch Deep Learning Models.
Includes endpoints for API status, health metrics, model inference, interactive docs,
and structured HTTP exception handling.
"""

import time
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string
from model_loader import get_model_engine

# 1. Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("api_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Flask-DL-API")

# 2. Initialize Flask App
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# 3. Pre-load PyTorch Inference Engine on App Launch
try:
    model_engine = get_model_engine()
    logger.info("Deep Learning Model loaded successfully during app startup.")
except Exception as e:
    logger.error(f"Failed to load model during startup: {str(e)}")
    model_engine = None

# Helper function for standardized timestamp
def get_iso_timestamp():
    return datetime.now(timezone.utc).isoformat()

# Helper function for error responses
def make_error_response(status_code, error_code, message):
    return jsonify({
        "status": "error",
        "error_code": error_code,
        "message": message,
        "timestamp": get_iso_timestamp()
    }), status_code

# ----------------------------------------------------
# HTTP ERROR HANDLERS
# ----------------------------------------------------
@app.errorhandler(400)
def bad_request_error(e):
    logger.warning(f"HTTP 400 Bad Request: {str(e)}")
    return make_error_response(400, "BAD_REQUEST", str(e.description if hasattr(e, 'description') else str(e)))

@app.errorhandler(404)
def not_found_error(e):
    logger.warning(f"HTTP 404 Not Found: {request.path}")
    return make_error_response(404, "NOT_FOUND", f"The requested URL '{request.path}' was not found on this server.")

@app.errorhandler(405)
def method_not_allowed_error(e):
    logger.warning(f"HTTP 405 Method Not Allowed: {request.method} on {request.path}")
    return make_error_response(405, "METHOD_NOT_ALLOWED", f"The method {request.method} is not allowed for URL '{request.path}'.")

@app.errorhandler(415)
def unsupported_media_type_error(e):
    logger.warning(f"HTTP 415 Unsupported Media Type: Content-Type={request.content_type}")
    return make_error_response(415, "UNSUPPORTED_MEDIA_TYPE", "Content-Type header must be 'application/json'.")

@app.errorhandler(422)
def unprocessable_entity_error(e):
    logger.warning(f"HTTP 422 Unprocessable Entity: {str(e)}")
    return make_error_response(422, "UNPROCESSABLE_ENTITY", str(e.description if hasattr(e, 'description') else str(e)))

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"HTTP 500 Internal Server Error: {str(e)}", exc_info=True)
    return make_error_response(500, "INTERNAL_SERVER_ERROR", "An unexpected internal server error occurred while processing the request.")

# ----------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------

@app.route("/", methods=["GET"])
def root_endpoint():
    """API Landing & Metadata Endpoint"""
    return jsonify({
        "status": "success",
        "service_name": "Health Risk Deep Learning REST API",
        "version": "1.0.0",
        "framework": "Flask 3.1 & PyTorch 2.12",
        "description": "REST API exposing a trained PyTorch Deep Neural Network for clinical risk prediction.",
        "endpoints": {
            "GET /": "API Landing and System Info",
            "GET /health": "Server and Model Health Status",
            "POST /predict": "Deep Learning Inference Endpoint",
            "GET /docs": "Interactive HTML Documentation"
        },
        "timestamp": get_iso_timestamp()
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    """Health & Readiness Probe Endpoint"""
    if model_engine is None or not model_engine._initialized:
        return jsonify({
            "status": "unhealthy",
            "model_loaded": False,
            "message": "Model inference engine is not initialized.",
            "timestamp": get_iso_timestamp()
        }), 503

    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "model_name": model_engine.config["model_name"],
        "device": str(model_engine.device),
        "feature_count": model_engine.input_dim,
        "classes": model_engine.class_labels,
        "timestamp": get_iso_timestamp()
    }), 200

@app.route("/predict", methods=["POST"])
def predict():
    """
    Main Deep Learning Prediction Endpoint.
    Accepts JSON input payloads and returns predictions with confidence scores.
    """
    start_time = time.time()

    # 1. Enforce Content-Type Header
    if not request.is_json:
        return make_error_response(415, "UNSUPPORTED_MEDIA_TYPE", "Content-Type must be 'application/json'.")

    # 2. Extract JSON Body
    try:
        data = request.get_json(silent=False)
    except Exception as e:
        return make_error_response(400, "MALFORMED_JSON", f"Failed to parse JSON body: {str(e)}")

    if not data or not isinstance(data, dict):
        return make_error_response(400, "INVALID_PAYLOAD", "Request body must be a non-empty JSON object.")

    # 3. Check Model Health
    if model_engine is None or not model_engine._initialized:
        return make_error_response(500, "MODEL_NOT_AVAILABLE", "Model engine is currently unavailable.")

    # 4. Extract Input Instances
    instances = []
    
    # Payload Pattern A: {"features": [v1, v2, ...]}
    if "features" in data:
        raw_feats = data["features"]
        if not isinstance(raw_feats, list):
            return make_error_response(422, "INVALID_FEATURE_FORMAT", "'features' field must be a list of numerical values.")
        instances = [raw_feats]

    # Payload Pattern B: {"instances": [[v1, v2, ...], [v1, v2, ...]]}
    elif "instances" in data:
        raw_instances = data["instances"]
        if not isinstance(raw_instances, list) or len(raw_instances) == 0:
            return make_error_response(422, "INVALID_INSTANCES_FORMAT", "'instances' must be a non-empty list of feature vectors.")
        instances = raw_instances

    # Payload Pattern C: {"data": {"age": 45, "bmi": 26.5, ...}}
    elif "data" in data and isinstance(data["data"], dict):
        feat_dict = data["data"]
        missing_keys = [f for f in model_engine.feature_names if f not in feat_dict]
        if missing_keys:
            return make_error_response(422, "MISSING_FEATURE_KEYS", f"Missing required feature keys in 'data': {', '.join(missing_keys)}")
        vec = [feat_dict[f] for f in model_engine.feature_names]
        instances = [vec]

    else:
        return make_error_response(400, "MISSING_REQUIRED_KEY", "JSON payload must contain 'features', 'instances', or 'data' dictionary.")

    # 5. Parse and Validate Numerical Values
    try:
        parsed_instances = []
        for sample in instances:
            if not isinstance(sample, list):
                return make_error_response(422, "INVALID_SAMPLE_FORMAT", "Each sample inside instances must be a list of numerical values.")
            numeric_sample = []
            for item in sample:
                if isinstance(item, (int, float)) and not isinstance(item, bool):
                    numeric_sample.append(float(item))
                else:
                    return make_error_response(422, "NON_NUMERIC_FEATURE", f"Feature value '{item}' is non-numeric. All inputs must be numbers.")
            parsed_instances.append(numeric_sample)
    except Exception as e:
        return make_error_response(422, "TYPE_CASTING_ERROR", f"Error validating feature values: {str(e)}")

    # 6. Execute Deep Learning Model Inference
    try:
        predictions = model_engine.predict(parsed_instances)
    except ValueError as val_err:
        return make_error_response(422, "MODEL_VALIDATION_ERROR", str(val_err))
    except Exception as exec_err:
        logger.error(f"Inference execution failed: {str(exec_err)}", exc_info=True)
        return make_error_response(500, "INFERENCE_EXECUTION_ERROR", f"An internal error occurred during neural network inference: {str(exec_err)}")

    execution_time_ms = round((time.time() - start_time) * 1000, 2)

    # 7. Format Successful JSON Response
    return jsonify({
        "status": "success",
        "predictions_count": len(predictions),
        "predictions": predictions,
        "latency_ms": execution_time_ms,
        "model_name": model_engine.config["model_name"],
        "timestamp": get_iso_timestamp()
    }), 200

# ----------------------------------------------------
# INTERACTIVE DOCUMENTATION ROUTE
# ----------------------------------------------------
HTML_DOCS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Risk Deep Learning REST API - Documentation</title>
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --code-bg: #090d16;
            --success: #22c55e;
            --error: #ef4444;
        }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 30px;
            line-height: 1.6;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }
        header {
            border-bottom: 1px solid #334155;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        h1 { color: var(--accent); font-size: 2.2rem; margin-bottom: 8px; }
        .badge {
            display: inline-block;
            background: #1e3a8a;
            color: #93c5fd;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid #334155;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);
        }
        h2 { color: #f1f5f9; font-size: 1.4rem; margin-top: 0; }
        .method {
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.9rem;
            margin-right: 10px;
        }
        .method.get { background: #166534; color: #86efac; }
        .method.post { background: #1e40af; color: #93c5fd; }
        pre {
            background: var(--code-bg);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            color: #e2e8f0;
            border: 1px solid #1e293b;
        }
        code { font-family: 'Consolas', 'Courier New', monospace; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
        }
        th, td {
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #334155;
        }
        th { color: var(--accent); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Health Risk Deep Learning REST API</h1>
            <span class="badge">Flask 3.1</span>
            <span class="badge">PyTorch 2.12</span>
            <span class="badge">Status: Production Active</span>
            <p style="color: var(--text-muted); margin-top: 12px;">
                Interactive API reference documentation for the trained PyTorch Deep Neural Network prediction endpoints.
            </p>
        </header>

        <div class="card">
            <h2>Endpoints Overview</h2>
            <table>
                <thead>
                    <tr><th>Method</th><th>Endpoint</th><th>Description</th></tr>
                </thead>
                <tbody>
                    <tr><td><span class="method get">GET</span></td><td><code>/</code></td><td>API Root Info & Status</td></tr>
                    <tr><td><span class="method get">GET</span></td><td><code>/health</code></td><td>Health Readiness Probe & Model Metadata</td></tr>
                    <tr><td><span class="method post">POST</span></td><td><code>/predict</code></td><td>Deep Learning Inference Endpoint</td></tr>
                    <tr><td><span class="method get">GET</span></td><td><code>/docs</code></td><td>API Interactive Documentation (This page)</td></tr>
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>POST /predict - Sample Request (Single Instance)</h2>
            <pre><code>curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [55.0, 29.4, 135.0, 140.0, 240.0, 82.0, 2.5, 6.0]
  }'</code></pre>
        </div>

        <div class="card">
            <h2>POST /predict - Sample Response</h2>
            <pre><code>{
    "status": "success",
    "predictions_count": 1,
    "predictions": [
        {
            "sample_index": 0,
            "input_features": {
                "age": 55.0,
                "bmi": 29.4,
                "blood_pressure": 135.0,
                "glucose_level": 140.0,
                "cholesterol": 240.0,
                "heart_rate": 82.0,
                "physical_activity_hours": 2.5,
                "sleep_hours": 6.0
            },
            "predicted_class_id": 2,
            "predicted_label": "High Risk",
            "confidence_score": 0.8942,
            "class_probabilities": {
                "Low Risk": 0.0105,
                "Moderate Risk": 0.0821,
                "High Risk": 0.8942,
                "Critical Risk": 0.0132
            }
        }
    ],
    "latency_ms": 2.45,
    "model_name": "DeepHealthRiskNet",
    "timestamp": "2026-09-13T09:47:00Z"
}</code></pre>
        </div>
    </div>
</body>
</html>
"""

@app.route("/docs", methods=["GET"])
def api_documentation_page():
    """Interactive HTML Documentation Page"""
    return render_template_string(HTML_DOCS_TEMPLATE), 200

if __name__ == "__main__":
    print("Starting Flask REST API Server on http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
