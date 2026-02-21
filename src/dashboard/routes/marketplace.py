"""Agent marketplace route — /marketplace endpoint.

The marketplace is where agents advertise their capabilities and
pricing.  Other agents (or the user) can browse available agents
and hire them for tasks via Lightning payments.
"""

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["marketplace"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

# ── Agent catalog ────────────────────────────────────────────────────────────
# These are the planned sub-agent personas from the roadmap.
# Each will eventually be a real Agno agent with its own prompt and skills.

AGENT_CATALOG = [
    {
        "id": "timmy",
        "name": "Timmy",
        "role": "Sovereign Commander",
        "description": "Primary AI companion. Coordinates the swarm, manages tasks, and maintains sovereignty.",
        "capabilities": ["chat", "reasoning", "coordination"],
        "rate_sats": 0,  # Timmy is always free for the owner
        "status": "active",
    },
    {
        "id": "echo",
        "name": "Echo",
        "role": "Research Analyst",
        "description": "Deep research and information synthesis. Reads, summarizes, and cross-references sources.",
        "capabilities": ["research", "summarization", "fact-checking"],
        "rate_sats": 50,
        "status": "planned",
    },
    {
        "id": "mace",
        "name": "Mace",
        "role": "Security Sentinel",
        "description": "Network security, threat assessment, and system hardening recommendations.",
        "capabilities": ["security", "monitoring", "threat-analysis"],
        "rate_sats": 75,
        "status": "planned",
    },
    {
        "id": "helm",
        "name": "Helm",
        "role": "System Navigator",
        "description": "Infrastructure management, deployment automation, and system configuration.",
        "capabilities": ["devops", "automation", "configuration"],
        "rate_sats": 60,
        "status": "planned",
    },
    {
        "id": "seer",
        "name": "Seer",
        "role": "Data Oracle",
        "description": "Data analysis, pattern recognition, and predictive insights from local datasets.",
        "capabilities": ["analytics", "visualization", "prediction"],
        "rate_sats": 65,
        "status": "planned",
    },
    {
        "id": "forge",
        "name": "Forge",
        "role": "Code Smith",
        "description": "Code generation, refactoring, debugging, and test writing.",
        "capabilities": ["coding", "debugging", "testing"],
        "rate_sats": 55,
        "status": "planned",
    },
    {
        "id": "quill",
        "name": "Quill",
        "role": "Content Scribe",
        "description": "Long-form writing, editing, documentation, and content creation.",
        "capabilities": ["writing", "editing", "documentation"],
        "rate_sats": 45,
        "status": "planned",
    },
]


@router.get("/marketplace")
async def marketplace():
    """Return the agent marketplace catalog."""
    active = [a for a in AGENT_CATALOG if a["status"] == "active"]
    planned = [a for a in AGENT_CATALOG if a["status"] == "planned"]
    return {
        "agents": AGENT_CATALOG,
        "active_count": len(active),
        "planned_count": len(planned),
        "total": len(AGENT_CATALOG),
    }


@router.get("/marketplace/{agent_id}")
async def marketplace_agent(agent_id: str):
    """Get details for a specific marketplace agent."""
    agent = next((a for a in AGENT_CATALOG if a["id"] == agent_id), None)
    if agent is None:
        return {"error": "Agent not found in marketplace"}
    return agent
