# Timmy Time — Mission Control

Sovereign AI agent dashboard. Monitor and interact with local and cloud AI agents.

## Stack

| Layer     | Tech                         |
|-----------|------------------------------|
| Agent     | Agno + Ollama (llama3.2)     |
| Memory    | SQLite via Agno SqliteDb     |
| Backend   | FastAPI                      |
| Frontend  | HTMX + Jinja2                |
| Tests     | Pytest                       |

## Quickstart

```bash
pip install -e ".[dev]"

# Ollama (separate terminal)
ollama serve && ollama pull llama3.2

# Dashboard
uvicorn dashboard.app:app --reload

# Tests (no Ollama needed)
pytest
```

## CLI

```bash
timmy chat "What is sovereignty?"
timmy think "Bitcoin and self-custody"
timmy status
```

## Project Structure

```
src/
  timmy/          # Agent identity — soul (prompt) + body (Agno)
  dashboard/      # Mission Control UI
    routes/       # FastAPI route handlers
    templates/    # Jinja2 HTML (HTMX-powered)
static/           # CSS
tests/            # Pytest suite
```

## Roadmap

| Version | Name       | Milestone                                  |
|---------|------------|--------------------------------------------|
| 1.0.0   | Genesis    | Agno + Ollama + SQLite + Dashboard         |
| 2.0.0   | Exodus     | MCP tools + multi-agent                    |
| 3.0.0   | Revelation | Bitcoin Lightning treasury + single `.app` |
