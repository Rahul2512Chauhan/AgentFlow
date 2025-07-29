# tools/web_search.py
from .base import BaseTool
import random

class WebSearchTool(BaseTool):
    def __init__(self, name: str = "web_search"):
        super().__init__(name)

    def run(self, input: dict) -> dict:
        query = input.get("query")
        if not query:
            return {"error": "Missing 'query' in input"}
        return self._stub_search(query)

    def _stub_search(self, query: str) -> dict:
        fake_titles = [
            "Improving LLM Summarization with Graph Agents",
            "A Survey on Autonomous Language Agents",
            "Multi-agent Planning using Transformers",
            "Memory-Augmented LLMs for Scientific Papers",
            "Retrieval-Augmented Generation with Multi-Tool Systems"
        ]
        selected_title = random.choice(fake_titles)
        fake_arxiv_id = f"2407.{random.randint(10000,99999)}"
        return {
            "query": query,
            "title": selected_title,
            "arxiv_id": fake_arxiv_id,
            "url": f"https://arxiv.org/abs/{fake_arxiv_id}",
            "source": "stub"
        }
