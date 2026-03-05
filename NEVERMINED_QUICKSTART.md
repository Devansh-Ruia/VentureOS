# Nevermined Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Get Nevermined API Key
1. Visit [nevermined.io](https://nevermined.io)
2. Sign up and get your API key
3. Add to `backend/.env`:
```bash
NVM_API_KEY=your_api_key_here
NVM_ENVIRONMENT=sandbox
```

### Step 3: Register VentureOS as a Seller
```bash
cd backend
python -m nevermined.seller
```

You'll see output like:
```
✅ VentureOS registered successfully!

Add these to your .env file:
NVM_AGENT_ID=did:nv:abc123...
NVM_PLAN_ID=did:nv:xyz789...
```

Copy these values into your `backend/.env` file.

### Step 4: Set Your Base URL
Add to `backend/.env`:
```bash
VENTUREOS_BASE_URL=http://localhost:8000
```

For production, use your actual domain:
```bash
VENTUREOS_BASE_URL=https://ventureos.vercel.app
```

### Step 5: Test It!

**Start the backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Test the agent card:**
```bash
curl http://localhost:8000/.well-known/agent.json
```

**Test payment protection:**
```bash
# This should return 402 Payment Required
curl -X POST http://localhost:8000/api/run \
  -H "Content-Type: application/json" \
  -d '{"idea": "AI-powered meal planner"}'
```

## 🎯 Optional: Enable External Research Purchases

If you want Scout Agent to buy research from other hackathon agents:

1. Get the external agent's DID and plan ID
2. Add to `backend/.env`:
```bash
NVM_RESEARCH_AGENT_ID=did:nv:external_agent_id
NVM_RESEARCH_PLAN_ID=did:nv:external_plan_id
```

3. Scout Agent will automatically query the external agent during research

## 🎨 Optional: Show Nevermined Badge

Add to root `.env` or `frontend/.env.local`:
```bash
NEXT_PUBLIC_NVM_AGENT_ID=did:nv:your_agent_id
```

The badge will appear in the bottom-right corner of the frontend.

## 🧪 Testing Without Nevermined

The system works perfectly without any Nevermined configuration:

1. Don't set any `NVM_*` environment variables
2. Run VentureOS normally
3. All features work (no payment required)

This is great for development and testing!

## 📚 Full Environment Variables

```bash
# Required for Nevermined Seller
NVM_API_KEY=                    # Get from nevermined.io
NVM_ENVIRONMENT=sandbox         # sandbox | production
NVM_AGENT_ID=                   # Set after registration
NVM_PLAN_ID=                    # Set after registration
VENTUREOS_BASE_URL=             # Your public URL

# Optional for Nevermined Buyer
NVM_RESEARCH_AGENT_ID=          # External agent DID
NVM_RESEARCH_PLAN_ID=           # External plan DID

# Optional for Frontend Badge
NEXT_PUBLIC_NVM_AGENT_ID=       # Your agent DID
```

## 🔧 Troubleshooting

### "Module 'payments_py' not found"
```bash
pip install payments-py
```

### "NVM_API_KEY not set"
Make sure you have a `.env` file in the `backend/` directory with your API key.

### "Agent registration failed"
- Check your API key is valid
- Verify you're using the correct environment (sandbox vs production)
- Check your internet connection

### "Payment validation failed"
- Verify `NVM_AGENT_ID` and `NVM_PLAN_ID` are set correctly
- Check the payment signature is valid
- Ensure the plan has available credits

## 🎉 You're Done!

Your VentureOS instance is now:
- ✅ Registered as a Nevermined seller agent
- ✅ Protected by payment validation
- ✅ Ready to accept USDC credits
- ✅ Able to purchase research from other agents (if configured)

Share your agent DID with hackathon participants and start accepting payments!

## 📖 More Information

- Full documentation: `NEVERMINED_IMPLEMENTATION_COMPLETE.md`
- Verification checklist: `NEVERMINED_VERIFICATION.md`
- Nevermined docs: https://docs.nevermined.io
- Payments SDK: https://github.com/nevermined-io/payments-py
