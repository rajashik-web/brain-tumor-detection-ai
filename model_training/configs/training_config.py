import tensorflow as tf


# ==========================
# Model
# ==========================

INPUT_SHAPE = (224, 224, 3)

NUM_CLASSES = 4

# ==========================
# Training
# ==========================

EPOCHS = 15

LEARNING_RATE = 1e-5

BATCH_SIZE = 32

# ==========================
# Optimizer
# ==========================

OPTIMIZER = tf.keras.optimizers.Adam(
    learning_rate=LEARNING_RATE
)

# ==========================
# Loss
# ==========================

LOSS = "sparse_categorical_crossentropy"

# ==========================
# Metrics
# ==========================

METRICS = [
    "accuracy"
]

# ==========================
# CNN
# ==========================

DROPOUT_RATE = 0.5


EARLY_STOPPING_PATIENCE = 5

REDUCE_LR_PATIENCE = 2

MIN_LEARNING_RATE = 1e-7



# ==========================
# Class Labels
# ==========================

CLASS_NAMES = [
    "Glioma",
    "Meningioma",
    "No Tumor",
    "Pituitary",
]