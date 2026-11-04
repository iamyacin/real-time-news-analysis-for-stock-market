# Demo fixtures

Generated from `Data/CollectedData/LabeledData.json` by:

```bash
python scripts/generate_fixtures.py
```

Files:

- `news_sample.json` — 120 NewsAPI-shaped articles, 40 per sentiment class.
- `tweets_sample.json` — 40 sample tweets.
- `societies_seed.csv` — tickers, names, sectors, and industries used by both UIs.

`scripts/seed_demo.py` shifts any old fixture date into the last ~60 days before
inserting it, so the restored Spring UI's 90-day charts stay populated.
