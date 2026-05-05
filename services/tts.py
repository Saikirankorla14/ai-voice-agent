# services/tts.py
# We use the browser's built-in Web Speech API (free, no server call needed).
# This file exists for future upgrades — e.g. swapping in OpenAI TTS later.

def get_tts_provider() -> str:
    """Returns which TTS method the frontend should use."""
    return "browser"  # options: "browser", "openai"