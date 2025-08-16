# agents/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional ,List
from tools.base import BaseTool
from tools.load_tools import load_tools
import uuid

class BaseAgent(ABC):
    """
    Abstract base class for tool-using agents.
    """

    def __init__(
        self, 
        name: Optional[str] = None,
        task_id: Optional[str] = None, 
        tool_names: Optional[List[str]] = None,
    ):
         
        self.task_id = task_id or str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self.tools: Dict[str, BaseTool] = load_tools(use=tool_names or [])

    def get_tool(self, name: str) -> BaseTool:
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not loaded for this agent.")
        return self.tools[name]

    def log(self, message: str) -> None:
        print(f"[{self.name}] {message}")

    @abstractmethod
    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main agent execution method.
        Must be implemented by subclasses.
        """
        pass
