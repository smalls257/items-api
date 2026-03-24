# AGENTS.md

This file guides automated agents working in this repository.

## Stack & Conventions
- Language: Python 3.12+
- Framework: FastAPI
- Pattern: Single-module app — all logic in main.py; expand to routers/services only if scope grows
- Storage: In-memory Python list — no database, resets on restart
- Tests: pytest — run pytest to verify; all tests live in tests/
- Style: ruff enforced — run ruff check . before committing
- Container: Single Dockerfile, no external services required

## API Surface
- GET /items — returns [{id, name}, ...]
- POST /items — accepts {name}, returns {id, name} with HTTP 201
- Item IDs: auto-increment integers starting at 1

## Rules
1. Read this file before writing any code.
2. Follow existing patterns — keep the implementation minimal and dependency-free.
3. Never add a database or external service dependency.
4. The build must pass (pytest) before finishing any task.
5. All endpoints must match the exact response shape specified above.

## Repository: smalls257/items-api
