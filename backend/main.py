from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from orchestrator import run_venture_pipeline
from dotenv import load_dotenv
import json

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    idea: str


@app.post("/api/run")
async def run_venture(request: RunRequest):
    async def event_stream():
        async for event in run_venture_pipeline(request.idea):
            data = json.dumps(event.model_dump())
            yield f"data: {data}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")
