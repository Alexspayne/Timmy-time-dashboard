"""TDD: Luna audio pipeline tests — written before implementation."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from luna.models import TicketStatus
from luna.store import clear_tickets, create_ticket, get_ticket


@pytest.fixture(autouse=True)
def clean_store():
    clear_tickets()
    yield
    clear_tickets()


@pytest.fixture
def mock_transcriber():
    t = AsyncMock()
    t.transcribe = AsyncMock(return_value="Fix the login bug on the settings page")
    return t


@pytest.fixture
def mock_timmy():
    agent = MagicMock()
    run = MagicMock()
    run.content = '{"title": "Fix login bug", "description": "Login broken on settings page", "priority": "high"}'
    agent.run.return_value = run
    return agent


async def test_pipeline_moves_ticket_to_ready(mock_transcriber, mock_timmy):
    from luna.pipeline import process_audio

    ticket = create_ticket()
    with patch("luna.pipeline.create_timmy", return_value=mock_timmy):
        await process_audio(ticket, b"fake audio", mock_transcriber)

    result = get_ticket(ticket.id)
    assert result.status == TicketStatus.READY


async def test_pipeline_stores_transcript(mock_transcriber, mock_timmy):
    from luna.pipeline import process_audio

    ticket = create_ticket()
    with patch("luna.pipeline.create_timmy", return_value=mock_timmy):
        await process_audio(ticket, b"fake audio", mock_transcriber)

    result = get_ticket(ticket.id)
    assert result.transcript == "Fix the login bug on the settings page"


async def test_pipeline_structures_title(mock_transcriber, mock_timmy):
    from luna.pipeline import process_audio

    ticket = create_ticket()
    with patch("luna.pipeline.create_timmy", return_value=mock_timmy):
        await process_audio(ticket, b"fake audio", mock_transcriber)

    result = get_ticket(ticket.id)
    assert result.title == "Fix login bug"


async def test_pipeline_structures_priority(mock_transcriber, mock_timmy):
    from luna.pipeline import process_audio

    ticket = create_ticket()
    with patch("luna.pipeline.create_timmy", return_value=mock_timmy):
        await process_audio(ticket, b"fake audio", mock_transcriber)

    result = get_ticket(ticket.id)
    assert result.priority.value == "high"


async def test_pipeline_sets_error_on_transcription_failure():
    from luna.pipeline import process_audio

    failing_transcriber = AsyncMock()
    failing_transcriber.transcribe = AsyncMock(side_effect=RuntimeError("whisper not available"))

    ticket = create_ticket()
    await process_audio(ticket, b"fake audio", failing_transcriber)

    result = get_ticket(ticket.id)
    assert result.status == TicketStatus.ERROR
    assert "whisper not available" in result.error


async def test_pipeline_falls_back_when_llm_fails(mock_transcriber):
    from luna.pipeline import process_audio

    ticket = create_ticket()
    with patch("luna.pipeline.create_timmy", side_effect=Exception("ollama offline")):
        await process_audio(ticket, b"fake audio", mock_transcriber)

    # Should still be READY using the transcript as fallback title
    result = get_ticket(ticket.id)
    assert result.status == TicketStatus.READY
    assert result.title != ""
