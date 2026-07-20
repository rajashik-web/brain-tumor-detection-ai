from pathlib import Path


# Project Paths
BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

MODEL_PATH = (
    BASE_DIR.parent
    / "model_training"
    / "saved_models"
    / "brain_tumor_model.keras"
)

# Allowed Image Types
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png"
}

# Maximum Upload Size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024