from pathlib import Path
from collections import Counter
from tqdm import tqdm

from PIL import Image
from PIL import UnidentifiedImageError

from model_training.configs.config import (
    TRAIN_DIR,
    TEST_DIR,
)

from model_training.utils.file_utils import get_image_files


def count_images(directory: Path):
    """
    Count images inside each class folder.
    """

    counts = {}

    for class_dir in tqdm(
        sorted(directory.iterdir()), desc=f"Counting classes ({directory.name})"
    ):

        if not class_dir.is_dir():
            continue

        images = get_image_files(class_dir)

        counts[class_dir.name] = len(images)

    return counts


def find_corrupt_images(directory: Path):
    """
    Find corrupted or unreadable images.
    """

    corrupt_images = []

    image_files = get_image_files(directory)

    for image_path in tqdm(
        image_files, desc=f"Checking corrupt images ({directory.name})"
    ):

        try:
            with Image.open(image_path) as img:
                img.verify()

        except (UnidentifiedImageError, OSError, IOError):
            corrupt_images.append(image_path)

    return corrupt_images


def analyze_image_sizes(directory: Path):
    """
    Analyze image dimensions.
    """

    image_files = get_image_files(directory)

    widths = []
    heights = []
    resolutions = Counter()

    for image_path in tqdm(
        image_files, desc=f"Analyzing image sizes ({directory.name})"
    ):

        with Image.open(image_path) as img:

            width, height = img.size

            widths.append(width)
            heights.append(height)

            resolutions[(width, height)] += 1

    return {
        "min_width": min(widths),
        "max_width": max(widths),
        "avg_width": sum(widths) / len(widths),
        "min_height": min(heights),
        "max_height": max(heights),
        "avg_height": sum(heights) / len(heights),
        "unique_resolutions": len(resolutions),
        "most_common": resolutions.most_common(5),
    }


def analyze_image_properties(directory: Path):
    """
    Analyze image formats and color modes.
    """

    image_files = get_image_files(directory)

    formats = Counter()
    color_modes = Counter()

    for image_path in tqdm(
        image_files, desc=f"Analyzing image properties ({directory.name})"
    ):

        with Image.open(image_path) as img:

            formats[img.format] += 1
            color_modes[img.mode] += 1

    return {
        "formats": formats,
        "color_modes": color_modes,
    }


def print_image_size_report(title, report):

    print("=" * 50)
    print(title)
    print("=" * 50)

    print(f"Minimum Width  : {report['min_width']}")
    print(f"Maximum Width  : {report['max_width']}")
    print(f"Average Width  : {report['avg_width']:.2f}")

    print()

    print(f"Minimum Height : {report['min_height']}")
    print(f"Maximum Height : {report['max_height']}")
    print(f"Average Height : {report['avg_height']:.2f}")

    print()

    print(f"Unique Resolutions : {report['unique_resolutions']}")

    print()

    print("\nMost Common Resolutions")

    for resolution, count in report["most_common"]:
        print(f"{resolution} -> {count}")

    print()


def print_summary(name, counts):

    print("=" * 50)
    print(name)
    print("=" * 50)

    total = 0

    for cls, count in counts.items():

        print(f"{cls:<20}{count}")

        total += count

    print("-" * 50)

    print(f"Total Images : {total}")

    print()


def print_image_property_report(title, report):

    print("=" * 50)
    print(title)
    print("=" * 50)

    print("Image Formats")

    for image_format, count in report["formats"].items():
        print(f"{image_format:<10}{count}")

    print()

    print("Color Modes")

    for mode, count in report["color_modes"].items():
        print(f"{mode:<10}{count}")

    print()


def print_corrupt_images(corrupt_images):

    print("=" * 50)
    print("CORRUPT IMAGE REPORT")
    print("=" * 50)

    if not corrupt_images:
        print("No corrupt images found.\n")
        return

    print(f"Total Corrupt Images : {len(corrupt_images)}\n")

    for image in corrupt_images:
        print(image)

    print()


def main():

    train_counts = count_images(TRAIN_DIR)
    test_counts = count_images(TEST_DIR)

    print_summary("TRAIN DATASET", train_counts)
    print_summary("TEST DATASET", test_counts)

    train_corrupt = find_corrupt_images(TRAIN_DIR)
    test_corrupt = find_corrupt_images(TEST_DIR)

    print_corrupt_images(train_corrupt)
    print_corrupt_images(test_corrupt)

    train_sizes = analyze_image_sizes(TRAIN_DIR)
    test_sizes = analyze_image_sizes(TEST_DIR)

    print_image_size_report("TRAIN DATASET IMAGE SIZES", train_sizes)
    print_image_size_report("TEST DATASET IMAGE SIZES", test_sizes)

    train_properties = analyze_image_properties(TRAIN_DIR)
    test_properties = analyze_image_properties(TEST_DIR)

    print_image_property_report("TRAIN IMAGE PROPERTIES", train_properties)

    print_image_property_report("TEST IMAGE PROPERTIES", test_properties)


if __name__ == "__main__":
    main()
