"""
Fake News Detection - Model Training Script
Trains a TF-IDF + Logistic Regression / Passive-Aggressive Classifier pipeline
on Real and Fake news datasets and exports model artifacts with joblib.
"""

import os
import re
import argparse
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


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
    
    # 1. Lowercase
    text = text.lower()
    # 2. Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # 3. Remove HTML markup
    text = re.sub(r"<.*?>+", " ", text)
    # 4. Remove punctuation, symbols, and digits (retain letters only)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    # 5. Remove multiple whitespace / newlines
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_dataset(data_dir: str = "data"):
    """
    Loads Real and Fake datasets from CSV.
    Compatible with Kaggle 'Fake and Real News Dataset' (True.csv and Fake.csv).
    """
    true_path = os.path.join(data_dir, "True.csv")
    fake_path = os.path.join(data_dir, "Fake.csv")
    
    if os.path.exists(true_path) and os.path.exists(fake_path):
        print(f"[*] Found separate datasets: '{true_path}' and '{fake_path}'")
        df_true = pd.read_csv(true_path)
        df_fake = pd.read_csv(fake_path)
        
        # Label: real = 1, fake = 0
        df_true["label"] = 1
        df_fake["label"] = 0
        
        # Combine title and text if present
        def get_content(df):
            if "title" in df.columns and "text" in df.columns:
                return df["title"].fillna("") + " " + df["text"].fillna("")
            elif "text" in df.columns:
                return df["text"].fillna("")
            elif "title" in df.columns:
                return df["title"].fillna("")
            else:
                return df.iloc[:, 0].astype(str)
        
        df_true["content"] = get_content(df_true)
        df_fake["content"] = get_content(df_fake)
        
        df = pd.concat([df_true[["content", "label"]], df_fake[["content", "label"]]], ignore_index=True)
    else:
        # Fallback to unified dataset if available
        combined_path = os.path.join(data_dir, "news.csv")
        if os.path.exists(combined_path):
            print(f"[*] Found unified dataset: '{combined_path}'")
            df = pd.read_csv(combined_path)
            if "label" not in df.columns:
                raise ValueError("Dataset CSV must contain a 'label' column.")
            # Map labels if textual (e.g. 'REAL'/'FAKE')
            if df["label"].dtype == object:
                df["label"] = df["label"].str.upper().map({"REAL": 1, "TRUE": 1, "FAKE": 0, "FALSE": 0})
            if "content" not in df.columns:
                if "title" in df.columns and "text" in df.columns:
                    df["content"] = df["title"].fillna("") + " " + df["text"].fillna("")
                elif "text" in df.columns:
                    df["content"] = df["text"].fillna("")
                else:
                    df["content"] = df.iloc[:, 0].astype(str)
        else:
            raise FileNotFoundError(
                f"No dataset found in '{data_dir}'. Expected 'True.csv' and 'Fake.csv' or 'news.csv'."
            )
            
    # Drop empty records
    df = df.dropna(subset=["content", "label"]).reset_index(drop=True)
    print(f"[*] Total dataset size: {len(df)} samples (Real: {(df['label'] == 1).sum()}, Fake: {(df['label'] == 0).sum()})")
    return df


def train(model_type: str = "logistic", data_dir: str = "data", model_dir: str = "model"):
    """
    Executes end-to-end preprocessing, training, evaluation, and serialization.
    """
    os.makedirs(model_dir, exist_ok=True)
    
    # 1. Load data
    df = load_dataset(data_dir)
    
    # 2. Clean text
    print("[*] Cleaning text data (lowercasing, stripping punctuation, URLs, whitespace)...")
    df["clean_content"] = df["content"].apply(clean_text)
    
    # Filter out empty cleaned strings
    df = df[df["clean_content"].str.strip().str.len() > 0].reset_index(drop=True)
    
    X = df["clean_content"]
    y = df["label"].astype(int)
    
    # 3. Train / Test Split (80% train, 20% test)
    print("[*] Splitting dataset into 80% train and 20% test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"    Train size: {len(X_train)} | Test size: {len(X_test)}")
    
    # 4. Fit TF-IDF Vectorizer (max_df=0.7, stop_words='english')
    print("[*] Vectorizing text using TF-IDF (max_df=0.7, stop_words='english')...")
    vectorizer = TfidfVectorizer(
        max_df=0.7,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=2
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"    TF-IDF vocabulary size: {len(vectorizer.vocabulary_)} features")
    
    # 5. Initialize Classifier
    if model_type.lower() == "passive_aggressive":
        print("[*] Training PassiveAggressiveClassifier with probability calibration...")
        base_pac = PassiveAggressiveClassifier(max_iter=1000, random_state=42, C=0.5)
        # Use CalibratedClassifierCV to enable predict_proba for accurate confidence scores
        clf = CalibratedClassifierCV(estimator=base_pac, cv=3)
    else:
        print("[*] Training Logistic Regression Classifier...")
        clf = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
        
    clf.fit(X_train_vec, y_train)
    
    # 6. Evaluation
    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["FAKE (0)", "REAL (1)"])
    
    print("\n" + "="*50)
    print("           MODEL EVALUATION RESULTS")
    print("="*50)
    print(f"Model Accuracy: {acc * 100:.2f}%\n")
    print("Confusion Matrix:")
    print("               Predicted FAKE   Predicted REAL")
    print(f"Actual FAKE:         {cm[0][0]:<14} {cm[0][1]}")
    print(f"Actual REAL:         {cm[1][0]:<14} {cm[1][1]}")
    print("\nClassification Report:")
    print(report)
    print("="*50 + "\n")
    
    # 7. Save model and vectorizer with joblib
    model_path = os.path.join(model_dir, "model.pkl")
    vectorizer_path = os.path.join(model_dir, "vectorizer.pkl")
    
    joblib.dump(clf, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"[+] Model saved to: '{model_path}'")
    print(f"[+] Vectorizer saved to: '{vectorizer_path}'")
    print("[+] Training completed successfully!")
    
    return clf, vectorizer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fake News Detection Classifier")
    parser.add_argument(
        "--model",
        type=str,
        default="logistic",
        choices=["logistic", "passive_aggressive"],
        help="Classifier type: 'logistic' (default) or 'passive_aggressive'"
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="data",
        help="Directory containing True.csv and Fake.csv"
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default="model",
        help="Directory to save model.pkl and vectorizer.pkl"
    )
    args = parser.parse_args()
    train(model_type=args.model, data_dir=args.data_dir, model_dir=args.model_dir)
