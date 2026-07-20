import numpy as np

from model_training.configs.training_config import (
    CLASS_NAMES,
)


class PostProcessor:

    def __init__(self):

        self.class_names = CLASS_NAMES

    def get_prediction(self, probabilities):

        prediction_index = int(
            np.argmax(probabilities)
        )

        prediction = self.class_names[
            prediction_index
        ]

        confidence = float(
            probabilities[prediction_index]
        )

        return prediction, confidence

    def get_probabilities(self, probabilities):

        return {
            class_name: float(probability)
            for class_name, probability in zip(
                self.class_names,
                probabilities,
            )
        }

    def process(self, probabilities):

        prediction, confidence = self.get_prediction(
            probabilities
        )

        return {
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": self.get_probabilities(
                probabilities
            ),
        }