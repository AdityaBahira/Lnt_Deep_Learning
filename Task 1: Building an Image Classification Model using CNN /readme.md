# Flower Image Classification using CNN

## Introduction

This project develops a Convolutional Neural Network (CNN) to classify flower images into five categories: daisy, dandelion, roses, sunflowers, and tulips.

## Dataset

- Dataset: TensorFlow Flowers
- Total images: 3,670
- Classes: 5
- Image size: 180 × 180 × 3

## CNN Architecture

The model consists of convolutional and max-pooling layers followed by Global Average Pooling and dense layers.

- Conv2D: 32 filters
- Conv2D: 64 filters
- Conv2D: 128 filters
- Conv2D: 256 filters
- Global Average Pooling
- Dense: 256 neurons
- Dropout: 0.5
- Output: 5 classes

## Results

- Test Accuracy: **73%**
- Test Images: **382**
- Model Parameters: **455,493**

## Classification Report

| Class | Precision | Recall | F1-Score |
|---|---:|---:|---:|
| Daisy | 0.62 | 0.84 | 0.72 |
| Dandelion | 0.77 | 0.75 | 0.76 |
| Roses | 0.67 | 0.67 | 0.67 |
| Sunflowers | 0.78 | 0.86 | 0.81 |
| Tulips | 0.79 | 0.59 | 0.68 |

## Results

- The final CNN achieved an overall test accuracy of **73%** on 382 test images.
- The model contains **455,493 parameters**.
- **Sunflowers** achieved the highest F1-score of **0.81**.
- **Dandelions** also performed well with an F1-score of **0.76**.
- A new flower image was successfully classified as **tulips with 96.25% confidence**.

## Observations

- The model learned useful visual features during training.
- Sunflowers and dandelions were classified relatively well.
- Roses and tulips were comparatively more difficult to distinguish.
- Data augmentation helped the model handle variations in the input images.
- The confusion matrix showed that most classification errors occurred between visually similar flower classes.
- Overall, the custom CNN achieved reasonable performance for this five-class flower classification task.


## Conclusion

The CNN successfully classified the five flower categories with an overall accuracy of approximately **73%**. The model performed particularly well on sunflowers and dandelions, while roses and tulips were more challenging to distinguish.
