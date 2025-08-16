import sys ,uuid
from agents.search_agent.search_agent import SearchAgent
from agents.pdf_downloader_agent.pdf_downloader_agent import PDFDownloaderAgent
from agents.summariser_agent.summariser_agent import SummariserAgent
from agents.writer_agent.writer_agent import WriterAgent
from utils.logger import log_info , log_warn

def main(query: str):
    task_id = str(uuid.uuid4())
    log_info("Starting pipeline...(task_id={task_id})")

    # 1. Search relevant papers
    search_agent = SearchAgent(task_id=task_id)
    search_output = search_agent.run({"query": query})
    results = search_output.get("papers", [])
    if not results:
        log_warn("No search results, Exiting early")
        return


    # 2. Download PDFs
    pdf_downloader = PDFDownloaderAgent(task_id=task_id)
    pdf_output = pdf_downloader.run({"papers": results})
    pdfs = pdf_output.get("pdfs", [])
    if not pdfs:
        log_warn("No PDFs downloaded. Exiting early")


    # 3. Summarise PDFs
    summariser = SummariserAgent(task_id=task_id)
    summary_output = summariser.run(pdf_output)
    summaries = summary_output.get("summaries", [])
    if not summaries:
        log_warn("No summaries generated . Exiting early")
        return


    # 4. Compile summaries into final report
    writer = WriterAgent(task_id=task_id)
    report_output = writer.run(summary_output)


    #  Done
    log_info("✅ Pipeline complete!")
    if report_output.get("report_path"):
        log_info(f"📄 Final report saved at: {report_output['report_path']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your-query>'")
        sys.exit(1)
    main(sys.argv[1])
