import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from utils.logger import log_error, log_info, log_warn

ARXIV_API_URL = "http://export.arxiv.org/api/query"

def search_papers(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search arXiv using their API.
    """
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
    }

    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=10)
        if response.status_code != 200:
            log_warn(f"[arXiv] API request failed with {response.status_code}")
            return []

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        papers = []
        for entry in root.findall("atom:entry", ns):
            paper_id = entry.find("atom:id", ns).text
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            url = paper_id

            papers.append({
                "arxiv_id": paper_id.split("/")[-1],
                "title": title,
                "summary": summary,
                "url": url,
            })

        log_info(f"[arXiv] Found {len(papers)} papers for query='{query}'")
        return papers

    except Exception as e:
        log_error(f"[arXiv] Error while searching: {e}")
        return []
