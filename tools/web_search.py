from .base import BaseTool
from agents.search_agent.tools import search_papers
from utils.logger import log_info, log_error


class WebSearchTool(BaseTool):
    """
    Tool for searching research papers from arXiv.
    """

    def __init__(self, name: str = "web_search"):
        super().__init__(name)

    def run(self, input: dict) -> dict:
        query = input.get("query")
        if not query:
            return {"error": "Missing 'query' in input"}

        try:
            log_info(f"[WebSearchTool] 🔎 Running web search for query='{query}'...")
            results = search_papers(query, max_results=5)

            if not results:
                log_info(f"[WebSearchTool] ⚠️ No results found for query='{query}'")
                return {"results": []}

            log_info(f"[WebSearchTool] ✅ Retrieved {len(results)} results")
            return {"results": results}

        except Exception as e:
            log_error(f"[WebSearchTool] ❌ Error during web search: {e}")
            return {"error": str(e)}
