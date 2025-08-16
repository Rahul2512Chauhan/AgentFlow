from .base import BaseTool
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
from utils.logger import log_info, log_warn, log_error

ARXIV_API_URL = "http://export.arxiv.org/api/query"


def _search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    """Pure arXiv API search with minimal deps."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
    }

    try:
        resp = requests.get(ARXIV_API_URL, params=params, timeout=15)
    except Exception as e:
        log_error(f"[arXiv] Request error: {e}")
        return []

    if resp.status_code != 200:
        log_warn(f"[arXiv] API request failed with {resp.status_code}")
        return []

    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as e:
        log_error(f"[arXiv] XML parse error: {e}")
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers: List[Dict] = []

    for entry in root.findall("atom:entry", ns):
        try:
            paper_id = entry.find("atom:id", ns).text  # e.g., http://arxiv.org/abs/2307.00865v1
            title = (entry.find("atom:title", ns).text or "").strip()
            summary = (entry.find("atom:summary", ns).text or "").strip()
            arxiv_id = paper_id.split("/")[-1] if paper_id else ""

            # direct PDF link
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf" if arxiv_id else None

            papers.append({
                "arxiv_id": arxiv_id,
                "title": title,
                "summary": summary,
                "url": paper_id,     # abstract page
                "pdf_url": pdf_url,  # direct PDF
            })
        except Exception as e:
            log_warn(f"[arXiv] Skipping malformed entry: {e}")

    return papers


class WebSearchTool(BaseTool):
    """
    Tool for searching research papers from arXiv.
    """

    def __init__(self, name: str = "web_search"):
        super().__init__(name)

    def run(self, input: dict) -> dict:
        query = input.get("query")
        max_results = int(input.get("max_results", 5))
        if not query:
            return {"error": "Missing 'query' in input"}

        try:
            log_info(f"[WebSearchTool] 🔎 Running web search for query='{query}'...")
            results = _search_arxiv(query, max_results=max_results)

            if not results:
                log_warn(f"[WebSearchTool] ⚠️ No results found for query='{query}'")
                # Keep both keys for compatibility with agents
                return {"results": [], "papers": []}

            log_info(f"[WebSearchTool] ✅ Retrieved {len(results)} results")
            # Provide both keys: results (tool-style) and papers (agent-style)
            return {"results": results, "papers": results}

        except Exception as e:
            log_error(f"[WebSearchTool] ❌ Error during web search: {e}")
            return {"error": str(e)}
