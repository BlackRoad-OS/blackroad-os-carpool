# 08 — Deployment

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Overview

BlackRoad deploys across multiple platforms:

| Service | Platform | Domain |
|---------|----------|--------|
| Marketing site | Vercel | blackroad.io |
| Web app | Vercel | app.blackroad.io |
| Documentation | Vercel | docs.blackroad.io |
| API | Railway | api.blackroad.io |
| Database | Railway | (internal) |
| Cache | Railway | (internal) |
| Storage | Cloudflare R2 | (internal) |
| DNS/CDN | Cloudflare | *.blackroad.io |

---

## Environment Setup

### Prerequisites

- Node.js 20+
- pnpm 8+
- Python 3.11+ (for API if using FastAPI)
- Docker (for local development)
- Accounts: Vercel, Railway, Cloudflare, Clerk, Stripe

### Local Development

```bash
# Clone repositories
git clone git@github.com:BlackRoad-OS/blackroad-os-web.git
git clone git@github.com:BlackRoad-OS/blackroad-os-api.git

# Frontend
cd blackroad-os-web
pnpm install
cp .env.example .env.local
# Edit .env.local with your keys
pnpm dev

# Backend (in separate terminal)
cd blackroad-os-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn src.main:app --reload
```

---

## Frontend Deployment (Vercel)

### Initial Setup

1. **Connect Repository**
   - Go to vercel.com → New Project
   - Import `blackroad-os-web` from GitHub
   - Select BlackRoad-OS organization

2. **Configure Project**
   ```
   Framework Preset: Next.js
   Root Directory: ./
   Build Command: pnpm build
   Output Directory: .next
   Install Command: pnpm install
   ```

3. **Set Environment Variables**
   ```
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
   CLERK_SECRET_KEY=sk_live_...
   NEXT_PUBLIC_API_URL=https://api.blackroad.io
   NEXT_PUBLIC_APP_URL=https://app.blackroad.io
   ```

4. **Configure Domains**
   - Production: `app.blackroad.io`
   - Preview: `*.blackroad-os-web.vercel.app`

### Deploy Process

```bash
# Automatic deployment on push to main
git push origin main

# Manual deployment
vercel --prod
```

### Preview Deployments

- Every PR gets a preview URL
- Format: `blackroad-os-web-git-<branch>-blackroad-os.vercel.app`
- Shares production environment variables (except secrets)

---

## Backend Deployment (Railway)

### Initial Setup

1. **Create Project**
   - Go to railway.app → New Project
   - Select "Deploy from GitHub repo"
   - Choose `blackroad-os-api`

2. **Add Services**
   - API Service (from repo)
   - PostgreSQL (add database)
   - Redis (add database)

3. **Configure API Service**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Environment Variables**
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   CLERK_SECRET_KEY=sk_live_...
   ENCRYPTION_SECRET=<32-byte-hex>
   R2_ACCOUNT_ID=...
   R2_ACCESS_KEY_ID=...
   R2_SECRET_ACCESS_KEY=...
   R2_BUCKET_NAME=blackroad-storage
   ENVIRONMENT=production
   ```

5. **Configure Domain**
   - Add custom domain: `api.blackroad.io`
   - Railway provides SSL automatically

### Deploy Process

```bash
# Automatic deployment on push to main
git push origin main

# Manual deployment via Railway CLI
railway up
```

### Database Migrations

```bash
# Connect to Railway
railway link

# Run migrations
railway run prisma migrate deploy
# OR for Python/SQLAlchemy
railway run alembic upgrade head
```

---

## DNS Configuration (Cloudflare)

### Required DNS Records

| Type | Name | Content | Proxy |
|------|------|---------|-------|
| CNAME | @ | cname.vercel-dns.com | Yes |
| CNAME | app | cname.vercel-dns.com | Yes |
| CNAME | docs | cname.vercel-dns.com | Yes |
| CNAME | api | <railway-domain>.up.railway.app | Yes |

### Cloudflare Settings

**SSL/TLS:**
- Mode: Full (strict)
- Always Use HTTPS: On
- Automatic HTTPS Rewrites: On

**Caching:**
- API routes: Bypass cache (via Page Rule)
- Static assets: Cache Everything

**Security:**
- Bot Fight Mode: On
- Browser Integrity Check: On

**Page Rules:**
```
api.blackroad.io/*
  Cache Level: Bypass
  SSL: Full (strict)
```

---

## Storage Setup (Cloudflare R2)

### Create Bucket

1. Go to Cloudflare Dashboard → R2
2. Create bucket: `blackroad-storage`
3. Set location hint: Automatic

### Create API Token

1. R2 → Manage R2 API Tokens
2. Create token with:
   - Permissions: Object Read & Write
   - Specify bucket: `blackroad-storage`
3. Save Access Key ID and Secret Access Key

### Usage in Code

```typescript
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';

const r2 = new S3Client({
  region: 'auto',
  endpoint: `https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: R2_ACCESS_KEY_ID,
    secretAccessKey: R2_SECRET_ACCESS_KEY,
  },
});

// Upload file
await r2.send(new PutObjectCommand({
  Bucket: 'blackroad-storage',
  Key: `uploads/${userId}/${filename}`,
  Body: fileBuffer,
}));
```

---

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm typecheck

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
        with:
          version: 8
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm test

  # Vercel handles deployment automatically
```

### Deployment Triggers

| Branch | Frontend | Backend |
|--------|----------|---------|
| `main` | Production (app.blackroad.io) | Production (api.blackroad.io) |
| `staging` | Preview | Staging service |
| PR branches | Preview URL | No deployment |

---

## Monitoring

### Vercel Analytics
- Enabled by default
- Tracks: Page views, Web Vitals, errors

### Railway Metrics
- CPU, Memory, Network usage
- Request logs
- Build logs

### Error Tracking (Sentry)

```typescript
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.VERCEL_ENV,
  tracesSampleRate: 0.1,
});
```

### Uptime Monitoring
- Use BetterUptime or similar
- Monitor:
  - `https://blackroad.io` (landing)
  - `https://app.blackroad.io` (app)
  - `https://api.blackroad.io/health` (API)

---

## Rollback Procedures

### Frontend (Vercel)
1. Go to Vercel Dashboard → Deployments
2. Find previous successful deployment
3. Click "..." → "Promote to Production"

### Backend (Railway)
1. Go to Railway Dashboard → Deployments
2. Find previous successful deployment
3. Click "Rollback"

### Database
```bash
# Connect to Railway
railway link

# Rollback migration
railway run prisma migrate resolve --rolled-back <migration-name>
# OR
railway run alembic downgrade -1
```

---

## Secrets Management

### Production Secrets
- Stored in Vercel/Railway environment variables
- Never committed to git
- Rotated quarterly

### Secret Rotation Checklist
- [ ] Clerk API keys
- [ ] Encryption secret
- [ ] R2 credentials
- [ ] Stripe API keys
- [ ] Database connection string (if manually set)

### Accessing Secrets
```bash
# Vercel
vercel env pull .env.local

# Railway
railway variables
```
