import os
from crewai import Agent
from anthropic import Anthropic
from models import VentureBrief, GTMPlan


def create_gtm_agent() -> Agent:
    """Create the GTM agent for go-to-market strategy."""
    return Agent(
        role="Growth Strategist",
        goal="Design actionable Week 1 go-to-market plans for new products",
        backstory="Expert at identifying high-leverage distribution channels and crafting compelling messaging",
        verbose=True,
        allow_delegation=False,
    )


def run_gtm_task(brief: VentureBrief) -> VentureBrief:
    """
    Generate Week 1 go-to-market plan.
    Returns final VentureBrief with GTM strategy.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    prompt = f"""Create a Week 1 go-to-market plan for this product:

Brand: {brief.brand_name}
Idea: {brief.idea}
Differentiation: {brief.differentiation}
Landing Page: {brief.landing_page_url}

Generate:
1. reddit_communities: Array of 5 subreddit names (no r/ prefix, just names)
2. cold_email: Object with "subject" and "body" (body under 150 words total)
3. tweet_drafts: Array of exactly 3 tweets (each under 280 chars)
4. product_hunt_blurb: Single string under 200 chars

All content must be specific to THIS product. No generic marketing language.

Return ONLY valid JSON with structure:
{{
  "reddit_communities": ["subreddit1", "subreddit2", ...],
  "cold_email": {{"subject": "...", "body": "..."}},
  "tweet_drafts": ["tweet1", "tweet2", "tweet3"],
  "product_hunt_blurb": "..."
}}"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    result = json.loads(response.content[0].text)
    
    cold_email_str = f"Subject: {result['cold_email']['subject']}\n\n{result['cold_email']['body']}"
    
    brief.gtm_plan = GTMPlan(
        reddit_communities=result["reddit_communities"][:5],
        cold_email=cold_email_str,
        tweet_drafts=result["tweet_drafts"][:3],
        product_hunt_blurb=result["product_hunt_blurb"]
    )
    
    return brief
