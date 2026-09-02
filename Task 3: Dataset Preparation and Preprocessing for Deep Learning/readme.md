# Task 3: Dataset Preparation and Preprocessing for Deep Learning

## 📌 Overview

This project focuses on **dataset preparation and preprocessing for deep learning applications** using the **CIFAR-10 image dataset**.

The task covers exploratory data analysis (EDA), data-quality checks, image normalization, image augmentation, dataset splitting, visualization, and preparation of efficient TensorFlow data pipelines.

## 🎯 Objective

The main objective is to prepare the CIFAR-10 dataset for deep learning by applying appropriate preprocessing and feature transformation techniques.

The following activities are performed:

* Exploratory Data Analysis (EDA)
* Data-quality and integrity checks
* Image preprocessing
* Pixel normalization
* Image augmentation
* Train-validation-test splitting
* Data visualization
* TensorFlow dataset pipeline preparation

## 📊 Dataset

### CIFAR-10

CIFAR-10 is an image classification dataset containing:

* **60,000 color images**
* Image size: **32 × 32 pixels**
* **3 RGB channels**
* **10 classes**
* 50,000 training images
* 10,000 test images

### Classes

| Label | Class      |
| ----: | ---------- |
|     0 | Airplane   |
|     1 | Automobile |
|     2 | Bird       |
|     3 | Cat        |
|     4 | Deer       |
|     5 | Dog        |
|     6 | Frog       |
|     7 | Horse      |
|     8 | Ship       |
|     9 | Truck      |

The dataset is perfectly balanced, with **5,000 training images per class**.

## 🛠️ Technologies and Libraries

* Python
* TensorFlow / Keras
* NumPy
* Pandas
* Matplotlib
* Seaborn
* Jupyter Notebook

## 🔍 Exploratory Data Analysis

The following EDA operations are performed:

1. Dataset size and shape inspection
2. Image dimension analysis
3. Class-name identification
4. Sample image visualization
5. Class distribution visualization
6. Pixel-value distribution analysis

The analysis confirms that the CIFAR-10 dataset contains images of consistent dimensions and a balanced distribution across all ten classes.

## 🧹 Data Quality Checks

The dataset is checked for:

* Missing values
* Invalid labels
* Invalid pixel values
* Unexpected image dimensions
* Duplicate images in a 10,000-image subset

### Results

* Missing values in training images: **0**
* Missing values in test images: **0**
* Missing values in training labels: **0**
* Missing values in test labels: **0**
* Valid labels: **0–9**
* Valid image shape: **32 × 32 × 3**
* Pixel range before preprocessing: **0–255**
* Duplicate images in checked 10,000-image subset: **0**

## ✂️ Train-Validation-Test Split

The original CIFAR-10 training set is divided into training and validation sets.

| Dataset    | Number of Images |
| ---------- | ---------------: |
| Training   |           45,000 |
| Validation |            5,000 |
| Test       |           10,000 |
| **Total**  |       **60,000** |

The test set remains the original CIFAR-10 test set.

## 🖼️ Image Preprocessing

### Pixel Normalization

The image pixel values are originally represented in the range:

```text
0 – 255
```

They are converted to floating-point values and normalized to:

```text
0 – 1
```

using:

```python
x_train_norm = x_train.astype("float32") / 255.0
x_val_norm = x_val.astype("float32") / 255.0
x_test_norm = x_test.astype("float32") / 255.0
```

After normalization:

* Minimum pixel value: **0.0**
* Maximum pixel value: **1.0**
* Data type: **float32**

## 🔄 Image Augmentation

Image augmentation is applied **only to the training data**.

The following augmentation techniques are used:

* Random horizontal flipping
* Random rotation
* Random zoom
* Random translation

Implementation:

```python
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
    layers.RandomTranslation(0.1, 0.1)
], name="data_augmentation")
```

Augmentation introduces controlled variations in training images and can help improve model generalization and reduce overfitting.

Validation and test images are kept unaugmented to ensure fair evaluation.

## ⚡ TensorFlow Data Pipeline

The preprocessed arrays are converted into TensorFlow `tf.data.Dataset` objects.

A batch size of **64** is used.

The training dataset is:

* Shuffled
* Batched
* Prefetched

Validation and test datasets are:

* Batched
* Prefetched

Example:

```python
BATCH_SIZE = 64
AUTOTUNE = tf.data.AUTOTUNE

train_ds = tf.data.Dataset.from_tensor_slices(
    (x_train_norm, y_train)
)

train_ds = train_ds.shuffle(
    10000, seed=42
).batch(
    BATCH_SIZE
).prefetch(AUTOTUNE)
```

A sample training batch has the shape:

```text
Images: (64, 32, 32, 3)
Labels: (64, 1)
Pixel range: 0.0 – 1.0
Data type: float32
```

## 📈 Visualizations

The notebook includes visualizations for:

* Sample images from all 10 CIFAR-10 classes
* Training class distribution
* Pixel-value distribution before normalization
* Normalized images
* Augmented images
* Preprocessed training batches

## 📁 Project Structure

```text
Task-3-CIFAR10-Preprocessing/
│
├── Task_3_CIFAR10_Dataset_Preprocessing.ipynb
├── Task_3_CIFAR10_Preprocessing_Report.docx
└── README.md
```

## 📝 Observations

1. CIFAR-10 contains RGB images with dimensions **32 × 32 × 3**.
2. The dataset contains **10 balanced classes**.
3. Pixel values initially range from **0 to 255**.
4. No missing values were found in the loaded CIFAR-10 arrays.
5. All labels are valid class IDs from **0 to 9**.
6. Image normalization scales pixel values to **0–1**.
7. Data augmentation introduces additional variation into training images.
8. Validation and test datasets remain unaugmented.
9. The final TensorFlow datasets are batched and prefetched for efficient deep-learning training.

## ✅ Results

The CIFAR-10 dataset was successfully prepared for deep learning.

The final preprocessing pipeline provides:

* Clean and validated image data
* Proper train-validation-test separation
* Normalized image inputs
* Training-time image augmentation
* Visual EDA outputs
* Efficient TensorFlow data pipelines

The processed dataset is ready to be used as input for a **Convolutional Neural Network (CNN)** or another image-based deep-learning model.

## 🏁 Conclusion

This project demonstrates the complete preprocessing workflow required before training a deep-learning model on an image dataset.

CIFAR-10 was analyzed, validated, split, normalized, augmented, visualized, and converted into efficient TensorFlow datasets. The resulting pipeline provides a suitable foundation for the next stage of deep-learning model development and image classification.

---

### 📚 Task Information

**Task:** Task 3 – Dataset Preparation and Preprocessing for Deep Learning
**Dataset:** CIFAR-10
**Domain:** Computer Vision / Deep Learning
**Framework:** TensorFlow / Keras
**Language:** Python
**Environment:** Jupyter Notebook / Google Colab
