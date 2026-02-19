from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from timmy.agent import create_timmy

router = APIRouter(prefix="/agents", tags=["agents"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

AGENT_REGISTRY = {
    "timmy": {
        "id": "timmy",
        "name": "Timmy",
        "type": "sovereign",
        "model": "llama3.2",
        "backend": "ollama",
        "version": "1.0.0",
    }
}


@router.get("")
async def list_agents():
    return {"agents": list(AGENT_REGISTRY.values())}


@router.post("/timmy/chat", response_class=HTMLResponse)
async def chat_timmy(request: Request, message: str = Form(...)):
    timestamp = datetime.now().strftime("%H:%M:%S")
    response_text = None
    error_text = None

    try:
        agent = create_timmy()
        run = agent.run(message, stream=False)
        response_text = run.content if hasattr(run, "content") else str(run)
    except Exception as exc:
        error_text = f"Timmy is offline: {exc}"

    return templates.TemplateResponse(
        request,
        "partials/chat_message.html",
        {
            "user_message": message,
            "response": response_text,
            "error": error_text,
            "timestamp": timestamp,
        },
    )
