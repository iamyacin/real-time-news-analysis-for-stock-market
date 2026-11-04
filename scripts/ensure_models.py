"""Ensure the local demo has model artifacts available.

Run automatically by the Docker service entrypoint so a fresh clone can start
without committing model binaries.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run(script: str) -> None:
    print(f"[ensure_models] running {script}")
    subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / script)], check=True, cwd=PROJECT_ROOT)


def main() -> None:
    news_dir = PROJECT_ROOT / "PythonObjects" / "NewsClassifierObjects"
    polarity_dir = PROJECT_ROOT / "PythonObjects" / "PolaritySklearn"
    if not all((news_dir / name).exists() for name in ("vectorizer.joblib", "selector.joblib", "classifier.joblib")):
        _run("train_news_classifier.py")
    if not all((polarity_dir / name).exists() for name in ("vectorizer.joblib", "model.joblib")):
        _run("train_polarity_sklearn.py")


if __name__ == "__main__":
    main()
