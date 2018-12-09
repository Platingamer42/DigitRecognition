import pickle, gzip, shutil, os
import numpy as np
import gzip

#_read32, extract_images and extract_labels were published under the following license:

# "Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License."
#WARNING: This script doesn't download the files - They have to be in /data/datasets/MNIST_data/!
#You can download them here: yann.lecun.com/exdb/mnist/

def _read32(bytestream):
    #frombuffer interprets smth. as a 1-D array. See https://docs.scipy.org/doc/numpy/reference/generated/numpy.frombuffer.html
    dt = np.dtype(np.uint32).newbyteorder('>')
    test =  np.frombuffer(bytestream.read(4), dtype=dt)[0]
    return(test)

def extract_images(f):
    with gzip.GzipFile(fileobj=f) as bytestream:
        magic = _read32(bytestream)
        if magic != 2051:
            raise ValueError('Invalid magic number %d in MNIST image file: %s' %
                           (magic, f.name))
        num_images = _read32(bytestream)
        rows = _read32(bytestream)
        cols = _read32(bytestream)
        buf = bytestream.read(rows * cols * num_images)
        data = np.frombuffer(buf, dtype=np.uint8)
        data = data.reshape(num_images, rows, cols, 1)
        assert data.shape[3] == 1
        data = data.reshape(data.shape[0],data.shape[1] * data.shape[2])
        data = data.astype(np.float32)
        data = np.multiply(data, 1.0 / 255.0)
        return data

def extract_labels(f):
    with gzip.GzipFile(fileobj=f) as bytestream:
        magic = _read32(bytestream)
        if magic != 2049:
            raise ValueError('Invalid magic number %d in MNIST label file: %s' %
                           (magic, f.name))
        num_items = _read32(bytestream)
        buf = bytestream.read(num_items)
        labels = np.frombuffer(buf, dtype=np.uint8)
        return labels

with open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/MNIST_data/train-images-idx3-ubyte.gz", "rb") as f:
    train_images = extract_images(f)
with open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/MNIST_data/train-labels-idx1-ubyte.gz", "rb") as f:
    train_labels = extract_labels(f)
with open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/MNIST_data/t10k-images-idx3-ubyte.gz", "rb") as f:
    test_images = extract_images(f)
with open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/MNIST_data/t10k-labels-idx1-ubyte.gz", "rb") as f:   
    test_labels = extract_labels(f)

pickle.dump((train_images,train_labels,test_images,test_labels), open(os.path.dirname(os.path.realpath(__file__)) + "/data/datasets/mnist.pkl", "wb"), protocol=pickle.HIGHEST_PROTOCOL)

with open(os.path.dirname(os.path.realpath(__file__)) + '/data/datasets/mnist.pkl', 'rb') as f:
    with gzip.open(os.path.dirname(os.path.realpath(__file__)) + '/data/datasets/mnist.pkl.gz', 'wb') as gfile:
        shutil.copyfileobj(f, gfile)
os.remove(os.path.dirname(os.path.realpath(__file__)) + '/data/datasets/mnist.pkl')