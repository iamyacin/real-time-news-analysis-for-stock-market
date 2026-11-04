# 5-minute demo

## Start

```bash
cp .env.example .env
docker compose up --build
```

Wait for:

- MongoDB healthy
- prediction service healthy
- seed job completed
- Streamlit and legacy UI running

## 1. Streamlit — new dashboard

Open <http://localhost:8501>.

Show:

1. **Overview** — number of articles, positive/neutral/negative split, top tickers.
2. **Filters** — choose a ticker and a sentiment, watch the table and charts update.
3. **Ticker explorer** — sentiment over time for one company.
4. **Analyze text** — paste:

   > Apple beats earnings expectations as services revenue hits a record.

   Show the business prediction, polarity label, score, and backend.

## 2. Original React + Spring UI — report screenshots

Open <http://localhost:3000>.

Login:

```text
username: admin
password: admin123
```

Show:

1. Dashboard — top tickers and sentiment chart.
2. Societies — seeded companies with sectors.
3. Society details — news list and statistics for a ticker.
4. News links open in a new tab.

Both UIs read the same MongoDB data, so the numbers match.

Run the automated end-to-end check:

```bash
make smoke
```

## 3. Scientific work

Open:

- `MachineLearning/NewsClassifier.ipynb` — original Random Forest experiment.
- `MachineLearning/NewsPolarityClassifier.ipynb` — original BERT experiment.
- `Documents/RapportPFE_BusinessNewsAnalysis.pdf` — full report.

Explain:

- RF business filter: 88.9% on the restored split.
- BERT polarity: 87% in the original report.
- Demo default: pretrained FinBERT (57.5% on the bundled fixture labels).
- Offline fallback: project-trained TF-IDF polarity (82.5% on the same fixtures).
- Set `POLARITY_BACKEND=sklearn` for the highest accuracy on this dataset.

## 4. Optional live collection

```bash
# add NEWSAPI_KEY to .env first
python scripts/collect_news.py --limit 5
```

Then refresh the dashboard.

## Troubleshooting

| Problem | Fix |
|---|---|
| Streamlit says MongoDB unavailable | `docker compose up -d mongo` then `make seed` |
| No data | `make seed` |
| FinBERT download slow | set `POLARITY_BACKEND=sklearn` in `.env` and restart |
| Legacy UI login fails | check `docker compose logs legacy-backend`; user is seeded as `admin/admin123` |
| Legacy UI charts empty | fixtures use recent dates; re-run `python scripts/generate_fixtures.py` and `make seed` |
| Port already in use | stop the conflicting service or change the port mapping |
