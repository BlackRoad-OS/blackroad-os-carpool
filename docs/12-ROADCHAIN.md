# 12 — RoadChain Protocol

**Version:** 1.0.0  
**Last Updated:** December 28, 2024  
**Domain:** roadchain.io

---

## Abstract

RoadChain is an append-only ledger that serves as the canonical source of truth for economic events, agent actions, and verification proofs within the BlackRoad OS ecosystem.

**It is NOT a blockchain** in the cryptocurrency sense — there is no mining, no consensus mechanism, no decentralization requirement. It is a **centralized, cryptographically-linked ledger** optimized for auditability, performance, and integration with traditional payment rails (Stripe).

---

## Design Philosophy

### What RoadChain Is

| Property | Description |
|----------|-------------|
| **Append-only** | Entries are never modified or deleted |
| **Cryptographically linked** | Each entry references the previous hash |
| **Centralized** | Single source of truth, no consensus needed |
| **Auditable** | Complete history of all economic events |
| **Stripe-mirrored** | Every fiat transaction has a RoadChain entry |

### What RoadChain Is NOT

| Property | Description |
|----------|-------------|
| **Not a cryptocurrency** | RoadCoin is an internal credit, not a token |
| **Not decentralized** | No blockchain, no mining, no gas fees |
| **Not speculative** | Credits have utility value, not investment value |
| **Not immutable** | We can fix bugs, but with full audit trail |

### Core Principles

```
1. EVERYTHING IS RECORDED
   Every credit grant, burn, transfer, and verification event
   gets a RoadChain entry. No off-ledger transactions.

2. HASH CHAINS PROVIDE INTEGRITY
   Each entry includes the hash of the previous entry.
   Tampering breaks the chain, detection is trivial.

3. STRIPE IS THE FIAT BRIDGE
   Real money moves through Stripe. RoadChain records
   the corresponding credit events. Two systems, one truth.

4. HUMANS CAN AUDIT
   The ledger is queryable. Balance sheets are derivable.
   No black boxes.
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     EXTERNAL WORLD                               │
│                                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐     │
│  │  Stripe  │   │  Users   │   │  Agents  │   │  Packs   │     │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘     │
└───────┼──────────────┼──────────────┼──────────────┼────────────┘
        │              │              │              │
        │ webhooks     │ actions      │ compute      │ purchases
        ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ROADCHAIN API GATEWAY                         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Webhook     │  │   REST API   │  │  Event Bus   │          │
│  │  Handlers    │  │   Handlers   │  │  Consumers   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼─────────────────┼─────────────────┼───────────────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ROADCHAIN CORE                                │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Entry Processor                        │  │
│  │                                                           │  │
│  │  1. Validate entry                                        │  │
│  │  2. Fetch previous hash                                   │  │
│  │  3. Compute new hash (PS-SHA∞)                            │  │
│  │  4. Write to database                                     │  │
│  │  5. Update balance cache                                  │  │
│  │  6. Archive to R2 (periodic)                              │  │
│  │  7. Emit events                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        STORAGE                                   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  PostgreSQL  │  │    Redis     │  │ Cloudflare   │          │
│  │  (Entries)   │  │  (Balances)  │  │  R2 (Archive)│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Entry Types

### Credit Grant (`credit_grant`)

Issued when credits are added to an entity's balance.

**Triggers:**
- Stripe payment completed (subscription, one-time)
- Manual admin grant
- Referral bonus
- Promotional credit

```json
{
  "entry_type": "credit_grant",
  "to_entity_type": "user",
  "to_entity_id": "usr_abc123",
  "amount": 2900.00,
  "currency": "ROADCOIN",
  "stripe_payment_intent_id": "pi_xyz789",
  "metadata": {
    "plan": "pro",
    "period": "monthly",
    "source": "stripe_subscription"
  }
}
```

### Credit Burn (`credit_burn`)

Issued when credits are consumed.

**Triggers:**
- AI model usage (tokens)
- Storage consumption
- API calls
- Agent compute

```json
{
  "entry_type": "credit_burn",
  "from_entity_type": "user",
  "from_entity_id": "usr_abc123",
  "amount": 15.50,
  "currency": "ROADCOIN",
  "metadata": {
    "resource": "gpt-4o",
    "tokens_input": 1200,
    "tokens_output": 450,
    "conversation_id": "conv_xyz"
  }
}
```

### Transfer (`transfer`)

Issued when credits move between entities.

**Triggers:**
- Pack purchase (buyer → creator)
- Agent-to-agent payment
- Tip or donation

```json
{
  "entry_type": "transfer",
  "from_entity_type": "user",
  "from_entity_id": "usr_buyer123",
  "to_entity_type": "user",
  "to_entity_id": "usr_creator456",
  "amount": 500.00,
  "currency": "ROADCOIN",
  "metadata": {
    "reason": "pack_purchase",
    "pack_id": "pack_finance",
    "net_to_creator": 350.00,
    "platform_fee": 150.00
  }
}
```

### Verification (`verification`)

Issued when a claim is cryptographically verified.

**Triggers:**
- Agent action proof
- Memory commit
- Audit checkpoint

```json
{
  "entry_type": "verification",
  "entity_type": "agent",
  "entity_id": "agt_cece",
  "amount": 0,
  "currency": "ROADCOIN",
  "metadata": {
    "claim": "task_execution",
    "task_id": "tsk_123",
    "input_hash": "sha256:abc...",
    "output_hash": "sha256:def...",
    "model_version": "claude-3-5-sonnet",
    "truth_state_hash": "ps-sha:ghi..."
  }
}
```

### Reward (`reward`)

Issued when an entity earns credits.

**Triggers:**
- Creator revenue share
- Referral bonus
- Achievement unlock

```json
{
  "entry_type": "reward",
  "to_entity_type": "user",
  "to_entity_id": "usr_creator456",
  "amount": 350.00,
  "currency": "ROADCOIN",
  "metadata": {
    "reason": "pack_revenue_share",
    "pack_id": "pack_finance",
    "sale_id": "sale_xyz",
    "gross_amount": 500.00,
    "percentage": 0.70
  }
}
```

### Payout (`payout`)

Issued when credits are converted to fiat.

**Triggers:**
- Creator withdrawal
- Refund to user

```json
{
  "entry_type": "payout",
  "from_entity_type": "user",
  "from_entity_id": "usr_creator456",
  "amount": 10000.00,
  "currency": "ROADCOIN",
  "metadata": {
    "fiat_amount": 90.00,
    "fiat_currency": "USD",
    "exchange_rate": 0.009,
    "fee_percentage": 0.10,
    "stripe_transfer_id": "tr_abc123"
  }
}
```

---

## Database Schema

### Core Tables

```sql
-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main entries table (append-only)
CREATE TABLE roadchain_entries (
  -- Identity
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  sequence_number BIGSERIAL UNIQUE,
  
  -- Entry type
  entry_type VARCHAR(50) NOT NULL,
  
  -- Parties
  from_entity_type VARCHAR(20),
  from_entity_id UUID,
  to_entity_type VARCHAR(20),
  to_entity_id UUID,
  
  -- Value
  amount DECIMAL(20, 8) NOT NULL DEFAULT 0,
  currency VARCHAR(10) NOT NULL DEFAULT 'ROADCOIN',
  
  -- External references
  stripe_payment_intent_id VARCHAR(255),
  stripe_invoice_id VARCHAR(255),
  stripe_transfer_id VARCHAR(255),
  stripe_subscription_id VARCHAR(255),
  
  -- Chain integrity
  previous_entry_id UUID REFERENCES roadchain_entries(id),
  previous_hash VARCHAR(128),
  entry_hash VARCHAR(128) NOT NULL,
  
  -- Metadata
  reason VARCHAR(100),
  metadata JSONB DEFAULT '{}',
  idempotency_key VARCHAR(255) UNIQUE,
  
  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Constraints
  CONSTRAINT valid_entry_type CHECK (
    entry_type IN (
      'credit_grant', 'credit_burn', 'transfer',
      'verification', 'reward', 'payout', 'adjustment'
    )
  ),
  CONSTRAINT valid_entity_type CHECK (
    (from_entity_type IS NULL OR from_entity_type IN ('user', 'org', 'agent', 'system')) AND
    (to_entity_type IS NULL OR to_entity_type IN ('user', 'org', 'agent', 'system'))
  ),
  CONSTRAINT valid_currency CHECK (
    currency IN ('ROADCOIN', 'USD', 'EUR', 'GBP')
  ),
  CONSTRAINT positive_amount CHECK (amount >= 0)
);

-- Indexes for common queries
CREATE INDEX idx_entries_to_entity ON roadchain_entries(to_entity_type, to_entity_id);
CREATE INDEX idx_entries_from_entity ON roadchain_entries(from_entity_type, from_entity_id);
CREATE INDEX idx_entries_type ON roadchain_entries(entry_type);
CREATE INDEX idx_entries_created ON roadchain_entries(created_at DESC);
CREATE INDEX idx_entries_hash ON roadchain_entries(entry_hash);
CREATE INDEX idx_entries_stripe_pi ON roadchain_entries(stripe_payment_intent_id);
CREATE INDEX idx_entries_sequence ON roadchain_entries(sequence_number DESC);

-- Balance cache (materialized view, updated on each entry)
CREATE TABLE roadchain_balances (
  entity_type VARCHAR(20) NOT NULL,
  entity_id UUID NOT NULL,
  currency VARCHAR(10) NOT NULL DEFAULT 'ROADCOIN',
  balance DECIMAL(20, 8) NOT NULL DEFAULT 0,
  last_entry_id UUID REFERENCES roadchain_entries(id),
  last_entry_sequence BIGINT,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  PRIMARY KEY (entity_type, entity_id, currency),
  CONSTRAINT non_negative_balance CHECK (balance >= 0)
);

CREATE INDEX idx_balances_entity ON roadchain_balances(entity_type, entity_id);

-- Audit log for admin actions
CREATE TABLE roadchain_audit_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  admin_user_id UUID NOT NULL,
  action VARCHAR(50) NOT NULL,
  target_entry_id UUID REFERENCES roadchain_entries(id),
  reason TEXT NOT NULL,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Entity Types

| Type | Description | Examples |
|------|-------------|----------|
| `user` | Human user | Individual accounts |
| `org` | Organization | Team/company accounts |
| `agent` | AI agent | Cece, Cadillac, custom agents |
| `system` | System account | Fees, treasury, operations |

### Reserved System Accounts

```sql
-- System accounts (pseudo-entities)
INSERT INTO roadchain_balances (entity_type, entity_id, currency, balance) VALUES
  ('system', '00000000-0000-0000-0000-000000000001', 'ROADCOIN', 0),  -- Treasury
  ('system', '00000000-0000-0000-0000-000000000002', 'ROADCOIN', 0),  -- Fees
  ('system', '00000000-0000-0000-0000-000000000003', 'ROADCOIN', 0),  -- Rewards Pool
  ('system', '00000000-0000-0000-0000-000000000004', 'ROADCOIN', 0);  -- Operations
```

---

## Cryptographic Primitives

### PS-SHA∞ (Persistent State SHA Infinity)

RoadChain uses PS-SHA∞ for entry hashing, providing:
- **Persistence** — Hash represents complete state history
- **Verification** — Any entry can be verified against the chain
- **Efficiency** — Single hash operation per entry

#### Hash Computation

```python
import hashlib
import json
from typing import Optional

def compute_entry_hash(entry: dict, previous_hash: Optional[str]) -> str:
    """
    Compute PS-SHA∞ hash for a RoadChain entry.
    
    The hash is computed over:
    1. Previous entry hash (or genesis marker)
    2. Entry type
    3. Parties (from/to)
    4. Amount and currency
    5. Timestamp
    6. Metadata (canonicalized)
    """
    
    # Canonicalize the entry
    canonical = {
        "prev": previous_hash or "GENESIS",
        "type": entry["entry_type"],
        "from": f"{entry.get('from_entity_type', 'null')}:{entry.get('from_entity_id', 'null')}",
        "to": f"{entry.get('to_entity_type', 'null')}:{entry.get('to_entity_id', 'null')}",
        "amount": str(entry["amount"]),
        "currency": entry["currency"],
        "ts": entry["created_at"].isoformat(),
        "meta": json.dumps(entry.get("metadata", {}), sort_keys=True),
    }
    
    # Serialize deterministically
    serialized = json.dumps(canonical, sort_keys=True, separators=(',', ':'))
    
    # Compute SHA-256
    hash_bytes = hashlib.sha256(serialized.encode('utf-8')).hexdigest()
    
    return f"ps-sha256:{hash_bytes}"
```

#### Chain Verification

```python
def verify_chain(entries: list[dict]) -> bool:
    """
    Verify the integrity of a chain of entries.
    Returns True if all hashes are valid, False otherwise.
    """
    previous_hash = None
    
    for entry in entries:
        expected_hash = compute_entry_hash(entry, previous_hash)
        
        if entry["entry_hash"] != expected_hash:
            print(f"Hash mismatch at sequence {entry['sequence_number']}")
            return False
        
        previous_hash = entry["entry_hash"]
    
    return True
```

---

## API Specification

### Base URL

```
https://api.blackroad.io/v1/roadchain
```

### Authentication

All endpoints require Bearer token authentication.

```
Authorization: Bearer <clerk_jwt>
```

### Create Entry

```http
POST /entries
```

**Request:**
```json
{
  "entry_type": "credit_burn",
  "from_entity_type": "user",
  "from_entity_id": "usr_abc123",
  "amount": 15.50,
  "currency": "ROADCOIN",
  "reason": "model_usage",
  "metadata": {
    "model": "gpt-4o",
    "tokens": 1650
  },
  "idempotency_key": "usage_conv123_msg456"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "ent_xyz789",
    "sequence_number": 42069,
    "entry_hash": "ps-sha256:abc123...",
    "balance_after": 2884.50,
    "created_at": "2024-12-28T12:00:00Z"
  }
}
```

### Get Balance

```http
GET /balances/:entity_type/:entity_id
```

**Response:**
```json
{
  "success": true,
  "data": {
    "entity_type": "user",
    "entity_id": "usr_abc123",
    "balances": {
      "ROADCOIN": 2884.50
    },
    "last_entry_sequence": 42069,
    "updated_at": "2024-12-28T12:00:00Z"
  }
}
```

### List Entries

```http
GET /entries?entity_id=usr_abc123&limit=50&offset=0
```

**Response:**
```json
{
  "success": true,
  "data": {
    "entries": [...],
    "total": 156,
    "limit": 50,
    "offset": 0
  }
}
```

### Verify Chain

```http
POST /verify
```

**Request:**
```json
{
  "from_sequence": 42000,
  "to_sequence": 42069
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "verified": true,
    "entries_checked": 70,
    "chain_head": "ps-sha256:xyz789..."
  }
}
```

---

## Stripe Integration

### Webhook Events

| Stripe Event | RoadChain Action |
|--------------|------------------|
| `checkout.session.completed` | `credit_grant` for subscription/purchase |
| `invoice.paid` | `credit_grant` for recurring subscription |
| `invoice.payment_failed` | No entry (flag for retry) |
| `customer.subscription.deleted` | No entry (stop future grants) |
| `transfer.created` | `payout` for creator withdrawal |

### Webhook Handler

```python
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Map Stripe amount to RoadCoin
        amount_cents = session["amount_total"]
        roadcoin_amount = amount_cents  # $1 = 100 RC, so cents = RC
        
        # Create RoadChain entry
        await create_entry({
            "entry_type": "credit_grant",
            "to_entity_type": "user",
            "to_entity_id": session["client_reference_id"],  # Our user ID
            "amount": roadcoin_amount,
            "currency": "ROADCOIN",
            "stripe_payment_intent_id": session["payment_intent"],
            "metadata": {
                "source": "stripe_checkout",
                "product": session["metadata"].get("product"),
            },
            "idempotency_key": f"stripe_{session['id']}",
        })
    
    return {"received": True}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| `RC001` | Insufficient balance |
| `RC002` | Invalid entry type |
| `RC003` | Entity not found |
| `RC004` | Hash verification failed |
| `RC005` | Rate limit exceeded |
| `RC006` | Invalid currency |
| `RC007` | Transfer to self |
| `RC008` | Negative amount |
| `RC009` | Duplicate idempotency key |
| `RC010` | Unauthorized |
| `RC011` | Chain integrity violation |
| `RC012` | System account restricted |

---

## Implementation Roadmap

### Phase 1: Core Ledger (v0.1) — January 2025
- [x] Database schema
- [ ] Entry creation API
- [ ] Balance tracking
- [ ] Hash chain implementation
- [ ] Stripe webhook integration

### Phase 2: SDK & Integrations (v0.2) — February 2025
- [ ] TypeScript SDK
- [ ] Python SDK
- [ ] Agent usage tracking
- [ ] Pack purchase flow
- [ ] Creator payouts

### Phase 3: Audit & Export (v0.3) — March 2025
- [ ] Admin dashboard
- [ ] Export API
- [ ] R2 archival
- [ ] Chain verification tools
- [ ] Audit log UI

### Phase 4: Advanced Features (v1.0) — April 2025
- [ ] Multi-currency support
- [ ] Scheduled transfers
- [ ] Spending limits
- [ ] Dispute resolution
- [ ] Public explorer (read-only)
