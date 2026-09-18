# Task 2: Transfer Learning using ResNet50

## Overview

This project demonstrates **Transfer Learning** using a pre-trained **ResNet50** model and compares its performance with a custom CNN trained from scratch.

The experiment is performed on the **Flowers Recognition Dataset**, with the goal of analyzing whether a pre-trained deep learning model can provide better classification performance than a simple CNN trained from scratch.

## Objective

The main objectives of this task are:

1. Load and preprocess the Flowers Recognition dataset.
2. Build and train a custom CNN model from scratch as a baseline.
3. Implement transfer learning using a pre-trained ResNet50 model with ImageNet weights.
4. Compare both models based on:

   * Validation accuracy
   * Validation loss
   * Training time
5. Visualize the validation accuracy and loss curves.
6. Analyze the advantages and trade-offs of transfer learning.

---

## Dataset

**Flowers Recognition Dataset**

The dataset is downloaded directly from Kaggle using `kagglehub`.

**Dataset:** `alxmamaev/flowers-recognition`

### Dataset Details

* Total images: **4317**
* Number of classes: **5**
* Training images: **3454**
* Validation images: **863**

### Classes

* Daisy
* Dandelion
* Rose
* Sunflower
* Tulip

The dataset is divided into training and validation sets using an **80/20 split**.

---

## Technologies and Libraries

The notebook uses the following Python libraries and frameworks:

* Python
* TensorFlow
* Keras
* NumPy
* Matplotlib
* KaggleHub

The notebook is configured to use a **GPU accelerator (T4)** when available.

---

## Data Preprocessing

The images are loaded using TensorFlow's `image_dataset_from_directory`.

### Configuration

* Image size: **180 × 180**
* Batch size: **32**
* Training/validation split: **80/20**
* Random seed: **123**

Pixel values are rescaled from `[0, 255]` to `[0, 1]`.

The notebook also uses `tf.data.AUTOTUNE` for dataset prefetching.

### Data Augmentation

A data augmentation pipeline is used to reduce overfitting:

* Random horizontal flipping
* Random rotation of up to `0.15`
* Random zoom of up to `0.15`

The same augmentation pipeline is incorporated into both models.

---

# Model 1: Baseline Custom CNN

A custom CNN is created and trained from scratch to provide a baseline for comparison.

### Architecture

The model consists of:

1. Input layer
2. Data augmentation
3. Conv2D — 32 filters
4. MaxPooling2D
5. Conv2D — 64 filters
6. MaxPooling2D
7. Conv2D — 128 filters
8. MaxPooling2D
9. Flatten
10. Dense — 128 neurons
11. Dropout — 0.5
12. Output Dense layer with 5 classes and Softmax activation

### Compilation

* Optimizer: **Adam**
* Loss: **Sparse Categorical Crossentropy**
* Metric: **Accuracy**

The model is trained for **10 epochs**.

---

# Model 2: ResNet50 Transfer Learning

The second model uses **ResNet50 pretrained on ImageNet** as a feature extractor.

The original ResNet50 classification head is removed using:

```python
include_top=False
```

The ResNet50 base layers are frozen so that their pretrained weights are not updated during training.

### Transfer Learning Architecture

The model consists of:

1. Input layer
2. Data augmentation
3. ResNet50 preprocessing
4. Pre-trained ResNet50 backbone
5. Global Average Pooling
6. Batch Normalization
7. Dense — 256 neurons with ReLU
8. Dropout — 0.4
9. Dense output layer with Softmax activation

### Compilation

* Optimizer: **Adam**
* Learning rate: `0.001`
* Loss: **Sparse Categorical Crossentropy**
* Metric: **Accuracy**

The model is also trained for **10 epochs**.

---

# Experimental Results

Both models were trained using the same training and validation datasets for a fair comparison.

| Metric                        | Baseline CNN | ResNet50 Transfer Learning |
| ----------------------------- | -----------: | -------------------------: |
| Best Validation Accuracy      |       70.57% |                 **89.22%** |
| Lowest Validation Loss        |       0.7811 |                 **0.4143** |
| Total Training Time           |      81.09 s |                   143.83 s |
| Validation Accuracy — Epoch 1 |       56.32% |                 **85.63%** |

---

## Performance Comparison

### Validation Accuracy

The baseline CNN achieved a best validation accuracy of **70.57%**.

The ResNet50 transfer learning model achieved **89.22%**, resulting in an improvement of approximately:

**18.65 percentage points**

This demonstrates the benefit of using features learned from ImageNet for the flower classification task.

### Validation Loss

The baseline CNN achieved a lowest validation loss of **0.7811**.

ResNet50 achieved a substantially lower validation loss of **0.4143**.

This indicates that the transfer learning model produced more confident predictions on the validation dataset.

### Convergence

ResNet50 achieved **85.63% validation accuracy during the first epoch**.

The baseline CNN never reached this level of validation accuracy during its 10 epochs of training.

This demonstrates the advantage of starting with pretrained feature representations rather than learning all visual features from scratch.

### Training Time

The baseline CNN required:

**81.09 seconds**

for 10 epochs.

The ResNet50 transfer learning model required:

**143.83 seconds**

for 10 epochs.

Therefore, ResNet50 required more computational time per run because of its considerably larger backbone, even though the backbone weights were frozen.

However, the transfer learning model reached a much higher accuracy much earlier.

---

# Visualization

The notebook generates comparison plots for:

* Validation Accuracy
* Validation Loss

The curves of the baseline CNN and ResNet50 are plotted together to visually compare their learning behavior over the 10 training epochs.

---

# Observations

### 1. Significant Accuracy Improvement

ResNet50 achieved **89.22%** best validation accuracy compared with **70.57%** for the baseline CNN.

This represents an improvement of approximately **18.65 percentage points**.

### 2. Faster Convergence

The transfer learning model achieved **85.63% validation accuracy in the first epoch**, while the baseline CNN remained below this level throughout its 10 epochs.

This shows that pretrained convolutional features already provide useful representations for flower classification.

### 3. Lower Validation Loss

ResNet50 achieved a lowest validation loss of **0.4143**, compared with **0.7811** for the baseline CNN.

The substantially lower loss indicates better prediction performance.

### 4. Limitations of the Baseline CNN

The baseline CNN was trained from scratch using approximately **3454 training images**.

With only three convolutional blocks and no pretrained knowledge, the model reached approximately 70% validation accuracy and showed a more variable validation loss curve.

### 5. Training Time Trade-off

ResNet50 required more time per training run:

* Baseline CNN: **81.09 s**
* ResNet50: **143.83 s**

However, this additional computational cost resulted in a substantial improvement in accuracy and convergence speed.

### 6. Overfitting Control

By freezing the ResNet50 base layers and using:

* Data augmentation
* Dropout (`0.4`)

the transfer learning model maintained a relatively small gap between training and validation accuracy.

The final training accuracy was **93.69%**, while validation accuracy was **89.22%**.

---

# Conclusion

The experiment demonstrates that **transfer learning using a pretrained ResNet50 model significantly outperforms a custom CNN trained from scratch** on the Flowers Recognition dataset.

ResNet50 achieved:

* **Higher validation accuracy:** 89.22% vs. 70.57%
* **Lower validation loss:** 0.4143 vs. 0.7811
* **Much faster convergence**

The main trade-off is increased training time per epoch because ResNet50 has a much larger architecture.

Overall, for small-to-medium-sized image classification datasets, **transfer learning provides a more effective and practical approach than training a CNN completely from scratch**, particularly when a suitable pretrained model is available.
