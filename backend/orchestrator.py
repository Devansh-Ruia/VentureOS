from typing import AsyncGenerator
from models import VentureBrief, AgentEvent
from agents.scout_agent import run_scout_task
from agents.brand_agent import run_brand_task
from agents.builder_agent import run_builder_task
from agents.gtm_agent import run_gtm_task


async def run_venture_pipeline(idea: str) -> AsyncGenerator[AgentEvent, None]:
    """
    Execute the four-agent pipeline in sequence.
    Yields AgentEvent objects for streaming progress.
    """
    brief = VentureBrief(idea=idea)
    
    # Scout Agent
    try:
        yield AgentEvent(agent="scout", status="running")
        brief = run_scout_task(brief)
        yield AgentEvent(
            agent="scout",
            status="done",
            output={
                "market_size": brief.market_size,
                "competitors": brief.competitors,
                "differentiation": brief.differentiation
            }
        )
    except Exception as e:
        yield AgentEvent(agent="scout", status="error", output={"error": str(e)})
        return
    
    # Brand Agent
    try:
        yield AgentEvent(agent="brand", status="running")
        brief = run_brand_task(brief)
        yield AgentEvent(
            agent="brand",
            status="done",
            output={
                "brand_name": brief.brand_name,
                "domain": brief.domain,
                "tagline": brief.tagline
            }
        )
    except Exception as e:
        yield AgentEvent(agent="brand", status="error", output={"error": str(e)})
        return
    
    # Builder Agent
    try:
        yield AgentEvent(agent="builder", status="running")
        brief = run_builder_task(brief)
        yield AgentEvent(
            agent="builder",
            status="done",
            output={"landing_page_url": brief.landing_page_url}
        )
    except Exception as e:
        yield AgentEvent(agent="builder", status="error", output={"error": str(e)})
        return
    
    # GTM Agent
    try:
        yield AgentEvent(agent="gtm", status="running")
        brief = run_gtm_task(brief)
        yield AgentEvent(
            agent="gtm",
            status="done",
            output={
                "reddit_communities": brief.gtm_plan.reddit_communities,
                "cold_email": brief.gtm_plan.cold_email,
                "tweet_drafts": brief.gtm_plan.tweet_drafts,
                "product_hunt_blurb": brief.gtm_plan.product_hunt_blurb
            }
        )
    except Exception as e:
        yield AgentEvent(agent="gtm", status="error", output={"error": str(e)})
        return
    
    # Final completion event
    yield AgentEvent(agent="orchestrator", status="done", output=brief.model_dump())
