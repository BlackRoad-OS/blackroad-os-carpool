# BlackRoad Carpool

**Multi-AI Orchestration Platform**

> Bring any AI. Train your own. Never leave.

---

## What is Carpool?

**Carpool** is BlackRoad's multi-AI orchestration system — the core engine that coordinates, routes, and manages multiple AI models working together.

Named "carpool" because like a carpool service, it:
- **Picks the right vehicle** (AI model) for each journey (task)
- **Shares resources** efficiently across passengers (users)
- **Routes intelligently** based on destination (task requirements)
- **Optimizes costs** by avoiding single-occupancy trips (over-provisioned models)

---

## Core Capabilities

### 1. **Multi-Model Routing** (Lucidia)
Intelligently routes each task to the best available AI model:
- GPT-4o for complex reasoning
- Claude for long-context analysis
- Gemini for multimodal tasks
- Grok for real-time information
- Local models for privacy-sensitive work

### 2. **Bring Your Own Everything (BYO-E)**
Users connect their own:
- API keys (OpenAI, Anthropic, Google, xAI)
- Tool integrations (Notion, Slack, GitHub, etc.)
- Infrastructure (or use ours)

### 3. **Local Model Forking**
Train personalized AI models from user context:
- Fine-tune LLaMA, Qwen, Phi, Mistral on your conversations
- Deploy to local machines, BlackRoad cloud, or your infrastructure
- True AI continuity — models that learn from *you*

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LUCIDIA CLASSIFIER                           │
│  Analyzes: complexity, task type, capabilities needed           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CARPOOL ROUTER                             │
│  Selects best model from user's connected providers             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────┬──────────────┬──────────────┬──────────────────┐
│   GPT-4o     │  Claude 3.5  │  Gemini 2.0  │  Local Models    │
└──────────────┴──────────────┴──────────────┴──────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CONTEXT MEMORY SYSTEM                         │
│  Logs conversation, updates user model training queue           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

```yaml
backend:
  language: Python (FastAPI) or Node.js (Hono)
  orchestration: Lucidia (custom router)
  model_adapters: OpenAI SDK, Anthropic SDK, Google SDK, etc.

database:
  primary: PostgreSQL (Railway)
  vector: pgvector for embeddings
  cache: Redis (Railway/Upstash)

storage:
  files: Cloudflare R2
  secrets: Encrypted API keys in Postgres

auth:
  provider: Clerk

hosting:
  api: Railway
  edge: Cloudflare Workers
  frontend: Vercel (Next.js)
```

---

## Key Features

### Smart Routing
- **Task Analysis**: Understands complexity, required capabilities, context length
- **Model Selection**: Chooses optimal model from user's connected providers
- **Fallback Logic**: Automatically retries with alternative models on failure
- **Cost Optimization**: Routes to cheaper models when appropriate

### Memory & Context
- **Conversation History**: Full context across all interactions
- **Cross-Model Memory**: Maintains context when switching between AIs
- **Vector Search**: Semantic search across all user conversations
- **Training Queue**: Automatically queues data for local model fine-tuning

### Tool Integration
- **OAuth Flows**: Connect Notion, Slack, GitHub, Gmail, etc.
- **Webhook Handling**: Receive real-time updates from integrated tools
- **Function Calling**: Unified interface across all model providers
- **Custom Tools**: Users can bring their own API endpoints

---

## Roadmap

### Phase 1: Core Routing (MVP)
- ✅ Multi-model API adapter layer
- ✅ Lucidia classification system
- ✅ Basic conversation memory
- 🚧 API key management UI
- 🚧 Single workspace per user

### Phase 2: Tool Integration
- 🔜 Notion, Slack, GitHub connectors
- 🔜 OAuth flow implementation
- 🔜 Webhook receiver system
- 🔜 Multiple workspaces

### Phase 3: Local Model Forking
- 🔜 Context distillation pipeline
- 🔜 LoRA fine-tuning system
- 🔜 Model deployment interface
- 🔜 Edge deployment (Raspberry Pi, local servers)

### Phase 4: Infrastructure Abstraction
- 🔜 One-click deployment
- 🔜 Automatic resource provisioning
- 🔜 DNS/SSL management
- 🔜 Auto-scaling

---

## Getting Started

### For Users
Visit [blackroad.io](https://blackroad.io) to:
1. Create an account
2. Connect your AI provider API keys
3. Start chatting with Lucidia
4. Watch as Carpool intelligently routes between your models

### For Developers
```bash
# Clone repository
git clone https://github.com/BlackRoad-OS/blackroad-os-carpool.git
cd blackroad-os-carpool

# Install dependencies
npm install  # or: pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API keys and configuration

# Run development server
npm run dev  # or: uvicorn main:app --reload
```

---

## Documentation

**Complete documentation suite available in [`/docs`](./docs/):**

| Doc | Purpose | Read When |
|-----|---------|-----------|
| [00-MASTER-INDEX](./docs/00-MASTER-INDEX.md) | Documentation overview & quick reference | Starting any work |
| [01-VISION](./docs/01-VISION.md) | Why BlackRoad exists, core thesis, positioning | Onboarding, strategic decisions |
| [02-ARCHITECTURE](./docs/02-ARCHITECTURE.md) | System design, service boundaries, data flow | Designing features, debugging |
| [03-DATABASE-SCHEMA](./docs/03-DATABASE-SCHEMA.md) | All tables, relationships, indexes | Writing queries, migrations |
| [04-API-CONTRACTS](./docs/04-API-CONTRACTS.md) | Every endpoint, request/response shapes | Building frontend/backend |
| [05-USER-FLOWS](./docs/05-USER-FLOWS.md) | Step-by-step user journeys | Designing UX, testing |
| [06-COMPONENTS](./docs/06-COMPONENTS.md) | Every UI component needed | Building frontend |
| [07-INTEGRATIONS](./docs/07-INTEGRATIONS.md) | How each provider/tool connects | Adding new integrations |
| [08-DEPLOYMENT](./docs/08-DEPLOYMENT.md) | How to deploy each service | DevOps, releases |
| [09-ROADMAP](./docs/09-ROADMAP.md) | Phased timeline with milestones | Planning, prioritization |
| [10-GLOSSARY](./docs/10-GLOSSARY.md) | Terms and definitions | Avoiding confusion |
| [ARCHITECTURE](./docs/ARCHITECTURE.md) | Technical architecture deep-dive | System design work |
| [BLACKROAD_IO_VISION](./BLACKROAD_IO_VISION.md) | Original vision document | Product strategy

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

Key areas:
- Model adapters for new AI providers
- Tool integrations
- Routing algorithm improvements
- Local model deployment targets

---

## License

BlackRoad Proprietary License - See [LICENSE](./LICENSE) for details

---

## Contact

- **Website**: [blackroad.io](https://blackroad.io)
- **Email**: blackroad.systems@gmail.com
- **GitHub**: [BlackRoad-OS](https://github.com/BlackRoad-OS)

---

**Built with ❤️ by the BlackRoad team**

*The OS for AI agents*

---

## 📜 License & Copyright

**Copyright © 2026 BlackRoad OS, Inc. All Rights Reserved.**

**CEO:** Alexa Amundson | **PROPRIETARY AND CONFIDENTIAL**

This software is NOT for commercial resale. Testing purposes only.

### 🏢 Enterprise Scale:
- 30,000 AI Agents
- 30,000 Human Employees
- CEO: Alexa Amundson

**Contact:** blackroad.systems@gmail.com

See [LICENSE](LICENSE) for complete terms.
