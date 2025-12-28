# BlackRoad OS Corporate Documents

**⚠️ MOVED TO PRIVATE REPOSITORY**

All corporate documents have been moved to the private `blackroad-os-secrets` repository for security.

---

## 🔒 Location

**Private Repository:** [BlackRoad-OS/blackroad-os-secrets](https://github.com/BlackRoad-OS/blackroad-os-secrets)

```bash
# Clone the secrets repository (requires access)
git clone https://github.com/BlackRoad-OS/blackroad-os-secrets.git

# Location on local machine
cd /Users/alexa/blackroad-os-secrets
```

---

## 📂 What's Stored There

### Corporate Documents (`/corporate/incorporation/`)
- ✅ Certificate of Incorporation
- ✅ Bylaws
- ✅ Stock certificates
- ✅ Section 83(b) election
- ✅ CIIAA (IP assignment)
- ✅ RSPA (stock purchase agreement)
- ✅ Indemnification agreements
- ✅ Tax documents (SS-4, CP 575, Form 8821)
- ✅ Board actions and consents
- ✅ BrokerCheck credentials

**Total:** 18 documents, 4.5MB

### Credentials (`/credentials/`)
- API keys for all services
- SSH keys for servers
- SSL/TLS certificates

### Legal (`/legal/`)
- Contracts
- NDAs
- Patent filings

### Financial (`/financial/`)
- Banking information
- Tax returns
- Payroll data

---

## 🔐 Why Moved to Private Repo?

**Security Best Practices:**
1. ✅ Sensitive documents in private repository only
2. ✅ Separated from public codebase
3. ✅ Better access control
4. ✅ Audit trail for document access
5. ✅ Encrypted in transit and at rest

**This Repo (blackroad-os-carpool):**
- Public or semi-public codebase
- Product development
- Documentation
- Templates and frontend

**Secrets Repo (blackroad-os-secrets):**
- Private only
- Corporate documents
- Credentials and keys
- Sensitive information

---

## 📝 Local Reference

A **local copy** of corporate documents is maintained at:
```
/Users/alexa/blackroad-os-carpool/corporate/incorporation/
```

**However, this directory is:**
- ✅ Excluded from Git via `.gitignore`
- ✅ Never committed to this repository
- ✅ Used for local reference only

**Source of Truth:** [blackroad-os-secrets](https://github.com/BlackRoad-OS/blackroad-os-secrets)

---

## 🔗 Access

**Who has access:**
- Alexa Louise Amundson (Owner)
- Authorized team members only

**To request access:**
```bash
# Owner grants access
gh api repos/BlackRoad-OS/blackroad-os-secrets/collaborators/[username] -X PUT
```

**Security Requirements:**
- 2FA enabled on GitHub
- Trusted devices only
- Never clone on public machines

---

## 📚 Documentation

For detailed information, see:
- [blackroad-os-secrets/README.md](https://github.com/BlackRoad-OS/blackroad-os-secrets/blob/master/README.md)
- [corporate/incorporation/README.md](https://github.com/BlackRoad-OS/blackroad-os-secrets/blob/master/corporate/incorporation/README.md)

---

**Repository Created:** December 28, 2024
**Status:** ✅ All documents secured in private repository
**Access:** 🔐 Private access only

**For corporate document needs, use the [blackroad-os-secrets](https://github.com/BlackRoad-OS/blackroad-os-secrets) repository.**
