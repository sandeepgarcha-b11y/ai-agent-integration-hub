# CX Agent Integration Hub

A small, readable model of the plumbing behind an AI customer service agent for an ecommerce brand.
It is built step by step as a learning project about **webhooks, authentication and failure handling**.

When finished, the hub will:
- receive order events from a fake Shopify-like store via **webhooks**
- keep an up-to-date view of each customer's orders in **SQLite**
- call a fake **carrier API** using proper authentication (API key, then OAuth 2.0)
- let a simple **agent** answer "where is my order?"
- handle what goes wrong: forged events, duplicates, out-of-order events, outages, expired tokens, rate limits

## Progress

| Step | Topic | Status |
|------|-------|--------|
| 1 | Setup: FastAPI app, SQLite, health checks | ✅ |
| 2 | Webhooks basics | ⏳ |
| 3 | Verifying webhooks (HMAC, replay attacks) | ⏳ |
| 4 | Duplicates and ordering (idempotency) | ⏳ |
| 5 | Async processing, retries, dead-letter table | ⏳ |
| 6 | Calling external APIs with an API key | ⏳ |
| 7 | OAuth 2.0 (authorization code, refresh, scopes) | ⏳ |
| 8 | Outbound resilience (timeouts, retries, 429s) | ⏳ |
| 9 | The "where is my order?" agent | ⏳ |
| 10 | Observability and reconciliation | ⏳ |
| 11 | Wrap-up and mock interview | ⏳ |

## Project layout

```
app/
  main.py   # the web server and its endpoints
  db.py     # SQLite connection and table definitions
TALK_TRACK.md  # interview cheat sheet: how to explain each step to engineers
```

## Run it

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload --port 8000
```

The database file `hub.db` is created on startup. Set `HUB_DB_PATH` to use a different file.

## Endpoints so far

| Method | Path | What it does |
|--------|------|--------------|
| GET | `/ping` | **Liveness.** 200 if the process is up. Checks nothing else; used to decide "restart me?" |
| GET | `/health` | **Readiness.** 200 if we can reach the database, 503 if not; used to decide "send me traffic?" |
| GET | `/orders/{order_id}` | Look up one order. 404 if we don't know it. |

```bash
curl -i localhost:8000/health            # 200 {"status":"ok"}
curl -i localhost:8000/orders/1001       # 404 {"detail":"order not found"}
```

Interactive API docs are at http://localhost:8000/docs while the server is running.
