import os
import httpx
from typing import Dict, Any, Optional


class AgentStaffingAPI:
    """Client for the Agent Staffing Agency API."""
    
    def __init__(self):
        self.base_url = os.getenv("AGENT_STAFFING_API_URL", "https://noel-argumentatious-tomika.ngrok-free.dev")
        self.plan_id = os.getenv("AGENT_STAFFING_PLAN_ID", "66865841526873856749601918817346860702290875391909441726439397882859395830112")
        self.nvm_api_key = os.getenv("NVM_API_KEY")
    
    async def try_free_endpoint(self, query: str) -> Dict[str, Any]:
        """
        Call the free /try endpoint.
        Returns the API response or error information.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/try",
                    headers={
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "true"
                    },
                    json={"query": query}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def compare_sellers(self, query: str) -> Dict[str, Any]:
        """
        Call the /compare endpoint to get results from top 3 sellers.
        Returns the API response or error information.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/compare",
                    headers={
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "true"
                    },
                    json={"query": query}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def ask_mindra(self, query: str) -> Dict[str, Any]:
        """
        Call the /ask-mindra endpoint for orchestrated execution through Mindra.
        Returns the API response or error information.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/ask-mindra",
                    headers={
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "true"
                    },
                    json={"query": query}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def get_seller_status(self) -> Dict[str, Any]:
        """
        Call the /alive endpoint to check which sellers are currently up.
        Returns the API response or error information.
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/alive",
                    headers={"ngrok-skip-browser-warning": "true"}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def get_sellers_catalog(self) -> Dict[str, Any]:
        """
        Call the /sellers endpoint to get the full catalog with quality scores.
        Returns the API response or error information.
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/sellers",
                    headers={"ngrok-skip-browser-warning": "true"}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    async def ask_with_auth(self, query: str, access_token: str) -> Dict[str, Any]:
        """
        Call the paid /ask endpoint with authorization.
        Requires a valid access token from the Nevermined payment system.
        Returns the API response or error information.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/ask",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={"query": query}
                )
                response.raise_for_status()
                return {"success": True, "data": response.json()}
        except httpx.HTTPError as e:
            return {"success": False, "error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}


def create_agent_staffing_client() -> AgentStaffingAPI:
    """
    Factory function to create an Agent Staffing API client.
    Returns a configured client instance.
    """
    return AgentStaffingAPI()


async def query_market_research(query: str) -> Dict[str, Any]:
    """
    Query the Agent Staffing Agency API for market research.
    Uses the free /try endpoint by default.
    Returns the research data or error information.
    """
    client = create_agent_staffing_client()
    result = await client.try_free_endpoint(query)
    
    if not result["success"]:
        # Fallback to compare endpoint if try fails
        result = await client.compare_sellers(query)
    
    return result


async def query_competitor_analysis(query: str) -> Dict[str, Any]:
    """
    Query the Agent Staffing Agency API for competitor analysis.
    Uses the /compare endpoint to get multiple perspectives.
    Returns the analysis data or error information.
    """
    client = create_agent_staffing_client()
    return await client.compare_sellers(query)


async def query_market_validation(query: str) -> Dict[str, Any]:
    """
    Query the Agent Staffing Agency API for market validation.
    Uses the /ask-mindra endpoint for orchestrated execution.
    Returns the validation data or error information.
    """
    client = create_agent_staffing_client()
    return await client.ask_mindra(query)
