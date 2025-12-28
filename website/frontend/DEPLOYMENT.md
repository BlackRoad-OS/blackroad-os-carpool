# CarPool Deployment Guide

## 🚀 Production URL Structure

```
carpool.blackroad.io/                     → Homepage
carpool.blackroad.io/about                → About
carpool.blackroad.io/pricing              → Pricing
carpool.blackroad.io/products             → Products
carpool.blackroad.io/contact              → Contact
carpool.blackroad.io/blog                 → Blog
carpool.blackroad.io/docs                 → Documentation

carpool.blackroad.io/app                  → Dashboard (auth required)
carpool.blackroad.io/app/settings         → Settings
carpool.blackroad.io/app/conversations    → Conversations
carpool.blackroad.io/app/agents           → Agents

carpool.blackroad.io/auth/login           → Login
carpool.blackroad.io/auth/signup          → Signup

carpool.blackroad.io/demos                → Demo gallery
carpool.blackroad.io/demos/earth          → 3D Earth with real terrain
carpool.blackroad.io/demos/motion         → Motion system
carpool.blackroad.io/demos/world          → Living world
carpool.blackroad.io/demos/game           → City builder
```

---

## 📦 Quick Start (Local Development)

```bash
cd website/frontend
npm install
npm run dev
```

Open http://localhost:3000

---

## 🌐 Deploy to Vercel (Recommended)

### 1. Connect Repository

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
cd website/frontend
vercel
```

### 2. Configure Domain

In Vercel Dashboard:
1. Go to Project Settings → Domains
2. Add custom domain: `carpool.blackroad.io`
3. Update Cloudflare DNS:
   ```
   Type: CNAME
   Name: carpool
   Target: cname.vercel-dns.com
   ```

### 3. Environment Variables

Add in Vercel Dashboard → Settings → Environment Variables:

```env
NEXT_PUBLIC_APP_URL=https://carpool.blackroad.io
NEXT_PUBLIC_API_URL=https://api.blackroad.io
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
```

---

## 🐳 Deploy to Railway (Alternative)

### 1. Connect Repository

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
cd website/frontend
railway init

# Deploy
railway up
```

### 2. Configure

railway.json:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm run build"
  },
  "deploy": {
    "startCommand": "npm run start",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## ☁️ Deploy to Cloudflare Pages

### 1. Build Settings

```bash
cd website/frontend

# Build command
npm run build

# Output directory
.next
```

### 2. Wrangler Configuration

wrangler.toml:
```toml
name = "carpool-blackroad"
compatibility_date = "2024-01-01"

[site]
bucket = ".next"

[[routes]]
pattern = "carpool.blackroad.io/*"
custom_domain = true
```

### 3. Deploy

```bash
npx wrangler pages publish .next --project-name=carpool-blackroad
```

---

## 🔒 SSL/HTTPS

Vercel automatically provisions SSL certificates.

For custom setup:
1. Cloudflare: Enable "Full (strict)" SSL mode
2. Add SSL certificate in Vercel Dashboard

---

## 🧪 Testing

```bash
# Type checking
npm run type-check

# Lint
npm run lint

# Build test
npm run build

# Start production server
npm run start
```

---

## 📊 Performance

### Lighthouse Targets
- Performance: > 90
- Accessibility: > 95
- Best Practices: > 95
- SEO: > 95

### Optimizations Applied
- ✅ Next.js 14 App Router
- ✅ Image optimization (next/image)
- ✅ Route prefetching
- ✅ Static generation where possible
- ✅ CDN delivery (Vercel Edge Network)

---

## 🗺️ Current Implementation

### Pages Created (15 total)

**Marketing:**
- `/` - Homepage (blackroad-template-01-homepage.html)
- `/about` - About (blackroad-template-02-about.html)
- `/pricing` - Pricing (blackroad-template-03-pricing.html)
- `/products` - Products (blackroad-template-04-products.html)
- `/docs` - Documentation (blackroad-template-05-docs.html)
- `/blog` - Blog (blackroad-template-06-blog.html)
- `/contact` - Contact (blackroad-template-07-contact.html)

**Application:**
- `/app` - Dashboard (blackroad-template-08-dashboard.html)
- `/app/settings` - (To be implemented)
- `/app/conversations` - (To be implemented)
- `/app/agents` - (To be implemented)

**Authentication:**
- `/auth/login` - Login (blackroad-template-09-auth.html)
- `/auth/signup` - Signup (blackroad-template-09-auth.html)

**Demos:**
- `/demos` - Demo gallery (custom page with grid)
- `/demos/earth` - 3D Earth map (blackroad-earth-street.html)
- `/demos/motion` - Motion showcase (blackroad-animation.html)
- `/demos/world` - Living world (blackroad-living-world.html)
- `/demos/game` - City builder (blackroad-game.html)

**Error Pages:**
- `/404` - Not Found (blackroad-template-10-error.html)

---

## 🔄 Update Process

### 1. Update Templates

```bash
# Edit templates
cd website/templates
# Make changes to HTML files

# Copy to frontend
cp *.html ../frontend/public/templates/
```

### 2. Deploy

```bash
cd website/frontend
vercel --prod
```

---

## 🎯 Next Steps

### Phase 1 (Week 1)
- [x] Set up Next.js structure
- [x] Create all page routes
- [x] Integrate templates
- [ ] Deploy to Vercel
- [ ] Configure domain (carpool.blackroad.io)
- [ ] Add Clerk authentication

### Phase 2 (Week 2)
- [ ] Convert templates to React components
- [ ] Add Tailwind styling
- [ ] Implement real API connections
- [ ] Add user dashboard functionality

### Phase 3 (Week 3)
- [ ] Stripe integration for payments
- [ ] Conversation interface
- [ ] Agent management
- [ ] Settings page

### Phase 4 (Week 4)
- [ ] Blog CMS integration
- [ ] Analytics setup
- [ ] Performance optimization
- [ ] Production launch

---

## 📝 Notes

- All templates are currently served via iframes for rapid deployment
- This allows immediate production deployment while we convert to React
- Templates are self-contained with no external dependencies
- Future: Convert to proper Next.js pages with Tailwind + Framer Motion

---

## 🆘 Troubleshooting

### iframes not loading
- Check that files exist in `public/templates/`
- Verify X-Frame-Options headers in next.config.js

### Build failures
- Run `npm run type-check` to find TypeScript errors
- Check that all dependencies are installed

### Domain not resolving
- Verify Cloudflare DNS settings
- Check Vercel domain configuration
- Wait 5-10 minutes for DNS propagation

---

**Ready for deployment!** 🚀

Run `npm run dev` to test locally, then `vercel` to deploy.
