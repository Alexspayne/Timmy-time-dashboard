from typing import Optional

import typer

from timmy.agent import create_timmy
from timmy.prompts import TIMMY_STATUS_PROMPT

app = typer.Typer(help="Timmy — sovereign AI agent")

# Shared option definitions (reused across commands for consistency).
_BACKEND_OPTION = typer.Option(
    None,
    "--backend",
    "-b",
    help="Inference backend: 'ollama' (default) | 'airllm' | 'auto'",
)
_MODEL_SIZE_OPTION = typer.Option(
    None,
    "--model-size",
    "-s",
    help="AirLLM model size when --backend airllm: '8b' | '70b' | '405b'",
)


@app.command()
def think(
    topic: str = typer.Argument(..., help="Topic to reason about"),
    backend: Optional[str] = _BACKEND_OPTION,
    model_size: Optional[str] = _MODEL_SIZE_OPTION,
):
    """Ask Timmy to think carefully about a topic."""
    timmy = create_timmy(backend=backend, model_size=model_size)
    timmy.print_response(f"Think carefully about: {topic}", stream=True)


@app.command()
def chat(
    message: str = typer.Argument(..., help="Message to send"),
    backend: Optional[str] = _BACKEND_OPTION,
    model_size: Optional[str] = _MODEL_SIZE_OPTION,
):
    """Send a message to Timmy."""
    timmy = create_timmy(backend=backend, model_size=model_size)
    timmy.print_response(message, stream=True)


@app.command()
def status(
    backend: Optional[str] = _BACKEND_OPTION,
    model_size: Optional[str] = _MODEL_SIZE_OPTION,
):
    """Print Timmy's operational status."""
    timmy = create_timmy(backend=backend, model_size=model_size)
    timmy.print_response(TIMMY_STATUS_PROMPT, stream=False)


def main():
    app()
