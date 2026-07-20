import numpy as np

from backend.inference.model_loader import ModelLoader
from backend.inference.preprocess import ImagePreprocessor

class Predictor:

    def __init__(self):

        self.model = ModelLoader.get_model()

        self.preprocessor = ImagePreprocessor()

    def predict(self, image_path):

        image_tensor = self.preprocessor.preprocess(image_path)

        probabilities = self.model.predict(
            image_tensor,
            verbose=0,
        )[0]
        if probabilities.shape[0] != 4:
            raise ValueError("Unexpected prediction output.")

        return probabilities

    def predict_batch(self, image_paths):

        predictions = []

        for image_path in image_paths:

            probabilities = self.predict(image_path)

            predictions.append(probabilities)

        return np.array(predictions)
