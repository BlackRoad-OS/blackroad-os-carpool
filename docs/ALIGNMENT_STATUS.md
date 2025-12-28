# CarPool ↔ BlackRoad Docs Alignment Status

**Last Updated:** 2025-12-28
**Repository:** https://github.com/BlackRoad-OS/blackroad-os-carpool

---

## Overview

This document tracks alignment between the CarPool codebase and the comprehensive BlackRoad documentation suite found in `/docs`.

**Purpose:** Ensure all implementation matches the canonical specifications in docs 01-10.

---

## Alignment Summary

| Component | Doc Reference | Status | Notes |
|-----------|---------------|--------|-------|
| Database Schema | 03-DATABASE-SCHEMA.md | ⚠️ Partial | `database.py` needs workspace_members, tool_connections, agents tables |
| API Endpoints | 04-API-CONTRACTS.md | ⚠️ Partial | `main.py` has scaffolds, needs full implementation |
| Lucidia Router | 01-VISION.md, 02-ARCHITECTURE.md | ✅ Aligned | Core routing logic matches vision |
| Frontend Structure | 02-ARCHITECTURE.md, 06-COMPONENTS.md | 🔄 Planned | `frontend/package.json` exists, needs full build-out |
| Authentication | 02-ARCHITECTURE.md | 🔄 Planned | Clerk integration defined, not implemented |
| Deployment | 08-DEPLOYMENT.md | 🔄 Planned | Railway/Vercel configs needed |

**Legend:**
- ✅ Aligned - Implementation matches docs
- ⚠️ Partial - Started but incomplete
- 🔄 Planned - Not started, documented
- ❌ Mismatch - Implementation differs from docs

---

## Database Schema Alignment

### ✅ Already Implemented

From `backend/database.py`:

```python
✅ User           # Matches 03-DATABASE-SCHEMA.md
✅ Workspace      # Matches (missing slug field)
✅ APIKey         # Matches (missing endpoint_url, last_tested_at)
✅ Conversation   # Matches (missing agent_id reference)
✅ Message        # Matches (missing provider_used, tool_calls, tool_results)
✅ MessageEmbedding  # Matches
✅ TrainingJob    # Matches
```

### ⚠️ Missing Tables

Need to add from 03-DATABASE-SCHEMA.md:

```python
❌ WorkspaceMember   # For team plans
❌ ToolConnection    # OAuth tokens for Notion, Slack, etc.
❌ Agent             # Custom agents
❌ ModelFork         # Deployed trained models
```

### 🔧 Fields to Add

**Workspace:**
- `slug` (unique, for URLs like `app.blackroad.io/w/my-workspace`)
- `plan` (free, pro, team, enterprise)

**APIKey:**
- `endpoint_url` (for custom providers like Ollama)
- `is_valid` (track if key works)
- `last_tested_at` (last validation timestamp)

**Conversation:**
- `agent_id` (reference to Agent table)
- `is_archived` (soft delete)

**Message:**
- `provider_used` (openai, anthropic, google, xai)
- `tool_calls` (JSONB - function calling requests)
- `tool_results` (JSONB - function calling responses)
- `latency_ms` (response time tracking)

---

## API Endpoints Alignment

### ✅ Scaffolds Exist

From `backend/main.py`:

```
✅ GET  /
✅ GET  /health
✅ POST /api/v1/workspaces
✅ GET  /api/v1/workspaces/:id
✅ POST /api/v1/workspaces/:id/providers
✅ GET  /api/v1/workspaces/:id/providers
✅ POST /api/v1/chat
✅ GET  /api/v1/conversations/:id
✅ GET  /api/v1/lucidia/status
✅ GET  /api/v1/workspaces/:id/training-queue
```

### ⚠️ Need Full Implementation

Per 04-API-CONTRACTS.md, need to add:

```
❌ GET    /auth/me
❌ GET    /workspaces
❌ PATCH  /workspaces/:id
❌ DELETE /workspaces/:id
❌ POST   /workspaces/:id/members (team plans)

❌ DELETE /workspaces/:id/keys/:provider
❌ POST   /workspaces/:id/keys/:provider/test

❌ GET    /workspaces/:id/conversations (list)
❌ POST   /workspaces/:id/conversations
❌ DELETE /workspaces/:id/conversations/:id
❌ POST   /workspaces/:id/conversations/:id/messages (STREAMING)

❌ GET    /agents
❌ POST   /workspaces/:id/agents
❌ GET    /agents/:id
❌ PATCH  /workspaces/:id/agents/:id
❌ DELETE /workspaces/:id/agents/:id

❌ POST   /workspaces/:id/training/jobs
❌ GET    /workspaces/:id/training/jobs/:id
❌ DELETE /workspaces/:id/training/jobs/:id

❌ GET    /workspaces/:id/models
❌ POST   /workspaces/:id/models/:id/deploy
❌ DELETE /workspaces/:id/models/:id/deploy
```

### 🔧 Streaming Implementation

Per 04-API-CONTRACTS.md:

- Message endpoint should support Server-Sent Events (SSE)
- Events: `message_start`, `content_delta`, `message_end`
- Query param: `?stream=false` for non-streaming

---

## Lucidia Router Alignment

### ✅ Fully Aligned

From `backend/lucidia.py`:

**Matches 01-VISION.md and 02-ARCHITECTURE.md:**

✅ Task complexity classification (trivial → expert)
✅ Task type classification (chat, code, analysis, creative, multimodal, reasoning, realtime)
✅ Model capability database (OpenAI, Anthropic, Google, xAI)
✅ Scoring algorithm (quality match, cost efficiency, speed tier)
✅ Routing decision with reasoning
✅ Support for user preferences
✅ Token counting with tiktoken

**Philosophy: "Don't use GPT-4 for trivial tasks"** — ✅ Implemented

---

## Frontend Alignment

### 🔄 Planned

Per 02-ARCHITECTURE.md, need Next.js app with routes:

```
/ → Landing page
/docs → Documentation
/pricing → Pricing
/app → Main workspace (auth required)
/app/chat → Chat interface
/app/chat/:id → Specific conversation
/app/agents → Agent gallery
/app/settings → Account settings
/app/settings/keys → API key management
/app/settings/tools → Tool connections
/app/settings/billing → Subscription
/app/workspace → Team settings
```

### Current Status

- ✅ `frontend/package.json` created with dependencies
- ❌ No routes implemented yet
- ❌ No components created yet
- ❌ Clerk auth not configured

See 06-COMPONENTS.md for full component inventory needed.

---

## Authentication Alignment

### 🔄 Planned

Per 02-ARCHITECTURE.md:

**Flow:**
1. User visits app.blackroad.io
2. Clerk middleware checks session
3. Frontend includes JWT in API calls: `Authorization: Bearer <token>`
4. Gateway verifies JWT with Clerk public keys
5. Extract `user_id`, authorize request

**Current Status:**
- ❌ Clerk not configured in frontend
- ❌ JWT verification not implemented in backend
- ❌ User sync webhook not implemented

---

## Model Adapters Alignment

### ⚠️ Not Started

Per 02-ARCHITECTURE.md, need adapters in `backend/adapters/`:

```
❌ base.py → BaseAdapter interface
❌ openai.py → OpenAI (GPT-4o, o1)
❌ anthropic.py → Anthropic (Claude)
❌ google.py → Google (Gemini)
❌ xai.py → xAI (Grok)
❌ custom.py → Custom OpenAI-compatible
```

**Required Interface:**

```python
class BaseAdapter:
    async def chat(messages, model, stream=True, **kwargs) -> AsyncIterator[str]
    async def count_tokens(text: str) -> int
```

---

## Encryption Alignment

### ⚠️ Partially Defined

Per 02-ARCHITECTURE.md:

**Specification:**
- Algorithm: AES-256-GCM
- Key: derived from `ENCRYPTION_SECRET` env var
- Each key gets unique IV (initialization vector)
- Decrypted keys never logged or cached

**Current Status:**
- ❌ Encryption functions not implemented
- ✅ Database has `encrypted_key` and `iv` fields
- ❌ `.env.example` has `ENCRYPTION_KEY` placeholder

Need to implement in `backend/crypto.py` or similar.

---

## Deployment Alignment

### 🔄 Not Started

Per 08-DEPLOYMENT.md, need:

```
❌ Railway configuration for backend
❌ Vercel configuration for frontend
❌ Cloudflare R2 setup
❌ Cloudflare Workers (edge functions)
❌ Environment variable documentation
❌ CI/CD pipelines
❌ Database migration scripts
```

---

## Priority Action Items

### Phase 1: Database Completion

1. Add missing tables to `database.py`:
   - `WorkspaceMember`
   - `ToolConnection`
   - `Agent`
   - `ModelFork`

2. Add missing fields:
   - `Workspace.slug`, `Workspace.plan`
   - `APIKey.endpoint_url`, `APIKey.is_valid`, `APIKey.last_tested_at`
   - `Conversation.agent_id`, `Conversation.is_archived`
   - `Message.provider_used`, `Message.tool_calls`, `Message.tool_results`, `Message.latency_ms`

3. Create Alembic migration

### Phase 2: API Implementation

1. Implement Clerk JWT verification
2. Implement User sync webhook (`POST /auth/webhook`)
3. Complete CRUD endpoints per 04-API-CONTRACTS.md
4. Implement SSE streaming for chat
5. Add rate limiting (Redis)

### Phase 3: Model Adapters

1. Create `backend/adapters/base.py`
2. Implement OpenAI adapter
3. Implement Anthropic adapter
4. Implement Google adapter
5. Implement xAI adapter
6. Integrate adapters with Lucidia

### Phase 4: Encryption

1. Create `backend/crypto.py`
2. Implement AES-256-GCM encryption/decryption
3. Update API key storage to use encryption
4. Update tool connection storage to use encryption

### Phase 5: Frontend

1. Set up Clerk auth in Next.js
2. Build routes per 02-ARCHITECTURE.md
3. Implement components per 06-COMPONENTS.md
4. Connect to backend API
5. Implement streaming chat UI

### Phase 6: Deployment

1. Create Railway project
2. Configure Postgres + pgvector
3. Configure Redis
4. Deploy backend to Railway
5. Deploy frontend to Vercel
6. Configure custom domains

---

## Conclusion

**Current State:** Strong foundation with Lucidia router and database schema scaffolds.

**Next Steps:** Complete database schema, implement full API contracts, build model adapters.

**Documentation Quality:** Excellent — docs 01-10 provide comprehensive specifications.

**Recommendation:** Use this alignment doc to track progress as we build toward MVP.

---

**Generated:** 2025-12-28
**By:** Claude Code (CarPool integration session)
**Repository:** https://github.com/BlackRoad-OS/blackroad-os-carpool
