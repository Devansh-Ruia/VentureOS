from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from orchestrator import run_venture_pipeline
from dotenv import load_dotenv
import json
import os

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Nevermined payment middleware
try:
    from nevermined.middleware import NeverminedPaymentMiddleware
    app.add_middleware(NeverminedPaymentMiddleware)
except ImportError:
    pass  # payments-py not installed yet


class RunRequest(BaseModel):
    idea: str


@app.post("/api/run")
async def run_venture(request: dict):
    idea = request.get("idea", "")

    async def stream():
        import asyncio
        pipeline = run_venture_pipeline(idea)
        while True:
            try:
                event = await asyncio.wait_for(
                    pipeline.__anext__(), 
                    timeout=15.0
                )
                yield f"data: {event.model_dump_json()}\n\n"
            except asyncio.TimeoutError:
                # keepalive ping — prevents Render from closing the connection
                yield ": keepalive\n\n"
            except StopAsyncIteration:
                break

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.post("/api/demo")
async def demo(request: dict):
    import asyncio

    idea = request.get("idea", "a business idea")
    brand = "TrimStack"

    events = [
        ("scout", "running", None),
        ("scout", "done", {
            "viability_score": 74,
            "market_summary": "The SaaS management market is growing rapidly as businesses accumulate more subscriptions than they can track. Tools for solopreneurs are underserved compared to enterprise solutions.",
            "competitors": ["Cleanshelf", "Torii", "Zluri"],
            "differentiation": "Built specifically for solopreneurs, not enterprise IT teams."
        }),
        ("brand", "running", None),
        ("brand", "done", {
            "brand_name": brand,
            "domain": "trimstack.io",
            "domain_available": True
        }),
        ("builder", "running", None),
        ("builder", "done", {
            "landing_page_url": "https://trimstack-xyz.vercel.app",
            "stripe_payment_link": "https://buy.stripe.com/test_demo"
        }),
        ("gtm", "running", None),
        ("gtm", "done", {
            "gtm_plan": {
                "reddit_communities": ["entrepreneur", "SaaS", "solopreneur", "startups", "indiehackers"],
                "cold_email": "Subject: You're probably paying for tools you forgot about\n\nTrimStack finds every subscription you're paying for and helps you cut what you don't need. Built for solopreneurs, not IT teams.\n\nTry it free: trimstack.io",
                "tweet_drafts": [
                    "Solopreneurs waste $2,400/year on forgotten SaaS tools. TrimStack finds them all.",
                    "Built TrimStack to track every subscription I forgot I was paying for. Now it's yours.",
                    "Your SaaS bill is lying to you. trimstack.io"
                ],
                "product_hunt_blurb": "TrimStack: subscription tracking built for solopreneurs, not enterprise"
            }
        }),
        ("orchestrator", "done", {
            "idea": idea,
            "brand_name": brand,
            "domain": "trimstack.io",
            "domain_available": True,
            "viability_score": 74,
            "market_summary": "The SaaS management market is growing rapidly as businesses accumulate more subscriptions than they can track. Tools for solopreneurs are underserved compared to enterprise solutions.",
            "competitors": ["Cleanshelf", "Torii", "Zluri"],
            "differentiation": "Built specifically for solopreneurs, not enterprise IT teams.",
            "landing_page_url": "https://trimstack-xyz.vercel.app",
            "stripe_payment_link": "https://buy.stripe.com/test_demo",
            "gtm_plan": {
                "reddit_communities": ["entrepreneur", "SaaS", "solopreneur", "startups", "indiehackers"],
                "cold_email": "Subject: You're probably paying for tools you forgot about\n\nTrimStack finds every subscription you're paying for and helps you cut what you don't need. Built for solopreneurs, not IT teams.\n\nTry it free: trimstack.io",
                "tweet_drafts": [
                    "Solopreneurs waste $2,400/year on forgotten SaaS tools. TrimStack finds them all.",
                    "Built TrimStack to track every subscription I forgot I was paying for. Now it's yours.",
                    "Your SaaS bill is lying to you. trimstack.io"
                ],
                "product_hunt_blurb": "TrimStack: subscription tracking built for solopreneurs, not enterprise"
            }
        })
    ]

    async def stream():
        for agent, status, output in events:
            await asyncio.sleep(1.5)
            event = {"agent": agent, "status": status, "output": output, "message": None}
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/.well-known/agent.json")
async def agent_card():
    """Nevermined A2A agent card."""
    base_url = os.getenv("VENTUREOS_BASE_URL", "http://localhost:8000")
    plan_id = os.getenv("NVM_PLAN_ID", "")
    agent_id = os.getenv("NVM_AGENT_ID", "")
    
    return JSONResponse({
        "name": "VentureOS",
        "description": "Autonomous business launch agent. Input a business idea, receive a live URL, brand, and go-to-market plan.",
        "url": f"{base_url}/api/run",
        "capabilities": {
            "streaming": True,
            "extensions": [
                {
                    "uri": "urn:nevermined:payment",
                    "description": "1 credit per business launch",
                    "required": True,
                    "params": {
                        "paymentType": "fixed",
                        "credits": 1,
                        "planId": plan_id,
                        "agentId": agent_id
                    }
                }
            ]
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "idea": {
                    "type": "string",
                    "description": "Plain-English business idea"
                }
            },
            "required": ["idea"]
        }
    })
