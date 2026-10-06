"""
Fake News Detector - Flask Application
Serves the web UI and provides the /predict API endpoint.
"""

import os
import re
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Paths for serialized models
MODEL_PATH = os.path.join("model", "model.pkl")
VECTORIZER_PATH = os.path.join("model", "vectorizer.pkl")

# Load model and vectorizer at startup
model = None
vectorizer = None


def load_artifacts():
    """Loads the model and TF-IDF vectorizer once at startup."""
    global model, vectorizer
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("[+] Model and Vectorizer loaded successfully into Flask app.")
        else:
            print(f"[-] Warning: Model artifacts not found at '{MODEL_PATH}' and '{VECTORIZER_PATH}'.")
            print("[-] Please run 'python train_model.py' to generate model artifacts.")
    except Exception as e:
        print(f"[-] Error loading model artifacts: {e}")


def clean_text(text: str) -> str:
    """
    Cleans raw text for NLP model consumption:
    - Lowercases text
    - Removes URLs and hyperlinks
    - Removes HTML tags
    - Strips non-alphabetic characters and punctuation
    - Normalizes extra whitespace
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"<.*?>+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Initialize artifacts
load_artifacts()


@app.route("/")
def index():
    """Renders the main web interface."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    Analyzes submitted news text and returns classification (REAL or FAKE)
    along with confidence score (0-100).
    """
    global model, vectorizer

    # 1. Ensure artifacts are loaded
    if model is None or vectorizer is None:
        load_artifacts()
        if model is None or vectorizer is None:
            return jsonify({
                "error": "Model is not loaded. Please ensure 'train_model.py' has been run to generate the model artifacts."
            }), 500

    # 2. Validate JSON payload
    if not request.is_json:
        return jsonify({"error": "Invalid request content type. Expected application/json."}), 400

    data = request.get_json(silent=True)
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field in JSON payload."}), 400

    raw_text = data.get("text", "")

    if not isinstance(raw_text, str):
        return jsonify({"error": "Field 'text' must be a string."}), 400

    text_stripped = raw_text.strip()

    # 3. Validation: Non-empty
    if not text_stripped:
        return jsonify({"error": "Please enter or paste news text to analyze."}), 400

    # 4. Validation: Minimum 20 words
    words = text_stripped.split()
    word_count = len(words)
    if word_count < 20:
        return jsonify({
            "error": f"Text is too short ({word_count} words). Please enter at least 20 words for a reliable prediction."
        }), 400

    # 5. Validation: Maximum ~5000 characters
    char_count = len(raw_text)
    if char_count > 5000:
        return jsonify({
            "error": f"Text exceeds maximum limit of 5,000 characters (currently {char_count:,} characters). Please shorten your article."
        }), 400

    # 6. Clean text
    cleaned_text = clean_text(raw_text)
    if not cleaned_text:
        return jsonify({
            "error": "The provided text contains insufficient alphabetic words after cleaning. Please input valid article content."
        }), 400

    try:
        # 7. Vectorize
        text_vec = vectorizer.transform([cleaned_text])

        # 8. Predict and Calculate Confidence
        prediction = model.predict(text_vec)[0]  # 1 for REAL, 0 for FAKE

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(text_vec)[0]
            # Identify class index for 0 (FAKE) and 1 (REAL)
            classes = list(model.classes_)
            fake_idx = classes.index(0) if 0 in classes else 0
            real_idx = classes.index(1) if 1 in classes else 1
            prob_fake = float(probabilities[fake_idx])
            prob_real = float(probabilities[real_idx])
        else:
            # Fallback for models without predict_proba using decision_function
            if hasattr(model, "decision_function"):
                decision = float(model.decision_function(text_vec)[0])
                # Sigmoid transformation
                prob_real = float(1.0 / (1.0 + np.exp(-decision)))
                prob_fake = 1.0 - prob_real
            else:
                prob_real = 1.0 if prediction == 1 else 0.0
                prob_fake = 0.0 if prediction == 1 else 1.0

        label = "REAL" if prediction == 1 else "FAKE"
        predicted_confidence = prob_real if prediction == 1 else prob_fake
        confidence_percentage = round(predicted_confidence * 100, 2)

        return jsonify({
            "label": label,
            "confidence": confidence_percentage,
            "probabilities": {
                "real": round(prob_real * 100, 2),
                "fake": round(prob_fake * 100, 2)
            },
            "stats": {
                "word_count": word_count,
                "character_count": char_count
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred while processing the prediction: {str(e)}"
        }), 500


if __name__ == "__main__":
    # Run development server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
