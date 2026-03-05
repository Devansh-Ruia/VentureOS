"""VentureOS Nevermined Seller Agent Registration."""
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent.parent / ".env")

from payments_py import Payments
from payments_py import PaymentOptions
from payments_py.common.types import PlanMetadata

_payments_instance = None


def get_payments_instance() -> Payments:
    """Get or create singleton Payments instance."""
    global _payments_instance
    if _payments_instance is None:
        _payments_instance = Payments(PaymentOptions(
            nvm_api_key=os.getenv("NVM_API_KEY"),
            environment=os.getenv("NVM_ENVIRONMENT", "sandbox"),
        ))
    return _payments_instance


def register_ventureos_agent() -> dict:
    """
    Register VentureOS as a Nevermined seller agent.
    Run once. Copy the printed agent_id and plan_id into your .env.
    """
    payments = get_payments_instance()
    base_url = os.getenv("VENTUREOS_BASE_URL", "http://localhost:8000")

    # 1. Create credits-based pricing plan
    plan_metadata = PlanMetadata(
        name="VentureOS Launch Plan",
        description="1 credit per autonomous business launch",
        tags=["launch", "startup", "autonomous"],
    )
    # USDC on Arbitrum Sepolia (sandbox)
    USDC_ADDRESS = "0x75faf114eafb1BDbe2F0316DF893fd58CE46AA4d"
    price_config = payments.plans.get_erc20_price_config(
        10_000_000,          # 10 USDC (6 decimals)
        USDC_ADDRESS,
        payments.account_address,
    )
    credits_config = payments.plans.get_fixed_credits_config(100)
    plan_res = payments.plans.register_credits_plan(
        plan_metadata, price_config, credits_config
    )
    plan_id = plan_res["planId"]
    print(f"✅ Plan created: {plan_id}")

    # 2. Register VentureOS agent
    agent_metadata = {
        "name": "VentureOS",
        "description": (
            "Autonomous business launch agent. "
            "Input a business idea, receive a live URL, brand, and go-to-market plan."
        ),
        "tags": ["launch", "startup", "autonomous", "business"],
    }
    agent_api = {
        "endpoints": [{"POST": f"{base_url}/api/run"}],
        "agentDefinitionUrl": f"{base_url}/.well-known/agent.json",
    }
    agent_res = payments.agents.register_agent(
        agent_metadata,
        agent_api,
        [plan_id],
    )
    agent_id = agent_res["agentId"]
    print(f"✅ Agent created: {agent_id}")

    print(f"\nAdd these to your .env file:")
    print(f"NVM_AGENT_ID={agent_id}")
    print(f"NVM_PLAN_ID={plan_id}")

    return {"agent_id": agent_id, "plan_id": plan_id}


if __name__ == "__main__":
    result = register_ventureos_agent()
    print(f"\nDone: {result}")