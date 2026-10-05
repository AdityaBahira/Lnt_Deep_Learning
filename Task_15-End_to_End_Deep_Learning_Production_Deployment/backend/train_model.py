"""
train_model.py
--------------
End-to-End Deep Learning Training Pipeline for Task 15.
Trains DeepMedVisionNet directly on the real Kaggle COVID-19 Radiography Dataset:
(COVID, Lung_Opacity, Normal, Viral Pneumonia) across real patient chest X-rays.

Outputs:
- Serialized PyTorch models (.pt) and architecture configs (.json)
- Real clinical diagnostic images in sample_data/ for live inference testing
- Model evaluation curves (Loss, Accuracy, Confusion Matrix) saved to screenshots/
"""

import os
import sys
import json
import glob
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set reproducibility seeds
np.random.seed(42)
torch.manual_seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "COVID-19_Radiography_Dataset")
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
SAMPLE_DATA_DIR = os.path.join(PROJECT_DIR, "sample_data")
SCREENSHOTS_DIR = os.path.join(PROJECT_DIR, "screenshots")

os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
os.makedirs(SAMPLE_DATA_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

CLASS_NAMES = ["COVID", "Lung_Opacity", "Normal", "Viral Pneumonia"]
CLASS_LABELS_MAP = {
    "COVID": "COVID-19 Infiltration",
    "Lung_Opacity": "Lung Opacity / Bacterial",
    "Normal": "Normal / Healthy",
    "Viral Pneumonia": "Viral Pneumonia"
}
IMG_SIZE = 64

# ==============================================================================
# 1. PyTorch Neural Network Architecture
# ==============================================================================
class DeepMedVisionNet(nn.Module):
    """
    Production Deep Convolutional Neural Network for multi-class image diagnostics.
    Incorporates 4 convolutional blocks with Batch Normalization, Max Pooling,
    Adaptive Average Pooling, and Dropout for robust regularization.
    """
    def __init__(self, num_classes=4, in_channels=3):
        super(DeepMedVisionNet, self).__init__()
        self.features = nn.Sequential(
            # Block 1: 3 -> 32
            nn.Conv2d(in_channels, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 64 -> 32
            
            # Block 2: 32 -> 64
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 32 -> 16
            
            # Block 3: 64 -> 128
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),  # 16 -> 8
            
            # Block 4: 128 -> 256
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((4, 4))            # Fixed 4x4 spatial grid
        )
        
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 4 * 4, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.35),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.25),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        feat = self.features(x)
        logits = self.classifier(feat)
        return logits


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

# ==============================================================================
# 2. Real Kaggle Dataset Ingestion & Loader
# ==============================================================================
class RealRadiographyDataset(Dataset):
    def __init__(self, image_paths, labels, size=IMG_SIZE):
        self.image_paths = image_paths
        self.labels = labels
        self.size = size

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        path = self.image_paths[idx]
        label = self.labels[idx]
        
        # Load real patient radiograph
        img = Image.open(path).convert("RGB").resize((self.size, self.size))
        arr = np.array(img, dtype=np.float32) / 255.0
        
        # Standard normalization: (x - mean) / std
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        arr = (arr - mean) / std
        arr = np.transpose(arr, (2, 0, 1))  # (C, H, W)
        
        return torch.tensor(arr, dtype=torch.float32), torch.tensor(label, dtype=torch.long)

def load_real_kaggle_dataset(samples_per_class=600):
    print("=" * 80)
    print(" INGESTING REAL KAGGLE COVID-19 RADIOGRAPHY DATASET ")
    print("=" * 80)
    
    all_paths = []
    all_labels = []
    
    for c_idx, c_name in enumerate(CLASS_NAMES):
        img_dir = os.path.join(DATASET_DIR, c_name, "images")
        files = glob.glob(os.path.join(img_dir, "*.png"))
        print(f"[*] Class '{c_name}': Found {len(files)} total real X-ray scans.")
        
        random.shuffle(files)
        selected = files[:samples_per_class]
        all_paths.extend(selected)
        all_labels.extend([c_idx] * len(selected))
        print(f"    -> Sampled {len(selected)} balanced scans for training & evaluation.")
        
    # Shuffle combined dataset
    combined = list(zip(all_paths, all_labels))
    random.shuffle(combined)
    paths_shuffled, labels_shuffled = zip(*combined)
    
    n_total = len(paths_shuffled)
    n_train = int(n_total * 0.70)
    n_val = int(n_total * 0.15)
    n_test = n_total - n_train - n_val
    
    train_paths = paths_shuffled[:n_train]
    train_labels = labels_shuffled[:n_train]
    
    val_paths = paths_shuffled[n_train:n_train + n_val]
    val_labels = labels_shuffled[n_train:n_train + n_val]
    
    test_paths = paths_shuffled[n_train + n_val:]
    test_labels = labels_shuffled[n_train + n_val:]
    
    print(f"\n[*] Total Ingested Dataset: {n_total} real patient chest X-rays")
    print(f"[*] Training Cohort: {len(train_paths)} scans")
    print(f"[*] Validation Cohort: {len(val_paths)} scans")
    print(f"[*] Test Benchmark Cohort: {len(test_paths)} scans")
    
    return train_paths, train_labels, val_paths, val_labels, test_paths, test_labels

# ==============================================================================
# 3. Training & Evaluation Pipeline
# ==============================================================================
def train_vision_model():
    train_paths, train_labels, val_paths, val_labels, test_paths, test_labels = load_real_kaggle_dataset(samples_per_class=550)
    
    train_ds = RealRadiographyDataset(train_paths, train_labels)
    val_ds = RealRadiographyDataset(val_paths, val_labels)
    test_ds = RealRadiographyDataset(test_paths, test_labels)
    
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=32, shuffle=False)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training on target accelerator: {device}")
    
    model = DeepMedVisionNet(num_classes=4, in_channels=3).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=1e-3)
    
    epochs = 12
    train_losses, val_losses = [], []
    train_accs, val_accs = [], []
    
    print(f"\n[*] Commencing {epochs}-epoch convergence on real radiography images...")
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * len(batch_y)
            _, predicted = torch.max(outputs, 1)
            total += len(batch_y)
            correct += (predicted == batch_y).sum().item()
            
        train_loss = running_loss / total
        train_acc = correct / total
        
        # Validation
        model.eval()
        v_loss = 0.0
        v_correct = 0
        v_total = 0
        with torch.no_grad():
            for bx, by in val_loader:
                bx, by = bx.to(device), by.to(device)
                out = model(bx)
                l = criterion(out, by)
                v_loss += l.item() * len(by)
                _, p = torch.max(out, 1)
                v_total += len(by)
                v_correct += (p == by).sum().item()
                
        val_loss = v_loss / v_total
        val_acc = v_correct / v_total
        
        train_losses.append(train_loss)
        val_losses.append(val_loss)
        train_accs.append(train_acc)
        val_accs.append(val_acc)
        
        print(f" Epoch [{epoch:02d}/{epochs:02d}] | Train Loss: {train_loss:.4f} | Train Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f} | Val Acc: {val_acc*100:.2f}%")
        
    # Final Test Set Evaluation
    model.eval()
    all_preds, all_targets = [], []
    with torch.no_grad():
        for bx, by in test_loader:
            bx = bx.to(device)
            out = model(bx)
            _, p = torch.max(out, 1)
            all_preds.extend(p.cpu().numpy().tolist())
            all_targets.extend(by.numpy().tolist())
            
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    test_accuracy = float(np.mean(all_preds == all_targets))
    print(f"\n[+] Real Kaggle Test Set Accuracy: {test_accuracy * 100:.2f}%")
    
    # Confusion Matrix
    cm = np.zeros((4, 4), dtype=int)
    for t, p in zip(all_targets, all_preds):
        cm[t, p] += 1
        
    print("\nReal-World Confusion Matrix Breakdown:")
    print(cm)
    
    # Save Model Weights
    model_save_path = os.path.join(SAVED_MODELS_DIR, "deep_vision_model.pt")
    torch.save(model.state_dict(), model_save_path)
    
    config = {
        "model_name": "DeepMedVisionNet",
        "dataset_name": "COVID-19 Radiography Database (Kaggle)",
        "dataset_url": "https://www.kaggle.com/datasets/tawsifurrahman/covid19-radiography-database",
        "architecture": "4-Stage Deep CNN with BatchNorm and Dropout",
        "input_shape": [3, IMG_SIZE, IMG_SIZE],
        "num_classes": 4,
        "classes": CLASS_NAMES,
        "class_labels": [CLASS_LABELS_MAP[c] for c in CLASS_NAMES],
        "test_accuracy": round(test_accuracy * 100, 2),
        "validation_accuracy": round(val_accs[-1] * 100, 2),
        "training_epochs": epochs,
        "mean_norm": [0.485, 0.456, 0.406],
        "std_norm": [0.229, 0.224, 0.225],
        "version": "1.0.0"
    }
    config_save_path = os.path.join(SAVED_MODELS_DIR, "vision_config.json")
    with open(config_save_path, "w") as f:
        json.dump(config, f, indent=2)
        
    print(f"[OK] Vision Model weights saved to: {model_save_path}")
    print(f"[OK] Vision Model configuration saved to: {config_save_path}")
    
    # Copy Real Verification Test Samples to sample_data/
    sample_mappings = {
        "COVID": "covid_case.png",
        "Lung_Opacity": "lung_opacity_case.png",
        "Normal": "normal_case.png",
        "Viral Pneumonia": "viral_case.png"
    }
    for c_name, target_file in sample_mappings.items():
        img_dir = os.path.join(DATASET_DIR, c_name, "images")
        files = glob.glob(os.path.join(img_dir, "*.png"))
        if files:
            # Pick a clean representative sample
            src_img = Image.open(files[0]).convert("RGB").resize((128, 128))
            dest_path = os.path.join(SAMPLE_DATA_DIR, target_file)
            src_img.save(dest_path)
            print(f"[OK] Saved real patient verification sample: {dest_path}")
            
    # Plot Evaluation Curves
    plot_training_results(train_losses, val_losses, train_accs, val_accs, cm, test_accuracy)
    
    return config

def plot_training_results(train_losses, val_losses, train_accs, val_accs, cm, test_accuracy):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Loss
    axes[0].plot(train_losses, 'b-o', label='Training Loss', linewidth=2)
    axes[0].plot(val_losses, 'r--s', label='Validation Loss', linewidth=2)
    axes[0].set_title('Real Radiography Training & Validation Loss', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=10)
    axes[0].set_ylabel('Cross-Entropy Loss', fontsize=10)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    axes[0].legend()
    
    # Accuracy
    axes[1].plot([a * 100 for a in train_accs], 'b-o', label='Training Acc (%)', linewidth=2)
    axes[1].plot([a * 100 for a in val_accs], 'g--^', label=f'Val Acc (Final: {val_accs[-1]*100:.1f}%)', linewidth=2)
    axes[1].set_title('Classification Accuracy Progression', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=10)
    axes[1].set_ylabel('Accuracy (%)', fontsize=10)
    axes[1].grid(True, linestyle='--', alpha=0.6)
    axes[1].legend()
    
    # Confusion Matrix
    im = axes[2].imshow(cm, cmap='Blues', interpolation='nearest')
    axes[2].set_title(f'Real Test Confusion Matrix (Acc: {test_accuracy*100:.1f}%)', fontsize=12, fontweight='bold')
    tick_marks = np.arange(len(CLASS_NAMES))
    axes[2].set_xticks(tick_marks)
    axes[2].set_xticklabels(CLASS_NAMES, rotation=35, ha='right')
    axes[2].set_yticks(tick_marks)
    axes[2].set_yticklabels(CLASS_NAMES)
    axes[2].set_ylabel('Ground Truth Clinical Label', fontsize=10)
    axes[2].set_xlabel('Predicted Diagnostic Class', fontsize=10)
    
    for i in range(len(CLASS_NAMES)):
        for j in range(len(CLASS_NAMES)):
            color = "white" if cm[i, j] > cm.max() / 2 else "black"
            axes[2].text(j, i, format(cm[i, j], 'd'),
                         ha="center", va="center", color=color, fontweight='bold')
                         
    fig.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
    plt.tight_layout()
    
    chart_path = os.path.join(SCREENSHOTS_DIR, "fig1_model_training_curves.png")
    plt.savefig(chart_path, dpi=200)
    plt.close()
    print(f"[OK] Real dataset evaluation charts saved to: {chart_path}")

def train_tabular_model():
    print("\n[*] Training companion DeepHealthRiskNet for Multi-Condition Risk scoring...")
    input_dim = 14
    num_classes = 4
    n_samples = 1000
    
    X_raw = np.random.randn(n_samples, input_dim).astype(np.float32)
    risk_scores = 0.5 * X_raw[:, 0] + 0.8 * X_raw[:, 2] - 0.4 * X_raw[:, 4] + 0.3 * np.random.randn(n_samples)
    y = np.digitize(risk_scores, bins=np.percentile(risk_scores, [25, 50, 75])).astype(np.int64)
    
    model = DeepHealthRiskNet(input_dim=input_dim, num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    dataset = torch.utils.data.TensorDataset(torch.tensor(X_raw), torch.tensor(y))
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    for epoch in range(10):
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            
    pt_path = os.path.join(SAVED_MODELS_DIR, "dl_model.pt")
    torch.save(model.state_dict(), pt_path)
    
    tab_cfg = {
        "model_name": "DeepHealthRiskNet",
        "input_dim": 14,
        "classes": ["Low Risk", "Moderate Risk", "High Risk", "Critical Risk"],
        "version": "1.0.0",
        "scaler_means": [float(m) for m in np.mean(X_raw, axis=0)],
        "scaler_stds": [float(s) for s in np.std(X_raw, axis=0)]
    }
    with open(os.path.join(SAVED_MODELS_DIR, "config.json"), "w") as f:
        json.dump(tab_cfg, f, indent=2)
    print(f"[OK] Tabular DeepHealthRiskNet saved to: {pt_path}")

if __name__ == "__main__":
    train_vision_model()
    train_tabular_model()
    print("\n[SUCCESS] Phase 1: Real Kaggle Dataset Model Training & Artifact Serialization Complete!")
