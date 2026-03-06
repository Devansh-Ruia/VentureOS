import os
from groq import Groq
from models import VentureBrief
from tools.stripe_tools import create_payment_link
from tools.vercel_tools import deploy_landing_page


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
    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    copy = json.loads(raw)
    
    template_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "landing_page.html")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    payment_result = create_payment_link(brief.brand_name, 2900)
    payment_url = payment_result.get("payment_link_url", "#")
    
    html = html.replace("{{brand_name}}", brief.brand_name or "")
    html = html.replace("{{headline}}", copy.get("headline", ""))
    html = html.replace("{{subheadline}}", copy.get("subheadline", ""))
    html = html.replace("{{feature_1}}", copy.get("feature1", copy.get("feature_1", "")))
    html = html.replace("{{feature_2}}", copy.get("feature2", copy.get("feature_2", "")))
    html = html.replace("{{feature_3}}", copy.get("feature3", copy.get("feature_3", "")))
    html = html.replace("{{cta_label}}", copy.get("cta_label", "Get Started"))
    html = html.replace("{{cta_url}}", payment_url)
    html = html.replace("{{social_proof}}", copy.get("social_proof", ""))
    
    deploy_result = deploy_landing_page(html, brief.brand_name)
    
    brief.landing_page_url = deploy_result.get("url")
    brief.stripe_payment_link = payment_url
    
    return brief
