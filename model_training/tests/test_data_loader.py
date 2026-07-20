from model_training.configs.config import TRAIN_DIR
from model_training.data_loader import DatasetLoader


def main():

    loader = DatasetLoader()

    dataset = loader.prepare_dataset(TRAIN_DIR)

    print()

    print(dataset)

    print()

    for images, labels in dataset.take(1):

        print("Images Shape :", images.shape)
        print("Labels Shape :", labels.shape)

        print()

        print("Minimum Pixel :", images.numpy().min())
        print("Maximum Pixel :", images.numpy().max())

        print()

        print("Labels")

        print(labels.numpy())


if __name__ == "__main__":
    main()