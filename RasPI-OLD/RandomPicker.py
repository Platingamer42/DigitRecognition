import pickle, gzip, random
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

    #Get a few digits (Only the pixel-values, you know)
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
    

