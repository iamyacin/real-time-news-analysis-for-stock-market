# Migrating the Twitter collector to API v2

## Why the original script no longer works

`RealTimeScripts/StreamingTwitterAPI.py` in the 2020 project used:

- `tweepy.StreamListener`
- `tweepy.OAuthHandler` with consumer/token secrets
- the v1.1 filtered stream endpoint

`StreamListener` was removed in Tweepy 4.x, and X's current API is v2. The
original code is preserved in git history and the report; the restored
repository uses fixture mode by default.

## Default path: fixture mode

```bash
python RealTimeScripts/StreamingTwitterAPI.py
```

This reads `Data/fixtures/tweets_sample.json`, calls the prediction service, and
stores the records in MongoDB exactly like the live path. It requires no X
account.

## Real path: API v2 filtered stream

`RealTimeScripts/StreamingTwitterAPIV2.py` is a working skeleton. Requirements:

1. An X developer account with access to the **filtered stream** endpoint.
2. A **bearer token**.
3. `tweepy>=4.14`.

Install:

```bash
pip install "tweepy>=4.14"
```

Configure:

```bash
export TWITTER_BEARER_TOKEN=your_bearer_token
# optional
export SERVICE_URL=http://localhost:5000
```

Run:

```bash
python RealTimeScripts/StreamingTwitterAPIV2.py
```

The script:

- creates filters for the demo tickers;
- streams matching English tweets;
- excludes retweets;
- calls `POST /analyze`;
- stores only business-related tweets in MongoDB;
- uses the same schema as the news pipeline.

## API v1.1 → v2 mapping

| v1.1 (original) | v2 (current) |
|---|---|
| `StreamListener.on_data(raw)` | `StreamingClient.on_tweet(tweet)` |
| `Stream(auth, listener).filter(follow=...)` | `StreamingClient.filter(...)` with rules |
| consumer key/secret + access token/secret | bearer token (app auth) |
| `tweet["text"]` | `tweet.text` |
| `tweet["user"]["screen_name"]` | `tweet.author_id` / expansions |
| follow users | `from:` rules or filtered stream rules |

## Rules

The skeleton uses:

```text
(AAPL OR Apple OR MSFT OR Microsoft OR TSLA OR Tesla) lang:en -is:retweet
```

Rules are limited by your X access level. Check existing rules before adding
duplicates:

```python
for rule in client.get_rules().data or []:
    print(rule.id, rule.value)
```

Delete stale rules with `client.delete_rules([rule_id])`.

## Access and rate limits

- Free/basic access may not include filtered stream or may have very low caps.
- The filtered stream is billed/limited by your X plan.
- Handle `429` with backoff; do not restart aggressively.
- Store the tweet ID and use `update_one(..., upsert=True)` to avoid duplicates.

## Troubleshooting

| Problem | Fix |
|---|---|
| `ImportError: StreamingClient` | `pip install "tweepy>=4.14"` |
| `401 Unauthorized` | Check the bearer token and app permissions |
| `403 Forbidden` | Your X plan does not include the filtered stream |
| No tweets | Broaden rules; check `client.get_rules()` and account access |
| Service errors | Start the prediction service and check `SERVICE_URL` |
