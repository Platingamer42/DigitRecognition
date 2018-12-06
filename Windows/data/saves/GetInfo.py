from keras import models
import os, gzip, pickle

if __name__ == "__main__":
    model_arr = []
    for file in os.listdir():
        if "model_keras" in file:
            model_arr.append(file)
        f = gzip.open("../datasets/mnist.pkl.gz", "rb")
    train_images, train_labels, test_images, test_labels = pickle.load(f, encoding="latin1")
    
    f.close()
    for m in model_arr:
        try:
            model = models.load_model(m)
            foo, accuracy = model.evaluate(test_images, test_labels)
            print("file: {}; accuracy: {}".format(m, accuracy))
        except ValueError:
            print("Error reading file: {}".format(m))
            
        
