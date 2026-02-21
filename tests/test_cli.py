from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from timmy.cli import app
from timmy.prompts import TIMMY_STATUS_PROMPT

runner = CliRunner()


def test_status_uses_status_prompt():
    """status command must pass TIMMY_STATUS_PROMPT to the agent."""
    mock_timmy = MagicMock()

    with patch("timmy.cli.create_timmy", return_value=mock_timmy):
        runner.invoke(app, ["status"])

    mock_timmy.print_response.assert_called_once_with(TIMMY_STATUS_PROMPT, stream=False)


def test_status_does_not_use_inline_string():
    """status command must not pass the old inline hardcoded string."""
    mock_timmy = MagicMock()

    with patch("timmy.cli.create_timmy", return_value=mock_timmy):
        runner.invoke(app, ["status"])

    call_args = mock_timmy.print_response.call_args
    assert call_args[0][0] != "Brief status report — one sentence."
