import os
import requests


def search_similar_products(idea: str) -> dict:
    """
    Search for semantically similar products using Exa API.
    Uses autoprompt for better semantic matching.
    Returns top 5 results with title, url, and summary.
    """
    try:
        api_key = os.getenv("EXA_API_KEY")
        url = "https://api.exa.ai/search"
        
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
            },
            json={
                "query": idea,
                "useAutoprompt": True,
                "numResults": 5,
                "contents": {"summary": True},
            },
            timeout=30,
        )
        response.raise_for_status()
        
        data = response.json()
        results = [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "summary": r.get("summary", ""),
            }
            for r in data.get("results", [])
        ]
        
        return {"results": results}
    
    except Exception as e:
        return {"error": str(e), "results": []}
