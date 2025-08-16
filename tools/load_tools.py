from typing import List, Dict, Optional
from .base import BaseTool
from utils.logger import log_error ,log_info , log_warn

def load_tools(use: Optional[List[str]] = None) -> Dict[str, BaseTool]:
    """
    Initialize and return the selected tools.

    Arguments:
        use: List of tool names to load. 
            Options: "pdf_parser", "memory", "web_search".

    Returns:
        Dict mapping tool name to initialized tool instance.
    """

    use = use or ["pdf_parser", "memory", "web_search"]
    tools: Dict[str, BaseTool] = {}

    for tool_name in use:
        try:
            if tool_name == "pdf_parser":
                from .pdf_parser import PDFParserTool
                tools["pdf_parser"] = PDFParserTool(name="pdf_parser")
                log_info("[LoadTools] ✅ Loaded PDFParserTool")

            elif tool_name == "memory":
                from .memory import MemoryTool
                tools["memory"] = MemoryTool(name="memory")
                log_info("[LoadTools] ✅ Loaded MemoryTool")

            elif tool_name == "web_search":
                from .web_search import WebSearchTool
                tools["web_search"] = WebSearchTool(name="web_search")
                log_info("[LoadTools] ✅ Loaded WebSearchTool")
            
            else:
                log_warn(f"[LoadTools] ⚠️ Unknown tool requested: '{tool_name}'")

        except Exception as e:
            log_error(f"LoadTools] ❌ Failed to load tool '{tool_name}': {e}")

    return tools
