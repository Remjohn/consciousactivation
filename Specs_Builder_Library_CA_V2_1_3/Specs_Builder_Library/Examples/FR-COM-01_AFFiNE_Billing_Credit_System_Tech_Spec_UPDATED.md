# PRE-WORK LOG

1. **Existing Spec:** Read `docs/architecture/FR-COM-01_AFFiNE_Billing_Credit_System_Tech_Spec.md`.
2. **Master Protocol:** Read `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` to adhere to Era 3 standards.
3. **Source PRD Module:** Read `PRD-09_CPSC_Silent_Referral.md` — confirmed transition from legacy weekly billing and CBCS credits to the new monthly 4-tier model ($0, $39.99, $99.99, $199.99) plus $9.99 à la carte video fees, eliminating free trials.
4. **PROOF (Specific Section Quoted):** Section 2 Overview of the existing spec states: *"The CCP operates a multi-tenant SaaS where coaches pay a recurring weekly subscription ($25 or $50) plus metered per-client CBCS credits ($4/user)."*

---

# Tech-Spec: FR-COM-01 — AFFiNE Billing & Credit System (UPDATED)

**Created:** 2026-03-30
**Updated:** 2026-05-11
**Status:** Ready for Development
**Version:** 2.0 (Era 3 4-Tier Model Update)
**Architecture Reference:** ADR-01 (Coach Isolation), SPEC-INFRA-001 §5 (Redis)
**Skill Implementation:** `CBCS/backend/billing/billing_middleware.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

- `docs/other files/active lab archive/temporary lab/affine_billing_architecture.md` — Stripe metered billing, Redis state, jail system
- `docs/other files/active lab archive/temporary lab/pricing_strategy_analysis.md` — Pricing tiers, CBCS credits
- `docs/architecture/Infrastructure_AWS_NIM_Deployment_Spec.md` — §5 Redis, §8 Cost thresholds
- `CBCS/backend/database/migrations/003_full_schema.sql` — Existing `payments` table
- `docs/prd/modules/PRD_09_CPSC_Silent_Referral.md` — Canonical 4-Tier Pricing Model

---

## 2. Overview

### Problem Statement
<!-- UPDATED: Replaced legacy weekly $25/$50 and metered CBCS references with the 4-tier monthly model and offer_tier_governor integration -->
The CCP operates a multi-tenant SaaS where coaches are assigned to a 4-tier monthly progression: $0 (Proof Layer), $39.99/mo (Speaking & Learning Tier 1), $99.99/mo (Coach OS Tier 2), and $199.99/mo (Elite Tier 3). Currently, the `payments` table in migration 003 records transactions but has no middleware enforcement — a coach can request à la carte videos ($9.99 each) or consume GPU resources without a valid payment method. There is no mechanism to block pipeline execution when a subscription lapses, no automated usage reporting to Stripe, no `offer_tier_governor` integration to validate tier ceilings, and no Redis-cached permission state to avoid querying Stripe on every action. The billing architecture exists only as a prose artifact with no database schema, no API contracts, and no integration with the existing pipeline.

### Solution
<!-- UPDATED: Removed legacy "free trial" reference, replaced with $0 Proof Layer -->
FR-COM-01 implements the **Billing Middleware** — a "coin-operated" enforcement layer that sits between every billable coach action and the backend. Every action (request video, deploy CBCS bot) passes through `requireCredits()` middleware that checks the coach's cached permission state in Redis, validates the action against the `offer_tier_governor` ceiling, reports usage to Stripe, and blocks execution if the subscription is inactive or the tier ceiling is exceeded. Stripe webhooks update Redis in real-time. A "jail" system prevents abuse (instant usage locking, grace period muting, watermarking for the $0 Proof Layer).

### Scope
**In scope:**
<!-- UPDATED: Replaced weekly cycle with monthly cycle, removed legacy active_clients cache -->
- Stripe Subscriptions with Metered Billing (monthly cycle for à la carte videos)
- Redis permission state cache (`coach:{uuid}:status`, `coach:{uuid}:tier`)
- Billing Middleware (`requireCredits()`) validating against `offer_tier_governor` for all billable endpoints
- Stripe Webhook listener (payment success/failure → Redis update)
- AFFiNE Wallet/Billing Block (dashboard showing current cost)
- Abuse prevention ("jail" system: instant usage lock, muting, watermarking)
- Grace period behavior (read-only mode on payment failure)

**Out of scope:**
- Client-side payment collection (coaches handle their own client billing — Model A)
- Stripe Connect (Model B, future premium feature)
- Pricing tier configuration (business decision, not tech spec — see pricing_strategy_analysis.md)
- GPU cost monitoring (FR-INFRA, handled by CloudWatch kill switch)

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role |
|---|---|---|
| `DEP-COM-001` | Billing Middleware | OUTPUT — `requireCredits()` function wrapping all billable endpoints. |
| `DEP-COM-002` | Stripe Webhook Handler | OUTPUT — Lambda/endpoint consuming Stripe events. |
| `DEP-COM-003` | Redis Permission State | STATE — Cached coach billing status. |
| `DEP-COM-004` | AFFiNE Wallet Block | OUTPUT — Coach-facing billing dashboard. |
<!-- UPDATED: Added DEP-COM-005 to reflect the Offer Tier Governor integration mandate -->
| `DEP-COM-005` | Offer Tier Governor | CORE — Validates tier capabilities (e.g., video quotas). |
| `DEP-ENG-041` | Receipt Chain Guard | AUDIT — Billing events hashed into receipt chain. |
| `SPEC-INFRA-001` §5 | Redis (ElastiCache) | INFRASTRUCTURE — Permission state cache. |

### Existing Backend Integration
This spec extends the following existing architecture:
- **API Routes:** Integrates new webhook endpoints into `src/ccp/api/main.py`.
- **Database:** Extends Supabase schemas via `src/ccp/scripts/setup_supabase.py` (`coach_subscriptions` and `billing_events`).
- **Services:** Extends tier integrations using `src/ccp/services/offer_tier_governor.py`.
- **Audit Logging:** Emits immutable logs to `src/ccp/core/receipt_chain.py`.

### ADR-05 Primitives
- **`EXP-FRC-002: Friction-Zero Ability`:** Governs the $0 Proof Layer access to eliminate entry friction before monetization.

### CBAR Mandate Enforcement
- **Phase 1 M-07 (The Payment Masking Rule):** Enforced in Stage 3 (Stripe Webhook Handler). The `invoice.payment_succeeded` webhook must instantly trigger the Telegram experiential reward to mask Coach OS backend provisioning.

### Technical Decisions

1. **Redis-First, Not Stripe-First:** Every billing check reads from Redis, never from Stripe directly. Stripe is the source of truth, but Redis is the enforcement cache. Webhook reconciliation keeps them in sync. This eliminates Stripe API latency from the critical path.
<!-- UPDATED: Removed $4 CBCS charge, updated to $9.99 à la carte video generation lock -->
2. **Instant Usage Lock:** The $9.99 à la carte video charge is locked the moment the rendering pipeline successfully initiates, preventing "cancel-before-delivery" exploits for metered tier usage.
3. **Muting, Not Deletion:** When payment fails, client data is preserved but all bots are muted (stop sending messages) and the AFFiNE workspace enters read-only mode. Data is never deleted due to billing issues.
<!-- UPDATED: Changed from weekly base+CBCS to monthly 4-tier model -->
4. **Monthly Billing Cycle:** Aligned with the PRD-09 pricing strategy. Stripe calculates: Monthly Subscription Tier ($39.99/$99.99/$199.99) + (à la carte videos × $9.99) at the end of each month.
5. **Tier Governor Integration:** The `offer_tier_governor.py` is the absolute authority on tier ceilings. The billing middleware MUST query the governor to resolve access limits (e.g., locking access when a Coach OS user requests a 13th video without approving the $9.99 upcharge).

---

## 4. Implementation Plan

### Stage 1: Stripe Product Setup
*Outputs:* Stripe Product IDs, Price IDs

<!-- UPDATED: Replaced weekly $25/$50 and metered $4 prices with PRD-09 monthly 4-tier + $9.99 metered pricing -->
| Stripe Object | ID Pattern | Configuration |
|---|---|---|
| Product: Tier 1 | `prod_ccp_speaking_learning` | Speaking & Learning Tier |
| Price: $39.99/mo | `price_ccp_tier1_3999` | Recurring, monthly interval |
| Product: Tier 2 | `prod_ccp_coach_os` | Coach OS Tier |
| Price: $99.99/mo | `price_ccp_tier2_9999` | Recurring, monthly interval |
| Product: Tier 3 | `prod_ccp_elite` | Elite / Operator Tier |
| Price: $199.99/mo | `price_ccp_tier3_19999` | Recurring, monthly interval |
| Product: À La Carte Video | `prod_ccp_alacarte_video` | Metered billing |
| Price: $9.99/video | `price_ccp_video_999` | Metered, sum usage, monthly |

### Stage 2: Billing Middleware
*Inputs:* Coach UUID, action type
*Outputs:* ALLOW or BLOCK

```python
<!-- UPDATED: Added integration with offer_tier_governor.py to validate tier ceilings -->
async def require_credits(coach_id: UUID, action: str, cost: int = 0):
    """
    Middleware gate for all billable actions.
    1. Check Redis for coach permission state.
    2. Consult offer_tier_governor.py for tier ceilings.
    3. If active & within tier → report usage to Stripe if metered → allow action.
    4. If inactive or out of bounds → block action → return billing error.
    """
    status = await redis.get(f"coach:{coach_id}:status")
    
    if status != "active" and status != "proof_layer":
        raise BillingError(
            code="SUBSCRIPTION_INACTIVE",
            message="Payment method required. Update card in Wallet.",
            redirect="/wallet"
        )
        
    # Consult Offer Tier Governor for ceiling validation
    tier_resolution, ceiling = offer_tier_governor.resolve(coach_id)
    if ceiling.is_exceeded_by(action):
        raise BillingError(
            code="TIER_CEILING_EXCEEDED",
            message="Action exceeds current tier limits. Upgrade required.",
            redirect="/wallet/upgrade"
        )
    
    if cost > 0:
        await stripe.usage_records.create(
            subscription_item=await get_metered_item(coach_id),
            quantity=cost,
            action="increment"
        )
        
        # Write to PostgreSQL billing_events
        await db.execute(
            "INSERT INTO billing_events (coach_id, event_type, amount_cents, description) VALUES ($1, $2, $3, $4)",
            coach_id, "alacarte_video", cost * 999, f"Rendered video for action {action}"
        )
    
    # Write Receipt Chain Guard
    await receipt_chain.write({
        "stage": "BILLING_GATE",
        "agent": "billing_middleware",
        "coach_id": str(coach_id),
        "action": action,
        "cost": cost,
        "status": "ALLOWED"
    })
    
    return True
```

### Stage 3: Stripe Webhook Handler
*Inputs:* Stripe webhook events
*Outputs:* Redis state updates, PostgreSQL inserts, Receipt Chain writes, and Provisioning Triggers

| Stripe Event | Backend Actions |
|---|---|
| `invoice.payment_succeeded` | 1. `SET coach:{uuid}:status active`<br>2. `INSERT INTO billing_events (event_type: 'subscription_payment')`<br>3. `receipt_chain.write(stage='BILLING_WEBHOOK', status='SUCCESS')`<br>4. Trigger Telegram experiential reward & background Coach OS provisioning (Enforces Phase 1 M-07 Payment Masking Rule) |
| `invoice.payment_failed` | 1. `SET coach:{uuid}:status past_due`<br>2. `INSERT INTO billing_events (event_type: 'payment_failed')`<br>3. `receipt_chain.write(stage='BILLING_WEBHOOK', status='FAILED')` |
| `customer.subscription.deleted` | 1. `SET coach:{uuid}:status cancelled`<br>2. `receipt_chain.write(stage='BILLING_WEBHOOK', status='CANCELLED')` |
| `customer.subscription.updated` | Update tier in `coach:{uuid}:tier` |

### Stage 4: AFFiNE Wallet Block
*Outputs:* Coach-facing billing dashboard

<!-- UPDATED: Replaced weekly breakdown with monthly subscription + à la carte videos -->
- Current monthly cost breakdown: Subscription Tier + À La Carte Videos (N × $9.99) = Total
- Payment status indicator (green/amber/red)
- "Update Card" button → Stripe Elements modal (embedded, never leaves AFFiNE)
- Usage history (last 4 weeks)
- Alert banner on payment failure: "Billing failed. Client bots are paused. [Update Card]"

### Stage 5: Jail System (Abuse Prevention)
*Outputs:* Anti-abuse enforcement rules

<!-- UPDATED: Replaced CBCS client triggers with Video Generation triggers and removed "Free Trial" reference -->
| Rule | Trigger | Action |
|---|---|---|
| **Instant Usage Lock** | Rendering pipeline initiated for à la carte video | Report +1 usage to Stripe immediately. $9.99 locked for this billing cycle. |
| **Grace Period Mute** | `invoice.payment_failed` webhook | Bots stop sending messages. AFFiNE → read-only. Data preserved. |
| **Watermark Enforcement** | $0 Proof Layer active | The `require_credits` middleware injects a `requires_watermark: true` flag into the `CCFRoutingRecommendation` payload, enforcing the CCP watermark directly in the CMF Arc-Governed Rendering pipeline. Removed upon upgrade to Speaking & Learning ($39.99) or higher. |
| **Re-activation** | `invoice.payment_succeeded` after `past_due` | Bots resume. AFFiNE → full access. Watermarks removed. |

---

## 5. Data Model

### Table: `coach_subscriptions`

```sql
<!-- UPDATED: Updated schema to reflect monthly PRD-09 pricing tiers and removed legacy fields -->
CREATE TABLE IF NOT EXISTS coach_subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL UNIQUE,
    stripe_customer_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_subscription_id VARCHAR(50) NOT NULL UNIQUE,
    stripe_metered_item_id VARCHAR(50),
    tier VARCHAR(30) NOT NULL DEFAULT 'proof_layer' CHECK (tier IN ('proof_layer', 'speaking_learning', 'coach_os', 'elite')),
    monthly_base_price_cents INTEGER NOT NULL DEFAULT 0,
    alacarte_video_price_cents INTEGER NOT NULL DEFAULT 999,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN (
        'active', 'past_due', 'cancelled', 'paused'
    )),
    payment_method_last4 VARCHAR(4),
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    total_monthly_cost_cents INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sub_coach ON coach_subscriptions(coach_id);
CREATE INDEX idx_sub_status ON coach_subscriptions(status);

ALTER TABLE coach_subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own subscription"
    ON coach_subscriptions FOR SELECT
    USING (auth.uid() = coach_id);
```

### Table: `billing_events`

```sql
CREATE TABLE IF NOT EXISTS billing_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    coach_id UUID NOT NULL,
<!-- UPDATED: Removed 'cbcs_credit' from event types -->
    event_type VARCHAR(50) NOT NULL,                -- 'alacarte_video', 'subscription_payment', 'payment_failed'
    stripe_event_id VARCHAR(100) UNIQUE,
    amount_cents INTEGER,
    description TEXT,
    receipt_chain_block VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_billing_coach ON billing_events(coach_id);
CREATE INDEX idx_billing_type ON billing_events(event_type);

ALTER TABLE billing_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Coach sees own billing events"
    ON billing_events FOR SELECT
    USING (auth.uid() = coach_id);
```

---

## 6. Backward Compatibility

The existing `payments` table (migration 003) is a legacy MVP table. It remains for historical records. New billing events flow through `billing_events` + `coach_subscriptions`. A one-time migration script maps any existing `payments.user_id` entries to `coach_subscriptions.coach_id`.

---

## 7. Tasks

<!-- UPDATED: Updated tasks to reflect monthly 4-tier setup and offer_tier_governor integration -->
- [ ] **Task 1:** Create Stripe Products and Prices (Proof $0, Speaking & Learning $39.99, Coach OS $99.99, Elite $199.99, metered video $9.99).
- [ ] **Task 2:** Implement `billing_middleware.py` with `require_credits()` function, integrating with `offer_tier_governor.py`.
- [ ] **Task 3:** Build Stripe webhook handler (4 event types → Redis state updates).
- [ ] **Task 4:** Implement Redis permission state schema (`coach:{uuid}:status`, `coach:{uuid}:tier`).
- [ ] **Task 5:** Build AFFiNE Wallet Block (cost breakdown, payment status, Stripe Elements modal).
- [ ] **Task 6:** Implement Jail System (instant usage lock, grace period mute, watermark enforcement for Proof Layer).
- [ ] **Task 7:** Build payment failure → bot muting integration (webhook → Redis → Telegram bot pause).
- [ ] **Task 8:** Register DEP-COM-001 through DEP-COM-005 in the dependency registry.

---

## 8. Acceptance Criteria

<!-- UPDATED: Replaced legacy AC scenarios with PRD-09 compliant scenarios using the 4-tier pricing model -->
- [ ] **AC1 (Happy Path):** Coach on Coach OS Tier ($99.99) generates a 13th video. Assert: `offer_tier_governor` approves metered overage, Redis status is `active`, Stripe usage record created (+1 at $9.99), video rendered successfully.
- [ ] **AC2 (Payment Block):** Coach with `past_due` status attempts to trigger a video render. Assert: `require_credits()` blocks the action. Error returned: `SUBSCRIPTION_INACTIVE`. Render aborted.
- [ ] **AC3 (Instant Usage Lock):** Coach initiates à la carte video render. Assert: Stripe usage record created immediately as pipeline starts. Coach aborts render manually midway. Assert: $9.99 charge still applies for this cycle.
- [ ] **AC4 (Grace Period Mute):** `invoice.payment_failed` fires. Assert: Redis status → `past_due`. All coach's Telegram bots stop sending. AFFiNE workspace → read-only. Client data preserved (not deleted).
- [ ] **AC5 (Re-activation):** Coach updates card → payment succeeds. Assert: Redis status → `active`. Bots resume sending. AFFiNE → full access.
- [ ] **AC6 (Wallet Display):** Coach on Speaking & Learning Tier ($39.99/mo) generates 2 à la carte videos. Assert: Wallet shows "$59.97/mo ($39.99 base + 2 × $9.99 videos)".

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| DEP-COM-001 (Billing Middleware) | Output | `require_credits()` wrapping all billable endpoints. |
| DEP-COM-002 (Webhook Handler) | Output | Stripe → Redis state sync. |
| DEP-COM-003 (Redis Permission State) | State | Cached billing status per coach. |
| DEP-COM-004 (AFFiNE Wallet Block) | Output | Coach-facing billing UI. |
<!-- UPDATED: Added Offer Tier Governor dependency -->
| DEP-COM-005 (Offer Tier Governor) | Core | Authoritative resolution of tier capabilities and ceilings. |
| SPEC-INFRA-001 §5 (Redis) | Infrastructure | ElastiCache for permission cache. |
| Stripe API | External | Subscriptions, Metered Billing, Webhooks, Elements. |
| FR-COM-03 (Telegram Onboarding) | Downstream | Onboarding triggers CBCS usage report. |
| FR-COM-04 (Campaign Manager) | Downstream | Program creation requires active subscription. |

---

## 10. Testing Strategy

### Unit Tests
- **Middleware Gate:** Mock Redis with `status: active` → assert allow. Mock Redis with `status: past_due` → assert block.
- **Usage Reporting:** Mock Stripe API. Assert `require_credits(cost=1)` calls `usage_records.create` with `quantity=1`.
<!-- UPDATED: Added Tier Ceiling test case -->
- **Tier Ceilings:** Mock `offer_tier_governor` returning `is_exceeded_by = True`. Assert `require_credits()` raises `BillingError(code="TIER_CEILING_EXCEEDED")`.

### Integration Tests
- **Full Billing Flow:** Create Stripe test subscription → add client → trigger bot → verify usage record → trigger `invoice.payment_succeeded` webhook → verify Redis state.
- **Failure Recovery:** Trigger `invoice.payment_failed` → verify bot muting → update card → trigger `invoice.payment_succeeded` → verify bot resumption.

### Safety Tests
- **Webhook Replay:** Send the same Stripe webhook event twice. Assert idempotent handling (no double charge, no duplicate Redis update).
- **Redis Failure:** Kill Redis connection. Assert middleware falls back to Stripe API direct query (degraded but functional).
