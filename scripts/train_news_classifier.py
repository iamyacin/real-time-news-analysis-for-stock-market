"""Train the business-vs-other Random Forest classifier.

This reproduces the model described in the PFE report:
Porter stemming -> CountVectorizer -> chi-square SelectKBest(900) ->
RandomForestClassifier(100 trees).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402
from news_analysis.preprocess import preprocess_text  # noqa: E402

DATASET = PROJECT_ROOT / "Data" / "GeneratedData" / "NewsClasses(Other=0, Buissness=1).csv"


def main() -> dict:
    data = pd.read_csv(DATASET)
    data = data.dropna(subset=["News", "Class"])
    texts = [preprocess_text(str(value)) for value in data["News"].tolist()]
    labels = data["Class"].astype(int).tolist()

    from sklearn.feature_extraction.text import CountVectorizer

    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform(texts)
    selector = SelectKBest(chi2, k=min(900, matrix.shape[1]))
    features = selector.fit_transform(matrix, labels)

    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.20, random_state=0, stratify=labels
    )
    classifier = RandomForestClassifier(n_estimators=100, random_state=111)
    classifier.fit(x_train, y_train)
    predictions = classifier.predict(x_test)
    accuracy = float(accuracy_score(y_test, predictions))

    out_dir = Path(config.NEWS_CLASSIFIER_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, out_dir / "vectorizer.joblib")
    joblib.dump(selector, out_dir / "selector.joblib")
    joblib.dump(classifier, out_dir / "classifier.joblib")
    metrics = {
        "accuracy": round(accuracy, 4),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "classification_report": classification_report(
            y_test, predictions, output_dict=True, zero_division=0
        ),
        "n_samples": int(len(data)),
        "n_features": int(matrix.shape[1]),
        "n_selected_features": int(features.shape[1]),
        "dataset": str(DATASET.relative_to(PROJECT_ROOT)),
    }
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"News classifier accuracy: {accuracy:.4f}")
    print(f"Saved artifacts to {out_dir}")
    return metrics


if __name__ == "__main__":
    main()
