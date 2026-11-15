
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in .env")

if not GROQ_MODEL:
    raise ValueError("GROQ_MODEL missing in .env")

llm = ChatGroq(
    model=GROQ_MODEL,
    temperature=0.2,
    max_tokens=1600,
    api_key=GROQ_API_KEY
)

print(f"BizPilot LLM configured: {GROQ_MODEL}")
