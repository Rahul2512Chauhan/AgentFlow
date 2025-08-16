from agents.base import BaseAgent
from .tools import search_papers
from utils.logger import log_info, log_warn, log_error


class SearchAgent(BaseAgent):
    """
    Agent responsible for searching research papers on arXiv.
    """

    def run(self, input: dict) -> dict:
        query = input.get("query")
        if not query:
            log_error("[SearchAgent] ❌ Missing 'query' in input")
            return {"error": "Missing 'query'"}

        try:
            log_info(f"[SearchAgent] 🔎 Searching arXiv for query='{query}'...")
            papers = search_papers(query, max_results=5)

            if not papers:
                log_warn(f"[SearchAgent] ⚠️ No results found for query='{query}'")
                return {"papers": []}

            log_info(f"[SearchAgent] ✅ Retrieved {len(papers)} papers")
            return {"papers": papers}

        except Exception as e:
            log_error(f"[SearchAgent] ❌ Error while searching arXiv: {e}")
            return {"error": str(e)}
