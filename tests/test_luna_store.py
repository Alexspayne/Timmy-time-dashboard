"""TDD: Luna ticket store tests — written before implementation."""

import pytest

from luna.models import TicketStatus
from luna.store import clear_tickets, create_ticket, get_ticket, list_tickets, update_ticket


@pytest.fixture(autouse=True)
def clean_store():
    clear_tickets()
    yield
    clear_tickets()


def test_create_ticket_returns_ticket():
    ticket = create_ticket()
    assert ticket.id is not None


def test_create_ticket_is_stored():
    ticket = create_ticket()
    found = get_ticket(ticket.id)
    assert found is not None


def test_get_ticket_returns_correct_ticket():
    ticket = create_ticket()
    found = get_ticket(ticket.id)
    assert found.id == ticket.id


def test_get_missing_ticket_returns_none():
    assert get_ticket("nonexistent") is None


def test_list_tickets_returns_all():
    create_ticket()
    create_ticket()
    create_ticket()
    assert len(list_tickets()) == 3


def test_list_tickets_empty_by_default():
    assert list_tickets() == []


def test_update_ticket_persists_status_change():
    ticket = create_ticket()
    ticket.status = TicketStatus.READY
    update_ticket(ticket)
    found = get_ticket(ticket.id)
    assert found.status == TicketStatus.READY


def test_update_ticket_persists_title():
    ticket = create_ticket()
    ticket.title = "Fix the login bug"
    update_ticket(ticket)
    found = get_ticket(ticket.id)
    assert found.title == "Fix the login bug"


def test_list_tickets_newest_first():
    import time
    t1 = create_ticket()
    time.sleep(0.01)
    t2 = create_ticket()
    tickets = list_tickets()
    assert tickets[0].id == t2.id
    assert tickets[1].id == t1.id


def test_clear_tickets_empties_store():
    create_ticket()
    create_ticket()
    clear_tickets()
    assert list_tickets() == []
