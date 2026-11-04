"""Configuration loaded from environment variables / .env.

No credentials are stored in this file.  The original 2020 scripts used
``config.MONGO``, ``config.DB``, ``config.COLLECTION`` and ``config.API1`` ...
``config.API10``; those aliases are kept so the legacy scripts remain readable.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "StockNewsDB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "NewsCollection")

# Legacy aliases
MONGO = MONGO_URI
DB = MONGO_DB
COLLECTION = MONGO_COLLECTION

# Prediction service
SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost:5000")
SERVICE_HOST = os.getenv("SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", "5000"))

# Model artifacts
MODEL_DIR = Path(os.getenv("MODEL_DIR", str(PROJECT_ROOT / "PythonObjects")))
NEWS_CLASSIFIER_DIR = Path(
    os.getenv("NEWS_CLASSIFIER_DIR", str(MODEL_DIR / "NewsClassifierObjects"))
)
POLARITY_BACKEND = os.getenv("POLARITY_BACKEND", "finbert").lower()
POLARITY_MODEL = os.getenv("POLARITY_MODEL", "ProsusAI/finbert")
POLARITY_MODEL_DIR = Path(
    os.getenv("POLARITY_MODEL_DIR", str(MODEL_DIR / "PolarityClassifier"))
)
POLARITY_SKLEARN_DIR = Path(
    os.getenv("POLARITY_SKLEARN_DIR", str(MODEL_DIR / "PolaritySklearn"))
)
LEGACY_POLARITY_DIR = Path(
    os.getenv("LEGACY_POLARITY_DIR", str(MODEL_DIR / "legacy" / "PolarityClassifier"))
)

# NewsAPI
_newsapi_keys = [
    key.strip()
    for key in os.getenv("NEWSAPI_KEYS", os.getenv("NEWSAPI_KEY", "")).split(",")
    if key.strip()
]
API1 = _newsapi_keys[0] if len(_newsapi_keys) > 0 else ""
API2 = _newsapi_keys[1] if len(_newsapi_keys) > 1 else ""
API3 = _newsapi_keys[2] if len(_newsapi_keys) > 2 else ""
API4 = _newsapi_keys[3] if len(_newsapi_keys) > 3 else ""
API5 = _newsapi_keys[4] if len(_newsapi_keys) > 4 else ""
API6 = _newsapi_keys[5] if len(_newsapi_keys) > 5 else ""
API7 = _newsapi_keys[6] if len(_newsapi_keys) > 6 else ""
API8 = _newsapi_keys[7] if len(_newsapi_keys) > 7 else ""
API9 = _newsapi_keys[8] if len(_newsapi_keys) > 8 else ""
API10 = _newsapi_keys[9] if len(_newsapi_keys) > 9 else ""
NEWSAPI_KEYS = _newsapi_keys

# Legacy UI / Spring backend
JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-env")
LEGACY_API_PORT = int(os.getenv("LEGACY_API_PORT", "8081"))
LEGACY_API_URL = os.getenv("LEGACY_API_URL", f"http://localhost:{LEGACY_API_PORT}")
STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
