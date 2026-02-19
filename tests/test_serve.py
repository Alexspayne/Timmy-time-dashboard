"""Tests for the `timmy serve` CLI command."""
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from timmy.cli import app

runner = CliRunner()


def test_serve_invokes_uvicorn():
    """serve command should call uvicorn.run with host=0.0.0.0 by default."""
    with patch("timmy.cli.uvicorn.run") as mock_run:
        result = runner.invoke(app, ["serve", "--port", "9999"])

    assert result.exit_code == 0
    mock_run.assert_called_once()
    call_kwargs = mock_run.call_args
    assert call_kwargs.kwargs["host"] == "0.0.0.0"
    assert call_kwargs.kwargs["port"] == 9999


def test_serve_custom_host():
    """--host flag should be forwarded to uvicorn."""
    with patch("timmy.cli.uvicorn.run") as mock_run:
        runner.invoke(app, ["serve", "--host", "127.0.0.1", "--port", "8000"])

    assert mock_run.call_args.kwargs["host"] == "127.0.0.1"


def test_serve_prints_network_url(capsys):
    """serve command should print the network URL so the user can open it on their phone."""
    with patch("timmy.cli.uvicorn.run"):
        with patch("timmy.cli.socket.socket") as mock_sock_cls:
            mock_sock = MagicMock()
            mock_sock.__enter__ = MagicMock(return_value=mock_sock)
            mock_sock.__exit__ = MagicMock(return_value=False)
            mock_sock.getsockname.return_value = ("192.168.1.42", 0)
            mock_sock_cls.return_value = mock_sock

            result = runner.invoke(app, ["serve", "--port", "8000"])

    assert "192.168.1.42" in result.output
    assert "8000" in result.output


def test_serve_reload_flag():
    """--reload flag should be forwarded to uvicorn."""
    with patch("timmy.cli.uvicorn.run") as mock_run:
        runner.invoke(app, ["serve", "--reload"])

    assert mock_run.call_args.kwargs["reload"] is True
