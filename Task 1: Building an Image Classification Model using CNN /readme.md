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

## Conclusion

The CNN successfully classified the five flower categories with an overall accuracy of approximately 73%. The model performed particularly well on sunflowers and dandelions, while roses and tulips were more challenging to distinguish.
