import os
import textwrap
from openai import OpenAI
from dotenv import load_dotenv
from utils.logger import log_info, log_error
from PyPDF2 import PdfReader

# ✅ Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env")

# ✅ Setup Groq client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ✅ Choose Groq model
MODEL_NAME = "llama3-8b-8192"  # Try also: llama3-70b, gemma-7b

# ✅ Summarisation Function
def summarise_text(text: str) -> str:
    if not text or not isinstance(text, str):
        log_error("Invalid input: Text must be a non-empty string.")
        return ""

    prompt = f"""Summarize the following scientific paper content in 5–7 bullet points:\n\n{textwrap.shorten(text, width=12000, placeholder="...")}"""

    try:
        log_info(f"[Summariser] Requesting summary from Groq (model={MODEL_NAME})...")
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
        log_info("[Summariser] ✅ Summary received from Groq.")
        return summary.strip()  # type: ignore

    except Exception as e:
        log_error(f"[Summariser] ❌ Groq request failed: {e}")
        return ""

# ✅ PDF Text Extraction Function
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file using PyPDF2.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        log_error(f"[ExtractText] ❌ Failed to read PDF: {e}")
        return ""
