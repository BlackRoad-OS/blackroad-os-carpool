# Secrets Integration — BlackRoad OS Corporate Documents

**Created:** December 28, 2024
**Status:** ✅ Complete and secure

---

## 🔐 Two-Repository Strategy

BlackRoad OS uses a **two-repository strategy** for maximum security:

### 1. **blackroad-os-carpool** (This Repo)
- **Visibility:** Public or semi-public
- **Purpose:** Product development, documentation, templates
- **URL:** https://github.com/BlackRoad-OS/blackroad-os-carpool
- **Contains:** Code, templates, docs, frontend

### 2. **blackroad-os-secrets** (Private Repo)
- **Visibility:** Private (access controlled)
- **Purpose:** Corporate documents, credentials, sensitive data
- **URL:** https://github.com/BlackRoad-OS/blackroad-os-secrets
- **Contains:** Incorporation docs, API keys, certificates

---

## 📂 What's Where

### In blackroad-os-carpool (Public)
```
blackroad-os-carpool/
├── corporate/
│   └── README.md               ← Reference pointing to secrets repo
├── docs/
│   ├── DOMAIN_EMPIRE.md        ← Domain strategy (public info)
│   └── SECRETS_INTEGRATION.md  ← This file
├── website/                    ← CarPool frontend
└── [other public code]
```

**Local copy only (gitignored):**
```
blackroad-os-carpool/
└── corporate/
    └── incorporation/          ← Local reference copy (NOT in Git)
        └── *.pdf               ← 18 PDFs (blocked by .gitignore)
```

### In blackroad-os-secrets (Private)
```
blackroad-os-secrets/
├── corporate/
│   └── incorporation/          ← SOURCE OF TRUTH
│       ├── README.md
│       └── [18 PDF files]      ← All Atlas documents
├── credentials/
│   ├── api-keys/               ← API keys by service
│   ├── ssh-keys/               ← SSH keys
│   └── certificates/           ← SSL/TLS certs
├── legal/                      ← Contracts, NDAs, patents
├── financial/                  ← Banking, tax, payroll
└── backups/                    ← Encrypted backups
```

---

## 🔗 How They Connect

### Reference Link
The **public repo** has a reference document:
- `/corporate/README.md` → Points to private repo
- Contains no sensitive information
- Explains where to find corporate docs

### Local Sync
Both repos can exist on the same machine:
```
/Users/alexa/
├── blackroad-os-carpool/       ← Product repo
│   └── corporate/
│       ├── README.md           ← Reference (in Git)
│       └── incorporation/      ← Local copy (NOT in Git)
│
└── blackroad-os-secrets/       ← Secrets repo
    └── corporate/
        └── incorporation/      ← Source of truth (in Git)
```

---

## 🛡️ Security Model

### GitIgnore Protection (carpool repo)
```gitignore
# Corporate documents - NEVER commit!
/corporate/**/*.pdf              ← Block all PDFs
/corporate/**/                   ← Block subdirectories
!corporate/                      ← Allow corporate/ directory
!corporate/README.md             ← Allow reference file
```

### Access Control (secrets repo)
- ✅ Private repository
- ✅ 2FA required
- ✅ Access by invitation only
- ✅ Audit trail for all changes

---

## 📋 Corporate Documents Inventory

All stored in **blackroad-os-secrets** repo:

### Formation Documents (5 files)
1. Certificate of Incorporation (Approved) — 1.7MB
2. Certificate of Incorporation (Signed) — 34KB
3. Bylaws — 142KB
4. Sole Incorporator Consent — 32KB
5. Secretary Certificate (Bylaws) — 30KB

### Stock & Equity (5 files)
6. Common Stock Certificate (Alexa) — 37KB
7. RSPA (Restricted Stock Purchase Agreement) — 107KB
8. Section 83(b) Election — 29KB ⚡ CRITICAL
9. Stock Assignment — 33KB
10. Joint Escrow Instructions — 47KB

### Employment & Legal (3 files)
11. CIIAA (IP Assignment) — 107KB
12. Indemnification Agreement — 94KB
13. Stockholder Consent — 38KB

### Tax Documents (3 files)
14. SS-4 (EIN Application) — 907KB
15. CP 575 Letter (EIN Confirmation) — 20KB
16. Form 8821 — 767KB

### Board Actions (2 files)
17. Initial Board Action — 63KB
18. BrokerCheck Credentials — 287KB

**Total:** 18 documents, 4.5MB

---

## 🔑 Credentials Management

API keys and credentials are stored in **blackroad-os-secrets** only:

### Service Categories
```
credentials/api-keys/
├── clerk.env           → Authentication
├── stripe.env          → Payments
├── mapbox.env          → Maps
├── openai.env          → OpenAI API
├── anthropic.env       → Claude API
├── google-ai.env       → Gemini API
├── cloudflare.env      → Infrastructure
├── railway.env         → Hosting
├── vercel.env          → Deployments
└── github.env          → Automation
```

### Usage Pattern
```bash
# Load from secrets repo
source /Users/alexa/blackroad-os-secrets/credentials/api-keys/clerk.env

# Or copy to project .env (gitignored)
cp ~/blackroad-os-secrets/credentials/api-keys/clerk.env ~/blackroad-os-carpool/.env.local
```

---

## ✅ Current Status

**Setup Complete:** December 28, 2024

### Repositories
- ✅ blackroad-os-secrets created (private)
- ✅ blackroad-os-carpool protected (.gitignore updated)
- ✅ Cross-references established

### Documents
- ✅ All 18 Atlas documents uploaded to secrets repo
- ✅ BrokerCheck credentials included
- ✅ Local copies maintained in carpool repo (gitignored)
- ✅ README files created in both repos

### Security
- ✅ All PDFs blocked from public commits
- ✅ Private repo access controlled
- ✅ Reference documents safe to commit
- ✅ Credentials structure ready for API keys

**Everything is secure and ready to use!** 🔐

---

**Last Updated:** December 28, 2024
**Status:** ✅ Production-ready
**Security Level:** 🔒 Maximum (two-repo strategy)
