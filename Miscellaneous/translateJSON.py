import json, os
import numpy as np

wfileold, bfileold = open(os.path.dirname(os.path.realpath(__file__)) + "/data/saves/weights.txt", "r"), open(os.path.dirname(os.path.realpath(__file__)) + "/data/saves/biases.txt", "r")
weights = []
biases = []

for line in wfileold:
    lst = eval(line) 
    weights.append(np.asarray(lst))
for line in bfileold:
    lst = eval(line)
    biases.append(np.asarray(lst))

wfileold.close()
bfileold.close()

data = {"w": [weight.tolist() for weight in weights],
        "b": [bias.tolist() for bias in biases]}

filenew = open(os.path.dirname(os.path.realpath(__file__)) + "/data/saves/network", "w")
json.dump(data, filenew)
