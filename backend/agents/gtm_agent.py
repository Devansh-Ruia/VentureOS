import os
from groq import Groq
from models import VentureBrief, GTMPlan
from tools.adagent_tools import run_adagent_campaign


async def run_gtm_task(brief: VentureBrief) -> VentureBrief:
    """
    Generate Week 1 go-to-market plan.
    Returns final VentureBrief with GTM strategy.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(raw)
    
    cold_email_str = f"Subject: {result['cold_email']['subject']}\n\n{result['cold_email']['body']}"
    
    brief.gtm_plan = GTMPlan(
        reddit_communities=result["reddit_communities"][:5],
        cold_email=cold_email_str,
        tweet_drafts=result["tweet_drafts"][:3],
        product_hunt_blurb=result["product_hunt_blurb"]
    )
    
    audience = brief.market_summary or "early adopters and founders"
    goal = f"Acquire first 100 customers for {brief.brand_name}"

    campaign = await run_adagent_campaign(
        brand=brief.brand_name or "",
        goal=goal,
        audience=audience,
        budget=15.0
    )

    if campaign and campaign.get("status") == "complete":
        strategy = campaign.get("strategy", {})
        brief.adagent_campaign_id = campaign.get("campaign_id")
        brief.adagent_strategy = strategy
        brief.adagent_metrics = campaign.get("metrics")
        brief.adagent_channels = strategy.get("channels", [])
        brief.adagent_messaging = strategy.get("messaging", [])
    
    return brief
