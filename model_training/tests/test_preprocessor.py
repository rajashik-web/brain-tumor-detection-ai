from model_training.configs.config import (
    TRAIN_DIR,
)

from model_training.preprocessing.dataset_preprocessor import (
    DatasetPreprocessor,
)

def main():

    processor = DatasetPreprocessor()

    X, y, classes = processor.prepare_dataset(
        TRAIN_DIR
    )

    print()

    print("Dataset Loaded Successfully")

    print()

    print("X Shape :", X.shape)

    print("y Shape :", y.shape)

    print()

    print("Classes")

    print(classes)

    print()

    print("Encoded Labels")

    print(y[:10])


if __name__ == "__main__":
    main()