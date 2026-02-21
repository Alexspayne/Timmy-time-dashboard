import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings
from dashboard.routes.agents import router as agents_router
from dashboard.routes.health import router as health_router
from dashboard.routes.mobile_test import router as mobile_test_router
from dashboard.routes.swarm import router as swarm_router
from dashboard.routes.marketplace import router as marketplace_router
from dashboard.routes.voice import router as voice_router
from dashboard.routes.voice_enhanced import router as voice_enhanced_router
from dashboard.routes.mobile import router as mobile_router
from dashboard.routes.swarm_ws import router as swarm_ws_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent.parent

app = FastAPI(
    title="Timmy Time — Mission Control",
    version="1.0.0",
    # Docs disabled unless DEBUG=true in env / .env
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="static")

app.include_router(health_router)
app.include_router(agents_router)
app.include_router(mobile_test_router)
app.include_router(swarm_router)
app.include_router(marketplace_router)
app.include_router(voice_router)
app.include_router(voice_enhanced_router)
app.include_router(mobile_router)
app.include_router(swarm_ws_router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/shortcuts/setup")
async def shortcuts_setup():
    """Siri Shortcuts setup guide."""
    from shortcuts.siri import get_setup_guide
    return get_setup_guide()
