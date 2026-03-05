# Nevermined Integration - Implementation Complete ✅

## Overview
VentureOS now has full Nevermined agent-to-agent payment infrastructure in both directions:
- **VentureOS as Seller** — Other agents/users pay USDC credits to trigger launches
- **VentureOS as Buyer** — Scout Agent purchases research from external Nevermined agents

## Files Created/Modified

### Backend Files
1. **backend/nevermined/seller.py** ✅
   - Singleton Payments SDK instance
   - `register_ventureos_agent()` — Creates plan (10 USDC, 1 credit) and registers agent
   - CLI entrypoint: `python -m nevermined.seller`

2. **backend/nevermined/buyer.py** ✅
   - `query_external_research_agent(idea)` — Purchases and queries external agents
   - Returns None if not configured (graceful fallback)
   - Integrated into Scout Agent

3. **backend/nevermined/middleware.py** ✅
   - FastAPI middleware validates `payment-signature` header
   - Protects POST /api/run endpoint
   - Burns 1 credit after successful response
   - Allows unauthenticated access if NVM not configured

4. **backend/agents/scout_agent.py** ✅
   - Calls `query_external_research_agent()` after Apify + Exa
   - Appends external data to Claude context if available
   - No changes to existing research flow

5. **backend/main.py** ✅
   - Middleware registered after CORS
   - New endpoint: `GET /.well-known/agent.json` (A2A agent card)

### Frontend Files
6. **frontend/components/NeverminedBadge.tsx** ✅
   - Renders "⚡ Powered by Nevermined" badge
   - Only shows if `NEXT_PUBLIC_NVM_AGENT_ID` is set
   - Links to nevermined.app agent page

7. **frontend/app/page.tsx** ✅
   - Imports and renders `<NeverminedBadge />` at bottom

### Configuration Files
8. **backend/.env.example** ✅
   - Added all NVM environment variables

9. **.env.example** (root) ✅
   - Added NVM variables + `NEXT_PUBLIC_NVM_AGENT_ID`

10. **backend/requirements.txt** ✅
    - Already includes `payments-py`

11. **README.md** ✅
    - Added "Nevermined Integration" section with setup instructions

## Setup Instructions

### 1. Register VentureOS as Seller (One-Time)
```bash
cd backend
python -m nevermined.seller
```
Copy the printed `agent_id` and `plan_id` into your `.env`:
```bash
NVM_AGENT_ID=did:nv:...
NVM_PLAN_ID=did:nv:...
```

### 2. Configure Environment Variables
Add to `backend/.env`:
```bash
NVM_API_KEY=your_nevermined_api_key
NVM_ENVIRONMENT=sandbox
NVM_AGENT_ID=did:nv:...          # From step 1
NVM_PLAN_ID=did:nv:...           # From step 1
VENTUREOS_BASE_URL=http://localhost:8000  # Or production URL
```

### 3. (Optional) Enable External Research Purchases
If you want Scout Agent to buy research from other hackathon agents:
```bash
NVM_RESEARCH_AGENT_ID=did:nv:...  # External agent DID
NVM_RESEARCH_PLAN_ID=did:nv:...   # External plan DID
```

### 4. (Optional) Show Frontend Badge
Add to root `.env` or `frontend/.env.local`:
```bash
NEXT_PUBLIC_NVM_AGENT_ID=did:nv:...
```

## How It Works

### Seller Flow (VentureOS receives payments)
1. External agent/user purchases "VentureOS Launch Plan" on nevermined.app
2. They get an access token
3. They call `POST /api/run` with header: `payment-signature: <token>`
4. Middleware validates token and burns 1 credit
5. VentureOS executes the full pipeline

### Buyer Flow (VentureOS purchases research)
1. Scout Agent checks if `NVM_RESEARCH_AGENT_ID` is set
2. If yes, purchases credits from external agent's plan
3. Gets access token and calls external agent's endpoint
4. Appends external research to Claude synthesis prompt
5. Falls back gracefully if external agent unavailable

## Testing

### Test Seller (Payment Required)
```bash
# Without payment signature (should fail with 402)
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"idea": "AI-powered meal planner"}'

# With valid payment signature (should succeed)
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -H "payment-signature: <valid_token>" \
  -d '{"idea": "AI-powered meal planner"}'
```

### Test Agent Card
```bash
curl http://localhost:8000/.well-known/agent.json
```

### Test Buyer (External Research)
Set `NVM_RESEARCH_AGENT_ID` and `NVM_RESEARCH_PLAN_ID` in `.env`, then run a normal launch. Check logs for "External research agent" messages.

## Key Features

✅ **Non-Breaking** — All existing flows work without NVM configuration  
✅ **Singleton SDK** — Single Payments instance shared across seller/buyer  
✅ **Graceful Fallback** — Scout Agent works without external research  
✅ **Minimal Frontend** — Badge only renders if configured  
✅ **A2A Compatible** — Agent card follows Nevermined spec  
✅ **Credit Management** — Auto-purchase and burn credits correctly  

## Constraints Followed

- ✅ No changes to orchestrator.py
- ✅ No changes to existing agent files (except Scout integration)
- ✅ No changes to tool files
- ✅ Nevermined is optional (not required)
- ✅ Single Payments SDK instance
- ✅ Uses payments-py (not TypeScript SDK in backend)
- ✅ Minimal code (no verbose implementations)

## Next Steps

1. Get Nevermined API key from [nevermined.io](https://nevermined.io)
2. Run `python -m nevermined.seller` to register
3. Test with payment signatures
4. Deploy to production and update `VENTUREOS_BASE_URL`
5. Share agent DID with hackathon participants

## Support

- Nevermined Docs: https://docs.nevermined.io
- Payments SDK: https://github.com/nevermined-io/payments-py
- Hackathon Starters: https://github.com/nevermined-io/hackathons
