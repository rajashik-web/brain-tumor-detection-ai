from pathlib import Path

import tensorflow as tf


class ImagePreprocessor:

    def __init__(
        self,
        image_size=(224, 224),
    ):

        self.image_size = image_size

    def load_image(
        self,
        image_path: str | Path,
    ):

        image = tf.keras.utils.load_img(
            image_path,
            target_size=self.image_size,
        )

        return image

    def image_to_tensor(
        self,
        image,
    ):

        tensor = tf.keras.utils.img_to_array(image)

        tensor = tf.cast(
            tensor,
            tf.float32,
        )

        return tensor

    def add_batch_dimension(
        self,
        tensor,
    ):

        return tf.expand_dims(
            tensor,
            axis=0,
        )

    def preprocess(
        self,
        image_path,
    ):

        image = self.load_image(image_path)

        tensor = self.image_to_tensor(image)

        tensor = self.add_batch_dimension(tensor)

        return tensor