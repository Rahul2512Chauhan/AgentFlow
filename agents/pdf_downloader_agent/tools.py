import os
import re
import requests
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_fixed
from utils.logger import log_info, log_error


def sanitize_filename(name: str) -> str:
    return re.sub(r'[^\w\-_. ]', '_', name)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def download_pdf(arxiv_url: str, output_dir: str = "data/papers") -> Optional[str]:
    """
    Downloads the PDF of an arXiv paper given its abstract URL.
    Returns the local file path of the downloaded PDF, or None if failed.
    """
    match = re.search(r'arxiv\.org\/abs\/([^\s\/]+)', arxiv_url)
    if not match:
        log_error(f"[Invalid URL] Cannot extract arXiv ID from: {arxiv_url}")
        return None

    arxiv_id = match.group(1)
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    safe_filename = sanitize_filename(f"{arxiv_id}.pdf")
    file_path = os.path.join(output_dir, safe_filename)

    # Skip if already downloaded
    if os.path.exists(file_path):
        log_info(f"[Skip] PDF already exists: {file_path}")
        return file_path

    os.makedirs(output_dir, exist_ok=True)
    log_info(f"[Download] Fetching PDF from {pdf_url}")

    try:
        response = requests.get(pdf_url, timeout=10)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        log_info(f"[Saved] PDF saved to: {file_path}")
        return file_path

    except requests.exceptions.RequestException as e:
        log_error(f"[Error] Failed to download PDF from {pdf_url} — {e}")
        raise  # tenacity will retry
