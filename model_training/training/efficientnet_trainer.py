import tensorflow as tf

from model_training.configs.config import (
    TRAIN_DIR,
    TEST_DIR,
)

from model_training.configs.training_config import (
    LEARNING_RATE,
    OPTIMIZER,
    LOSS,
    METRICS,
    EPOCHS,
)

from model_training.data_loader import DatasetLoader

from model_training.models.efficientnet_model import (
    EfficientNetModel,
)

class EfficientNetTrainer:

    def __init__(self):

        self.loader = DatasetLoader()

        self.model = EfficientNetModel().build()
        
    def load_data(self):

        train_dataset = self.loader.prepare_dataset(TRAIN_DIR)

        validation_dataset = self.loader.prepare_dataset(TEST_DIR)

        return train_dataset, validation_dataset
    

    def compile_model(self):

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(
                learning_rate=LEARNING_RATE
            ),
            loss=LOSS,
            metrics=METRICS,
        )
        
    def get_callbacks(self):

        checkpoint = tf.keras.callbacks.ModelCheckpoint(

            filepath="model_training/checkpoints/efficientnet_best.keras",

            monitor="val_accuracy",

            save_best_only=True,

            verbose=1,
        )

        early_stop = tf.keras.callbacks.EarlyStopping(

            monitor="val_accuracy",

            patience=5,

            restore_best_weights=True,
        )

        csv_logger = tf.keras.callbacks.CSVLogger(

            "model_training/logs/efficientnet_training.csv"
        )

        return [

            checkpoint,

            early_stop,

            csv_logger,
        ]
        
    def train(self):

        train_dataset, validation_dataset = self.load_data()

        self.compile_model()
        
        for images, labels in train_dataset.take(1):
            print("Image Shape:", images.shape)
            print("Min:", tf.reduce_min(images).numpy())
            print("Max:", tf.reduce_max(images).numpy())
            print("Mean:", tf.reduce_mean(images).numpy())
            print("Labels:", labels[:10].numpy())

        history = self.model.fit(

            train_dataset,

            validation_data=validation_dataset,

            epochs=EPOCHS,

            callbacks=self.get_callbacks(),
        )

        return history
    
    def save_model(self):

        self.model.save(

            "model_training/saved_models/efficientnet_final.keras"
        )
        
def main():

    trainer = EfficientNetTrainer()

    trainer.train()

    trainer.save_model()


if __name__ == "__main__":

    main()