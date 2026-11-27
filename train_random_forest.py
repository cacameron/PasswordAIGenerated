"""Train, evaluate, and save a password-strength random forest."""

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from train_decision_tree import FEATURE_NAMES, MODEL_DIR, load_training_data


def train_random_forest(file_path=None, max_samples=40000):
    # Use the same training/test split as the decision tree.
    X_train, X_test, y_train, y_test = load_training_data(file_path, max_samples)

    # Train the model.
    model = RandomForestClassifier(
        n_estimators=100, max_depth=12, random_state=42, n_jobs=-1
    )
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
                MODEL_DIR / "random_forest.joblib", compress=3)
    print("Random forest accuracy:", format(metrics["accuracy"], ".2%"))
    print("Saved trained_models/random_forest.joblib")
    return metrics


if __name__ == "__main__":
    train_random_forest()
