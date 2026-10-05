"""
train_model.py
--------------
End-to-End Deep Learning Training Pipeline for Task 15.
Designs, trains, evaluates, and serializes a high-performance PyTorch Deep Convolutional
Neural Network (DeepMedVisionNet) for multi-class radiological image classification,
alongside a clinical biomarker Deep Neural Network (DeepHealthRiskNet).

Outputs:
- Serialized PyTorch models (.pt) and architecture configs (.json)
- Sample diagnostic images in sample_data/ for live inference testing
- Model evaluation curves (Loss, Accuracy, Confusion Matrix) saved to screenshots/
"""

import os
import sys
import json
import math
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from PIL import Image, ImageDraw, ImageFilter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set reproducibility seeds
np.random.seed(42)
torch.manual_seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
SAMPLE_DATA_DIR = os.path.join(PROJECT_DIR, "sample_data")
SCREENSHOTS_DIR = os.path.join(PROJECT_DIR, "screenshots")

os.makedirs(SAVED_MODELS_DIR, exist_ok=True)
os.makedirs(SAMPLE_DATA_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

CLASS_NAMES = [
    "Normal / Healthy",
    "Bacterial Pneumonia",
    "Viral Pneumonia",
    "COVID-19 Infiltration"
]
IMG_SIZE = 64

# ==============================================================================
# 1. PyTorch Deep Neural Network Architectures
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
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        feat = self.features(x)
        logits = self.classifier(feat)
        return logits


class DeepHealthRiskNet(nn.Module):
    """
    Multi-Layer Perceptron for Clinical Biomarker Multi-Condition Risk Assessment.
    """
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
# 2. Synthetic Radiological Data Synthesis Engine
# ==============================================================================
def generate_synthetic_radiograph(class_idx, size=IMG_SIZE):
    """
    Generates a realistic synthetic chest radiograph simulation based on clinical pathology.
    Class 0: Normal (clear bilateral lung fields, central cardiac silhouette).
    Class 1: Bacterial Pneumonia (dense focal lobar consolidation in right lower lobe).
    Class 2: Viral Pneumonia (diffuse bilateral interstitial reticular markings).
    Class 3: COVID-19 (peripheral ground-glass opacities and bilateral patches).
    """
    img = Image.new('L', (size, size), color=15)
    draw = ImageDraw.Draw(img)
    
    # Anatomical thorax contour
    draw.ellipse([size * 0.1, size * 0.05, size * 0.9, size * 0.95], fill=30)
    
    # Left & Right lung fields (translucent low radiodensity)
    draw.ellipse([size * 0.15, size * 0.2, size * 0.45, size * 0.8], fill=70)
    draw.ellipse([size * 0.55, size * 0.2, size * 0.85, size * 0.8], fill=70)
    
    # Central mediastinum / cardiac silhouette
    draw.polygon([
        (size * 0.45, size * 0.25),
        (size * 0.55, size * 0.25),
        (size * 0.62, size * 0.70),
        (size * 0.38, size * 0.70)
    ], fill=120)
    
    # Rib cage lattice
    for y in range(int(size * 0.25), int(size * 0.8), int(size * 0.1)):
        draw.arc([size * 0.12, y, size * 0.88, y + 15], 0, 180, fill=90, width=1)
    
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, 5.0, arr.shape)
    arr = np.clip(arr + noise, 0, 255)
    
    # Pathology-specific features
    if class_idx == 1:
        # Bacterial consolidation (dense bright lobar patch in right lower field)
        y, x = np.ogrid[:size, :size]
        mask = ((x - size * 0.3)**2 + (y - size * 0.6)**2) <= (size * 0.18)**2
        arr[mask] = np.clip(arr[mask] + np.random.uniform(90, 140), 0, 255)
    elif class_idx == 2:
        # Viral interstitial markings (bilateral reticular streaks)
        streaks = np.sin(np.linspace(0, 20 * math.pi, size))[:, None] * 35.0
        arr = np.clip(arr + streaks, 0, 255)
    elif class_idx == 3:
        # COVID-19 peripheral bilateral ground glass opacities
        y, x = np.ogrid[:size, :size]
        mask_l = ((x - size * 0.2)**2 + (y - size * 0.55)**2) <= (size * 0.15)**2
        mask_r = ((x - size * 0.8)**2 + (y - size * 0.55)**2) <= (size * 0.15)**2
        arr[mask_l | mask_r] = np.clip(arr[mask_l | mask_r] + np.random.uniform(70, 120), 0, 255)
        
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    rgb = np.stack([arr, arr, arr], axis=-1)
    return Image.fromarray(rgb)

def create_dataset(num_samples=1200):
    print(f"[*] Generating {num_samples} diagnostic radiological samples across 4 classes...")
    images = []
    labels = []
    samples_per_class = num_samples // len(CLASS_NAMES)
    
    for c_idx in range(len(CLASS_NAMES)):
        for _ in range(samples_per_class):
            im = generate_synthetic_radiograph(c_idx, size=IMG_SIZE)
            arr = np.array(im, dtype=np.float32) / 255.0  # Normalize to [0, 1]
            arr = np.transpose(arr, (2, 0, 1))           # (C, H, W)
            images.append(arr)
            labels.append(c_idx)
            
    images = np.array(images, dtype=np.float32)
    labels = np.array(labels, dtype=np.int64)
    
    # Shuffle
    indices = np.random.permutation(len(images))
    images = images[indices]
    labels = labels[indices]
    
    return images, labels

# ==============================================================================
# 3. Model Training & Evaluation Pipeline
# ==============================================================================
def train_vision_model():
    print("=" * 80)
    print(" TASK 15: TRAINING DEEPMED-VISION CONVOLUTIONAL NEURAL NETWORK ")
    print("=" * 80)
    
    X, y = create_dataset(num_samples=1200)
    n_total = len(X)
    n_train = int(n_total * 0.70)
    n_val = int(n_total * 0.15)
    n_test = n_total - n_train - n_val
    
    X_train, y_train = torch.tensor(X[:n_train]), torch.tensor(y[:n_train])
    X_val, y_val = torch.tensor(X[n_train:n_train+n_val]), torch.tensor(y[n_train:n_train+n_val])
    X_test, y_test = torch.tensor(X[n_train+n_val:]), torch.tensor(y[n_train+n_val:])
    
    train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32, shuffle=False)
    test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=32, shuffle=False)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Training on target hardware accelerator: {device}")
    
    model = DeepMedVisionNet(num_classes=4, in_channels=3).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    
    epochs = 15
    train_losses, val_losses = [], []
    train_accs, val_accs = [], []
    
    print(f"[*] Starting {epochs}-epoch convergence optimization...")
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
        
        if epoch % 3 == 0 or epoch == epochs:
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
    print(f"\n[+] Test Set Accuracy: {test_accuracy * 100:.2f}%")
    
    # Compute Confusion Matrix
    cm = np.zeros((4, 4), dtype=int)
    for t, p in zip(all_targets, all_preds):
        cm[t, p] += 1
        
    # Serialize Vision Model Artifacts
    model_save_path = os.path.join(SAVED_MODELS_DIR, "deep_vision_model.pt")
    torch.save(model.state_dict(), model_save_path)
    
    config = {
        "model_name": "DeepMedVisionNet",
        "architecture": "4-Stage Deep CNN with BatchNorm and Dropout",
        "input_shape": [3, IMG_SIZE, IMG_SIZE],
        "num_classes": 4,
        "classes": CLASS_NAMES,
        "test_accuracy": round(test_accuracy * 100, 2),
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
    
    # Generate Sample Test Images for Client / UI Demonstrations
    sample_files = {}
    for c_idx, c_name in enumerate(CLASS_NAMES):
        slug = c_name.split()[0].lower() + "_case.png"
        s_img = generate_synthetic_radiograph(c_idx, size=128)
        s_path = os.path.join(SAMPLE_DATA_DIR, slug)
        s_img.save(s_path)
        sample_files[c_name] = s_path
        print(f"[OK] Generated verification diagnostic image: {s_path}")
        
    # Plot Loss / Accuracy Curves and Confusion Matrix
    plot_training_results(train_losses, val_losses, train_accs, val_accs, cm)
    
    return config

def plot_training_results(train_losses, val_losses, train_accs, val_accs, cm):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # 1. Loss Curves
    axes[0].plot(train_losses, 'b-o', label='Training Loss', linewidth=2)
    axes[0].plot(val_losses, 'r--s', label='Validation Loss', linewidth=2)
    axes[0].set_title('Deep Learning Training & Validation Loss', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Epoch', fontsize=10)
    axes[0].set_ylabel('Cross-Entropy Loss', fontsize=10)
    axes[0].grid(True, linestyle='--', alpha=0.6)
    axes[0].legend()
    
    # 2. Accuracy Curves
    axes[1].plot([a * 100 for a in train_accs], 'b-o', label='Training Acc (%)', linewidth=2)
    axes[1].plot([a * 100 for a in val_accs], 'g--^', label='Validation Acc (%)', linewidth=2)
    axes[1].set_title('Classification Accuracy Progression', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Epoch', fontsize=10)
    axes[1].set_ylabel('Accuracy (%)', fontsize=10)
    axes[1].grid(True, linestyle='--', alpha=0.6)
    axes[1].legend()
    
    # 3. Confusion Matrix Heatmap
    im = axes[2].imshow(cm, cmap='Blues', interpolation='nearest')
    axes[2].set_title('Test Set Confusion Matrix', fontsize=12, fontweight='bold')
    tick_marks = np.arange(len(CLASS_NAMES))
    short_labels = ["Normal", "Bacterial", "Viral", "COVID-19"]
    axes[2].set_xticks(tick_marks)
    axes[2].set_xticklabels(short_labels, rotation=45, ha='right')
    axes[2].set_yticks(tick_marks)
    axes[2].set_yticklabels(short_labels)
    axes[2].set_ylabel('Ground Truth Label', fontsize=10)
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
    print(f"[OK] Training evaluation charts saved to: {chart_path}")

# ==============================================================================
# 4. Clinical Tabular Risk Model Serialization
# ==============================================================================
def train_tabular_model():
    """Trains and serializes the companion DeepHealthRiskNet for clinical biomarker risk."""
    print("\n[*] Training companion DeepHealthRiskNet for Multi-Condition Risk scoring...")
    input_dim = 14
    num_classes = 4
    n_samples = 1000
    
    # Generate realistic biomarker distribution
    X_raw = np.random.randn(n_samples, input_dim).astype(np.float32)
    # Synthetic target correlated with biomarkers
    risk_scores = 0.5 * X_raw[:, 0] + 0.8 * X_raw[:, 2] - 0.4 * X_raw[:, 4] + 0.3 * np.random.randn(n_samples)
    y = np.digitize(risk_scores, bins=np.percentile(risk_scores, [25, 50, 75])).astype(np.int64)
    
    model = DeepHealthRiskNet(input_dim=input_dim, num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    dataset = TensorDataset(torch.tensor(X_raw), torch.tensor(y))
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    for epoch in range(10):
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
            
    # Serialize weights
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
    print("\n[SUCCESS] Phase 1: Deep Learning Models Training & Artifact Serialization Complete!")
