#src: https://github.com/MichalDanielDobrzanski/DeepLearningPython35 
#(Based on the book "Neural Networks and Deep Learning" by Michael A. Nielsen; http://neuralnetworksanddeeplearning.com/)
#Minor changes were made. License:

#MIT License

#Copyright (c) 2012-2018 Michael Nielsen

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
#to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import random, pickle, gzip, os
import numpy as np

class Network:
    def __init__(self, sizes):
        np.set_printoptions(threshold=np.nan, suppress=True)
        self.num_layers = len(sizes)
        self.sizes = sizes
        #input-layer haben weder biases, noch weights
        #-> Daher von 1 bis zum ende der Liste.
        #.randn(LängeLayerX,DimensionOfArray)
        self.biases = [np.random.randn(y,1) for y in sizes[1:]]


        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]
        #zip() returnt ein tuple, eine nicht änderbare Liste
        #Immer 0-0, 1-1 (e.g.: sizes=[1,2,4] -> zip(oben) zu (1,2), (2,4)
        #print(self.weights)
        
    #simply send a variable through the damn network...     
    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a
    #Wir brauchen noch SGD (Stochastic gradient descent) Methode, oder?    
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data = None):
        #replaced xrange (python2) with range
        #Problem: Might be slower (especialliy if the dataset is large!)
        training_data = list(training_data)
        if test_data:
            test_data = list(test_data)
            self.test_data = test_data
            n_test = len(test_data)
            current_peak = 0
            bestWeights = []
            bestBiases = []
        n = len(training_data)
        for j in range(epochs):
            print("Epoch started: {0}".format(j))
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                rate = self.evaluate(self.test_data)
                if (current_peak < rate):
                    current_peak = rate
                    bestWeights = self.weights[:]
                    bestBiases = self.biases[:]
                print("Epoch {0}: {1} / {2}; Peak: {3} / {2}".format(j, rate, n_test, current_peak))   
            else:
                print("Epoch {0} complete".format(j))
        if test_data:
            print("The PEAK was at: {0} / {1}".format(current_peak, n_test))
            self.weights = bestWeights[:]
            self.biases = bestBiases[:]
            #print(self.evaluate(self.test_data))
    def update_mini_batch(self, mini_batch, eta):
        """Update the network's weights and biases by applying
        gradient descent using backpropagation to a single mini batch.
        The "mini_batch" is a list of tuples "(x, y)", and "eta"
        is the learning rate."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w-(eta/len(mini_batch))*nw 
                        for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b-(eta/len(mini_batch))*nb 
                       for b, nb in zip(self.biases, nabla_b)]
    def backprop(self, x, y):
        """Return a tuple ``(nabla_b, nabla_w)`` representing the
        gradient for the cost function C_x.  ``nabla_b`` and
        ``nabla_w`` are layer-by-layer lists of np arrays, similar
        to ``self.biases`` and ``self.weights``."""
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # feedforward
        activation = x
        activations = [x] # list to store all the activations, layer by layer
        zs = [] # list to store all the z vectors, layer by layer
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # backward pass
        delta = self.cost_derivative(activations[-1], y) * \
            sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        # Note that the variable l in the loop below is used a little
        # differently to the notation in Chapter 2 of the book.  Here,
        # l = 1 means the last layer of neurons, l = 2 is the
        # second-last layer, and so on.  It's a renumbering of the
        # scheme in the book, used here to take advantage of the fact
        # that Python can use negative indices in lists.
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose())
        return (nabla_b, nabla_w)

    def evaluate(self, test_data):
        """Return the number of test inputs for which the neural
        network outputs the correct result. Note that the neural
        network's output is assumed to be the index of whichever
        neuron in the final layer has the highest activation."""
        test_results = [(np.argmax(self.feedforward(x)), y)
                        for (x, y) in test_data]
        return sum(int(x == y) for (x, y) in test_results)

    def cost_derivative(self, output_activations, y):
        """Return the vector of partial derivatives partial C_x 
        partial a for the output activations."""
        return (output_activations-y)
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
def sigmoid_prime(z):
    """Derivative of the sigmoid function."""
    return sigmoid(z)*(1-sigmoid(z))


def loadData():
    f = gzip.open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/mnist.pkl.gz", 'rb')
    tr_i, tr_l, te_i, te_l = pickle.load(f, encoding="latin1")
    training_data = [tr_i, tr_l]
    test_data = [te_i, te_l]
    f.close()
    return (training_data, test_data)

def load_data_wrapper():
    tr_d, te_d = loadData()
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, test_data)

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1.0
    return e

training_data, test_data = load_data_wrapper()[0], load_data_wrapper()[1]
net = Network([784,30,10])
net.SGD(training_data,30,10,3,test_data)

b = net.biases[:]
w = net.weights[:]

weights, biases = [], []
wFile = open("/data/saves/weights.txt", "w")
bFile = open("/data/saves/biases.txt", "w")

#safeWeights

for layer in w:
    string = str(layer.tolist()) + "\n"
    wFile.write(string)

#safeBiases
for layer in b:
    string = str(layer.tolist()) + "\n"
    bFile.write(string)


bFile.close()
wFile.close()

net.weights = weights
net.biases = biases
