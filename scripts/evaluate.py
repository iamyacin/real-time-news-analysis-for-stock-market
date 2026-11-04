"""Evaluate the running prediction service against the bundled fixtures."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402

FIXTURES = PROJECT_ROOT / "Data" / "fixtures" / "news_sample.json"
OUT = PROJECT_ROOT / "reports" / "evaluation.json"


def main() -> None:
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    response = requests.post(
        f"{config.SERVICE_URL.rstrip('/')}/analyze/batch",
        json={"items": [{"text": f"{f['title']} {f['description']}"} for f in fixtures]},
        timeout=300,
    )
    response.raise_for_status()
    results = response.json()["results"]

    confusion = Counter()
    correct = 0
    for fixture, result in zip(fixtures, results):
        expected = fixture["expected_sentiment"]
        predicted = result["polarity_label"]
        confusion[(expected, predicted)] += 1
        correct += expected == predicted

    accuracy = correct / len(fixtures)
    labels = ["Positive", "Neutral", "Negative"]
    matrix = [[confusion[(expected, predicted)] for predicted in labels] for expected in labels]
    report = {
        "accuracy": round(accuracy, 4),
        "samples": len(fixtures),
        "labels": labels,
        "confusion_matrix": matrix,
        "backend": results[0]["backend"] if results else None,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
