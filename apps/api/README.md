# October API (FastAPI + MongoDB)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

## Deterministic checks

```bash
ruff check app tests
pyright app
pytest -q
```
