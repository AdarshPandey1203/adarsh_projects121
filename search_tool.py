from ddgs import DDGS

def search_web(query, max_results=5):
    """
    Performs a web search using DuckDuckGo and returns the results.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        return results
