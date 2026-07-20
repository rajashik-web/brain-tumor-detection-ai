from pathlib import Path

path = Path("model_training/saved_models/efficientnet_finetuned.keras")

print("Exists:", path.exists())
print("Size:", path.stat().st_size)