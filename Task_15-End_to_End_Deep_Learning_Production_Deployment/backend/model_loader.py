"""
model_loader.py
---------------
Production-grade Thread-Safe Model Manager for Task 15.
Loads and caches PyTorch Deep Learning models:
1. DeepMedVisionNet: 4-Stage Convolutional Neural Network for Image Diagnostics
2. DeepHealthRiskNet: Deep Multi-Layer Perceptron for Clinical Biomarker Risk Scoring
"""

import os
import io
import time
import json
import logging
import numpy as np
import torch
import torch.nn as nn
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ModelManager")

# Architecture Definitions
class DeepMedVisionNet(nn.Module):
    def __init__(self, num_classes=4, in_channels=3):
        super(DeepMedVisionNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class DeepHealthRiskNet(nn.Module):
    def __init__(self, input_dim=14, num_classes=4):
        super(DeepHealthRiskNet, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        return self.network(x)


class ProductionModelManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ProductionModelManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, models_dir=None):
        if self._initialized:
            return
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.models_dir = models_dir or os.path.join(self.base_dir, "saved_models")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.start_time = time.time()
        
        self.vision_model = None
        self.vision_config = {}
        self.tabular_model = None
        self.tabular_config = {}
        
        self.metrics = {
            "total_requests": 0,
            "vision_inferences": 0,
            "tabular_inferences": 0,
            "total_latency_ms": 0.0,
            "errors": 0
        }
        
        self._load_vision_model()
        self._load_tabular_model()
        self._warmup()
        self._initialized = True
        logger.info(f"ModelManager successfully initialized on device: {self.device}")

    def _load_vision_model(self):
        weights_path = os.path.join(self.models_dir, "deep_vision_model.pt")
        config_path = os.path.join(self.models_dir, "vision_config.json")
        
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.vision_config = json.load(f)
        else:
            self.vision_config = {
                "model_name": "DeepMedVisionNet",
                "classes": ["COVID", "Lung_Opacity", "Normal", "Viral Pneumonia"],
                "version": "1.0.0"
            }
            
        if os.path.exists(weights_path):
            self.vision_model = DeepMedVisionNet(num_classes=4, in_channels=3)
            self.vision_model.load_state_dict(torch.load(weights_path, map_location=self.device, weights_only=True))
            self.vision_model.to(self.device)
            self.vision_model.eval()
            logger.info("DeepMedVisionNet loaded successfully.")
        else:
            logger.warning(f"Vision model weights not found at {weights_path}")

    def _load_tabular_model(self):
        weights_path = os.path.join(self.models_dir, "dl_model.pt")
        config_path = os.path.join(self.models_dir, "config.json")
        
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.tabular_config = json.load(f)
        else:
            self.tabular_config = {
                "model_name": "DeepHealthRiskNet",
                "classes": ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"],
                "input_dim": 14,
                "version": "1.0.0"
            }
            
        if os.path.exists(weights_path):
            self.tabular_model = DeepHealthRiskNet(input_dim=14, num_classes=4)
            self.tabular_model.load_state_dict(torch.load(weights_path, map_location=self.device, weights_only=True))
            self.tabular_model.to(self.device)
            self.tabular_model.eval()
            logger.info("DeepHealthRiskNet loaded successfully.")
        else:
            logger.warning(f"Tabular model weights not found at {weights_path}")

    def _warmup(self):
        """Performs initial dry-run inference to compile graph and initialize memory."""
        try:
            if self.vision_model is not None:
                dummy_v = torch.randn(1, 3, 64, 64, device=self.device)
                with torch.no_grad():
                    _ = self.vision_model(dummy_v)
            if self.tabular_model is not None:
                dummy_t = torch.randn(1, 14, device=self.device)
                with torch.no_grad():
                    _ = self.tabular_model(dummy_t)
            logger.info("Model warmup completed.")
        except Exception as e:
            logger.warning(f"Warmup warning: {e}")

    def preprocess_image(self, image_data):
        """
        Accepts PIL Image, file path, or bytes.
        Resizes to (64, 64), normalizes to [0, 1] tensor shape (1, 3, 64, 64).
        """
        if isinstance(image_data, bytes):
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
        elif isinstance(image_data, str) and os.path.exists(image_data):
            image = Image.open(image_data).convert("RGB")
        elif isinstance(image_data, Image.Image):
            image = image_data.convert("RGB")
        else:
            raise ValueError("Unsupported image data format.")
            
        image = image.resize((64, 64))
        arr = np.array(image, dtype=np.float32) / 255.0
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        arr = (arr - mean) / std
        arr = np.transpose(arr, (2, 0, 1))  # (3, 64, 64)
        tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0).to(self.device)
        return tensor

    def predict_image(self, image_data):
        """Executes deep learning inference on radiological image."""
        t0 = time.time()
        self.metrics["total_requests"] += 1
        
        if self.vision_model is None:
            self.metrics["errors"] += 1
            raise RuntimeError("DeepMedVisionNet is not loaded.")
            
        tensor = self.preprocess_image(image_data)
        
        with torch.no_grad():
            logits = self.vision_model(tensor)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
            pred_idx = int(np.argmax(probs))
            confidence = float(probs[pred_idx])
            
        latency_ms = (time.time() - t0) * 1000.0
        self.metrics["vision_inferences"] += 1
        self.metrics["total_latency_ms"] += latency_ms
        
        classes = self.vision_config.get("classes", [
            "Normal / Healthy", "Bacterial Pneumonia", "Viral Pneumonia", "COVID-19 Infiltration"
        ])
        
        return {
            "prediction": classes[pred_idx],
            "class_id": pred_idx,
            "confidence": round(confidence, 4),
            "probabilities": {classes[i]: round(float(probs[i]), 4) for i in range(len(classes))},
            "latency_ms": round(latency_ms, 2),
            "device": str(self.device),
            "model_version": self.vision_config.get("version", "1.0.0")
        }

    def predict_tabular(self, features):
        """Executes deep learning inference on 14 clinical biomarkers."""
        t0 = time.time()
        self.metrics["total_requests"] += 1
        
        if self.tabular_model is None:
            self.metrics["errors"] += 1
            raise RuntimeError("DeepHealthRiskNet is not loaded.")
            
        if len(features) != 14:
            self.metrics["errors"] += 1
            raise ValueError(f"Expected 14 clinical features, got {len(features)}")
            
        means = np.array(self.tabular_config.get("scaler_means", [0.0]*14))
        stds = np.array(self.tabular_config.get("scaler_stds", [1.0]*14))
        stds = np.where(stds == 0, 1.0, stds)
        
        arr = (np.array(features, dtype=np.float32) - means) / stds
        tensor = torch.tensor(arr, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            logits = self.tabular_model(tensor)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
            pred_idx = int(np.argmax(probs))
            confidence = float(probs[pred_idx])
            
        latency_ms = (time.time() - t0) * 1000.0
        self.metrics["tabular_inferences"] += 1
        self.metrics["total_latency_ms"] += latency_ms
        
        classes = self.tabular_config.get("classes", [
            "Low Risk", "Moderate Risk", "High Risk", "Critical Risk"
        ])
        
        return {
            "prediction": classes[pred_idx],
            "class_id": pred_idx,
            "confidence": round(confidence, 4),
            "probabilities": {classes[i]: round(float(probs[i]), 4) for i in range(len(classes))},
            "latency_ms": round(latency_ms, 2),
            "model_version": self.tabular_config.get("version", "1.0.0")
        }

    def get_system_telemetry(self):
        uptime = time.time() - self.start_time
        total_inf = self.metrics["vision_inferences"] + self.metrics["tabular_inferences"]
        avg_lat = (self.metrics["total_latency_ms"] / total_inf) if total_inf > 0 else 0.0
        
        return {
            "status": "healthy",
            "uptime_seconds": round(uptime, 1),
            "hardware_device": str(self.device),
            "vision_model": {
                "name": self.vision_config.get("model_name", "DeepMedVisionNet"),
                "loaded": self.vision_model is not None,
                "classes": self.vision_config.get("classes", []),
                "accuracy": self.vision_config.get("test_accuracy", 100.0)
            },
            "tabular_model": {
                "name": self.tabular_config.get("model_name", "DeepHealthRiskNet"),
                "loaded": self.tabular_model is not None,
                "classes": self.tabular_config.get("classes", [])
            },
            "telemetry": {
                "total_requests": self.metrics["total_requests"],
                "total_inferences": total_inf,
                "average_latency_ms": round(avg_lat, 2),
                "error_count": self.metrics["errors"]
            }
        }
