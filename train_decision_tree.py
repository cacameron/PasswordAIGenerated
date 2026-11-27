"""Train, evaluate, and save a password-strength decision tree."""

import csv
from pathlib import Path
import random

import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from feature_extraction import extract_features

BASE_DIR = Path(__file__).resolve().parent
FEATURE_NAMES = list(extract_features(""))
MODEL_DIR = BASE_DIR / "trained_models"


def load_training_data(file_path=None, max_samples=40000):
    if max_samples < 30:
        raise ValueError("Use at least 30 examples.")

    cleaned = BASE_DIR / "Dataset/Processed/Password Strength Classifier_cleaned.csv"
    original = BASE_DIR / "Dataset/Password Strength Classifier.csv"
    source = Path(file_path) if file_path else (cleaned if cleaned.is_file() else original)
    passwords = {}
    conflicts = set()

    # Keep passwords as text, including numeric passwords and valid spaces.
    with source.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        header = [name.strip() for name in next(reader, [])]
        if header != ["password", "strength"]:
            raise ValueError("Expected password,strength columns.")

        for row in reader:
            if len(row) != 2:
                continue
            password, label_text = row
            try:
                label = float(label_text)
            except ValueError:
                continue
            if (not password or len(password) > 256 or label not in (0, 1, 2)
                    or any(ord(c) < 32 or ord(c) == 127 for c in password)):
                continue
            label = int(label)
            if password in passwords and passwords[password] != label:
                conflicts.add(password)
            passwords[password] = label

    # Remove conflicting labels and duplicates before splitting.
    for password in conflicts:
        del passwords[password]
    selected = list(passwords)
    if len(selected) > max_samples:
        selected = random.Random(42).sample(selected, max_samples)

    X = [list(extract_features(password).values()) for password in selected]
    y = [passwords[password] for password in selected]
    if any(y.count(label) < 2 for label in (0, 1, 2)):
        raise ValueError("Need at least two examples of each strength label.")

    # Stratify keeps similar class proportions in training and testing.
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def train_decision_tree(file_path=None, max_samples=40000):
    # Load the data and separate training from testing.
    X_train, X_test, y_train, y_test = load_training_data(file_path, max_samples)

    # Train the model.
    model = DecisionTreeClassifier(max_depth=10, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate on examples the model did not train on.
    predictions = model.predict(X_test)
    majority_label = max(set(y_train), key=y_train.count)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "majority_baseline_accuracy": y_test.count(majority_label) / len(y_test),
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "split": "80/20 stratified split; random_state=42",
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=[0, 1, 2]).tolist(),
        "classification_report": classification_report(
            y_test, predictions, labels=[0, 1, 2],
            target_names=["Weak", "Medium", "Strong"], output_dict=True, zero_division=0
        )
    }

    # Save the model with its evaluation results.
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump({"model": model, "feature_names": FEATURE_NAMES, "metrics": metrics},
                MODEL_DIR / "decision_tree.joblib", compress=3)
    print("Decision tree accuracy:", format(metrics["accuracy"], ".2%"))
    print("Saved trained_models/decision_tree.joblib")
    return metrics


if __name__ == "__main__":
    train_decision_tree()
