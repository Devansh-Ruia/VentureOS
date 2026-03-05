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
async def run_venture(request: RunRequest):
    async def event_stream():
        async for event in run_venture_pipeline(request.idea):
            data = json.dumps(event.model_dump())
            yield f"data: {data}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")


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
