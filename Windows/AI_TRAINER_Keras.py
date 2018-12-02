import keras
from MNIST_LOADER import MNIST_LOADER
#Could be updated to use the .pkl file. But it's not necessary.

loader = MNIST_LOADER()
loader.loadMNIST()

train_images, train_labels, test_images, test_labels = loader.getData()

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