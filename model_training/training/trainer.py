import tensorflow as tf
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    CSVLogger,
)

from model_training.configs.config import (
    TRAIN_DIR,
    TEST_DIR,
)
from model_training.configs.training_config import (
    OPTIMIZER,
    LOSS,
    METRICS,
    EPOCHS,
)


from model_training.data_loader import DatasetLoader
from model_training.models.cnn_model import BrainTumorCNN


class ModelTrainer:

    def __init__(self):

        self.loader = DatasetLoader()

        self.model = BrainTumorCNN().build()

    def load_data(self):

        train_dataset = self.loader.prepare_dataset(TRAIN_DIR)

        test_dataset = self.loader.prepare_dataset(TEST_DIR)

        return train_dataset, test_dataset

    def compile_model(self):

        self.model.compile(optimizer=OPTIMIZER, loss=LOSS, metrics=METRICS)

    def train(self, epochs=EPOCHS):

        train_dataset, test_dataset = self.load_data()

        self.compile_model()

        history = self.model.fit(
            train_dataset,
            validation_data=test_dataset,
            epochs=epochs,
            callbacks=self.get_callbacks(),
        )

        return history

    def save_model(self):

        self.model.save("model_training/saved_models/brain_tumor_cnn.keras")

    def get_callbacks(self):

        checkpoint = ModelCheckpoint(
            filepath="model_training/checkpoints/best_model.keras",
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        )

        early_stopping = EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        )

        csv_logger = CSVLogger("model_training/logs/training_log.csv")

        return [
            checkpoint,
            early_stopping,
            csv_logger,
        ]


def main():

    trainer = ModelTrainer()

    trainer.train(epochs=10)

    trainer.save_model()


if __name__ == "__main__":
    main()
