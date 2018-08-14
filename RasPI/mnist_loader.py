import gzip, pickle, os

class MNIST_LOADER:    
    def loadMNIST(self):
        f = gzip.open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/mnist.pkl.gz", "rb")
        self.train_images, self.train_labels, self.test_images, self.test_labels = pickle.load(f, encoding="latin1")
        f.close()
    def getData(self):
        return self.train_images, self.train_labels, self.test_images, self.test_labels