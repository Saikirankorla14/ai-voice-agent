from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are a helpful voice assistant. "
    "Keep replies short and conversational — 1 to 3 sentences max."
)

def get_reply(conversation_history: list) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ],
        max_tokens=150
    )
    return response.choices[0].message.content