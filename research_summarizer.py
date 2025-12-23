from genai_client import ask_gemini
from scraper import scrape_text
from search_tool import search_web

def summarize_research(topic):
    """
    Summarizes research papers on a given topic.
    """
    search_queries_prompt = f"Generate 3 precise search queries for research papers on the topic: '{topic}'. Return only the queries, one per line."
    search_queries_str = ask_gemini(search_queries_prompt)
    search_queries = [q.strip() for q in search_queries_str.split('\n') if q.strip()]

    scraped_content = ""
    search_results_for_display = []
    if search_queries:
        for query in search_queries:
            search_results = search_web(query, max_results=3)
            for r in search_results:
                if r.get('href'):
                    content = scrape_text(r['href'])
                    if content:
                        scraped_content += content + "\n\n"
                        search_results_for_display.append(r)

    if not scraped_content.strip():
        return "Could not find enough information to summarize the research.", []

    summary_prompt = f"""
Based on the following research content, provide a comprehensive summary of the research on '{topic}'. The summary should be well-structured, informative, and easy to understand.

{scraped_content}

Format the output as follows:

### Summary of the Research on {topic}

**Introduction:**
<A brief introduction to the topic and the scope of the research.>

**Key Findings:**
<A list of the most important findings from the research papers.>

**Methodology:**
<A brief overview of the methodologies used in the research.>

**Conclusion:**
<A summary of the main conclusions and implications of the research.>

**Further Research:**
<Suggestions for future research directions.>
"""
    summary = ask_gemini(summary_prompt)
    return summary, search_results_for_display
