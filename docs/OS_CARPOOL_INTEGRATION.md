# OS ↔ CarPool Integration — Domain Architecture

**Created:** December 28, 2024
**Status:** ✅ Ready for deployment

---

## 🌐 Domain Structure

BlackRoad uses a **multi-domain architecture** where each product has its own subdomain:

```
                    🌌 BLACKROAD ECOSYSTEM 🌌

        ┌─────────────────┬──────────────────┬─────────────────┐
        │                 │                  │                 │
   🏢 COMPANY         🎯 PRODUCTS        💰 ECONOMICS      🤖 AI/AGENTS
        │                 │                  │                 │
        │                 │                  │                 │
  os.blackroad.io    carpool.blackroad.io  roadchain.io  lucidia.earth
  (landing page)     (multi-AI platform)   (blockchain)  (agent world)
```

---

## 🎯 Domain Responsibilities

### os.blackroad.io (Main Landing)
- **Purpose:** Ecosystem overview and company landing page
- **Template:** `blackroad-os-landing.html` (82KB)
- **Content:**
  - What is BlackRoad OS?
  - Complete ecosystem showcase
  - Links to all products (CarPool, Lucidia, RoadChain, RoadCoin)
  - Company mission and vision
  - Getting started guide

- **Target Audience:** New visitors, investors, press
- **CTA:** "Try CarPool" → Directs to `carpool.blackroad.io`

### carpool.blackroad.io (Product)
- **Purpose:** CarPool multi-AI orchestration platform
- **Stack:** Next.js 14 frontend (`website/frontend/`)
- **Content:**
  - Product features
  - Pricing and plans
  - User dashboard
  - Documentation
  - Blog/updates

- **Target Audience:** Users, developers, customers
- **CTA:** Sign up, start trial, access dashboard

---

## 🔗 Integration Points

### 1. Navigation Flow

**User Journey:**
```
Google Search "AI orchestration"
    ↓
Lands on os.blackroad.io (ecosystem overview)
    ↓
Sees "CarPool — Bring any AI" product card
    ↓
Clicks "Learn More" or "Try CarPool"
    ↓
Redirects to carpool.blackroad.io
    ↓
User signs up / explores product
```

### 2. Cross-Domain Links

**From os.blackroad.io:**
```html
<!-- Product Cards -->
<a href="https://carpool.blackroad.io">
  <h3>CarPool</h3>
  <p>Bring any AI. Train your own. Never leave.</p>
  <button>Try CarPool →</button>
</a>

<a href="https://lucidia.earth">
  <h3>Lucidia</h3>
  <p>Agent world in Unity metaverse</p>
  <button>Enter Lucidia →</button>
</a>

<a href="https://roadchain.io">
  <h3>RoadChain</h3>
  <p>Blockchain protocol for compute</p>
  <button>Learn More →</button>
</a>
```

**From carpool.blackroad.io:**
```html
<!-- Header/Footer -->
<nav>
  <a href="https://os.blackroad.io">BlackRoad OS</a>
  <a href="https://carpool.blackroad.io">CarPool</a>
  <a href="https://lucidia.earth">Lucidia</a>
</nav>

<!-- Breadcrumb -->
<div class="breadcrumb">
  <a href="https://os.blackroad.io">BlackRoad OS</a> /
  <a href="https://carpool.blackroad.io">CarPool</a>
</div>
```

### 3. Shared Branding

**Both domains use:**
- ✅ Same color palette (amber, hot-pink, electric-blue, violet)
- ✅ Same typography (JetBrains Mono)
- ✅ Same spacing (golden ratio φ = 1.618)
- ✅ Same animation easing (Apple cubic-bezier)
- ✅ Same glassmorphism style

**Visual Consistency:**
```css
/* Shared CSS Variables */
:root {
    --black: #000000;
    --white: #FFFFFF;
    --amber: #F5A623;
    --hot-pink: #FF1D6C;
    --electric-blue: #2979FF;
    --violet: #9C27B0;

    --gradient-brand: linear-gradient(135deg,
        var(--amber) 0%,
        var(--hot-pink) 38.2%,
        var(--violet) 61.8%,
        var(--electric-blue) 100%
    );
}
```

---

## 📂 Repository Structure

### This Repo (blackroad-os-carpool)

```
blackroad-os-carpool/
├── website/
│   ├── templates/
│   │   ├── blackroad-os-landing.html      ← os.blackroad.io landing
│   │   └── blackroad-template-*.html      ← carpool.blackroad.io pages
│   │
│   └── frontend/                          ← carpool.blackroad.io Next.js app
│       ├── app/
│       │   ├── page.tsx                   → carpool.blackroad.io/
│       │   ├── about/                     → carpool.blackroad.io/about
│       │   ├── pricing/                   → carpool.blackroad.io/pricing
│       │   └── app/                       → carpool.blackroad.io/app (dashboard)
│       └── public/
│           └── templates/                 ← Templates served via iframe
│
└── docs/
    ├── DOMAIN_EMPIRE.md                   ← Full domain strategy
    ├── OS_CARPOOL_INTEGRATION.md          ← This file
    └── SECRETS_INTEGRATION.md             ← Private repo connection
```

---

## 🚀 Deployment Strategy

### Option 1: Vercel (Recommended)

**Deploy os.blackroad.io:**
```bash
# Static HTML deployment
vercel --prod

# Configure custom domain
# Domain: os.blackroad.io
# Target: cname.vercel-dns.com
```

**Deploy carpool.blackroad.io:**
```bash
cd website/frontend
vercel --prod

# Configure custom domain
# Domain: carpool.blackroad.io
# Target: cname.vercel-dns.com
```

### Option 2: Cloudflare Pages

**Both can be deployed to Cloudflare Pages:**

```bash
# OS Landing
wrangler pages publish website/templates/blackroad-os-landing.html \
  --project-name=blackroad-os-landing \
  --branch=main

# CarPool App
cd website/frontend
npm run build
wrangler pages publish .next \
  --project-name=carpool-blackroad \
  --branch=main
```

### DNS Configuration (Cloudflare)

```
Type: CNAME
Name: os
Target: cname.vercel-dns.com (or Cloudflare Pages URL)

Type: CNAME
Name: carpool
Target: cname.vercel-dns.com (or Cloudflare Pages URL)
```

---

## 🎨 Branding Integration

### Logo Usage

**os.blackroad.io:**
- Full "BlackRoad OS" logo
- Tagline: "The Complete AI Ecosystem"
- Emphasis on ecosystem

**carpool.blackroad.io:**
- "CarPool" product logo
- Tagline: "Bring any AI. Train your own. Never leave."
- Emphasis on product features

### Color Coding (Optional)

**Product Color Themes:**
- **os.blackroad.io** → Full gradient (amber → pink → violet → blue)
- **carpool.blackroad.io** → Amber/Hot-pink emphasis
- **lucidia.earth** → Violet/Electric-blue emphasis
- **roadchain.io** → Electric-blue/Violet emphasis
- **roadcoin.io** → Amber/Orange emphasis

---

## 📊 Analytics & Tracking

### Cross-Domain Tracking

**Google Analytics 4:**
```html
<!-- Both domains -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    'linker': {
      'domains': ['os.blackroad.io', 'carpool.blackroad.io']
    }
  });
</script>
```

### Conversion Tracking

**Events to track:**
- `os_to_carpool_click` — User clicks CarPool CTA from OS landing
- `carpool_signup` — User signs up on CarPool
- `carpool_trial_start` — User starts trial
- `ecosystem_navigation` — Movement between domains

---

## 🔐 Authentication Integration

### Shared Auth (Clerk)

**Both domains can share authentication:**

```javascript
// Clerk configuration
const clerkConfig = {
  publishableKey: process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY,
  // Enable cross-domain auth
  isSatellite: false, // os.blackroad.io (primary)
  domain: 'blackroad.io',
  signInUrl: 'https://carpool.blackroad.io/auth/login',
}
```

**User Flow:**
1. User visits `os.blackroad.io` (not logged in)
2. Clicks "Try CarPool" → redirects to `carpool.blackroad.io`
3. Signs up on `carpool.blackroad.io`
4. Returns to `os.blackroad.io` → automatically logged in (shared session)

---

## 🌟 Feature Showcase

### os.blackroad.io Features

```html
<section class="products">
  <div class="product-card">
    <h3>🚀 CarPool</h3>
    <p>Multi-AI orchestration platform</p>
    <ul>
      <li>✅ BYO-Everything (API keys, models, data)</li>
      <li>✅ Train & fork models</li>
      <li>✅ Never leave your data</li>
      <li>✅ Model comparison tools</li>
    </ul>
    <a href="https://carpool.blackroad.io">Try CarPool →</a>
  </div>

  <div class="product-card">
    <h3>🌍 Lucidia</h3>
    <p>Agent world in Unity metaverse</p>
    <a href="https://lucidia.earth">Enter Lucidia →</a>
  </div>

  <div class="product-card">
    <h3>⛓️ RoadChain</h3>
    <p>Blockchain protocol for AI compute</p>
    <a href="https://roadchain.io">Learn More →</a>
  </div>

  <div class="product-card">
    <h3>💰 RoadCoin</h3>
    <p>Cryptocurrency for compute credits</p>
    <a href="https://roadcoin.io">Get RoadCoin →</a>
  </div>
</section>
```

---

## 🎯 SEO Strategy

### Keyword Targeting

**os.blackroad.io:**
- "AI ecosystem"
- "complete AI platform"
- "BlackRoad OS"
- "AI infrastructure"
- Generic AI company keywords

**carpool.blackroad.io:**
- "multi AI platform"
- "AI orchestration"
- "bring your own AI keys"
- "model forking"
- "train AI models"
- Product-specific keywords

### Meta Tags

**os.blackroad.io:**
```html
<title>BlackRoad OS — The Complete AI Ecosystem</title>
<meta name="description" content="Complete AI ecosystem with CarPool (multi-AI platform), Lucidia (agent world), RoadChain (blockchain), and RoadCoin (crypto).">
```

**carpool.blackroad.io:**
```html
<title>CarPool — Bring any AI. Train your own. Never leave.</title>
<meta name="description" content="Multi-AI orchestration platform with BYO-Everything. Bring your API keys, train models, fork and fine-tune, never leave your data.">
```

---

## 🔄 Update Workflow

### Adding New Product to Ecosystem

1. **Update os.blackroad.io:**
   ```html
   <!-- Add new product card -->
   <div class="product-card">
     <h3>New Product</h3>
     <p>Description</p>
     <a href="https://newproduct.blackroad.io">Try It →</a>
   </div>
   ```

2. **Update DOMAIN_EMPIRE.md:**
   - Add domain to inventory
   - Update SEO strategy
   - Document integration points

3. **Deploy:**
   ```bash
   vercel --prod
   ```

---

## ✅ Checklist for Launch

### os.blackroad.io
- [ ] Deploy `blackroad-os-landing.html` to hosting
- [ ] Configure DNS (os.blackroad.io → CNAME)
- [ ] Test all product links (CarPool, Lucidia, RoadChain, RoadCoin)
- [ ] Add analytics tracking
- [ ] Test mobile responsiveness
- [ ] SSL certificate verified

### carpool.blackroad.io
- [ ] Deploy Next.js frontend to Vercel
- [ ] Configure DNS (carpool.blackroad.io → CNAME)
- [ ] Add Clerk authentication
- [ ] Link back to os.blackroad.io in nav/footer
- [ ] Test all page routes (/, /about, /pricing, /app, etc.)
- [ ] SSL certificate verified

### Integration
- [ ] Cross-domain tracking configured
- [ ] Shared authentication working
- [ ] Branding consistent across both domains
- [ ] All CTAs and links tested
- [ ] Mobile navigation working

---

## 📚 Related Documentation

- [DOMAIN_EMPIRE.md](./DOMAIN_EMPIRE.md) — Complete domain strategy (17+ domains)
- [SECRETS_INTEGRATION.md](./SECRETS_INTEGRATION.md) — Private repo connection
- [website/frontend/DEPLOYMENT.md](../website/frontend/DEPLOYMENT.md) — CarPool deployment guide
- [website/templates/TEMPLATE_INVENTORY.md](../website/templates/TEMPLATE_INVENTORY.md) — All templates catalog

---

**Status:** ✅ Ready for deployment
**Created:** December 28, 2024
**Next Step:** Deploy os.blackroad.io and configure DNS

**The ecosystem is ready to go live!** 🌌
