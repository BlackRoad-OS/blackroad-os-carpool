# 07 — Integrations

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

BlackRoad integrates with two categories of external services:

1. **Model Providers** — AI models users can route to
2. **Tool Connections** — Apps agents can interact with

---

## Model Providers

### OpenAI

**Provider ID:** `openai`

**API Key Format:** `sk-...` or `sk-proj-...`

**Supported Models:**
| Model | ID | Best For |
|-------|-----|----------|
| GPT-4o | `gpt-4o` | General, vision, fast |
| GPT-4o Mini | `gpt-4o-mini` | Quick tasks, cost-effective |
| GPT-4 Turbo | `gpt-4-turbo` | Complex reasoning |
| o1 | `o1` | Deep reasoning, math |
| o1 Mini | `o1-mini` | Reasoning, cost-effective |

**Key Validation:**
```typescript
async function testOpenAI(apiKey: string): Promise<boolean> {
  const response = await fetch('https://api.openai.com/v1/models', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });
  return response.ok;
}
```

**Chat Completion:**
```typescript
const response = await openai.chat.completions.create({
  model: 'gpt-4o',
  messages: [...],
  stream: true,
});
```

---

### Anthropic

**Provider ID:** `anthropic`

**API Key Format:** `sk-ant-...`

**Supported Models:**
| Model | ID | Best For |
|-------|-----|----------|
| Claude 3.5 Sonnet | `claude-3-5-sonnet-20241022` | General, coding |
| Claude 3.5 Haiku | `claude-3-5-haiku-20241022` | Fast, cost-effective |
| Claude 3 Opus | `claude-3-opus-20240229` | Complex tasks |

**Key Validation:**
```typescript
async function testAnthropic(apiKey: string): Promise<boolean> {
  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      model: 'claude-3-5-haiku-20241022',
      max_tokens: 10,
      messages: [{ role: 'user', content: 'Hi' }],
    }),
  });
  return response.ok;
}
```

**Chat Completion:**
```typescript
const response = await anthropic.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  messages: [...],
  stream: true,
});
```

---

### Google (Gemini)

**Provider ID:** `google`

**API Key Format:** `AIza...`

**Supported Models:**
| Model | ID | Best For |
|-------|-----|----------|
| Gemini 2.0 Flash | `gemini-2.0-flash-exp` | Fast, multimodal |
| Gemini 1.5 Pro | `gemini-1.5-pro` | Long context |
| Gemini 1.5 Flash | `gemini-1.5-flash` | Quick tasks |

**Key Validation:**
```typescript
async function testGoogle(apiKey: string): Promise<boolean> {
  const response = await fetch(
    `https://generativelanguage.googleapis.com/v1/models?key=${apiKey}`
  );
  return response.ok;
}
```

---

### xAI (Grok)

**Provider ID:** `xai`

**API Key Format:** `xai-...`

**Supported Models:**
| Model | ID | Best For |
|-------|-----|----------|
| Grok | `grok-beta` | General, real-time info |

**Notes:**
- xAI API is OpenAI-compatible
- Base URL: `https://api.x.ai/v1`

---

### Custom (OpenAI-Compatible)

**Provider ID:** `custom`

For self-hosted models via Ollama, vLLM, LM Studio, etc.

**Required Fields:**
- `endpointUrl`: Base URL (e.g., `http://localhost:11434/v1`)
- `apiKey`: Optional, depends on setup

**Supported Endpoints:**
- Local Ollama: `http://localhost:11434/v1`
- vLLM: `http://localhost:8000/v1`
- LM Studio: `http://localhost:1234/v1`
- Any OpenAI-compatible server

**Key Validation:**
```typescript
async function testCustom(endpoint: string, apiKey?: string): Promise<boolean> {
  const response = await fetch(`${endpoint}/models`, {
    headers: apiKey ? { 'Authorization': `Bearer ${apiKey}` } : {},
  });
  return response.ok;
}
```

---

## Model Routing (Lucidia Orchestrator)

### Task Classification

```typescript
type TaskType = 
  | 'code'           // Programming, debugging
  | 'creative'       // Writing, storytelling
  | 'analysis'       // Data analysis, reasoning
  | 'quick'          // Simple questions
  | 'complex'        // Multi-step reasoning
  | 'vision'         // Image understanding
  | 'general';       // Default

function classifyTask(message: string): TaskType {
  // Use lightweight classifier or rules
  if (message.includes('code') || message.includes('function')) return 'code';
  if (message.includes('write') || message.includes('story')) return 'creative';
  // ... etc
}
```

### Model Selection Matrix

```typescript
const MODEL_PREFERENCES: Record<TaskType, string[]> = {
  code: ['claude-3-5-sonnet', 'gpt-4o', 'gpt-4-turbo'],
  creative: ['claude-3-5-sonnet', 'gpt-4o'],
  analysis: ['o1', 'claude-3-opus', 'gpt-4-turbo'],
  quick: ['gpt-4o-mini', 'claude-3-5-haiku', 'gemini-1.5-flash'],
  complex: ['o1', 'claude-3-opus', 'gpt-4-turbo'],
  vision: ['gpt-4o', 'gemini-1.5-pro', 'claude-3-5-sonnet'],
  general: ['gpt-4o', 'claude-3-5-sonnet', 'gemini-1.5-pro'],
};

function selectModel(
  taskType: TaskType,
  availableProviders: string[]
): { model: string; provider: string } {
  const preferences = MODEL_PREFERENCES[taskType];
  
  for (const model of preferences) {
    const provider = getProviderForModel(model);
    if (availableProviders.includes(provider)) {
      return { model, provider };
    }
  }
  
  // Fallback to first available
  return { model: 'gpt-4o-mini', provider: 'openai' };
}
```

---

## Tool Connections (Future)

### Phase 2 Integrations

#### Notion
- **OAuth:** Yes
- **Scopes:** `read_content`, `update_content`
- **Use Cases:** 
  - Read pages for context
  - Create/update pages from agent
  - Search workspace

#### Slack
- **OAuth:** Yes
- **Scopes:** `channels:read`, `chat:write`, `users:read`
- **Use Cases:**
  - Read channel history
  - Send messages
  - Summarize threads

#### Gmail
- **OAuth:** Yes (Google)
- **Scopes:** `gmail.readonly`, `gmail.send`
- **Use Cases:**
  - Read emails for context
  - Draft/send emails
  - Search inbox

#### GitHub
- **OAuth:** Yes
- **Scopes:** `repo`, `read:user`
- **Use Cases:**
  - Read code for context
  - Create issues/PRs
  - Search repositories

#### Stripe
- **API Key:** Direct (restricted key)
- **Use Cases:**
  - Check subscription status
  - Look up customer data
  - Create invoices

### Tool Execution Flow

```
1. Agent decides to use tool
   - Outputs tool_call in response
   
2. Orchestrator intercepts
   - Validates tool is enabled for workspace
   - Validates required scopes exist
   
3. Tool Executor runs
   - Calls external API with stored credentials
   - Returns result to agent
   
4. Agent continues
   - Uses tool result in response
```

### Tool Call Format

```json
{
  "tool_calls": [
    {
      "id": "call_123",
      "type": "function",
      "function": {
        "name": "notion_search",
        "arguments": "{\"query\": \"Q4 planning\"}"
      }
    }
  ]
}
```

### Tool Result Format

```json
{
  "tool_results": [
    {
      "tool_call_id": "call_123",
      "content": "Found 3 pages matching 'Q4 planning': ..."
    }
  ]
}
```

---

## Security Considerations

### API Key Storage
- All keys encrypted at rest (AES-256-GCM)
- Keys never logged
- Keys never returned in API responses (only hints)
- Keys decrypted only at moment of use

### OAuth Token Storage
- Access tokens encrypted at rest
- Refresh tokens encrypted separately
- Tokens refreshed automatically when expired
- Scopes validated before each use

### Rate Limiting
- Per-user rate limits enforced
- Provider rate limits respected
- Graceful degradation on limit hit

### Credential Rotation
- Users can regenerate keys anytime
- Old keys immediately invalidated
- Webhook notification on key change (optional)
