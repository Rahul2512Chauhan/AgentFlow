# agents/summariser_agent/tools.py

import os
import textwrap
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader
from utils.logger import log_info, log_error


# ✅ Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env")

# ✅ Setup Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL_NAME = "llama3-8b-8192"  # Other options: llama3-70b, gemma-7b

# ✅ Summarise text using Groq LLM
def summarise_text(text: str) -> str:
    if not text.strip():
        log_error("Invalid input: Empty text")
        return ""

    prompt = f"""Summarize the following scientific paper in 5–7 bullet points:\n\n{textwrap.shorten(text, width=12000, placeholder="...")}"""

    try:
        log_info("[Summariser] Requesting summary from Groq...")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes academic PDFs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=512,
        )
        summary = response.choices[0].message.content
        log_info("[Summariser] ✅ Received summary from Groq.")
        return summary.strip() if summary else ""
    except Exception as e:
        log_error(f"[Summariser] ❌ Groq request failed: {e}")
        return ""

# ✅ Extract raw text from PDF
def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text.strip()
    except Exception as e:
        log_error(f"[ExtractText] ❌ PDF read failed: {e}")
        return ""
