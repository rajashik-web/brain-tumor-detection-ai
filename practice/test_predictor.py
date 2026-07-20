from pathlib import Path

from backend.inference.predictor import Predictor

predictor = Predictor()

image_path = Path("single_test") / "notumor" / "Te-no_18.jpg"

probabilities = predictor.predict(str(image_path))

print("Shape:", probabilities.shape)
print("\nProbabilities:")
print(probabilities)