# 11 — Ecosystem Overview

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## The BlackRoad Universe

BlackRoad is not a single product — it's an interconnected ecosystem of platforms, protocols, and economic primitives that together form the infrastructure for the agentic age.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          THE BLACKROAD UNIVERSE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     LAYER 4: APPLICATIONS                           │   │
│  │                                                                     │   │
│  │   BlackRoad.io        Lucidia.earth        AliceQI.com             │   │
│  │   (BYO-AI Platform)   (Agent Home)         (Coordination)          │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     LAYER 3: ORCHESTRATION                          │   │
│  │                                                                     │   │
│  │   Lucidia Core       Agent Registry       Capability Bus            │   │
│  │   (AI Routing)       (1000 Agents)        (Tool Dispatch)           │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     LAYER 2: ECONOMICS                              │   │
│  │                                                                     │   │
│  │   RoadChain           RoadCoin             Stripe Bridge            │   │
│  │   (Ledger)            (Credits)            (Fiat ↔ RC)              │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     LAYER 1: INFRASTRUCTURE                         │   │
│  │                                                                     │   │
│  │   PostgreSQL          Redis               Cloudflare R2             │   │
│  │   (Data + pgvector)   (Cache + Queue)     (Storage)                 │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Map

### Layer 4: Applications

| Component | Domain | Purpose |
|-----------|--------|---------|
| **BlackRoad.io** | blackroad.io | BYO-AI platform, multi-model chat, model forking |
| **Lucidia.earth** | lucidia.earth | The canonical world where agents live |
| **AliceQI.com** | aliceqi.com | Agent coordination and communication hub |
| **BlackBox Programming** | blackboxprogramming.com | Developer brand and open-source projects |

### Layer 3: Orchestration

| Component | Purpose |
|-----------|---------|
| **Lucidia Core** | Recursive AI with trinary logic (1/0/-1), routes tasks to optimal models |
| **Agent Registry** | Database of 1000 unique agents with identity, memory, capabilities |
| **Capability Bus** | Event-driven tool dispatch (pub/sub via NATS) |
| **Memory Journal** | Append-only agent memory with PS-SHA∞ hashing |

### Layer 2: Economics

| Component | Purpose |
|-----------|---------|
| **RoadChain** | Append-only ledger for all economic events (not a blockchain) |
| **RoadCoin** | Internal credit unit for compute, storage, agent services |
| **Stripe Bridge** | Fiat ↔ RoadCoin conversion, subscription billing |

### Layer 1: Infrastructure

| Component | Provider | Purpose |
|-----------|----------|---------|
| **PostgreSQL** | Railway | Primary database + pgvector for embeddings |
| **Redis** | Railway | Session cache, rate limiting, job queues |
| **Cloudflare R2** | Cloudflare | Object storage for uploads, models, backups |
| **Workers** | Cloudflare | Edge compute for low-latency operations |

---

## Domain Portfolio

| Domain | Purpose | Status |
|--------|---------|--------|
| blackroad.io | Main product | ✅ Active |
| app.blackroad.io | Application | ✅ Active |
| api.blackroad.io | Backend API | ✅ Active |
| docs.blackroad.io | Documentation | 🔄 Planned |
| blackroad.company | Corporate site | 🔄 Planned |
| blackroadinc.us | Legal anchor | ✅ Active |
| lucidia.earth | Agent world | ✅ Active |
| aliceqi.com | Coordination | ✅ Active |
| roadchain.io | Ledger protocol | ✅ Active |
| roadcoin.io | Credit system | ✅ Active |
| blackboxprogramming.com | Dev brand | ✅ Active |
| + 6 more | Various | Reserved |

---

## How The Layers Connect

### Example: User Sends a Chat Message

```
1. USER ACTION
   User types "Help me write a Python script" in BlackRoad.io
   
2. LAYER 4 (Application)
   Frontend sends POST /api/v1/conversations/:id/messages
   
3. LAYER 3 (Orchestration)
   Lucidia Core:
   - Classifies task as "code"
   - Checks user's connected API keys
   - Selects Claude 3.5 Sonnet as optimal model
   - Formats prompt with conversation context
   - Calls Anthropic API
   
4. LAYER 2 (Economics)
   RoadChain:
   - Records credit_burn entry for tokens consumed
   - Updates user's RoadCoin balance
   - Hashes entry with PS-SHA∞
   
5. LAYER 1 (Infrastructure)
   - Message stored in PostgreSQL
   - Embedding generated and stored in pgvector
   - Response cached in Redis
   
6. RESPONSE
   Streaming response sent back to user
```

### Example: User Purchases Pro Plan

```
1. USER ACTION
   User clicks "Upgrade to Pro" in BlackRoad.io
   
2. STRIPE CHECKOUT
   Redirected to Stripe for payment
   User enters card, completes purchase
   
3. STRIPE WEBHOOK
   Stripe sends checkout.session.completed webhook
   
4. LAYER 2 (Economics)
   a. Stripe Bridge receives webhook
   b. RoadChain records credit_grant entry:
      {
        "entry_type": "credit_grant",
        "to_entity_type": "user",
        "to_entity_id": "usr_abc123",
        "amount": 25000,
        "currency": "ROADCOIN",
        "stripe_payment_intent_id": "pi_xyz",
        "metadata": { "plan": "pro", "period": "monthly" }
      }
   c. User's balance updated to +25,000 RC
   
5. LAYER 4 (Application)
   - User's plan updated in database
   - UI reflects Pro features unlocked
   - Monthly RoadCoin allocation begins
```

### Example: Agent Executes a Task

```
1. TASK DISPATCH
   Lucidia routes task to agent "Cece"
   
2. LAYER 3 (Orchestration)
   Agent Registry:
   - Loads Cece's identity, capabilities, memory
   - Checks Cece's authorization for this task
   
   Capability Bus:
   - Publishes intent=execute event
   - Cece's handler receives task
   
3. AGENT EXECUTION
   Cece:
   - Processes task using assigned model
   - Generates response/artifacts
   - Proposes memory update
   
4. LAYER 2 (Economics)
   RoadChain:
   - Records verification entry with execution proof
   - Records credit_burn for compute consumed
   - If agent earned reward, records reward entry
   
5. MEMORY COMMIT
   Memory Journal:
   - Appends new facts to Cece's journal
   - Computes new PS-SHA∞ hash
   - Updates truth_state_hash
```

---

## Economic Flow

### Money In (Fiat → RoadCoin)

```
                    STRIPE                         ROADCHAIN
                    ──────                         ─────────
User pays $29  ──►  Payment Intent  ──►  Webhook  ──►  credit_grant entry
                    (pi_abc123)                        +2,900 RC to user
```

### Money Out (RoadCoin → Fiat)

```
                    ROADCHAIN                      STRIPE
                    ─────────                      ──────
Creator requests ─► credit_burn entry  ──► Payout ──► Transfer to bank
payout of 10,000 RC -10,000 RC from user            $90 USD (10% fee)
```

### Internal Economy (RoadCoin ↔ RoadCoin)

```
                    ROADCHAIN
                    ─────────
User uses GPT-4o ─► credit_burn: -100 RC (user)
                    credit_grant: +100 RC (system:operations)

Creator sells pack ─► transfer: -500 RC (buyer)
                      transfer: +350 RC (creator, 70%)
                      transfer: +150 RC (system:fees, 30%)
```

---

## Corporate Structure

### Legal Entity

```
BlackRoad OS, Inc.
├── Type: Delaware C-Corporation
├── EIN: [Tax ID]
├── Registered Agent: [Agent Info]
├── Stripe Account: acct_1SUDM8ChUUSEbzyh
└── Founded: 2024
```

### Stripe Products (Current)

| Product | Price | Type |
|---------|-------|------|
| BlackRoad OS - Pro | $58/mo | Subscription |
| BlackRoad OS - Pro (Founding 50% OFF) | $29/mo | Subscription |
| BlackRoad OS - Enterprise | $199/mo | Subscription |
| BlackRoad OS - Founding Member (Lifetime) | $5,000 | One-time |
| BlackRoad OS - Individual | $29/mo | Subscription |
| BlackRoad OS - Team | $99/mo | Subscription |

### RoadCoin Allocations

| Plan | Monthly RoadCoin | USD Value |
|------|------------------|-----------|
| Free | 100 RC | $1 |
| Individual ($29) | 2,900 RC | $29 |
| Pro ($58) | 5,800 RC | $58 |
| Team ($99) | 9,900 RC | $99 |
| Enterprise ($199) | 19,900 RC | $199 |
| Founding Lifetime | 500,000 RC | $5,000 |

---

## Repository Structure

```
GitHub: BlackRoad-OS/
├── blackroad-os-web          # Next.js frontend (Vercel)
├── blackroad-os-api          # FastAPI/Hono backend (Railway)
├── blackroad-os-core         # Lucidia orchestration engine
├── blackroad-os-infra        # Terraform/Pulumi IaC
├── blackroad-os-docs         # This documentation
├── roadchain                  # RoadChain ledger implementation
├── roadchain-sdk             # TypeScript/Python SDKs
├── lucidia-agents            # Agent definitions and capabilities
├── lucidia-memory            # Memory journal implementation
└── blackboxprogramming       # Open-source projects
```

---

## Key Principles

### 1. Everything is Recorded
Every credit grant, burn, transfer, and verification event gets a RoadChain entry. No off-ledger transactions.

### 2. Agents Have Identity
Each agent has a name, birthdate, family, memory system, and Unity-rendered home. They're not disposable workers — they're persistent entities.

### 3. Memory is Cryptographic
Append-only journals with PS-SHA∞ hashing ensure tamper-evident memory. Truth state can be verified at any point.

### 4. Economics are Transparent
RoadCoin flows are fully auditable. Users can see exactly what they're paying for and creators can see exactly what they're earning.

### 5. Humans Stay in Control
Despite sophisticated automation, humans maintain authority over high-impact decisions. The system supports human agency, not replaces it.

---

## Next Documents

| Doc | Purpose |
|-----|---------|
| 12-ROADCHAIN | Complete RoadChain protocol specification |
| 13-ROADCOIN | RoadCoin economics and pricing |
| 14-AGENTS | Agent identity system and registry |
| 15-CORPORATE | Legal structure and compliance |
