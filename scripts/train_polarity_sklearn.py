"""Train a fast offline TF-IDF polarity model.

This is the zero-download fallback used when FinBERT is not available.  The
original BERT training path remains documented in docs/TRAIN_POLARITY_MODEL.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402

DATASET = PROJECT_ROOT / "Data" / "GeneratedData" / "LabeledNews.csv"


def main() -> dict:
    data = pd.read_csv(DATASET).dropna(subset=["News", "Sentiment"])
    texts = data["News"].astype(str).tolist()
    labels = data["Sentiment"].astype(str).tolist()

    x_train, x_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=0, stratify=labels
    )
    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2), sublinear_tf=True)
    x_train_vec = vectorizer.fit_transform(x_train)
    x_test_vec = vectorizer.transform(x_test)
    classifier = LogisticRegression(max_iter=1000, class_weight="balanced")
    classifier.fit(x_train_vec, y_train)
    predictions = classifier.predict(x_test_vec)
    accuracy = float(accuracy_score(y_test, predictions))

    out_dir = Path(config.POLARITY_SKLEARN_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, out_dir / "vectorizer.joblib")
    joblib.dump(classifier, out_dir / "model.joblib")
    (out_dir / "labels.json").write_text(
        json.dumps(sorted(set(labels))), encoding="utf-8"
    )
    metrics = {
        "accuracy": round(accuracy, 4),
        "classification_report": classification_report(
            y_test, predictions, output_dict=True, zero_division=0
        ),
        "n_samples": int(len(data)),
        "model": "TF-IDF + LogisticRegression (offline fallback)",
        "dataset": str(DATASET.relative_to(PROJECT_ROOT)),
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Offline polarity accuracy: {accuracy:.4f}")
    print(f"Saved artifacts to {out_dir}")
    return metrics


if __name__ == "__main__":
    main()
