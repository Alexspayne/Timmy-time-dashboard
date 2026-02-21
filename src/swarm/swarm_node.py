"""SwarmNode — a single agent's view of the swarm.

A SwarmNode registers itself in the SQLite registry, listens for tasks
via the comms layer, and submits bids through the auction system.
Used by agent_runner.py when a sub-agent process is spawned.
"""

import logging
import random
from typing import Optional

from swarm import registry
from swarm.comms import CHANNEL_TASKS, SwarmComms, SwarmMessage

logger = logging.getLogger(__name__)


class SwarmNode:
    """Represents a single agent participating in the swarm."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        capabilities: str = "",
        comms: Optional[SwarmComms] = None,
    ) -> None:
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self._comms = comms or SwarmComms()
        self._joined = False

    async def join(self) -> None:
        """Register with the swarm and start listening for tasks."""
        registry.register(
            name=self.name,
            capabilities=self.capabilities,
            agent_id=self.agent_id,
        )
        self._comms.subscribe(CHANNEL_TASKS, self._on_task_posted)
        self._joined = True
        logger.info("SwarmNode %s (%s) joined the swarm", self.name, self.agent_id)

    async def leave(self) -> None:
        """Unregister from the swarm."""
        registry.update_status(self.agent_id, "offline")
        self._joined = False
        logger.info("SwarmNode %s (%s) left the swarm", self.name, self.agent_id)

    def _on_task_posted(self, msg: SwarmMessage) -> None:
        """Handle an incoming task announcement by submitting a bid."""
        task_id = msg.data.get("task_id")
        if not task_id:
            return
        # Simple bidding strategy: random bid between 10 and 100 sats
        bid_sats = random.randint(10, 100)
        self._comms.submit_bid(
            task_id=task_id,
            agent_id=self.agent_id,
            bid_sats=bid_sats,
        )
        logger.info(
            "SwarmNode %s bid %d sats on task %s",
            self.name, bid_sats, task_id,
        )

    @property
    def is_joined(self) -> bool:
        return self._joined
