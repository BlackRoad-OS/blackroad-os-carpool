# 01 — Vision

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## The Core Thesis

**BlackRoad is the operating system for AI agents.**

Not a chatbot. Not an API wrapper. Not another "chat with GPT" clone.

It's the layer that sits *above* all AI providers and *below* all user workflows — orchestrating, remembering, and creating at scale.

---

## The Problem We Solve

### Current State (Fragmented)

Users today must:
- Juggle multiple AI subscriptions (ChatGPT, Claude, Gemini, etc.)
- Manually copy context between tools
- Set up infrastructure to deploy anything
- Lose all memory when switching between AIs
- Start from scratch with every new conversation

### Future State (BlackRoad)

Users will:
- Connect all their AIs in one place
- Have continuous memory across all interactions
- Train personal models on their own data
- Deploy agents without touching infrastructure
- Never repeat themselves to an AI again

---

## The Three Pillars

### Pillar 1: Bring Your Own Everything (BYO-E)

**What it means:**
- Users connect their existing API keys (OpenAI, Anthropic, Google, xAI)
- Users connect their existing tools (Notion, Slack, Gmail, GitHub, Stripe)
- Users can optionally connect their own infrastructure

**Why it matters:**
- **Cost:** Users pay their own token costs → we don't burn cash on inference
- **Liability:** Users own their data relationships → cleaner legal position
- **Flexibility:** Users get best-of-breed routing → Lucidia picks the right model

**How it works:**
```
User adds API key → Encrypted storage → Lucidia gains new capability
User adds tool OAuth → Token storage → Agents gain new actions
```

### Pillar 2: Local Model Forking (The Continuity Engine)

**What it means:**
- All user interactions create a unified context pool
- Users can fine-tune/LoRA open-source models on their data
- Resulting models become personal "BlackRoad Agents"
- These agents run locally, on BlackRoad cloud, or user's own infra

**Supported base models:**
- LLaMA 3.x (Meta) — General purpose
- Qwen 2.5 (Alibaba) — Multilingual, reasoning
- SmolLM (Hugging Face) — Edge deployment
- Phi-3/Phi-4 (Microsoft) — Efficient reasoning
- Mistral/Mixtral — Open weights, MoE

**The promise:**
> Your AI gets smarter *from you*, not just from training data. Continuity isn't just "memory" — it's model evolution.

### Pillar 3: One-Stop Infrastructure Abstraction

**What it means:**
Users never have to:
- Create a Cloudflare account
- Set up Railway services
- Configure Vercel deployments
- Manage databases or DNS
- Deal with SSL certificates

**BlackRoad handles:**

| User Action | BlackRoad Does |
|-------------|----------------|
| "Deploy my agent" | Railway/Workers provisioning |
| "Store my data" | Postgres + R2 + Vector allocation |
| "Connect my domain" | DNS + SSL + CDN config |
| "Scale up" | Auto-scaling, load balancing |
| "Add a connector" | OAuth flows, webhooks, credentials |

**The promise:**
> One button. One bill. Everything works.

---

## Competitive Positioning

| Competitor | What They Do | What's Missing |
|------------|--------------|----------------|
| **OpenRouter** | Multi-model API routing | No memory, no orchestration, no agents |
| **LangChain/CrewAI** | Agent frameworks | Developer-only, no product, no continuity |
| **Zapier/Make** | Workflow automation | Not AI-native, no model routing |
| **ChatGPT/Claude** | Single-model chat | Walled garden, no multi-AI, no forking |
| **Replit Agent** | AI-assisted coding | Code-only, no general orchestration |
| **Notion AI** | Embedded AI | Locked to Notion platform |

**BlackRoad's unique position:**
> The only platform where you can bring any AI, train your own, orchestrate them together, and never leave to manage infrastructure.

---

## Product Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 4: MARKETPLACE                         │
│  Packs │ Templates │ Pre-trained agents │ Community models      │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 3: CREATION                            │
│  Fork models │ Train on context │ Build agents │ Deploy apps    │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 2: ORCHESTRATION                       │
│  Lucidia routing │ Multi-model coordination │ Tool execution    │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1: CONNECTIONS                         │
│  API keys │ OAuth │ Infrastructure │ Data sources               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Target Users

### Primary: AI Power Users
- Use multiple AI tools daily
- Frustrated by fragmentation
- Willing to pay for unified experience
- Technical enough to understand value of local models

### Secondary: Developers
- Building AI-powered applications
- Want agent orchestration without building infrastructure
- Need multi-model support

### Tertiary: Teams/Enterprises
- Need shared context across team members
- Compliance requirements for data control
- Want to train company-specific models

---

## Business Model

### Revenue Streams

1. **Subscription Tiers**
   - Free: Limited conversations, 1 workspace, 1 model connection
   - Pro ($20/mo): Unlimited conversations, 5 workspaces, all providers
   - Team ($50/user/mo): Shared workspaces, team memory, admin controls
   - Enterprise (custom): SSO, dedicated infra, compliance

2. **Compute Margin**
   - Users can use BlackRoad-managed infrastructure
   - We mark up Railway/Cloudflare costs ~20-30%
   - Optional — BYO infrastructure users skip this

3. **Marketplace Cut**
   - Agents/packs sold on marketplace
   - 15-30% platform fee

4. **Training Jobs**
   - Fine-tuning/LoRA jobs on user data
   - Per-job or subscription pricing

---

## Success Metrics

### North Star
**Monthly Active Workspaces** — Workspaces with 10+ conversations/month

### Supporting Metrics
- API keys connected per workspace
- Models used per conversation (multi-model = stickiness)
- Training jobs initiated
- Time to first value (signup → first meaningful conversation)

---

## One-Line Pitch

> **BlackRoad: Bring any AI. Train your own. Never leave.**
