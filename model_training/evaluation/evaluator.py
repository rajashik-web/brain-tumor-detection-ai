import numpy as np
import tensorflow as tf
from pathlib import Path

from model_training.configs.config import TEST_DIR
from model_training.data_loader import DatasetLoader
from model_training.evaluation.metrics import calculate_metrics


MODEL_PATH = Path(
    "model_training/saved_models/efficientnet_finetuned.keras"
)


class ModelEvaluator:

    def __init__(self, model_path: Path):

        self.loader = DatasetLoader()

        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = tf.keras.models.load_model(
            self.model_path
        )

    def load_test_data(self):

        return self.loader.prepare_dataset(TEST_DIR)

    def predict(self):

        dataset = self.load_test_data()

        y_true = []
        y_pred = []

        for images, labels in dataset:

            predictions = self.model.predict(
                images,
                verbose=0,
            )

            predicted_classes = np.argmax(
                predictions,
                axis=1,
            )

            y_true.extend(labels.numpy())
            y_pred.extend(predicted_classes)

        return np.array(y_true), np.array(y_pred)

    def evaluate(self):

        y_true, y_pred = self.predict()

        accuracy, report, matrix = calculate_metrics(
            y_true,
            y_pred,
        )

        print("=" * 60)
        print(f"Model: {self.model_path.name}")
        print("=" * 60)
        print(f"Accuracy : {accuracy:.4f}")
        print("=" * 60)
        print(report)
        print("=" * 60)
        print("Confusion Matrix")
        print(matrix)
        print("=" * 60)

        return accuracy, report, matrix


def main():

    evaluator = ModelEvaluator(MODEL_PATH)

    evaluator.evaluate()


if __name__ == "__main__":
    main()