import os
import json
from typing import Dict, Any, Optional
from tools.base import BaseTool
from utils.logger import log_info, log_warn


class MemoryTool(BaseTool):
    def __init__(self, name: str = "MemoryTool"):  # ✅ Accept `name` for compatibility
        super().__init__(name)
        self.memory_file = "data/shared_memory.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump({}, f)

    def _read_memory(self) -> Dict[str, Dict[str, Any]]:
        with open(self.memory_file, "r") as f:
            return json.load(f)

    def _write_memory(self, memory: Dict[str, Dict[str, Any]]) -> None:
        with open(self.memory_file, "w") as f:
            json.dump(memory, f, indent=2)

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        action: Optional[str] = input.get("action")
        paper_id: Optional[str] = input.get("paper_id")
        key: Optional[str] = input.get("key")

        # 🚨 Enforce non-None + type-safety
        if not isinstance(action, str) or not isinstance(paper_id, str) or not isinstance(key, str):
            log_warn("[MemoryTool] ❌ Invalid 'action', 'paper_id', or 'key' type.")
            return {"status": "error", "message": "Invalid input: 'action', 'paper_id', and 'key' must be strings."}

        memory = self._read_memory()

        if action == "write":
            data = input.get("data")
            if paper_id not in memory:
                memory[paper_id] = {}
            memory[paper_id][key] = data
            self._write_memory(memory)
            log_info(f"[MemoryTool] ✅ Stored key='{key}' for paper_id='{paper_id}'")
            return {"status": "success"}

        elif action == "read":
            value = memory.get(paper_id, {}).get(key)
            log_info(f"[MemoryTool] ✅ Loaded key='{key}' for paper_id='{paper_id}'")
            return {"result": value}

        else:
            log_warn(f"[MemoryTool] ❌ Unknown action: '{action}'")
            return {"status": "error", "message": "Unknown action"}
