import os
import json
from typing import Dict, Any, Optional
from tools.base import BaseTool
from utils.logger import log_info, log_warn ,log_error


class MemoryTool(BaseTool):
    def __init__(self, name: str = "memory"):
        super().__init__(name)
        self.memory_file = "data/shared_memory.json"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump({}, f)


    def _read_memory(self) -> Dict[str, Dict[str, Any]]:
        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except Exception as e:
            log_error(f"[MemoryTool] ❌ Failed to read memory: {e}")
            return {}


    def _write_memory(self, memory: Dict[str, Dict[str, Any]]) -> None:
        try:
            with open(self.memory_file, "w") as f:
                json.dump(memory, f, indent=2)
        except Exception as e:
            log_error(f"[MemoryTool] ❌ Failed to write memory: {e}")


    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        action: Optional[str] = input.get("action")
        paper_id: Optional[str] = input.get("paper_id")
        key: Optional[str] = input.get("key")

        if not isinstance(action, str):
            return {"status": "error", "message": "Missing or invalid 'action' (must be string)"}
        if action not in ["write", "read", "delete", "list"]:
            return {"status": "error", "message": f"Unknown action '{action}'"}

        memory = self._read_memory()

        # 📝 Write
        if action == "write":
            if not isinstance(paper_id, str) or not isinstance(key, str):
                return {"status": "error", "message": "'paper_id' and 'key' must be strings"}
            data = input.get("data")
            if paper_id not in memory:
                memory[paper_id] = {}
            memory[paper_id][key] = data
            self._write_memory(memory)
            log_info(f"[MemoryTool] ✅ Stored key='{key}' for paper_id='{paper_id}'")
            return {"status": "success"}

        # 📖 Read
        elif action == "read":
            if not isinstance(paper_id, str) or not isinstance(key, str):
                return {"status": "error", "message": "'paper_id' and 'key' must be strings"}
            value = memory.get(paper_id, {}).get(key)
            if value is None:
                log_warn(f"[MemoryTool] ⚠️ Key='{key}' not found for paper_id='{paper_id}'")
                return {"status": "not_found", "result": None}
            log_info(f"[MemoryTool] ✅ Loaded key='{key}' for paper_id='{paper_id}'")
            return {"status": "success", "result": value}
        
        # ❌ Delete
        elif action == "delete":
            if not isinstance(paper_id, str) or not isinstance(key, str):
                return {"status": "error", "message": "'paper_id' and 'key' must be strings"}
            if paper_id in memory and key in memory[paper_id]:
                del memory[paper_id][key]
                if not memory[paper_id]:  # cleanup empty dict
                    del memory[paper_id]
                self._write_memory(memory)
                log_info(f"[MemoryTool] 🗑️ Deleted key='{key}' for paper_id='{paper_id}'")
                return {"status": "success"}
            else:
                return {"status": "not_found", "message": f"Key='{key}' not found"}

        # 📋 List
        elif action == "list":
            if not isinstance(paper_id, str):
                return {"status": "error", "message": "'paper_id' must be a string"}
            keys = list(memory.get(paper_id, {}).keys())
            log_info(f"[MemoryTool] 📋 Keys for paper_id='{paper_id}': {keys}")
            return {"status": "success", "keys": keys}

        

