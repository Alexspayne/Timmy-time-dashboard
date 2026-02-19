"""Luna project — audio recording → ticket pipeline routes."""

import logging
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from luna.pipeline import process_audio
from luna.store import create_ticket, get_ticket, list_tickets
from luna.transcriber import WhisperTranscriber

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/luna", tags=["luna"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

# Shared transcriber instance — swappable for tests via dependency override
_transcriber = WhisperTranscriber()


@router.post("/record", response_class=HTMLResponse)
async def record_audio(
    request: Request,
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
):
    """Accept a recorded audio blob, create a ticket, kick off the pipeline."""
    ticket = create_ticket()
    audio_bytes = await audio.read()
    background_tasks.add_task(process_audio, ticket, audio_bytes, _transcriber)
    logger.info("luna: received audio for ticket %s (%d bytes)", ticket.id, len(audio_bytes))
    return templates.TemplateResponse(
        request,
        "partials/ticket_card.html",
        {"ticket": ticket},
    )


@router.get("/tickets", response_class=HTMLResponse)
async def tickets_panel(request: Request):
    """Return the full Luna tickets panel (HTMX target for initial load)."""
    tickets = list_tickets()
    return templates.TemplateResponse(
        request,
        "partials/luna_tickets.html",
        {"tickets": tickets},
    )


@router.get("/tickets/{ticket_id}/status", response_class=HTMLResponse)
async def ticket_status(request: Request, ticket_id: str):
    """Return a single ticket card fragment. Used by HTMX polling."""
    ticket = get_ticket(ticket_id)
    if not ticket:
        return HTMLResponse(content="<div>not found</div>", status_code=404)
    return templates.TemplateResponse(
        request,
        "partials/ticket_card.html",
        {"ticket": ticket},
    )
