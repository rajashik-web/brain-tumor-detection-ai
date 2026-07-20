import shutil
from pathlib import Path

import tensorflow as tf

from model_training.configs.config import TRAIN_DIR
from model_training.configs.training_config import (
    LOSS,
    METRICS,
    LEARNING_RATE,
    EPOCHS,
    EARLY_STOPPING_PATIENCE,
    REDUCE_LR_PATIENCE,
    MIN_LEARNING_RATE,
)

from model_training.data_loader import DatasetLoader
from model_training.models.efficientnet_finetune import EfficientNetFineTune


class EfficientNetFineTuneTrainer:

    def __init__(self):

        self.loader = DatasetLoader()

        self.model = EfficientNetFineTune().build()

        self.model.summary()

        trainable_params = sum(
            tf.keras.backend.count_params(weight)
            for weight in self.model.trainable_weights
        )

        print("=" * 60)
        print(f"Trainable Parameters : {trainable_params:,}")
        print("=" * 60)

    def load_data(self):

        train_dataset = self.loader.prepare_dataset(
            TRAIN_DIR,
            subset="training",
        )

        validation_dataset = self.loader.prepare_dataset(
            TRAIN_DIR,
            subset="validation",
        )

        return train_dataset, validation_dataset

    def compile_model(self):

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=LEARNING_RATE,
            ),
            loss=LOSS,
            metrics=METRICS,
        )

    def get_callbacks(self):

        checkpoint_dir = Path("model_training/checkpoints")
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

        logs_dir = Path("model_training/logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=str(
                checkpoint_dir / "efficientnet_finetuned.keras"
            ),
            monitor="val_accuracy",
            mode="max",
            save_best_only=True,
            verbose=1,
        )

        reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=REDUCE_LR_PATIENCE,
            min_lr=MIN_LEARNING_RATE,
            verbose=1,
        )

        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
            verbose=1,
        )

        csv_logger = tf.keras.callbacks.CSVLogger(
            str(
                logs_dir /
                "efficientnet_finetuned_training.csv"
            )
        )

        return [
            checkpoint,
            reduce_lr,
            early_stop,
            csv_logger,
        ]

    def train(self):

        train_dataset, validation_dataset = self.load_data()

        self.compile_model()

        history = self.model.fit(
            train_dataset,
            validation_data=validation_dataset,
            epochs=EPOCHS,
            callbacks=self.get_callbacks(),
        )

        return history

    def save_model(self):

        checkpoint = Path(
            "model_training/checkpoints/efficientnet_finetuned.keras"
        )

        save_directory = Path(
            "model_training/saved_models"
        )

        save_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        final_model = (
            save_directory /
            "efficientnet_finetuned.keras"
        )

        if not checkpoint.exists():
            raise FileNotFoundError(
                f"Checkpoint not found: {checkpoint}"
            )

        shutil.copy2(
            checkpoint,
            final_model,
        )

        print("=" * 60)
        print("Training completed successfully.")
        print(f"Best model saved to:\n{final_model}")
        print("=" * 60)


def main():

    trainer = EfficientNetFineTuneTrainer()

    history = trainer.train()

    trainer.save_model()

    return history


if __name__ == "__main__":

    main()