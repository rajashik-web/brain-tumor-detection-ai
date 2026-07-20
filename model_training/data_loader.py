import tensorflow as tf

from model_training.configs.config import (
    IMAGE_SIZE,
    BATCH_SIZE,
    SEED,
)


class DatasetLoader:

    def __init__(self):
        self.image_size = IMAGE_SIZE
        self.batch_size = BATCH_SIZE
        self.seed = SEED

    def load_dataset(self, dataset_directory, subset=None):

        if subset is None:
            dataset = tf.keras.utils.image_dataset_from_directory(
                dataset_directory,
                labels="inferred",
                label_mode="int",
                image_size=self.image_size,
                batch_size=self.batch_size,
                shuffle=False,
            )
        else:
            dataset = tf.keras.utils.image_dataset_from_directory(
                dataset_directory,
                labels="inferred",
                label_mode="int",
                validation_split=0.2,
                subset=subset,
                seed=self.seed,
                image_size=self.image_size,
                batch_size=self.batch_size,
                shuffle=True,
            )

        return dataset

    def normalize(self, image, label):

        image = tf.cast(image, tf.float32)

        return image, label

    def prepare_dataset(self, dataset_directory, subset=None):

        dataset = self.load_dataset(
            dataset_directory,
            subset=subset,
        )

        dataset = dataset.map(
            self.normalize,
            num_parallel_calls=tf.data.AUTOTUNE,
        )

        dataset = dataset.prefetch(tf.data.AUTOTUNE)

        return dataset