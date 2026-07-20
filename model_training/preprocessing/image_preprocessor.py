from pathlib import Path

import numpy as np
from PIL import Image

from model_training.configs.config import IMAGE_SIZE

class ImagePreprocessor:
    """
    Preprocess a single image.
    """

    def __init__(self, image_size=IMAGE_SIZE):
        self.image_size = image_size
        
    def load_image(self, image_path: Path):

        return Image.open(image_path)
    
    def convert_to_rgb(self, image: Image.Image):

        return image.convert("RGB")
    
    def resize(self, image: Image.Image):

        return image.resize(self.image_size)
    
    def to_numpy(self, image: Image.Image):

        return np.array(image)
    
    def normalize(self, image):

        image = image.astype(np.float32)

        image /= 255.0

        return image
    
    def preprocess(self, image_path: Path):

        image = self.load_image(image_path)

        image = self.convert_to_rgb(image)

        image = self.resize(image)

        image = self.to_numpy(image)

        image = self.normalize(image)

        return image