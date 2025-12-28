# 02 — Architecture

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USERS                                          │
│         Web Browser │ Mobile │ API │ CLI │ Partner Apps                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CLOUDFLARE EDGE                                     │
│   DNS │ CDN │ WAF │ DDoS Protection │ SSL Termination                      │
│   Workers (edge functions) │ R2 (object storage) │ D1 (edge DB)            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    ▼                                   ▼
┌───────────────────────────────────┐   ┌───────────────────────────────────┐
│         VERCEL (Frontend)         │   │        RAILWAY (Backend)          │
│                                   │   │                                   │
│  blackroad.io (landing)           │   │  api.blackroad.io                 │
│  app.blackroad.io (workspace)     │   │  ├── Gateway Service              │
│  docs.blackroad.io (docs)         │   │  ├── Auth Service                 │
│                                   │   │  ├── Workspace Service            │
│  Next.js 14 │ React │ TypeScript  │   │  ├── Conversation Service         │
│  Tailwind │ shadcn/ui             │   │  ├── Agent Service                │
│                                   │   │  ├── Training Service             │
│                                   │   │  └── Orchestrator (Lucidia)       │
└───────────────────────────────────┘   └───────────────────────────────────┘
                                                        │
                    ┌───────────────────────────────────┼───────────────────┐
                    ▼                                   ▼                   ▼
┌───────────────────────────┐   ┌───────────────────────────┐   ┌─────────────────┐
│   PostgreSQL (Railway)    │   │     Redis (Railway)       │   │  Cloudflare R2  │
│                           │   │                           │   │                 │
│  Users, Workspaces        │   │  Session cache            │   │  User uploads   │
│  API Keys (encrypted)     │   │  Rate limiting            │   │  Model artifacts│
│  Conversations, Messages  │   │  Job queues               │   │  Training data  │
│  Training jobs            │   │  Pub/sub                  │   │  Backups        │
│  + pgvector (embeddings)  │   │                           │   │                 │
└───────────────────────────┘   └───────────────────────────┘   └─────────────────┘
```

---

## Service Boundaries

### Frontend Services (Vercel)

#### `blackroad.io` — Marketing Site
- **Purpose:** Landing page, pricing, about, blog
- **Tech:** Next.js 14, static generation where possible
- **Auth:** None (public)

#### `app.blackroad.io` — Main Workspace
- **Purpose:** The product — chat, settings, agents, etc.
- **Tech:** Next.js 14, App Router, server components
- **Auth:** Clerk (required)
- **Key routes:**
  ```
  /                    → Dashboard (redirect to /chat)
  /chat                → Conversation interface
  /chat/[id]           → Specific conversation
  /agents              → Agent gallery
  /agents/[id]         → Agent detail/config
  /settings            → Account settings
  /settings/keys       → API key management
  /settings/tools      → Tool connections
  /settings/billing    → Subscription management
  /workspace           → Workspace settings (team plans)
  ```

#### `docs.blackroad.io` — Documentation
- **Purpose:** Technical docs, guides, API reference
- **Tech:** Next.js + MDX or Mintlify
- **Auth:** None (public)

---

### Backend Services (Railway)

#### Gateway Service
- **Purpose:** Request routing, rate limiting, API versioning
- **Endpoints:** All `/api/v1/*` traffic enters here
- **Responsibilities:**
  - Request validation
  - Authentication verification (Clerk JWT)
  - Rate limiting (Redis)
  - Request logging
  - Route to appropriate service

#### Auth Service
- **Purpose:** Clerk webhook handling, user sync
- **Endpoints:**
  ```
  POST /api/v1/auth/webhook    → Clerk webhook receiver
  GET  /api/v1/auth/me         → Current user details
  ```

#### Workspace Service
- **Purpose:** Workspace CRUD, membership, settings
- **Endpoints:**
  ```
  GET    /api/v1/workspaces              → List user's workspaces
  POST   /api/v1/workspaces              → Create workspace
  GET    /api/v1/workspaces/:id          → Get workspace
  PATCH  /api/v1/workspaces/:id          → Update workspace
  DELETE /api/v1/workspaces/:id          → Delete workspace
  POST   /api/v1/workspaces/:id/members  → Add member (team plans)
  ```

#### Keys Service
- **Purpose:** API key management (encrypted storage)
- **Endpoints:**
  ```
  GET    /api/v1/keys                    → List connected providers
  POST   /api/v1/keys                    → Add API key
  DELETE /api/v1/keys/:provider          → Remove API key
  POST   /api/v1/keys/:provider/test     → Test API key validity
  ```

#### Conversation Service
- **Purpose:** Chat CRUD, message storage
- **Endpoints:**
  ```
  GET    /api/v1/conversations           → List conversations
  POST   /api/v1/conversations           → Create conversation
  GET    /api/v1/conversations/:id       → Get conversation + messages
  DELETE /api/v1/conversations/:id       → Delete conversation
  POST   /api/v1/conversations/:id/messages → Add message (triggers orchestrator)
  ```

#### Agent Service
- **Purpose:** Agent CRUD, configuration
- **Endpoints:**
  ```
  GET    /api/v1/agents                  → List available agents
  POST   /api/v1/agents                  → Create custom agent
  GET    /api/v1/agents/:id              → Get agent config
  PATCH  /api/v1/agents/:id              → Update agent
  DELETE /api/v1/agents/:id              → Delete agent
  ```

#### Training Service
- **Purpose:** Model fine-tuning jobs
- **Endpoints:**
  ```
  GET    /api/v1/training/jobs           → List training jobs
  POST   /api/v1/training/jobs           → Start training job
  GET    /api/v1/training/jobs/:id       → Get job status
  DELETE /api/v1/training/jobs/:id       → Cancel job
  ```

#### Orchestrator (Lucidia Core)
- **Purpose:** The brain — routes requests to appropriate models
- **Internal service:** Not directly exposed via API
- **Responsibilities:**
  - Analyze incoming message
  - Determine best model(s) for task
  - Execute model call(s)
  - Aggregate responses
  - Update memory/context
  - Trigger tool calls if needed

---

## Data Flow: Send Message

```
1. User types message in app.blackroad.io
                    │
                    ▼
2. Frontend POST /api/v1/conversations/:id/messages
   Body: { content: "...", attachments: [...] }
                    │
                    ▼
3. Gateway validates JWT, rate limits, routes to Conversation Service
                    │
                    ▼
4. Conversation Service:
   - Stores user message in DB
   - Loads conversation context
   - Loads workspace API keys (decrypted)
   - Calls Orchestrator
                    │
                    ▼
5. Orchestrator (Lucidia):
   - Analyzes message intent
   - Checks available models (from user's keys)
   - Selects optimal model for task
   - Formats prompt with context
   - Calls external API (OpenAI/Anthropic/etc.)
                    │
                    ▼
6. External API returns response (streamed)
                    │
                    ▼
7. Orchestrator:
   - Streams response to frontend via SSE/WebSocket
   - Stores assistant message in DB
   - Updates context/embeddings
   - Optionally triggers tool calls
                    │
                    ▼
8. Frontend renders streaming response
```

---

## Authentication Flow

```
1. User visits app.blackroad.io
                    │
                    ▼
2. Clerk middleware checks for session
   - If no session → redirect to /sign-in
   - If session → continue
                    │
                    ▼
3. Frontend makes API call with Clerk JWT in header
   Authorization: Bearer <clerk_jwt>
                    │
                    ▼
4. Gateway verifies JWT with Clerk public keys
   - Invalid → 401 Unauthorized
   - Valid → extract user_id, continue
                    │
                    ▼
5. Service uses user_id for authorization checks
   - Is this user's workspace?
   - Does user have permission?
```

---

## Key Encryption

API keys are stored encrypted at rest:

```
1. User submits API key via frontend
                    │
                    ▼
2. Frontend sends key to /api/v1/keys
   (over HTTPS, key in request body)
                    │
                    ▼
3. Keys Service encrypts key using:
   - Algorithm: AES-256-GCM
   - Key: derived from ENCRYPTION_SECRET env var
   - Each key gets unique IV
                    │
                    ▼
4. Encrypted key stored in PostgreSQL
   {
     provider: "openai",
     encrypted_key: "...",
     iv: "...",
     key_hint: "sk-...abc" (last 3 chars for UI)
   }
                    │
                    ▼
5. When needed, Keys Service decrypts on-demand
   - Decrypted keys never logged
   - Decrypted keys never stored in cache
```

---

## Scaling Considerations

### Current (MVP)
- Single Railway instance per service
- Single Postgres database
- Vertical scaling as needed

### Future (Scale)
- Kubernetes/Railway autoscaling
- Read replicas for Postgres
- Connection pooling (PgBouncer)
- Dedicated Redis cluster
- Regional edge workers

### Bottleneck Points
1. **Orchestrator** — CPU-bound (prompt processing)
   - Solution: Horizontal scaling, queue-based processing
2. **Database** — Write-heavy (messages)
   - Solution: Partitioning by workspace, read replicas
3. **External APIs** — Rate limits
   - Solution: User's own keys, queue overflow

---

## Environment Variables

### Frontend (Vercel)
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_API_URL=https://api.blackroad.io
```

### Backend (Railway)
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
CLERK_SECRET_KEY=sk_...
ENCRYPTION_SECRET=<32-byte-hex>
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET_NAME=blackroad-storage
```

---

## Repository Structure

```
BlackRoad-OS/
├── blackroad-os-web/          # Next.js frontend (Vercel)
│   ├── app/
│   │   ├── (marketing)/       # Public pages
│   │   ├── (app)/             # Authenticated app
│   │   └── api/               # API routes (minimal, mostly proxy)
│   ├── components/
│   ├── lib/
│   └── package.json
│
├── blackroad-os-api/          # Backend services (Railway)
│   ├── src/
│   │   ├── gateway/
│   │   ├── services/
│   │   │   ├── auth/
│   │   │   ├── workspace/
│   │   │   ├── keys/
│   │   │   ├── conversation/
│   │   │   ├── agent/
│   │   │   └── training/
│   │   ├── orchestrator/      # Lucidia core
│   │   └── shared/
│   ├── prisma/                # Or SQLAlchemy models
│   └── pyproject.toml         # Or package.json
│
├── blackroad-os-infra/        # Infrastructure as Code
│   ├── terraform/
│   └── pulumi/
│
└── blackroad-os-docs/         # Documentation
    └── ...
```
