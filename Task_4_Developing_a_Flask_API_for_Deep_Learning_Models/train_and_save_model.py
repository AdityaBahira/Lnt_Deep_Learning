"""
train_and_save_model.py
-----------------------
Trains a PyTorch Deep Neural Network (DeepHealthRiskNet) on the real 1,000-row
clinical health dataset using a Multi-Condition Health Risk Score target.
Serializes model weights, metadata, feature scaling stats, and class labels.
"""

import os
import json
import csv
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

# Dataset File Location
DATASET_PATH = os.path.join(BASE_DIR, "health_activity_data.csv")

# 1. Define PyTorch Neural Network Architecture
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

# 2. Data Preprocessing & Multi-Condition Risk Label Calculation
def load_and_preprocess_dataset(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")

    raw_features = []
    risk_scores = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            age = float(row['Age'])
            height = float(row['Height_cm'])
            weight = float(row['Weight_kg'])
            bmi = float(row['BMI'])
            steps = float(row['Daily_Steps'])
            calories = float(row['Calories_Intake'])
            sleep = float(row['Hours_of_Sleep'])
            hr = float(row['Heart_Rate'])
            
            bp_parts = row['Blood_Pressure'].split('/')
            systolic_bp = float(bp_parts[0])
            diastolic_bp = float(bp_parts[1])

            exercise = float(row['Exercise_Hours_per_Week'])
            alcohol = float(row['Alcohol_Consumption_per_Week'])
            smoker = 1.0 if row['Smoker'].strip().lower() == 'yes' else 0.0
            diabetic = 1.0 if row['Diabetic'].strip().lower() == 'yes' else 0.0
            heart_disease = 1.0 if row['Heart_Disease'].strip().lower() == 'yes' else 0.0

            # Feature Vector (14 numerical inputs)
            feat_vec = [
                age, height, weight, bmi, steps, calories, sleep,
                hr, systolic_bp, diastolic_bp, exercise, alcohol, smoker, diabetic
            ]
            raw_features.append(feat_vec)

            # Multi-Condition Clinical Health Risk Score calculation
            score = (
                0.03 * age +
                0.04 * (systolic_bp - 120.0) +
                0.02 * (diastolic_bp - 80.0) +
                0.05 * (bmi - 22.0) +
                0.02 * (hr - 70.0) +
                1.5 * smoker +
                1.8 * diabetic +
                2.2 * heart_disease +
                0.15 * alcohol -
                0.10 * exercise -
                0.0001 * steps
            )
            risk_scores.append(score)

    X = np.array(raw_features, dtype=np.float32)
    scores = np.array(risk_scores, dtype=np.float32)

    # Class assignment based on Risk Score Quantiles
    q25, q50, q75 = np.percentile(scores, [25, 50, 75])
    y = np.zeros(len(scores), dtype=np.int64)
    y[scores >= q25] = 1 # Moderate Risk
    y[scores >= q50] = 2 # High Risk
    y[scores >= q75] = 3 # Critical Risk

    return X, y

# 3. Model Training & Export Function
def train_and_export():
    print(f"Loading and preprocessing dataset from: {DATASET_PATH}")
    X_raw, y_raw = load_and_preprocess_dataset(DATASET_PATH)

    print(f"Dataset shape: {X_raw.shape} | Target samples count: {len(y_raw)}")
    print(f"Class distribution: Low Risk (0): {(y_raw==0).sum()}, Moderate Risk (1): {(y_raw==1).sum()}, High Risk (2): {(y_raw==2).sum()}, Critical Risk (3): {(y_raw==3).sum()}")

    feature_names = [
        "age", "height_cm", "weight_kg", "bmi", "daily_steps",
        "calories_intake", "hours_of_sleep", "heart_rate",
        "systolic_bp", "diastolic_bp", "exercise_hours_per_week",
        "alcohol_consumption_per_week", "smoker", "diabetic"
    ]

    # Compute Feature Normalization Statistics (Mean & Std)
    mean = np.mean(X_raw, axis=0)
    std = np.std(X_raw, axis=0) + 1e-8 # avoid div by zero
    X_scaled = (X_raw - mean) / std

    # Train/Val Split (80% Train, 20% Validation)
    split_idx = int(0.8 * len(X_scaled))
    X_train, X_val = X_scaled[:split_idx], X_scaled[split_idx:]
    y_train, y_val = y_raw[:split_idx], y_raw[split_idx:]

    train_dataset = TensorDataset(torch.tensor(X_train, dtype=torch.float32), torch.tensor(y_train, dtype=torch.long))
    val_dataset = TensorDataset(torch.tensor(X_val, dtype=torch.float32), torch.tensor(y_val, dtype=torch.long))

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

    model = DeepHealthRiskNet(input_dim=14, num_classes=4)
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

    # 4. Save Model State Dict & Metadata Config JSON
    torch.save(model.state_dict(), MODEL_PATH)

    config_data = {
        "model_name": "DeepHealthRiskNet",
        "input_dim": 14,
        "num_classes": 4,
        "feature_names": feature_names,
        "class_labels": {
            "0": "Low Risk",
            "1": "Moderate Risk",
            "2": "High Risk",
            "3": "Critical Risk"
        },
        "mean": mean.tolist(),
        "std": std.tolist(),
        "training_epochs": epochs,
        "framework": "PyTorch 2.12"
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config_data, f, indent=4)

    print(f"Model state saved successfully to: {MODEL_PATH}")
    print(f"Config metadata exported successfully to: {CONFIG_PATH}")

if __name__ == "__main__":
    train_and_export()
