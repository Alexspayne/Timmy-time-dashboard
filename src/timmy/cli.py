import socket

import typer
import uvicorn
from rich.console import Console
from rich.panel import Panel

from timmy.agent import create_timmy

app = typer.Typer(help="Timmy — sovereign AI agent")
console = Console()


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
    timmy.print_response("Brief status report — one sentence.", stream=False)


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind (0.0.0.0 = all interfaces)"),
    port: int = typer.Option(8000, help="Port to listen on"),
    reload: bool = typer.Option(False, "--reload", help="Auto-reload on code changes"),
):
    """Start the Mission Control dashboard (accessible on your local network)."""
    # Resolve the LAN IP so the user can open it on their phone
    try:
        lan_ip = socket.gethostbyname(socket.gethostname())
        # On some Linux setups gethostbyname returns 127.x; use a UDP trick instead
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            lan_ip = s.getsockname()[0]
    except Exception:
        lan_ip = "your-machine-ip"

    console.print(
        Panel(
            f"[bold green]Dashboard running[/bold green]\n\n"
            f"  Local:   [cyan]http://localhost:{port}[/cyan]\n"
            f"  Network: [cyan]http://{lan_ip}:{port}[/cyan]  ← open this on your phone",
            title="Timmy Mission Control",
            expand=False,
        )
    )

    uvicorn.run(
        "dashboard.app:app",
        host=host,
        port=port,
        reload=reload,
        app_dir="src",
    )


def main():
    app()
