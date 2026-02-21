"""Mobile-optimized dashboard route — /mobile endpoint.

Provides a simplified, mobile-first view of the dashboard that
prioritizes the chat interface and essential status information.
Designed for quick access from a phone's home screen.
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["mobile"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("/mobile", response_class=HTMLResponse)
async def mobile_dashboard(request: Request):
    """Render the mobile-optimized dashboard.

    Falls back to the main index template which is already responsive.
    A dedicated mobile template can be added later for a more
    streamlined experience.
    """
    return templates.TemplateResponse(request, "index.html")


@router.get("/mobile/status")
async def mobile_status():
    """Lightweight status endpoint optimized for mobile polling."""
    from dashboard.routes.health import check_ollama
    from config import settings

    ollama_ok = await check_ollama()
    return {
        "ollama": "up" if ollama_ok else "down",
        "model": settings.ollama_model,
        "agent": "timmy",
        "ready": True,
    }
