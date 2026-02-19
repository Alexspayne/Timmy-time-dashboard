from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb

from timmy.prompts import TIMMY_SYSTEM_PROMPT


def create_timmy(db_file: str = "timmy.db") -> Agent:
    """Instantiate Timmy with Agno + Ollama + SQLite memory."""
    return Agent(
        name="Timmy",
        model=Ollama(id="llama3.2"),
        db=SqliteDb(db_file=db_file),
        description=TIMMY_SYSTEM_PROMPT,
        add_history_to_context=True,
        num_history_runs=10,
        markdown=True,
    )
