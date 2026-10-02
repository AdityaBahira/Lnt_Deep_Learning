import os
import time
import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

# Data directory for persistent volume testing
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "service": "Deep Learning Model Container",
        "version": "1.0.0",
        "storage_path": DATA_DIR
    })

@app.route("/predict", methods=["GET", "POST"])
def predict():
    # Simulate DL model matrix multiplication / inference
    weights = np.random.randn(5, 5)
    inputs = np.random.randn(5, 1)
    output = np.dot(weights, inputs).tolist()
    
    # Save log to volume storage if mounted
    log_file = os.path.join(DATA_DIR, "predictions.log")
    with open(log_file, "a") as f:
        f.write(f"[{time.ctime()}] Prediction performed successfully.\n")

    return jsonify({
        "status": "success",
        "input_shape": list(inputs.shape),
        "output_shape": list(output),
        "logged_to_volume": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
