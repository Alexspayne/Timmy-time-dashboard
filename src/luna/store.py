"""Luna project — in-memory ticket store."""

from typing import Optional

from luna.models import Ticket

_tickets: dict[str, Ticket] = {}


def create_ticket() -> Ticket:
    ticket = Ticket()
    _tickets[ticket.id] = ticket
    return ticket


def get_ticket(ticket_id: str) -> Optional[Ticket]:
    return _tickets.get(ticket_id)


def list_tickets() -> list[Ticket]:
    return sorted(_tickets.values(), key=lambda t: t.created_at, reverse=True)


def update_ticket(ticket: Ticket) -> None:
    _tickets[ticket.id] = ticket


def clear_tickets() -> None:
    _tickets.clear()
