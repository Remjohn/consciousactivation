# Infrastructure Foundation (Phase 1) - Epic Breakdown

**Author:** PM John (BMAD)
**Date:** 2026-05-08
**CBAR Hardened:** 2026-05-10
**Project Level:** Phase 1 Infrastructure
**Target Scale:** Host Shell, Registry Query Service, In-Chat Payments
**Audit Reference:** `docs/architecture/cbar_audits/CBAR_Audit_Phase1_Infrastructure.md`

---

## Canonical CBAR Mandates

> The following 7 structural mandates were produced by the CBAR adversarial audit of this Epic document. Engineering teams must treat these resolutions as canonical and non-negotiable. Any future story modifications to Phase 1 must be re-validated against these rules.

| # | Mandate | Origin | Governing Primitive | Rule |
|---|---------|--------|---------------------|------|
| 1 | **The Optimistic Render Rule** | Story 1.1 | `EXP-FRC-002` | Mini App initialization MUST decouple authentication (`initData`) from visual rendering. The first experiential screen renders optimistically; hash validation occurs asynchronously in the background. |
| 2 | **The Zero-Network Theme Rule** | Story 1.2 | `EXP-TRS-001` | `ResolvedPalette` CSS variables must be injected via the Telegram `startapp` URL parameter and decoded locally. Network calls that block the initial React render are strictly banned. |
| 3 | **The Primer Screen Rule** | Story 1.3 | `EXP-FRC-003` | Deep-links encountering OS permission blockers (microphone, camera) must route to a high-emotion System 1 primer screen that justifies the request before triggering the OS dialogue. Cold OS prompts are strictly banned. |
| 4 | **The Hot-Reload Rule** | Story 2.1 | `EXP-FBK-001` | The registry service must implement targeted Redis key invalidation whenever a primitive is updated, forcing the FastAPI worker to hot-reload only the affected YAML block into memory. Stale cache serving is strictly banned. |
| 5 | **The Deterministic Override Rule** | Story 2.2 | Orchestration Engine | The Primitive Registry Query Service must feature a `Conflict_Resolver` middleware. Deterministic `conflicts_with` field precedence overrides probabilistic AI requests. Contradictory primitive payloads are strictly banned. |
| 6 | **The Stored Value Rule** | Story 3.1 | `EXP-PER-003` | The offer tier eligibility check must combine `stripe_status` with `cumulative_assets_stored` from the `asset_manager`. Generic beginner pitches to high-investment free users are strictly banned. |
| 7 | **The Payment Masking Rule** | Story 3.3 | `EXP-FBK-001` | Stripe webhook resolution must immediately trigger a pre-rendered experiential reward (video/audio) to mask backend Coach OS provisioning latency. "Not ready" errors after successful payment are strictly banned. |

---

## Overview

This document provides the complete epic and story breakdown for the **Phase 1 Infrastructure** module. These foundational layers were initially drafted as Technical Specifications directly, but are retroactively decomposed here into user-value stories to ensure complete alignment with the `ERA3_Epic_and_Story_Writing_Protocol.md`. 

By mapping infrastructure to user value, we ensure no code is written in a vacuum, and every foundational piece adheres to the Experience Primitive Quality Standards.

> **CBAR Audit Status:** All 8 stories have been adversarially audited. 6 REWRITE REQUIRED verdicts, 1 FATAL CONFLICT verdict, and 1 PASS WITH NOTE verdict have been resolved and permanently integrated below.

> **Hallucination Purge:** The original document referenced `EXP-TRB-004` ("Attractive Things Work Better"). This primitive ID does not exist in the registry. The correct verified primitive is `EXP-TRS-001` ("Visceral Hooking / Premium Authority Aesthetic"), sourced from Donald A. Norman's *Emotional Design*, Chapter 1: "Attractive Things Work Better." All references have been corrected.

---

## Functional Requirements (FR) Inventory

*   **FR-ERA3-08 (Mini App Host Shell):** The container that allows Telegram to load Vite/React Mini Apps securely, applying DPA branding and handling routing.
*   **FR-ERA3-06 (Primitive Registry Query):** The backend FastAPI service that parses the 243+ YAML primitive files and serves them dynamically to the orchestration engine.
*   **FR-ERA3-02 (In-Chat Payments):** The native Telegram checkout flow for upgrading tiers, checking eligibility via the Offer Tier Governor.

---

## Epic 1: The Mini App Host Shell (FR-ERA3-08)
**Goal:** Establish the foundational frontend container that allows Telegram to natively host all our interactive experiences without dumping users out to external browsers.

### Story 1.1: Secure Web App Initialization
As a User, I want the Mini App to open instantly within Telegram and securely verify my identity, so that I don't have to repeatedly log in.

**Acceptance Criteria:**
*   **Given** I tap a Web App button in Telegram,
*   **When** the shell loads,
*   **Then** it renders the System 1 UI optimistically without blocking for network responses,
*   **And** it validates the `initData` hash against the bot token asynchronously in the background.

**CBAR Mandate Enforced:** `#1 — The Optimistic Render Rule`

**Primitive Quality Constraints (EXP-FRC-002: System 1 to System 2 Escalation):**
*   **Quality Standard (No Registration):** The transition from Telegram chat to active Web App must be seamless. No separate login screens, no email inputs. Identity is assumed via Telegram.
*   **Quality Standard (Optimistic Rendering):** The first experiential screen must render instantly using locally available data (Telegram context object, URL parameters). Authentication validation occurs asynchronously. If validation fails after render, the system gracefully downgrades access — it never blocks the initial render.
*   **Anti-Pattern Prevention:** Do not prompt the user for permissions or data that is already available via the Telegram context object. Do not display loading spinners, skeleton screens, or blank states while waiting for `initData` hash validation.

**Downstream Constraint:** Story 1.2 inherits this optimistic rendering mandate. Theme resolution cannot introduce network-blocking behaviour that contradicts this rule.

---

### Story 1.2: Global DPA Theme Resolution
As a Coach, I want the entire Mini App interface to reflect my brand archetype's colors and fonts, so that the experience feels like my proprietary app.

**Acceptance Criteria:**
*   **Given** the shell is initialized via a Telegram button tap,
*   **When** it determines the visual theme,
*   **Then** it decodes the `ResolvedPalette` directly from the injected `startapp` URL parameter,
*   **And** it applies the global CSS variables instantly with zero backend network requests.

**CBAR Mandate Enforced:** `#2 — The Zero-Network Theme Rule`

**Primitive Quality Constraints (EXP-TRS-001: Visceral Hooking / Premium Authority Aesthetic):**
*   **Quality Standard (Immediate Trust):** The aesthetic transition must be instant. The shell must not flash a generic gray theme before loading the brand colors. The `ResolvedPalette` is pre-computed by the backend and injected into the Telegram `startapp` URL parameter as an encoded payload, enabling the Mini App to decode and apply CSS variables locally with zero network dependency.
*   **Quality Standard (Visceral Authority):** Per `EXP-TRS-001`, the loaded palette must establish premium visual authority within milliseconds. The user's visceral processing layer must register the environment as high-status before any behavioral task is presented.
*   **Anti-Pattern Prevention:** Do not fetch theme data from the backend on Mini App initialization. Do not block rendering until a `ResolvedPalette` API response arrives. Do not display a white or system-default background at any point during initialization.

**Downstream Constraint:** Story 1.3 inherits this zero-network initialization constraint. Routing must also rely entirely on URL parameters, not backend context state.

---

### Story 1.3: Dynamic Surface Routing
As a User, I want the Mini App to open directly to the specific experience I tapped (e.g., Debate vs Tierlist), so that I don't have to navigate a complex menu.

**Acceptance Criteria:**
*   **Given** a Telegram button contains a `startapp` parameter (e.g., `react_solo`),
*   **When** the React Router deep-links to that specific module,
*   **Then** it checks required hardware permissions (microphone, camera) before rendering the active tool,
*   **And** if permissions are unset, it routes to a high-emotion System 1 primer screen that justifies the request before triggering the OS permission dialogue.

**CBAR Mandate Enforced:** `#3 — The Primer Screen Rule`

**Primitive Quality Constraints (EXP-FRC-003: The B=MAP Friction Audit):**
*   **Quality Standard (Physical Effort):** Eliminate the "Home Menu" entirely. Users must land directly inside the tool they intended to use. Max 0 clicks from launch to active tool.
*   **Quality Standard (Permission Priming):** If the target module requires hardware access (microphone for recording, camera for video), the routing engine must check the browser permissions API. If permissions are not yet granted, the user is routed to a contextual primer screen — a visually rich, emotionally compelling justification for the permission — before the OS-level dialogue fires. This ensures the user's Fogg Ability remains high and the OS prompt arrives with full contextual motivation.
*   **Anti-Pattern Prevention:** Do not fire a cold, context-free OS permission dialogue immediately on deep-link. Do not route users to modules that require hardware access without first confirming the access is available.

---

## Epic 2: The Primitive Registry Query Service (FR-ERA3-06)
**Goal:** Create the backend brain that allows the probabilistic NIM logic to query deterministic YAML rules.

### Story 2.1: Registry Parsing & Caching
As the System Architecture, I want to load all 243+ YAML primitives into memory on startup, so that runtime queries are sub-millisecond and don't require disk reads.

**Acceptance Criteria:**
*   **Given** the FastAPI application starts or a primitive is updated in the database,
*   **When** `lifespan` initialization occurs or a targeted invalidation event is received,
*   **Then** the service caches or hot-reloads the specific YAML primitives into Redis,
*   **And** serves all runtime queries from in-memory cache without disk I/O.

**CBAR Mandate Enforced:** `#4 — The Hot-Reload Rule`

**Primitive Quality Constraints (EXP-FBK-001: RIM Feedback Discipline):**
*   **Quality Standard (Latency Protection):** To meet the 3-second SLA for feedback loops across the platform, the registry must resolve primitive rules in memory. Disk I/O during a user session is strictly banned.
*   **Quality Standard (Cache Freshness):** If a primitive YAML is updated dynamically (e.g., a new primitive version is deployed), the system must emit a targeted Redis key invalidation event. The affected FastAPI worker hot-reloads only that specific YAML block into its in-memory cache, preserving freshness without compromising the 3-second SLA. The system must never serve stale rules, as Immediate feedback that is no longer Relevant or Meaningful violates the RIM standard and destroys user trust in the scoring engine.
*   **Anti-Pattern Prevention:** Do not perform full cache flushes on single-primitive updates. Do not rely on time-based cache expiry (TTL) as the sole freshness mechanism — event-driven invalidation is mandatory.

**Downstream Constraint:** Story 2.2 inherits this cache. The resolution query will always hit a fresh but in-memory cache, preserving the 3-second SLA.

---

### Story 2.2: Context-Aware Primitive Resolution
As the Orchestration Engine, I want to query the registry for specific primitives based on tags, families, or urgency, so that I can apply the correct behavioral rules to a user session.

**Acceptance Criteria:**
*   **Given** an active Reaction Loop,
*   **When** the system requests target primitives (e.g., `['EXP-TRG-002', 'EXP-SAF-003']`),
*   **Then** the service checks the requested set against their respective `conflicts_with` YAML fields,
*   **And** it applies a `Conflict_Resolver` precedence hierarchy to filter out mutually exclusive rules before returning the JSON payload.

**CBAR Mandate Enforced:** `#5 — The Deterministic Override Rule`

**Primitive Quality Constraints (Orchestration Engine Context):**
*   **Quality Standard (Deterministic Hierarchy):** The Orchestration Engine uses probabilistic AI (NIM models) to determine which primitives to apply. When the AI requests two or more primitives that mutually conflict based on their `conflicts_with` YAML fields, the deterministic rules take absolute precedence. The `Conflict_Resolver` middleware must parse the `conflicts_with` fields, apply a strict precedence hierarchy, and strip conflicting entries before the payload reaches any downstream generation system.
*   **Quality Standard (Payload Cleanliness):** All downstream generation systems (prompt engines, scoring engines, content factories) must receive a clean, non-contradictory constraint configuration. A schizophrenic prompt that demands both high friction and low friction simultaneously is a critical system failure.
*   **Anti-Pattern Prevention:** Do not return raw, unfiltered primitive payloads when the requested set contains mutual conflicts. Do not defer conflict resolution to downstream consumers — the Query Service is the single source of truth for conflict resolution.

---

## Epic 3: In-Chat Telegram Payments (FR-ERA3-02)
**Goal:** Enable frictionless upgrades (e.g., the $99.99 Coach OS) entirely within the Telegram chat interface.

### Story 3.1: Offer Tier Eligibility Check
As a Free User, I want the system to know exactly what tier I am eligible to buy, so that I am never offered a product I already own or am not ready for.

**Acceptance Criteria:**
*   **Given** I trigger an upgrade intent,
*   **When** the system generates the invoice,
*   **Then** it queries both `stripe_status` and `cumulative_assets_stored` from the `asset_manager`,
*   **And** it triggers a tailored 'Loyalty Unlock' offer flow if I have high stored value but low billing status.

**CBAR Mandate Enforced:** `#6 — The Stored Value Rule`

**Primitive Quality Constraints (EXP-PER-003: Cumulative Investment):**
*   **Quality Standard (Status Recognition):** The system must respect the user's historical purchases and cumulative investment. Pitching a foundational tier to an advanced user violates the trust architecture.
*   **Quality Standard (Investment-Aware Eligibility):** `EXP-PER-003` (Stored Value / IKEA Effect) dictates that user loyalty is proportional to the data/effort they have deposited. A Free Tier user with massive stored value (hundreds of recordings, a trained Voice DNA model, an extensive content archive) must not receive a generic beginner pitch. The `offer_tier_governor` must query both `stripe_status` (billing state) and `cumulative_assets_stored` (behavioral investment state). High-investment users on Free tiers trigger a 'Loyalty Unlock' flow with copy that explicitly acknowledges their investment and frames the upgrade as a natural next step for someone at their level.
*   **Anti-Pattern Prevention:** Do not base eligibility solely on billing state. Do not pitch generic upgrade copy to users who have already demonstrated significant platform investment.

**Downstream Constraint:** Story 3.2 inherits this tailored invoice payload, ensuring the Telegram native invoice reflects the advanced status copy.

---

### Story 3.2: Native Invoice Generation
As a User, I want to pay without leaving Telegram, so that the checkout process is completely frictionless.

**Acceptance Criteria:**
*   **Given** I am eligible for the $99.99 Coach OS,
*   **When** the agent sends the offer,
*   **Then** it uses Telegram's `sendInvoice` API to display a native payment button,
*   **And** if Stripe returns a `requires_action` state (e.g., 3D Secure / SCA), the system sends a reassuring, high-status Telegram bot message to keep the user engaged while they navigate the external verification.

**CBAR Audit Note:** PASS WITH NOTE — The `requires_action` Stripe state handling was added per the CBAR audit recommendation. *(UNVERIFIED ASSUMPTION: Telegram Bot API allows intercepting `requires_action` callbacks smoothly. Must be validated during Tech Spec implementation.)*

**Primitive Quality Constraints (EXP-FRC-003: The B=MAP Friction Audit):**
*   **Quality Standard (Checkout Velocity):** The checkout flow must utilize native OS payment methods (Apple Pay/Google Pay via Telegram). Sending the user to an external Stripe checkout page in a browser is strictly banned as it adds massive friction and context switching.
*   **Quality Standard (SCA Friction Mitigation):** Stripe Strong Customer Authentication (SCA) may force a 3D Secure verification loop, pulling the user into an external bank webview. When the system detects a `requires_action` Stripe state, it must deploy a high-status Telegram bot message that keeps the user in System 1 (reassuring, identity-affirming copy like "Your Coach OS credentials are being verified by the banking network. This confirms your elite access.") rather than failing silently or displaying a generic error.
*   **Anti-Pattern Prevention:** Do not allow a silent failure when `requires_action` fires. Do not display raw Stripe error codes to the user. Do not leave the user stranded in a bank webview without Telegram-native reassurance.

**Downstream Constraint:** Story 3.3 inherits this because fulfillment must wait for the asynchronous SCA challenge to clear before executing.

---

### Story 3.3: Post-Payment Fulfillment
As a Paying Customer, I want my account upgraded the exact second my payment clears, so that I get immediate gratification.

**Acceptance Criteria:**
*   **Given** a successful Stripe/Telegram payment,
*   **When** the `successful_payment` webhook fires,
*   **Then** my PostgreSQL tenant record is updated and an instant experiential reward (pre-rendered video/audio asset) is pushed to Telegram immediately,
*   **And** this reward asset masks the background execution of the Coach OS provisioning scripts (vector namespace creation, Voice DNA profile initialization) so that the user never encounters a "Not ready" state.

**CBAR Mandate Enforced:** `#7 — The Payment Masking Rule`

**Primitive Quality Constraints (EXP-FBK-001: RIM Feedback Discipline):**
*   **Quality Standard (Instant Reward):** The platform must immediately trigger a "Welcome/Unlock" experience the millisecond the webhook clears. Do not make the user wait for a batch process or manual approval.
*   **Quality Standard (Latency Masking):** Unlocking Coach OS requires heavy backend provisioning (creating vector namespaces, Voice DNA profile initialization, etc.) that may take 30-60 seconds. During this time, the user must be consuming a pre-rendered, high-production-value experiential reward (welcome video, audio message from the Agent, animated onboarding sequence) that was pushed via Telegram bot immediately upon webhook receipt. By the time the user finishes consuming this asset, the background provisioning is complete and the full Coach OS is ready. The user never sees a loading screen, "Not ready" error, or empty dashboard.
*   **Anti-Pattern Prevention:** Do not make the user tap the Coach OS button and receive a "Not ready" or "Still provisioning" error. Do not display a generic "Welcome! Your account has been upgraded." text message as the sole confirmation — the reward must be experiential, not informational. Do not write a success receipt to `receipt_chain` without simultaneously triggering the reward asset delivery.
