# VentureOS

An autonomous business launch agent that transforms plain-English business ideas into live ventures with validation, branding, landing pages, and go-to-market plans.

## Overview

VentureOS executes four specialized AI agents in sequence:

1. **Scout** — Market validation and competitive intelligence
2. **Brand** — Name generation and domain availability
3. **Builder** — Landing page creation and deployment
4. **GTM** — Go-to-market strategy and distribution plan

**Output:** Live URL + Comprehensive Venture Brief

## Stack

- **Backend:** Python, FastAPI, CrewAI, LangChain
- **LLM:** Claude 3.5 Sonnet (Anthropic)
- **Research:** Apify (web scraping), Exa (semantic search)
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS
- **Deployment:** Vercel API
- **Payments:** Stripe (test mode)

## Prerequisites

- Python 3.11+
- Node.js 18+
- API keys (see Environment Variables below)

## Quick Start

### 1. Clone and Install

```bash
git clone <repository-url>
cd VentureOS
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file in the `backend/` directory:

```bash
cp ../.env.example .env
```

Edit `.env` with your API keys (see Environment Variables section).

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

Create `next.config.js` if it doesn't exist:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
```

### 4. Run the Project

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## Environment Variables

Create a `.env` file in the `backend/` directory with the following:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...           # Get from console.anthropic.com
APIFY_API_TOKEN=apify_api_...          # Get from apify.com
EXA_API_KEY=...                        # Get from exa.ai
VERCEL_TOKEN=...                       # Get from vercel.com/account/tokens
STRIPE_SECRET_KEY=sk_test_...          # Get from dashboard.stripe.com (test mode)

# Optional
VERCEL_TEAM_ID=                        # Only if using Vercel team account
NAMECHEAP_API_KEY=                     # For real domain checks (optional)
NAMECHEAP_API_USER=                    # For real domain checks (optional)
RESEND_API_KEY=                        # For email notifications (not yet implemented)
MINDRA_API_KEY=                        # Alternative to Anthropic (not yet implemented)

# Demo Mode (default: true)
DEMO_MODE=true                         # Set to false to enable real domain purchases
```

### Getting API Keys

- **Anthropic:** [console.anthropic.com](https://console.anthropic.com)
- **Apify:** [apify.com/account/api](https://apify.com/account/api)
- **Exa:** [exa.ai](https://exa.ai)
- **Vercel:** [vercel.com/account/tokens](https://vercel.com/account/tokens)
- **Stripe:** [dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys)

## Project Structure

```
VentureOS/
├── backend/
│   ├── agents/
│   │   ├── scout_agent.py      # Market validation
│   │   ├── brand_agent.py      # Naming + domain
│   │   ├── builder_agent.py    # Landing page + deploy
│   │   └── gtm_agent.py        # Go-to-market plan
│   ├── tools/
│   │   ├── apify_tools.py      # Web scraping
│   │   ├── exa_tools.py        # Semantic search
│   │   ├── domain_tools.py     # Domain availability
│   │   ├── vercel_tools.py     # Deployment
│   │   └── stripe_tools.py     # Payment links
│   ├── orchestrator.py         # Agent pipeline
│   ├── models.py               # Pydantic models
│   ├── main.py                 # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main UI
│   │   └── api/run/route.ts    # API proxy (optional)
│   └── components/
│       ├── IdeaInput.tsx       # User input form
│       ├── AgentStream.tsx     # Real-time agent status
│       └── VentureBrief.tsx    # Final output display
├── templates/
│   └── landing_page.html       # Tailwind template
├── .env.example
└── README.md
```

## How It Works

1. **User submits idea** → Frontend sends POST to `/api/run`
2. **Backend streams events** → SSE (Server-Sent Events) for real-time updates
3. **Scout Agent** → Researches market, competitors, viability score
4. **Brand Agent** → Generates names, checks domain availability
5. **Builder Agent** → Creates landing page, deploys to Vercel, adds Stripe payment
6. **GTM Agent** → Generates Reddit communities, cold email, tweets, Product Hunt blurb
7. **Frontend displays** → Live URL + full Venture Brief

## Demo Mode

By default, `DEMO_MODE=true` prevents real money transactions:

- Domain checks simulate availability (no actual Namecheap API calls)
- Stripe creates test payment links (no real charges)
- Vercel deployments are real (free tier)

Set `DEMO_MODE=false` to enable production behavior.

## Troubleshooting

### Backend won't start
- Verify Python 3.11+ with `python --version`
- Check all required API keys are in `.env`
- Install dependencies: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check `next.config.js` has correct proxy rewrite
- Verify CORS settings in `backend/main.py`

### Agents fail with API errors
- Check API key validity and rate limits
- Verify `DEMO_MODE=true` if missing Namecheap credentials
- Review backend logs for specific error messages

### Deployment fails
- Verify Vercel token has deployment permissions
- Check `VERCEL_TEAM_ID` if using team account
- Ensure project name is valid (lowercase, no spaces)

## Development

### Adding a new agent
1. Create `backend/agents/new_agent.py`
2. Define `create_new_agent()` and `run_new_task(brief)`
3. Add to `orchestrator.py` pipeline
4. Update `AgentStream.tsx` with new agent key

### Adding a new tool
1. Create `backend/tools/new_tool.py`
2. Add docstring for CrewAI reasoning
3. Wrap external API calls in try/except
4. Return structured dict (never raise exceptions)

## Nevermined Integration

VentureOS supports agent-to-agent payments via the Nevermined protocol.

### Register as a Seller Agent (run once)
```bash
cd backend
python -m nevermined.seller
```
Copy the printed `agent_id` and `plan_id` into your `.env` file as `NVM_AGENT_ID` and `NVM_PLAN_ID`.

### Buying research from external agents
Set `NVM_RESEARCH_AGENT_ID` and `NVM_RESEARCH_PLAN_ID` in `.env` to enable Scout Agent to autonomously purchase research from other hackathon agents.

### Payment flow
External agents and users can trigger a VentureOS launch by:
1. Purchasing the VentureOS Launch Plan on nevermined.app
2. Calling `POST /api/run` with header: `payment-signature: <access_token>`

### Environment Variables for Nevermined
```bash
NVM_API_KEY=                    # Get from nevermined.io
NVM_ENVIRONMENT=sandbox         # sandbox | production
NVM_AGENT_ID=                   # Set after registration
NVM_PLAN_ID=                    # Set after registration
NVM_RESEARCH_AGENT_ID=          # External research agent DID (optional)
NVM_RESEARCH_PLAN_ID=           # External research plan DID (optional)
VENTUREOS_BASE_URL=             # Public URL (e.g., https://ventureos.vercel.app)
NEXT_PUBLIC_NVM_AGENT_ID=       # For frontend badge (optional)
```

## License

MIT

## Support

For issues or questions, open a GitHub issue or contact the maintainers.
