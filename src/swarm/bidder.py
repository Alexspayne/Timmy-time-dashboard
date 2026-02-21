"""15-second auction system for swarm task assignment.

When a task is posted, agents have 15 seconds to submit bids (in sats).
The lowest bid wins.  If no bids arrive, the task remains unassigned.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

AUCTION_DURATION_SECONDS = 15


@dataclass
class Bid:
    agent_id: str
    bid_sats: int
    task_id: str


@dataclass
class Auction:
    task_id: str
    bids: list[Bid] = field(default_factory=list)
    closed: bool = False
    winner: Optional[Bid] = None

    def submit(self, agent_id: str, bid_sats: int) -> bool:
        """Submit a bid.  Returns False if the auction is already closed."""
        if self.closed:
            return False
        self.bids.append(Bid(agent_id=agent_id, bid_sats=bid_sats, task_id=self.task_id))
        return True

    def close(self) -> Optional[Bid]:
        """Close the auction and determine the winner (lowest bid)."""
        self.closed = True
        if not self.bids:
            logger.info("Auction %s: no bids received", self.task_id)
            return None
        self.winner = min(self.bids, key=lambda b: b.bid_sats)
        logger.info(
            "Auction %s: winner is %s at %d sats",
            self.task_id, self.winner.agent_id, self.winner.bid_sats,
        )
        return self.winner


class AuctionManager:
    """Manages concurrent auctions for multiple tasks."""

    def __init__(self) -> None:
        self._auctions: dict[str, Auction] = {}

    def open_auction(self, task_id: str) -> Auction:
        auction = Auction(task_id=task_id)
        self._auctions[task_id] = auction
        logger.info("Auction opened for task %s", task_id)
        return auction

    def get_auction(self, task_id: str) -> Optional[Auction]:
        return self._auctions.get(task_id)

    def submit_bid(self, task_id: str, agent_id: str, bid_sats: int) -> bool:
        auction = self._auctions.get(task_id)
        if auction is None:
            logger.warning("No auction found for task %s", task_id)
            return False
        return auction.submit(agent_id, bid_sats)

    def close_auction(self, task_id: str) -> Optional[Bid]:
        auction = self._auctions.get(task_id)
        if auction is None:
            return None
        return auction.close()

    async def run_auction(self, task_id: str) -> Optional[Bid]:
        """Open an auction, wait the bidding period, then close and return winner."""
        self.open_auction(task_id)
        await asyncio.sleep(AUCTION_DURATION_SECONDS)
        return self.close_auction(task_id)

    @property
    def active_auctions(self) -> list[str]:
        return [tid for tid, a in self._auctions.items() if not a.closed]
