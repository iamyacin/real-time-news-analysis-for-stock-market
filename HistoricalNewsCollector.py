"""Legacy entrypoint replaced by the restored collector.

The original 2020 implementation used ktrain directly and hardcoded credentials.
It remains available in git history; this wrapper keeps the filename working:

    python HistoricalNewsCollector.py --limit 5
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.collect_news import main

if __name__ == "__main__":
    main()
