from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dashboard.routes.agents import router as agents_router
from dashboard.routes.health import router as health_router

BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent.parent

app = FastAPI(title="Timmy Time — Mission Control", version="1.0.0")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(PROJECT_ROOT / "static")), name="static")

app.include_router(health_router)
app.include_router(agents_router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")
