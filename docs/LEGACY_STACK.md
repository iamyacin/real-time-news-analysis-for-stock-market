# Legacy 2020 stack

The original PFE code targeted Python 3.10, TensorFlow/ktrain, pandas 1.x, and
Tweepy 3.x. The 2026 restoration keeps the original notebooks and report intact
and provides a modern runnable path. This page documents the legacy option.

## Original versions used by the report

| Component | Version / library |
|---|---|
| Python | 3.10.5 |
| Deep learning | TensorFlow + Keras via ktrain |
| ML | scikit-learn 1.1.x, pandas 1.x, NumPy 1.x |
| Web service | Flask + Flask-RESTful |
| Database | MongoDB Atlas |
| News | NewsAPI |
| Twitter | Tweepy 3.x `StreamListener` |

The original notebooks are:

- `MachineLearning/NewsClassifier.ipynb`
- `MachineLearning/NewsPolarityClassifier.ipynb`

The original scripts are still visible in git history. Find the commit before the
2026 restoration and inspect it:

```bash
git log --oneline -- HistoricalNewsCollector.py
git show <original-commit>:HistoricalNewsCollector.py
git show <original-commit>:RealTimeScripts/StreamingTwitterAPI.py
```

## Legacy Python environment

```bash
python3.10 -m venv .venv-legacy
source .venv-legacy/bin/activate
pip install -r legacy/requirements-py310.txt
```

Then run the original scripts from the repository root. The legacy BERT
predictor must be placed at:

```text
PythonObjects/legacy/PolarityClassifier/BertPolarityClassifier/
```

and the service must use:

```bash
POLARITY_BACKEND=legacy
```

See `docs/TRAIN_POLARITY_MODEL.md` for training and installation.

## What was restored in 2026

| Area | Change |
|---|---|
| Service artifact names | `Classifier(RF).pickle` path mismatch fixed; modern joblib artifacts |
| Models | RF and offline polarity retrained by scripts; FinBERT default |
| Paths | Resolved from the repository root via `config.py` |
| Credentials | Removed from code; `.env` |
| Database | Local Docker default; Atlas configurable |
| Collectors | Call the HTTP service instead of importing ktrain |
| React/Spring | Restored from `dda2c55^` and adapted |
| Data schema | `publishedAt` ISO string; `prediction` label string; `$TICKER` |
| Demo | Fixtures + seed script + Streamlit |

## Why the legacy path is not the default demo

- TensorFlow + ktrain wheels are large and sensitive to Python/GPU versions.
- The original BERT predictor was not committed to git.
- The public demo must work from a clean clone without a GPU or a cloud model.

The legacy path remains fully documented so the report's method can be
reproduced.

## Authorship

The original 2020 PFE was a pair project by **Yassine DAOUJI** and
**Mohammed AZZOUZ**. Yassine led the overall project and did the data
collection, ML, backend, and report work; Mohammed built the original
React/Spring report application.

The 2026 project was reviewed and enhanced by **Yassine DAOUJI in collaboration
with the OpenCode AI coding agent, using the DeepSeek V4.1 Flash model**. See
[`docs/AI_ASSISTANCE.md`](AI_ASSISTANCE.md) for the exact split between the
original work and the AI-assisted restoration.
