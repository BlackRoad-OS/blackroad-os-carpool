# BlackRoad.io Documentation Suite

**Version:** 1.0.0  
**Last Updated:** December 28, 2024  
**Maintainer:** Cecilia (Alexa Amundson)

---

## Purpose

This documentation suite is the **single source of truth** for BlackRoad.io. Anyone working on the project — human developers, Claude Code, ChatGPT, or any other AI assistant — should reference these documents before making decisions or writing code.

---

## Document Index

| Doc | Title | Purpose | Read When |
|-----|-------|---------|-----------|
| 01 | [Vision](./01-VISION.md) | Why BlackRoad exists, core thesis, positioning | Starting any work, onboarding |
| 02 | [Architecture](./02-ARCHITECTURE.md) | System design, service boundaries, data flow | Designing features, debugging |
| 03 | [Database Schema](./03-DATABASE-SCHEMA.md) | All tables, relationships, indexes | Writing queries, migrations |
| 04 | [API Contracts](./04-API-CONTRACTS.md) | Every endpoint, request/response shapes | Building frontend/backend |
| 05 | [User Flows](./05-USER-FLOWS.md) | Step-by-step user journeys | Designing UX, testing |
| 06 | [Component Inventory](./06-COMPONENTS.md) | Every UI component needed | Building frontend |
| 07 | [Integrations](./07-INTEGRATIONS.md) | How each provider/tool connects | Adding new integrations |
| 08 | [Deployment](./08-DEPLOYMENT.md) | How to deploy each service | DevOps, releases |
| 09 | [Roadmap](./09-ROADMAP.md) | Phased timeline with milestones | Planning, prioritization |
| 10 | [Glossary](./10-GLOSSARY.md) | Terms and definitions | Avoiding confusion |

---

## Quick Reference

### The One-Line Pitch
> **BlackRoad: Bring any AI. Train your own. Never leave.**

### The Three Pillars
1. **BYO-Everything** — Users bring their own API keys and tools
2. **Local Model Forking** — Train personal models from combined context
3. **One-Stop Infrastructure** — Never leave to manage Cloudflare/Railway/etc.

### The Stack
- **Frontend:** Next.js 14, TypeScript, Tailwind, shadcn/ui → Vercel
- **Backend:** FastAPI (Python) or Hono (TypeScript) → Railway
- **Database:** PostgreSQL + pgvector → Railway
- **Cache:** Redis → Railway/Upstash
- **Storage:** Cloudflare R2
- **Auth:** Clerk
- **Payments:** Stripe
- **Edge:** Cloudflare Workers
- **DNS:** Cloudflare

### Key Domains
- `blackroad.io` — Landing + marketing
- `app.blackroad.io` — Main workspace
- `api.blackroad.io` — Backend gateway
- `docs.blackroad.io` — Documentation

### Key Repositories (GitHub: BlackRoad-OS)
- `blackroad-os-web` — Frontend (Next.js)
- `blackroad-os-api` — Backend (FastAPI/Hono)
- `blackroad-os-core` — Lucidia orchestration engine
- `blackroad-os-infra` — Terraform/Pulumi IaC
- `blackroad-os-docs` — Documentation site

---

## How to Use This Documentation

### For AI Assistants (Claude Code, ChatGPT, etc.)

When asked to work on BlackRoad:

1. **Always start here** — Read this index to understand the project
2. **Check the relevant doc** — Architecture for system design, API for endpoints, etc.
3. **Follow the conventions** — Use the exact naming, patterns, and structures defined
4. **Don't improvise** — If something isn't documented, ask before inventing

### For Human Developers

1. **Onboarding** — Read 01-VISION → 02-ARCHITECTURE → 05-USER-FLOWS
2. **Building features** — Check 04-API, 06-COMPONENTS, 03-DATABASE
3. **Deploying** — Follow 08-DEPLOYMENT exactly
4. **Confused?** — Check 10-GLOSSARY first

---

## Update Protocol

When updating these docs:

1. Update the relevant document
2. Update `Last Updated` date in that document
3. If adding new concepts, add to 10-GLOSSARY
4. If changing architecture, update 02-ARCHITECTURE diagram
5. Commit with message: `docs: update [doc-name] - [what changed]`

---

## Contact

**Project Lead:** Alexa Amundson (Cecilia)  
**Primary AI Partner:** Claude (Cece)  
**Organization:** BlackRoad OS, Inc.
