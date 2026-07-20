from pathlib import Path

import numpy as np
from tqdm import tqdm

from model_training.preprocessing.image_preprocessor import ImagePreprocessor
from model_training.utils.file_utils import get_image_files
from model_training.preprocessing.label_encoder import TumorLabelEncoder

class DatasetPreprocessor:

    def __init__(self):

        self.image_preprocessor = ImagePreprocessor()

        self.label_encoder = TumorLabelEncoder()
        
    def process_class(self, class_directory: Path):

        images = []

        image_files = get_image_files(class_directory)

        for image_path in tqdm(
            image_files,
            desc=f"Processing {class_directory.name}"
        ):

            image = self.image_preprocessor.preprocess(image_path)

            images.append(image)

        return images
    
    
    def process_dataset(self, dataset_directory: Path):

        X = []
        y = []

        class_names = []
    
        for class_directory in sorted(dataset_directory.iterdir()):

            if not class_directory.is_dir():
                continue

            class_names.append(class_directory.name)

            images = self.process_class(class_directory)

            X.extend(images)

            y.extend(
                [class_directory.name] * len(images)
            )

        return (
            np.array(X),
            np.array(y),
            class_names,
        )
        
    def prepare_dataset(self, dataset_directory):

        X, y, class_names = self.process_dataset(
            dataset_directory
        )

        y = self.label_encoder.fit_transform(y)

        return (
            X,
            y,
            class_names,
    )
    