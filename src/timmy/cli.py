import typer

from timmy.agent import create_timmy
from timmy.prompts import TIMMY_STATUS_PROMPT

app = typer.Typer(help="Timmy — sovereign AI agent")


@app.command()
def think(topic: str = typer.Argument(..., help="Topic to reason about")):
    """Ask Timmy to think carefully about a topic."""
    timmy = create_timmy()
    timmy.print_response(f"Think carefully about: {topic}", stream=True)


@app.command()
def chat(message: str = typer.Argument(..., help="Message to send")):
    """Send a message to Timmy."""
    timmy = create_timmy()
    timmy.print_response(message, stream=True)


@app.command()
def status():
    """Print Timmy's operational status."""
    timmy = create_timmy()
    timmy.print_response(TIMMY_STATUS_PROMPT, stream=False)


def main():
    app()
