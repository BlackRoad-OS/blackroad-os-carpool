# 04 — API Contracts

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

**Base URL:** `https://api.blackroad.io/v1`  
**Authentication:** Bearer token (Clerk JWT)  
**Content-Type:** `application/json`

---

## Authentication

All authenticated endpoints require:

```
Authorization: Bearer <clerk_jwt_token>
```

The JWT is obtained from Clerk on the frontend and included in all API requests.

---

## Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... }  // Optional
  }
}
```

### Common Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid JWT |
| `FORBIDDEN` | 403 | User lacks permission |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `VALIDATION_ERROR` | 400 | Invalid request body |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

---

## Endpoints

### Auth

#### `GET /auth/me`
Get current user details.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "clerkId": "user_xxx",
    "email": "user@example.com",
    "name": "John Doe",
    "avatarUrl": "https://...",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

---

### Workspaces

#### `GET /workspaces`
List user's workspaces.

**Response:**
```json
{
  "success": true,
  "data": {
    "workspaces": [
      {
        "id": "uuid",
        "name": "My Workspace",
        "slug": "my-workspace",
        "plan": "pro",
        "role": "owner",
        "createdAt": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### `POST /workspaces`
Create a new workspace.

**Request:**
```json
{
  "name": "My Workspace"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "name": "My Workspace",
    "slug": "my-workspace",
    "plan": "free",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

#### `GET /workspaces/:id`
Get workspace details.

#### `PATCH /workspaces/:id`
Update workspace.

**Request:**
```json
{
  "name": "New Name",
  "settings": { ... }
}
```

#### `DELETE /workspaces/:id`
Delete workspace (owner only).

---

### API Keys

#### `GET /workspaces/:workspaceId/keys`
List connected providers.

**Response:**
```json
{
  "success": true,
  "data": {
    "keys": [
      {
        "provider": "openai",
        "keyHint": "...abc",
        "isValid": true,
        "lastTestedAt": "2024-01-01T00:00:00Z",
        "createdAt": "2024-01-01T00:00:00Z"
      },
      {
        "provider": "anthropic",
        "keyHint": "...xyz",
        "isValid": true,
        "lastTestedAt": "2024-01-01T00:00:00Z",
        "createdAt": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### `POST /workspaces/:workspaceId/keys`
Add an API key.

**Request:**
```json
{
  "provider": "openai",
  "apiKey": "sk-...",
  "endpointUrl": null  // Optional, for custom providers
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "provider": "openai",
    "keyHint": "...abc",
    "isValid": true
  }
}
```

#### `DELETE /workspaces/:workspaceId/keys/:provider`
Remove an API key.

#### `POST /workspaces/:workspaceId/keys/:provider/test`
Test API key validity.

**Response:**
```json
{
  "success": true,
  "data": {
    "isValid": true,
    "models": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
    "testedAt": "2024-01-01T00:00:00Z"
  }
}
```

---

### Conversations

#### `GET /workspaces/:workspaceId/conversations`
List conversations.

**Query Parameters:**
- `limit` (int, default 20): Number of results
- `offset` (int, default 0): Pagination offset
- `archived` (bool, default false): Include archived

**Response:**
```json
{
  "success": true,
  "data": {
    "conversations": [
      {
        "id": "uuid",
        "title": "Help with Python",
        "agentId": null,
        "messageCount": 12,
        "lastMessageAt": "2024-01-01T00:00:00Z",
        "createdAt": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 45,
    "limit": 20,
    "offset": 0
  }
}
```

#### `POST /workspaces/:workspaceId/conversations`
Create a new conversation.

**Request:**
```json
{
  "title": "Optional title",
  "agentId": "uuid or null",
  "settings": {
    "preferredModel": "gpt-4o",
    "temperature": 0.7
  }
}
```

#### `GET /workspaces/:workspaceId/conversations/:id`
Get conversation with messages.

**Query Parameters:**
- `messageLimit` (int, default 50): Number of messages to include

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Help with Python",
    "agentId": null,
    "settings": { ... },
    "messages": [
      {
        "id": "uuid",
        "role": "user",
        "content": "How do I sort a list?",
        "createdAt": "2024-01-01T00:00:00Z"
      },
      {
        "id": "uuid",
        "role": "assistant",
        "content": "You can use the sorted() function...",
        "modelUsed": "gpt-4o",
        "providerUsed": "openai",
        "tokensInput": 45,
        "tokensOutput": 120,
        "latencyMs": 1250,
        "createdAt": "2024-01-01T00:00:01Z"
      }
    ],
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

#### `DELETE /workspaces/:workspaceId/conversations/:id`
Delete conversation.

---

### Messages (Chat)

#### `POST /workspaces/:workspaceId/conversations/:id/messages`
Send a message and get AI response.

**Request:**
```json
{
  "content": "How do I sort a list in Python?",
  "attachments": []  // Future: file uploads
}
```

**Response (Streaming):**
Uses Server-Sent Events (SSE) for streaming.

```
Content-Type: text/event-stream

event: message_start
data: {"messageId": "uuid", "model": "gpt-4o", "provider": "openai"}

event: content_delta
data: {"delta": "You can "}

event: content_delta
data: {"delta": "use the "}

event: content_delta
data: {"delta": "sorted() function..."}

event: message_end
data: {"tokensInput": 45, "tokensOutput": 120, "latencyMs": 1250}
```

**Response (Non-Streaming):**
Add `?stream=false` query param.

```json
{
  "success": true,
  "data": {
    "message": {
      "id": "uuid",
      "role": "assistant",
      "content": "You can use the sorted() function...",
      "modelUsed": "gpt-4o",
      "providerUsed": "openai",
      "tokensInput": 45,
      "tokensOutput": 120,
      "latencyMs": 1250,
      "createdAt": "2024-01-01T00:00:00Z"
    }
  }
}
```

---

### Agents

#### `GET /agents`
List available agents (system + user's custom).

**Response:**
```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "id": "uuid",
        "name": "Lucidia",
        "description": "Your AI orchestrator",
        "avatarUrl": "https://...",
        "isSystem": true,
        "isPublic": false
      },
      {
        "id": "uuid",
        "name": "Code Assistant",
        "description": "Specialized for coding tasks",
        "avatarUrl": null,
        "isSystem": false,
        "isPublic": false
      }
    ]
  }
}
```

#### `POST /workspaces/:workspaceId/agents`
Create custom agent.

**Request:**
```json
{
  "name": "My Agent",
  "description": "Helps with...",
  "systemPrompt": "You are a helpful assistant that...",
  "modelConfig": {
    "preferredModel": "claude-3-5-sonnet",
    "temperature": 0.5
  },
  "toolsEnabled": ["web_search", "code_execution"]
}
```

#### `GET /agents/:id`
Get agent details.

#### `PATCH /workspaces/:workspaceId/agents/:id`
Update agent.

#### `DELETE /workspaces/:workspaceId/agents/:id`
Delete agent.

---

### Training

#### `GET /workspaces/:workspaceId/training/jobs`
List training jobs.

**Response:**
```json
{
  "success": true,
  "data": {
    "jobs": [
      {
        "id": "uuid",
        "baseModel": "llama-3-8b",
        "status": "completed",
        "metrics": {
          "finalLoss": 0.45,
          "epochs": 3
        },
        "createdAt": "2024-01-01T00:00:00Z",
        "completedAt": "2024-01-01T01:00:00Z"
      }
    ]
  }
}
```

#### `POST /workspaces/:workspaceId/training/jobs`
Start training job.

**Request:**
```json
{
  "baseModel": "llama-3-8b",
  "config": {
    "learningRate": 0.0001,
    "epochs": 3,
    "batchSize": 4,
    "adapterType": "lora",
    "loraRank": 16
  },
  "dataSource": {
    "type": "conversations",
    "conversationIds": ["uuid1", "uuid2"]  // Or "all"
  }
}
```

#### `GET /workspaces/:workspaceId/training/jobs/:id`
Get job status.

#### `DELETE /workspaces/:workspaceId/training/jobs/:id`
Cancel job.

---

### Model Forks

#### `GET /workspaces/:workspaceId/models`
List user's forked models.

**Response:**
```json
{
  "success": true,
  "data": {
    "models": [
      {
        "id": "uuid",
        "name": "My Custom LLaMA",
        "baseModel": "llama-3-8b",
        "adapterType": "lora",
        "isDeployed": true,
        "endpointUrl": "https://...",
        "createdAt": "2024-01-01T00:00:00Z"
      }
    ]
  }
}
```

#### `POST /workspaces/:workspaceId/models/:id/deploy`
Deploy a forked model.

**Response:**
```json
{
  "success": true,
  "data": {
    "endpointUrl": "https://models.blackroad.io/xxx",
    "status": "deploying"
  }
}
```

#### `DELETE /workspaces/:workspaceId/models/:id/deploy`
Undeploy a model.

---

## Rate Limits

| Plan | Requests/min | Messages/day |
|------|--------------|--------------|
| Free | 20 | 50 |
| Pro | 60 | Unlimited |
| Team | 120 | Unlimited |
| Enterprise | Custom | Unlimited |

Rate limit headers included in all responses:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1704067200
```

---

## Webhooks (Future)

For enterprise integrations, we'll support webhooks:

```json
POST https://your-server.com/webhook

{
  "event": "message.created",
  "timestamp": "2024-01-01T00:00:00Z",
  "data": {
    "workspaceId": "uuid",
    "conversationId": "uuid",
    "messageId": "uuid",
    "role": "assistant",
    "content": "..."
  }
}
```
