# AGENTS.md

This file guides automated agents working in this repository.

## Project
Items API — a minimal REST API that manages a list of named items in memory.
Built with Python 3.12+ and FastAPI. No database, no auth, no frontend.

## Stack & Conventions
- Language: Python 3.12+
- Framework: FastAPI with Pydantic v2 models
- Server: uvicorn (run `uvicorn app.main:app --reload`)
- Storage: In-memory `list[Item]` — data does NOT persist between restarts (by design)
- Tests: pytest + httpx — run `pytest` to verify
- Linting: ruff — run `ruff check .` before committing
- No external database or auth

## Project Layout
```
app/
  __init__.py
  main.py      ← FastAPI app instance, routes, in-memory store
  models.py    ← Pydantic models: ItemCreate, Item
tests/
  test_api.py
requirements.txt
Dockerfile
```

## Data Model
- Item: id (int, auto-incremented from 1), name (str, required)
- ItemCreate: name (str, required) — request body for POST /items

## API Surface
- GET  /items       → 200 JSON array of all items `[{id, name}]`; empty array when no items exist
- POST /items       → 201 JSON of created item `{id, name}`; body: `{"name": "<string>"}`

## Rules
1. Read this file before writing any code.
2. Follow existing patterns — check app/main.py before adding new routes.
3. All IDs must auto-increment starting at 1; counter resets on restart.
4. Return [] (not 404) when no items exist on GET /items.
5. Return HTTP 201 (not 200) on successful POST /items.
6. Run `pytest` and confirm all tests pass before finishing any task.
7. Run `ruff check .` and fix all lint errors before finishing any task.

## Repository: smalls257/items-api

