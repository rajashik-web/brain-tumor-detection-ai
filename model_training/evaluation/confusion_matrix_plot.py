from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

from model_training.evaluation.evaluator import (
    MODEL_PATH,
    ModelEvaluator,
)


class ConfusionMatrixPlotter:

    def __init__(self):

        self.evaluator = ModelEvaluator(MODEL_PATH)

        self.output_dir = Path(
            "model_training/reports/figures"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def plot(self):

        y_true, y_pred = self.evaluator.predict()

        matrix = confusion_matrix(
            y_true,
            y_pred,
        )

        class_names = [
            "Glioma",
            "Meningioma",
            "No Tumor",
            "Pituitary",
        ]

        display = ConfusionMatrixDisplay(
            confusion_matrix=matrix,
            display_labels=class_names,
        )

        fig, ax = plt.subplots(figsize=(8, 8))

        display.plot(
    cmap="Blues",
    ax=ax,
    colorbar=False,
    values_format="d",
)

        plt.title("Confusion Matrix")

        plt.tight_layout()

        plt.savefig(
            self.output_dir / "confusion_matrix.png",
            dpi=300,
        )

        plt.close()

        print("Confusion matrix saved successfully.")
        
def main():

    plotter = ConfusionMatrixPlotter()

    plotter.plot()


if __name__ == "__main__":

    main()