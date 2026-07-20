from backend.inference.model_loader import ModelLoader

loader = ModelLoader()

model1 = loader.get_model()
model2 = loader.get_model()

print("First Model ID :", id(model1))
print("Second Model ID:", id(model2))
print("Same Object:", model1 is model2)