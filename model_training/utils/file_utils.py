from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".tif",
    ".tiff",
}


def get_image_files(directory: Path):
    """
    Return all supported image files recursively.
    """

    image_files = []

    for extension in SUPPORTED_EXTENSIONS:
        image_files.extend(directory.rglob(f"*{extension}"))
        image_files.extend(directory.rglob(f"*{extension.upper()}"))

    return sorted(image_files)


def is_image_file(path: Path):
    return path.suffix.lower() in SUPPORTED_EXTENSIONS