import sys
from agents.search_agent.search_agent import SearchAgent
from agents.pdf_downloader_agent.pdf_downloader_agent import PDFDownloaderAgent
from agents.summariser_agent.summariser_agent import SummariserAgent
from agents.writer_agent.writer_agent import WriterAgent
from utils.logger import log_info

def main(query: str):
    log_info("Starting pipeline...")

    # 1. Search relevant papers
    search_agent = SearchAgent()
    search_output = search_agent.run({"query": query})

    # 2. Download PDFs
    pdf_downloader = PDFDownloaderAgent()
    pdf_output = pdf_downloader.run(search_output)

    # 3. Summarise PDFs
    summariser = SummariserAgent()
    summary_output = summariser.run(pdf_output)

    # 4. Compile summaries into final report
    writer = WriterAgent()
    report_output = writer.run(summary_output)

    # ✅ Done
    log_info("✅ Pipeline complete!")
    if report_output.get("report_path"):
        log_info(f"📄 Final report saved at: {report_output['report_path']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your-query>'")
        sys.exit(1)

    query = sys.argv[1]
    main(query)
