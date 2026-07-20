from backend.inference.predictor import Predictor
from backend.inference.postprocess import PostProcessor


class InferencePipeline:

    def __init__(self):

        self.predictor = Predictor()
        self.postprocessor = PostProcessor()

    def predict(self, image_path: str) -> dict:

        probabilities = self.predictor.predict(image_path)

        result = self.postprocessor.process(probabilities)

        return result