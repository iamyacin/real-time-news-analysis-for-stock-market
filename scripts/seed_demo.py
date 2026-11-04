"""Seed MongoDB with the bundled demo fixtures.

Requires the prediction service to be running.  The Docker Compose stack starts
it automatically; locally use `make serve` in another terminal.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402
from news_analysis.schema import normalize_newsapi_article, normalize_tweet  # noqa: E402

FIXTURES = PROJECT_ROOT / "Data" / "fixtures"


def _recent_date(value: str, index: int) -> str:
    """Keep demo dates inside the legacy UI's 90-day aggregation window."""
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) - parsed <= timedelta(days=80):
            return value
    except (TypeError, ValueError):
        pass
    moment = datetime.now(timezone.utc) - timedelta(days=index % 60, hours=index % 12)
    return moment.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _analyze_many(service_url: str, texts: list[str]) -> list[dict]:
    response = requests.post(
        f"{service_url.rstrip('/')}/analyze/batch",
        json={"items": [{"text": text} for text in texts]},
        timeout=300,
    )
    response.raise_for_status()
    return response.json()["results"]


def seed_societies(db) -> int:
    path = FIXTURES / "societies_seed.csv"
    count = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            ticker = row["ticker"].upper()
            document = {
                "_id": ticker,
                "symbol": ticker,
                "shortName": row["name"],
                "longName": row["name"],
                "sector": row["sector"],
                "industry": row["industry"],
                "logo_url": row["logo_url"],
                "country": row["country"],
                "currency": row["currency"],
                "quoteType": "EQUITY",
            }
            db["SocietiesInfo"].update_one({"_id": ticker}, {"$set": document}, upsert=True)
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-url", default=config.SERVICE_URL)
    parser.add_argument("--reset", action="store_true", help="remove previous fixture records first")
    args = parser.parse_args()

    news = json.loads((FIXTURES / "news_sample.json").read_text(encoding="utf-8"))
    tweets = json.loads((FIXTURES / "tweets_sample.json").read_text(encoding="utf-8"))

    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[config.MONGO_DB]
    collection = db[config.MONGO_COLLECTION]
    collection.create_index("url", unique=True, sparse=True)
    collection.create_index([("ticker", 1), ("publishedAt", -1)])
    collection.create_index("prediction")

    if args.reset:
        collection.delete_many({"source_type": {"$in": ["newsapi_fixture", "twitter_fixture"]}})

    for index, article in enumerate(news):
        article["publishedAt"] = _recent_date(article.get("publishedAt"), index)
    for index, tweet in enumerate(tweets):
        tweet["created_at"] = _recent_date(tweet.get("created_at"), index)

    news_texts = [f"{item.get('title', '')} {item.get('description', '')}".strip() for item in news]
    tweet_texts = [item["text"] for item in tweets]
    results = _analyze_many(args.service_url, news_texts + tweet_texts)

    inserted = 0
    for index, article in enumerate(news):
        document = normalize_newsapi_article(
            article,
            ticker=article.get("ticker"),
            analysis=results[index],
            source_type="newsapi_fixture",
        )
        collection.update_one({"url": document["url"]}, {"$set": document}, upsert=True)
        inserted += 1

    for offset, tweet in enumerate(tweets):
        result = results[len(news) + offset]
        tweet = dict(tweet)
        tweet["url"] = f"https://twitter.com/i/web/status/fixture-{offset + 1}"
        document = normalize_tweet(tweet, analysis=result)
        document["source_type"] = "twitter_fixture"
        collection.update_one({"url": document["url"]}, {"$set": document}, upsert=True)
        inserted += 1

    societies = seed_societies(db)
    print(f"Seeded {inserted} news/tweet records and {societies} societies into {config.MONGO_DB}.")
    print(f"NewsCollection count: {collection.count_documents({})}")
    client.close()


if __name__ == "__main__":
    main()
