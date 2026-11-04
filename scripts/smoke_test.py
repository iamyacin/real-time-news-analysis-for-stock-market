"""End-to-end smoke test for the running demo stack."""

from __future__ import annotations

import sys
from pathlib import Path

import requests
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, fn) -> None:
    try:
        detail = fn()
        RESULTS.append((name, True, str(detail or "ok")))
    except Exception as exc:  # noqa: BLE001
        RESULTS.append((name, False, str(exc)))


def main() -> None:
    def service_health():
        response = requests.get(f"{config.SERVICE_URL}/health", timeout=10)
        response.raise_for_status()
        body = response.json()
        assert body["status"] == "ok"
        return f"polarity={body['polarity']['active']}, news={body['news_classifier']['ready']}"

    def analyze():
        response = requests.post(
            f"{config.SERVICE_URL}/analyze",
            json={"text": "Apple beats earnings expectations as services revenue hits a record"},
            timeout=120,
        )
        response.raise_for_status()
        body = response.json()
        assert body["polarity_label"] in {"Positive", "Neutral", "Negative"}
        return f"{body['polarity_label']} via {body['backend']}"

    def mongo_count():
        count = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)[config.MONGO_DB][
            config.MONGO_COLLECTION
        ].count_documents({})
        assert count > 0
        return f"{count} records"

    def spring_health():
        response = requests.get(f"{config.LEGACY_API_URL}/api/health", timeout=10)
        response.raise_for_status()
        return response.json()["status"]

    def login():
        response = requests.post(
            f"{config.LEGACY_API_URL}/api/auth/signin",
            json={"username": "admin", "password": "admin123"},
            timeout=10,
        )
        response.raise_for_status()
        token = response.json()["accessToken"]
        assert token
        return "admin token"

    def legacy_data():
        token_response = requests.post(
            f"{config.LEGACY_API_URL}/api/auth/signin",
            json={"username": "admin", "password": "admin123"},
            timeout=10,
        )
        token = token_response.json()["accessToken"]
        headers = {"Authorization": f"Bearer {token}"}
        societies = requests.get(
            f"{config.LEGACY_API_URL}/api/societies", headers=headers, timeout=10
        ).json()
        news = requests.get(
            f"{config.LEGACY_API_URL}/api/news/ticker/$AAPL", headers=headers, timeout=10
        ).json()
        assert len(societies) > 0 and len(news) > 0
        return f"{len(societies)} societies, {len(news)} AAPL news"

    def streamlit():
        response = requests.get(config.STREAMLIT_URL, timeout=10)
        response.raise_for_status()
        return response.status_code

    def frontend():
        response = requests.get(config.FRONTEND_URL, timeout=10)
        response.raise_for_status()
        return response.status_code

    check("prediction service", service_health)
    check("analyze endpoint", analyze)
    check("MongoDB data", mongo_count)
    check("Spring health", spring_health)
    check("Spring login", login)
    check("Spring data", legacy_data)
    check("Streamlit", streamlit)
    check("React frontend", frontend)

    failed = False
    for name, ok, detail in RESULTS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
        failed = failed or not ok
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
