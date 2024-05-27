# Experimentation Process

## Introduction
In this project, we aim to classify traffic signs using a convolutional neural network (CNN). We experimented with various configurations of convolutional and pooling layers, hidden layers, and dropout to achieve optimal performance.

## Data Preprocessing
We used OpenCV to read and resize images. Each image was resized to 30x30 pixels to maintain consistency across the dataset.

## Model Architecture
The final model architecture consists of three convolutional layers with increasing filter sizes `32`, followed by a max-pooling layer to reduce dimensionality. After flattening the output, we added a dense layer with 128 units and a dropout rate of 0.5 to prevent overfitting. The output layer has 43 units (one for each traffic sign category) with a softmax activation function.

## Results
The final model achieved high accuracy on the test set. The combination of the convolutional layer, a dense layer with dropout, and the Adam optimizer proved to be effective.

```
accuracy: 0.9707 - loss: 0.1016
```

## Conclusion
Through experimentation, we learned the importance of model depth and regularization techniques in training a CNN for image classification. Future work could involve hyperparameter tuning and data augmentation to further improve model performance.
