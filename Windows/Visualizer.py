from keras.utils import plot_model
import keras

model = keras.models.load_model("data/saves/model_keras.h5")
plot_model(model, to_file="modeltest.png")