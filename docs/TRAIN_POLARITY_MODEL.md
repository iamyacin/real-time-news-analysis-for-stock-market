# Train and install the polarity model

The project supports three polarity paths:

| Path | Use case | Training needed |
|---|---|---|
| FinBERT (`POLARITY_BACKEND=finbert`) | default demo | no |
| HuggingFace BERT (`POLARITY_BACKEND=hf`) | modern fine-tune | yes, GPU recommended |
| Legacy ktrain BERT (`POLARITY_BACKEND=legacy`) | faithful PFE notebook | yes, Colab GPU |

The default demo never requires training. This document explains how to
reproduce and install the trained models.

## Dataset

`Data/GeneratedData/LabeledNews.csv` contains 3,795 balanced rows:

```text
News,Sentiment
"Ferrari Profit Acceleration Eases A Bit ...",Negative
...
```

Classes: `Negative`, `Neutral`, `Positive` (1,265 each).

## Option A — original ktrain BERT (faithful to the report)

Use the cleaned Colab notebook:

`notebooks/colab/NewsPolarityClassifier_colab.ipynb`

### Steps

1. Open the notebook in Google Colab.
2. **Runtime → Change runtime type → GPU** (T4 is enough).
3. Run the install cell:

   ```python
   !pip install -q ktrain
   ```

   If Colab's TensorFlow version conflicts with ktrain, see Troubleshooting.
4. Upload `Data/GeneratedData/LabeledNews.csv` when prompted.
5. Run the data, split, `texts_from_array`, model, learner, and
   `fit_onecycle(2e-5, 4)` cells.
6. Run `learner.validate(...)` to see accuracy, precision, recall, and F1.
7. Run the predictor cell to check a sample prediction.
8. The final cell saves and downloads:

   ```text
   BertPolarityClassifier.zip
   ```

### Install the predictor

Unzip it, then place the folder here:

```text
PythonObjects/legacy/PolarityClassifier/BertPolarityClassifier/
```

Expected structure:

```text
PythonObjects/legacy/PolarityClassifier/BertPolarityClassifier/
├── config.json
├── model.h5
├── preproc/
└── ...
```

The exact files depend on the ktrain version; keep the whole folder.

### Run the legacy backend

The legacy backend imports `ktrain` and TensorFlow, so use the Python 3.10
legacy environment:

```bash
python3.10 -m venv .venv-legacy
source .venv-legacy/bin/activate
pip install -r legacy/requirements-py310.txt
pip install Flask flask-cors pymongo python-dotenv
```

Set:

```bash
POLARITY_BACKEND=legacy
LEGACY_POLARITY_DIR=PythonObjects/legacy/PolarityClassifier/BertPolarityClassifier
```

Start the service:

```bash
python NewsPredictionMicroservice/app.py
```

Check:

```bash
curl http://localhost:5000/health
```

The `polarity.active` field should become `legacy:BertPolarityClassifier` after
the first prediction. If it falls back to `sklearn`, check the `last_error` field
or the service logs.

> The default Docker image does not include TensorFlow/ktrain. The legacy path is
> intended for the Python 3.10 environment described in `docs/LEGACY_STACK.md`.

## Option B — HuggingFace BERT fine-tune

GPU recommended. The script saves a model that the modern service can load.

```bash
uv pip install -r requirements-ml.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu  # or CUDA wheel
python scripts/train_polarity.py \
  --base-model bert-base-uncased \
  --epochs 3 \
  --batch-size 8 \
  --output PythonObjects/PolarityClassifier
```

Then set:

```bash
POLARITY_BACKEND=hf
POLARITY_MODEL_DIR=PythonObjects/PolarityClassifier
```

Restart the service. `POST /analyze` should report a backend starting with `hf:`.

The script uses an 80/20 stratified split, `max_length=256`, and saves
`training_metrics.json` alongside the model.

## Option C — FinBERT (no training)

This is the default demo path:

```bash
POLARITY_BACKEND=finbert
POLARITY_MODEL=ProsusAI/finbert
```

The first request downloads the model from HuggingFace. If the download fails,
the service falls back to the offline TF-IDF model.

On the bundled fixture labels, pretrained FinBERT scores about **57.5%** while
the project-trained TF-IDF model scores **82.5%**. FinBERT is useful for
demonstrating the BERT path, but for the best accuracy on this dataset use
`POLARITY_BACKEND=sklearn` or fine-tune your own BERT (Option A/B).

To pre-download:

```bash
python - <<'PY'
from transformers import pipeline
pipeline("text-classification", model="ProsusAI/finbert")
PY
```

## Offline fallback

If FinBERT and a trained BERT model are unavailable:

```bash
POLARITY_BACKEND=sklearn
```

This loads `PythonObjects/PolaritySklearn/` (TF-IDF + Logistic Regression,
~80.5% on the bundled split). `scripts/ensure_models.py` trains it automatically.

## Verify the installation

```bash
curl -s http://localhost:5000/health | python -m json.tool
curl -s -X POST http://localhost:5000/analyze \
  -H 'Content-Type: application/json' \
  -d '{"text":"Apple beats earnings expectations as services revenue hits a record"}' \
  | python -m json.tool
```

Expected fields:

```json
{
  "is_business": 1,
  "polarity": 1,
  "polarity_label": "Positive",
  "backend": "finbert:ProsusAI/finbert"
}
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named ktrain` | Use the Python 3.10 legacy environment, not the default 3.11 venv |
| TensorFlow/ktrain version conflict | Pin `tensorflow==2.10.1` and `ktrain==0.38.2`; restart the Colab runtime |
| Colab runs out of memory | Reduce batch size to 4 or 2; keep `maxlen=350` |
| Runtime disconnects | Save checkpoints to Google Drive during training |
| `last_error` mentions a missing model | Check the path and that the whole predictor folder was copied |
| FinBERT download fails | Use `POLARITY_BACKEND=sklearn` or pre-download on a networked machine |
| Legacy service starts but falls back | Check `curl /health` and `docker compose logs` for the import error |

## Results reported in the PFE

| Model | Accuracy |
|---|---|
| Random Forest business filter | 88.9% (restored split) |
| Original BERT polarity | 87% (report) |
| Offline TF-IDF polarity | 80.5% (restored fallback) |

Use `python scripts/evaluate.py` to compare the running backend against the
bundled labeled fixtures.
