import mnist_loader_keras, pickle

with open("data/datasets/MNIST_data/train-images-idx3-ubyte.gz", "rb") as f:
    train_images = mnist_loader_keras.extract_images(f)
with open("data/datasets/MNIST_data/train-labels-idx1-ubyte.gz", "rb") as f:
    train_labels = mnist_loader_keras.extract_labels(f)
with open("data/datasets/MNIST_data/t10k-images-idx3-ubyte.gz", "rb") as f:
    test_images = mnist_loader_keras.extract_images(f)
with open("data/datasets/MNIST_data/t10k-labels-idx1-ubyte.gz", "rb") as f:   
    test_labels = mnist_loader_keras.extract_labels(f)

pickle.dump((train_images,train_labels,test_images,test_labels), open("data/datasets/mnistkeras.pkl", "wb"), protocol=pickle.HIGHEST_PROTOCOL)

