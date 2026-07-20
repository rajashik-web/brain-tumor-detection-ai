from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

TRAIN_DIR = RAW_DATA_DIR / "Training"
TEST_DIR = RAW_DATA_DIR / "Testing"

# Image Settings
IMAGE_SIZE = (224, 224)

# Random Seed
SEED = 42

# Batch Size
BATCH_SIZE = 32

# Epochs (we'll adjust later)
EPOCHS = 20

MODEL_PATH = Path(
    "model_training/saved_models/efficientnet_finetuned.keras"
)