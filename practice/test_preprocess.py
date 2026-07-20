from backend.inference.preprocess import ImagePreprocessor

preprocessor = ImagePreprocessor()

tensor = preprocessor.preprocess("single_test/notumor/Te-no_18.jpg")

print(tensor.shape)
print(tensor.dtype)