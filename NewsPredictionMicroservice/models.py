"""Model loading and prediction backends for the restored service."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib

import config
from news_analysis.preprocess import preprocess_text

log = logging.getLogger(__name__)

LABELS = ("Negative", "Neutral", "Positive")
LABEL_TO_SCORE = {"Negative": -1, "negative": -1, "Neutral": 0, "neutral": 0, "Positive": 1, "positive": 1}

_POSITIVE_WORDS = {
    "beat", "beats", "growth", "grow", "profit", "profits", "record", "surge",
    "rally", "gain", "gains", "upgrade", "upgraded", "strong", "success", "win",
    "wins", "rise", "rises", "higher", "bullish", "outperform", "buy", "dividend",
}
_NEGATIVE_WORDS = {
    "miss", "misses", "loss", "losses", "decline", "declines", "fall", "falls",
    "drop", "drops", "cut", "cuts", "downgrade", "downgraded", "weak", "fraud",
    "lawsuit", "probe", "recall", "bankrupt", "bankruptcy", "layoff", "layoffs",
    "lower", "bearish", "sell", "warning", "risk", "crash", "plunge",
}


class NewsClassifierModel:
    """TF-IDF + chi-square + Random Forest business-news classifier."""

    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = Path(model_dir or config.NEWS_CLASSIFIER_DIR)
        self.vectorizer = None
        self.selector = None
        self.classifier = None
        self._load()

    def _load(self) -> None:
        paths = {
            "vectorizer": self.model_dir / "vectorizer.joblib",
            "selector": self.model_dir / "selector.joblib",
            "classifier": self.model_dir / "classifier.joblib",
        }
        missing = [str(p) for p in paths.values() if not p.exists()]
        if missing:
            log.warning("News classifier artifacts missing: %s", ", ".join(missing))
            return
        self.vectorizer = joblib.load(paths["vectorizer"])
        self.selector = joblib.load(paths["selector"])
        self.classifier = joblib.load(paths["classifier"])

    @property
    def ready(self) -> bool:
        return all(x is not None for x in (self.vectorizer, self.selector, self.classifier))

    def predict(self, text: str) -> int:
        if not self.ready:
            # Safe fallback: treat text containing market words as business news.
            words = set((text or "").lower().split())
            market_words = {"stock", "shares", "earnings", "revenue", "market", "investor", "ceo", "profit", "company"}
            return int(bool(words & market_words))
        processed = preprocess_text(text)
        features = self.selector.transform(self.vectorizer.transform([processed]))
        return int(self.classifier.predict(features)[0])


class PolarityBackend:
    name = "base"

    def predict(self, text: str) -> tuple[str, int, str]:
        raise NotImplementedError


class SklearnPolarityBackend(PolarityBackend):
    name = "sklearn"

    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = Path(model_dir or config.POLARITY_SKLEARN_DIR)
        self.vectorizer = None
        self.classifier = None
        self._load()

    def _load(self) -> None:
        vectorizer_path = self.model_dir / "vectorizer.joblib"
        model_path = self.model_dir / "model.joblib"
        if vectorizer_path.exists() and model_path.exists():
            self.vectorizer = joblib.load(vectorizer_path)
            self.classifier = joblib.load(model_path)

    @property
    def ready(self) -> bool:
        return self.vectorizer is not None and self.classifier is not None

    def predict(self, text: str) -> tuple[str, int, str]:
        if not self.ready:
            raise RuntimeError("sklearn polarity artifacts are not available")
        features = self.vectorizer.transform([text or ""])
        label = str(self.classifier.predict(features)[0])
        label = {"negative": "Negative", "neutral": "Neutral", "positive": "Positive"}.get(
            label.lower(), label
        )
        return label, LABEL_TO_SCORE.get(label, 0), self.name


class FinBertBackend(PolarityBackend):
    name = "finbert"

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or config.POLARITY_MODEL
        self._pipeline = None

    def _load(self) -> None:
        if self._pipeline is not None:
            return
        from transformers import pipeline

        self._pipeline = pipeline(
            "text-classification",
            model=self.model_name,
            tokenizer=self.model_name,
            truncation=True,
            max_length=512,
        )

    def predict(self, text: str) -> tuple[str, int, str]:
        self._load()
        result = self._pipeline(text or "", truncation=True, max_length=512)[0]
        label = str(result["label"]).lower()
        label = {"label_0": "Negative", "label_1": "Neutral", "label_2": "Positive"}.get(
            label, label
        )
        label = {"negative": "Negative", "neutral": "Neutral", "positive": "Positive"}.get(
            label, label
        )
        return label, LABEL_TO_SCORE.get(label, 0), f"finbert:{self.model_name}"


class HFPolarityBackend(PolarityBackend):
    name = "hf"

    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = Path(model_dir or config.POLARITY_MODEL_DIR)
        self._pipeline = None

    def _load(self) -> None:
        if self._pipeline is not None:
            return
        if not (self.model_dir / "config.json").exists():
            raise FileNotFoundError(f"No HuggingFace model found in {self.model_dir}")
        from transformers import pipeline

        self._pipeline = pipeline(
            "text-classification",
            model=str(self.model_dir),
            tokenizer=str(self.model_dir),
            truncation=True,
            max_length=512,
        )

    def predict(self, text: str) -> tuple[str, int, str]:
        self._load()
        result = self._pipeline(text or "", truncation=True, max_length=512)[0]
        label = str(result["label"])
        label = {"negative": "Negative", "neutral": "Neutral", "positive": "Positive"}.get(
            label.lower(), label
        )
        return label, LABEL_TO_SCORE.get(label, 0), f"hf:{self.model_dir.name}"


class LegacyKtrainBackend(PolarityBackend):
    name = "legacy"

    def __init__(self, model_dir: Path | None = None) -> None:
        self.model_dir = Path(model_dir or config.LEGACY_POLARITY_DIR)
        self._predictor = None

    def _load(self) -> None:
        if self._predictor is not None:
            return
        import ktrain

        path = self.model_dir
        nested = path / "BertPolarityClassifier"
        if nested.exists():
            path = nested
        self._predictor = ktrain.load_predictor(str(path))

    def predict(self, text: str) -> tuple[str, int, str]:
        self._load()
        label = str(self._predictor.predict(text or ""))
        label = {"negative": "Negative", "neutral": "Neutral", "positive": "Positive"}.get(
            label.lower(), label
        )
        return label, LABEL_TO_SCORE.get(label, 0), f"legacy:{self.model_dir.name}"


class HeuristicPolarityBackend(PolarityBackend):
    name = "heuristic"

    def predict(self, text: str) -> tuple[str, int, str]:
        words = set((text or "").lower().split())
        pos = len(words & _POSITIVE_WORDS)
        neg = len(words & _NEGATIVE_WORDS)
        if pos > neg:
            return "Positive", 1, self.name
        if neg > pos:
            return "Negative", -1, self.name
        return "Neutral", 0, self.name


class PolarityService:
    """Configured polarity backend with graceful offline fallbacks."""

    def __init__(self) -> None:
        self.configured = config.POLARITY_BACKEND
        self.backend: PolarityBackend | None = None
        self.last_error: str | None = None

    def _candidates(self) -> list[PolarityBackend]:
        configured = self.configured
        if configured == "legacy":
            return [LegacyKtrainBackend(), SklearnPolarityBackend(), HeuristicPolarityBackend()]
        if configured == "hf":
            return [HFPolarityBackend(), SklearnPolarityBackend(), HeuristicPolarityBackend()]
        if configured == "sklearn":
            return [SklearnPolarityBackend(), HeuristicPolarityBackend()]
        if configured == "heuristic":
            return [HeuristicPolarityBackend()]
        # finbert / auto: try FinBERT, then the offline models.
        return [FinBertBackend(), SklearnPolarityBackend(), HeuristicPolarityBackend()]

    def predict(self, text: str) -> tuple[str, int, str]:
        if self.backend is not None:
            return self.backend.predict(text)
        errors: list[str] = []
        for candidate in self._candidates():
            try:
                result = candidate.predict(text)
                self.backend = candidate
                return result
            except Exception as exc:  # noqa: BLE001 - fallback is intentional
                self.last_error = f"{candidate.name}: {exc}"
                errors.append(self.last_error)
                log.warning("Polarity backend %s unavailable: %s", candidate.name, exc)
        self.backend = HeuristicPolarityBackend()
        return self.backend.predict(text)

    @property
    def active_name(self) -> str:
        return self.backend.name if self.backend else self.configured

    def health(self) -> dict[str, Any]:
        return {
            "configured": self.configured,
            "active": self.active_name if self.backend else None,
            "last_error": self.last_error,
        }
