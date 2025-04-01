from duckduckgo_search import DDGS
import trafilatura

def web_search(query: str, num_results: int = 3):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region='wt-wt', safesearch='moderate', max_results=num_results):
            url = r.get("href")
            title = r.get("title", "")
            if url:
                downloaded = trafilatura.fetch_url(url)
                content = trafilatura.extract(downloaded)
                if content:
                    results.append(f"{title}\n{content[:1000]}...")  # Keep it short
    return results
