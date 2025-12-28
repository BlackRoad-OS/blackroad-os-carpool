# CarPool Architecture
**by BlackRoad OS, Inc.**

## Overview

CarPool is a multi-AI orchestration platform that enables users to bring their own AI provider keys, route intelligently between models, and train personalized local models from their context.

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│              (Next.js + Clerk Auth + Tailwind)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CARPOOL API GATEWAY                        │
│                      (FastAPI + Pydantic)                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LUCIDIA ROUTER                             │
│         Task Analysis → Model Selection → Execution             │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐     ┌──────────────┐
│   OpenAI     │    │  Anthropic   │     │   Google     │
│  GPT-4o, o1  │    │ Claude 3.5   │     │  Gemini 2.0  │
└──────────────┘    └──────────────┘     └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      MEMORY SYSTEM                              │
│       Postgres + pgvector + Redis + R2 Storage                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LOCAL MODEL TRAINING                          │
│          LoRA Fine-tuning → User-Personalized Models            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Frontend (Next.js 14 + App Router)

**Location:** `/frontend`

**Tech Stack:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Clerk for authentication
- TanStack Query for data fetching
- Zustand for state management

**Key Features:**
- Server-side rendering for marketing pages
- Client components for interactive workspace
- Real-time streaming chat interface
- API key management UI
- Model selection preferences
- Conversation history browser

**Routes:**
```
/                    → Landing page (marketing)
/docs               → Documentation
/pricing            → Pricing page
/app                → Main workspace (auth required)
/app/chat           → Chat interface
/app/settings       → User settings
/app/providers      → API key management
/app/training       → Local model training queue
```

---

### 2. Backend API (FastAPI)

**Location:** `/backend`

**Tech Stack:**
- FastAPI (async Python)
- Pydantic for validation
- SQLAlchemy + Alembic for database
- JWT verification (Clerk)
- Cryptography for API key encryption

**Endpoints:**

#### Health & Info
- `GET /` - API info
- `GET /health` - Health check

#### Workspace Management
- `POST /api/v1/workspaces` - Create workspace
- `GET /api/v1/workspaces/{id}` - Get workspace
- `PATCH /api/v1/workspaces/{id}` - Update workspace settings

#### Provider Management
- `POST /api/v1/workspaces/{id}/providers` - Add AI provider
- `GET /api/v1/workspaces/{id}/providers` - List providers
- `DELETE /api/v1/workspaces/{id}/providers/{provider}` - Remove provider

#### Chat / Orchestration
- `POST /api/v1/chat` - Send message (Lucidia routes)
- `GET /api/v1/conversations/{id}` - Get conversation
- `GET /api/v1/conversations/{id}/messages` - Get messages

#### Lucidia Router
- `GET /api/v1/lucidia/status` - Router status
- `POST /api/v1/lucidia/analyze` - Analyze task (no execution)

#### Training Queue
- `GET /api/v1/workspaces/{id}/training-queue` - Get training jobs
- `POST /api/v1/training/start` - Start fine-tuning job

---

### 3. Lucidia Router Engine

**Location:** `/backend/lucidia.py`

**Purpose:** The brain of CarPool. Analyzes tasks and intelligently routes to optimal AI model.

**Process:**

```python
1. Task Analysis
   ├─ Token counting
   ├─ Complexity estimation (trivial → expert)
   ├─ Task type classification (chat, code, analysis, etc.)
   └─ Requirement detection (vision, tools, realtime)

2. Model Filtering
   ├─ Available providers (from user config)
   ├─ Capability matching (vision, tools, context)
   └─ Context window validation

3. Model Scoring
   ├─ Quality match (don't use GPT-4 for trivial tasks)
   ├─ Cost efficiency (prefer cheaper when quality sufficient)
   ├─ Speed tier
   └─ User preferences

4. Routing Decision
   ├─ Select highest-scored model
   ├─ Generate reasoning explanation
   ├─ Provide alternatives
   └─ Estimate cost
```

**Example Decision:**

```json
{
  "selected_model": "claude-3-haiku",
  "selected_provider": "anthropic",
  "reasoning": "Selected claude-3-haiku for chat task with simple complexity. Model offers good quality at fast speed, matching task requirements (score: 23.0).",
  "alternatives": ["gpt-4o-mini", "gemini-2.0-flash"],
  "estimated_cost": 0.0001,
  "confidence_score": 23.0
}
```

---

### 4. Database Schema (PostgreSQL + pgvector)

**Migrations:** Alembic

**Tables:**

```sql
-- Users (synced from Clerk)
users (
  id UUID PRIMARY KEY,
  clerk_user_id TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
)

-- Workspaces
workspaces (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name TEXT NOT NULL,
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
)

-- API Keys (encrypted)
api_keys (
  id UUID PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id),
  provider TEXT NOT NULL,  -- openai, anthropic, google, xai
  encrypted_key TEXT NOT NULL,
  enabled BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
)

-- Conversations
conversations (
  id UUID PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id),
  title TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
)

-- Messages
messages (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id),
  role TEXT NOT NULL,  -- user, assistant, system
  content TEXT NOT NULL,
  model_used TEXT,
  tokens_used INTEGER,
  routing_decision JSONB,
  created_at TIMESTAMP DEFAULT NOW()
)

-- Message embeddings (for semantic search)
message_embeddings (
  id UUID PRIMARY KEY,
  message_id UUID REFERENCES messages(id),
  embedding VECTOR(1536),  -- pgvector
  created_at TIMESTAMP DEFAULT NOW()
)

-- Training jobs
training_jobs (
  id UUID PRIMARY KEY,
  workspace_id UUID REFERENCES workspaces(id),
  base_model TEXT NOT NULL,  -- llama-3.1, qwen-2.5, etc.
  status TEXT NOT NULL,  -- queued, running, completed, failed
  config JSONB,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
)
```

---

### 5. Model Adapters

**Purpose:** Unified interface to different AI providers

**Location:** `/backend/adapters/`

**Structure:**

```
adapters/
├─ base.py          → BaseAdapter interface
├─ openai.py        → OpenAI (GPT-4o, o1, etc.)
├─ anthropic.py     → Anthropic (Claude)
├─ google.py        → Google (Gemini)
├─ xai.py           → xAI (Grok)
└─ custom.py        → Custom OpenAI-compatible endpoints
```

**BaseAdapter Interface:**

```python
class BaseAdapter:
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = True,
        **kwargs
    ) -> AsyncIterator[str]:
        raise NotImplementedError

    async def count_tokens(self, text: str) -> int:
        raise NotImplementedError
```

---

### 6. Memory & Context System

**Components:**

1. **Conversation Storage** (Postgres)
   - Full message history
   - Routing decisions logged
   - Token usage tracked

2. **Vector Search** (pgvector)
   - Semantic search across conversations
   - Find similar past interactions
   - Context retrieval for local model training

3. **Cache Layer** (Redis)
   - Recent conversations
   - User preferences
   - Model availability

4. **File Storage** (Cloudflare R2)
   - Uploaded documents
   - Generated images
   - Training datasets

---

### 7. Local Model Training Pipeline

**Process:**

```
1. Context Collection
   ├─ User conversations
   ├─ Tool interactions
   └─ Uploaded documents

2. Dataset Preparation
   ├─ Format conversion
   ├─ Quality filtering
   └─ Deduplication

3. Model Selection
   ├─ LLaMA 3.1 (general)
   ├─ Qwen 2.5 (coding)
   ├─ Phi-3 (small/fast)
   └─ Mistral (efficient)

4. Fine-tuning
   ├─ LoRA adapters
   ├─ Parameter-efficient
   └─ Quality validation

5. Deployment
   ├─ Local (Ollama)
   ├─ BlackRoad cloud
   └─ User infrastructure
```

---

## Security

### API Key Storage
- Encrypted at rest (AES-256)
- Never logged
- Scoped to workspace
- Deletable by user

### Authentication
- Clerk JWT verification
- Row-level security (RLS)
- Rate limiting per workspace

### Data Privacy
- User data isolated by workspace
- Optional local-only mode
- Training jobs use user's own data only

---

## Deployment

### Production Stack

```yaml
Frontend:
  platform: Vercel
  domain: app.blackroad.io
  env: production

Backend API:
  platform: Railway
  domain: api.blackroad.io
  instances: 2+ (auto-scale)
  env: production

Database:
  platform: Railway (Postgres + pgvector)
  backups: daily
  replicas: 1 read replica

Cache:
  platform: Upstash (Redis)
  regions: global

Storage:
  platform: Cloudflare R2
  regions: global

CDN:
  platform: Cloudflare
  domains: *.blackroad.io
```

---

## Monitoring

- **Sentry** - Error tracking
- **Prometheus** - Metrics collection
- **Grafana** - Dashboards
- **Uptime Robot** - Service monitoring

---

## Development Workflow

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Database migrations
cd backend
alembic upgrade head
```

---

**Built by BlackRoad OS, Inc.**
*The OS for AI agents*
