"""Voice routes — /voice/* endpoints.

Provides NLU intent detection and TTS control endpoints for the
voice interface.
"""

from fastapi import APIRouter, Form

from voice.nlu import detect_intent, extract_command

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/nlu")
async def nlu_detect(text: str = Form(...)):
    """Detect intent from a text utterance."""
    intent = detect_intent(text)
    command = extract_command(text)
    return {
        "intent": intent.name,
        "confidence": intent.confidence,
        "entities": intent.entities,
        "command": command,
        "raw_text": intent.raw_text,
    }


@router.get("/tts/status")
async def tts_status():
    """Check TTS engine availability."""
    try:
        from timmy_serve.voice_tts import voice_tts
        return {
            "available": voice_tts.available,
            "voices": voice_tts.get_voices() if voice_tts.available else [],
        }
    except Exception:
        return {"available": False, "voices": []}


@router.post("/tts/speak")
async def tts_speak(text: str = Form(...)):
    """Speak text aloud via TTS."""
    try:
        from timmy_serve.voice_tts import voice_tts
        if not voice_tts.available:
            return {"spoken": False, "reason": "TTS engine not available"}
        voice_tts.speak(text)
        return {"spoken": True, "text": text}
    except Exception as exc:
        return {"spoken": False, "reason": str(exc)}
