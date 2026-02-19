"""TDD: Luna route tests — written before implementation."""

from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest

from luna.store import clear_tickets, create_ticket


@pytest.fixture(autouse=True)
def clean_store():
    clear_tickets()
    yield
    clear_tickets()


def test_record_returns_200(client):
    with patch("dashboard.routes.luna.process_audio", new_callable=AsyncMock):
        response = client.post(
            "/luna/record",
            files={"audio": ("rec.webm", BytesIO(b"fake"), "audio/webm")},
        )
    assert response.status_code == 200


def test_record_response_contains_ticket_id(client):
    with patch("dashboard.routes.luna.process_audio", new_callable=AsyncMock):
        response = client.post(
            "/luna/record",
            files={"audio": ("rec.webm", BytesIO(b"fake"), "audio/webm")},
        )
    assert "ticket-" in response.text


def test_record_shows_recording_status(client):
    with patch("dashboard.routes.luna.process_audio", new_callable=AsyncMock):
        response = client.post(
            "/luna/record",
            files={"audio": ("rec.webm", BytesIO(b"fake"), "audio/webm")},
        )
    assert "recording" in response.text.lower()


def test_list_tickets_returns_200(client):
    response = client.get("/luna/tickets")
    assert response.status_code == 200


def test_list_tickets_empty_state(client):
    response = client.get("/luna/tickets")
    assert response.status_code == 200
    assert "no tickets" in response.text.lower()


def test_ticket_status_not_found(client):
    response = client.get("/luna/tickets/nonexistent/status")
    assert response.status_code == 404


def test_ticket_status_returns_card(client):
    ticket = create_ticket()
    response = client.get(f"/luna/tickets/{ticket.id}/status")
    assert response.status_code == 200
    assert ticket.id in response.text


def test_ticket_status_ready_has_no_polling(client):
    from luna.models import TicketStatus
    from luna.store import update_ticket

    ticket = create_ticket()
    ticket.status = TicketStatus.READY
    ticket.title = "Bug fixed"
    update_ticket(ticket)

    response = client.get(f"/luna/tickets/{ticket.id}/status")
    # A ready ticket should NOT have hx-trigger polling
    assert "every 2s" not in response.text


def test_ticket_status_processing_has_polling(client):
    from luna.models import TicketStatus
    from luna.store import update_ticket

    ticket = create_ticket()
    ticket.status = TicketStatus.TRANSCRIBING
    update_ticket(ticket)

    response = client.get(f"/luna/tickets/{ticket.id}/status")
    assert "every 2s" in response.text
