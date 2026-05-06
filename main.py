from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from services.stt import transcribe_audio
from services.llm import get_reply

app = FastAPI()

# Allow ngrok hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

conversation_history = []

@app.get("/")
async def home():
    with open("static/index.html") as f:
        return HTMLResponse(f.read())

@app.post("/talk")
async def talk(audio: UploadFile = File(...)):
    audio_bytes = await audio.read()
    transcript = await transcribe_audio(audio_bytes)

    if not transcript:
        return {"reply": "", "transcript": ""}

    conversation_history.append({"role": "user", "content": transcript})
    reply = get_reply(conversation_history)
    conversation_history.append({"role": "assistant", "content": reply})

    if len(conversation_history) > 20:
        conversation_history.pop(0)
        conversation_history.pop(0)

    return {"reply": reply, "transcript": transcript}

@app.delete("/reset")
async def reset():
    conversation_history.clear()
    return {"status": "cleared"}