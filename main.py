from agents.search_agent.search_agent import SearchAgent
from agents.pdf_downloader_agent.pdf_downloader_agent import PDFDownloaderAgent
from agents.summariser_agent.summariser_agent import SummariserAgent
from utils.logger import log_info

import sys

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "Large Language Models in Healthcare"
    log_info("Starting pipeline...")

    # Step 1: Search
    search_agent = SearchAgent()
    search_results = search_agent.run({"query": query})

    if not search_results.get("results"):
        log_info("No results from SearchAgent.")
        return

    # Step 2: Download PDFs (✅ FIX: pass correct key 'results')
    pdf_agent = PDFDownloaderAgent()
    pdfs = pdf_agent.run({"results": search_results["results"]})

    if not pdfs.get("pdfs"):
        log_info("No PDFs downloaded. Exiting.")
        return

    # Step 3: Summarise PDFs
    summariser = SummariserAgent()
    summaries = summariser.run(pdfs)

    log_info("✅ Pipeline complete!")
    for i, summary in enumerate(summaries["summaries"], 1):
        print(f"\n📄 Summary {i}: {summary['title']}\n{summary['summary']}\n")

if __name__ == "__main__":
    main()
