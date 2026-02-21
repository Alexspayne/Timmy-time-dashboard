"""Swarm dashboard routes — /swarm/* endpoints.

Provides REST endpoints for managing the swarm: listing agents,
spawning sub-agents, posting tasks, and viewing auction results.
"""

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from swarm.coordinator import coordinator
from swarm.tasks import TaskStatus

router = APIRouter(prefix="/swarm", tags=["swarm"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))


@router.get("")
async def swarm_status():
    """Return the current swarm status summary."""
    return coordinator.status()


@router.get("/live", response_class=HTMLResponse)
async def swarm_live_page(request: Request):
    """Render the live swarm dashboard page."""
    return templates.TemplateResponse(
        "swarm_live.html",
        {"request": request, "page_title": "Swarm Live"},
    )


@router.get("/agents")
async def list_swarm_agents():
    """List all registered swarm agents."""
    agents = coordinator.list_swarm_agents()
    return {
        "agents": [
            {
                "id": a.id,
                "name": a.name,
                "status": a.status,
                "capabilities": a.capabilities,
                "last_seen": a.last_seen,
            }
            for a in agents
        ]
    }


@router.post("/spawn")
async def spawn_agent(name: str = Form(...)):
    """Spawn a new sub-agent in the swarm."""
    result = coordinator.spawn_agent(name)
    return result


@router.delete("/agents/{agent_id}")
async def stop_agent(agent_id: str):
    """Stop and unregister a swarm agent."""
    success = coordinator.stop_agent(agent_id)
    return {"stopped": success, "agent_id": agent_id}


@router.get("/tasks")
async def list_tasks(status: Optional[str] = None):
    """List swarm tasks, optionally filtered by status."""
    task_status = TaskStatus(status) if status else None
    tasks = coordinator.list_tasks(task_status)
    return {
        "tasks": [
            {
                "id": t.id,
                "description": t.description,
                "status": t.status.value,
                "assigned_agent": t.assigned_agent,
                "result": t.result,
                "created_at": t.created_at,
                "completed_at": t.completed_at,
            }
            for t in tasks
        ]
    }


@router.post("/tasks")
async def post_task(description: str = Form(...)):
    """Post a new task to the swarm for bidding."""
    task = coordinator.post_task(description)
    return {
        "task_id": task.id,
        "description": task.description,
        "status": task.status.value,
    }


@router.post("/tasks/auction")
async def post_task_and_auction(description: str = Form(...)):
    """Post a task and immediately run an auction to assign it."""
    task = coordinator.post_task(description)
    winner = await coordinator.run_auction_and_assign(task.id)
    updated = coordinator.get_task(task.id)
    return {
        "task_id": task.id,
        "description": task.description,
        "status": updated.status.value if updated else task.status.value,
        "assigned_agent": updated.assigned_agent if updated else None,
        "winning_bid": winner.bid_sats if winner else None,
    }


@router.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get details for a specific task."""
    task = coordinator.get_task(task_id)
    if task is None:
        return {"error": "Task not found"}
    return {
        "id": task.id,
        "description": task.description,
        "status": task.status.value,
        "assigned_agent": task.assigned_agent,
        "result": task.result,
        "created_at": task.created_at,
        "completed_at": task.completed_at,
    }
