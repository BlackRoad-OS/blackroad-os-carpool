# 09 — Roadmap

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

This roadmap outlines the phased delivery of BlackRoad.io from MVP to full platform.

---

## Phase 0: Foundation (December 2024)
**Status:** ✅ In Progress

### Goals
- Finalize architecture documentation
- Set up repositories and CI/CD
- Configure hosting infrastructure

### Deliverables
| Item | Owner | Status |
|------|-------|--------|
| Documentation suite | Cecilia + Claude | ✅ Complete |
| GitHub org + repos | Cecilia | 🔄 In Progress |
| Vercel project setup | Cecilia | ⬜ Not Started |
| Railway project setup | Cecilia | ⬜ Not Started |
| Cloudflare DNS config | Cecilia | ⬜ Not Started |
| Clerk app creation | Cecilia | ⬜ Not Started |

### Exit Criteria
- All docs committed to `blackroad-os-docs`
- `blackroad-os-web` repo initialized with Next.js
- `blackroad-os-api` repo initialized with FastAPI/Hono
- CI/CD pipelines running
- Domains pointing correctly

---

## Phase 1: MVP (January 2025)
**Target:** January 31, 2025

### Goals
- Working chat interface with multi-model support
- User can connect API keys and chat
- Basic conversation persistence

### Features

#### 1.1 Authentication
- [ ] Clerk integration
- [ ] Sign up / Sign in flows
- [ ] User profile page
- [ ] Session management

#### 1.2 Workspace
- [ ] Create workspace on signup
- [ ] Workspace settings page
- [ ] Single workspace per user (MVP)

#### 1.3 API Key Management
- [ ] Add/remove API keys UI
- [ ] Key encryption at rest
- [ ] Key validation on add
- [ ] Support: OpenAI, Anthropic

#### 1.4 Chat Interface
- [ ] Create new conversation
- [ ] Message list with history
- [ ] Chat input with send
- [ ] Streaming responses
- [ ] Model badge display

#### 1.5 Lucidia Orchestrator (Basic)
- [ ] Task classification (simple)
- [ ] Model selection based on available keys
- [ ] OpenAI API integration
- [ ] Anthropic API integration
- [ ] Error handling & fallbacks

#### 1.6 Landing Page
- [ ] Hero section
- [ ] Feature overview
- [ ] Pricing placeholder
- [ ] CTA to sign up

### Exit Criteria
- User can sign up and chat
- Conversations persist across sessions
- Multiple API keys work
- Responses stream correctly
- < 3 min from landing to first message

---

## Phase 2: Multi-Provider & Tools (February 2025)
**Target:** February 28, 2025

### Goals
- Add Google and xAI support
- Custom endpoint support (Ollama)
- First tool integrations

### Features

#### 2.1 Additional Providers
- [ ] Google (Gemini) integration
- [ ] xAI (Grok) integration
- [ ] Provider status monitoring
- [ ] Automatic failover between providers

#### 2.2 Custom Providers
- [ ] Custom endpoint configuration
- [ ] Ollama support
- [ ] vLLM support
- [ ] LM Studio support

#### 2.3 Enhanced Orchestrator
- [ ] Better task classification (LLM-based)
- [ ] Cost-aware routing
- [ ] Latency-aware routing
- [ ] User preference overrides

#### 2.4 Conversation Features
- [ ] Conversation search
- [ ] Export conversations
- [ ] Share conversation (public link)
- [ ] Conversation branching

#### 2.5 First Tool: Web Search
- [ ] Integrate web search API
- [ ] Agent can search and cite sources
- [ ] Search results in conversation

### Exit Criteria
- 4+ model providers working
- Custom Ollama endpoint works
- Web search functional
- Routing is noticeably intelligent

---

## Phase 3: Agent Customization (March 2025)
**Target:** March 31, 2025

### Goals
- Users can create custom agents
- Agent gallery with system agents
- System prompts and configurations

### Features

#### 3.1 Agent Creation
- [ ] Create custom agent UI
- [ ] System prompt editor
- [ ] Model preference settings
- [ ] Tool enable/disable per agent

#### 3.2 Agent Gallery
- [ ] Browse available agents
- [ ] System agents (Lucidia, etc.)
- [ ] User's custom agents
- [ ] Agent detail pages

#### 3.3 Agent-Specific Chat
- [ ] Start chat with specific agent
- [ ] Agent avatar in conversation
- [ ] Agent personality in responses

#### 3.4 System Agents
- [ ] Lucidia (general orchestrator)
- [ ] Code Assistant
- [ ] Writing Assistant
- [ ] Research Assistant

### Exit Criteria
- Users can create agents with custom prompts
- Agents affect conversation behavior
- Gallery shows all available agents

---

## Phase 4: Training & Forking (April 2025)
**Target:** April 30, 2025

### Goals
- Users can train models on their data
- Deploy custom models
- Personal AI that learns

### Features

#### 4.1 Training Data Preparation
- [ ] Select conversations for training
- [ ] Data export/format
- [ ] Data preview and cleaning

#### 4.2 Training Job Management
- [ ] Start training job UI
- [ ] Base model selection
- [ ] Hyperparameter configuration
- [ ] Job progress tracking
- [ ] Job cancellation

#### 4.3 Training Backend
- [ ] Queue system for jobs
- [ ] LoRA training pipeline
- [ ] Model artifact storage (R2)
- [ ] Training metrics tracking

#### 4.4 Model Deployment
- [ ] Deploy to BlackRoad Cloud
- [ ] Export adapter weights
- [ ] Custom endpoint registration
- [ ] Model usage in chat

### Exit Criteria
- User can train LoRA on LLaMA
- Trained model usable in chat
- Training completes in reasonable time
- Cost tracking for training

---

## Phase 5: Team & Billing (May 2025)
**Target:** May 31, 2025

### Goals
- Multi-user workspaces
- Stripe billing integration
- Team collaboration features

### Features

#### 5.1 Team Workspaces
- [ ] Invite team members
- [ ] Role-based permissions
- [ ] Shared API keys
- [ ] Shared agents
- [ ] Shared trained models

#### 5.2 Billing Integration
- [ ] Stripe subscription setup
- [ ] Plan selection UI
- [ ] Payment method management
- [ ] Invoice history
- [ ] Usage tracking

#### 5.3 Plans & Limits
- [ ] Free tier limits
- [ ] Pro tier features
- [ ] Team tier features
- [ ] Usage enforcement

#### 5.4 Admin Features
- [ ] Workspace admin panel
- [ ] Member management
- [ ] Billing management
- [ ] Usage dashboard

### Exit Criteria
- Teams can collaborate
- Billing works end-to-end
- Limits enforced correctly
- Upgrade flow smooth

---

## Phase 6: Infrastructure Abstraction (June 2025)
**Target:** June 30, 2025

### Goals
- One-click infrastructure provisioning
- Users never leave BlackRoad

### Features

#### 6.1 Managed Databases
- [ ] One-click Postgres provisioning
- [ ] One-click Redis provisioning
- [ ] Connection string management
- [ ] Backup configuration

#### 6.2 Managed Storage
- [ ] One-click R2 bucket
- [ ] File upload UI
- [ ] Storage usage tracking

#### 6.3 Managed Compute
- [ ] Deploy custom code (Workers)
- [ ] Cron job scheduling
- [ ] Webhook management

#### 6.4 Domain Management
- [ ] Connect custom domains
- [ ] SSL provisioning
- [ ] DNS management UI

### Exit Criteria
- User can deploy agent with database
- No external accounts needed
- Everything manageable from BlackRoad

---

## Phase 7: Marketplace (Q3 2025)
**Target:** September 30, 2025

### Goals
- Public agent/pack marketplace
- Monetization for creators
- Community ecosystem

### Features

- [ ] Publish agents to marketplace
- [ ] Agent pricing & purchasing
- [ ] Revenue sharing
- [ ] Reviews and ratings
- [ ] Creator dashboard
- [ ] Pack bundles

---

## Phase 8: Enterprise (Q4 2025)
**Target:** December 31, 2025

### Goals
- Enterprise-ready features
- Compliance and security
- Custom deployments

### Features

- [ ] SSO/SAML integration
- [ ] Audit logging
- [ ] Data residency options
- [ ] Dedicated infrastructure
- [ ] SLA guarantees
- [ ] Custom contracts

---

## Success Metrics by Phase

| Phase | Primary Metric | Target |
|-------|----------------|--------|
| 1 | Users signed up | 500 |
| 2 | Daily active users | 100 |
| 3 | Custom agents created | 200 |
| 4 | Training jobs completed | 50 |
| 5 | Paying customers | 50 |
| 6 | Infra provisions | 100 |
| 7 | Marketplace listings | 50 |
| 8 | Enterprise contracts | 5 |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Provider API changes | Abstract provider calls, monitor changelogs |
| Training costs | Clear pricing, job limits, spot instances |
| Security breach | Encryption, audits, bug bounty |
| Scaling issues | Load testing each phase, Railway autoscale |
| Competition | Move fast, unique positioning, community |
