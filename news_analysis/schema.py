"""Normalization helpers for records written to MongoDB."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def polarity_label(score: int) -> str:
    return {-1: "Negative", 0: "Neutral", 1: "Positive"}.get(int(score), "Neutral")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ticker_with_prefix(ticker: str | None) -> str | None:
    if not ticker:
        return None
    ticker = str(ticker).strip().upper()
    return ticker if ticker.startswith("$") else f"${ticker}"


def normalize_newsapi_article(
    article: dict[str, Any],
    *,
    ticker: str | None,
    analysis: dict[str, Any] | None = None,
    source_type: str = "newsapi",
) -> dict[str, Any]:
    """Convert a NewsAPI-like article into the shared MongoDB schema.

    ``publishedAt`` stays an ISO string because the restored Spring backend
    aggregates it with MongoDB ``$substr`` operations.
    """
    analysis = analysis or {}
    ticker = _ticker_with_prefix(ticker or article.get("ticker"))
    description = article.get("description") or ""
    title = article.get("title") or ""
    text = article.get("text") or description or title
    url = article.get("url") or article.get("news_url")

    return {
        "source_type": source_type,
        "source": article.get("source") or article.get("source_name") or "Unknown",
        "author": article.get("author"),
        "title": title,
        "description": description,
        "text": text,
        "url": url,
        "urlToImage": article.get("urlToImage") or article.get("image_url"),
        "publishedAt": article.get("publishedAt") or article.get("date") or utc_now_iso(),
        "ticker": ticker,
        "tickers": [ticker] if ticker else [],
        "is_business": int(analysis.get("is_business", 1)),
        "prediction": analysis.get("polarity_label", "Neutral"),
        "polarity": analysis.get("polarity_label", "Neutral"),
        "polarity_score": int(analysis.get("polarity", 0)),
        "polarity_backend": analysis.get("backend"),
        "collected_at": utc_now_iso(),
    }


def normalize_tweet(
    tweet: dict[str, Any],
    *,
    analysis: dict[str, Any] | None = None,
) -> dict[str, Any]:
    analysis = analysis or {}
    tickers = tweet.get("tickers") or []
    if isinstance(tickers, str):
        tickers = [tickers]
    tickers = [_ticker_with_prefix(t) for t in tickers if t]
    ticker = tickers[0] if tickers else None
    text = tweet.get("text") or ""
    return {
        "source_type": "twitter",
        "source": tweet.get("source") or tweet.get("user") or "twitter",
        "author": tweet.get("author") or tweet.get("user"),
        "title": text[:180],
        "description": text,
        "text": text,
        "url": tweet.get("url"),
        "urlToImage": None,
        "publishedAt": tweet.get("created_at") or utc_now_iso(),
        "ticker": ticker,
        "tickers": tickers,
        "is_business": int(analysis.get("is_business", 1)),
        "prediction": analysis.get("polarity_label", "Neutral"),
        "polarity": analysis.get("polarity_label", "Neutral"),
        "polarity_score": int(analysis.get("polarity", 0)),
        "polarity_backend": analysis.get("backend"),
        "collected_at": utc_now_iso(),
    }
