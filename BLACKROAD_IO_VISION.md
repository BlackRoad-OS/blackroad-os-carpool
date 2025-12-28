# BlackRoad.io Vision Document

**Last Updated:** 2025-12-28
**Status:** Canonical Product Specification
**Owner:** Alexa Amundson

---

## The Core Thesis

**BlackRoad is the operating system for AI agents.**

Not a chatbot. Not an API wrapper. Not another "chat with GPT" clone.

It's the layer that sits *above* all AI providers and *below* all user workflows — orchestrating, remembering, and creating at scale.

---

## The Three Pillars

### 1. **BRING YOUR OWN EVERYTHING (BYO-E)**

Users connect their own:
- **Model Keys**: OpenAI, Anthropic, Google (Gemini), xAI (Grok)
- **Tool Keys**: Notion, Slack, Gmail, Stripe, GitHub, etc.
- **Infrastructure**: Or we abstract it entirely (see Pillar 3)

**Why this matters:**
- User pays their own token costs → we're not burning cash on inference
- User owns their data relationships → cleaner liability
- User gets best-of-breed routing → Lucidia picks the right model for each task

### 2. **LOCAL MODEL FORKING (The Continuity Engine)**

This is the differentiator nobody else is doing well:

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER'S CONTEXT POOL                         │
│  All conversations │ All documents │ All tool outputs           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BLACKROAD DISTILLATION                       │
│  Fine-tune / LoRA / RAG-index into:                            │
│  • LLaMA 3.x fork    → "Your personal LLaMA"                   │
│  • Qwen fork         → "Your personal Qwen"                    │
│  • SmolLM fork       → "Your edge-deployable agent"            │
│  • Phi-3 fork        → "Your local reasoning engine"           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BLACKROAD AGENT FLEET                         │
│  These forked models become YOUR agents:                        │
│  • Run locally (Ollama/vLLM)                                   │
│  • Run on BlackRoad cloud                                      │
│  • Run on your own infra                                       │
│  • THEY REMEMBER EVERYTHING                                    │
└─────────────────────────────────────────────────────────────────┘
```

**The promise:** Your AI gets smarter *from you*, not just from OpenAI's training data. Continuity isn't just "memory" — it's model evolution.

### 3. **ONE-STOP INFRASTRUCTURE ABSTRACTION**

Users should never have to:
- Create a Cloudflare account
- Set up Railway
- Configure Vercel
- Manage databases
- Deal with DNS

**BlackRoad handles:**

| User Sees | BlackRoad Handles |
|-----------|-------------------|
| "Deploy my agent" | Railway/Cloudflare Workers provisioning |
| "Store my data" | Postgres + R2 + Vector DB allocation |
| "Connect my domain" | DNS + SSL + CDN configuration |
| "Scale up" | Auto-scaling, load balancing |
| "Add a connector" | OAuth flows, webhook setup, credential storage |

**The abstraction:** One button. One bill. Everything works.

---

## The Product Layers

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

## Competitive Positioning

| Competitor | What They Do | What's Missing |
|------------|--------------|----------------|
| **OpenRouter** | Multi-model API routing | No memory, no orchestration, no agents |
| **LangChain/CrewAI** | Agent frameworks | Developer-only, no product, no continuity |
| **Zapier/Make** | Workflow automation | Not AI-native, no model routing |
| **ChatGPT/Claude** | Single-model excellence | Walled garden, no multi-AI, no forking |
| **Replit Agent** | AI-assisted coding | Code-only, no general orchestration |
| **Notion AI / Coda AI** | Embedded AI | Locked to their platform |

**BlackRoad's unique position:**
> The only platform where you can bring any AI, train your own, orchestrate them together, and never leave to manage infrastructure.

---

## Day 1 MVP vs Full Vision

### MVP (Today's Push)
1. Landing page at blackroad.io that sells the vision
2. Auth (Clerk) + API key input (OpenAI, Anthropic, Gemini, xAI)
3. Basic chat with Lucidia that routes between connected models
4. Conversation memory (Postgres)
5. Single "workspace" per user

### Phase 2 (January)
- Tool connectors (Notion, Slack, GitHub, Gmail)
- Multiple workspaces
- Agent gallery

### Phase 3 (February)
- Local model forking UI
- LoRA training on user context
- Deploy your own agent

### Phase 4 (March)
- One-click infrastructure provisioning
- Marketplace for packs/agents
- Team workspaces

---

## Technical Specifications

### Stack

```yaml
frontend: Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui
backend: FastAPI (Python) or Node.js + Hono
database: PostgreSQL (Railway) + pgvector for embeddings
cache: Redis (Railway or Upstash)
storage: Cloudflare R2
auth: Clerk
payments: Stripe
hosting:
  frontend: Vercel
  backend: Railway
  edge: Cloudflare Workers
  dns: Cloudflare
```

### Domains

- `blackroad.io` - Landing + marketing
- `app.blackroad.io` - Main workspace
- `api.blackroad.io` - Backend gateway
- `docs.blackroad.io` - Documentation

### API Key Providers

- **OpenAI**: GPT-4, GPT-4o, o1, etc.
- **Anthropic**: Claude 3.5/4
- **Google**: Gemini 1.5/2.0
- **xAI**: Grok
- **Custom**: Any OpenAI-compatible endpoint

### Local Model Targets

- **LLaMA 3.x** (Meta)
- **Qwen 2.5** (Alibaba)
- **SmolLM** (Hugging Face)
- **Phi-3/Phi-4** (Microsoft)
- **Mistral/Mixtral** (Mistral AI)

### Orchestration Pattern

1. User message → Lucidia classifier
2. Classifier determines: task type, complexity, required capabilities
3. Router selects: best available model from user's connected providers
4. Execution: stream response, log to memory, update context
5. Optional: trigger tool calls, update local model training queue

### Database Schema

```sql
-- Core tables
users (id, email, created_at)
workspaces (id, user_id, name, settings)
api_keys (id, workspace_id, provider, encrypted_key, created_at)
conversations (id, workspace_id, title, created_at)
messages (id, conversation_id, role, content, model_used, tokens, created_at)
tool_connections (id, workspace_id, tool_type, oauth_tokens, created_at)
training_jobs (id, workspace_id, base_model, status, created_at)
```

### Brand

```yaml
colors:
  primary: "#FF9D08"    # orange
  secondary: "#FF0066"  # pink
  accent: "#7780FF"     # purple
  highlight: "#0866FF"  # blue
theme: dark mode default
voice: confident, technical, slightly irreverent
```

---

## One-Line Pitch

> **BlackRoad: Bring any AI. Train your own. Never leave.**

---

## Implementation Notes

### Current Infrastructure
- GitHub: BlackRoad-OS organization (66 repos across 15 orgs)
- Cloudflare: 16 zones, 8 Pages, 8 KV, 1 D1
- Railway: 12+ projects
- DigitalOcean: 159.65.43.12 (codex-infinity)
- Raspberry Pi: Multiple devices for edge testing

### Integration Points
- Memory System: `~/memory-system.sh` for coordination
- Codex: 8,789+ components for reuse
- GreenLight: Project traffic light system
- Task Marketplace: `~/memory-task-marketplace.sh`

### Next Actions
1. Create landing page wireframe
2. Set up Clerk auth flow
3. Build API key management UI
4. Implement Lucidia router backend
5. Deploy MVP to app.blackroad.io
