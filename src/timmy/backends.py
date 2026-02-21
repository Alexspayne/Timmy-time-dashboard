"""AirLLM backend — only imported when the airllm extra is installed.

Provides TimmyAirLLMAgent: a drop-in replacement for an Agno Agent that
exposes both the run(message, stream) → RunResult interface used by the
dashboard and the print_response(message, stream) interface used by the CLI.
On Apple Silicon (arm64 Darwin) the MLX backend is selected automatically;
everywhere else AutoModel (PyTorch) is used.

No cloud.  No telemetry.  Sats are sovereignty, boss.
"""

import platform
from dataclasses import dataclass
from typing import Literal

from timmy.prompts import TIMMY_SYSTEM_PROMPT

# HuggingFace model IDs for each supported size.
_AIRLLM_MODELS: dict[str, str] = {
    "8b":   "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "70b":  "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "405b": "meta-llama/Meta-Llama-3.1-405B-Instruct",
}

ModelSize = Literal["8b", "70b", "405b"]


@dataclass
class RunResult:
    """Minimal Agno-compatible run result — carries the model's response text."""
    content: str


def is_apple_silicon() -> bool:
    """Return True when running on an M-series Mac (arm64 Darwin)."""
    return platform.system() == "Darwin" and platform.machine() == "arm64"


def airllm_available() -> bool:
    """Return True when the airllm package is importable."""
    try:
        import airllm  # noqa: F401
        return True
    except ImportError:
        return False


class TimmyAirLLMAgent:
    """Thin AirLLM wrapper compatible with both dashboard and CLI call sites.

    Exposes:
      run(message, stream)           → RunResult(content=...)  [dashboard]
      print_response(message, stream) → None                   [CLI]

    Maintains a rolling 10-turn in-memory history so Timmy remembers the
    conversation within a session — no SQLite needed at this layer.
    """

    def __init__(self, model_size: str = "70b") -> None:
        model_id = _AIRLLM_MODELS.get(model_size)
        if model_id is None:
            raise ValueError(
                f"Unknown model size {model_size!r}. "
                f"Choose from: {list(_AIRLLM_MODELS)}"
            )

        if is_apple_silicon():
            from airllm import AirLLMMLX  # type: ignore[import]
            self._model = AirLLMMLX(model_id)
        else:
            from airllm import AutoModel  # type: ignore[import]
            self._model = AutoModel.from_pretrained(model_id)

        self._history: list[str] = []
        self._model_size = model_size

    # ── public interface (mirrors Agno Agent) ────────────────────────────────

    def run(self, message: str, *, stream: bool = False) -> RunResult:
        """Run inference and return a structured result (matches Agno Agent.run()).

        `stream` is accepted for API compatibility; AirLLM always generates
        the full output in one pass.
        """
        prompt = self._build_prompt(message)

        input_tokens = self._model.tokenizer(
            [prompt],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=2048,
        )
        output = self._model.generate(
            **input_tokens,
            max_new_tokens=512,
            use_cache=True,
            do_sample=True,
            temperature=0.7,
        )

        # Decode only the newly generated tokens, not the prompt.
        input_len = input_tokens["input_ids"].shape[1]
        response = self._model.tokenizer.decode(
            output[0][input_len:], skip_special_tokens=True
        ).strip()

        self._history.append(f"User: {message}")
        self._history.append(f"Timmy: {response}")

        return RunResult(content=response)

    def print_response(self, message: str, *, stream: bool = True) -> None:
        """Run inference and render the response to stdout (CLI interface)."""
        result = self.run(message, stream=stream)
        self._render(result.content)

    # ── private helpers ──────────────────────────────────────────────────────

    def _build_prompt(self, message: str) -> str:
        context = TIMMY_SYSTEM_PROMPT + "\n\n"
        # Include the last 10 turns (5 exchanges) for continuity.
        if self._history:
            context += "\n".join(self._history[-10:]) + "\n\n"
        return context + f"User: {message}\nTimmy:"

    @staticmethod
    def _render(text: str) -> None:
        """Print response with rich markdown when available, plain text otherwise."""
        try:
            from rich.console import Console
            from rich.markdown import Markdown
            Console().print(Markdown(text))
        except ImportError:
            print(text)
