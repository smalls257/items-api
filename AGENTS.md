# Items API — Agent Guide

## Project Overview
A minimal REST API for managing a list of named items. Built with Python / FastAPI, using in-memory storage only. No database, no auth.

## Stack
| Concern | Choice |
|---------|--------|
| Language | Python 3.11 |
| Framework | FastAPI |
| Validation | Pydantic v2 |
| In-memory store | `list[Item]` with auto-increment ID |
| ASGI server | uvicorn |
| Containerization | Docker (python:3.11-slim) |
| Auth | None |
| Database | None |

## Repository Layout
```
items-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + routes + in-memory store
│   └── models.py        # Pydantic v2: Item, ItemCreate
├── tests/
│   ├── __init__.py
│   └── test_items.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── AGENTS.md
```

## API Surface
| Method | Path | Body | Response | Status |
|--------|------|------|----------|--------|
| GET | /items | — | `[{id, name}…]` | 200 |
| POST | /items | `{name: str}` | `{id, name}` | 201 |

## Data Model
```python
class Item(BaseModel):
    id: int
    name: str

class ItemCreate(BaseModel):
    name: str  # min_length=1 enforced by Pydantic

# In-memory store
items: list[Item] = []
# ID generation: max(i.id for i in items) + 1, default 1 when empty
```

## Development Guidelines
- Keep all routes in `app/main.py` (project is intentionally minimal — no separate router file needed)
- Use Pydantic v2 for all request/response schemas
- In-memory store intentionally does NOT persist across restarts
- All tests go in `tests/test_items.py` using pytest + httpx (TestClient)
- Docker image must be runnable with `docker run -p 8000:8000 items-api`

## Running Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Running Tests
```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Building Docker Image
```bash
docker build -t items-api .
docker run -p 8000:8000 items-api
```

## MCP / Tool Usage
- All file edits via GitHub MCP tools
- Validate with pytest before opening PRs
- One GitHub issue per feature; reference issue number in commit/PR
