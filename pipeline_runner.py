# pipeline_runner.py

import os
from agents.summariser_agent.summariser_agent import SummariserAgent
from agents.writer_agent.writer_agent import WriterAgent
from tools.memory import MemoryTool
from utils.logger import log_info, log_error

# 👇 Define constants at top-level
TASK_ID = "pipeline_test_001"
PAPER_ID = "attention_is_all_you_need"
PDF_PATH = "sample_data/attention_is_all_you_need.pdf"
TITLE = "Attention Is All You Need"
URL = "https://arxiv.org/abs/1706.03762"


def run_pipeline():
    log_info("🚀 Starting full pipeline...")

    # ✅ Check file exists
    if not os.path.exists(PDF_PATH):
        log_error(f"❌ PDF not found at: {PDF_PATH}")
        return

    # 🔹 Step 1: Summarise the paper
    summariser = SummariserAgent(task_id=TASK_ID)
    summary_input = {
        "pdfs": [
            {
                "title": TITLE,
                "url": URL,
                "file_path": PDF_PATH
            }
        ]
    }
    summary_output = summariser.run(summary_input)
    summaries = summary_output.get("summaries", [])

    if not summaries:
        log_error("❌ No summaries returned. Exiting.")
        return

    # 🔹 Step 2: Store summary in shared memory
    memory = MemoryTool()
    try:
        summary_item = summaries[0]
        store_result = memory.run({
            "action": "write",
            "paper_id": PAPER_ID,
            "key": "summary",
            "data": summary_item["summary"]
        })
        if store_result.get("status") != "success":
            raise Exception("Failed to store summary")
    except Exception as e:
        log_error(f"❌ Error storing summary to memory: {e}")
        return

    # 🔹 Step 3: Load summary from memory
    try:
        loaded = memory.run({
            "action": "read",
            "paper_id": PAPER_ID,
            "key": "summary"
        })
        loaded_summary = loaded.get("result")
        if not loaded_summary:
            raise Exception("Summary not found in memory")
    except Exception as e:
        log_error(f"❌ Error loading summary from memory: {e}")
        return

    # 🔹 Step 4: Compile final report
    writer = WriterAgent(task_id=TASK_ID)
    writer_input = {
        "summaries": [
            {
                "title": TITLE,
                "url": URL,
                "summary": loaded_summary
            }
        ]
    }
    report_output = writer.run(writer_input)

    if report_output.get("report_path"):
        log_info(f"📄 Final report saved at: {report_output['report_path']}")
    else:
        log_error("❌ Report generation failed.")

    log_info("✅ Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
