# Elasticsearch Python lab

MovieLens CSV → Elasticsearch bulk-indexing lab imported from the
`elasticsearch-with-python` repository.

- `IndexRatings.py` creates the `ratings` index from `ratings.csv`.
- `IndexTags.py` creates the `tags` index from `tags.csv`.

Both scripts expect the CSV files in the current working directory, so run them
from `data/`:

```bash
cd data
python ../IndexRatings.py
python ../IndexTags.py
```

Elasticsearch is expected on `localhost:9200`. The scripts use the older
`elasticsearch` Python client API, so an appropriate client version may be
required.
