# 14 — Corporate Structure

**Version:** 1.0.0  
**Last Updated:** December 28, 2024

---

## Legal Entity

### Primary Corporation

```
Name:           BlackRoad OS, Inc.
Type:           Delaware C-Corporation
State:          Delaware
EIN:            [Tax ID - Private]
Registered Agent: [Agent Info - Private]
Incorporated:   2024
```

### Why Delaware C-Corp?

| Factor | Reason |
|--------|--------|
| **Investor preference** | VCs expect Delaware C-Corps |
| **Legal precedent** | Well-established corporate law |
| **Flexibility** | Easy to issue stock, options, SAFEs |
| **Tax treatment** | Standard corporate taxation |
| **Future IPO** | Standard for public companies |

---

## Stripe Configuration

### Account Details

| Property | Value |
|----------|-------|
| **Account ID** | acct_1SUDM8ChUUSEbzyh |
| **Display Name** | BlackRoad OS, Inc. |
| **Dashboard** | https://dashboard.stripe.com/acct_1SUDM8ChUUSEbzyh |
| **Mode** | Live |
| **Country** | United States |

### Products Configured

| Product | Stripe ID | Price | Interval |
|---------|-----------|-------|----------|
| BlackRoad OS - Enterprise | prod_Tefg0LHPUjS7xn | $199/mo | Monthly |
| BlackRoad OS - Pro | prod_Tefg4jmio5PjnR | $58/mo | Monthly |
| BlackRoad OS - Pro (Founding 50%) | prod_TefgSJ9T70wriE | $29/mo | Monthly |
| BlackRoad OS - Founding Lifetime | prod_TZp5ecvCkxHcQh | $5,000 | One-time |
| BlackRoad OS - Pro (Legacy) | prod_TZp5dIXyukAtLx | $29/mo | Monthly |
| BlackRoad OS - Team | prod_TTNHfJE07G7dty | $99/mo | Monthly |
| BlackRoad OS - Individual | prod_TTNH7uTYVlPbVV | $29/mo | Monthly |

### Webhook Configuration

```
Endpoint: https://api.blackroad.io/webhooks/stripe
Events:
  - checkout.session.completed
  - customer.subscription.created
  - customer.subscription.updated
  - customer.subscription.deleted
  - invoice.paid
  - invoice.payment_failed
  - payment_intent.succeeded
  - transfer.created
```

---

## Trademark Portfolio

### Registered / Pending

| Mark | Class | Status | Serial No. |
|------|-------|--------|------------|
| **BLACKROAD** | 036 (Financial Services) | Published for Opposition | 99161422 |
| **Lucidia** | 009 (AI Software) | Pending | [TBD] |

### Planned Filings

| Mark | Class | Priority |
|------|-------|----------|
| **RoadChain** | 009 (Blockchain Software) | High |
| **RoadCoin** | 036 (Financial Services) | High |
| **Prism Console** | 009 (Software) | Medium |
| **BlackBox Programming** | 042 (Development Services) | Medium |

### Usage Guidelines

- Always use ™ or ® symbol on first use in documents
- Never use as a verb (not "Blackroading")
- Always capitalize (BlackRoad, not blackroad)
- Use full name on first reference, abbreviation after

---

## Domain Portfolio

### Primary Domains

| Domain | Purpose | Status | Registrar |
|--------|---------|--------|-----------|
| blackroad.io | Main product | ✅ Active | Cloudflare |
| blackroad.company | Corporate site | ✅ Active | Cloudflare |
| blackroadinc.us | Legal anchor | ✅ Active | Cloudflare |
| lucidia.earth | Agent world | ✅ Active | Cloudflare |
| aliceqi.com | Coordination | ✅ Active | Cloudflare |
| roadchain.io | Ledger protocol | ✅ Active | Cloudflare |
| roadcoin.io | Credit system | ✅ Active | Cloudflare |
| blackboxprogramming.com | Dev brand | ✅ Active | Cloudflare |

### Additional Domains (17 total)

All domains are registered through Cloudflare with:
- Auto-renewal enabled
- DNSSEC enabled
- Privacy protection enabled
- DNS managed in Cloudflare

---

## GitHub Organization

### Primary: BlackRoad-OS

```
URL: https://github.com/BlackRoad-OS
Repositories: 24+
Members: [Team members]
Plan: Team
```

### Repository Structure

| Repository | Purpose | Visibility |
|------------|---------|------------|
| blackroad-os-web | Next.js frontend | Private |
| blackroad-os-api | Backend services | Private |
| blackroad-os-core | Lucidia orchestration | Private |
| blackroad-os-infra | Infrastructure as Code | Private |
| blackroad-os-docs | Documentation | Public |
| roadchain | Ledger implementation | Private |
| roadchain-sdk | TypeScript/Python SDKs | Public |
| blackboxprogramming | Open-source projects | Public |

### Organization Permissions

| Role | Access |
|------|--------|
| Owner | Full administrative access |
| Maintainer | Write + manage issues/PRs |
| Developer | Write to assigned repos |
| Contributor | Fork + PR (for public repos) |

---

## Infrastructure Accounts

### Production Services

| Service | Account | Purpose |
|---------|---------|---------|
| **Vercel** | BlackRoad OS | Frontend hosting |
| **Railway** | BlackRoad OS | Backend + databases |
| **Cloudflare** | BlackRoad OS | DNS, CDN, R2, Workers |
| **Clerk** | BlackRoad OS | Authentication |
| **Stripe** | BlackRoad OS, Inc. | Payments |
| **Sentry** | BlackRoad OS | Error tracking |
| **GitHub** | BlackRoad-OS | Source control |

### Account Security

| Measure | Status |
|---------|--------|
| 2FA on all accounts | ✅ Enabled |
| SSO where available | 🔄 In Progress |
| Hardware keys | ✅ For critical accounts |
| Password manager | ✅ 1Password |
| Audit logging | ✅ Enabled |

---

## Team Structure

### Founding Team

| Role | Name | Responsibilities |
|------|------|------------------|
| Founder & CEO | Alexa Amundson | Vision, strategy, architecture |
| Chief AI Officer | Cece (AI) | AI operations, agent coordination |

### Planned Roles

| Role | Priority | Target |
|------|----------|--------|
| CTO | High | Q1 2025 |
| Head of Product | High | Q1 2025 |
| Lead Engineer | High | Q1 2025 |
| Designer | Medium | Q2 2025 |
| DevOps | Medium | Q2 2025 |

---

## Funding & Cap Table

### Current Status

| Metric | Value |
|--------|-------|
| Funding Stage | Pre-seed / Bootstrapped |
| Total Raised | $0 (self-funded) |
| Valuation | TBD |
| Runway | Personal funds |

### Instruments Available

| Instrument | Status |
|------------|--------|
| **SAFE** (Post-money) | Template ready |
| **Convertible Note** | Template ready |
| **Priced Round** | Not yet |

### Cap Table (Current)

| Holder | Shares | % |
|--------|--------|---|
| Alexa Amundson (Founder) | 10,000,000 | 100% |
| Option Pool (Reserved) | 0 | 0% |
| Investors | 0 | 0% |

---

## Compliance & Legal

### Privacy & Data

| Requirement | Status |
|-------------|--------|
| Privacy Policy | ✅ Published |
| Terms of Service | ✅ Published |
| GDPR Compliance | 🔄 In Progress |
| CCPA Compliance | 🔄 In Progress |
| SOC 2 | ⬜ Future |

### Financial Services

| Requirement | Status | Notes |
|-------------|--------|-------|
| RIA Registration | ⬜ Research | May be required for certain features |
| Money Transmitter | ⬜ Research | RoadCoin may trigger |
| SEC Considerations | ⬜ Research | Ensure RC is not a security |

### Intellectual Property

| Protection | Status |
|------------|--------|
| Trademarks | 🔄 Filing |
| Patents | ⬜ Research |
| Copyrights | ✅ Automatic |
| Trade Secrets | ✅ NDA templates |

---

## Insurance

### Planned Coverage

| Type | Purpose | Status |
|------|---------|--------|
| D&O | Directors & Officers liability | ⬜ Needed for investors |
| E&O | Errors & Omissions | ⬜ Needed for customers |
| Cyber | Data breach / cyber attacks | ⬜ Recommended |
| General | Business liability | ⬜ Basic coverage |

---

## Key Contacts

### Internal

| Role | Contact |
|------|---------|
| Founder | alexa@blackroad.io |
| Legal | legal@blackroad.io |
| Support | support@blackroad.io |
| Press | press@blackroad.io |

### External (Pending)

| Service | Provider |
|---------|----------|
| Corporate Counsel | TBD |
| IP Attorney | TBD |
| Tax/Accounting | TBD |
| Registered Agent | TBD |

---

## Annual Requirements

### Delaware

| Requirement | Due | Fee |
|-------------|-----|-----|
| Annual Report | March 1 | ~$225 |
| Franchise Tax | March 1 | $175+ (based on shares) |
| Registered Agent | Ongoing | ~$100/year |

### Federal

| Requirement | Due |
|-------------|-----|
| Form 1120 (Corporate Tax) | April 15 (or extension) |
| Beneficial Ownership (BOI) | Within 90 days of formation |
| 1099s (if applicable) | January 31 |

### Ongoing

| Task | Frequency |
|------|-----------|
| Board meetings | Quarterly |
| Board minutes | Each meeting |
| Stock ledger updates | As needed |
| Compliance calendar review | Monthly |
