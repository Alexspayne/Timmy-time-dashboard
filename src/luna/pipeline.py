"""Luna project — audio-to-ticket processing pipeline."""

import json
import logging
import re

from luna.models import Ticket, TicketPriority, TicketStatus
from luna.store import update_ticket
from luna.transcriber import Transcriber
from timmy.agent import create_timmy

logger = logging.getLogger(__name__)


async def process_audio(ticket: Ticket, audio_bytes: bytes, transcriber: Transcriber) -> None:
    """Background task: transcribe audio, then structure into a Luna ticket."""
    try:
        # ── Stage 1: Transcribe ────────────────────────────────────────────────
        ticket.status = TicketStatus.TRANSCRIBING
        update_ticket(ticket)
        logger.info("luna: transcribing ticket %s", ticket.id)

        transcript = await transcriber.transcribe(audio_bytes)
        ticket.transcript = transcript
        logger.info("luna: transcript ready for ticket %s — %r", ticket.id, transcript[:60])

        # ── Stage 2: Structure via LLM ─────────────────────────────────────────
        ticket.status = TicketStatus.STRUCTURING
        update_ticket(ticket)
        logger.info("luna: structuring ticket %s with LLM", ticket.id)

        structured = _structure_with_llm(transcript)
        ticket.title = structured.get("title", transcript[:60].strip())
        ticket.description = structured.get("description", transcript)
        priority_raw = structured.get("priority", "medium")
        try:
            ticket.priority = TicketPriority(priority_raw)
        except ValueError:
            ticket.priority = TicketPriority.MEDIUM

        # ── Done ───────────────────────────────────────────────────────────────
        ticket.status = TicketStatus.READY
        update_ticket(ticket)
        logger.info("luna: ticket %s ready — %r", ticket.id, ticket.title)

    except Exception as exc:
        logger.exception("luna: pipeline error for ticket %s", ticket.id)
        ticket.status = TicketStatus.ERROR
        ticket.error = str(exc)
        update_ticket(ticket)


def _structure_with_llm(transcript: str) -> dict:
    """Ask Timmy to convert a raw transcript into structured ticket fields."""
    prompt = (
        f'You are a project manager. Convert this voice note into a ticket.\n'
        f'Voice note: "{transcript}"\n\n'
        f'Respond with ONLY valid JSON, no markdown, no explanation:\n'
        f'{{"title": "short title", "description": "full description", "priority": "high|medium|low"}}'
    )

    try:
        agent = create_timmy()
        run = agent.run(prompt, stream=False)
        content = run.content if hasattr(run, "content") else str(run)
        match = re.search(r'\{[^{}]*"title"[^{}]*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as exc:
        logger.warning("luna: LLM structuring failed (%s), using transcript fallback", exc)

    # Graceful fallback — use raw transcript
    return {
        "title": transcript[:60].strip(),
        "description": transcript,
        "priority": "medium",
    }
