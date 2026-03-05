# VentureOS + Nevermined Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         VentureOS System                         │
│                                                                   │
│  ┌────────────────┐                    ┌────────────────┐       │
│  │   Frontend     │                    │    Backend     │       │
│  │   (Next.js)    │◄──────SSE─────────►│   (FastAPI)    │       │
│  │                │                    │                │       │
│  │  - IdeaInput   │                    │  - Orchestrator│       │
│  │  - AgentStream │                    │  - 4 Agents    │       │
│  │  - VentureBrief│                    │  - Tools       │       │
│  │  - NvmBadge ⚡ │                    │                │       │
│  └────────────────┘                    └────────┬───────┘       │
│                                                  │               │
└──────────────────────────────────────────────────┼───────────────┘
                                                   │
                    ┌──────────────────────────────┼──────────────────────────┐
                    │                              │                          │
                    ▼                              ▼                          ▼
        ┌───────────────────┐        ┌───────────────────┐      ┌──────────────────┐
        │ Nevermined        │        │ External Research │      │ Existing APIs    │
        │ Payment Protocol  │        │ Agents (Buyer)    │      │ - Apify          │
        │                   │        │                   │      │ - Exa            │
        │ - Validate Token  │        │ - Agent A         │      │ - Vercel         │
        │ - Burn Credits    │        │ - Agent B         │      │ - Stripe         │
        │ - Order Plans     │        │ - Agent C         │      │ - Namecheap      │
        └───────────────────┘        └───────────────────┘      └──────────────────┘
```

## Payment Flow: VentureOS as Seller

```
External Agent/User                 Nevermined              VentureOS
      │                                 │                       │
      │  1. Purchase Launch Plan        │                       │
      ├────────────────────────────────►│                       │
      │                                 │                       │
      │  2. Receive Access Token        │                       │
      │◄────────────────────────────────┤                       │
      │                                 │                       │
      │  3. POST /api/run               │                       │
      │     Header: payment-signature   │                       │
      ├─────────────────────────────────┼──────────────────────►│
      │                                 │                       │
      │                                 │  4. Validate Token    │
      │                                 │◄──────────────────────┤
      │                                 │                       │
      │                                 │  5. Token Valid       │
      │                                 ├──────────────────────►│
      │                                 │                       │
      │  6. SSE Stream (Launch Events)  │                       │
      │◄────────────────────────────────┼───────────────────────┤
      │     - Scout: running            │                       │
      │     - Scout: done               │                       │
      │     - Brand: running            │                       │
      │     - Brand: done               │                       │
      │     - Builder: running          │                       │
      │     - Builder: done             │                       │
      │     - GTM: running              │                       │
      │     - GTM: done                 │                       │
      │     - Orchestrator: done        │                       │
      │                                 │                       │
      │                                 │  7. Burn 1 Credit     │
      │                                 │◄──────────────────────┤
      │                                 │                       │
```

## Payment Flow: VentureOS as Buyer

```
VentureOS Scout Agent          Nevermined         External Research Agent
      │                            │                         │
      │  1. Check Plan Balance     │                         │
      ├───────────────────────────►│                         │
      │                            │                         │
      │  2. Balance = 0            │                         │
      │◄───────────────────────────┤                         │
      │                            │                         │
      │  3. Order Plan             │                         │
      ├───────────────────────────►│                         │
      │                            │                         │
      │  4. Get Access Token       │                         │
      ├───────────────────────────►│                         │
      │                            │                         │
      │  5. Access Token           │                         │
      │◄───────────────────────────┤                         │
      │                            │                         │
      │  6. POST /research         │                         │
      │     Header: Authorization   │                         │
      ├────────────────────────────┼────────────────────────►│
      │                            │                         │
      │  7. Research Data          │                         │
      │◄───────────────────────────┼─────────────────────────┤
      │                            │                         │
      │  8. Append to Claude       │                         │
      │     Context                │                         │
      │                            │                         │
```

## Component Architecture

```
backend/
├── main.py
│   ├── FastAPI App
│   ├── CORS Middleware
│   ├── NeverminedPaymentMiddleware ◄─── Validates payment-signature
│   ├── POST /api/run ◄───────────────── Protected by middleware
│   └── GET /.well-known/agent.json ◄─── Agent card for discovery
│
├── nevermined/
│   ├── seller.py
│   │   ├── get_payments_instance() ◄─── Singleton Payments SDK
│   │   └── register_ventureos_agent() ◄ One-time registration
│   │
│   ├── buyer.py
│   │   └── query_external_research_agent() ◄─ Purchase & query
│   │
│   └── middleware.py
│       └── NeverminedPaymentMiddleware
│           ├── Check payment-signature header
│           ├── Validate with Nevermined
│           └── Burn credits after response
│
└── agents/
    └── scout_agent.py
        └── run_scout_task()
            ├── Apify research
            ├── Exa research
            ├── query_external_research_agent() ◄─ NEW
            └── Claude synthesis
```

## Data Flow

```
1. User Input
   └─► Frontend: IdeaInput.tsx
       └─► POST /api/run { idea: "..." }
           └─► Middleware: Check payment-signature
               ├─► If NVM_AGENT_ID not set: Allow
               └─► If set: Validate token
                   ├─► Invalid: Return 402
                   └─► Valid: Continue
                       └─► Orchestrator
                           ├─► Scout Agent
                           │   ├─► Apify
                           │   ├─► Exa
                           │   └─► External Nevermined Agent (optional)
                           ├─► Brand Agent
                           ├─► Builder Agent
                           └─► GTM Agent
                               └─► SSE Stream to Frontend
                                   └─► Burn 1 credit

2. External Agent Calls VentureOS
   └─► Purchase plan on nevermined.app
       └─► Get access token
           └─► POST /api/run
               Header: payment-signature: <token>
               └─► Same flow as above
```

## Environment Configuration

```
┌─────────────────────────────────────────────────────────────┐
│ Backend (.env)                                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Seller Configuration (VentureOS as Service)                 │
│ ├─ NVM_API_KEY          ◄─── Nevermined API key            │
│ ├─ NVM_ENVIRONMENT      ◄─── sandbox | production          │
│ ├─ NVM_AGENT_ID         ◄─── Set after registration        │
│ ├─ NVM_PLAN_ID          ◄─── Set after registration        │
│ └─ VENTUREOS_BASE_URL   ◄─── Public endpoint URL           │
│                                                              │
│ Buyer Configuration (Scout Agent)                           │
│ ├─ NVM_RESEARCH_AGENT_ID ◄─── External agent DID           │
│ └─ NVM_RESEARCH_PLAN_ID  ◄─── External plan DID            │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Frontend (.env.local)                                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ └─ NEXT_PUBLIC_NVM_AGENT_ID ◄─── For badge display         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### ✅ Backward Compatible
- Works without Nevermined configuration
- Graceful degradation if payments-py not installed
- Existing flows unchanged

### ✅ Bidirectional Payments
- Sell: VentureOS as purchasable service
- Buy: Scout Agent purchases external research

### ✅ Credit-Based Pricing
- 10 USDC = 1 launch credit
- Automatic credit burning after successful launch
- Balance checking and auto-purchase for buyer mode

### ✅ Standards Compliant
- A2A agent card at /.well-known/agent.json
- payment-signature header validation
- Nevermined protocol integration

### ✅ Production Ready
- Singleton Payments SDK instance
- Error handling and logging
- Async-compatible for SSE streaming
- Try/except blocks for resilience
