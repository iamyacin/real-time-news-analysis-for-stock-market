"""Flask prediction service for the restored PFE project.

Legacy endpoints keep their original plain-integer contract so the old Java
integration still works.  The new `/analyze` endpoints return JSON for the
Streamlit dashboard and collectors.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402
from NewsPredictionMicroservice.models import NewsClassifierModel, PolarityService  # noqa: E402

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def _text_from_request() -> str:
    payload = request.get_json(silent=True) or {}
    text = payload.get("text") or request.form.get("text") or request.values.get("text")
    if not text or not str(text).strip():
        raise ValueError("'text' is required")
    return str(text).strip()


def _mongo_status() -> dict:
    try:
        from pymongo import MongoClient

        client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=800)
        client.admin.command("ping")
        client.close()
        return {"ok": True}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": str(exc)}


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    classifier = NewsClassifierModel()
    polarity = PolarityService()

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "Stock News Analyzer prediction service",
                "endpoints": ["/health", "/NewsOrNot", "/Polarity", "/analyze", "/analyze/batch"],
            }
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "status": "ok",
                "news_classifier": {
                    "ready": classifier.ready,
                    "model_dir": str(classifier.model_dir),
                },
                "polarity": polarity.health(),
                "mongo": _mongo_status(),
            }
        )

    @app.post("/NewsOrNot")
    def news_or_not():
        try:
            text = _text_from_request()
        except ValueError as exc:
            return Response(str(exc), status=400, mimetype="text/plain")
        value = classifier.predict(text)
        return Response(str(value), mimetype="text/plain")

    @app.post("/Polarity")
    def polarity_only():
        try:
            text = _text_from_request()
        except ValueError as exc:
            return Response(str(exc), status=400, mimetype="text/plain")
        _label, score, _backend = polarity.predict(text)
        return Response(str(score), mimetype="text/plain")

    @app.post("/analyze")
    def analyze():
        try:
            text = _text_from_request()
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        label, score, backend = polarity.predict(text)
        return jsonify(
            {
                "text": text,
                "is_business": classifier.predict(text),
                "polarity": score,
                "polarity_label": label,
                "backend": backend,
            }
        )

    @app.post("/analyze/batch")
    def analyze_batch():
        payload = request.get_json(silent=True) or {}
        items = payload.get("items")
        if not isinstance(items, list) or not items:
            return jsonify({"error": "'items' must be a non-empty list"}), 400
        results = []
        for item in items:
            text = item.get("text") if isinstance(item, dict) else item
            if not text:
                results.append({"error": "missing text"})
                continue
            label, score, backend = polarity.predict(str(text))
            results.append(
                {
                    "text": str(text),
                    "is_business": classifier.predict(str(text)),
                    "polarity": score,
                    "polarity_label": label,
                    "backend": backend,
                }
            )
        return jsonify({"results": results})

    @app.errorhandler(Exception)
    def handle_error(exc):
        log.exception("Unhandled error")
        return jsonify({"error": str(exc)}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=config.SERVICE_HOST, port=config.SERVICE_PORT)
