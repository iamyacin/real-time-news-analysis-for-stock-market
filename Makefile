PYTHON := .venv/bin/python
PIP := uv pip install --python $(PYTHON)

.PHONY: help setup train serve seed demo legacy-ui dashboard mongo-up down test smoke collect clean

help:
	@echo "Stock News Analyzer - common commands"
	@echo "  make setup       Create .venv and install Python dependencies"
	@echo "  make train       Train/restore local model artifacts"
	@echo "  make serve       Run the prediction service on :5000"
	@echo "  make seed        Load demo fixtures into MongoDB"
	@echo "  make dashboard   Run Streamlit on :8501"
	@echo "  make demo        Docker Compose: Mongo + service + seed + both UIs"
	@echo "  make legacy-ui   Docker Compose: Spring API + React report UI"
	@echo "  make mongo-up    Start only local MongoDB"
	@echo "  make collect     Live NewsAPI collection (requires NEWSAPI_KEY)"
	@echo "  make test        Run the Python tests"
	@echo "  make down        Stop the Docker Compose stack"

setup:
	uv venv --python 3.11 .venv
	$(PIP) -r requirements.txt

train:
	$(PYTHON) scripts/ensure_models.py

serve: train
	$(PYTHON) NewsPredictionMicroservice/app.py

seed:
	$(PYTHON) scripts/seed_demo.py

dashboard:
	$(PYTHON) -m streamlit run dashboard/app.py

demo:
	docker compose up --build

legacy-ui:
	docker compose up --build legacy-backend legacy-frontend

mongo-up:
	docker compose up -d mongo

down:
	docker compose down

collect:
	$(PYTHON) scripts/collect_news.py --limit 5

test:
	$(PYTHON) -m pytest -q

smoke:
	$(PYTHON) scripts/smoke_test.py

clean:
	rm -rf .pytest_cache
