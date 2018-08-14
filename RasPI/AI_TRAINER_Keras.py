import keras
from mnist_loader_keras import extract_images, extract_labels

#Could be updated to use the .pkl file. But it's not necessary.

with open("data/datasets/MNIST_data/train-images-idx3-ubyte.gz", "rb") as f:
    train_images = extract_images(f)
with open("data/datasets/MNIST_data/train-labels-idx1-ubyte.gz", "rb") as f:
    train_labels = extract_labels(f)
with open("data/datasets/MNIST_data/t10k-images-idx3-ubyte.gz", "rb") as f:
    test_images = extract_images(f)
with open("data/datasets/MNIST_data/t10k-labels-idx1-ubyte.gz", "rb") as f:   
    test_labels = extract_labels(f)

#Main-idea for the values: https://machinelearningmastery.com/dropout-regularization-deep-learning-models-keras/
model = keras.Sequential([
    keras.layers.Dropout(0.2),
    keras.layers.Dense(784, activation="relu", input_shape=(784,)),
    
    keras.layers.Dropout(0.2),
    keras.layers.Dense(145, activation="relu"),
    
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="SGD", lr=0.5, momentum=0.95, 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=100, batch_size=20)

loss, accuracy = model.evaluate(test_images, test_labels)

print('accuracy:{}; loss: {}'.format(accuracy, loss))

model.save("data/saves/model_keras.h5")