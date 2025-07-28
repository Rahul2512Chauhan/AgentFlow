from agents.base import BaseAgent
from utils.logger import log_info, log_error
from typing import Dict
from agents.search_agent import tools  # We’ll add the actual tool function later

class SearchAgent(BaseAgent):
    """Agent that searches research papers based on a query."""

    def __init__(self):
        super().__init__(name="SearchAgent")

    def run(self, input_dict: Dict) -> Dict:
        """
        Accepts a dictionary with a 'query' key and returns search results.
        """
        query = input_dict.get("query", "").strip()

        if not query:
            log_error("SearchAgent received empty or missing 'query'")
            return {
                "agent": self.name,
                "query": None,
                "results": [],
                "error": "Missing or empty 'query'"
            }

        log_info(f"{self.name} received query: {query}")

        try:
            # Placeholder call — we'll define this in tools.py
            results = tools.search_papers(query)

            return {
                "agent": self.name,
                "query": query,
                "results": results
            }

        except Exception as e:
            log_error(f"{self.name} failed to fetch results: {e}")
            return {
                "agent": self.name,
                "query": query,
                "results": [],
                "error": str(e)
            }
