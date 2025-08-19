from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import uuid
from tools.load_tools import load_tools
from utils.logger import log_info


class BaseAgent(ABC):
    """
    Abstract base class for agents.

    Each agent has:
      - name: readable agent name
      - task_id: unique identifier for a run
      - tools: optional dict of loaded tools (via load_tools)
    """

    def __init__(
        self,
        name: Optional[str] = None,
        task_id: Optional[str] = None,
        tool_names: Optional[List[str]] = None,
    ):
        self.name = name or self.__class__.__name__
        self.task_id = task_id or str(uuid.uuid4())
        self.tools: Dict[str, Any] = load_tools(use=tool_names or [])

        log_info(f"[BaseAgent] Initialized agent '{self.name}' (task_id={self.task_id})")

    def get_tool(self, tool_name: str) -> Any:
        """
        Return a tool instance by name or raise ValueError.
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not loaded for agent '{self.name}'")
        return self.tools[tool_name]

    def list_tools(self) -> List[str]:
        """
        List tool names loaded for this agent.
        """
        return list(self.tools.keys())

    def log(self, message: str) -> None:
        """
        Log a message prefixed with agent name.
        """
        log_info(f"[{self.name}] {message}")

    @abstractmethod
    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main agent execution method.
        Must be implemented by subclasses.
        """
        raise NotImplementedError
