# Timmy Time — Status

## Current Version: 1.0.0 (Genesis)

### What's Built
- `src/timmy/` — Agno-powered Timmy agent (llama3.2 via Ollama, SQLite memory)
- `src/dashboard/` — FastAPI Mission Control dashboard (HTMX + Jinja2)
- CLI: `timmy think / chat / status`
- Pytest test suite (prompts, agent config, dashboard routes)

### System Requirements
- Python 3.11+
- Ollama running at `http://localhost:11434`
- `llama3.2` model pulled

### Quickstart
```bash
pip install -e ".[dev]"

# Start Ollama (separate terminal)
ollama serve
ollama pull llama3.2

# Run dashboard
uvicorn dashboard.app:app --reload

# Run tests (no Ollama required)
pytest
```

### Dashboard
`http://localhost:8000` — Mission Control UI with:
- Timmy agent status panel
- Ollama health indicator (auto-refreshes every 30s)
- Live chat interface

---

## Roadmap

| Tag   | Name       | Milestone                                    |
|-------|------------|----------------------------------------------|
| 1.0.0 | Genesis    | Agno + Ollama + SQLite + Dashboard           |
| 2.0.0 | Exodus     | MCP tools + multi-agent support              |
| 3.0.0 | Revelation | Bitcoin Lightning treasury + single `.app`   |

_Last updated: 2026-02-19_
