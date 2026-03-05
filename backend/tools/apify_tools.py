import os
from apify_client import ApifyClient


def run_competitor_search(idea: str) -> dict:
    """
    Search for competitors using Apify Google Search Scraper.
    Queries ProductHunt and Crunchbase for similar products.
    Returns top 5 results with title, url, and description.
    """
    try:
        client = ApifyClient(os.getenv("APIFY_API_TOKEN"))
        query = f"{idea} competitors site:producthunt.com OR site:crunchbase.com"
        
        run = client.actor("apify/google-search-scraper").call(
            run_input={
                "queries": query,
                "maxPagesPerQuery": 1,
                "resultsPerPage": 5,
            }
        )
        
        results = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
            })
            if len(results) >= 5:
                break
        
        return {"results": results}
    
    except Exception as e:
        return {"error": str(e), "results": []}
