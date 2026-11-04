"""Twitter/X API v2 streaming client (optional real-data path).

This file is a working skeleton, not part of the default demo.  It requires a
Tweepy version that supports StreamingClient and an X API bearer token with
access to the filtered stream endpoint.

    export TWITTER_BEARER_TOKEN=...
    python RealTimeScripts/StreamingTwitterAPIV2.py

See docs/TWITTER_V2_MIGRATION.md for rules, access levels, and troubleshooting.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import requests
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402
from news_analysis.schema import normalize_tweet  # noqa: E402

try:
    from tweepy import StreamingClient, StreamRule
except ImportError:  # pragma: no cover
    StreamingClient = None
    StreamRule = None

RULES = ["(AAPL OR Apple OR MSFT OR Microsoft OR TSLA OR Tesla) lang:en -is:retweet"]


class Listener(StreamingClient if StreamingClient else object):
    def on_tweet(self, tweet):
        text = getattr(tweet, "text", "") or ""
        try:
            response = requests.post(
                f"{config.SERVICE_URL.rstrip('/')}/analyze",
                json={"text": text},
                timeout=60,
            )
            response.raise_for_status()
            analysis = response.json()
        except Exception as exc:  # noqa: BLE001
            print(f"prediction service error: {exc}")
            return
        if not analysis.get("is_business"):
            return
        document = normalize_tweet(
            {
                "text": text,
                "created_at": getattr(tweet, "created_at", None),
                "source": "twitter-v2",
                "tickers": [],
            },
            analysis=analysis,
        )
        document["url"] = f"https://twitter.com/i/web/status/{getattr(tweet, 'id', '')}"
        collection = MongoClient(config.MONGO_URI)[config.MONGO_DB][config.MONGO_COLLECTION]
        collection.update_one({"url": document["url"]}, {"$set": document}, upsert=True)
        print(f"stored tweet {getattr(tweet, 'id', '')}")


def main() -> None:
    if StreamingClient is None:
        raise SystemExit("Install tweepy>=4.14: pip install tweepy")
    token = os.getenv("TWITTER_BEARER_TOKEN")
    if not token:
        raise SystemExit("Set TWITTER_BEARER_TOKEN in .env or the environment.")
    client = Listener(token)
    existing = {rule.value for rule in client.get_rules().data or []}
    for rule in RULES:
        if rule not in existing:
            client.add_rules(StreamRule(rule))
    print("Listening for financial tweets...")
    client.filter(tweet_fields=["created_at"])


if __name__ == "__main__":
    main()
