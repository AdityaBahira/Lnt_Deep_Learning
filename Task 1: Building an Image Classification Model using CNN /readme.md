# 🌸 Task 1: Flower Classification using CNN

## 📌 Introduction

This project develops a Convolutional Neural Network (CNN) for classifying flower images into five categories: Daisy, Dandelion, Roses, Sunflowers, and Tulips.

The project covers dataset exploration, image preprocessing, data augmentation, CNN model development, training, evaluation, model saving, and prediction.

---

## 📂 Dataset

The project uses the **TF Flowers** dataset.

- **Total Images:** 3,670
- **Number of Classes:** 5
- **Classes:**
  - Daisy
  - Dandelion
  - Roses
  - Sunflowers
  - Tulips
- **Image Size:** 180 × 180 × 3

### Dataset Split

| Dataset | Images |
|---|---:|
| Training | 2,936 |
| Validation | 352 |
| Testing | 382 |

---

## 🧠 CNN Architecture

The custom CNN consists of:

- Rescaling layer
- Random Horizontal Flip
- Random Rotation
- Random Zoom
- Conv2D - 32 filters
- MaxPooling2D
- Conv2D - 64 filters
- MaxPooling2D
- Conv2D - 128 filters
- MaxPooling2D
- Conv2D - 256 filters
- MaxPooling2D
- Global Average Pooling
- Dense layer - 256 neurons
- Dropout - 0.5
- Output layer - 5 classes

**Total Parameters:** 455,493

---

## ⚙️ Training Configuration

- **Image Size:** 180 × 180
- **Batch Size:** 32
- **Optimizer:** Adam
- **Loss Function:** Sparse Categorical Crossentropy
- **Epochs:** 20
- **Data Augmentation:** Yes

---

## 📊 Results

The model achieved approximately **73.6% test accuracy**.

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| Daisy | 0.62 | 0.84 | 0.72 | 51 |
| Dandelion | 0.77 | 0.75 | 0.76 | 101 |
| Roses | 0.67 | 0.67 | 0.67 | 61 |
| Sunflowers | 0.78 | 0.86 | 0.81 | 77 |
| Tulips | 0.79 | 0.59 | 0.68 | 92 |
| **Accuracy** | | | **0.73** | **382** |

### Overall Metrics

- **Test Accuracy:** ~73.6%
- **Test Samples:** 382
- **Correct Predictions:** 280
- **Model:** Custom CNN
- **Parameters:** 455,493

---

## 🔍 Observations

- Training accuracy improved steadily during training.
- Sunflowers and dandelions were classified relatively well.
- Roses and tulips were comparatively more difficult to distinguish.
- The confusion matrix shows misclassification between visually similar flower categories.
- Data augmentation helped the model handle variations in flower images.
- Overall, the custom CNN achieved reasonable performance for a basic image-classification task.

---

## 🧪 Sample Prediction

The trained model was tested on new flower images.

Example:

**Predicted Flower:** Tulips  
**Confidence:** 97.76%

The model was also tested through a Streamlit application and successfully classified uploaded flower images.

---

## 💾 Model Saving

The trained model was saved as:

```text
flower_cnn_model.keras
```
