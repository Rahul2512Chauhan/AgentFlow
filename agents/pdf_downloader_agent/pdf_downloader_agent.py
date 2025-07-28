import os
from agents.base import BaseAgent
from agents.pdf_downloader_agent.tools import download_pdf
from utils.logger import log_info, log_warn, log_error

class PDFDownloaderAgent(BaseAgent):
    def __init__(self):
        self.output_dir = "data/papers"
        os.makedirs(self.output_dir, exist_ok=True)
        log_info("PDFDownloaderAgent initialized.")

    def run(self, input_dict: dict) -> dict:
        arxiv_results = input_dict.get("results", [])
        if not arxiv_results:
            log_warn("No results found in input_dict.")
            return {"pdfs": []}

        log_info(f"Downloading {len(arxiv_results)} PDFs...")

        downloaded_pdfs = []
        for idx, result in enumerate(arxiv_results, start=1):
            url = result.get("url")
            title = result.get("title", "Unknown Title")

            if not url:
                log_warn(f"Missing URL for result #{idx}: {title}")
                continue

            try:
                pdf_path = download_pdf(url, self.output_dir)
                downloaded_pdfs.append({
                    "title": title,
                    "url": url,
                    "pdf_path": pdf_path
                })
                log_info(f"✅ Downloaded: {title}")
            except Exception as e:
                log_error(f"❌ Failed to download {title} — {e}")

        log_info(f"✅ Downloaded {len(downloaded_pdfs)} PDFs.")
        return {"pdfs": downloaded_pdfs}
