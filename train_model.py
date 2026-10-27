"""
Train a Convolutional Neural Network (CNN) for crop disease detection.

Dataset: PlantVillage (download from Kaggle: "PlantVillage Dataset" / "New Plant Diseases Dataset").
Expected folder structure:

    dataset/
        Tomato___Early_blight/
            img1.jpg
            ...
        Tomato___healthy/
        Potato___Late_blight/
        ...

Run:
    python train_model.py
"""

import json
import os

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks

# ---------------- Configuration ----------------
DATASET_DIR = "dataset"
MODEL_DIR = "model"
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.2
SEED = 42

os.makedirs(MODEL_DIR, exist_ok=True)

# ---------------- Load data ----------------
print("Loading dataset...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_DIR,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Found {num_classes} classes: {class_names}")

# Save class names so the web app can use them
with open(os.path.join(MODEL_DIR, "class_names.json"), "w") as f:
    json.dump(class_names, f, indent=2)

# Speed up input pipeline
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# ---------------- Build CNN ----------------
data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.1),
    ],
    name="augmentation",
)


def conv_block(x, filters):
    x = layers.Conv2D(filters, (3, 3), padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2))(x)
    return x


inputs = layers.Input(shape=IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = layers.Rescaling(1.0 / 255)(x)  # normalization happens inside the model

x = conv_block(x, 32)
x = conv_block(x, 64)
x = conv_block(x, 128)
x = conv_block(x, 256)

x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.4)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(inputs, outputs, name="crop_disease_cnn")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)
model.summary()

# ---------------- Train ----------------
cbs = [
    callbacks.ModelCheckpoint(
        os.path.join(MODEL_DIR, "crop_model.keras"),
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1,
    ),
    callbacks.EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True),
    callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=2, verbose=1),
]

history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=cbs)

# ---------------- Evaluate + plot ----------------
loss, acc = model.evaluate(val_ds)
print(f"\nFinal validation accuracy: {acc * 100:.2f}%")

plt.figure(figsize=(11, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="Train")
plt.plot(history.history["val_accuracy"], label="Validation")
plt.title("Accuracy")
plt.xlabel("Epoch")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="Train")
plt.plot(history.history["val_loss"], label="Validation")
plt.title("Loss")
plt.xlabel("Epoch")
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(MODEL_DIR, "training_curves.png"), dpi=150)
print("Saved model, class names and training curves in the 'model' folder.")
