import os
from groq import Groq
from models import VentureBrief
from tools.apify_tools import run_competitor_search
from tools.exa_tools import search_similar_products


async def run_scout_task(brief: VentureBrief) -> VentureBrief:
    """
    Execute market validation research.
    Returns updated VentureBrief with market intelligence.
    """
    competitor_data = run_competitor_search(brief.idea)
    similar_products = search_similar_products(brief.idea)
    
    # Query external Nevermined research agent if configured
    external_data = None
    try:
        from nevermined.buyer import query_external_research_agent
        external_data = await query_external_research_agent(brief.idea)
    except ImportError:
        pass
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    external_context = f"\n\nExternal Research Data:\n{external_data}" if external_data else ""
    
    prompt = f"""Analyze this business idea and research data:

Idea: {brief.idea}

Competitor Search Results:
{competitor_data.get('results', [])}

Similar Products (Exa):
{similar_products.get('results', [])}{external_context}

Generate:
1. market_summary: 2-3 sentences about the market opportunity
2. competitors: List top 3 competitor names only (just company names, no descriptions)
3. differentiation: 1 sentence explaining how this idea could differentiate
4. viability_score: Integer 0-100 using this logic:
   - Start at 50
   - Add up to +20 for clear monetization potential
   - Add up to +15 for trending market signals
   - Add up to +15 for low direct competition
   - Subtract up to -20 for saturated markets
   - Subtract up to -15 for unclear monetization

Return ONLY valid JSON with keys: market_summary, competitors (array of 3 strings), differentiation, viability_score"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(raw)
    
    brief.market_summary = result["market_summary"]
    brief.competitors = result["competitors"][:3]
    brief.differentiation = result["differentiation"]
    brief.viability_score = result["viability_score"]
    
    return brief
