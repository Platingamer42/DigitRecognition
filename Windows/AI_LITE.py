import numpy as np

class AI_LITE:
    def __init__(self):
        np.set_printoptions(threshold=np.nan, suppress=True)
        self.biases = []
        self.weights = []

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a


    def initialize(self):
        wFile, bFile = open("data/saves/weights.txt", "r"), open("data/saves/biases.txt", "r")
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
        self.biases = biases

def sigmoid(z):
   return 1.0/(1.0+np.exp(-z))