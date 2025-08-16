import os
from agents.base import BaseAgent
from utils.logger import log_error, log_info, log_warn
from agents.summariser_agent.tools import summarise_text, extract_text_from_pdf
from typing import Dict, List, Any


class SummariserAgent(BaseAgent):
    def __init__(self, task_id: str | None = None):
        super().__init__(name="SummariserAgent",task_id=task_id, tool_names=[])
        log_info("SummariserAgent initialized.")

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        pdfs: List[Dict[str, Any]] = input.get("pdfs", [])
        if not pdfs:
            log_warn("No PDFs found in input.")
            return {"summaries": []}

        log_info(f"Summarising {len(pdfs)} PDFs...")
        summaries = []

        for i, pdf in enumerate(pdfs, start=1):
            title = pdf.get("title", f"untitled-{i}")
            file_path = pdf.get("file_path")

            if not file_path or not os.path.exists(file_path):
                log_warn(f"[{i}] Invalid or missing file path for: {title}")
                continue

            try:
                text = extract_text_from_pdf(file_path)
                if not text:
                    log_warn(f"[{i}] No text extracted from: {title}")
                    continue

                log_info(f"[{i}] Summarising: {title}")
                summary = summarise_text(text)
                if not summary:
                    log_warn(f"[{i}] Empty summary for: {title}")
                    continue
                summary_path = os.path.splitext(file_path)[0] + ".summary.txt"

                try:
                    with open(summary_path, "w", encoding="utf-8") as f:
                        f.write(summary)
                    log_info(f"[{i}] ✅ Summary saved to: {summary_path}")
                except Exception as file_error:
                    log_warn(f"[{i}] ⚠️ Could not save summary: {file_error}")
                pdf["summary"] = summary
                pdf["summary_path"] = summary_path
                summaries.append(pdf)
                log_info(f"[{i}] ✅ Summarised: {title}")

            except Exception as e:
                log_error(f"[{i}] ❌ Failed to summarise '{title}': {e}")

        log_info(f"✅ Generated summaries for {len(summaries)} / {len(pdfs)} PDFs.")
        return {"summaries": summaries}
