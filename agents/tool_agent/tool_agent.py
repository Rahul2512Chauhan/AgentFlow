from typing import Dict , Any , Optional
from agents.base import BaseAgent
from utils.logger import log_error, log_info

class ToolAgent(BaseAgent):
    """
    General-purpose agent that can call tools dynamically.
    Example:
        input = {"tool": "pdf_parser", "args": {"pdf_path": "data/papers/x.pdf"}}
        output = agent.run(input)
    """

    def __init__(self, name: Optional[str] = None, task_id: Optional[str] = None, tool_names=None):
        super().__init__(name=name or "ToolAgent", task_id=task_id, tool_names=tool_names)

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a tool call based on input dict.

        Expected input:
          {
              "tool": "<tool_name>",
              "args": { ... }
          }
        """
        tool_name = input.get("tool")
        tool_args = input.get("args", {})

        if not tool_name:
            return {"status": "error", "message": "No tool specified in input."}

        try:
            tool = self.get_tool(tool_name)
            self.log(f"🔧 Running tool '{tool_name}' with args={tool_args}...")
            result = tool.run(tool_args)
            self.log(f"Tool '{tool_name}' completed successfully.")
            return {"status": "success", "tool": tool_name, "result": result}

        except Exception as e:
            log_error(f"[ToolAgent]  Failed running tool '{tool_name}': {str(e)}")
            return {"status": "error", "tool": tool_name, "message": str(e)}
