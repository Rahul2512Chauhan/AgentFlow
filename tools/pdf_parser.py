from .base import BaseTool
from utils.logger import log_error ,log_info , log_warn
import os

try:
    import fitz #PyMuPDF
    _HAVE_FITZ = True
except ImportError:
    fitz = None
    _HAVE_FITZ = False


class PDFParserTool(BaseTool):
    def __init__(self, name: str = "pdf_parser"):
        super().__init__(name)

    def run(self, input: dict) -> dict:
        pdf_path = input.get("pdf_path")
        if not pdf_path:
            return {"status":"error", "message":"Missing 'pdf_path' in input"}

        if not os.path.exists(pdf_path):
            return {"status":"error", "message": f"PDF file not found at: {pdf_path}"}

        if not _HAVE_FITZ:
            log_error("[PDFParserTool] ❌ PyMuPDF (fitz) not installed. Cannot parse PDFs.")
            return {"status": "error", "message": "PyMuPDF not installed"}
        
        try:
            text = self.extract_text(pdf_path)
            log_info(f"[PDFParserTool] ✅ Extracted {len(text)} characters from {pdf_path}")
            return {
                "text": text,
                "length": len(text),
                "status": "success"
            }
        except Exception as e:
            log_error(f"[PDFParserTool] ❌ Failed to parse {pdf_path}: {e}")
            return {"status": "error", "message": str(e)}

    def extract_text(self, pdf_path: str) -> str:
        text_chunks = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text("text") 
                if page_text:
                    text_chunks.append(page_text.strip())
        return "\n\n".join(text_chunks)
