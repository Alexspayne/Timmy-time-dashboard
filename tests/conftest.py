import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

# ── Mock agno so tests run without it installed ───────────────────────────────
# Uses setdefault: real module is used if installed, mock otherwise.
for _mod in [
    "agno",
    "agno.agent",
    "agno.models",
    "agno.models.ollama",
    "agno.db",
    "agno.db.sqlite",
]:
    sys.modules.setdefault(_mod, MagicMock())


@pytest.fixture
def client():
    from dashboard.app import app
    with TestClient(app) as c:
        yield c
