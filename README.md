# Coinwise

A full-stack credit-card spending and rewards dashboard built for the Digital Alpha take-home. It uses a React + TypeScript frontend, a FastAPI backend, and PostgreSQL.

## Run locally

1. Start Postgres: `docker compose up -d db`
2. In `backend`: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. Set `DATABASE_URL=postgresql+psycopg://coinwise:coinwise@localhost:5432/coinwise`
4. Seed: `python -m app.seed ../data/transactions.json` (or omit the path for 10,000 deterministic demo records)
5. Start API: `uvicorn app.main:app --reload --port 8000`
6. In `frontend`: `npm install && npm run dev`

Open `http://localhost:5173`. The frontend proxies `/api` to the API server.

## What is complete

- Server-side search, combinable filters, sorting, pagination and transaction detail.
- Category and monthly spend analytics; clicking a category filters the table.
- Current coin balance, reward catalogue and validated, transactional redemption.
- PostgreSQL schema, indexes and one-command seed support.
- Responsive hand-built table with sticky header, loading, empty and error states.

## Notes

The provided `transactions.json` was not available in the local workspace. The seeder accepts the original file unchanged when it is supplied, and otherwise creates a reproducible 10,000-row development fixture. See `ASSUMPTIONS.md`.

## API

- `GET /api/transactions?search=&category=&status=&date_from=&date_to=&min_amount=&max_amount=&sort_by=date&sort_dir=desc&page=1&page_size=50`
- `GET /api/transactions/{id}`
- `GET /api/analytics/spending`
- `GET /api/rewards/balance`
- `GET /api/rewards/catalog`
- `POST /api/rewards/redeem` with `{ "reward_id": 1 }`
