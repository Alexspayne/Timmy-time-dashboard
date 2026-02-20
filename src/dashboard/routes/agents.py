from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from timmy.agent import create_timmy
from dashboard.store import message_log

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


@router.get("/timmy/history", response_class=HTMLResponse)
async def get_history(request: Request):
    return templates.TemplateResponse(
        request,
        "partials/history.html",
        {"messages": message_log.all()},
    )


@router.delete("/timmy/history", response_class=HTMLResponse)
async def clear_history(request: Request):
    message_log.clear()
    return templates.TemplateResponse(
        request,
        "partials/history.html",
        {"messages": []},
    )


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

    message_log.append(role="user", content=message, timestamp=timestamp)
    if response_text is not None:
        message_log.append(role="agent", content=response_text, timestamp=timestamp)
    else:
        message_log.append(role="error", content=error_text, timestamp=timestamp)

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
