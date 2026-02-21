"""Text-to-speech output via pyttsx3.

Provides a non-blocking TTS interface that speaks Timmy's responses
aloud.  Falls back gracefully when pyttsx3 is not installed or when
no audio device is available (e.g., headless servers, CI).
"""

import logging
import threading
from typing import Optional

logger = logging.getLogger(__name__)


class VoiceTTS:
    """Text-to-speech engine for Timmy's voice output."""

    def __init__(self, rate: int = 175, volume: float = 0.9) -> None:
        self._engine = None
        self._rate = rate
        self._volume = volume
        self._available = False
        self._lock = threading.Lock()
        self._init_engine()

    def _init_engine(self) -> None:
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate", self._rate)
            self._engine.setProperty("volume", self._volume)
            self._available = True
            logger.info("VoiceTTS: engine initialized (rate=%d)", self._rate)
        except Exception as exc:
            self._available = False
            logger.warning("VoiceTTS: not available — %s", exc)

    @property
    def available(self) -> bool:
        return self._available

    def speak(self, text: str) -> None:
        """Speak text aloud.  Non-blocking — runs in a background thread."""
        if not self._available or self._engine is None:
            logger.debug("VoiceTTS: skipping (not available)")
            return

        def _do_speak():
            with self._lock:
                try:
                    self._engine.say(text)
                    self._engine.runAndWait()
                except Exception as exc:
                    logger.error("VoiceTTS: speech failed — %s", exc)

        thread = threading.Thread(target=_do_speak, daemon=True)
        thread.start()

    def speak_sync(self, text: str) -> None:
        """Speak text aloud synchronously (blocks until done)."""
        if not self._available or self._engine is None:
            return
        with self._lock:
            try:
                self._engine.say(text)
                self._engine.runAndWait()
            except Exception as exc:
                logger.error("VoiceTTS: speech failed — %s", exc)

    def set_rate(self, rate: int) -> None:
        self._rate = rate
        if self._engine:
            self._engine.setProperty("rate", rate)

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))
        if self._engine:
            self._engine.setProperty("volume", self._volume)

    def get_voices(self) -> list[dict]:
        """Return available system voices."""
        if not self._engine:
            return []
        try:
            voices = self._engine.getProperty("voices")
            return [
                {"id": v.id, "name": v.name, "languages": getattr(v, "languages", [])}
                for v in voices
            ]
        except Exception:
            return []

    def set_voice(self, voice_id: str) -> None:
        if self._engine:
            self._engine.setProperty("voice", voice_id)


# Module-level singleton
voice_tts = VoiceTTS()
