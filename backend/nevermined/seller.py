"""VentureOS Nevermined Seller Agent Registration."""
import os
from payments_py import Payments, PaymentOptions

_payments_instance = None


def get_payments_instance():
    """Get or create singleton Payments instance."""
    global _payments_instance
    if _payments_instance is None:
        _payments_instance = Payments.get_instance(
            PaymentOptions(
                nvm_api_key=os.getenv("NVM_API_KEY"),
                environment=os.getenv("NVM_ENVIRONMENT", "sandbox")
            )
        )
    return _payments_instance


def register_ventureos_agent() -> dict:
    """
    Register VentureOS as a Nevermined seller agent.
    Returns dict with agent_id and plan_id to save in .env
    """
    payments = get_payments_instance()
    base_url = os.getenv("VENTUREOS_BASE_URL", "http://localhost:8000")
    
    # Create credits-based pricing plan (10 USDC, 1 credit)
    plan = payments.ai_query_api.create_credits_plan(
        name="VentureOS Launch Plan",
        description="1 credit per autonomous business launch",
        price=10,
        token_address=payments.ai_query_api.get_usdc_address(),
        amount_of_credits=1,
        tags=["launch", "startup", "autonomous"]
    )
    plan_id = plan["did"]
    
    # Register VentureOS agent
    agent = payments.ai_query_api.create_agent(
        name="VentureOS",
        description="Autonomous business launch agent. Input a business idea, receive a live URL, brand, and go-to-market plan.",
        service_charge_type="fixed",
        auth_type="bearer",
        amount_of_credits=1,
        min_credits_to_charge=1,
        max_credits_to_charge=1,
        endpoints=[{"POST": f"{base_url}/api/run"}],
        usage_docs=f"{base_url}/.well-known/agent.json",
        is_for_sale=True,
        sample_link="",
        tags=["launch", "startup", "autonomous", "business"]
    )
    agent_id = agent["did"]
    
    # Link agent to plan
    payments.ai_query_api.add_agent_to_plan(plan_id, agent_id)
    
    result = {"agent_id": agent_id, "plan_id": plan_id}
    
    print(f"\n✅ VentureOS registered successfully!")
    print(f"\nAdd these to your .env file:")
    print(f"NVM_AGENT_ID={agent_id}")
    print(f"NVM_PLAN_ID={plan_id}")
    
    return result


if __name__ == "__main__":
    result = register_ventureos_agent()
    print(f"\nAgent registered: {result}")
