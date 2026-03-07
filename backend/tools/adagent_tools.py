import os
import httpx

ADAGENT_ENDPOINT = "https://adagent-studio-seven.vercel.app/api/run-campaign"


async def run_adagent_campaign(
    brand: str,
    goal: str,
    audience: str,
    budget: float = 15.0
) -> dict | None:
    access_token = os.getenv("NVM_ADAGENT_ACCESS_TOKEN")
    if not access_token:
        return None

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                ADAGENT_ENDPOINT,
                headers={
                    "Content-Type": "application/json",
                    "payment-signature": access_token
                },
                json={
                    "brand": brand,
                    "goal": goal,
                    "audience": audience,
                    "budget": budget
                }
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception:
        return None
