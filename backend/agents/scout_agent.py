import os
from groq import Groq
from models import VentureBrief
from tools.apify_tools import run_competitor_search
from tools.exa_tools import search_similar_products
from tools.agent_staffing_tools import query_market_research, query_competitor_analysis, query_market_validation


async def run_scout_task(brief: VentureBrief) -> VentureBrief:
    """
    Execute market validation research.
    Returns updated VentureBrief with market intelligence.
    """
    competitor_data = run_competitor_search(brief.idea)
    similar_products = search_similar_products(brief.idea)
    
    # Query Agent Staffing Agency API for enhanced research
    agent_research = None
    competitor_analysis = None
    market_validation = None
    
    try:
        # Get general market research
        market_result = await query_market_research(f"Market analysis for: {brief.idea}")
        if market_result.get("success"):
            agent_research = market_result.get("data")
        
        # Get competitor analysis
        competitor_result = await query_competitor_analysis(f"Competitor analysis for: {brief.idea}")
        if competitor_result.get("success"):
            competitor_analysis = competitor_result.get("data")
        
        # Get market validation
        validation_result = await query_market_validation(f"Validate this business idea: {brief.idea}")
        if validation_result.get("success"):
            market_validation = validation_result.get("data")
            
    except Exception as e:
        print(f"Agent Staffing API error: {e}")
        # Continue without Agent Staffing data if API fails
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Build context from Agent Staffing Agency API
    agent_context = ""
    if agent_research:
        agent_context += f"\n\nMarket Research (Agent Staffing Agency):\n{agent_research}"
    if competitor_analysis:
        agent_context += f"\n\nCompetitor Analysis (Agent Staffing Agency):\n{competitor_analysis}"
    if market_validation:
        agent_context += f"\n\nMarket Validation (Agent Staffing Agency):\n{market_validation}"
    
    prompt = f"""Analyze this business idea and research data:

Idea: {brief.idea}

Competitor Search Results:
{competitor_data.get('results', [])}

Similar Products (Exa):
{similar_products.get('results', [])}{agent_context}

Generate:
1. market_summary: 2-3 sentences about the market opportunity
2. market_size: Short string like "~$40B globally"
3. tagline: One short punchy line describing the product, under 10 words
4. competitors: List top 3 competitor names only (just company names, no descriptions)
5. differentiation: 1 sentence explaining how this idea could differentiate
6. viability_score: Integer 0-100 using this logic:
   - Start at 50
   - Add up to +20 for clear monetization potential
   - Add up to +15 for trending market signals
   - Add up to +15 for low direct competition
   - Subtract up to -20 for saturated markets
   - Subtract up to -15 for unclear monetization

Return ONLY valid JSON with keys: market_summary, market_size, tagline, competitors (array of 3 strings), differentiation, viability_score"""

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
    brief.market_size = result["market_size"]
    brief.tagline = result["tagline"]
    brief.competitors = result["competitors"][:3]
    brief.differentiation = result["differentiation"]
    brief.viability_score = result["viability_score"]
    
    return brief
