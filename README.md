# Real-Time News Analysis for Stock Market

End-of-studies (PFE) project that collects financial news and tweets, filters
business-related text, predicts sentiment, associates items with stock tickers,
and stores the enriched records for analysis.

The original project was built in 2020. This repository preserves that work
and adds a small 2026 restoration so it can be cloned, run, and demonstrated
without private cloud credentials or expired API keys.

## What you get

- **Two working UIs**
  - Streamlit dashboard at `http://localhost:8501` (new)
  - Original React + Spring Boot admin app at `http://localhost:3000` (restored from git history)
- **Working prediction service** at `http://localhost:5000`
  - `/NewsOrNot` — business vs other news (Random Forest)
  - `/Polarity` — positive / neutral / negative sentiment
  - `/analyze` and `/analyze/batch` — JSON endpoints used by the collectors and dashboards
- **Offline demo data** generated from the original labeled dataset
- **Local MongoDB** via Docker, with optional MongoDB Atlas configuration
- **Original notebooks, report, and presentation** preserved under `MachineLearning/`, `Documents/`, and `notebooks/`

## Screenshots

| Streamlit dashboard | Restored React report UI |
|---|---|
| ![Streamlit dashboard](docs/screenshots/streamlit.png) | ![Legacy dashboard](docs/screenshots/legacy-dashboard.png) |

More screenshots: [login](docs/screenshots/legacy-login.png),
[societies](docs/screenshots/legacy-societies.png),
[society details](docs/screenshots/legacy-society-details.png),
[news list](docs/screenshots/legacy-society-news.png),
[charts](docs/screenshots/legacy-society-charts.png),
[live analyzer](docs/screenshots/streamlit-analyzer.png).

## Architecture

```mermaid
flowchart LR
    A[NewsAPI / fixtures / tweets] --> B[Python collectors]
    B -->|HTTP| C[Flask prediction service]
    C --> D[(MongoDB)]
    D --> E[Spring Boot API :8081]
    E --> F[React report UI :3000]
    D --> G[Streamlit dashboard :8501]
    C --> H[Random Forest business filter]
    C --> I[FinBERT / HF BERT / legacy ktrain]
```

The old React/Spring app and the new Streamlit dashboard read the same MongoDB
collections, so both show the same data.

## Quick start (Docker)

Requirements: Docker with Compose.

```bash
cp .env.example .env
docker compose up --build
```

Then open:

| Service | URL |
|---|---|
| Streamlit dashboard | http://localhost:8501 |
| Original React UI | http://localhost:3000 |
| Legacy login | `admin` / `admin123` |
| Prediction service | http://localhost:5000/health |
| Spring API | http://localhost:8081/api/health |

The demo uses bundled fixtures and a local MongoDB container; no API keys are
required. On the first run the service tries FinBERT and downloads it if
network access is available. If the download fails, it automatically falls back
to the offline TF-IDF polarity model.

To start only the new dashboard:

```bash
docker compose up --build mongo prediction-service seed streamlit
```

To start only the restored report UI:

```bash
make legacy-ui
```

### Using MongoDB Atlas

Local Docker MongoDB is the default. To make Atlas the primary database while
keeping the local container as a fallback, add a fresh URI to `.env`:

```bash
MONGO_URI_DOCKER=mongodb+srv://USER:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
```

Then restart the stack:

```bash
docker compose up -d
```

`MONGO_URI_DOCKER` is used by the containers; `MONGO_URI` is used by Python
scripts run on the host. Never commit either URI.

## Local development (without Docker for Python)

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# optional: local FinBERT / HuggingFace support
# uv pip install torch --index-url https://download.pytorch.org/whl/cpu
# uv pip install -r requirements-ml.txt

docker compose up -d mongo
python scripts/ensure_models.py
python NewsPredictionMicroservice/app.py    # terminal 1
python scripts/seed_demo.py                 # terminal 2
streamlit run dashboard/app.py              # terminal 3
```

Useful Make targets:

```bash
make setup        # create .venv and install dependencies
make train        # train/restore RF and offline polarity artifacts
make serve        # run Flask service
make seed         # load fixtures into MongoDB
make dashboard    # run Streamlit
make demo         # full Docker Compose stack
make legacy-ui    # Spring + React only
make test         # Python tests
make smoke        # end-to-end check of both UIs and APIs
make collect      # live NewsAPI collection (needs NEWSAPI_KEY)
```

## Data sources

### Default: bundled fixtures

`Data/fixtures/news_sample.json` contains 120 recent-dated articles generated
from `Data/CollectedData/LabeledData.json`. `Data/fixtures/tweets_sample.json`
contains sample tweets. Dates are shifted close to today so the restored Spring
dashboard's 90-day charts are populated.

### Optional: live NewsAPI

Add a key to `.env`:

```bash
NEWSAPI_KEY=your_key_here
```

Then run:

```bash
python scripts/collect_news.py --limit 5
```

NewsAPI free plans are limited and development-only; the demo does not depend on
them. The `HistoricalNewsCollector.py` and `RealTimeScripts/StreamingNewsAPI.py`
entrypoints now delegate to the same restored collector.

### Twitter/X

The default path is fixture mode:

```bash
python RealTimeScripts/StreamingTwitterAPI.py
```

Real streaming requires X API v2 access. See
[`docs/TWITTER_V2_MIGRATION.md`](docs/TWITTER_V2_MIGRATION.md) and
`RealTimeScripts/StreamingTwitterAPIV2.py`.

## Models

| Model | Purpose | Result | Where |
|---|---|---|---|
| Random Forest + CountVectorizer + chi² | Business vs other news | **88.9% accuracy** on the bundled split | `scripts/train_news_classifier.py` |
| TF-IDF + Logistic Regression | Offline polarity fallback | **80.5% accuracy** | `scripts/train_polarity_sklearn.py` |
| FinBERT (`ProsusAI/finbert`) | Demo polarity model | pretrained financial BERT; **57.5%** on the bundled fixture labels | `NewsPredictionMicroservice/models.py` |
| Original ktrain BERT | Faithful PFE polarity model (87% in the report) | trained on Colab | [`docs/TRAIN_POLARITY_MODEL.md`](docs/TRAIN_POLARITY_MODEL.md) |

The offline TF-IDF model is trained on the project's own labels and scores
**82.5%** on the bundled fixtures, while pretrained FinBERT is a different
financial-domain model and scores lower here. The default demo uses FinBERT so
the BERT path is exercised; set `POLARITY_BACKEND=sklearn` for the highest
accuracy on this dataset.

Switch polarity backend in `.env`:

```bash
POLARITY_BACKEND=finbert   # default demo
POLARITY_BACKEND=sklearn   # fast, fully offline
POLARITY_BACKEND=hf        # local HuggingFace model
POLARITY_BACKEND=legacy    # original ktrain predictor (Python 3.10 env)
```

Model binaries are not committed. `python scripts/ensure_models.py` trains the
small local models on first use.

## Repository layout

```text
HistoricalNewsCollector.py       # restored entrypoint for historical collection
RealTimeScripts/                 # NewsAPI + Twitter entrypoints
NewsPredictionMicroservice/      # Flask service and model backends
news_analysis/                   # shared preprocessing and MongoDB schema
scripts/                         # training, fixtures, seeding, evaluation, collectors
dashboard/                       # Streamlit dashboard
apps/legacy-ui/backend/          # restored Spring Boot API
apps/legacy-ui/frontend/         # restored React/CoreUI app
MachineLearning/                 # original training notebooks
notebooks/colab/                 # original + cleaned Colab training notebooks
Data/                            # raw data and generated demo fixtures
Documents/                       # PFE report and presentation
docs/                            # architecture, demo, training, migration, security
```

## Original vs restored

| Original 2020 | 2026 restoration |
|---|---|
| Python 3.10, TensorFlow/ktrain, old pandas/Tweepy | Python 3.11 default; original stack documented in `legacy/` |
| MongoDB Atlas + hardcoded credentials | Local Docker MongoDB default; Atlas via `.env` |
| Missing BERT artifacts | FinBERT default + offline fallback + Colab training guide |
| Service loaded a mismatched artifact name | Artifact contract fixed; models auto-trained |
| Collectors loaded ktrain directly | Collectors call the prediction service |
| React/Spring app removed from HEAD | Restored from git history and adapted to the restored data schema |
| No demo data | 120 news fixtures + 40 tweets generated from the labeled dataset |

## 2026 restoration and AI assistance

The original 2020 PFE work — data collection, model-training notebooks,
report, presentation, original application code, and datasets — was authored by
**Yassine DAOUJI**.

The 2026 project was reviewed and enhanced by **Yassine DAOUJI in collaboration
with the OpenCode AI coding agent, using the DeepSeek V4.1 Flash model**. The author defined the goals and scope, reviewed the technical choices,
and ran and validated the resulting stack. The agent implemented and documented
the restoration work: the repaired prediction service, FinBERT/offline polarity
backends, normalized data pipeline, fixtures, Streamlit dashboard, restored
React/Spring UI, Docker setup, tests, and documentation.

The full breakdown is in [`docs/AI_ASSISTANCE.md`](docs/AI_ASSISTANCE.md).

## Documentation

- [`docs/AI_ASSISTANCE.md`](docs/AI_ASSISTANCE.md) — original work vs 2026 AI-assisted restoration
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/DEMO.md`](docs/DEMO.md) — 5-minute defense walkthrough
- [`docs/TRAIN_POLARITY_MODEL.md`](docs/TRAIN_POLARITY_MODEL.md) — notebook training and model installation
- [`docs/TWITTER_V2_MIGRATION.md`](docs/TWITTER_V2_MIGRATION.md)
- [`docs/LEGACY_STACK.md`](docs/LEGACY_STACK.md)
- [`docs/SECURITY.md`](docs/SECURITY.md)

## Security

The original repository contained hardcoded MongoDB, NewsAPI, and Twitter
credentials. They have been removed from the current code and replaced with
environment variables. The old values still exist in git history, so **rotate
any key that may still be active** and see [`docs/SECURITY.md`](docs/SECURITY.md)
for the history-purge procedure.

Do not commit `.env`.

## Academic context

This repository accompanies the PFE report:

- `Documents/RapportPFE_BusinessNewsAnalysis.pdf`
- `Documents/Rapport_PFE_Business_News_Analysis.docx`
- `Documents/Présentation PFE.pptx`

The original notebooks are kept for transparency; the restored code is a
reproducibility layer around them, not a replacement for the academic work.
