import keras
from mnist_loader_keras import extract_images, extract_labels

class AI_LITE_Keras:
    def __init__(self):
        self.model = keras.models.load_model("data/saves/model_keras.h5")
    def loadDataset(self):
        with open("data/datasets/MNIST_data/train-images-idx3-ubyte.gz", "rb") as f:
            train_images = extract_images(f)
        with open("data/datasets/MNIST_data/train-labels-idx1-ubyte.gz", "rb") as f:
            train_labels = extract_labels(f)
        with open("data/datasets/MNIST_data/t10k-images-idx3-ubyte.gz", "rb") as f:
            test_images = extract_images(f)
        with open("data/datasets/MNIST_data/t10k-labels-idx1-ubyte.gz", "rb") as f:   
            test_labels = extract_labels(f)
        #This has no use, at the moment.

    def sendThrough(self, x):
        output = self.model.predict(x)
        return output