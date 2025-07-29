from .base import BaseTool
import fitz
import os

class PDFParserTool(BaseTool):
    def __init__(self, name: str = "pdf_parser"):
        super().__init__(name)

    def run(self, input: dict) -> dict:
        pdf_path = input.get("pdf_path")
        if not pdf_path:
            return {"error": "Missing 'pdf_path' in input"}

        if not os.path.exists(pdf_path):
            return {"error": f"PDF file not found at: {pdf_path}"}

        try:
            text = self.extract_text(pdf_path)
            return {
                "text": text,
                "length": len(text),
                "status": "success"
            }
        except Exception as e:
            return {"error": str(e)}

    def extract_text(self, pdf_path: str) -> str:
        text = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text("text")  # type: ignore
                if page_text:
                    text.append(page_text.strip())
        return "\n\n".join(text)
