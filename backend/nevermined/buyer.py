"""VentureOS Nevermined Buyer Agent Logic."""
import os
import httpx
from typing import Optional
from nevermined.seller import get_payments_instance


async def query_external_research_agent(idea: str) -> Optional[dict]:
    """
    Purchase and query external Nevermined research agent.
    Returns research data or None if not configured or on error.
    """
    agent_id = os.getenv("NVM_RESEARCH_AGENT_ID")
    plan_id = os.getenv("NVM_RESEARCH_PLAN_ID")
    
    if not agent_id or not plan_id:
        return None
    
    try:
        payments = get_payments_instance()
        
        # Check balance and purchase if needed
        balance = payments.ai_query_api.get_plan_balance(plan_id)
        if balance == 0:
            payments.ai_query_api.order_plan(plan_id)
        
        # Get access token
        access_token = payments.ai_query_api.get_service_token(agent_id=agent_id)
        
        # Get agent endpoint
        agent_details = payments.ai_query_api.get_agent_details(agent_id)
        endpoints = agent_details.get("endpoints", [])
        agent_url = endpoints[0].get("POST", "") if endpoints else ""
        
        if not agent_url:
            return None
        
        # Call external agent
        async with httpx.AsyncClient() as client:
            response = await client.post(
                agent_url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json={"query": idea},
                timeout=20.0
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
            
    except Exception as e:
        print(f"External research agent error: {e}")
        return None
