import keras, os
from keras.datasets import mnist
from keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D
from keras.models import Sequential
from MNIST_LOADER import MNIST_LOADER

# input image dimensions
img_x, img_y = 28, 28

loader = MNIST_LOADER()
loader.loadMNIST("/../Windows/data/datasets/mnist.pkl.gz")

# load the MNIST data set, which already splits into train and test sets for us
train_images, train_labels, test_images, test_labels = loader.getData()

#RESHAPE
train_images = train_images.reshape(train_images.shape[0], img_x, img_y, 1)
test_images = test_images.reshape(test_images.shape[0], img_x, img_y, 1)
input_shape = (img_x, img_y, 1)

model = Sequential()


try:
        model = keras.models.load_model("cnn.h5")
except OSError:

        model.add(Dropout(0.20))
        #CONV1
        model.add(Conv2D(32, kernel_size=(3, 3),
                activation='relu',
                input_shape=input_shape))
        #pool1
        model.add(MaxPooling2D(pool_size=(2, 2)))
        
        
        model.add(Dropout(0.25))
        #CONV2
        model.add(Conv2D(64, kernel_size=(2, 2),
                activation='relu',
                input_shape=input_shape))
        #pool2
        model.add(MaxPooling2D(pool_size=(2, 2)))

        #-> Fully connected Layer
        model.add(Flatten())

        #-> Relu & Output
        model.add(Dropout(0.25))
        model.add(Dense(128, activation='relu'))

        model.add(Dropout(0.50))
        model.add(Dense(10, activation='softmax'))
        
        #AdaDelta ~ "smart" learning rate
        model.compile(optimizer=keras.optimizers.Adadelta(), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

model.save("cnn_last.h5")

model.fit(train_images, train_labels,
        batch_size=50,
        epochs=16,
        verbose=1, #PRINTING
        validation_data=(test_images, test_labels))

model.save("cnn.h5")