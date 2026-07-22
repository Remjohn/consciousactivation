# Pipelines & Engines (Phase 4) - Epic Breakdown

**Author:** PM John (BMAD)
**Date:** 2026-05-08
**CBAR Hardened:** 2026-05-11
**Project Level:** Phase 4 Pipelines & Engines
**Target Scale:** 7 Foundational Backend Architecture Components
**Audit Reference:** `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md`

---

## Canonical CBAR Mandates

> The following 7 structural mandates were produced by the CBAR adversarial audit of this Epic document. Engineering teams must treat these resolutions as canonical and non-negotiable. Any future story modifications to Phase 4 must be re-validated against these rules.

| # | Mandate | Origin | Governing Primitive | Rule |
|---|---------|--------|---------------------|------|
| 1 | **The Intelligence-Gated Intercept Rule** | Story 1.1 | `EXP-PER-003` | Operators MUST NOT execute an intercept without first reviewing the specific diagnostic excerpt that triggered the red flag. The UI must enforce an excerpt-review gate before the intercept voice recorder unlocks, ensuring flawless tailoring. |
| 2 | **The Cinematic Meaning Rule** | Story 2.1 | `EXP-TRS-004` | The CMF rendering engine must map scripts to high-contrast, intense visual grammar to preserve the Epic Meaning / Crusade narrative. Flat, brightly lit, "corporate SaaS" aesthetic outputs are strictly banned. |
| 3 | **The Inline Routing SLA** | Story 3.1 | `EXP-PRG-001` | Async routing across the four backend surfaces must execute inline (< 3 seconds) to preserve Hook Cycle Velocity. Batched, overnight, or delayed routing is strictly banned. |
| 4 | **The Frictionless Block Rule** | Story 4.1 | `EXP-FRC-006` | The Execution Guard must not display static error walls. A blocked generation request must instantly trigger a Telegram Voice recording modal pre-loaded with a provocative prompt derived from the coach's initial intent. |
| 5 | **The Actionable Rejection Rule** | Story 5.1 | `EXP-FBK-001` | Anti-Centroid Validator rejections must highlight the exact transcript sentences that triggered the centroid collapse and provide a specific, actionable coaching fix. Generic "too generic" rejections are strictly banned. |
| 6 | **The Sonic Prestige Rule** | Story 6.1 | `EXP-TRS-003` | All dynamic voice prompts must pass through the premium `ConsciousVoice` TTS model (or pre-recorded human coach audio). Generic robotic TTS is strictly banned as it destroys Reflective Social Proof and the premium illusion. |
| 7 | **The Long Loop Framing Rule** | Story 7.1 | `EXP-PRG-004` | Any algorithm-driven downgrade in difficulty must be explicitly framed by the Relationship Engine against the user's positive 30-day macro trend to prevent shame-based churn. Unexplained downgrades are strictly banned. |

---

## Overview

This document provides the complete epic and story breakdown for the **Phase 4 Pipelines & Engines** module. These are the backend intelligence layers that power the Mini Apps built in Phase 3. The logic here is strictly derived from the core operating doctrines in PRD-02, 03, 04, 05, and 07.

**Living Document Notice:** This document is generated via the `*create-epics-and-stories` BMAD workflow. It serves as the definitive structural input for the Era 3 Tech Spec Writing Protocol, moving backend services away from generic generation toward trigger-first, primitive-governed orchestration.

> **CBAR Audit Status:** All 7 stories have been adversarially audited. 7 REWRITE REQUIRED verdicts have been resolved and permanently integrated below.

> **Hallucination Purge:** The original document contained 4 catastrophic mapping errors where the BMAD pipeline fabricated both primitive names and prefixes:
> - `EXP-TRB-004` ("Attractive Things Work Better") → Corrected to `EXP-TRS-004` (Epic Meaning Framing). Prefix was hallucinated (`TRB` does not exist); name was fabricated from a Norman chapter title, not the registry definition.
> - `EXP-PRG-001` ("Discover→Master→Replay") → Corrected display name to "Hook Cycle Velocity" per verified YAML registry.
> - `EXP-TRB-003` ("Visceral Hooking") → Corrected to `EXP-TRS-003` (Reflective Social Proof). Prefix was hallucinated (`TRB` does not exist); name was fabricated.
> - `EXP-PRG-004` ("Flow Through Grinding") → Corrected display name to "Long Loops for Habit Formation" per verified YAML registry.
>
> All references have been corrected to enforce the true physics of the platform.

---

## Functional Requirements (FR) Inventory

*   **FR-ERA3-07 (AFFiNE Studio Block Orchestration):** The sovereign command center allowing coaches to control and broadcast programs, review scorecards, and intervene natively (PRD-01, PRD-04, PRD-07).
*   **FR-ERA3-12 (CMF Arc-Governed Rendering):** The deterministic visual and sonic assembly engine utilizing Beat Clusters to translate meaning into premium media (PRD-03).
*   **FR-ERA3-13 (Four-Surface Async Skill Ladder):** The routing system managing progression through Law28, Webinar, Networking (OFAP), and Social Reaction mastery (PRD-04).
*   **FR-ERA3-15 (Trigger-First Execution Guard):** The compiler law that prevents content generation unless an authentic reaction has been captured first (PRD-02).
*   **FR-ERA3-16 (Archetype Container Runtime):** The structured semantic containers that hold primitive coalitions for downstream rendering before visual formatting is decided (PRD-02).
*   **FR-ERA3-17 (Voice Prompt Engine):** The engine responsible for executing the Six Emotional Jobs (Orient, Relieve, Validate, Invite, Redirect, Celebrate) via voice notes (PRD-04).
*   **FR-ERA3-18 (CBCS Four-Engine Runtime):** The Diagnostic, Ritual, Evidence, and Relationship engine architecture powering adaptive challenges and progression (PRD-05).

---

## Epic 1: AFFiNE Studio Block Orchestration (FR-ERA3-07)
**Goal:** Enable operators to orchestrate coaching natively from the AFFiNE dashboard, ensuring Lean Cognitive Load while providing sovereign control over the audience's Telegram experience (PRD-01, PRD-04, PRD-07).

### Story 1.1: Operator Intervention and Dashboard Review
As an Operator, I want to see a consolidated view of my clients' progress and red flags, so that I can execute human intercepts precisely when automation fails or excels.

**Acceptance Criteria:**
*   **Given** I log into the AFFiNE command center,
*   **When** I view the Client Card,
*   **Then** I see the visual completion arc, streak flame, composite Conviction Score, and Red Flag Feed,
*   **And** each red flag entry includes a qualitative diagnostic excerpt (e.g., "Client paused for 4 seconds after mentioning pricing" or a transcription snippet of the flagged moment),
*   **And** the intercept voice recorder remains locked until I explicitly confirm review of the diagnostic excerpt.

**CBAR Mandate Enforced:** `#1 — The Intelligence-Gated Intercept Rule`

**Primitive Quality Constraints (EXP-PER-003: Tailoring & Suggestion):**
*   **Quality Standard (Contextual Intelligence):** The Red Flag Feed must not be a raw analytics alert. Each flag must surface the specific diagnostic excerpt or transcription snippet that triggered it, providing the operator with enough qualitative context to craft a hyper-personalized intercept. The operator must understand *why* the user failed before they speak.
*   **Quality Standard (Gated Recorder):** The one-click "Intercept Button" must gate the voice recorder behind a confirmed excerpt review state. The operator must tap "I've reviewed this" (or equivalent explicit confirmation) before the recorder activates, ensuring every intercept is informed rather than reflexive.
*   **Anti-Pattern Prevention:** Do not surface red flags as bare quantitative alerts (e.g., "Low Confidence: 0.3") without qualitative context. Do not allow operators to fire an intercept voice note without first confirming review of the diagnostic excerpt. The coach must never send a generic "keep going!" message that reveals they are reading automated alerts.

**Downstream Constraint:** The diagnostic excerpt format must be compatible with the CBCS Evidence Engine (Epic 7), which produces the biometric scores that feed the Red Flag Feed.

---

## Epic 2: CMF Arc-Governed Rendering (FR-ERA3-12)
**Goal:** Deploy the three-phase media pipeline (Composition, Generation, Assembly) to translate CCF meaning packets into cinematic visuals using Beat Clusters and the Deterministic Control Layer (PRD-03).

### Story 2.1: Narrative Geometry Translation
As the CMF Pipeline, I want to assemble video shots based on an emotional arc, so that the visual pacing matches the psychological truth of the script.

**Acceptance Criteria:**
*   **Given** a Coalition Script Spine from CCF,
*   **When** it enters the Narrative Rendering Model,
*   **Then** it translates the meaning into specific Beat Clusters, applying distinct shot grammar and music tempo for the assigned arc (e.g., Rally, Witness, Reflection),
*   **And** the Deterministic Control Layer enforces Cinematic Meaning visual grammar: high-contrast lighting, cinematic pacing, intense sonic beds, First Frame Composer hooks, ConsciousPose, and Identity LoRA,
*   **And** no output is released unless it passes the Epic Meaning Framing quality gate, which rejects flat, brightly lit, corporate-aesthetic renders.

**CBAR Mandate Enforced:** `#2 — The Cinematic Meaning Rule`

**Primitive Quality Constraints (EXP-TRS-004: Epic Meaning Framing):**
*   **Quality Standard (Crusade Narrative):** `EXP-TRS-004` mandates that every media artifact must frame the coach's message as a high-stakes manifesto — not a corporate explainer. The Narrative Rendering Model must explicitly map the `Coalition Script Spine` to Epic Meaning visual grammar: dramatic lighting, cinematic shot composition, and sonic beds that evoke urgency and significance. The artifact must feel like a movement-defining statement that the coach is proud to attach their name to.
*   **Quality Standard (First-Frame Safety):** The Deterministic Control Layer must strictly enforce First Frame Composer hooks, ConsciousPose directives, and Identity LoRA parameters to prevent the asset from dissolving into generic AI slop. The first frame of every generated asset must pass a visual authority check before the full render pipeline executes.
*   **Anti-Pattern Prevention:** Do not render with flat, even lighting. Do not use generic stock music or royalty-free background tracks that strip emotional weight. Do not produce assets that look or feel like SaaS tutorial videos, webinar slides, or corporate explainers. If the coach recorded a paradigm-shifting defense, the visual output must match that intensity.

**Downstream Constraint:** The Archetype Container Runtime (Epic 5) feeds this pipeline. The emotional weight locked in the container dictates the intensity level the CMF must match.

---

## Epic 3: Four-Surface Async Skill Ladder (FR-ERA3-13)
**Goal:** Create the routing logic that moves users seamlessly across the platform's four communication disciplines, prioritizing asynchronous daily repetition over live scheduling (PRD-04).

### Story 3.1: Voice-First Asynchronous Progression
As a Participant, I want to practice my speaking skills on my own schedule via Telegram, so that I can achieve daily repetitions without scheduling friction.

**Acceptance Criteria:**
*   **Given** my `ExperienceStatePacket` dictates my next developmental task,
*   **When** I interact with the system via Telegram voice notes,
*   **Then** the backend routes my practice into the correct surface (Law28, Webinar, Networking, or Social) and returns me to the next logical step (the reward, the scorecard, or the rebuttal prompt) inline within < 3 seconds,
*   **And** the corresponding content exhaust is generated automatically without requiring a separate batch processing step.

**CBAR Mandate Enforced:** `#3 — The Inline Routing SLA`

**Primitive Quality Constraints (EXP-PRG-001: Hook Cycle Velocity):**
*   **Quality Standard (Inline Execution):** `EXP-PRG-001` mandates that the neurological link between action and reward must never be severed. The `ExperienceStatePacket` routing across all four backend surfaces must execute inline. The user must receive their next logical step (feedback score, rebuttal prompt, or reward) within 3 seconds of voice note submission. Overnight batch processing, background queue-based compilation, or any routing mechanism that introduces a "Processing..." delay is strictly banned.
*   **Quality Standard (Async-First Default):** The system must treat async voice repetition as the primary engine for mastery. Live touchpoints are strictly optional multipliers, not prerequisites. The routing logic must never block progression waiting for a scheduled live event.
*   **Anti-Pattern Prevention:** Do not batch-process voice submissions to the Webinar or Networking surfaces overnight. Do not display "Processing..." states that promise future compilation. Do not sever the action→reward loop by deferring feedback to a later session.

**Downstream Constraint:** The CBCS Four-Engine Runtime (Epic 7) depends on this SLA. The Evidence Engine must receive the routing payload inline to update state dynamically during a single session.

---

## Epic 4: Trigger-First Execution Guard (FR-ERA3-15)
**Goal:** Enforce the core CCF compiler doctrine: no content is generated without prior authentic reaction or psychological pressure (PRD-02).

### Story 4.1: The Blank-Page Prevention Block
As the System Architecture, I want to reject any request to generate content unless accompanied by a recorded voice reaction, so that we never produce hallucinated AI slop.

**Acceptance Criteria:**
*   **Given** the content factory receives an execution request,
*   **When** the request lacks an authenticated source dependency (e.g., `CoachResponseCapture`),
*   **Then** the execution guard halts compilation and instantly surfaces the Telegram Voice recording modal,
*   **And** the modal is pre-loaded with a specific, provocative prompt derived from the coach's initial intent (e.g., "Tell me why your competitors are wrong about this"),
*   **And** upon voice capture, the system immediately feeds the reaction into the Archetype Container Runtime (Epic 5) without requiring additional navigation.

**CBAR Mandate Enforced:** `#4 — The Frictionless Block Rule`

**Primitive Quality Constraints (EXP-FRC-006: Poka-Yoke / Constraint as Focus):**
*   **Quality Standard (Intuitively Guided Block):** `EXP-FRC-006` mandates a true Poka-Yoke — a constraint that intuitively guides the user to the correct behavior — not a dumb friction wall. The Execution Guard must transform the hard block into a frictionless path to compliance. When generation is blocked, the system must not display a static error message ("Blocked: Authenticated Source Required"). Instead, it must instantly pop up the Telegram Voice recording modal with a provocative, contextual prompt that channels the coach's original intent into an authentic reaction.
*   **Quality Standard (Constraint as Trigger):** The block itself becomes the trigger. By framing the rejection as an invitation to record, the system converts a frustrating dead-end into the exact behavior the platform needs: an authentic voice reaction that feeds the Archetype Container Runtime downstream.
*   **Anti-Pattern Prevention:** Do not display static error messages (e.g., "Error: No reaction found," "Blocked: Authenticated Source Required"). Do not require the coach to navigate away from their current context to find the recording interface. Do not present the block as a system limitation — present it as a creative prompt.

**Downstream Constraint:** The Archetype Container Runtime (Epic 5) receives the voice capture directly from this modal, creating a seamless trigger→container→CMF pipeline.

---

## Epic 5: Archetype Container Runtime (FR-ERA3-16)
**Goal:** Route compiled primitive coalitions into specific psychological semantic containers before deciding the visual format, preserving the narrative's emotional weight (PRD-02).

### Story 5.1: Psychological Container Formatting
As the Content Compiler, I want to assemble the coach's reaction into a structured archetype (e.g., "Myth Debunk" or "Achievement Story"), so that the underlying persuasion geometry is locked before CMF rendering.

**Acceptance Criteria:**
*   **Given** a validated Primitive Coalition Signature,
*   **When** it is processed by the runtime,
*   **Then** it generates a specific Archetype Container that dictates the narrative pacing and logic, passing this as the `CCFRoutingRecommendation` to the CMF,
*   **And** if the Anti-Centroid Validator rejects the take, the failure response payload must return the exact transcript sentences that triggered the centroid collapse, along with specific coaching feedback (e.g., "Your stance on X matches 90% of the industry. Inject a specific client anecdote here to pass the gate"),
*   **And** the coach is re-routed to the voice recording modal with the specific failing sentences highlighted as a re-recording prompt.

**CBAR Mandate Enforced:** `#5 — The Actionable Rejection Rule`

**Primitive Quality Constraints (EXP-FBK-001: RIM Feedback Discipline):**
*   **Quality Standard (Anti-Centroid Law):** The output must pass the Anti-Centroid Validator, ensuring the coach's signature quirks and sharpest takes are not flattened into corporate compromises. The Validator compares the coach's reaction against the industry centroid and rejects takes that lack differentiation.
*   **Quality Standard (Actionable RIM Failure):** When the Anti-Centroid Validator rejects a take, the `CCFRoutingRecommendation` failure state must be fully actionable per RIM discipline. The response payload must include: (a) the exact transcript sentences that collapsed into the centroid, (b) a quantified similarity score showing *how* generic the take is, and (c) a specific, coaching-style fix that tells the coach exactly what to inject (a personal anecdote, a contrarian data point, a named client example) to pass the gate on the next attempt.
*   **Anti-Pattern Prevention:** Do not return vague rejection messages (e.g., "Your reaction is too generic. Try again."). Do not present the Anti-Centroid Validator as a black box. Do not reject the coach's take without providing them a clear, specific path to redemption. The coach must never feel judged by an opaque algorithm.

**Downstream Constraint:** The CMF Arc-Governed Rendering engine (Epic 2) receives the container output. Rejection loops must resolve before the container reaches CMF, preserving pipeline integrity.

---

## Epic 6: Voice Prompt Engine (FR-ERA3-17)
**Goal:** Treat system voice notes as high-fidelity coaching tools with specific emotional jobs rather than generic notification readings (PRD-04).

### Story 6.1: Emotional Job Routing
As a User, I want the system's voice notes to sound supportive after a failure but commanding during a challenge, so that the experience feels emotionally intelligent.

**Acceptance Criteria:**
*   **Given** a system prompt needs to be delivered,
*   **When** the `VoicePromptPacket` is generated,
*   **Then** it dynamically selects exactly one emotional job (Orient, Relieve, Validate, Invite, Redirect, Celebrate) and applies the correct tone profile and sonic bed,
*   **And** the voice output is rendered exclusively through the premium `ConsciousVoice` TTS model (or pre-recorded human coach audio),
*   **And** the output passes a sonic quality gate that rejects robotic, low-fidelity, or tonally mismatched renders before delivery to the user.

**CBAR Mandate Enforced:** `#6 — The Sonic Prestige Rule`

**Primitive Quality Constraints (EXP-TRS-003: Reflective Social Proof):**
*   **Quality Standard (One Emotional Job):** Noisy, multipurpose voice prompts are banned. Each voice note must perform a single emotional job flawlessly, keeping the voice as the lead instrument in the user's experience. Combining "Celebrate" and "Redirect" in a single voice note creates emotional dissonance and is a critical UX failure.
*   **Quality Standard (Premium Sonic Authority):** `EXP-TRS-003` mandates Reflective Social Proof — the user must be proud to be associated with the platform's voice. All dynamic voice prompts must be rendered through the premium, latency-optimized `ConsciousVoice` TTS model or pre-recorded human coach audio. Generic, robotic TTS (Siri-like, Google TTS default, or any model that triggers the "AI uncanny valley") is strictly banned. The sonic delivery must be elite enough that the user would willingly share or replay the voice note as social proof.
*   **Anti-Pattern Prevention:** Do not fall back to generic system TTS when the `ConsciousVoice` model is unavailable — queue and retry or use pre-recorded fallbacks. Do not deliver a "Celebrate" job with a flat, monotone vocal profile. Do not combine multiple emotional jobs in a single voice note to save API calls.

**Downstream Constraint:** The CBCS Four-Engine Runtime (Epic 7) depends on this engine to deliver its feedback payloads. If the voice quality is substandard, the entire CBCS feedback loop loses trust authority.

---

## Epic 7: CBCS Four-Engine Runtime (FR-ERA3-18)
**Goal:** Implement the Diagnostic, Ritual, Evidence, and Relationship engines that power the adaptive, self-coding challenges (PRD-05).

### Story 7.1: Continuous Voice Evidence Routing
As a Participant, I want my next challenge task to be dictated by my actual speaking weaknesses, so that I am always improving my specific bottlenecks.

**Acceptance Criteria:**
*   **Given** I submit daily voice notes,
*   **When** the Evidence Engine extracts my FR61 biometric scores,
*   **Then** the Diagnostic Engine updates my capacity track and the Ritual Engine modifies tomorrow's drill to address the specific performance delta,
*   **And** if the Diagnostic Engine downgrades a capacity track or assigns an easier ritual, the Relationship Engine intercepts the notification and contextualizes it against my positive Long Loop macro trend (e.g., "We are stepping back to solidify your pause architecture, but you are still up 20% over the last 14 days"),
*   **And** the user-facing message explicitly frames the downgrade as a strategic refinement, not a regression.

**CBAR Mandate Enforced:** `#7 — The Long Loop Framing Rule`

**Primitive Quality Constraints (EXP-PRG-004: Long Loops for Habit Formation):**
*   **Quality Standard (Engine Separation):** The backend must physically separate the four engines (Diagnostic, Ritual, Evidence, Relationship) to prevent the challenge system from becoming a monolithic, opaque loop that ignores the user's psychological state. Each engine must have a distinct service boundary, clear input/output contracts, and independent scaling characteristics.
*   **Quality Standard (Long Loop Visibility):** `EXP-PRG-004` mandates that macro-progression must remain visible even during local setbacks. When the Diagnostic Engine downgrades a capacity track, the Relationship Engine must intercept the notification and frame it against the user's 14-day or 30-day positive trend. The user must never see only that they are "going backward" — they must always see the Long Loop context that transforms a local failure into a strategic pause.
*   **Quality Standard (Shame Prevention):** The Relationship Engine's intercept must use identity-affirming language that acknowledges the difficulty while reinforcing the user's commitment trajectory. Raw score downgrades without narrative context are a retention-critical failure.
*   **Anti-Pattern Prevention:** Do not expose raw capacity track downgrades to the user without Relationship Engine contextualization. Do not allow the Diagnostic Engine to directly push notifications — all user-facing communications from the CBCS must route through the Relationship Engine's framing layer. Do not display numerical regression without accompanying positive Long Loop metrics.

---

## FR Coverage Matrix

| FR ID | Feature | Mapped Epic & Story |
| :--- | :--- | :--- |
| FR-ERA3-07 | AFFiNE Studio Block Orchestration | Epic 1 (Story 1.1) |
| FR-ERA3-12 | CMF Arc-Governed Rendering | Epic 2 (Story 2.1) |
| FR-ERA3-13 | Four-Surface Async Skill Ladder | Epic 3 (Story 3.1) |
| FR-ERA3-15 | Trigger-First Execution Guard | Epic 4 (Story 4.1) |
| FR-ERA3-16 | Archetype Container Runtime | Epic 5 (Story 5.1) |
| FR-ERA3-17 | Voice Prompt Engine | Epic 6 (Story 6.1) |
| FR-ERA3-18 | CBCS Four-Engine Runtime | Epic 7 (Story 7.1) |
