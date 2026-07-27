# Experience Mini Apps (Phase 3) - Epic Breakdown

**Author:** PM John (BMAD)
**Date:** 2026-05-10
**CBAR Audit Applied:** 2026-05-10 — All hallucinated primitive mappings purged; 7 Canonical CBAR Mandates integrated.
**Project Level:** Phase 3 Experience Mini Apps
**Target Scale:** 6 Dedicated Standalone Mini App Surfaces

---

## Overview

This document provides the complete epic and story breakdown for the **Phase 3 Experience Mini Apps** module. It strictly implements the architecture defined in PRD-02, 03, 04, 05, 07, and 09, ensuring all features are deeply tied to the Source of Truth PRDs rather than generalized UI ideas.

**Living Document Notice:** This document is generated via the `*create-epics-and-stories` BMAD workflow and subsequently hardened by the CBAR Audit Engine. It serves as the definitive structural input for the Era 3 Tech Spec Writing Protocol. Every Mini App built downstream is anchored in a concrete user story and governed by verified Experience Primitive Quality Standards. **Primitive IDs and names are frozen to the YAML registry — no narrative overrides are permitted.**

> **CBAR AUDIT STATUS:** Audit completed 2026-05-10. 5 catastrophic hallucination errors purged. 5 stories rewritten. 1 fatal conflict resolved. See `## Canonical CBAR Mandates` below.

---

## Functional Requirements (FR) Inventory

*   **FR-ERA3-01 (Webinar Companion):** The audience-facing dual-interface viewer (Telegram Mini App) that drives synchronous and async replay participation capture, while the coach operates from AFFiNE.
*   **FR-ERA3-11 (Challenge Arena):** The 28-day challenge engine utilizing Adaptive Layers, Capacity Tracks, and the Sunday Postcard ritual, replacing static calendar schedules.
*   **FR-ERA3-09 (Conscious Editor):** The backstage artifact compiler enforcing Trigger-First Execution, Archetype Container Routing, and Operator Review for CMF media validation.
*   **FR-ERA3-19 (Testimonial Builder & User Cards):** The momentum-triggered capture mechanic generating prismatic, status-bearing identity artifacts for the weekly gallery sharing ritual.
*   **Score Card Viewer:** The reflection-based FR61 evidence dashboard tracking conviction density, hedge frequency, pause architecture, and pitch stability.
*   **FR-ERA3-10 (Onboarding Flow):** The audit-to-challenge conversion path delivering the $0 free proof layer via one obvious action and meaningful reveal.

---

## Canonical CBAR Mandates

> These 7 mandates are derived directly from the CBAR Audit Constraint Resolution Manifest and are **non-negotiable**. Every story in this document must be validated against the applicable mandate during sprint review. Any Tech Spec that violates a mandate is considered a build blocker and must be re-submitted.

| # | Mandate Name | Rule |
| :-- | :--- | :--- |
| **M-01** | **Ambient Prompt Rule** | Audience participation prompts during live or replay webinars MUST render as non-blocking ambient UI overlays (e.g., lower-thirds, slide-in drawers). No participation UI element may ever obscure the primary video focal point (the coach's face). |
| **M-02** | **Per-Slide Feedback Rule** | Rehearsal and Rep Mode scorecards MUST be evaluated and presented instantly as the coach advances to the next slide. Aggregating feedback into a monolithic end-of-session report is a build blocker — it violates the Immediate mandate of `EXP-FBK-001`. |
| **M-03** | **Lateral Progression Rule** | The Adaptive Engine MUST implement a Lateral Progression Fallback. If vertical layer advancement is locked due to insufficient scores, the system MUST assign lateral drill variations within the current layer. The 28-day path UI must continue to show forward movement regardless. Stalling the UI is a churn event. |
| **M-04** | **Telemetry Surfacing Rule** | The Sunday Postcard MUST explicitly aggregate and visualize cumulative behavioral telemetry (e.g., total words spoken, total micro-pauses executed, sessions completed). Qualitative LLM-only summaries are banned. The postcard must weaponize the Sunk Cost Fallacy by making hidden effort visible. |
| **M-05** | **Modular CMF Recovery Rule** | The Conscious Editor MUST allow coaches to manually edit raw JSON/text transcript data in-browser to correct AI transcription errors without triggering a full audio re-recording or NIM pipeline re-run. Rejecting the entire take for a single-word correction is a UX failure state. |
| **M-06** | **Peer-Gated Apex Rule** | Solo behavioral stats MUST NOT unlock the apex tier. The Prismatic User Card tier is strictly gated behind peer endorsement (e.g., winning a public debate or receiving a threshold number of jury votes). Solo grinding can advance a user to Platinum maximum. This is a FATAL CONFLICT enforcement — `EXP-SOC-001` physics demand social activation for apex status. |
| **M-07** | **Auth-Free Benchmark Rule** | The onboarding audit result (benchmark teaser score) MUST be delivered instantly within the Telegram UI or anonymous Mini App session. No registration wall, email verification, or authentication gate may precede the benchmark reveal. The dopamine hit must occur before any commercial ask. |

---

## Epic 1: Webinar Companion Viewer (FR-ERA3-01)
**Goal:** Deliver the "Dual-Interface Broadcasting Architecture" (PRD-07). The coach broadcasts via the AFFiNE Studio Block, while the audience engages via the Telegram Mini App Webinar Companion. It must support 4 operating modes (YOLO, Interactive, Rep, Extract) and capture audience participation to fuel downstream content.

### Story 1.1: Audience Participation Capture (Replay & Live)
As an Audience Member, I want to respond to specific moments during the webinar (live or replay) using voice notes, polls, or reactions, so that my input is tied to the exact teaching claim — **without my participation UI ever breaking my emotional connection to the speaker.**

**Acceptance Criteria:**
*   **Given** I am watching a V2WS webinar replay inside the Mini App,
*   **When** the webinar hits a predefined extraction marker or high-tension moment,
*   **Then** a timed participation prompt appears as a **non-blocking ambient overlay** (lower-third bar or slide-in drawer) that never covers the coach's face or primary video focal point, allowing me to submit a voice-note reaction or vote while the coach remains fully visible.
*   **And** all captures are tagged with webinar ID, module/slide range, participant identity, and reaction type to feed the silent referral and content extraction engines.

> **CBAR Enforcement — M-01 (Ambient Prompt Rule):** Any implementation where a participation modal obscures the primary video focal point will be rejected at QA. UI element z-index and overlay geometry must be validated as non-blocking before sprint completion.

**Primitive Quality Constraints (`EXP-TRS-003`: Reflective Social Proof):**
*   **Quality Standard (Participation Memory Without Immersion Collapse):** The system must prove that the participation capture mechanism *amplifies* audience investment in the speaker rather than severing it. Overlay design must be validated to ensure the social proof capture does not produce cognitive displacement from the live teaching moment.

---

### Story 1.2: Rep Mode Delivery Scoring
As a Coach, I want to receive module-level delivery feedback **immediately after each slide**, so that I can correct pacing, reduce hedge density, and internalize improvements while the emotional state of that exact moment is still fresh.

**Acceptance Criteria:**
*   **Given** I enter "Rep Mode" in the AFFiNE Studio block,
*   **When** I complete the recording for a single slide and advance to the next,
*   **Then** the system **immediately** generates and displays a per-slide scorecard (hedge density, CTA pressure stability, pause architecture) for that slide *before* I begin recording the next one — **no monolithic end-of-session report is produced**.
*   **And** extraction-worthy moments are flagged in real time for the Extraction-First Planning engine.

> **CBAR Enforcement — M-02 (Per-Slide Feedback Rule):** Acceptance testing must verify that the score for Slide N is presented before the coach begins recording Slide N+1. A system that batches all 45 minutes and presents one report at session end will be rejected as a violation of `EXP-FBK-001` Immediacy.

**Primitive Quality Constraints (`EXP-FBK-001`: RIM Feedback Discipline):**
*   **Quality Standard (Repetition Without Pitch-Switch Collapse):** Feedback must isolate transition integrity, measuring if the coach's tone collapses when moving from teaching to invitation. This measurement must surface slide-by-slide, not as an averaged session metric, to be actionable.

---

## Epic 2: Challenge Arena & Adaptive Progression (FR-ERA3-11)
**Goal:** Deploy the frontend UI for the CBCS Law28 adaptive coaching engine. It must rely on Dual-Program Architecture (coach self-improvement vs. client deployment) and replace rigid calendar weeks with Readiness-Gated Adaptive Layers (Foundation, Structure, Nuance, Command) (PRD-05).

### Story 2.1: Capacity Track Routing & 28-Command Layer
As a Participant, I want my daily drills to match my current skill capacity and psychological readiness — and I want to **always feel I am moving forward** even when vertical skill progression is temporarily locked.

**Acceptance Criteria:**
*   **Given** my continuous FR61 voice evidence and diagnostic state,
*   **When** I open the Challenge Arena on any given day,
*   **Then** the Adaptive Engine assigns the next ritual from the 28-Command Operating Layer based on my specific Capacity Track.
*   **And** if vertical layer advancement is blocked because my conviction score or stability is below threshold, the engine **MUST assign a Lateral Progression drill** — a variation of the current Foundation layer drill — so I am never shown the same locked screen twice.
*   **And** the 28-day path UI continues to show me moving forward in session count regardless of whether my conceptual layer has escalated.

> **CBAR Enforcement — M-03 (Lateral Progression Rule):** The Tech Spec for the Adaptive Engine must include a defined Lateral Progression Fallback state machine. A UI that shows a user "Day 3" for 14 consecutive days with no variation is a confirmed churn event and must fail QA.

**Primitive Quality Constraints (`EXP-PRG-002`: Discover → Master → Replay):**
*   **Quality Standard (Evidence-Gated Escalation With Visible Forward Motion):** Users cannot advance to the next conceptual layer if their conviction score or stability is insufficient. However, the system MUST preserve perceived progression momentum by surfacing lateral variations that feed the Discover → Master → Replay arc within the current layer.

---

### Story 2.2: The Sunday Postcard Ritual
As a Participant, I want a weekly narrative compression of my efforts that **shows me the undeniable proof of how much I have invested**, so that I feel seen by the system and anchored for the next week.

**Acceptance Criteria:**
*   **Given** I have completed my active days for the week,
*   **When** Sunday arrives,
*   **Then** the Relationship Engine generates a "Sunday Postcard" that MUST include:
    *   **Cumulative behavioral telemetry:** Total words spoken, total micro-pauses executed, total sessions completed for the week.
    *   **Delta visualization:** A visual before/after comparison of at least one tracked metric (e.g., hedge frequency this week vs. last week).
    *   **One qualitative interpretation** of the data (e.g., "Your pause architecture stabilized in your final 3 sessions, suggesting the new drill is anchoring") — but this interpretation MUST reference specific numbers, not generic encouragement.
    *   **A forward forecast** naming the next layer or drill unlocking.

> **CBAR Enforcement — M-04 (Telemetry Surfacing Rule):** A postcard that contains only LLM-generated qualitative text ("You did great this week!") with no quantitative telemetry will be rejected. The Sunk Cost Fallacy must be weaponized by making the user's hidden investment measurable and visible.

**Primitive Quality Constraints (`EXP-FBK-004`: Bring the Data Forward):**
*   **Quality Standard (Reflection Grounded in Evidence, Not Platitude):** The postcard must surface the user's invisible compounding effort through hard numbers. Generic AI encouragement is explicitly banned. Dignity is created by the system acknowledging specific, real behavioral data — not by soft language.

---

## Epic 3: Conscious Editor - Compiler Backstage (FR-ERA3-09)
**Goal:** Provide the Operator Review surface where coaches inspect compiled meaning and orchestrated media. It enforces Trigger-First Execution (no blank pages) and Archetype Container Routing (PRD-02, PRD-03).

### Story 3.1: Trigger-First Artifact Review
As a Coach, I want to review content generated exclusively from my authentic voice recordings, so that I never have to stare at a blank prompt box.

**Acceptance Criteria:**
*   **Given** I have recorded a reaction or coaching voice note,
*   **When** the CCF meaning compiler finishes processing,
*   **Then** I am presented with the semantic artifact, structured into its Archetype Container (e.g., Myth Debunk, Achievement Story), before any visual format is applied.

**Primitive Quality Constraints (`EXP-PER-003`: Tailoring & Suggestion):**
*   **Quality Standard (Export Governance):** The UI must highlight the Coalition Signature and any Anti-Centroid Validator warnings, proving the artifact hasn't collapsed into generic AI sludge.

---

### Story 3.2: CMF Media Validation & Operator Review
As a Coach, I want to inspect the final visual and sonic rendering of my content and **fix minor errors in the AI transcript without discarding the entire take**, so I can approve premium quality at high throughput without being punished for a single-word correction.

**Acceptance Criteria:**
*   **Given** an artifact has passed CCF meaning compilation and CMF has rendered the static/motion/sonic assets,
*   **When** I open the Conscious Editor review tier,
*   **Then** the system displays the video/carousel with a **side-by-side editable transcript panel** showing the raw JSON/text transcript layer.
*   **And** I can directly edit the transcript text in the browser (e.g., fix a misspelled word in a B-roll caption) and re-render **only** the affected caption or text layer — **without re-recording audio or re-running the biometric NIM pipeline**.
*   **And** the media object displays its full lineage back to the original voice recording, confirming meaning was not re-authored by the media generator.

> **CBAR Enforcement — M-05 (Modular CMF Recovery Rule):** The Tech Spec must define granular re-render scopes. A pipeline that forces a full NIM re-run for a single-word transcript correction fails `EXP-SAF-002` Possible-Win Scarcity physics. Coaches must experience a "Possible Win" (fixable error) not an "Impossible Recovery" (total discard).

**Primitive Quality Constraints (`EXP-SAF-002`: Possible-Win Scarcity):**
*   **Quality Standard (Modular Failure Recovery):** Failure states inside the Conscious Editor must always offer a viable, scoped recovery path. The experience of fixing an error must feel achievable, not catastrophic. If the only recovery path requires discarding all prior work, the system has failed the Possible-Win physics mandate.

---

## Epic 4: Silent Testimonial Builder & User Cards (FR-ERA3-19)
**Goal:** Automatically capture transformation evidence during momentum peaks and generate status-bearing User Cards for the weekly sharing gallery, fueling Silent Referral (PRD-05, PRD-09).

### Story 4.1: Momentum-Triggered Capture Flow
As a Participant, I want to be naturally prompted to reflect on my breakthrough right when I achieve it, so that I can capture my true emotional state.

**Acceptance Criteria:**
*   **Given** I cross a benchmark threshold or complete a significant challenge layer,
*   **When** the score is revealed,
*   **Then** the system initiates the 6-step momentum capture flow, seamlessly extracting my reflection via voice or video.

**Primitive Quality Constraints (`EXP-TRG-002`: Hook Cycle Velocity):**
*   **Quality Standard (Immediate Proof at Peak Emotional State):** The capture must be triggered at the exact moment of score reveal — not delayed by a loading state, navigation change, or confirmation modal. The Hook Cycle momentum must be preserved through to the capture submission.

---

### Story 4.2: Prismatic User Card Progression
As a Participant, I want my progress visualized on a premium digital trading card, and I want the highest tier to feel **truly earned through the community** — not achievable by grinding alone.

**Acceptance Criteria:**
*   **Given** my performance stats and streak count,
*   **When** my profile updates weekly,
*   **Then** my User Card dynamically renders my avatar, tier badge, primary stats, and weekly delta arrows, evolving in color from Bronze → Silver → Gold → Platinum via solo behavioral performance milestones.
*   **And** the **Prismatic tier is strictly gated behind peer endorsement** — specifically, a user must win a public debate judged by peers OR receive a threshold number of jury endorsement votes from certified community members. Solo stats alone CANNOT unlock Prismatic tier under any condition.
*   **And** the Prismatic gate is clearly communicated in the UI before Platinum, so users understand the peer-engagement requirement is coming.

> **CBAR Enforcement — M-06 (Peer-Gated Apex Rule) — FATAL CONFLICT RESOLUTION:** The original story allowed Prismatic to be unlocked by solo grinding. This is a fatal violation of `EXP-SOC-001` (Social Treasures + Group Quests), which mandates that apex-tier social rewards cannot be earned by individual effort alone. This rule is non-negotiable. Any Tech Spec that allows solo stat progression to unlock Prismatic will be rejected as a FATAL BUILD BLOCKER.

**Primitive Quality Constraints (`EXP-SOC-001`: Social Treasures + Group Quests):**
*   **Quality Standard (Apex Status Requires Social Activation):** The Prismatic card carries no social weight if it can be earned in isolation. The peer-endorsement gate is not a game mechanic — it is the engine of the Silent Referral loop. The coach must share their work publicly to obtain votes, creating the viral distribution event the platform depends on.

---

## Epic 5: Score Card Viewer
**Goal:** Present the FR61 evidence contract (Conviction Density, Hedge Frequency, Pause Architecture, Pitch Stability) as a reflective, status-bearing artifact rather than a punishing clinical report (PRD-04, PRD-05).

### Story 5.1: Actionable Biometric Reflection
As a Participant, I want to view my speaking biometrics in a way that shows me exactly how to improve, so that my score feels like a roadmap, not a judgment.

**Acceptance Criteria:**
*   **Given** my continuous voice submissions have generated an FR61 evidence packet,
*   **When** I open the Score Card Viewer,
*   **Then** I see my trend deltas for hedge frequency and conviction density, paired explicitly with a developmental insight or next-step recommendation.

**Primitive Quality Constraints (`EXP-FBK-001`: RIM Feedback Discipline):**
*   **Quality Standard (Scoring as Reflection):** Data without interpretation is banned. A bad score must create reflection, a viable comeback path, and the belief that improvement is possible. RIM mandates: the data is Relevant (tied to specific behaviors), Immediate (presented in real time), and Meaningful (actionable, not decorative).

---

## Epic 6: Zero-Config Onboarding Flow (FR-ERA3-10)
**Goal:** Execute the "Audit-to-Challenge" conversion path. Deliver the $0 free proof layer (free benchmark teaser and Lead Magnet) via one obvious action and one emotionally satisfying reveal — with **zero authentication gates before the reveal** (PRD-01, PRD-04, PRD-05).

### Story 6.1: The Audit-to-Challenge Conversion
As a New Client, I want to receive immediate insight into my speaking style without filling out forms or creating an account, so that I immediately understand the value of the system and willingly take the next step.

**Acceptance Criteria:**
*   **Given** I tap a Silent Referral link and enter the Telegram Mini App,
*   **When** I complete the single, obvious 60-second baseline voice audit,
*   **Then** the system **immediately delivers a meaningful benchmark teaser score** within the Telegram chat UI or anonymous Mini App session — **no registration, email verification, or authentication gate is triggered before this reveal**.
*   **And** after the teaser is revealed, the Lead Magnet layer is surfaced as the natural, friction-minimal next step.

> **CBAR Enforcement — M-07 (Auth-Free Benchmark Rule):** Any implementation that gates the audit score behind an account creation flow will be rejected. The dopamine hit of seeing the score must precede any commercial ask. Auth walls at this moment guarantee churn.

**Primitive Quality Constraints (`EXP-FRC-002`: Friction-Zero Ability):**
*   **Quality Standard (First-Session Architecture):** The flow must optimize for one obvious action, one meaningful output, and one clear next step. It must deliver an undeniable "shock of value" before any commercial ask. Friction-Zero means the cognitive load of participation must be near-zero at every decision point in this flow.

---

## FR Coverage Matrix

| FR ID | Feature | Mapped Epic & Story | CBAR Status |
| :--- | :--- | :--- | :--- |
| FR-ERA3-01 | Webinar Companion | Epic 1 (Stories 1.1, 1.2) | ✅ Rewritten |
| FR-ERA3-11 | Challenge Arena | Epic 2 (Stories 2.1, 2.2) | ✅ Rewritten |
| FR-ERA3-09 | Conscious Editor | Epic 3 (Stories 3.1, 3.2) | ✅ Partially Rewritten (3.2) |
| FR-ERA3-19 | Testimonial Builder & Cards | Epic 4 (Stories 4.1, 4.2) | ✅ Fatal Conflict Resolved (4.2) |
| N/A | Score Card Viewer | Epic 5 (Story 5.1) | ✅ Pass — No Changes Required |
| FR-ERA3-10 | Onboarding Flow | Epic 6 (Story 6.1) | ✅ Auth-Wall Guard Added |

---

## Primitive ID Correction Log

> This table serves as the canonical hallucination correction record for this document. Any future BMAD pipeline output must be validated against this log before being merged.

| Location | Hallucinated ID | Hallucinated Name | Corrected ID | Correct Registry Name |
| :--- | :--- | :--- | :--- | :--- |
| Story 1.1 | `EXP-TRB-003` | Visceral Hooking | `EXP-TRS-003` | Reflective Social Proof |
| Story 2.1 | `EXP-PRG-001` | Discover→Master→Replay | `EXP-PRG-002` | Discover → Master → Replay |
| Story 2.2 | `EXP-FBK-004` | Signature Moment | `EXP-FBK-004` | Bring the Data Forward |
| Story 3.2 | `EXP-SAF-002` | Sovereign Control | `EXP-SAF-002` | Possible-Win Scarcity |
| Story 4.1 | `EXP-TRG-002` | Kairos / Urgent Optimism | `EXP-TRG-002` | Hook Cycle Velocity |

*Note for Registry Maintainers: The audit identified that `EXP-TRG-002` and `EXP-PRG-001` both carry the name "Hook Cycle Velocity" across families. This bloat must be resolved in the primitive YAML registry to prevent future mapping collisions.*
