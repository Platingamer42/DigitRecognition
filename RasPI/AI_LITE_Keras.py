import keras

class AI_LITE_Keras:
    def __init__(self):
        self.model = keras.models.load_model("data/saves/model_keras.h5")
    
    def sendThrough(self, x):
        output = self.model.predict(x)
        return output