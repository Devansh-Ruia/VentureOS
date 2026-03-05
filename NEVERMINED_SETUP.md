# Nevermined Quick Setup Guide

## Prerequisites
- VentureOS backend and frontend running
- Nevermined API key from [nevermined.io](https://nevermined.io)

## Step 1: Install Dependencies
```bash
cd backend
pip install payments-py
```

## Step 2: Configure Environment
Add to `backend/.env`:
```bash
NVM_API_KEY=your_nevermined_api_key
NVM_ENVIRONMENT=sandbox
VENTUREOS_BASE_URL=http://localhost:8000
```

## Step 3: Register VentureOS as Seller
```bash
cd backend
python -m nevermined.seller
```

Expected output:
```
✅ VentureOS registered successfully!

Add these to your .env file:
NVM_AGENT_ID=did:nv:abc123...
NVM_PLAN_ID=did:nv:xyz789...
```

## Step 4: Update .env with Registration IDs
Add the output from Step 3 to `backend/.env`:
```bash
NVM_AGENT_ID=did:nv:abc123...
NVM_PLAN_ID=did:nv:xyz789...
```

## Step 5: Restart Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

## Step 6: Test Agent Card
```bash
curl http://localhost:8000/.well-known/agent.json
```

Should return JSON with your agent details.

## Optional: Enable Buyer Mode

To allow Scout Agent to purchase from external research agents:

Add to `backend/.env`:
```bash
NVM_RESEARCH_AGENT_ID=did:nv:external_agent_id
NVM_RESEARCH_PLAN_ID=did:nv:external_plan_id
```

## Optional: Enable Frontend Badge

Add to `frontend/.env.local`:
```bash
NEXT_PUBLIC_NVM_AGENT_ID=did:nv:abc123...
```

Restart frontend:
```bash
cd frontend
npm run dev
```

## Verification

### 1. Check Middleware is Active
Without payment signature:
```bash
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"idea": "test"}'
```

Should return:
```json
{
  "error": "Payment required",
  "plan_id": "did:nv:xyz789..."
}
```

### 2. Check Agent Card
```bash
curl http://localhost:8000/.well-known/agent.json | jq
```

Should show your agent metadata with payment extensions.

### 3. Check Frontend Badge
Open http://localhost:3000 — should see "⚡ Powered by Nevermined" badge in bottom-right corner.

## Troubleshooting

### "ModuleNotFoundError: No module named 'payments_py'"
```bash
cd backend
pip install payments-py
```

### "NVM_API_KEY not set"
Add to `backend/.env`:
```bash
NVM_API_KEY=your_key_here
```

### Middleware not blocking requests
Ensure `NVM_AGENT_ID` and `NVM_PLAN_ID` are set in `.env` and backend is restarted.

### Badge not showing
Ensure `NEXT_PUBLIC_NVM_AGENT_ID` is set in `frontend/.env.local` and frontend is restarted.

## Production Deployment

1. Deploy backend to production (Railway, Render, etc.)
2. Update `VENTUREOS_BASE_URL` to production URL
3. Re-run registration with production URL:
   ```bash
   NVM_ENVIRONMENT=production python -m nevermined.seller
   ```
4. Update frontend env vars with production agent ID
5. Deploy frontend to Vercel

## Support

- Nevermined Docs: https://docs.nevermined.io
- VentureOS Issues: GitHub Issues
- Hackathon Discord: [link]
