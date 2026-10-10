# Async Content and Lead-Triage API

FastAPI service for CMS content sync/cache and lead intake with async task processing.

## Features
- Strapi-style content payload sync into MongoDB and Redis cache
- API-key protected routes
- TTL-based cache-aside reads
- Lead triage with a transparent keyword baseline and Celery task
- Docker Compose for API, MongoDB, Redis, and worker
- Pytest coverage for classifier and request validation

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Set `MONGODB_URL`, `REDIS_URL`, and `API_KEY` for your environment. The default key is development-only. Swagger is at `/docs`.

## Docker Compose
```bash
docker compose up --build
```

## Tests
```bash
pytest -q
```

## Notes
The classifier is an explainable baseline, not a trained scikit-learn model. Replace it with a validated/persisted model pipeline and add dataset evaluation before claiming production accuracy. Storage-backed routes require MongoDB and Redis to be running.

## API contract
All `/api/*` routes require `X-API-Key`; use the configured development key only locally.
