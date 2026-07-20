import tensorflow as tf
import numpy as np

MODEL_PATH = "model_training/saved_models/efficientnet_finetuned.keras"

IMAGE_PATH = r"C:\Users\ashik\OneDrive\Desktop\brain-tumor-ai\data\raw\Testing\notumor\Te-no_18.jpg"

CLASS_NAMES = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary",
]

model = tf.keras.models.load_model(MODEL_PATH)

image = tf.keras.utils.load_img(
    IMAGE_PATH,
    target_size=(224, 224)
)

image = tf.keras.utils.img_to_array(image)
image = tf.expand_dims(image, axis=0)

predictions = model.predict(image, verbose=0)[0]

print("=" * 50)
for i, class_name in enumerate(CLASS_NAMES):
    print(f"{class_name:12}: {predictions[i]:.6f}")

predicted_index = np.argmax(predictions)

print("=" * 50)
print("Predicted:", CLASS_NAMES[predicted_index])
print("Confidence:", predictions[predicted_index])
print("=" * 50)

model = tf.keras.models.load_model(
    "model_training/saved_models/efficientnet_finetuned.keras"
)

model.summary()