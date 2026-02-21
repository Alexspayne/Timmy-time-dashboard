"""Sub-agent runner — entry point for spawned swarm agents.

This module is executed as a subprocess by swarm.manager.  It creates a
SwarmNode, joins the registry, and waits for tasks.

Usage:
    python -m swarm.agent_runner --agent-id <id> --name <name>
"""

import argparse
import asyncio
import logging
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Swarm sub-agent runner")
    parser.add_argument("--agent-id", required=True, help="Unique agent identifier")
    parser.add_argument("--name", required=True, help="Human-readable agent name")
    args = parser.parse_args()

    # Lazy import to avoid circular deps at module level
    from swarm.swarm_node import SwarmNode

    node = SwarmNode(args.agent_id, args.name)
    await node.join()

    logger.info("Agent %s (%s) running — waiting for tasks", args.name, args.agent_id)

    # Run until terminated
    stop = asyncio.Event()

    def _handle_signal(*_):
        logger.info("Agent %s received shutdown signal", args.name)
        stop.set()

    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, _handle_signal)

    try:
        await stop.wait()
    finally:
        await node.leave()
        logger.info("Agent %s (%s) shut down", args.name, args.agent_id)


if __name__ == "__main__":
    asyncio.run(main())
