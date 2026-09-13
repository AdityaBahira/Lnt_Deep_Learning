"""
train_and_save_model.py
-----------------------
Trains a multi-layer Deep Neural Network using PyTorch for Health Risk Classification
and serializes the model weights, metadata, and feature normalization metrics.
"""

import os
import json
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Set random seeds for reproducibility
np.random.seed(42)
torch.manual_seed(42)

# Define Directory Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "dl_model.pt")
CONFIG_PATH = os.path.join(MODEL_DIR, "config.json")

# 1. Define PyTorch Neural Network Architecture
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

# 2. Synthetic Dataset Generator
def generate_dataset(num_samples=2500):
    """
    Generates synthetic clinical dataset with 8 numerical features:
    0: Age (18 - 85)
    1: BMI (16.0 - 42.0)
    2: Blood Pressure (90 - 180)
    3: Glucose Level (70 - 240)
    4: Cholesterol (130 - 320)
    5: Heart Rate (55 - 110)
    6: Activity Hours per week (0 - 15)
    7: Sleep Hours per day (4 - 10)
    """
    age = np.random.uniform(18, 85, num_samples)
    bmi = np.random.uniform(16.0, 42.0, num_samples)
    bp = np.random.uniform(90, 180, num_samples)
    glucose = np.random.uniform(70, 240, num_samples)
    chol = np.random.uniform(130, 320, num_samples)
    hr = np.random.uniform(55, 110, num_samples)
    activity = np.random.uniform(0, 15, num_samples)
    sleep = np.random.uniform(4, 10, num_samples)

    X = np.column_stack([age, bmi, bp, glucose, chol, hr, activity, sleep])

    # Rule-based synthetic target calculation with soft noise
    risk_score = (
        0.02 * age + 
        0.05 * (bmi - 22) + 
        0.03 * (bp - 120) + 
        0.04 * (glucose - 100) + 
        0.02 * (chol - 200) + 
        0.01 * (hr - 70) - 
        0.08 * activity - 
        0.05 * sleep + 
        np.random.normal(0, 0.5, num_samples)
    )

    # Class assignment based on quantiles
    y = np.zeros(num_samples, dtype=np.int64)
    q33, q66, q90 = np.percentile(risk_score, [33, 66, 90])
    y[risk_score >= q33] = 1 # Moderate Risk
    y[risk_score >= q66] = 2 # High Risk
    y[risk_score >= q90] = 3 # Critical Risk

    return X, y

# 3. Model Training Function
def train_and_export():
    print("Generating training dataset...")
    X_raw, y_raw = generate_dataset(3000)

    # Compute Feature Normalization Statistics (Mean & Std)
    mean = np.mean(X_raw, axis=0)
    std = np.std(X_raw, axis=0) + 1e-8 # avoid div by zero
    X_scaled = (X_raw - mean) / std

    # Train/Val Split
    split_idx = int(0.8 * len(X_scaled))
    X_train, X_val = X_scaled[:split_idx], X_scaled[split_idx:]
    y_train, y_val = y_raw[:split_idx], y_raw[split_idx:]

    train_dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    val_dataset = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.long))

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)

    model = DeepHealthRiskNet(input_dim=8, num_classes=4)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)

    print("Training PyTorch Deep Learning Model...")
    epochs = 40
    for epoch in range(1, epochs + 1):
        model.train()
        total_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * batch_x.size(0)

        # Validation evaluation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for val_x, val_y in val_loader:
                preds = model(val_x)
                _, predicted = torch.max(preds, 1)
                total += val_y.size(0)
                correct += (predicted == val_y).sum().item()

        acc = (correct / total) * 100
        if epoch % 10 == 0 or epoch == epochs:
            avg_loss = total_loss / len(train_dataset)
            print(f"Epoch [{epoch:02d}/{epochs:02d}] - Train Loss: {avg_loss:.4f} | Val Accuracy: {acc:.2f}%")

    # 4. Save Model Weights & TorchScript/StateDict
    torch.save(model.state_dict(), MODEL_PATH)
    print(f"Model saved successfully to: {MODEL_PATH}")

    # 5. Export Configuration Metadata
    class_labels = {
        "0": "Low Risk",
        "1": "Moderate Risk",
        "2": "High Risk",
        "3": "Critical Risk"
    }

    feature_names = [
        "age", "bmi", "blood_pressure", "glucose_level", 
        "cholesterol", "heart_rate", "physical_activity_hours", "sleep_hours"
    ]

    config_data = {
        "model_name": "DeepHealthRiskNet",
        "input_dim": 8,
        "num_classes": 4,
        "feature_names": feature_names,
        "class_labels": class_labels,
        "mean": mean.tolist(),
        "std": std.tolist(),
        "training_epochs": epochs,
        "framework": "PyTorch 2.12"
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config_data, f, indent=4)
    print(f"Configuration metadata saved to: {CONFIG_PATH}")

if __name__ == "__main__":
    train_and_export()
