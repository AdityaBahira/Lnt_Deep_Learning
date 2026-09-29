"""
flask_api.py
------------
Flask REST API Backend for serving PyTorch Deep Learning Model (DeepHealthRiskNet).
Exposes RESTful HTTP endpoints for real-time single and batch predictions, health probes,
and interactive documentation.
"""

import time
import logging
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from model_loader import get_model_engine

# 1. Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Flask-DL-Backend")

# 2. Initialize Flask App
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.json.compact = False

# 3. Pre-load PyTorch Inference Engine on App Launch
try:
    model_engine = get_model_engine()
    logger.info("PyTorch Model Engine loaded successfully on Flask startup.")
except Exception as e:
    logger.error(f"Failed to initialize PyTorch Model Engine: {str(e)}")
    model_engine = None

def get_iso_timestamp():
    return datetime.now(timezone.utc).isoformat()

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
    return make_error_response(400, "BAD_REQUEST", str(e.description if hasattr(e, 'description') else str(e)))

@app.errorhandler(404)
def not_found_error(e):
    return make_error_response(404, "NOT_FOUND", f"Endpoint '{request.path}' not found.")

@app.errorhandler(405)
def method_not_allowed_error(e):
    return make_error_response(405, "METHOD_NOT_ALLOWED", f"Method '{request.method}' not allowed on '{request.path}'.")

@app.errorhandler(415)
def unsupported_media_type_error(e):
    return make_error_response(415, "UNSUPPORTED_MEDIA_TYPE", "Content-Type must be 'application/json'.")

@app.errorhandler(422)
def unprocessable_entity_error(e):
    return make_error_response(422, "UNPROCESSABLE_ENTITY", str(e.description if hasattr(e, 'description') else str(e)))

@app.errorhandler(500)
def internal_server_error(e):
    return make_error_response(500, "INTERNAL_SERVER_ERROR", "An unexpected internal server error occurred.")

# ----------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------
@app.route("/", methods=["GET"])
def root_endpoint():
    """API Root Landing & Metadata Endpoint."""
    return jsonify({
        "status": "success",
        "service_name": "Health Risk Deep Learning REST API",
        "version": "1.0.0",
        "framework": "Flask 3.1 & PyTorch 2.x",
        "description": "REST API exposing PyTorch DeepHealthRiskNet model for clinical risk inference.",
        "endpoints": {
            "GET /": "API Metadata",
            "GET /health": "Health and Readiness Probe",
            "POST /predict": "Neural Network Real-Time Inference Endpoint"
        },
        "timestamp": get_iso_timestamp()
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    """Health & Readiness Probe Endpoint."""
    if model_engine is None or not getattr(model_engine, "_initialized", False):
        return jsonify({
            "status": "unhealthy",
            "model_loaded": False,
            "message": "Model inference engine is uninitialized.",
            "timestamp": get_iso_timestamp()
        }), 503

    return jsonify({
        "status": "healthy",
        "model_loaded": True,
        "model_name": model_engine.config.get("model_name", "DeepHealthRiskNet"),
        "device": str(model_engine.device),
        "feature_count": model_engine.input_dim,
        "classes": list(model_engine.class_labels.values()),
        "timestamp": get_iso_timestamp()
    }), 200

@app.route("/predict", methods=["POST"])
def predict():
    """
    Main Deep Learning Prediction Endpoint.
    Accepts JSON payloads in formats:
    - {"features": [v1, v2, ..., v14]}
    - {"instances": [[v1, ...], [v2, ...]]}
    - {"data": {"age": 45, "bmi": 26.5, ...}}
    """
    start_time = time.time()

    if not request.is_json:
        return make_error_response(415, "UNSUPPORTED_MEDIA_TYPE", "Content-Type header must be 'application/json'.")

    try:
        data = request.get_json(silent=False)
    except Exception as e:
        return make_error_response(400, "MALFORMED_JSON", f"Failed to parse JSON body: {str(e)}")

    if not data or not isinstance(data, dict):
        return make_error_response(400, "INVALID_PAYLOAD", "Request payload must be a non-empty JSON object.")

    if model_engine is None or not getattr(model_engine, "_initialized", False):
        return make_error_response(500, "MODEL_NOT_AVAILABLE", "Model engine is currently offline or uninitialized.")

    instances = []

    # Format 1: {"features": [...]}
    if "features" in data:
        raw_feats = data["features"]
        if not isinstance(raw_feats, list):
            return make_error_response(422, "INVALID_FEATURE_FORMAT", "'features' must be a list of numeric values.")
        instances = [raw_feats]

    # Format 2: {"instances": [[...], [...]]}
    elif "instances" in data:
        raw_instances = data["instances"]
        if not isinstance(raw_instances, list) or len(raw_instances) == 0:
            return make_error_response(422, "INVALID_INSTANCES_FORMAT", "'instances' must be a non-empty list of feature vectors.")
        instances = raw_instances

    # Format 3: {"data": {"age": 45, ...}}
    elif "data" in data and isinstance(data["data"], dict):
        feat_dict = data["data"]
        missing_keys = [f for f in model_engine.feature_names if f not in feat_dict]
        if missing_keys:
            return make_error_response(422, "MISSING_FEATURE_KEYS", f"Missing required keys in 'data': {', '.join(missing_keys)}")
        instances = [[feat_dict[f] for f in model_engine.feature_names]]

    else:
        return make_error_response(400, "MISSING_REQUIRED_KEY", "JSON payload must contain 'features', 'instances', or 'data' dictionary.")

    # Validate numeric types
    try:
        parsed_instances = []
        for sample in instances:
            if not isinstance(sample, list):
                return make_error_response(422, "INVALID_SAMPLE_FORMAT", "Each sample must be a list of numeric feature values.")
            numeric_sample = []
            for item in sample:
                if isinstance(item, (int, float)) and not isinstance(item, bool):
                    numeric_sample.append(float(item))
                else:
                    return make_error_response(422, "NON_NUMERIC_FEATURE", f"Feature value '{item}' is non-numeric.")
            parsed_instances.append(numeric_sample)
    except Exception as e:
        return make_error_response(422, "TYPE_CASTING_ERROR", f"Error validating feature values: {str(e)}")

    # Execute PyTorch Inference
    try:
        predictions = model_engine.predict(parsed_instances)
    except ValueError as val_err:
        return make_error_response(422, "MODEL_VALIDATION_ERROR", str(val_err))
    except Exception as exec_err:
        logger.error(f"Inference execution failed: {str(exec_err)}", exc_info=True)
        return make_error_response(500, "INFERENCE_EXECUTION_ERROR", f"Error during model inference: {str(exec_err)}")

    execution_time_ms = round((time.time() - start_time) * 1000, 2)

    return jsonify({
        "status": "success",
        "predictions_count": len(predictions),
        "predictions": predictions,
        "latency_ms": execution_time_ms,
        "model_name": model_engine.config.get("model_name", "DeepHealthRiskNet"),
        "timestamp": get_iso_timestamp()
    }), 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask REST API server on http://127.0.0.1:{port} ...")
    app.run(host="0.0.0.0", port=port, debug=False)
