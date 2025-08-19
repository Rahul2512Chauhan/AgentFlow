import os
import json
from utils.logger import log_info, log_error
from agents.base import BaseAgent
from utils.llm import call_llm  # 🔹 assumes you have utils/llm.py wrapper

CACHE_FILE = "data/cache/planner_cache.json"


class PlannerAgent(BaseAgent):
    def __init__(self, name=None, task_id=None, reset_cache: bool = False):
        super().__init__(name=name or "PlannerAgent", task_id=task_id)

        # ensure cache dir exists
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

        self.cache_file = CACHE_FILE
        self.reset_cache = reset_cache

        # handle reset cache
        if self.reset_cache and os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            log_info("[PlannerAgent] 🗑️ Cache cleared.")

        # load cache if exists
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2)

    def run(self, input: dict) -> dict:
        """
        Generate workflow plan for an instruction.
        """
        instruction = input.get("instruction")
        num_papers = input.get("num_papers", 3)

        if not instruction:
            return {"status": "error", "message": "No instruction provided"}

        cache_key = f"{instruction.lower()}::{num_papers}"

        # 🔹 Check cache
        if cache_key in self.cache:
            log_info(f"[PlannerAgent] ⚡ Using cached workflow for: '{instruction}'")
            return self.cache[cache_key]

        # 🔹 Otherwise generate workflow
        log_info(f"[PlannerAgent] 🧠 Creating new workflow for instruction: '{instruction}'")

        prompt = f"""
        You are PlannerAgent. Convert this user instruction into a step-by-step agent workflow.
        Instruction: "{instruction}"
        Num papers: {num_papers}

        Use ONLY these agents: SearchAgent, PDFDownloaderAgent, SummariserAgent, WriterAgent.
        Always respond in strict JSON format like this:

        {{
            "workflow": [
                {{"agent": "SearchAgent", "params": {{"query": "...", "max_results": ...}}}},
                {{"agent": "PDFDownloaderAgent", "params": {{}}}},
                {{"agent": "SummariserAgent", "params": {{}}}},
                {{"agent": "WriterAgent", "params": {{}}}}
            ],
            "num_papers": {num_papers}
        }}
        """

        try:
            llm_response = call_llm(prompt)
            workflow = json.loads(llm_response)
            log_info("[PlannerAgent] ✅ Workflow generated via LLM.")
        except Exception as e:
            log_error(f"[PlannerAgent] ❌ Failed LLM planning, falling back. Error: {e}")

            workflow = {
                "workflow": [
                    {"agent": "SearchAgent", "params": {"query": instruction, "max_results": num_papers}},
                    {"agent": "PDFDownloaderAgent", "params": {}},
                    {"agent": "SummariserAgent", "params": {}},
                    {"agent": "WriterAgent", "params": {}}
                ],
                "num_papers": num_papers
            }

        # store in cache
        self.cache[cache_key] = workflow
        self._save_cache()

        return workflow
