# Experimentation Process

## Introduction
In this project, we aim to classify traffic signs using a convolutional neural network (CNN). We experimented with various configurations of convolutional and pooling layers, hidden layers, and dropout to achieve optimal performance.

## Data Preprocessing
We used OpenCV to read and resize images. Each image was resized to 30x30 pixels to maintain consistency across the dataset.

## Model Architecture
The final model architecture consists of three convolutional layers with increasing filter sizes (32, 64, 128), each followed by a max-pooling layer to reduce dimensionality. After flattening the output, we added a dense layer with 128 units and a dropout rate of 0.5 to prevent overfitting. The output layer has 43 units (one for each traffic sign category) with a softmax activation function.

## Experiments
1. **Initial Model**: We started with two convolutional layers and a single dense layer. This model achieved decent accuracy but was prone to overfitting.
2. **Adding Dropout**: Introducing a dropout layer improved generalization by reducing overfitting.
3. **Increasing Convolutional Layers**: Adding a third convolutional layer significantly improved accuracy by allowing the model to learn more complex features.
4. **Adjusting Filter Sizes**: We experimented with different filter sizes and found that increasing the number of filters in deeper layers yielded better performance.

## Results
The final model achieved high accuracy on the test set. The combination of three convolutional layers, a dense layer with dropout, and the Adam optimizer proved to be effective.

## Conclusion
Through experimentation, we learned the importance of model depth and regularization techniques in training a CNN for image classification. Future work could involve hyperparameter tuning and data augmentation to further improve model performance.
