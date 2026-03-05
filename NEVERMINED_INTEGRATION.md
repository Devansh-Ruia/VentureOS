# Nevermined Integration Summary

## Overview
VentureOS now supports bidirectional agent-to-agent payments via the Nevermined protocol:
1. **As a Seller** — Other agents can pay USDC credits to trigger VentureOS launches
2. **As a Buyer** — Scout Agent can purchase research from external Nevermined agents

## Files Created

### Backend
```
backend/nevermined/
├── __init__.py           # Package initialization
├── seller.py             # Seller agent registration
├── buyer.py              # Buyer logic for Scout Agent
└── middleware.py         # FastAPI payment validation middleware
```

### Frontend
```
frontend/components/
└── NeverminedBadge.tsx   # Payment status badge
```

## Implementation Details

### Part 1: Seller Agent (backend/nevermined/seller.py)

**Key Functions:**
- `get_payments_instance()` — Singleton Payments SDK instance
- `register_ventureos_agent()` — One-time registration script

**Registration Process:**
1. Creates a credits-based pricing plan (10 USDC, 1 credit per launch)
2. Registers VentureOS agent with endpoint and metadata
3. Links agent to plan
4. Outputs `agent_id` and `plan_id` to save in `.env`

**CLI Usage:**
```bash
cd backend
python -m nevermined.seller
```

### Part 2: Payment Middleware (backend/nevermined/middleware.py)

**Behavior:**
- Protects `POST /api/run` endpoint
- If `NVM_AGENT_ID` not set → allows unauthenticated access (backward compatible)
- If set → validates `payment-signature` header
- Returns HTTP 402 if invalid or missing
- Burns 1 credit after successful response

**Integration:**
Added to `backend/main.py` after CORS middleware with try/except for graceful degradation.

### Part 3: Agent Card Endpoint (backend/main.py)

**Endpoint:** `GET /.well-known/agent.json`

**Returns:** Nevermined-compatible A2A agent card with:
- Agent metadata (name, description, URL)
- Capabilities (streaming, payment extensions)
- Input schema (idea: string)
- Payment parameters (planId, agentId, credits)

### Part 4: Buyer Agent (backend/nevermined/buyer.py)

**Key Function:**
- `query_external_research_agent(idea: str) -> Optional[dict]`

**Behavior:**
1. Checks for `NVM_RESEARCH_AGENT_ID` and `NVM_RESEARCH_PLAN_ID`
2. Returns `None` if not configured (graceful fallback)
3. Checks plan balance, purchases if zero
4. Gets access token and calls external agent
5. Returns research data or `None` on error

**Integration:**
Added to `backend/agents/scout_agent.py` in `run_scout_task()`:
- Calls external agent after Apify + Exa
- Appends external data to Claude prompt context
- Does not replace existing research tools

### Part 5: Frontend Badge (frontend/components/NeverminedBadge.tsx)

**Behavior:**
- Renders only if `NEXT_PUBLIC_NVM_AGENT_ID` is set
- Displays "⚡ Powered by Nevermined" badge
- Links to `https://nevermined.app/agent/<agent_id>`
- Positioned bottom-right, styled with Tailwind

**Integration:**
Added to `frontend/app/page.tsx` at the bottom of the component tree.

## Environment Variables

### Backend (.env)
```bash
# Nevermined Seller Configuration
NVM_API_KEY=                    # Required for registration
NVM_ENVIRONMENT=sandbox         # sandbox | production
NVM_AGENT_ID=                   # Set after registration
NVM_PLAN_ID=                    # Set after registration
VENTUREOS_BASE_URL=             # Public URL for agent endpoint

# Nevermined Buyer Configuration (Optional)
NVM_RESEARCH_AGENT_ID=          # External research agent DID
NVM_RESEARCH_PLAN_ID=           # External research plan DID
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_NVM_AGENT_ID=       # For badge display (optional)
```

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt  # Includes payments-py
```

### 2. Configure Environment
Add Nevermined variables to `backend/.env`:
```bash
NVM_API_KEY=your_key_here
NVM_ENVIRONMENT=sandbox
VENTUREOS_BASE_URL=http://localhost:8000
```

### 3. Register as Seller (One-time)
```bash
cd backend
python -m nevermined.seller
```

Copy the output `agent_id` and `plan_id` to your `.env`:
```bash
NVM_AGENT_ID=did:nv:...
NVM_PLAN_ID=did:nv:...
```

### 4. (Optional) Configure Buyer
To enable Scout Agent to purchase external research:
```bash
NVM_RESEARCH_AGENT_ID=did:nv:...
NVM_RESEARCH_PLAN_ID=did:nv:...
```

### 5. (Optional) Enable Frontend Badge
Add to `frontend/.env.local`:
```bash
NEXT_PUBLIC_NVM_AGENT_ID=did:nv:...
```

## Payment Flow

### As a Seller
1. External agent/user purchases VentureOS Launch Plan on nevermined.app
2. Gets access token from Nevermined
3. Calls `POST /api/run` with header: `payment-signature: <token>`
4. Middleware validates token and burns 1 credit
5. VentureOS executes launch pipeline

### As a Buyer
1. Scout Agent checks for external research agent configuration
2. If configured, checks plan balance
3. Purchases plan if balance is zero
4. Gets access token and calls external agent
5. Appends external research to Claude prompt
6. Falls back to Apify + Exa if external agent fails

## Backward Compatibility

All changes are backward compatible:
- If `NVM_AGENT_ID` not set → middleware allows unauthenticated access
- If `NVM_RESEARCH_AGENT_ID` not set → Scout Agent skips external research
- If `NEXT_PUBLIC_NVM_AGENT_ID` not set → badge doesn't render
- Try/except blocks prevent crashes if `payments-py` not installed

## Testing

### Test Seller Registration
```bash
cd backend
python -m nevermined.seller
# Should output agent_id and plan_id
```

### Test Unauthenticated Access (No NVM_AGENT_ID)
```bash
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"idea": "AI-powered meal planner"}'
# Should stream events normally
```

### Test Payment Required (With NVM_AGENT_ID)
```bash
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"idea": "AI-powered meal planner"}'
# Should return 402 Payment Required
```

### Test Agent Card
```bash
curl http://localhost:8000/.well-known/agent.json
# Should return JSON with agent metadata
```

## Key Design Decisions

1. **Singleton Payments Instance** — Single instance in `seller.py`, imported by `buyer.py` and `middleware.py`
2. **Graceful Degradation** — All Nevermined features are optional, system works without them
3. **Minimal Changes** — Only modified `main.py`, `scout_agent.py`, and `page.tsx`
4. **No Breaking Changes** — Existing flows work unchanged
5. **Async-Compatible** — All payment operations use async/await for SSE streaming

## Reference Implementation

Based on Nevermined hackathon starter repos:
- Seller pattern: `hackathons/agents/seller-simple-agent`
- Buyer pattern: `hackathons/agents/buyer-simple-agent`

## Next Steps

1. Deploy VentureOS to production (Vercel/Railway)
2. Set `VENTUREOS_BASE_URL` to public URL
3. Register agent with production Nevermined environment
4. Test with other hackathon agents
5. Monitor credit usage and balance
