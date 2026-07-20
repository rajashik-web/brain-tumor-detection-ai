from pathlib import Path

from backend.inference.pipeline import InferencePipeline


pipeline = InferencePipeline()

image_path = Path("single_test") / "notumor" / "Te-no_18.jpg"

result = pipeline.predict(str(image_path))

print(result)