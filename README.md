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
