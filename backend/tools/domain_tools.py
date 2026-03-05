import os
import requests


def generate_domain_candidates(brand_name: str) -> list[str]:
    """
    Generate 3 domain name candidates from a brand name.
    Returns .com, .io, and get{brand} variants.
    """
    clean_name = brand_name.lower().replace(" ", "").replace("-", "")
    return [
        f"{clean_name}.com",
        f"{clean_name}.io",
        f"get{clean_name}.com",
    ]


def check_domain_availability(domain: str) -> dict:
    """
    Check if a domain is available via Namecheap API.
    In DEMO_MODE, simulates availability check on API failure.
    Returns domain name and availability boolean.
    """
    try:
        demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
        api_key = os.getenv("NAMECHEAP_API_KEY")
        api_user = os.getenv("NAMECHEAP_API_USER")
        
        if not api_key or not api_user:
            if demo_mode:
                return {"domain": domain, "available": True}
            return {"error": "Missing Namecheap credentials", "domain": domain, "available": False}
        
        url = "https://api.namecheap.com/xml.response"
        params = {
            "ApiUser": api_user,
            "ApiKey": api_key,
            "UserName": api_user,
            "Command": "namecheap.domains.check",
            "ClientIp": "127.0.0.1",
            "DomainList": domain,
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        available = "Available=\"true\"" in response.text
        return {"domain": domain, "available": available}
    
    except Exception as e:
        demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
        if demo_mode:
            return {"domain": domain, "available": True}
        return {"error": str(e), "domain": domain, "available": False}
