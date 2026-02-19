"""TDD: Luna ticket model tests — written before implementation."""

from luna.models import Ticket, TicketPriority, TicketStatus


def test_ticket_has_unique_id():
    t1 = Ticket()
    t2 = Ticket()
    assert t1.id != t2.id


def test_ticket_id_is_short():
    t = Ticket()
    assert len(t.id) == 8


def test_ticket_default_status_is_recording():
    t = Ticket()
    assert t.status == TicketStatus.RECORDING


def test_ticket_default_priority_is_medium():
    t = Ticket()
    assert t.priority == TicketPriority.MEDIUM


def test_ticket_default_project_is_luna():
    t = Ticket()
    assert t.project == "luna"


def test_ticket_title_starts_empty():
    t = Ticket()
    assert t.title == ""


def test_ticket_description_starts_empty():
    t = Ticket()
    assert t.description == ""


def test_ticket_transcript_starts_empty():
    t = Ticket()
    assert t.transcript == ""


def test_ticket_status_values_are_strings():
    assert TicketStatus.RECORDING == "recording"
    assert TicketStatus.TRANSCRIBING == "transcribing"
    assert TicketStatus.STRUCTURING == "structuring"
    assert TicketStatus.READY == "ready"
    assert TicketStatus.ERROR == "error"


def test_ticket_priority_values_are_strings():
    assert TicketPriority.HIGH == "high"
    assert TicketPriority.MEDIUM == "medium"
    assert TicketPriority.LOW == "low"


def test_ticket_has_created_at():
    from datetime import datetime
    t = Ticket()
    assert isinstance(t.created_at, datetime)


def test_ticket_is_terminal_when_ready():
    t = Ticket()
    t.status = TicketStatus.READY
    assert t.status.is_terminal


def test_ticket_is_terminal_when_error():
    t = Ticket()
    t.status = TicketStatus.ERROR
    assert t.status.is_terminal


def test_ticket_is_not_terminal_when_processing():
    assert not TicketStatus.RECORDING.is_terminal
    assert not TicketStatus.TRANSCRIBING.is_terminal
    assert not TicketStatus.STRUCTURING.is_terminal
