# MariaDB → LLM RAG Gateway (FastAPI)

A lightweight middleware service that converts natural-language questions into safe SELECT SQL queries against a MariaDB instance, formats results into natural-language context suitable for LLM prompts, and returns both the SQL and generated context.

This project focuses on:
- Read-only SELECT queries
- Allow-list based NL→SQL heuristics (no free-form SQL from users)
- Safe, parameterized queries
- Async FastAPI + connection pooling
- Schema introspection endpoint (protected)
- Config via `config.yaml` and env vars
- Basic API key auth

## Quickstart

1. Create a virtualenv and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Copy config.yaml and .env.example into .env or set the environment variables listed.

Start the server:

uvicorn app.main:app --reload


Open docs: http://127.0.0.1:8000/docs.

##Project structure
.
├── README.md
├── requirements.txt
├── config.yaml
├── .env.example
├── app
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── nl2sql.py
│   ├── formatter.py
│   ├── schemas.py
│   ├── security.py
│   └── utils.py
└── tests
    └── test_endpoints.py

Notes & Best Practices

Use a read-only DB user for the gateway.

Keep secrets in a secret manager; avoid committing config.yaml with credentials.

Place the app behind HTTPS and an API gateway in production.

Extend NL→SQL module with a tuned model (SQLCoder) when budget allows; keep allow-lists enforced.
