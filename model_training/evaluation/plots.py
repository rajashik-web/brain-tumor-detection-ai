from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


class TrainingPlotter:

    def __init__(self, csv_path):

        self.csv_path = Path(csv_path)

        if not self.csv_path.exists():
            raise FileNotFoundError(f"Training log not found: {self.csv_path}")

        self.history = pd.read_csv(self.csv_path)

        self.output_dir = Path("model_training/reports/figures")

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def plot_accuracy(self):

        plt.figure(figsize=(8, 5))

        plt.plot(
            self.history["accuracy"],
            label="Training Accuracy",
        )

        plt.plot(
            self.history["val_accuracy"],
            label="Validation Accuracy",
        )

        plt.title("Training vs Validation Accuracy")

        plt.xlabel("Epoch")

        plt.ylabel("Accuracy")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / "accuracy_curve.png",
            dpi=300,
        )

        plt.close()

    def plot_loss(self):

        plt.figure(figsize=(8, 5))

        plt.plot(
            self.history["loss"],
            label="Training Loss",
        )

        plt.plot(
            self.history["val_loss"],
            label="Validation Loss",
        )

        plt.title("Training vs Validation Loss")

        plt.xlabel("Epoch")

        plt.ylabel("Loss")

        plt.legend()

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            self.output_dir / "loss_curve.png",
            dpi=300,
        )

        plt.close()

    def create_all(self):

        self.plot_accuracy()

        self.plot_loss()

        print("Training plots saved successfully.")


def main():

    plotter = TrainingPlotter("model_training/logs/efficientnet_finetuned_training.csv")

    plotter.create_all()


if __name__ == "__main__":

    main()
