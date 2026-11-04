from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from NewsPredictionMicroservice.app import create_app  # noqa: E402


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
    assert "news_classifier" in body


def test_news_or_not_plain_integer(client):
    response = client.post("/NewsOrNot", data={"text": "Apple earnings beat expectations"})
    assert response.status_code == 200
    assert response.get_data(as_text=True).strip() in {"0", "1"}


def test_polarity_plain_integer(client):
    response = client.post("/Polarity", data={"text": "The company reported record profit"})
    assert response.status_code == 200
    assert response.get_data(as_text=True).strip() in {"-1", "0", "1"}


def test_analyze_json(client):
    response = client.post("/analyze", json={"text": "Tesla shares fall after weak deliveries"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["is_business"] in {0, 1}
    assert body["polarity_label"] in {"Positive", "Neutral", "Negative"}
    assert body["polarity"] in {-1, 0, 1}


def test_batch(client):
    response = client.post(
        "/analyze/batch",
        json={"items": [{"text": "Microsoft revenue grows"}, {"text": "Boeing faces a lawsuit"}]},
    )
    assert response.status_code == 200
    assert len(response.get_json()["results"]) == 2


def test_missing_text(client):
    response = client.post("/analyze", json={})
    assert response.status_code == 400
