# Real-Time News Analysis for Stock Market

End-of-masters (PFE) project that collects financial news and tweets, filters
business-related text, predicts sentiment, associates items with stock tickers,
and stores the enriched records for analysis.

## Overview

The project combines two text classifiers:

- a **news-vs-other** classifier (TF-IDF + chi-square feature selection +
  Random Forest), and
- a **polarity** classifier (BERT fine-tuned with `ktrain`, predicting
  Positive / Neutral / Negative).

Both models are exposed by a small Flask REST service. Collector scripts use
that service to enrich NewsAPI articles and Twitter/X posts before writing them
to MongoDB.

## Pipeline

1. **Prepare data** — `Preprocessing/` builds balanced sentiment data and the
   business-vs-other news dataset from the raw files in `Data/`.
2. **Train models** — `MachineLearning/NewsClassifier.ipynb` and
   `MachineLearning/NewsPolarityClassifier.ipynb` produce the serialized
   artifacts consumed by the service.
3. **Serve predictions** — `NewsPredictionMicroservice/app.py` exposes
   `POST /NewsOrNot` and `POST /Polarity`.
4. **Collect** — historical backfill and real-time streaming scripts pull news
   and tweets, call the service, and attach ticker symbols.
5. **Store** — enriched records are inserted into MongoDB collections.

## Repository layout

| Path | Purpose |
|---|---|
| `HistoricalNewsCollector.py` | Historical NewsAPI collection and enrichment |
| `RealTimeScripts/` | Streaming NewsAPI and Twitter collectors |
| `NewsPredictionMicroservice/` | Flask API serving the two classifiers |
| `MachineLearning/` | Training notebooks for the news and polarity models |
| `Preprocessing/` | Dataset preparation scripts |
| `Data/` | Raw and generated datasets, ticker lists |
| `Documents/` | PFE report and presentation |
| `Resources/` | Reference papers, articles, and sample code |
| `notebooks/colab/` | Early Colab notebooks imported from a separate repo |
| `integrations/` | Companion projects that use the prediction service |
| `labs/` | Older Kafka/Elasticsearch experiments kept for reference |
| `docs/` | Merge/provenance notes |

## Microservice API

The Flask service listens on port `5000` by default.

| Method | Endpoint | Body | Response |
|---|---|---|---|
| `POST` | `/NewsOrNot` | `text=<string>` | `0` (other) or `1` (business news) |
| `POST` | `/Polarity` | `text=<string>` | `-1` (negative), `0` (neutral), `1` (positive) |

## Running locally

The code targets the Python 3 environment used for the original project
(2021–2022). Install the libraries the scripts import, for example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas scikit-learn ktrain flask flask-restful pymongo \
  newsapi-python tweepy dill jupyter
```

Configuration values (MongoDB URI, database/collection names, NewsAPI keys) are
read from `config.py`. Replace them with your own values before running the
collectors. Credentials are intentionally not documented here.

Model artifacts are written to `PythonObjects/`, which is not tracked. Generate
them by running the notebooks before starting the microservice.

Typical commands:

```bash
# Historical collection (from the repository root)
python HistoricalNewsCollector.py

# Real-time NewsAPI collection
cd RealTimeScripts
python StreamingNewsAPI.py

# Twitter collection
cd RealTimeScripts
python StreamingTwitterAPI.py

# Prediction service
cd NewsPredictionMicroservice
python app.py
```

## Data and model artifacts

- `Data/stocks_cleaned.csv` and `Data/GeneratedData/tickers.csv` provide the
  ticker universe.
- `Data/CollectedData/LabeledData.json` is the labeled sentiment source.
- `Data/GeneratedData/LabeledNews.csv` is the combined title + text sentiment
  dataset used to train the polarity model.
- `Data/GeneratedData/NewsClasses(Other=0, Buissness=1).csv` is the
  business-vs-other training set.
- `PythonObjects/` contains local model artifacts and is gitignored.

## Imported history

Four earlier repositories were merged into this one with their commit history
preserved:

- `google-colab-notebooks` → `notebooks/colab/`
- `Kafka-Streams-Tweets-To-ElasticSearch` →
  `integrations/kafka-streams-crypto-tweets/`
- `kafka-with-twitter-and-elasticsearch` →
  `labs/kafka-twitter-elasticsearch/`
- `elasticsearch-with-python` → `labs/elasticsearch-python/`

See `docs/PROVENANCE.md` for original HEADs, source branches, and omitted files.

## Academic context

This repository contains the code and report for my end-of-masters project
(PFE). The written report and presentation are in `Documents/`.
