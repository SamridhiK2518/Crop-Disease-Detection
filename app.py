"""Flask web app for crop disease detection.

Run:
    python app.py
Then open http://127.0.0.1:5000
"""

import io
import json
import os

import numpy as np
from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError

from disease_info import get_info

MODEL_PATH = os.path.join("model", "crop_model.keras")
CLASSES_PATH = os.path.join("model", "class_names.json")
IMG_SIZE = (128, 128)
CONFIDENCE_THRESHOLD = 0.50
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit

model = None
class_names = []


def load_model():
    """Load the trained CNN once at startup."""
    global model, class_names
    if not (os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH)):
        print("WARNING: Trained model not found. Run train_model.py first.")
        return
    import tensorflow as tf

    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASSES_PATH) as f:
        class_names = json.load(f)
    print(f"Model loaded with {len(class_names)} classes.")


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html", model_ready=model is not None)


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model is not trained yet. Run train_model.py first."}), 503

    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify({"error": "Please choose an image."}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Only JPG, PNG or WEBP images are allowed."}), 400

    try:
        img = Image.open(io.BytesIO(file.read())).convert("RGB").resize(IMG_SIZE)
    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "That file is not a valid image."}), 400

    arr = np.expand_dims(np.array(img, dtype="float32"), axis=0)  # rescaling is inside the model
    probs = model.predict(arr, verbose=0)[0]

    top_idx = probs.argsort()[::-1][:3]
    top3 = []
    for i in top_idx:
        info = get_info(class_names[i])
        top3.append(
            {
                "label": f"{info['crop']} - {info['disease']}",
                "confidence": round(float(probs[i]) * 100, 2),
            }
        )

    best = get_info(class_names[top_idx[0]])
    best_conf = float(probs[top_idx[0]])

    return jsonify(
        {
            "crop": best["crop"],
            "disease": best["disease"],
            "is_healthy": best["is_healthy"],
            "confidence": round(best_conf * 100, 2),
            "low_confidence": best_conf < CONFIDENCE_THRESHOLD,
            "description": best["description"],
            "treatment": best["treatment"],
            "prevention": best["prevention"],
            "top3": top3,
        }
    )


@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "Image is too large. Maximum size is 5 MB."}), 413


if __name__ == "__main__":
    load_model()
    app.run(debug=False)
