"""
model_loader.py
---------------
Model Inference Engine for PyTorch Deep Learning Model.
Handles model loading, pre-processing (scaling), tensor transformation,
forward pass inference, softmax probability generation, and output formatting.
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn

# Re-define Neural Network Architecture matching train_and_save_model.py
class DeepHealthRiskNet(nn.Module):
    def __init__(self, input_dim=8, num_classes=4):
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

class ModelInferenceEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ModelInferenceEngine, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_dir=None):
        if self._initialized:
            return

        if model_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(base_dir, "saved_models")

        self.model_path = os.path.join(model_dir, "dl_model.pt")
        self.config_path = os.path.join(model_dir, "config.json")

        if not os.path.exists(self.model_path) or not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Model artifacts not found in {model_dir}. Please run train_and_save_model.py first.")

        # Load Metadata Configuration
        with open(self.config_path, "r") as f:
            self.config = json.load(f)

        self.input_dim = self.config["input_dim"]
        self.num_classes = self.config["num_classes"]
        self.feature_names = self.config["feature_names"]
        self.class_labels = self.config["class_labels"]
        self.mean = np.array(self.config["mean"], dtype=np.float32)
        self.std = np.array(self.config["std"], dtype=np.float32)

        # Initialize and Load PyTorch Model
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DeepHealthRiskNet(input_dim=self.input_dim, num_classes=self.num_classes)
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()

        self._initialized = True
        print(f"[ModelInferenceEngine] Successfully loaded {self.config['model_name']} on device: {self.device}")

    def predict(self, raw_instances):
        """
        Accepts raw feature vector(s) as list or numpy array.
        Returns list of prediction dictionaries.
        """
        if not isinstance(raw_instances, (list, np.ndarray)):
            raise ValueError("Input data must be a list of feature lists or a 2D array.")

        arr = np.array(raw_instances, dtype=np.float32)

        # Allow single 1D vector conversion to 2D
        if arr.ndim == 1:
            arr = np.expand_dims(arr, axis=0)

        if arr.ndim != 2:
            raise ValueError(f"Input data must be 2-dimensional [batch_size, {self.input_dim}], got {arr.ndim} dimensions.")

        if arr.shape[1] != self.input_dim:
            raise ValueError(f"Expected {self.input_dim} features per sample ({', '.join(self.feature_names)}), but got {arr.shape[1]} features.")

        if np.isnan(arr).any() or np.isinf(arr).any():
            raise ValueError("Input data contains invalid numerical values (NaN or Inf).")

        # Standardize features
        scaled_arr = (arr - self.mean) / self.std

        # Convert to PyTorch Tensor
        input_tensor = torch.tensor(scaled_arr, dtype=torch.float32).to(self.device)

        # Run Inference
        with torch.no_grad():
            logits = self.model(input_tensor)
            probabilities = torch.softmax(logits, dim=1).cpu().numpy()
            predicted_classes = np.argmax(probabilities, axis=1)

        results = []
        for i in range(len(arr)):
            pred_class_id = str(int(predicted_classes[i]))
            class_name = self.class_labels.get(pred_class_id, f"Class_{pred_class_id}")
            confidence = float(probabilities[i][int(pred_class_id)])

            all_probs = {
                self.class_labels.get(str(c), f"Class_{c}"): float(probabilities[i][c])
                for c in range(self.num_classes)
            }

            results.append({
                "sample_index": i,
                "input_features": {name: float(val) for name, val in zip(self.feature_names, arr[i])},
                "predicted_class_id": int(pred_class_id),
                "predicted_label": class_name,
                "confidence_score": round(confidence, 4),
                "class_probabilities": {k: round(v, 4) for k, v in all_probs.items()}
            })

        return results

# Singleton accessor function
def get_model_engine():
    return ModelInferenceEngine()
