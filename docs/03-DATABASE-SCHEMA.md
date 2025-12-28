# 03 — Database Schema

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

BlackRoad uses PostgreSQL with pgvector extension for embeddings.

**Database:** Railway PostgreSQL  
**ORM:** Prisma (TypeScript) or SQLAlchemy (Python)  
**Migrations:** Managed via ORM

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    users    │───┬───│   workspaces    │───────│ workspace_      │
│             │   │   │                 │       │ members         │
└─────────────┘   │   └─────────────────┘       └─────────────────┘
                  │            │
                  │            ├────────────────────────────┐
                  │            │                            │
                  │            ▼                            ▼
                  │   ┌─────────────────┐         ┌─────────────────┐
                  │   │    api_keys     │         │  conversations  │
                  │   │                 │         │                 │
                  │   └─────────────────┘         └─────────────────┘
                  │                                        │
                  │                                        ▼
                  │                               ┌─────────────────┐
                  │                               │    messages     │
                  │                               │                 │
                  │                               └─────────────────┘
                  │
                  │   ┌─────────────────┐         ┌─────────────────┐
                  ├───│ tool_connections│         │     agents      │
                  │   │                 │         │                 │
                  │   └─────────────────┘         └─────────────────┘
                  │
                  │   ┌─────────────────┐         ┌─────────────────┐
                  └───│  training_jobs  │         │  model_forks    │
                      │                 │         │                 │
                      └─────────────────┘         └─────────────────┘
```

---

## Tables

### users

Synced from Clerk via webhook. Minimal local storage.

```sql
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clerk_id        VARCHAR(255) UNIQUE NOT NULL,
  email           VARCHAR(255) NOT NULL,
  name            VARCHAR(255),
  avatar_url      TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_clerk_id ON users(clerk_id);
CREATE INDEX idx_users_email ON users(email);
```

### workspaces

A workspace is the primary container for all user data.

```sql
CREATE TABLE workspaces (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name            VARCHAR(255) NOT NULL,
  slug            VARCHAR(255) UNIQUE NOT NULL,
  owner_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan            VARCHAR(50) DEFAULT 'free',  -- free, pro, team, enterprise
  settings        JSONB DEFAULT '{}',
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_workspaces_owner ON workspaces(owner_id);
CREATE INDEX idx_workspaces_slug ON workspaces(slug);
```

### workspace_members

For team plans — maps users to workspaces with roles.

```sql
CREATE TABLE workspace_members (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role            VARCHAR(50) DEFAULT 'member',  -- owner, admin, member
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(workspace_id, user_id)
);

CREATE INDEX idx_workspace_members_workspace ON workspace_members(workspace_id);
CREATE INDEX idx_workspace_members_user ON workspace_members(user_id);
```

### api_keys

Encrypted storage for user's model provider API keys.

```sql
CREATE TABLE api_keys (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  provider        VARCHAR(50) NOT NULL,  -- openai, anthropic, google, xai, custom
  encrypted_key   TEXT NOT NULL,
  iv              VARCHAR(255) NOT NULL,  -- Initialization vector for AES
  key_hint        VARCHAR(10),            -- Last 3 chars for UI display
  endpoint_url    TEXT,                   -- For custom providers (Ollama, etc.)
  is_valid        BOOLEAN DEFAULT true,
  last_tested_at  TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(workspace_id, provider)
);

CREATE INDEX idx_api_keys_workspace ON api_keys(workspace_id);
```

### tool_connections

OAuth tokens for connected tools (Notion, Slack, etc.).

```sql
CREATE TABLE tool_connections (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  tool_type       VARCHAR(50) NOT NULL,  -- notion, slack, gmail, github, stripe
  access_token    TEXT NOT NULL,         -- Encrypted
  refresh_token   TEXT,                  -- Encrypted
  token_iv        VARCHAR(255) NOT NULL,
  expires_at      TIMESTAMPTZ,
  scopes          TEXT[],
  metadata        JSONB DEFAULT '{}',    -- Tool-specific data
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(workspace_id, tool_type)
);

CREATE INDEX idx_tool_connections_workspace ON tool_connections(workspace_id);
```

### conversations

A conversation is a chat thread.

```sql
CREATE TABLE conversations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  title           VARCHAR(255),
  agent_id        UUID REFERENCES agents(id),  -- Optional: specific agent
  settings        JSONB DEFAULT '{}',          -- Model preferences, etc.
  is_archived     BOOLEAN DEFAULT false,
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conversations_workspace ON conversations(workspace_id);
CREATE INDEX idx_conversations_updated ON conversations(updated_at DESC);
```

### messages

Individual messages within a conversation.

```sql
CREATE TABLE messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role            VARCHAR(20) NOT NULL,  -- user, assistant, system, tool
  content         TEXT NOT NULL,
  model_used      VARCHAR(100),          -- e.g., "gpt-4o", "claude-3-5-sonnet"
  provider_used   VARCHAR(50),           -- e.g., "openai", "anthropic"
  tokens_input    INTEGER,
  tokens_output   INTEGER,
  latency_ms      INTEGER,
  tool_calls      JSONB,                 -- If assistant made tool calls
  tool_results    JSONB,                 -- If this is a tool response
  metadata        JSONB DEFAULT '{}',
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);
```

### message_embeddings

Vector embeddings for semantic search / RAG.

```sql
-- Requires: CREATE EXTENSION vector;

CREATE TABLE message_embeddings (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id      UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  embedding       vector(1536),  -- OpenAI ada-002 dimension
  model_used      VARCHAR(100) DEFAULT 'text-embedding-ada-002',
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_message_embeddings_message ON message_embeddings(message_id);
CREATE INDEX idx_message_embeddings_vector ON message_embeddings 
  USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### agents

Custom agents created by users.

```sql
CREATE TABLE agents (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID REFERENCES workspaces(id) ON DELETE CASCADE,  -- NULL = system agent
  name            VARCHAR(255) NOT NULL,
  description     TEXT,
  avatar_url      TEXT,
  system_prompt   TEXT,
  model_config    JSONB DEFAULT '{}',    -- Preferred model, temperature, etc.
  tools_enabled   TEXT[],                -- Which tools this agent can use
  is_public       BOOLEAN DEFAULT false, -- Marketplace listing
  is_system       BOOLEAN DEFAULT false, -- Built-in agents (Lucidia, etc.)
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_agents_workspace ON agents(workspace_id);
CREATE INDEX idx_agents_public ON agents(is_public) WHERE is_public = true;
```

### training_jobs

Track fine-tuning / LoRA jobs.

```sql
CREATE TABLE training_jobs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  base_model      VARCHAR(100) NOT NULL,  -- llama-3-8b, qwen-2.5-7b, etc.
  status          VARCHAR(50) DEFAULT 'pending',  -- pending, running, completed, failed
  config          JSONB NOT NULL,         -- Training hyperparameters
  input_data_uri  TEXT,                   -- R2 path to training data
  output_model_uri TEXT,                  -- R2 path to trained model
  metrics         JSONB,                  -- Loss, accuracy, etc.
  error_message   TEXT,
  started_at      TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_training_jobs_workspace ON training_jobs(workspace_id);
CREATE INDEX idx_training_jobs_status ON training_jobs(status);
```

### model_forks

User's trained models (results of training jobs).

```sql
CREATE TABLE model_forks (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  training_job_id UUID REFERENCES training_jobs(id),
  name            VARCHAR(255) NOT NULL,
  base_model      VARCHAR(100) NOT NULL,
  model_uri       TEXT NOT NULL,          -- R2 path or external URL
  adapter_type    VARCHAR(50),            -- lora, qlora, full
  is_deployed     BOOLEAN DEFAULT false,
  endpoint_url    TEXT,                   -- If deployed, the inference URL
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_model_forks_workspace ON model_forks(workspace_id);
```

---

## Prisma Schema (TypeScript)

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  clerkId   String   @unique @map("clerk_id")
  email     String
  name      String?
  avatarUrl String?  @map("avatar_url")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  ownedWorkspaces   Workspace[]
  workspaceMemberships WorkspaceMember[]
  
  @@map("users")
}

model Workspace {
  id        String   @id @default(uuid())
  name      String
  slug      String   @unique
  ownerId   String   @map("owner_id")
  plan      String   @default("free")
  settings  Json     @default("{}")
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  owner         User              @relation(fields: [ownerId], references: [id], onDelete: Cascade)
  members       WorkspaceMember[]
  apiKeys       ApiKey[]
  toolConnections ToolConnection[]
  conversations Conversation[]
  agents        Agent[]
  trainingJobs  TrainingJob[]
  modelForks    ModelFork[]
  
  @@map("workspaces")
}

model WorkspaceMember {
  id          String   @id @default(uuid())
  workspaceId String   @map("workspace_id")
  userId      String   @map("user_id")
  role        String   @default("member")
  createdAt   DateTime @default(now()) @map("created_at")

  workspace Workspace @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  user      User      @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  @@unique([workspaceId, userId])
  @@map("workspace_members")
}

model ApiKey {
  id           String    @id @default(uuid())
  workspaceId  String    @map("workspace_id")
  provider     String
  encryptedKey String    @map("encrypted_key")
  iv           String
  keyHint      String?   @map("key_hint")
  endpointUrl  String?   @map("endpoint_url")
  isValid      Boolean   @default(true) @map("is_valid")
  lastTestedAt DateTime? @map("last_tested_at")
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")

  workspace Workspace @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  
  @@unique([workspaceId, provider])
  @@map("api_keys")
}

model Conversation {
  id          String   @id @default(uuid())
  workspaceId String   @map("workspace_id")
  title       String?
  agentId     String?  @map("agent_id")
  settings    Json     @default("{}")
  isArchived  Boolean  @default(false) @map("is_archived")
  createdAt   DateTime @default(now()) @map("created_at")
  updatedAt   DateTime @updatedAt @map("updated_at")

  workspace Workspace @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  agent     Agent?    @relation(fields: [agentId], references: [id])
  messages  Message[]
  
  @@map("conversations")
}

model Message {
  id             String   @id @default(uuid())
  conversationId String   @map("conversation_id")
  role           String
  content        String
  modelUsed      String?  @map("model_used")
  providerUsed   String?  @map("provider_used")
  tokensInput    Int?     @map("tokens_input")
  tokensOutput   Int?     @map("tokens_output")
  latencyMs      Int?     @map("latency_ms")
  toolCalls      Json?    @map("tool_calls")
  toolResults    Json?    @map("tool_results")
  metadata       Json     @default("{}")
  createdAt      DateTime @default(now()) @map("created_at")

  conversation Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  @@map("messages")
}

model Agent {
  id           String   @id @default(uuid())
  workspaceId  String?  @map("workspace_id")
  name         String
  description  String?
  avatarUrl    String?  @map("avatar_url")
  systemPrompt String?  @map("system_prompt")
  modelConfig  Json     @default("{}") @map("model_config")
  toolsEnabled String[] @map("tools_enabled")
  isPublic     Boolean  @default(false) @map("is_public")
  isSystem     Boolean  @default(false) @map("is_system")
  createdAt    DateTime @default(now()) @map("created_at")
  updatedAt    DateTime @updatedAt @map("updated_at")

  workspace     Workspace?     @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  conversations Conversation[]
  
  @@map("agents")
}

model TrainingJob {
  id             String    @id @default(uuid())
  workspaceId    String    @map("workspace_id")
  baseModel      String    @map("base_model")
  status         String    @default("pending")
  config         Json
  inputDataUri   String?   @map("input_data_uri")
  outputModelUri String?   @map("output_model_uri")
  metrics        Json?
  errorMessage   String?   @map("error_message")
  startedAt      DateTime? @map("started_at")
  completedAt    DateTime? @map("completed_at")
  createdAt      DateTime  @default(now()) @map("created_at")

  workspace  Workspace   @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  modelForks ModelFork[]
  
  @@map("training_jobs")
}

model ModelFork {
  id            String   @id @default(uuid())
  workspaceId   String   @map("workspace_id")
  trainingJobId String?  @map("training_job_id")
  name          String
  baseModel     String   @map("base_model")
  modelUri      String   @map("model_uri")
  adapterType   String?  @map("adapter_type")
  isDeployed    Boolean  @default(false) @map("is_deployed")
  endpointUrl   String?  @map("endpoint_url")
  createdAt     DateTime @default(now()) @map("created_at")

  workspace   Workspace    @relation(fields: [workspaceId], references: [id], onDelete: Cascade)
  trainingJob TrainingJob? @relation(fields: [trainingJobId], references: [id])
  
  @@map("model_forks")
}
```

---

## Migrations

### Initial Migration

```bash
# Generate migration
npx prisma migrate dev --name init

# Apply to production
npx prisma migrate deploy
```

### Enable pgvector

```sql
-- Run manually in Railway PostgreSQL
CREATE EXTENSION IF NOT EXISTS vector;
```
