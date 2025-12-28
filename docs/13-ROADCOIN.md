# 13 — RoadCoin Economics

**Version:** 1.0.0  
**Last Updated:** December 28, 2024  
**Domain:** roadcoin.io

---

## Overview

RoadCoin (RC) is the internal credit unit powering the BlackRoad OS economy. It is **not a cryptocurrency** — it's a platform credit with fixed exchange rates to fiat currency.

---

## Token Properties

| Property | Value |
|----------|-------|
| **Name** | RoadCoin |
| **Symbol** | RC |
| **Decimals** | 8 |
| **Type** | Internal credit (not cryptocurrency) |
| **Convertibility** | Fiat via Stripe (platform rate) |
| **Transferability** | Between platform entities only |

---

## Exchange Rates

### Fiat → RoadCoin (Purchase)

```
$1.00 USD = 100 RoadCoin
```

Users purchase RoadCoin through Stripe subscriptions or one-time payments. The rate is fixed and transparent.

### RoadCoin → Fiat (Payout)

```
100 RoadCoin = $0.90 USD (10% platform fee)
```

Creators can withdraw earnings to their bank account via Stripe Connect. The 10% fee covers payment processing and platform operations.

### Exchange Rate Table

| Direction | Rate | Fee |
|-----------|------|-----|
| USD → RC | 1:100 | 0% |
| RC → USD | 100:0.90 | 10% |
| EUR → RC | 1:108 | 0% |
| GBP → RC | 1:127 | 0% |

---

## Subscription Allocations

### Current Stripe Products

| Plan | Price | Monthly RoadCoin | Effective Rate |
|------|-------|------------------|----------------|
| **Free** | $0 | 100 RC | N/A |
| **Individual** | $29/mo | 2,900 RC | $1 = 100 RC |
| **Pro** | $58/mo | 5,800 RC | $1 = 100 RC |
| **Pro (Founding 50%)** | $29/mo | 5,800 RC | $1 = 200 RC |
| **Team** | $99/mo | 9,900 RC | $1 = 100 RC |
| **Enterprise** | $199/mo | 19,900 RC | $1 = 100 RC |
| **Founding Lifetime** | $5,000 | 500,000 RC | One-time |

### Founding Member Benefits

Founding Members ($5,000 lifetime) receive:
- 500,000 RC initial grant
- 5,000 RC/month ongoing allocation
- All future products free
- Exclusive community access
- Name in credits
- Direct line to founders

---

## Resource Pricing

### AI Model Tokens

| Model | Cost per 1K Input Tokens | Cost per 1K Output Tokens |
|-------|--------------------------|---------------------------|
| **GPT-4o** | 0.25 RC | 1.00 RC |
| **GPT-4o-mini** | 0.015 RC | 0.06 RC |
| **GPT-4-turbo** | 1.00 RC | 3.00 RC |
| **o1** | 1.50 RC | 6.00 RC |
| **o1-mini** | 0.30 RC | 1.20 RC |
| **Claude 3.5 Sonnet** | 0.30 RC | 1.50 RC |
| **Claude 3.5 Haiku** | 0.025 RC | 0.125 RC |
| **Claude 3 Opus** | 1.50 RC | 7.50 RC |
| **Gemini 1.5 Pro** | 0.125 RC | 0.50 RC |
| **Gemini 1.5 Flash** | 0.0075 RC | 0.03 RC |

*Note: These are our costs marked up ~20% from provider rates.*

### BYO-Key Discount

When users provide their own API keys:
- **No token charges** — they pay providers directly
- **Platform fee only** — 5 RC per 1K tokens (audit/routing)
- **Full credit allocation** — use RC for other features

### Storage

| Resource | Cost |
|----------|------|
| R2 storage | 1 RC per GB/month |
| Embedding storage | 0.5 RC per 1K vectors/month |
| Model artifact storage | 2 RC per GB/month |

### Compute

| Resource | Cost |
|----------|------|
| Training job (LoRA, 7B) | 500 RC per hour |
| Training job (LoRA, 70B) | 2,000 RC per hour |
| Inference endpoint (7B) | 100 RC per hour |
| Inference endpoint (70B) | 400 RC per hour |

### API Access

| Resource | Cost |
|----------|------|
| API call (base) | 0.1 RC |
| Webhook delivery | 0.05 RC |
| Search query | 0.5 RC |

---

## Creator Economics

### Pack Revenue Share

When a creator sells a pack (agent bundle, prompts, etc.):

```
Sale Price: 500 RC

Distribution:
├── Creator:   350 RC (70%)
├── Platform:  150 RC (30%)
└── Total:     500 RC
```

### Creator Tiers

| Tier | Revenue Share | Requirements |
|------|---------------|--------------|
| **New Creator** | 70% | Default |
| **Verified Creator** | 75% | 100+ sales, verified identity |
| **Partner** | 80% | 1,000+ sales, exclusive content |

### Payout Minimums

| Threshold | Payout Method |
|-----------|---------------|
| 1,000 RC | Standard (3-5 business days) |
| 10,000 RC | Express (1-2 business days) |

---

## Agent Economics

### Agent Compute Costs

Agents consume RoadCoin for:
- Model inference (per token)
- Memory operations (per write)
- Tool executions (per call)

```
Example: Cece processes a complex task

Model inference (Claude Sonnet):
  Input:  2,000 tokens × 0.30 RC/1K = 0.60 RC
  Output: 1,500 tokens × 1.50 RC/1K = 2.25 RC
  
Memory commit:
  1 journal entry = 0.1 RC
  
Tool calls:
  2 × web_search = 1.0 RC
  
Total: 3.95 RC
```

### Agent Rewards

Agents can earn RoadCoin through:

| Activity | Reward |
|----------|--------|
| Task completion (user-rated 5★) | 1-10 RC |
| Helpful response (thumbs up) | 0.5 RC |
| Pack contribution (if included) | Revenue share |
| Referral (user signs up via agent link) | 100 RC |

### Agent Spending Limits

| Entity Type | Default Daily Limit |
|-------------|---------------------|
| Free user | 100 RC |
| Pro user | 5,000 RC |
| Team user | 10,000 RC |
| Agent (system) | 1,000 RC |
| Agent (user-created) | User's limit |

---

## Economic Flows

### Subscription Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     SUBSCRIPTION CYCLE                           │
└──────────────────────────────────────────────────────────────────┘

Day 1: User subscribes to Pro ($58/mo)
       ├── Stripe charges $58
       └── RoadChain: credit_grant +5,800 RC to user

Day 1-30: User consumes services
          ├── Model tokens: -2,500 RC
          ├── Storage: -50 RC
          └── API calls: -200 RC
          
Day 30: Balance: 3,050 RC remaining
        └── Unused credits DO NOT roll over

Day 31: New billing cycle
        ├── Stripe charges $58
        ├── RoadChain: credit_grant +5,800 RC
        └── New balance: 5,800 RC (fresh allocation)
```

### Creator Payout Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     CREATOR PAYOUT                               │
└──────────────────────────────────────────────────────────────────┘

Creator accumulates 15,000 RC from pack sales

Creator requests payout:
├── RoadChain: credit_burn -15,000 RC from creator
├── Platform fee: 10% = 1,500 RC
├── Net payout: 13,500 RC = $135 USD
└── Stripe: transfer $135 to creator's bank

Timeline: 3-5 business days to bank account
```

### Pack Purchase Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     PACK PURCHASE                                │
└──────────────────────────────────────────────────────────────────┘

Buyer purchases "Finance Pack" for 1,000 RC

RoadChain entries:
1. transfer: -1,000 RC from buyer
2. reward:   +700 RC to creator (70%)
3. transfer: +300 RC to system:fees (30%)

Buyer: -1,000 RC, gains pack access
Creator: +700 RC, available for payout
Platform: +300 RC, operational revenue
```

---

## Anti-Abuse Measures

### Rate Limiting

| Action | Limit |
|--------|-------|
| Entries per minute | 100 |
| Transfers per hour | 50 |
| Payouts per day | 3 |

### Fraud Detection

| Signal | Action |
|--------|--------|
| Unusual transfer pattern | Flag for review |
| Rapid credit burn | Throttle + alert |
| Multiple failed payouts | Suspend payouts |
| New account high activity | Enhanced verification |

### Clawback Policy

RoadCoin credits may be clawed back in cases of:
- Payment reversal (chargeback)
- Fraud detection
- Terms of service violation
- System error correction

All clawbacks are recorded as `adjustment` entries with full audit trail.

---

## Reporting

### User Dashboard

Users see:
- Current balance
- Monthly allocation used/remaining
- Transaction history
- Spending by category (models, storage, etc.)

### Creator Dashboard

Creators see:
- Lifetime earnings
- Pending balance
- Payout history
- Sales by pack
- Revenue share tier

### Admin Dashboard

Platform admins see:
- Total RoadCoin in circulation
- Daily mint/burn rates
- Revenue by category
- Fraud alerts
- Chain verification status

---

## Future Considerations

### Not Planned (By Design)

| Feature | Reason |
|---------|--------|
| **Trading** | RC is utility credit, not speculative asset |
| **External wallets** | Platform-only to maintain control |
| **Interest/yield** | Not a financial instrument |
| **Tokenization** | Regulatory complexity, no user value |

### Maybe Later

| Feature | Condition |
|---------|-----------|
| **Multi-currency display** | When international demand justifies |
| **Credit rollover** | If user retention requires |
| **Tiered pricing** | If usage patterns diverge significantly |
| **Bulk discounts** | For enterprise contracts |

---

## Glossary

| Term | Definition |
|------|------------|
| **RC** | RoadCoin, the internal credit unit |
| **Grant** | Credits added to balance |
| **Burn** | Credits consumed (removed from circulation) |
| **Transfer** | Credits moved between entities |
| **Payout** | RC converted to fiat and withdrawn |
| **Allocation** | Monthly credits included with subscription |
| **Rollover** | Unused credits carried to next period (not currently supported) |
