# config.py
from dotenv import load_dotenv
import os

load_dotenv()  # reads .env file automatically

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Check your .env file.")