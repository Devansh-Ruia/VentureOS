from pydantic import BaseModel


class GTMPlan(BaseModel):
    reddit_communities: list[str]
    cold_email: str
    tweet_drafts: list[str]
    product_hunt_blurb: str


class VentureBrief(BaseModel):
    idea: str
    viability_score: int | None = None
    market_summary: str | None = None
    market_size: str | None = None
    competitors: list[str] = []
    differentiation: str | None = None
    brand_name: str | None = None
    tagline: str | None = None
    domain: str | None = None
    domain_available: bool | None = None
    landing_page_url: str | None = None
    stripe_payment_link: str | None = None
    gtm_plan: GTMPlan | None = None
    adagent_campaign_id: str | None = None
    adagent_strategy: dict | None = None
    adagent_metrics: dict | None = None
    adagent_channels: list[str] | None = None
    adagent_messaging: list[str] | None = None


class AgentEvent(BaseModel):
    agent: str
    status: str
    output: dict | None = None
    message: str | None = None
