from keras import models
import os, gzip, pickle

if __name__ == "__main__":
    model_arr = []
    model_cnn = []
            
    f = gzip.open("../datasets/mnist.pkl.gz", "rb")
    train_images, train_labels, test_images, test_labels = pickle.load(f, encoding="latin1")
    
    for file in os.listdir():
        if "model_keras" in file:
            model_arr.append(file)
        if "model_cnn" in file:
            model_cnn.append(file)

    
    f.close()
    for m in model_arr:
        try:
            model = models.load_model(m)
            foo, accuracy = model.evaluate(test_images, test_labels)
            print("=======file: {}; accuracy: {}=======".format(m, accuracy))
            model.summary()
            

        except ValueError:
            print("Error reading file: {}".format(m))
    #RESHAPE
    test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)
    for m in model_cnn:
        try:
            model = models.load_model(m)
            foo, accuracy = model.evaluate(test_images, test_labels)
            print("=======file: {}; accuracy: {}=======".format(m, accuracy))
            model.summary()
        except ValueError:
            print("Error")

            
        
