"""Legacy real-time NewsAPI entrypoint, now backed by the restored collector.

Run from the repository root:

    python RealTimeScripts/StreamingNewsAPI.py
    python scripts/collect_news.py --loop --interval 7200
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.collect_news import _societies, run_once


if __name__ == "__main__":
    run_once(_societies(), limit=5)
