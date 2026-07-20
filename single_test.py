import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(
    "model_training/saved_models/efficientnet_finetuned.keras"
)

dataset = tf.keras.utils.image_dataset_from_directory(
    "single_test",
    image_size=(224,224),
    batch_size=1,
    shuffle=False
)

print("Classes:", dataset.class_names)

for images, labels in dataset:

    pred = model.predict(images, verbose=0)[0]

    print("True Label:", labels.numpy()[0])

    print("Prediction:", np.argmax(pred))

    print(pred)