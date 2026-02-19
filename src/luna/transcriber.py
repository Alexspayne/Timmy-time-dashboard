"""Luna project — pluggable audio transcription interface."""

import abc
import tempfile
from pathlib import Path


class Transcriber(abc.ABC):
    @abc.abstractmethod
    async def transcribe(self, audio_bytes: bytes) -> str: ...


class WhisperTranscriber(Transcriber):
    """Local transcription via openai-whisper. Install with: pip install openai-whisper"""

    def __init__(self, model_name: str = "base"):
        self._model_name = model_name
        self._model = None  # lazy-loaded on first use

    def _load_model(self):
        try:
            import whisper
        except ImportError as exc:
            raise RuntimeError(
                "openai-whisper is not installed. Run: pip install openai-whisper"
            ) from exc
        if self._model is None:
            import whisper
            self._model = whisper.load_model(self._model_name)
        return self._model

    async def transcribe(self, audio_bytes: bytes) -> str:
        model = self._load_model()
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            f.write(audio_bytes)
            tmp_path = f.name
        try:
            result = model.transcribe(tmp_path)
            return result["text"].strip()
        finally:
            Path(tmp_path).unlink(missing_ok=True)
