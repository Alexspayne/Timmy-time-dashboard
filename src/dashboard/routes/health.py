import httpx
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from config import settings

router = APIRouter(tags=["health"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


async def check_ollama() -> bool:
    """Ping Ollama to verify it's running."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(settings.ollama_url)
            return r.status_code == 200
    except Exception:
        return False


@router.get("/health")
async def health():
    ollama_ok = await check_ollama()
    return {
        "status": "ok",
        "services": {
            "ollama": "up" if ollama_ok else "down",
        },
        "agents": ["timmy"],
    }


@router.get("/health/status", response_class=HTMLResponse)
async def health_status(request: Request):
    ollama_ok = await check_ollama()
    return templates.TemplateResponse(
        request,
        "partials/health_status.html",
        {"ollama": ollama_ok},
    )
