import tensorflow as tf
import numpy as np

MODEL_PATH = "model_training/saved_models/efficientnet_finetuned.keras"
IMAGE_PATH = r"C:\Users\ashik\OneDrive\Desktop\brain-tumor-ai\data\raw\Testing\notumor\Te-no_18.jpg"

model = tf.keras.models.load_model(MODEL_PATH)

dataset = tf.keras.utils.image_dataset_from_directory(
    r"C:\Users\ashik\OneDrive\Desktop\brain-tumor-ai\data\raw\Testing",
    labels="inferred",
    label_mode="int",
    image_size=(224, 224),
    batch_size=1,
    shuffle=False,
)

print("Class names:", dataset.class_names)

for images, labels in dataset:
    pred = model.predict(images, verbose=0)
    predicted = np.argmax(pred)

    print("True Label:", labels.numpy()[0])
    print("Predicted Label:", predicted)
    print("Probabilities:", pred[0])

    break