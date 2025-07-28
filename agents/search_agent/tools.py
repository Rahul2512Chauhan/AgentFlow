import arxiv
from typing import List , Dict
from utils.logger import log_error , log_info

def search_papers(query: str ,max_results: int = 5) -> List[Dict]:
    """
    Search arXiv papers using the official API.

    Args:
        query (str): The search query, e.g. "Graph Neural Networks in healthcare".
        max_results (int): Number of top results to return.

    Returns:
        List[Dict]: A list of search results with title, summary, and URL.
    """

    log_info(f"Searching arXiv for query: '{query}' (Top {max_results})")

    try:
        #create the arxiv query
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )

        results=[]        
        for result in search.results():
            paper = {
                "title": result.title.strip(),
                "summary": result.summary.strip(),
                "url": result.entry_id,  # Link to abstract
                "pdf_url": result.pdf_url,
                "authors": [author.name for author in result.authors],
                "published": result.published.strftime("%Y-%m-%d") 
            }

            results.append(paper)

        log_info(f"Found {len(results)} result(s) from arXiv")
        return results
    
    except Exception as e:
        log_error(f"Error during arXiv search: {e}")
        return []


if __name__ == "__main__":
    results = search_papers("LLMs in education", max_results=3)
    for r in results:
        print(r["title"], "→", r["url"])
