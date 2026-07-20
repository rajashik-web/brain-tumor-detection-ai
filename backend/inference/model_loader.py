import tensorflow as tf

from model_training.configs.config import MODEL_PATH


class ModelLoader:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading model...")

            cls._model = tf.keras.models.load_model(
                MODEL_PATH
            )

            print("Model loaded successfully.")

        return cls._model