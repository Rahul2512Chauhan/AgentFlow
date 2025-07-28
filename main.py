# main.py
from agents.search_agent.search_agent import SearchAgent
from agents.pdf_downloader_agent.pdf_downloader_agent import PDFDownloaderAgent
from utils.logger import log_info
from rich import print
import sys

def main():
    log_info("SearchAgent initialized.")
    search_agent = SearchAgent()

    # Accept input from CLI
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("🔍 Enter your research query: ")

    input_dict = {"query": query}
    search_output = search_agent.run(input_dict)

    print("\n[bold green]🔎 SearchAgent Output:[/bold green]")
    for i, res in enumerate(search_output.get("results", []), 1):
        print(f"\n[bold cyan]Result {i}[/bold cyan]")
        print(f"[bold]Title:[/bold] {res['title']}")
        print(f"[bold]URL:[/bold] {res['url']}")
        print(f"[bold]Summary:[/bold] {res['summary'][:300]}...")

    if not search_output["results"]:
        print("[yellow]No results found or an error occurred.[/yellow]")
        return

    # ✅ Pass results to PDFDownloaderAgent
    downloader = PDFDownloaderAgent()
    download_output = downloader.run(search_output)

    print("\n[bold green]📄 Downloaded PDFs:[/bold green]")
    for pdf in download_output.get("pdfs", []):
        print(f"[bold cyan]{pdf['title']}[/bold cyan] — Saved at: {pdf['pdf_path']}")

if __name__ == "__main__":
    main()
