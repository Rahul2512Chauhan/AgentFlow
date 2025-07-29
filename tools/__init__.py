# tools/__init__.py

from tools.base import BaseTool
from tools.pdf_parser import PDFParserTool
from tools.memory import MemoryTool
from tools.web_search import WebSearchTool

def load_tools(task_id: str) -> dict:
    """Returns a dictionary of tool_name -> tool_instance."""
    return {
        "pdf_parser": PDFParserTool(task_id),
        "memory": MemoryTool(task_id),
        "web_search": WebSearchTool(task_id),
    }
