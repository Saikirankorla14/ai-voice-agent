# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from services.stt import transcribe_audio
from services.llm import get_reply

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory conversation history (resets on server restart)
conversation_history = []

@app.get("/")
async def home():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.post("/talk")
async def talk(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()

    # 1. Speech → Text
    transcript = await transcribe_audio(audio_bytes)

    if not transcript:
        return {"reply": "", "transcript": ""}

    # 2. Text → LLM reply
    conversation_history.append({"role": "user", "content": transcript})
    reply = get_reply(conversation_history)
    conversation_history.append({"role": "assistant", "content": reply})

    # Keep last 20 messages only (10 turns)
    if len(conversation_history) > 20:
        conversation_history.pop(0)
        conversation_history.pop(0)

    return {"reply": reply, "transcript": transcript}

@app.delete("/reset")
async def reset():
    conversation_history.clear()
    return {"status": "cleared"}