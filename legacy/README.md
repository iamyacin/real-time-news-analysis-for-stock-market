# Legacy stack notes

This directory documents the original 2020 Python stack. It is optional and
not used by the default demo.

```bash
python3.10 -m venv .venv-legacy
source .venv-legacy/bin/activate
pip install -r legacy/requirements-py310.txt
```

The original scripts are still available from git history. Find the commit
before the 2026 restoration:

```bash
git log --oneline -- HistoricalNewsCollector.py
git show <original-commit>:HistoricalNewsCollector.py
git show <original-commit>:RealTimeScripts/StreamingTwitterAPI.py
```

Training and installing the original ktrain BERT model is documented in
[`docs/TRAIN_POLARITY_MODEL.md`](../docs/TRAIN_POLARITY_MODEL.md).

The modern restoration is recommended for the public demo:

```bash
cp .env.example .env
docker compose up --build
```

See [`docs/LEGACY_STACK.md`](../docs/LEGACY_STACK.md) for the full comparison.
