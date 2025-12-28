# BlackRoad.io Website

**CarPool by BlackRoad OS, Inc.**

This directory contains all website-related code for blackroad.io.

---

## Directory Structure

```
website/
├── frontend/          # Next.js 14 frontend application
│   ├── app/          # Next.js App Router
│   ├── components/   # React components
│   ├── lib/          # Utilities and helpers
│   ├── public/       # Static assets
│   └── styles/       # Global styles
│
├── backend/          # Website-specific backend (if needed)
│   ├── routes/       # Additional API routes
│   └── middleware/   # Custom middleware
│
├── templates/        # Email, document, and page templates
│   ├── emails/       # Email templates (Resend/SendGrid)
│   ├── pdfs/         # PDF generation templates
│   └── pages/        # Static page templates
│
├── components/       # Shared components (design system)
│   ├── ui/           # shadcn/ui components
│   ├── marketing/    # Landing page components
│   ├── app/          # Application components
│   └── shared/       # Cross-platform components
│
└── assets/           # Design assets
    ├── images/       # Images, logos, icons
    ├── fonts/        # Custom fonts
    ├── videos/       # Marketing videos
    └── mockups/      # Figma/design mockups

```

---

## Frontend (`/frontend`)

### Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **Auth:** Clerk
- **State:** Zustand
- **Data Fetching:** TanStack Query
- **Icons:** Lucide React

### Key Routes

```
/                    → Landing page
/pricing             → Pricing plans
/docs                → Documentation
/blog                → Blog (optional)
/about               → About us
/contact             → Contact form

/app                 → Main workspace (auth required)
/app/chat            → Chat interface
/app/settings        → Settings
/app/agents          → Agent gallery
```

### Development

```bash
cd frontend
npm install
npm run dev
```

### Deployment

Deployed to Vercel via GitHub integration.

---

## Backend (`/backend`)

### Purpose

Website-specific backend logic that doesn't belong in the main API:
- Contact form handling
- Newsletter subscriptions
- Blog post management (if self-hosted)
- Marketing analytics

### Tech Stack

- **Framework:** Next.js API Routes (preferred for simplicity)
- **Or:** Separate FastAPI/Hono service if needed

---

## Templates (`/templates`)

### Email Templates

Located in `/templates/emails`:

```
welcome.html           → Welcome email
verify-email.html      → Email verification
password-reset.html    → Password reset
upgrade-success.html   → Upgrade confirmation
invoice.html           → Invoice/receipt
```

**Tech:** Resend + React Email (or Handlebars)

### PDF Templates

Located in `/templates/pdfs`:

```
invoice.pdf.hbs        → Invoice generation
contract.pdf.hbs       → Service agreement
report.pdf.hbs         → Usage report
```

**Tech:** Puppeteer or jsPDF

### Page Templates

Located in `/templates/pages`:

```
landing-v1.html        → Landing page variations
pricing-v1.html        → Pricing page variations
```

---

## Components (`/components`)

Shared design system components used across frontend.

### UI Components (`/ui`)

shadcn/ui components:
- Button, Input, Card, Dialog, etc.
- Based on Radix UI primitives
- Styled with Tailwind CSS

### Marketing Components (`/marketing`)

Landing page specific:
- Hero, Features, Testimonials, CTA, Footer

### App Components (`/app`)

Application-specific:
- ChatInterface, AgentCard, WorkspaceSelector, etc.

---

## Assets (`/assets`)

### Images

```
/images/
├── logo.svg              → BlackRoad logo
├── logo-light.svg        → Light mode variant
├── logo-dark.svg         → Dark mode variant
├── hero-bg.png           → Hero background
├── features/             → Feature screenshots
└── agents/               → Agent avatars
```

### Brand Colors

From brand guidelines:
```css
:root {
  --primary: #FF9D08;      /* Orange */
  --secondary: #FF0066;    /* Pink */
  --accent: #7780FF;       /* Purple */
  --highlight: #0866FF;    /* Blue */
}
```

### Typography

```
Headings: Inter (Google Fonts)
Body: Inter
Mono: JetBrains Mono
```

---

## Environment Variables

### Frontend (.env.local)

```bash
# Clerk Auth
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...

# API
NEXT_PUBLIC_API_URL=https://api.blackroad.io

# Analytics (optional)
NEXT_PUBLIC_POSTHOG_KEY=...
NEXT_PUBLIC_GA_ID=...
```

### Backend (.env)

```bash
# Email
RESEND_API_KEY=...

# Newsletter
MAILCHIMP_API_KEY=...
```

---

## Deployment

### Frontend

**Provider:** Vercel
**Domain:** blackroad.io, app.blackroad.io
**Auto-deploy:** Push to `main` branch

### Backend

**Provider:** Railway (if separate from main API)
**Or:** Next.js API routes on Vercel

---

## Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/BlackRoad-OS/blackroad-os-carpool.git
cd blackroad-os-carpool/website/frontend
npm install
```

### 2. Set Up Environment

```bash
cp .env.example .env.local
# Fill in values
```

### 3. Run Development Server

```bash
npm run dev
# Open http://localhost:3000
```

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## Documentation

- [Vision](../docs/01-VISION.md) - Product vision
- [Architecture](../docs/02-ARCHITECTURE.md) - System design
- [Components](../docs/06-COMPONENTS.md) - Component inventory
- [Deployment](../docs/08-DEPLOYMENT.md) - Deployment guide

---

**Built by BlackRoad OS, Inc.**
