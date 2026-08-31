# Task 2: Transfer Learning using ResNet50

## Introduction

This project implements transfer learning using a pre-trained ResNet50 model on the CIFAR-10 dataset.

The main purpose of this task is to compare a pre-trained deep learning model with a custom CNN and observe the difference in accuracy and training performance.

## Dataset

The **CIFAR-10** dataset is used in this project.

It contains 60,000 colour images divided into 10 classes:

* Airplane
* Automobile
* Bird
* Cat
* Deer
* Dog
* Frog
* Horse
* Ship
* Truck

The dataset is loaded directly using TensorFlow/Keras.

## Models Used

### 1. Baseline CNN

A simple CNN model is created as the baseline.

It contains:

* Convolutional layers
* Max pooling layers
* Dense layers
* Softmax output layer

This model learns the image features from the CIFAR-10 dataset from the beginning.

### 2. ResNet50

A pre-trained **ResNet50** model with ImageNet weights is used for transfer learning.

The base ResNet50 layers are frozen, and additional classification layers are added for the 10 CIFAR-10 classes.

This allows the model to use features that were already learned from ImageNet.

## Data Preprocessing

The CIFAR-10 images are normalized by dividing the pixel values by 255.

The images are also resized from 32 × 32 to 96 × 96 before being given to ResNet50.

## Data Augmentation

Data augmentation is used to increase the variety of training images.

The following simple augmentation techniques are used:

* Random horizontal flipping
* Random rotation
* Random zoom

Data augmentation is applied to the training data to help the model generalize better.

## Hyperparameter Tuning

A simple automatic hyperparameter tuning step is included.

Two learning rates are tested:

* 0.001
* 0.0001

The learning rate giving better validation accuracy is selected for the final ResNet50 training.

## Training

Both the baseline CNN and ResNet50 are trained for a small number of epochs to keep the experiment manageable.

The training time of both models is recorded and compared.

## Evaluation

The models are evaluated using accuracy.

The following results are compared:

* Baseline CNN accuracy
* ResNet50 accuracy
* Accuracy improvement
* Baseline CNN training time
* ResNet50 training time

## Visualizations

The notebook contains graphs for:

* Training accuracy
* Validation accuracy
* Validation loss

These graphs are used to understand the training performance of both models.

## Results

The final accuracy and training time are obtained after running the notebook.

The results can be added here after training:

| Model        |   Accuracy | Training Time |
| ------------ | ---------: | ------------: |
| Baseline CNN | 0.53 |    14.74s |
| ResNet50     | 0.54 |    22.38s |

## Observation

The baseline CNN learns the image features directly from the CIFAR-10 dataset. ResNet50 starts with features learned from the ImageNet dataset.

Transfer learning can help the ResNet50 model achieve better performance because it already has useful learned features.

Data augmentation provides more variation in the training images, which can help improve generalization.

The actual results depend on the number of epochs, selected learning rate, and the hardware used for training.

## Conclusion

In this task, transfer learning was implemented using a pre-trained ResNet50 model on the CIFAR-10 dataset.

The performance was compared with a simple CNN model. Data augmentation and simple hyperparameter tuning were also used.

This experiment demonstrates how a pre-trained deep learning model can be used for a new image classification task with comparatively less training of the base model.

## Requirements

The notebook can be run using:

* Google Colab
* Python
* TensorFlow
* Matplotlib

## Files

```text
Task_2_Transfer_Learning_final.ipynb
README.md
```
