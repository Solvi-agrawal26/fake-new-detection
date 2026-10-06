# Veritas AI - Fake News Detection Web Application

An end-to-end Machine Learning web application designed to analyze and classify news articles and headlines as **REAL** or **FAKE** in real time, accompanied by calibrated confidence scores and linguistic diagnostic metrics.

Built with **Python, Flask, scikit-learn (TF-IDF + Logistic Regression / Passive-Aggressive Classifier)** on the backend, and modern **HTML5, CSS3 (Glassmorphism & Dark/Light modes), and Vanilla JavaScript** on the frontend.

---

## 📸 Overview & Features

- **Real-Time Classification**: Classifies submitted text into `REAL` or `FAKE` with high confidence accuracy.
- **Calibrated Confidence Score**: Shows exact statistical prediction percentage (0–100%) and dual probability distribution (Real % vs Fake %).
- **Rich Modern UI**:
  - Glassmorphic card styling, fluid animations, and custom ambient glowing accents.
  - Dark Mode and Light Mode support with persistent local storage.
  - Live interactive character counter, word counter, and estimated reading time calculator.
  - Visual word progress bar tracking minimum required token thresholds.
  - Instant One-Click Sample News buttons for fast demonstration.
  - Copyable verification report summary.
- **Strict Input Validation**:
  - Non-empty validation.
  - Minimum 20 words for sufficient linguistic feature extraction.
  - Maximum ~5,000 characters limit with inline error messaging.
- **ML Pipeline**:
  - Text normalization: Lowercasing, URL removal, HTML stripping, non-alphabetic filtering, and whitespace trimming.
  - Feature extraction: TF-IDF vectorizer (`max_df=0.7`, `ngram_range=(1,2)`, `stop_words='english'`).
  - Classifier: Calibrated classification engine achieving **97.5%+ test accuracy**.
  - Serialized model persistence using `joblib`.

---

## 📁 Project Structure

```text
Fake New/
├── app.py                  # Flask web server and /predict API endpoints
├── train_model.py          # ML training pipeline, evaluation metrics, and joblib exporter
├── generate_dataset.py     # Starter dataset generator (Kaggle schema compatible)
├── test_app.py             # Automated unit tests for backend API validation
├── requirements.txt        # Pinned Python package dependencies
├── README.md               # Project documentation and deployment guide
├── model/                  # Serialized ML artifacts
│   ├── model.pkl           # Trained classification model
│   └── vectorizer.pkl      # Fitted TF-IDF vectorizer
├── data/                   # Dataset directory (Kaggle True.csv & Fake.csv)
│   ├── True.csv            # Real news articles
│   └── Fake.csv            # Fake / sensationalist news articles
├── templates/
│   └── index.html          # Semantic HTML5 web interface
└── static/
    ├── css/
    │   └── style.css       # Design system, glassmorphism, dark/light themes
    └── js/
        └── script.js       # Client-side validation, async fetch, and animations
```

---

## 🚀 Quickstart Guide

### 1. Clone or Open Workspace
Navigate to the project root directory:
```bash
cd "c:\Users\solvi\OneDrive\Desktop\PROJECT\Fake New"
```

### 2. Create and Activate Virtual Environment (Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 4. (Optional) Generate or Update Dataset
The repository comes pre-bundled with starter datasets in `data/True.csv` and `data/Fake.csv`. You can regenerate them or expand them anytime:
```bash
python generate_dataset.py
```
> **Using Kaggle Dataset**: If you download the full Kaggle *"Fake and Real News Dataset"* (by Clement Bisaillon), simply place `True.csv` and `Fake.csv` directly into the `data/` folder.

### 5. Train the Machine Learning Model
Train the TF-IDF vectorizer and classifier, view the confusion matrix, and export the `.pkl` files into `model/`:

```bash
# Train using Logistic Regression (default, native probabilities)
python train_model.py

# Or train using Calibrated Passive-Aggressive Classifier:
python train_model.py --model passive_aggressive
```

**Sample Output:**
```text
[*] Total dataset size: 200 samples (Real: 100, Fake: 100)
[*] Splitting dataset into 80% train and 20% test sets...
[*] Vectorizing text using TF-IDF (max_df=0.7, stop_words='english')...
    TF-IDF vocabulary size: 3585 features
[*] Training Logistic Regression Classifier...

==================================================
           MODEL EVALUATION RESULTS
==================================================
Model Accuracy: 97.50%

Confusion Matrix:
               Predicted FAKE   Predicted REAL
Actual FAKE:         20             0
Actual REAL:         1              19

Classification Report:
              precision    recall  f1-score   support
    FAKE (0)       0.95      1.00      0.98        20
    REAL (1)       1.00      0.95      0.97        20
==================================================

[+] Model saved to: 'model/model.pkl'
[+] Vectorizer saved to: 'model/vectorizer.pkl'
```

### 6. Run the Flask Web Application
Launch the Flask development server:
```bash
python app.py
```
*Alternatively, you can use the Flask CLI:*
```bash
flask --app app run --port 5000 --debug
```

### 7. Access in Your Browser
Open your browser and navigate to:
```
http://localhost:5000
```
or
```
http://127.0.0.1:5000
```

---

## 🧪 Testing the Application

### Automated API & Unit Tests
Run the automated test suite to verify input validation boundaries (empty string, short text, oversized text) and prediction confidence:
```bash
python test_app.py
```

### Manual Testing with Included Samples
Click the **"Real News"** or **"Fake News"** sample chips directly on the web page to load pre-formatted test articles and click **"Check News Authenticity"**.

---

## ⚙️ How the ML Pipeline Works

1. **Text Preprocessing**: The raw text undergoes lowercasing, hyperlink removal, HTML stripping, removal of non-alphabetic characters, and spacing normalization.
2. **Feature Extraction (TF-IDF)**: Words are weighted by their frequency relative to the corpus. Rare high-signal words receive stronger weights while frequent noise words are filtered with `max_df=0.7` and English stopwords.
3. **Classification & Calibration**: The normalized vector is evaluated by the classifier. The prediction class (Real=1, Fake=0) and class probability distributions are computed.
4. **API Response**: Returns strict JSON format:
   ```json
   {
     "label": "REAL",
     "confidence": 72.22,
     "probabilities": {
       "real": 72.22,
       "fake": 27.78
     },
     "stats": {
       "word_count": 67,
       "character_count": 488
     }
   }
   ```

---

## ⚠️ Disclaimer

> **This tool gives a prediction based on a machine learning model and is not a guarantee of truth.**
> Machine learning algorithms detect statistical patterns and stylistic markers present in training datasets. They cannot substitute for independent verification, primary source investigation, and critical human judgment.

---

## 📜 License
MIT License. Open source for educational and research use.
