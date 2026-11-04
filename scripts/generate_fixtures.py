"""Generate small, recent demo fixtures from the original labeled dataset.

The text comes from the 2020 dataset, but dates are shifted near today so the
restored Spring UI's "last 90 days" charts are populated during a demo.
"""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "Data" / "CollectedData" / "LabeledData.json"
OUT_DIR = PROJECT_ROOT / "Data" / "fixtures"

SOCIETIES = [
    ("AAPL", "Apple", "Technology", "Consumer Electronics"),
    ("MSFT", "Microsoft", "Technology", "Software"),
    ("AMZN", "Amazon", "Consumer Discretionary", "E-commerce"),
    ("GOOGL", "Alphabet", "Communication Services", "Internet Content"),
    ("FB", "Meta Platforms", "Communication Services", "Social Media"),
    ("TSLA", "Tesla", "Consumer Discretionary", "Automobiles"),
    ("NFLX", "Netflix", "Communication Services", "Entertainment"),
    ("JPM", "JPMorgan Chase", "Financials", "Banks"),
    ("BAC", "Bank of America", "Financials", "Banks"),
    ("V", "Visa", "Financials", "Payment Services"),
    ("MA", "Mastercard", "Financials", "Payment Services"),
    ("DIS", "Walt Disney", "Communication Services", "Entertainment"),
    ("KO", "Coca-Cola", "Consumer Staples", "Beverages"),
    ("MCD", "McDonald's", "Consumer Discretionary", "Restaurants"),
    ("NKE", "Nike", "Consumer Discretionary", "Apparel"),
    ("SBUX", "Starbucks", "Consumer Discretionary", "Restaurants"),
    ("BA", "Boeing", "Industrials", "Aerospace"),
    ("F", "Ford", "Consumer Discretionary", "Automobiles"),
    ("GM", "General Motors", "Consumer Discretionary", "Automobiles"),
    ("T", "AT&T", "Communication Services", "Telecom"),
    ("VZ", "Verizon", "Communication Services", "Telecom"),
    ("IBM", "IBM", "Technology", "IT Services"),
    ("ORCL", "Oracle", "Technology", "Software"),
    ("CRM", "Salesforce", "Technology", "Software"),
    ("UBER", "Uber", "Industrials", "Transportation"),
    ("SHOP", "Shopify", "Technology", "Software"),
    ("BABA", "Alibaba", "Consumer Discretionary", "E-commerce"),
]
TICKERS = {row[0] for row in SOCIETIES}


def _iso(days_ago: int, hour: int) -> str:
    moment = datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hour % 12)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = payload["data"] if isinstance(payload, dict) else payload
    by_sentiment: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        tickers = record.get("tickers") or []
        ticker = next((t for t in tickers if t in TICKERS), None)
        sentiment = record.get("sentiment")
        if ticker and sentiment in {"Positive", "Neutral", "Negative"}:
            record["_ticker"] = ticker
            by_sentiment[sentiment].append(record)

    random.seed(42)
    selected: list[dict] = []
    for sentiment in ("Positive", "Neutral", "Negative"):
        pool = by_sentiment[sentiment]
        random.shuffle(pool)
        selected.extend(pool[:40])

    news = []
    for index, record in enumerate(selected):
        title = (record.get("title") or "").strip()
        text = (record.get("text") or "").strip()
        ticker = record["_ticker"]
        news.append(
            {
                "source": {"id": "pfe-fixture", "name": record.get("source_name") or "PFE fixture"},
                "author": "PFE 2020 dataset",
                "title": title,
                "description": text[:900],
                "url": f"https://example.com/pfe-fixture/{index + 1}",
                "urlToImage": record.get("image_url") or "/imgs/stock.jpeg",
                "publishedAt": _iso(index % 60, 8 + index % 10),
                "ticker": ticker,
                "expected_sentiment": record.get("sentiment"),
                "expected_business": 1,
            }
        )

    tweets = []
    for index, item in enumerate(news[:40]):
        tweets.append(
            {
                "text": f"${item['ticker']} {item['title']} {item['description'][:180]}",
                "created_at": item["publishedAt"],
                "user": ["MarketWatch", "CNBC", "ReutersBiz", "YahooFinance"][index % 4],
                "tickers": [item["ticker"]],
                "expected_sentiment": item["expected_sentiment"],
            }
        )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "news_sample.json").write_text(json.dumps(news, indent=2), encoding="utf-8")
    (OUT_DIR / "tweets_sample.json").write_text(json.dumps(tweets, indent=2), encoding="utf-8")

    with (OUT_DIR / "societies_seed.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["ticker", "name", "sector", "industry", "logo_url", "country", "currency"])
        for ticker, name, sector, industry in SOCIETIES:
            writer.writerow([ticker, name, sector, industry, "/imgs/logo.png", "United States", "USD"])

    print(f"Wrote {len(news)} news fixtures and {len(tweets)} tweets to {OUT_DIR}")


if __name__ == "__main__":
    main()
