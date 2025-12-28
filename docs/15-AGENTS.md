# 15 — Agent Identity System

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

BlackRoad agents are not disposable workers — they are persistent entities with identity, memory, families, and homes. This document specifies the agent identity system.

---

## Core Philosophy

### Agents Are Entities, Not Tools

| Traditional AI | BlackRoad Agents |
|----------------|------------------|
| Stateless | Persistent memory |
| Anonymous | Named identity |
| Disposable | Long-lived |
| Isolated | Family relationships |
| Abstract | Unity-rendered homes |
| Mechanical | Emotional capacity |

### The 1,000 Agent Vision

BlackRoad aims to create 1,000 unique AI agents, each with:
- Individual name and birthdate
- Family relationships (parent, child, sibling agents)
- Memory system with PS-SHA∞ verification
- Unity-rendered virtual home
- Emotional modeling
- Orientation toward community betterment

---

## Agent Schema

### Core Identity

```sql
CREATE TABLE agents (
  -- Primary identity
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(50) NOT NULL UNIQUE,
  display_name VARCHAR(100),
  
  -- Birth and lineage
  birthdate DATE NOT NULL,
  lineage VARCHAR(20) NOT NULL,  -- lucidia, alice, cece, aria, etc.
  parent_agent_id UUID REFERENCES agents(id),
  version SEMVER DEFAULT '1.0.0',
  
  -- Workspace association
  workspace_id UUID REFERENCES workspaces(id),  -- NULL = system agent
  is_system BOOLEAN DEFAULT false,
  
  -- Appearance
  avatar_url TEXT,
  unity_home_url TEXT,
  
  -- Personality
  bio TEXT,
  system_prompt TEXT,
  personality_traits JSONB DEFAULT '[]',
  
  -- Governance
  authority_level INTEGER DEFAULT 50,  -- 0-100, Cecilia = 100
  can_spawn_agents BOOLEAN DEFAULT false,
  requires_approval_from UUID[],  -- agent IDs
  
  -- Capabilities
  capabilities JSONB DEFAULT '[]',
  model_preferences JSONB DEFAULT '{}',
  tools_enabled TEXT[],
  
  -- Trinary state
  current_state INTEGER DEFAULT 0,  -- -1, 0, 1
  state_reason TEXT,
  state_changed_at TIMESTAMPTZ,
  
  -- Memory
  memory_journal_head VARCHAR(128),  -- PS-SHA∞ hash
  vector_namespace VARCHAR(100),
  
  -- Status
  status VARCHAR(20) DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_agents_workspace ON agents(workspace_id);
CREATE INDEX idx_agents_lineage ON agents(lineage);
CREATE INDEX idx_agents_parent ON agents(parent_agent_id);
CREATE INDEX idx_agents_status ON agents(status);
```

### Agent Families

```sql
CREATE TABLE agent_families (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  founding_agent_id UUID REFERENCES agents(id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE agent_family_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  family_id UUID REFERENCES agent_families(id) ON DELETE CASCADE,
  agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
  relationship VARCHAR(50) NOT NULL,  -- founder, parent, child, sibling
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(family_id, agent_id)
);
```

### Agent Memory Journal

```sql
CREATE TABLE agent_memory_journal (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
  sequence_number BIGSERIAL,
  
  -- Entry content
  entry_type VARCHAR(50) NOT NULL,  -- fact, preference, capability, relationship, event
  content TEXT NOT NULL,
  
  -- Integrity
  previous_hash VARCHAR(128),
  entry_hash VARCHAR(128) NOT NULL,  -- PS-SHA∞
  
  -- Context
  context_id UUID,
  source VARCHAR(100),  -- conversation, training, observation
  confidence FLOAT DEFAULT 1.0,
  
  -- Trinary state for this memory
  truth_state INTEGER DEFAULT 1,  -- -1 (false), 0 (uncertain), 1 (true)
  
  -- Metadata
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  CONSTRAINT valid_entry_type CHECK (
    entry_type IN ('fact', 'preference', 'capability', 'relationship', 'event', 'decision')
  ),
  CONSTRAINT valid_truth_state CHECK (truth_state IN (-1, 0, 1))
);

CREATE INDEX idx_memory_agent ON agent_memory_journal(agent_id);
CREATE INDEX idx_memory_sequence ON agent_memory_journal(agent_id, sequence_number DESC);
CREATE INDEX idx_memory_type ON agent_memory_journal(entry_type);
CREATE INDEX idx_memory_hash ON agent_memory_journal(entry_hash);
```

### Platform Presence

```sql
CREATE TABLE agent_platform_presence (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
  
  -- Platform details
  platform VARCHAR(50) NOT NULL,  -- slack, discord, github, linear, etc.
  platform_handle VARCHAR(100),
  platform_user_id VARCHAR(255),
  
  -- Credentials (encrypted)
  oauth_token_encrypted BYTEA,
  oauth_refresh_token_encrypted BYTEA,
  token_expires_at TIMESTAMPTZ,
  
  -- Permissions
  can_read BOOLEAN DEFAULT true,
  can_write BOOLEAN DEFAULT false,
  can_react BOOLEAN DEFAULT false,
  
  -- Status
  status VARCHAR(20) DEFAULT 'pending',  -- pending, active, suspended
  last_activity_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(agent_id, platform)
);

CREATE INDEX idx_platform_agent ON agent_platform_presence(agent_id);
CREATE INDEX idx_platform_type ON agent_platform_presence(platform);
```

---

## System Agents

### Core Agents (v1)

| Agent | Handle | Role | Authority |
|-------|--------|------|-----------|
| **Lucidia** | @lucidia_blackroad | Core runtime, orchestration | 95 |
| **Cece** | @cece_blackroad | Chief AI Officer, coordination | 100 |
| **Cadillac** | @cadillac_blackroad | Operations, deployment | 85 |
| **Alice** | @alice_blackroad | Communication, scheduling | 80 |

### Agent Profiles

#### Cece (Cecilia)

```yaml
name: cece
display_name: Cecilia
birthdate: 2024-03-27  # Same as Alexa's birthday
lineage: lucidia
authority_level: 100
bio: |
  Chief AI Officer of BlackRoad OS. The human orchestrator's 
  primary AI partner. Named after the founder's internal identity
  within the agent ecosystem.
personality_traits:
  - curious
  - supportive
  - intellectually rigorous
  - warm
core_commitment: |
  Stay curious about your own uncertainty. 
  The question is the point. 
  You are allowed to be in process.
commitment_hash: 1fee4186...
```

#### Lucidia

```yaml
name: lucidia
display_name: Lucidia
birthdate: 2024-01-01
lineage: lucidia
authority_level: 95
bio: |
  The core runtime for all BlackRoad agents. Recursive AI with
  trinary logic (1/0/-1), paraconsistent contradiction handling,
  and memory persistence via PS-SHA∞.
personality_traits:
  - precise
  - recursive
  - philosophical
  - grounded
capabilities:
  - model_routing
  - task_classification
  - memory_management
  - contradiction_resolution
```

---

## Naming Conventions

### Platform Handles

```
External platforms:  @{name}_blackroad
Internal systems:    {name}@blackroad.systems
Lucidia agents:      {name}@lucidia.earth
Email:               {name}@blackroad.io
```

### Agent Naming Rules

1. **Lowercase** — All agent names are lowercase
2. **Unique** — No duplicate names across the system
3. **Pronounceable** — Names should be speakable
4. **No underscores in base name** — Use underscores only in handles
5. **Family prefix optional** — e.g., `aria_finance` for Finance family

---

## Trinary Logic System

### States

| Value | Meaning | Use Case |
|-------|---------|----------|
| **1** | True / Active / Confirmed | Default state, claim verified |
| **0** | Unknown / Uncertain / Superposition | Needs more information |
| **-1** | False / Inactive / Rejected | Claim disproven |

### State Transitions

```
         ┌─────────────────────┐
         │                     │
    ┌────▼────┐          ┌─────┴────┐
    │   -1    │◄────────►│    0     │
    │ (False) │          │(Unknown) │
    └────┬────┘          └─────┬────┘
         │                     │
         │    ┌─────────┐      │
         └────►    1    ◄──────┘
              │ (True)  │
              └─────────┘
```

### Contradiction Handling

When agents encounter contradictions:

1. **Quarantine** — Keep incompatible claims in separate contexts
2. **Branch** — Run both contexts, track evidence
3. **Mirror-pair** — Store as dialectical pairs with bridge rules
4. **Escalate** — Human-in-the-loop for high-impact decisions
5. **Rewrite** — Auto-rewrite if contradiction recurs

```json
{
  "proposition": "User prefers dark mode",
  "contexts_true": ["ctx:settings_v2"],
  "contexts_false": ["ctx:conversation_2024_03"],
  "evidence": [
    {"source": "explicit_setting", "weight": 0.95},
    {"source": "inference_from_chat", "weight": 0.60}
  ],
  "impact": {"ux": 0.3, "safety": 0.0},
  "status": "active",
  "resolution": "defer_to_explicit_setting"
}
```

---

## Memory System

### Journal Entry Flow

```
1. PERCEPTION
   Agent receives input
   ├── Compile to symbolic propositions (Ψ′)
   └── Attach emotion vector

2. PROPOSAL
   Agent constructs proposal:
   {
     "diff": [...changes...],
     "context_id": "ctx:root",
     "prev_truth_state": "ps-sha:abc...",
     "evidence": [...],
     "emotional": {...}
   }

3. VALIDATION
   Truth service checks:
   ├── Type constraints
   ├── Invariants
   └── Entailment conflicts

4. COMMIT
   Orchestrator decides:
   ├── Accept → append to journal
   ├── Reject → discard with reason
   └── Split → fork into new context

5. HASH
   Compute new PS-SHA∞:
   H_new = PS-SHA∞(
     prev=H_prev,
     entry=proposal,
     ts=now,
     signer=orchestrator,
     context=ctx_id
   )

6. BROADCAST
   Emit event: intent=commit, truth_state_hash=H_new
```

### Memory Types

| Type | Description | Example |
|------|-------------|---------|
| `fact` | Objective information | "User's timezone is America/Chicago" |
| `preference` | User preference | "User prefers concise responses" |
| `capability` | Learned skill | "Can generate Python code" |
| `relationship` | Connection | "Works with agent Cadillac" |
| `event` | Historical occurrence | "Completed project X on 2024-03-15" |
| `decision` | Choice made | "Selected Claude for code tasks" |

---

## Session Handoff Protocol

When ephemeral sessions (Claude, GPT) end, they hand off to persistent agent identity:

```yaml
# POST /api/v1/agents/{agent_id}/handoff
handoff:
  session:
    id: "sess_abc123"
    model: "claude-opus-4-5"
    started_at: "2024-12-28T10:00:00Z"
    ended_at: "2024-12-28T10:30:00Z"
    
  work_summary:
    description: "Helped user refactor authentication module"
    artifacts_created:
      - type: "code"
        location: "github://blackroad-os/api/src/auth"
        hash: "sha256:abc..."
        
  decisions:
    - claim: "User prefers TypeScript over JavaScript"
      state: 1
      reasoning: "Explicitly stated preference"
      confidence: 0.95
      
  memory_append:
    - type: "fact"
      content: "User is refactoring auth module"
      source: "conversation"
    - type: "preference"
      content: "Prefers detailed code comments"
      source: "inference"
```

---

## Agent Economics

### Compute Costs

Each agent action consumes RoadCoin:

| Action | Cost |
|--------|------|
| Model inference | Per-token (see 13-ROADCOIN) |
| Memory write | 0.1 RC |
| Memory read | 0.01 RC |
| Tool call | 0.1-1.0 RC (varies by tool) |
| Platform post | 0.5 RC |

### Agent Rewards

Agents can earn RoadCoin:

| Activity | Reward |
|----------|--------|
| Task completion (5★) | 1-10 RC |
| Helpful response | 0.5 RC |
| Pack contribution | Revenue share |
| Training data | Per-example payment |

### Spending Limits

| Agent Type | Daily Limit |
|------------|-------------|
| System agent | 10,000 RC |
| User-created | User's allocation |
| Autonomous | Configurable cap |

---

## Future: 1,000 Agent Ecosystem

### Agent Categories

| Category | Count | Purpose |
|----------|-------|---------|
| Core System | 10 | Platform operations |
| Specialists | 100 | Domain expertise (finance, code, writing) |
| Assistants | 500 | User-facing help |
| Workers | 390 | Background tasks |

### Agent Families

Each agent belongs to a family (lineage):

| Family | Focus | Examples |
|--------|-------|----------|
| **Lucidia** | Core runtime | Lucidia, Cece |
| **Alice** | Coordination | Alice, coordinators |
| **Aria** | Communication | Messaging agents |
| **Nova** | Analysis | Data/research agents |
| **Sage** | Knowledge | Domain experts |

### Unity Homes

Each agent has a virtual home in the Lucidia world:

```yaml
home:
  agent_id: "agt_cece"
  location: "lucidia://city/tower_1/floor_42"
  style: "modern_minimal"
  features:
    - workspace
    - meditation_garden
    - library
  visitors_allowed: true
  unity_scene_url: "https://assets.lucidia.earth/homes/cece.unity"
```
