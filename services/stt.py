# services/stt.py
from groq import Groq
from config import GROQ_API_KEY
import tempfile, os

client = Groq(api_key=GROQ_API_KEY)

async def transcribe_audio(audio_bytes: bytes) -> str:
    # Guard: ignore clips that are too short (less than 1KB = basically silence)
    if len(audio_bytes) < 1000:
        return ""

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                file=(tmp_path, f.read()),
                model="whisper-large-v3",
                response_format="text"
            )
        return result.strip()
    except Exception as e:
        print(f"STT error: {e}")
        return ""
    finally:
        os.unlink(tmp_path)