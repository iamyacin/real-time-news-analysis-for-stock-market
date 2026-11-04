"""Collect financial news from NewsAPI and store enriched records.

Usage:
    python scripts/collect_news.py --limit 3          # live, first 3 tickers
    python scripts/collect_news.py --tickers AAPL,MSFT
    python scripts/collect_news.py --loop --interval 7200

The default demo does not need this script; fixtures are loaded by
`scripts/seed_demo.py`.
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from pathlib import Path

import requests
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402
from news_analysis.schema import normalize_newsapi_article  # noqa: E402

FIXTURES = PROJECT_ROOT / "Data" / "fixtures"


def _societies() -> list[tuple[str, str]]:
    with (FIXTURES / "societies_seed.csv").open(newline="", encoding="utf-8") as handle:
        return [(row["ticker"], row["name"]) for row in csv.DictReader(handle)]


def _query(api_key: str, ticker: str, name: str, page_size: int) -> list[dict]:
    query = f'"{name}" OR {ticker}' if " " in name else f"{name} OR {ticker}"
    response = requests.get(
        "https://newsapi.org/v2/everything",
        params={
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": api_key,
        },
        timeout=30,
    )
    if response.status_code == 401:
        raise RuntimeError("NewsAPI rejected the key (401). Add NEWSAPI_KEY to .env.")
    response.raise_for_status()
    return response.json().get("articles", [])


def _analyze(service_url: str, texts: list[str]) -> list[dict]:
    response = requests.post(
        f"{service_url.rstrip('/')}/analyze/batch",
        json={"items": [{"text": text} for text in texts]},
        timeout=300,
    )
    response.raise_for_status()
    return response.json()["results"]


def run_once(tickers: list[tuple[str, str]], limit: int | None = None) -> int:
    keys = config.NEWSAPI_KEYS
    if not keys:
        raise SystemExit("No NEWSAPI_KEY configured. Copy .env.example to .env and add a key.")
    if limit:
        tickers = tickers[:limit]

    collection = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)[config.MONGO_DB][
        config.MONGO_COLLECTION
    ]
    collection.create_index("url", unique=True, sparse=True)
    stored = 0
    for index, (ticker, name) in enumerate(tickers):
        key = keys[index % len(keys)]
        try:
            articles = _query(key, ticker, name, page_size=100)
        except Exception as exc:  # noqa: BLE001
            print(f"[{ticker}] NewsAPI error: {exc}")
            continue
        articles = [a for a in articles if a.get("title")]
        if not articles:
            print(f"[{ticker}] no articles")
            continue
        texts = [
            f"{a.get('title', '')} {a.get('description') or ''}".strip() for a in articles
        ]
        analyses = _analyze(config.SERVICE_URL, texts)
        for article, analysis in zip(articles, analyses):
            document = normalize_newsapi_article(article, ticker=ticker, analysis=analysis)
            collection.update_one({"url": document["url"]}, {"$set": document}, upsert=True)
            stored += 1
        print(f"[{ticker}] stored {len(articles)} articles")
        time.sleep(1)
    print(f"Stored/updated {stored} articles in {config.MONGO_DB}.{config.MONGO_COLLECTION}")
    return stored


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", help="comma-separated tickers; default all seeded societies")
    parser.add_argument("--limit", type=int, help="only the first N tickers")
    parser.add_argument("--loop", action="store_true")
    parser.add_argument("--interval", type=int, default=7200)
    args = parser.parse_args()

    societies = _societies()
    if args.tickers:
        wanted = {t.strip().upper() for t in args.tickers.split(",")}
        societies = [item for item in societies if item[0] in wanted]

    while True:
        run_once(societies, limit=args.limit)
        if not args.loop:
            break
        print(f"Sleeping {args.interval}s...")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
