"""Twitter/X ingestion in fixture mode.

The original 2020 script used Tweepy 3.x's StreamListener, which is removed from
modern Tweepy and no longer works with the X API.  This restored script reads
bundled sample tweets and runs them through the same prediction service and
MongoDB schema as the news pipeline.  See docs/TWITTER_V2_MIGRATION.md for the
real streaming client.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import requests
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402
from news_analysis.schema import normalize_tweet  # noqa: E402

FIXTURES = PROJECT_ROOT / "Data" / "fixtures" / "tweets_sample.json"


def main() -> None:
    tweets = json.loads(FIXTURES.read_text(encoding="utf-8"))
    response = requests.post(
        f"{config.SERVICE_URL.rstrip('/')}/analyze/batch",
        json={"items": [{"text": tweet["text"]} for tweet in tweets]},
        timeout=300,
    )
    response.raise_for_status()
    analyses = response.json()["results"]

    collection = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=5000)[config.MONGO_DB][
        config.MONGO_COLLECTION
    ]
    collection.create_index("url", unique=True, sparse=True)
    stored = 0
    for index, (tweet, analysis) in enumerate(zip(tweets, analyses)):
        tweet = dict(tweet)
        tweet.setdefault("url", f"https://twitter.com/i/web/status/fixture-{index + 1}")
        document = normalize_tweet(tweet, analysis=analysis)
        document["source_type"] = "twitter_fixture"
        collection.update_one({"url": document["url"]}, {"$set": document}, upsert=True)
        stored += 1
    print(f"Stored {stored} fixture tweets in {config.MONGO_DB}.{config.MONGO_COLLECTION}")


if __name__ == "__main__":
    main()
