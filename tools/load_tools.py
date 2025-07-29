# tools/load_tools.py
from typing import List, Dict, Optional
from .base import BaseTool
from .pdf_parser import PDFParserTool
from .memory import MemoryTool
from .web_search import WebSearchTool

def load_tools(use: Optional[List[str]] = None) -> Dict[str, BaseTool]:
    """
    Initialize and return the selected tools.

    Arguments:
        use: List of tool names to load. Options: "pdf_parser", "memory", "web_search".

    Returns:
        Dict mapping tool name to initialized tool instance.
    """
    use = use or ["pdf_parser", "memory", "web_search"]
    tools: Dict[str, BaseTool] = {}

    if "pdf_parser" in use:
        tools["pdf_parser"] = PDFParserTool(name="pdf_parser")

    if "memory" in use:
        tools["memory"] = MemoryTool(name="memory")

    if "web_search" in use:
        tools["web_search"] = WebSearchTool(name="web_search")

    return tools
