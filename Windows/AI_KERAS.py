from keras import models
import numpy as np

class AI_KERAS:
    cnn = True

    def __init__(self):
        self.model = models.load_model("data/saves/model_cnn (3).h5")

    def sendThrough(self, x):
        if self.cnn:
            x = x.reshape(1,28,28,1)
            output = self.model.predict(x)
            print(output)
        else:
            output = self.model.predict(x)
        return output