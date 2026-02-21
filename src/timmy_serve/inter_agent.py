"""Agent-to-agent messaging for the Timmy serve layer.

Provides a simple message-passing interface that allows agents to
communicate with each other.  Messages are routed through the swarm
comms layer when available, or stored in an in-memory queue for
single-process operation.
"""

import logging
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class AgentMessage:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str = ""
    to_agent: str = ""
    content: str = ""
    message_type: str = "text"  # text | command | response | error
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    replied: bool = False


class InterAgentMessenger:
    """In-memory message queue for agent-to-agent communication."""

    def __init__(self, max_queue_size: int = 1000) -> None:
        self._queues: dict[str, deque[AgentMessage]] = {}
        self._max_size = max_queue_size
        self._all_messages: list[AgentMessage] = []

    def send(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: str = "text",
    ) -> AgentMessage:
        """Send a message from one agent to another."""
        msg = AgentMessage(
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            message_type=message_type,
        )
        queue = self._queues.setdefault(to_agent, deque(maxlen=self._max_size))
        queue.append(msg)
        self._all_messages.append(msg)
        logger.info(
            "Message %s → %s: %s (%s)",
            from_agent, to_agent, content[:50], message_type,
        )
        return msg

    def receive(self, agent_id: str, limit: int = 10) -> list[AgentMessage]:
        """Receive pending messages for an agent (FIFO, non-destructive peek)."""
        queue = self._queues.get(agent_id, deque())
        return list(queue)[:limit]

    def pop(self, agent_id: str) -> Optional[AgentMessage]:
        """Pop the oldest message from an agent's queue."""
        queue = self._queues.get(agent_id, deque())
        if not queue:
            return None
        return queue.popleft()

    def pop_all(self, agent_id: str) -> list[AgentMessage]:
        """Pop all pending messages for an agent."""
        queue = self._queues.get(agent_id, deque())
        messages = list(queue)
        queue.clear()
        return messages

    def broadcast(self, from_agent: str, content: str, message_type: str = "text") -> int:
        """Broadcast a message to all known agents.  Returns count sent."""
        count = 0
        for agent_id in list(self._queues.keys()):
            if agent_id != from_agent:
                self.send(from_agent, agent_id, content, message_type)
                count += 1
        return count

    def history(self, limit: int = 50) -> list[AgentMessage]:
        """Return recent message history across all agents."""
        return self._all_messages[-limit:]

    def clear(self, agent_id: Optional[str] = None) -> None:
        """Clear message queue(s)."""
        if agent_id:
            self._queues.pop(agent_id, None)
        else:
            self._queues.clear()
            self._all_messages.clear()


# Module-level singleton
messenger = InterAgentMessenger()
