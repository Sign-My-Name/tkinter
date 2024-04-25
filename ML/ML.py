import tensorflow as tf


loaded_model = tf.keras.models.load_model(r"ML/model/model.h5")

loaded_model.save("testmodel")
