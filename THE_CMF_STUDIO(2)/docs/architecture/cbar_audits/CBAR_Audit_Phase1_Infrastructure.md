# CBAR Audit Manifest: Phase 1 Infrastructure Epics

**Author:** CBAR Epic & Story Hardening SKILL
**Date:** 2026-05-10
**Target Epic:** `Phase1_Infrastructure_Epics.md`
**Status:** Audit Complete

## Pre-Audit Load Summary

- **Primitives Audited:** `EXP-FRC-002`, `EXP-FRC-003`, `EXP-FBK-001`, `EXP-PER-003`
  - *Note: `EXP-TRB-004` (Attractive Things Work Better) was referenced in the drafted Epic, but does not exist in the primitive registry. This indicates a hallucination in the BMAD pipeline. Flagged as UNCODIFIED.*
- **PRD Modules Loaded:** `PRD_01_CCP_Platform_Strategy.md`
- **Tech Specs Loaded:** NONE — `FR-ERA3-08_Mini_App_Separation_Architecture_Tech_Spec.md` does not exist in the Era 3 `april_updates` directory. Assumed to be unwritten.
- **Protocol Evaluated:** `ERA3_Epic_and_Story_Writing_Protocol.md` (Lacks adversarial review gate)

---

## Epic 1: The Mini App Host Shell (FR-ERA3-08)

### 1.1 Story: Secure Web App Initialization
**Mapped Primitive:** `EXP-FRC-002` (System 1 to System 2 Escalation)

**Part 1 — The Tension:**
The PRD-01 architecture requires robust validation of the `initData` hash against the bot token to establish secure session state, which introduces mandatory network and database latency. `EXP-FRC-002` explicitly mandates "Intuitive On-Ramping" where entry points operate entirely in System 1 (zero-effort, emotional engagement) without waiting for backend processing.

**Part 2 — The UX Failure Scenario:**
The React app blocks the initial render for ~1 second while the FastAPI backend checks the hash against PostgreSQL/Redis. This delay destroys the System 1 momentum. The user experiences an immediate spike in cognitive friction (homework fatigue) and abandons the Mini App before even seeing the first prompt.

**Part 3 — The Resolution Demand:**
System 1 Escalation (`EXP-FRC-002`) takes absolute precedence over synchronous validation blocking. The rule of "Emotional, intuitive reaction first" (from `why_it_works`) demands that the UI must optimistically render the first experiential screen instantly. Asynchronous validation of the `initData` hash occurs in the background. *(UNVERIFIED ASSUMPTION: The future Tech Spec must explicitly support optimistic rendering capabilities.)*

**Part 4 — The Downstream Proof:**
Story 1.2 inherits this constraint. Because Story 1.1 demands optimistic rendering, Story 1.2 cannot block rendering to fetch brand palettes over the network.

**Verdict: REWRITE REQUIRED**
**CBAR-Hardened Acceptance Criteria:**
*   Given I tap a Web App button in Telegram,
*   When the shell loads,
*   Then it renders the System 1 UI optimistically without blocking for network responses,
*   And it validates the `initData` hash against the bot token asynchronously in the background.

---

### 1.2 Story: Global DPA Theme Resolution
**Mapped Primitive:** `EXP-TRB-004` *(UNCODIFIED HALLUCINATION)*

**Part 1 — The Tension:**
The drafted story states "it requests context from the backend" and "it blocks rendering until the ResolvedPalette is ready." This introduces a mandatory network round-trip. This directly conflicts with Story 1.1's resolution which mandates optimistic, instant rendering to satisfy `EXP-FRC-002`.

**Part 2 — The UX Failure Scenario:**
The app blocks rendering waiting for `ResolvedPalette`. The user stares at a blank screen. The aesthetic trust standard has actively killed the friction ability standard. The user bounces.

**Part 3 — The Resolution Demand:**
Instant rendering (Story 1.1 / `FRC-002`) takes absolute precedence over network-fetched aesthetics. The architecture must inject the `ResolvedPalette` CSS variables directly into the Telegram `startapp` URL parameter, allowing the Mini App to decode the theme locally with zero network calls upon initialization.

**Part 4 — The Downstream Proof:**
Story 1.3 inherits this zero-network initialization constraint. Routing must also rely entirely on URL parameters, not backend context state.

**Verdict: FATAL CONFLICT (Rewrite Required)**
**CBAR-Hardened Acceptance Criteria:**
*   Given the shell is initialized via a Telegram button tap,
*   When it determines the visual theme,
*   Then it decodes the `ResolvedPalette` directly from the injected `startapp` URL parameter,
*   And it applies the global CSS variables instantly with zero backend network requests.

---

### 1.3 Story: Dynamic Surface Routing
**Mapped Primitive:** `EXP-FRC-003` (The B=MAP Friction Audit)

**Part 1 — The Tension:**
The story uses React Router to deep-link directly to a specific module based on `startapp` parameters to satisfy `EXP-FRC-003` (max 0 clicks from launch). However, if the module requires hardware access (microphone/camera), the OS-level permission dialogue will block the deep-link immediately, conflicting with the "zero physical effort" mandate.

**Part 2 — The UX Failure Scenario:**
The user taps the Telegram button and is immediately hit with a cold OS "Please allow microphone" prompt before any context is established. Their Fogg Ability plummets, and the transaction is abandoned because motivation is not high enough to overcome the sudden OS friction.

**Part 3 — The Resolution Demand:**
`EXP-FRC-003` dictates removing physical/mental effort. Hitting a cold OS prompt is high effort. The routing must resolve this by dropping un-permissioned users into a high-emotion System 1 'primer' screen that justifies the request *before* triggering the OS blocker.

**Part 4 — The Downstream Proof:**
This resolves the routing edge case without introducing downstream constraints for the backend registry.

**Verdict: REWRITE REQUIRED**
**CBAR-Hardened Acceptance Criteria:**
*   Given a Telegram button contains a `startapp` parameter,
*   When the React Router deep-links to that specific module,
*   Then it checks hardware permissions before rendering the active tool,
*   And if permissions are unset, it routes to an emotional primer screen instead of firing a cold OS prompt.

---

## Epic 2: The Primitive Registry Query Service (FR-ERA3-06)

### 2.1 Story: Registry Parsing & Caching
**Mapped Primitive:** `EXP-FBK-001` (RIM Feedback Discipline)

**Part 1 — The Tension:**
`EXP-FBK-001` mandates Immediate feedback (max 3-second latency for audio processing). Loading all YAML primitives into Redis on `lifespan` initialization protects this latency. However, if a primitive is updated dynamically, the Redis cache becomes stale, causing the system to serve incorrect rules.

**Part 2 — The UX Failure Scenario:**
A coach updates their rules. They test a recording. The system uses the stale Redis cache and scores them using old rules. The feedback is Immediate, but it is no longer Relevant or Meaningful (violating RIM). The user loses trust in the scoring engine.

**Part 3 — The Resolution Demand:**
The backend must resolve the tension between in-memory latency protection and real-time relevance. The Acceptance Criteria must enforce a targeted Redis key invalidation event whenever a primitive is updated, forcing the FastAPI worker to hot-reload only that specific YAML block into memory.

**Part 4 — The Downstream Proof:**
Story 2.2 inherits this cache. The resolution query will always hit a fresh but in-memory cache, preserving the 3-second SLA.

**Verdict: REWRITE REQUIRED**
**CBAR-Hardened Acceptance Criteria:**
*   Given the FastAPI application starts or a primitive is updated in the database,
*   When `lifespan` initialization occurs or an invalidation event is received,
*   Then the service caches/hot-reloads the specific YAML primitives into Redis,
*   And serves all queries from memory without disk I/O.

---

### 2.2 Story: Context-Aware Primitive Resolution
**Mapped Primitive:** Orchestration Engine Context

**Part 1 — The Tension:**
The Orchestration Engine uses probabilistic AI (NIM models) to determine which primitives to apply. The Query Service returns deterministic YAML blocks. If the AI requests two primitives that mutually conflict based on their `conflicts_with` YAML fields, the deterministic rules clash.

**Part 2 — The UX Failure Scenario:**
The NIM logic requests an `EXP-SAF-003` (Safe Failure) and an `EXP-PRG-003` (Epic Win). The service returns both. The orchestration engine produces a schizophrenic prompt that demands both high friction and low friction simultaneously, confusing the user and causing a bounce.

**Part 3 — The Resolution Demand:**
Deterministic hierarchy overrides probabilistic AI requests. The Query Service must implement a `Conflict_Resolver` middleware that parses the `conflicts_with` fields of the queried primitives and applies a strict precedence hierarchy before returning the payload.

**Part 4 — The Downstream Proof:**
This ensures all downstream generation systems receive a clean, non-contradictory constraint configuration.

**Verdict: REWRITE REQUIRED**
**CBAR-Hardened Acceptance Criteria:**
*   Given an active Reaction Loop,
*   When the system requests target primitives,
*   Then the service checks the requested set against their respective `conflicts_with` fields,
*   And it applies a `Conflict_Resolver` precedence hierarchy to filter out mutually exclusive rules before returning the JSON payload.

---

## Epic 3: In-Chat Telegram Payments (FR-ERA3-02)

### 3.1 Story: Offer Tier Eligibility Check
**Mapped Primitive:** `EXP-PER-003` (Cumulative Investment)

**Part 1 — The Tension:**
The `offer_tier_governor` uses traditional SaaS billing state to determine eligibility. `EXP-PER-003` dictates that user loyalty is proportional to the data/effort they have deposited (Stored Value). A Free Tier user might have massive stored value, but standard billing logic pitches them a beginner tier.

**Part 2 — The UX Failure Scenario:**
An advanced user with high Stored Value triggers an upgrade intent. The system checks PostgreSQL, sees "Free", and sends a generic beginner pitch. The user feels their investment is unrecognized (loss of Status), is insulted by the pitch, and churns.

**Part 3 — The Resolution Demand:**
`EXP-PER-003` (Stored Value) must take precedence over pure billing state. The `offer_tier_governor` must query both `stripe_status` and `cumulative_assets_stored`. High-investment users on Free tiers must trigger a 'Loyalty Unlock' flow that acknowledges their status.

**Part 4 — The Downstream Proof:**
Story 3.2 inherits this tailored invoice payload, ensuring the Telegram native invoice reflects the advanced status copy.

**Verdict: REWRITE REQUIRED**
**CBAR-Hardened Acceptance Criteria:**
*   Given I trigger an upgrade intent,
*   When the system generates the invoice,
*   Then it queries both `stripe_status` and `cumulative_assets_stored` from the `asset_manager`,
*   And it triggers a tailored 'Loyalty Unlock' offer flow if I have high stored value but low billing status.

---

### 3.2 Story: Native Invoice Generation
**Mapped Primitive:** `EXP-FRC-003` (The B=MAP Friction Audit)

**Part 1 — The Tension:**
Telegram's `sendInvoice` API satisfies `EXP-FRC-003` by enabling zero-effort native payments. However, Stripe SCA (Strong Customer Authentication) often requires 3D Secure verification loops, pulling the user out of Telegram into an external bank webview.

**Part 2 — The UX Failure Scenario:**
The user taps "Pay". Instead of instant success, they hit a bank-branded webview requiring an SMS code they don't have. Ability drops, motivation fails to overcome the friction, and the transaction is abandoned in confusion.

**Part 3 — The Resolution Demand:**
The architecture must reconcile frictionless native payments with asynchronous SCA friction. The Acceptance Criteria must handle `requires_action` Stripe states by deploying a high-status Telegram bot message that keeps the user engaged in System 1 (reassuring copy) while they navigate the 3D secure process, rather than failing silently. *(UNVERIFIED ASSUMPTION: Telegram Bot API allows intercepting `requires_action` callbacks smoothly).*

**Part 4 — The Downstream Proof:**
Story 3.3 inherits this because fulfillment must wait for the asynchronous SCA challenge to clear before executing.

**Verdict: PASS WITH NOTE**
**Note:** Add Acceptance Criteria to explicitly handle the `requires_action` Stripe state with reassuring Telegram bot copy.

---

### 3.3 Story: Post-Payment Fulfillment
**Mapped Primitive:** `EXP-FBK-001` (RIM Feedback Discipline)

**Part 1 — The Tension:**
`EXP-FBK-001` demands immediate feedback the millisecond the webhook clears. However, unlocking Coach OS requires heavy backend provisioning (creating vector namespaces, Voice DNA profile initialization).

**Part 2 — The UX Failure Scenario:**
The webhook fires. The system updates the DB and begins a 45-second provisioning script. During this time, the user taps the Coach OS button in Telegram and gets a "Not ready" error. The 'Instant Reward' standard is broken, replacing excitement with buyer's remorse.

**Part 3 — The Resolution Demand:**
The system must provide an instant reward while masking backend latency. The webhook must immediately trigger a pre-rendered, high-production-value experiential reward (video/audio asset) via the Telegram bot. By the time the user finishes consuming the asset, the background DB provisioning is complete.

**Part 4 — The Downstream Proof:**
This successfully ends the epic cascade with a guaranteed instant-reward loop.

**Verdict: REWRITE REQUIRED**
**CBAR-Hardened Acceptance Criteria:**
*   Given a successful Stripe/Telegram payment,
*   When the `successful_payment` webhook fires,
*   Then my PostgreSQL tenant record is updated and an instant experiential reward (video/audio) is pushed to Telegram,
*   And this asset masks the background execution of the Coach OS provisioning scripts.

---

## Constraint Resolution Manifest

Based on the adversarial simulations executed above, the following structural mandates are permanently appended to the Phase 1 execution plan. Engineering teams must treat these resolutions as canonical.

1. **The Optimistic Render Rule (Story 1.1):** Mini App initialization MUST decouple authentication (`initData`) from visual rendering to satisfy System 1 Escalation.
2. **The Zero-Network Theme Rule (Story 1.2):** `ResolvedPalette` variables must be injected via Telegram URL parameters. Network calls blocking the initial React render are strictly banned.
3. **The Primer Screen Rule (Story 1.3):** Deep-links encountering OS permission blockers must route to a System 1 primer screen, never directly to an OS dialogue box.
4. **The Hot-Reload Rule (Story 2.1):** The `dpa_engine` must implement targeted Redis key invalidation for dynamic YAML updates to preserve 3-second RIM feedback SLAs.
5. **The Deterministic Override Rule (Story 2.2):** The Primitive Registry Query Service must feature a `Conflict_Resolver` middleware. Deterministic precedence overrides probabilistic AI requests.
6. **The Stored Value Rule (Story 3.1):** The offer tier eligibility must combine billing state with cumulative investment assets, preventing generic pitches to high-investment free users.
7. **The Payment Masking Rule (Story 3.3):** Stripe webhook resolution must trigger front-end experiential rewards (video/audio) to mask back-end provisioning latency.

---
═══════════════════════════════════════════════════════
CBAR AUDIT COMPLETION RECEIPT
═══════════════════════════════════════════════════════
PHASE:                   Phase 1 — Infrastructure
EPIC COUNT:              3
STORY COUNT:             8
─────────────────────────────────────────────────────
VERDICTS:
  PASS:                  0
  PASS WITH NOTE:        1
  REWRITE REQUIRED:      6
  FATAL CONFLICT:        1
─────────────────────────────────────────────────────
PRIMITIVES AUDITED:      EXP-FRC-002, EXP-FRC-003, EXP-FBK-001, EXP-PER-003
PRD MODULES LOADED:      PRD_01_CCP_Platform_Strategy.md
TECH SPECS LOADED:       NONE — flagged (FR-ERA3-08 missing)
─────────────────────────────────────────────────────
UNVERIFIED ASSUMPTIONS:  2 — [Tech Spec UI support, Telegram webhook interception]
CASCADE LOCK STATUS:     CLEAN
MANIFEST RULES:          7 canonical mandates produced
─────────────────────────────────────────────────────
TIMESTAMP:               2026-05-10T01:14:50+02:00
═══════════════════════════════════════════════════════
