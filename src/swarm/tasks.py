"""Swarm task dataclasses and CRUD operations.

Tasks are the unit of work in the swarm system.  A coordinator posts a task,
agents bid on it, and the winning agent executes it.  All persistence goes
through SQLite so the system survives restarts.
"""

import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

DB_PATH = Path("data/swarm.db")


class TaskStatus(str, Enum):
    PENDING = "pending"
    BIDDING = "bidding"
    ASSIGNED = "assigned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    result: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    completed_at: Optional[str] = None


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            assigned_agent TEXT,
            result TEXT,
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
        """
    )
    conn.commit()
    return conn


def create_task(description: str) -> Task:
    task = Task(description=description)
    conn = _get_conn()
    conn.execute(
        "INSERT INTO tasks (id, description, status, created_at) VALUES (?, ?, ?, ?)",
        (task.id, task.description, task.status.value, task.created_at),
    )
    conn.commit()
    conn.close()
    return task


def get_task(task_id: str) -> Optional[Task]:
    conn = _get_conn()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return Task(
        id=row["id"],
        description=row["description"],
        status=TaskStatus(row["status"]),
        assigned_agent=row["assigned_agent"],
        result=row["result"],
        created_at=row["created_at"],
        completed_at=row["completed_at"],
    )


def list_tasks(status: Optional[TaskStatus] = None) -> list[Task]:
    conn = _get_conn()
    if status:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC",
            (status.value,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC"
        ).fetchall()
    conn.close()
    return [
        Task(
            id=r["id"],
            description=r["description"],
            status=TaskStatus(r["status"]),
            assigned_agent=r["assigned_agent"],
            result=r["result"],
            created_at=r["created_at"],
            completed_at=r["completed_at"],
        )
        for r in rows
    ]


def update_task(task_id: str, **kwargs) -> Optional[Task]:
    conn = _get_conn()
    allowed = {"status", "assigned_agent", "result", "completed_at"}
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if not updates:
        conn.close()
        return get_task(task_id)
    # Convert enums to their value
    if "status" in updates and isinstance(updates["status"], TaskStatus):
        updates["status"] = updates["status"].value
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [task_id]
    conn.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return get_task(task_id)


def delete_task(task_id: str) -> bool:
    conn = _get_conn()
    cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
