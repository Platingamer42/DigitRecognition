from keras import models

class AI_KERAS:
    def __init__(self):
        self.model = models.load_model("data/saves/model_keras.h5")
    
    def sendThrough(self, x):
        output = self.model.predict(x)
        return output