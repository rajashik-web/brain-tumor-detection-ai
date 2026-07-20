import tensorflow as tf

print("=" * 50)
print("TensorFlow Version:", tf.__version__)
print("=" * 50)

print("GPU Available:", tf.config.list_physical_devices("GPU"))

print("CPU Available:", tf.config.list_physical_devices("CPU"))