from unittest.mock import MagicMock, patch


def test_create_timmy_returns_agent():
    """create_timmy should delegate to Agno Agent with correct config."""
    with patch("timmy.agent.Agent") as MockAgent, \
         patch("timmy.agent.Ollama"), \
         patch("timmy.agent.SqliteDb"):

        mock_instance = MagicMock()
        MockAgent.return_value = mock_instance

        from timmy.agent import create_timmy
        result = create_timmy()

        assert result is mock_instance
        MockAgent.assert_called_once()


def test_create_timmy_agent_name():
    with patch("timmy.agent.Agent") as MockAgent, \
         patch("timmy.agent.Ollama"), \
         patch("timmy.agent.SqliteDb"):

        from timmy.agent import create_timmy
        create_timmy()

        kwargs = MockAgent.call_args.kwargs
        assert kwargs["name"] == "Timmy"


def test_create_timmy_uses_llama32():
    with patch("timmy.agent.Agent"), \
         patch("timmy.agent.Ollama") as MockOllama, \
         patch("timmy.agent.SqliteDb"):

        from timmy.agent import create_timmy
        create_timmy()

        MockOllama.assert_called_once_with(id="llama3.2")


def test_create_timmy_history_config():
    with patch("timmy.agent.Agent") as MockAgent, \
         patch("timmy.agent.Ollama"), \
         patch("timmy.agent.SqliteDb"):

        from timmy.agent import create_timmy
        create_timmy()

        kwargs = MockAgent.call_args.kwargs
        assert kwargs["add_history_to_context"] is True
        assert kwargs["num_history_runs"] == 10
        assert kwargs["markdown"] is True


def test_create_timmy_custom_db_file():
    with patch("timmy.agent.Agent"), \
         patch("timmy.agent.Ollama"), \
         patch("timmy.agent.SqliteDb") as MockDb:

        from timmy.agent import create_timmy
        create_timmy(db_file="custom.db")

        MockDb.assert_called_once_with(db_file="custom.db")


def test_create_timmy_embeds_system_prompt():
    from timmy.prompts import TIMMY_SYSTEM_PROMPT

    with patch("timmy.agent.Agent") as MockAgent, \
         patch("timmy.agent.Ollama"), \
         patch("timmy.agent.SqliteDb"):

        from timmy.agent import create_timmy
        create_timmy()

        kwargs = MockAgent.call_args.kwargs
        assert kwargs["description"] == TIMMY_SYSTEM_PROMPT
