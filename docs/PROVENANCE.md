# Repository merge provenance

Date: **2026-10-31**

Four earlier repositories were imported into this project with their commit
history preserved. Each source was rewritten with:

```bash
git filter-repo --to-subdirectory-filter <destination-prefix> --force
```

This keeps commit messages, authorship, and dates, but changes commit hashes
because every historical path gains the destination prefix. Mirror clones and a
`git bundle` of the pre-merge state were created before the import.

| Source repository | Branch | Original HEAD | Imported path | Merge commit | Notes |
|---|---|---|---|---|---|
| `iamyacin/google-colab-notebooks` | `master` | `0b82c77aaab1205600385d19a6b6c6b1ebd5bd88` | `notebooks/colab/` | `b5b49a0` | Only `Untitled0.ipynb` and `Untitled1.ipynb` were imported |
| `iamyacin/Kafka-Streams-Tweets-To-ElasticSearch` | `main` | `2be874a151b363d5f299a743f90e1f7151539dd9` | `integrations/kafka-streams-crypto-tweets/` | `8f2b3a7` | Full source history imported |
| `iamyacin/kafka-with-twitter-and-elasticsearch` | `master` | `a481b182f98aa27b0a0e1f2b2e11a3ac576901b4` | `labs/kafka-twitter-elasticsearch/` | `96eba60` | Full source history imported |
| `iamyacin/elasticsearch-with-python` | `master` | `36586a4e99a2bdc8dfa12903818fd20bcd0689bc` | `labs/elasticsearch-python/` | `b945dc5` | Full source history imported |

## Files intentionally omitted from the Colab import

`google-colab-notebooks` contained four notebooks. Two were not imported:

- `NewsPolarityClassifier.ipynb` — byte-identical to
  `MachineLearning/NewsPolarityClassifier.ipynb` in this repository.
- `Untitled-FRI-Auto.ipynb` — an unrelated car-parts directory generator.

Both remain available in the archived source repository and its mirror backup.

## Post-import changes

- `Untitled0.ipynb` was renamed to `business-news-labeling.ipynb`.
- `Untitled1.ipynb` was renamed to `labeled-data-exploration.ipynb`.
- `KafkaStreams.iml` was removed as IDE metadata.
- README files and this provenance note were added.

## Source repository status

The four source repositories were archived after the merged branch was verified.
They are not deleted, so the original repository history remains independently
recoverable.

## 2026 AI-assisted restoration

This provenance file covers the imported Git repositories. The separate 2026
restoration and enhancement work is documented in
[`docs/AI_ASSISTANCE.md`](AI_ASSISTANCE.md).
