import numpy as np
import os, json

class AI_LITE:
    def __init__(self):
        np.set_printoptions(threshold=np.nan, suppress=True)
        self.biases = []
        self.weights = []

    def feedforward(self, a):
        a = np.reshape(a, (len(a), 1))
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    '''
    def initialize(self):
        wFile, bFile = open(os.path.dirname(os.path.realpath(__file__)) + "/data/saves/weights.txt", "r"), open(os.path.dirname(os.path.realpath(__file__)) + "/data/saves/biases.txt", "r")
        weights = []
        biases = []

        for line in wFile:
            lst = eval(line) 
            weights.append(np.asarray(lst))
        for line in bFile:
            lst = eval(line)
            biases.append(np.asarray(lst))

        wFile.close()
        bFile.close()

        self.weights = weights
        self.biases = biases'''
    def initialize(self):
        f = open(os.path.dirname(os.path.realpath(__file__)) + "/data/saves/network", "r")
        data = json.load(f)
        f.close()
        self.weights = [np.array(w) for w in data["w"]]
        self.biases = [np.array(b) for b in data["b"]]

def sigmoid(z):
   return 1.0/(1.0+np.exp(-z))