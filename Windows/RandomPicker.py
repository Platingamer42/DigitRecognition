import pickle, gzip, random, mnist_loader_keras
import numpy as np
from PIL import Image

class RandomPicker:
    def __init__(self):
        self.f = gzip.open('data/datasets/mnist.pkl.gz', 'rb')
        self.data = pickle.load(self.f, encoding="latin1")[0]
        self.f.close()
        #These are the digits, now! 
        self.digits = [np.reshape(x, (784, 1)) for x in self.data[0]]
        self.sol = self.data[1]
        #self.images_keras, self.labels_keras = self.loadMNIST_Keras()
        self.images_keras, self.labels_keras = pickle.load(open("data/datasets/mnistkeras.pkl","rb"))[0], pickle.load(open("data/datasets/mnistkeras.pkl","rb"))[1]

    #NIU, since pickle.load is used.
    def loadMNIST_Keras(self):
        with open("data/datasets/MNIST_data/t10k-images-idx3-ubyte.gz", "rb") as f:
            test_images = mnist_loader_keras.extract_images(f)
        with open("data/datasets/MNIST_data/t10k-labels-idx1-ubyte.gz", "rb") as f:   
            test_labels = mnist_loader_keras.extract_labels(f)
        return test_images, test_labels

    #Get a few digits (Only the pixel-values, ya know)
    def pickRandom(self):
        #Lets create a pic of a random-digit we pick from the dataset!
        img = Image.new('L', (28,28), (255))
        pixels = img.load()
        x = 0
        digit = random.randrange(len(self.digits))
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                #translate the float-value (black-white) into a "real" 0-255 Value
                pixels[j,i] = int(-self.digits[digit][x]*255+255)
                x +=1
        return img, str(self.sol[digit]), self.digits[digit]
    def pickRandomKeras(self):
        img = Image.new('L', (28,28), (255))
        pixels = img.load()
        x = 0
        digit = random.randrange(len(self.images_keras))
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                #translate the float-value (black-white) into a "real" 0-255 Value
                pixels[j,i] = int(-self.images_keras[digit][x]*255+255)
                x +=1
        return img, str(self.labels_keras[digit]), self.images_keras[digit]

