"""Luna project — ticket data models."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class TicketStatus(str, Enum):
    RECORDING = "recording"
    TRANSCRIBING = "transcribing"
    STRUCTURING = "structuring"
    READY = "ready"
    ERROR = "error"

    @property
    def is_terminal(self) -> bool:
        return self in (TicketStatus.READY, TicketStatus.ERROR)


class TicketPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Ticket:
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    title: str = ""
    description: str = ""
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.RECORDING
    transcript: str = ""
    error: str = ""
    project: str = "luna"
    created_at: datetime = field(default_factory=datetime.now)
