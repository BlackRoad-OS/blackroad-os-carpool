# 10 — Glossary

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Purpose

This glossary defines all terms used in BlackRoad documentation. Use these definitions consistently to avoid confusion.

---

## A

### Agent
A configured AI persona with a specific system prompt, model preferences, and enabled tools. Agents can be system-provided (like Lucidia) or user-created.

### API Key
A secret credential that authenticates requests to an AI model provider (OpenAI, Anthropic, etc.). Users provide their own keys ("BYO Keys").

### Adapter
In the context of model training, a set of additional weights (like LoRA) that modify a base model's behavior without changing the original weights.

---

## B

### Base Model
An open-source foundational model (like LLaMA, Qwen, Mistral) that can be fine-tuned or adapted for specific use cases.

### BYO (Bring Your Own)
BlackRoad's approach where users provide their own API keys, tools, and optionally infrastructure, rather than BlackRoad reselling these services.

### BlackRoad Cloud
BlackRoad's managed infrastructure option where users can deploy trained models and agents without managing their own servers.

---

## C

### Cecilia
The internal codename/persona used by Alexa Amundson when working within the BlackRoad AI ecosystem. Also the name Claude responds to.

### Clerk
The authentication service BlackRoad uses for user sign-up, sign-in, and session management.

### Conversation
A single chat thread containing multiple messages between a user and AI. Each conversation has an ID, optional title, and associated settings.

### Context
The information available to an AI when generating a response, including conversation history, system prompts, and any retrieved knowledge.

### Custom Provider
An OpenAI-compatible API endpoint (like Ollama, vLLM, or LM Studio) that users can connect to BlackRoad for using local or self-hosted models.

---

## D

### Deployment
The process of making a trained model available for inference, either on BlackRoad Cloud or a user's own infrastructure.

---

## E

### Embedding
A numerical vector representation of text, used for semantic search and similarity matching. BlackRoad uses embeddings for conversation memory and RAG.

### Encryption (Key)
BlackRoad encrypts all API keys at rest using AES-256-GCM. Keys are only decrypted at the moment of use.

---

## F

### Fine-tuning
The process of further training a base model on specific data to customize its behavior. BlackRoad supports LoRA fine-tuning.

### Fork (Model)
A user's personalized version of a base model, created by training on their conversation data. The fork becomes a "BlackRoad Agent."

---

## G

### Gateway
The API entry point that handles authentication, rate limiting, and request routing to internal services.

---

## I

### Integration
A connection to an external service, either a model provider (OpenAI) or a tool (Notion, Slack).

---

## J

### Job (Training)
A background process that fine-tunes a model on user data. Jobs have statuses (pending, running, completed, failed) and associated metrics.

---

## K

### Key Hint
The last few characters of an API key displayed in the UI (e.g., "...abc") so users can identify which key is connected without exposing the full key.

---

## L

### LoRA (Low-Rank Adaptation)
A training technique that adds small, trainable weights to a frozen base model. More efficient than full fine-tuning.

### Lucidia
The primary AI agent in BlackRoad, responsible for orchestrating conversations, routing to appropriate models, and managing the user experience.

---

## M

### Member
A user who belongs to a workspace but is not the owner. Members can have different roles (admin, member).

### Message
A single unit of conversation—either from the user, assistant, or system. Messages have content, role, and metadata (model used, tokens, etc.).

### Model
An AI system capable of generating responses. Can be a hosted API (GPT-4) or a local model (LLaMA via Ollama).

### Model Badge
UI element showing which model generated a response (e.g., "via GPT-4o").

---

## O

### Ollama
Open-source tool for running large language models locally. BlackRoad supports Ollama as a custom provider.

### Orchestrator
The core BlackRoad component (part of Lucidia) that decides which model to use for each request based on task type and available providers.

### Owner
The user who created a workspace and has full administrative control over it.

---

## P

### Pack
A bundle of agents, prompts, and configurations for a specific use case (e.g., "Finance Pack," "Marketing Pack"). Future marketplace feature.

### Plan
A subscription tier (Free, Pro, Team, Enterprise) that determines feature access and usage limits.

### Provider
An external service that hosts AI models. Supported providers: OpenAI, Anthropic, Google, xAI, Custom.

### pgvector
PostgreSQL extension for vector similarity search, used for embedding storage and retrieval.

---

## Q

### QLoRA (Quantized LoRA)
A memory-efficient variant of LoRA that uses quantization to reduce GPU memory requirements during training.

---

## R

### Railway
The platform BlackRoad uses for hosting backend services, PostgreSQL, and Redis.

### Rate Limiting
Restrictions on how many requests a user can make in a time period, enforced per plan tier.

### Role
A user's permission level within a workspace: owner, admin, or member.

### Routing
The process of selecting which AI model to use for a given request, based on task type, availability, and user preferences.

---

## S

### Streaming
The technique of sending AI responses incrementally (word by word) rather than waiting for the complete response. Improves perceived latency.

### System Prompt
Instructions given to an AI model that define its behavior, personality, and constraints. Each agent has a system prompt.

---

## T

### Task Type
A classification of user messages (code, creative, analysis, etc.) used by the orchestrator to select the appropriate model.

### Token
The basic unit of text processing for AI models. Roughly 4 characters or 0.75 words. Used for billing and context limits.

### Tool
A capability that agents can use to interact with external services (web search, Notion, Slack, etc.).

### Training
The process of teaching a model new behaviors by exposing it to examples. In BlackRoad, users train on their own conversations.

---

## U

### User
A person with a BlackRoad account, identified by their Clerk ID and email.

---

## V

### Vercel
The platform BlackRoad uses for hosting frontend applications.

### vLLM
High-performance inference engine for LLMs. BlackRoad supports vLLM as a custom provider.

---

## W

### Workspace
The primary organizational unit in BlackRoad. Contains conversations, API keys, agents, and trained models. Users can have multiple workspaces (on paid plans).

### Webhook
An HTTP callback triggered by events (e.g., Clerk user created, Stripe payment completed).

---

## X

### xAI
The company behind Grok. BlackRoad supports xAI as a model provider.

---

## Technical Abbreviations

| Abbreviation | Meaning |
|--------------|---------|
| API | Application Programming Interface |
| CDN | Content Delivery Network |
| CI/CD | Continuous Integration / Continuous Deployment |
| DNS | Domain Name System |
| JWT | JSON Web Token |
| LLM | Large Language Model |
| MoE | Mixture of Experts |
| OAuth | Open Authorization |
| RAG | Retrieval-Augmented Generation |
| REST | Representational State Transfer |
| SaaS | Software as a Service |
| SDK | Software Development Kit |
| SQL | Structured Query Language |
| SSE | Server-Sent Events |
| SSL | Secure Sockets Layer |
| SSO | Single Sign-On |
| UI | User Interface |
| URL | Uniform Resource Locator |
| UX | User Experience |
| WASM | WebAssembly |

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2024-12-28 | 1.0.0 | Initial glossary |
