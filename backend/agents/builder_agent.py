import os
from crewai import Agent
from groq import Groq
from models import VentureBrief
from tools.stripe_tools import create_payment_link
from tools.vercel_tools import deploy_landing_page


def create_builder_agent() -> Agent:
    """Create the Builder agent for landing page creation and deployment."""
    return Agent(
        role="Product Builder",
        goal="Create and deploy compelling landing pages with payment integration",
        backstory="Expert at translating product vision into high-converting web experiences",
        verbose=True,
        allow_delegation=False,
    )


def run_builder_task(brief: VentureBrief) -> VentureBrief:
    """
    Generate landing page, integrate Stripe, and deploy to Vercel.
    Returns updated VentureBrief with live URL and payment link.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Generate landing page copy for this product:

Brand: {brief.brand_name}
Idea: {brief.idea}
Differentiation: {brief.differentiation}

Generate:
- headline: Compelling main headline (under 60 chars)
- subheadline: Supporting text (under 120 chars)
- feature1, feature2, feature3: Three benefit bullets (each under 80 chars)
- cta_label: Call-to-action button text (under 20 chars)
- social_proof: One credibility line (under 100 chars)

Return ONLY valid JSON with these exact keys."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    copy = json.loads(response.choices[0].message.content)
    
    template_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "landing_page.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    payment_result = create_payment_link(brief.brand_name, 2900)
    payment_url = payment_result.get("payment_link_url", "#")
    
    html = html.replace("{{brand_name}}", brief.brand_name)
    html = html.replace("{{headline}}", copy["headline"])
    html = html.replace("{{subheadline}}", copy["subheadline"])
    html = html.replace("{{feature1}}", copy["feature1"])
    html = html.replace("{{feature2}}", copy["feature2"])
    html = html.replace("{{feature3}}", copy["feature3"])
    html = html.replace("{{cta_label}}", copy["cta_label"])
    html = html.replace("{{cta_url}}", payment_url)
    html = html.replace("{{social_proof}}", copy["social_proof"])
    
    deploy_result = deploy_landing_page(html, brief.brand_name)
    
    brief.landing_page_url = deploy_result.get("url")
    brief.stripe_payment_link = payment_url
    
    return brief
