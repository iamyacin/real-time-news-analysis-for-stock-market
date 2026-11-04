# Colab notebooks

Early Google Colab experiments imported from the separate
`google-colab-notebooks` repository.

- `business-news-labeling.ipynb` — loads `OtherNews.csv` and
  `LabeledNews.csv`, explores the news categories, and prepares the
  business-vs-other labeling used by the news classifier.
- `labeled-data-exploration.ipynb` — loads `LabeledData.json` and converts the
  records into a dataframe for exploration.
- `NewsPolarityClassifier_colab.ipynb` — cleaned 2026 Colab version of the
  original ktrain BERT polarity experiment. See
  `docs/TRAIN_POLARITY_MODEL.md`.

The notebooks were originally run with the datasets in the Colab working
directory, so the relative paths (`OtherNews.csv`, `LabeledNews.csv`,
`LabeledData.json`) need to be adjusted when running them from this repository.
The equivalent files live under `Data/`.

Two files from the source repository were intentionally not imported:

- `NewsPolarityClassifier.ipynb` — byte-identical to
  `MachineLearning/NewsPolarityClassifier.ipynb` in this repository.
- `Untitled-FRI-Auto.ipynb` — an unrelated car-parts directory generator.

Both remain available in the archived source repository and its mirror backup.
See `docs/PROVENANCE.md`.
