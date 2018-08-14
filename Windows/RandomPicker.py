import pickle, gzip, random
import numpy as np
from PIL import Image
import os, gzip

class RandomPicker:
    def __init__(self, mnist_loader):
        self.images, self.labels = mnist_loader.getData()[2:]

    #Get a few digits (Only the pixel-values, ya know)
    def pickRandom(self):
        #Lets create a pic of a random-digit we pick from the dataset!
        img = Image.new('L', (28,28), (255))
        pixels = img.load()
        x = 0
        digit = random.randrange(len(self.images))
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                #translate the float-value (black-white) into a "real" 0-255 Value
                pixels[j,i] = int(-self.images[digit][x]*255+255)
                x +=1
        return img, str(self.labels[digit]), self.images[digit]
    

