import os
from datetime import datetime
from typing import Dict, Any, List
from agents.base import BaseAgent
from utils.logger import log_error, log_info, log_warn

class WriterAgent(BaseAgent):
    def __init__(self, task_id: str | None = None):
        super().__init__(name="WriterAgent" , task_id=task_id, tool_names=[])
        self.output_dir = "data/reports"
        os.makedirs(self.output_dir, exist_ok=True)
        log_info("WriterAgent initialized.")

    def run(self, input: Dict[str, Any]) -> Dict[str, Any]:
        summaries: List[Dict[str, Any]] = input.get("summaries", [])
        if not summaries:
            log_warn("[Writer] No summaries found in input.")
            return {"report": "", "report_path": None}

        log_info(f"[Writer] Generating report for {len(summaries)} summaries...")

        date_str = datetime.now().strftime("%Y-%m-%d")
        report_lines: List[str] = []

        # Header
        report_lines.append("📘 Multi-Paper Summary Report")
        report_lines.append(f"Date: {date_str}")
        report_lines.append(f"Number of Papers: {len(summaries)}")
        report_lines.append("\n" + "─" * 40 + "\n")

        for idx, paper in enumerate(summaries, start=1):
            title = paper.get("title", f"Paper #{idx}")
            url = paper.get("url", "URL not available")
            summary = paper.get("summary")

            if not summary:
                log_warn(f"[Writer] Skipping '{title}' — summary missing.")
                continue

            report_lines.append(f"{idx}. 📝 Title: {title}")
            report_lines.append(f"🔗 URL: {url}\n")
            report_lines.append("Summary:\n")
            report_lines.append(summary.strip())
            report_lines.append("\n" + "─" * 40 + "\n")

        final_report = "\n".join(report_lines)

        # Save report
        report_path = os.path.join(self.output_dir, f"{date_str}_report.txt")
        
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write(final_report)
            log_info(f"[Writer] ✅ Report saved to: {report_path}")
        
        except Exception as e:
            log_error(f"[Writer] ❌ Failed to save report — {e}")
            report_path = None

        return {
            "report": final_report,
            "report_path": report_path
        }
