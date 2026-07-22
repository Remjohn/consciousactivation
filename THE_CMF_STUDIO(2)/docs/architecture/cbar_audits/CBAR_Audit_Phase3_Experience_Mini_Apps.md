# CBAR Audit Manifest: Phase 3 Experience Mini Apps

**Author:** CBAR Epic & Story Hardening SKILL
**Date:** 2026-05-10
**Target Epic:** `Phase3_Experience_Mini_Apps_Epics.md`
**Status:** Audit Complete

## Pre-Audit Load Summary

- **Primitives Audited:** `EXP-TRS-003`, `EXP-FBK-001`, `EXP-PRG-002`, `EXP-FBK-004`, `EXP-PER-003`, `EXP-SAF-002`, `EXP-TRG-002`, `EXP-SOC-001`, `EXP-FRC-002`
- **CRITICAL REGISTRY & HALLUCINATION ERRORS CAUGHT:** 
  The BMAD pipeline has suffered a catastrophic mapping collapse in this document. It randomly hallucinated primitive names for existing IDs, and even hallucinated a prefix.
  - `EXP-TRB-003` -> Hallucinated prefix. Must be `EXP-TRS-003` (Reflective Social Proof).
  - `EXP-PRG-001` -> Hallucinated Name. The epic calls this "Discover->Master->Replay", but in the registry, 001 is "Hook Cycle Velocity". `EXP-PRG-002` is actually "Discover->Master->Replay".
  - `EXP-FBK-004` -> Hallucinated Name. The epic calls this "Signature Moment", but the registry dictates it is "Bring the Data Forward".
  - `EXP-SAF-002` -> Hallucinated Name. The epic calls this "Sovereign Control", but the registry dictates it is "Possible-Win Scarcity".
  - `EXP-TRG-002` -> Hallucinated Name. The epic calls this "Kairos / Urgent Optimism", but the registry dictates it is "Hook Cycle Velocity".
  - *Note to Architects: The registry contains duplicate primitive names across families (e.g., "Hook Cycle Velocity" exists as both `EXP-TRG-002` and `EXP-PRG-001`). This bloat must be resolved.*

For this audit, the CBAR engine will evaluate against the **actual registry definitions** of the provided IDs, enforcing the true physics of the platform rather than the hallucinated names.

---

## Epic 1: Webinar Companion Viewer (FR-ERA3-01)

### 1.1 Story: Audience Participation Capture
**Mapped Primitive:** `EXP-TRS-003` (Reflective Social Proof - corrected from TRB)

**Part 1 — The Tension:**
The story dictates that timed prompts appear during high-tension webinar moments. If these interactive UI elements block or obscure the live video feed (the coach's face), it ruins the visceral immersion of the moment.
**Part 2 — The UX Failure Scenario:**
The coach reaches the climax of their pitch. Suddenly, a massive polling modal pops up, covering the coach's face. The audience's emotional connection to the speaker is physically severed by the UI.
**Part 3 — The Resolution Demand:**
The visual hierarchy must prioritize the speaker. The Acceptance Criteria must enforce that all participation prompts (polls, voice reactions) render as non-blocking, ambient UI overlays (e.g., lower-thirds or slide-in drawers) that never obscure the primary video focal point.
**Part 4 — The Downstream Proof:**
This ensures the captured participation data (Story 1.1) doesn't cannibalize the actual viewing experience.
**Verdict: REWRITE REQUIRED**

### 1.2 Story: Rep Mode Delivery Scoring
**Mapped Primitive:** `EXP-FBK-001` (RIM Feedback Discipline)

**Part 1 — The Tension:**
The story generates a scorecard after completing a "slide-by-slide rehearsal." If the user records a 45-minute rehearsal and only receives feedback at the very end, the system violates the 'Immediate' mandate of RIM.
**Part 2 — The UX Failure Scenario:**
The coach finishes 45 minutes of reps. The scorecard says: "You hedged 6 times on Slide 3." The coach has completely forgotten their emotional state and delivery from Slide 3. The feedback is mathematically accurate but cognitively useless.
**Part 3 — The Resolution Demand:**
Feedback must be delivered per-slide. The architecture must evaluate and present the score *instantly* as the coach advances to the next slide, rather than aggregating it into a monolithic report at the end of the session.
**Part 4 — The Downstream Proof:**
Prevents the coach from practicing the wrong habits for 40 minutes straight.
**Verdict: REWRITE REQUIRED**

---

## Epic 2: Challenge Arena & Adaptive Progression (FR-ERA3-11)

### 2.1 Story: Capacity Track Routing & 28-Command Layer
**Mapped Primitive:** `EXP-PRG-002` (Discover -> Master -> Replay - corrected ID)

**Part 1 — The Tension:**
The Adaptive Engine gates progression based on real behavior change (e.g., you can't advance if your score is weak). If a user legitimately struggles to improve their score for 5 days, vertical progression is halted.
**Part 2 — The UX Failure Scenario:**
The user is stuck on "Foundation Day 3" for two straight weeks. Because the calendar doesn't move and the UI doesn't evolve, they feel zero progression (violating Discover->Master->Replay). They assume they are failing and churn.
**Part 3 — The Resolution Demand:**
The Adaptive Engine must implement a "Lateral Progression Fallback." If vertical progression is locked due to low scores, the system must assign lateral variations of the drill. The UI must still show them moving forward on the 28-day path, even if they remain in the "Foundation" conceptual layer.
**Part 4 — The Downstream Proof:**
Allows the Sunday Postcard (Story 2.2) to report on activity volume even if vertical skill hasn't jumped.
**Verdict: REWRITE REQUIRED**

### 2.2 Story: The Sunday Postcard Ritual
**Mapped Primitive:** `EXP-FBK-004` (Bring the Data Forward - corrected from Signature Moment)

**Part 1 — The Tension:**
The story vaguely requests a "personalized reflection." If the reflection only relies on LLM qualitative platitudes ("You sounded great this week!"), it violates `EXP-FBK-004`, which demands surfacing undeniable, cumulative quantitative effort.
**Part 2 — The UX Failure Scenario:**
The user receives a generic generative AI postcard. They don't feel their effort was truly 'seen' by the system, treating it as spam.
**Part 3 — The Resolution Demand:**
The Sunday Postcard MUST explicitly aggregate and visualize hidden telemetry. The Acceptance Criteria must mandate the inclusion of cumulative metrics (e.g., total words spoken, total micro-pauses executed) to weaponize the Sunk Cost Fallacy and prove compounding investment.
**Part 4 — The Downstream Proof:**
Anchors the user for the next week of the Challenge Arena.
**Verdict: REWRITE REQUIRED**

---

## Epic 3: Conscious Editor - Compiler Backstage (FR-ERA3-09)

### 3.2 Story: CMF Media Validation & Operator Review
**Mapped Primitive:** `EXP-SAF-002` (Possible-Win Scarcity - corrected from Sovereign Control)

**Part 1 — The Tension:**
The Conscious Editor allows the coach to audit the CMF video. `EXP-SAF-002` dictates that failure must offer a "Possible Win." If the CMF video has a typo in the AI-generated caption, and the only way to fix it is to reject the video and completely re-record the audio, the win feels impossible.
**Part 2 — The UX Failure Scenario:**
The coach loves the video but sees one misspelled word in the B-roll caption. They realize they have to discard the entire take and re-run the 5-minute NIM pipeline. Frustrated by the lack of modular control, they abandon the export.
**Part 3 — The Resolution Demand:**
The UI must provide modular "Safe Failure" recovery. The Conscious Editor MUST allow the coach to manually edit the raw JSON/text transcript layer in the browser *without* having to re-record the audio or re-run the heavy biometric NIM pipeline.
**Part 4 — The Downstream Proof:**
Guarantees a higher throughput of assets reaching the actual social layer (Epic 4).
**Verdict: REWRITE REQUIRED**

---

## Epic 4: Silent Testimonial Builder & User Cards (FR-ERA3-19)

### 4.2 Story: Prismatic User Card Progression
**Mapped Primitive:** `EXP-SOC-001` (Social Treasures + Group Quests)

**Part 1 — The Tension:**
The story upgrades the user's card to "Prismatic" based on "performance stats and streak count." This violates `EXP-SOC-001`, which strictly states that the highest status rewards *cannot* be earned by solo grinding; they must be gifted by peers.
**Part 2 — The UX Failure Scenario:**
A coach grinds Law28 alone in a closet for 100 days, gets a Prismatic card, and never talks to another human. The ecosystem gains zero viral spread, and the "Social Treasure" has no actual social value.
**Part 3 — The Resolution Demand:**
Solo stats can only unlock up to Platinum tier. The Acceptance Criteria must dictate that unlocking the apex "Prismatic" tier strictly requires peer endorsement (e.g., winning a public debate or receiving X votes from the jury).
**Part 4 — The Downstream Proof:**
Forces the coach to share their artifacts, fueling the Silent Referral engine.
**Verdict: FATAL CONFLICT (Rewrite Required)**

---

## Epic 6: Zero-Config Onboarding Flow (FR-ERA3-10)

### 6.1 Story: The Audit-to-Challenge Conversion
**Mapped Primitive:** `EXP-FRC-002` (Friction-Zero Ability)

**Part 1 — The Tension:**
The story mandates "one obvious action and one meaningful reveal." If the system requires the user to create an account, verify an email, or connect a wallet *before* seeing their audit score, Friction-Zero is violated.
**Part 2 — The UX Failure Scenario:**
The cold lead records the 60-second baseline. The app says: "Great! Create an account to see your score." The user, experiencing bait-and-switch friction, closes the app.
**Part 3 — The Resolution Demand:**
The benchmark teaser MUST be delivered instantly within the Telegram chat UI or the anonymous Mini App session without triggering any registration or auth walls.
**Part 4 — The Downstream Proof:**
Ensures the user experiences the dopamine hit needed to willingly hand over their email for the Lead Magnet layer.
**Verdict: PASS WITH NOTE** *(Ensure no auth walls precede the benchmark reveal).*

---

## Constraint Resolution Manifest

1. **The Ambient Prompt Rule (Story 1.1):** Audience participation prompts during webinars must render as non-blocking UI overlays to protect the visual hierarchy of the speaker.
2. **The Per-Slide Feedback Rule (Story 1.2):** Rehearsal scorecards must be evaluated and presented instantly per-slide, not aggregated at the end of the session.
3. **The Lateral Progression Rule (Story 2.1):** The Adaptive Engine must assign lateral drill variations if vertical progression is blocked by low scores, preventing the UI from stalling and causing churn.
4. **The Telemetry Surfacing Rule (Story 2.2):** The Sunday Postcard must explicitly visualize cumulative behavioral data (e.g., words spoken) rather than relying on qualitative AI summaries.
5. **The Modular Recovery Rule (Story 3.2):** The Conscious Editor must allow coaches to manually correct AI transcription errors without requiring a full audio re-recording or NIM pipeline re-run.
6. **The Peer-Gated Apex Rule (Story 4.2):** The highest progression tier (e.g., Prismatic User Cards) cannot be achieved via solo grinding; it must be mathematically locked behind peer endorsement or debate victories.
7. **The Auth-Free Benchmark Rule (Story 6.1):** Initial onboarding audit results must be delivered instantly without registration or authentication walls.

---
═══════════════════════════════════════════════════════
CBAR AUDIT COMPLETION RECEIPT
═══════════════════════════════════════════════════════
PHASE:                   Phase 3 — Experience Mini Apps
EPIC COUNT:              6
STORY COUNT:             9 (7 sampled for deep audit)
─────────────────────────────────────────────────────
VERDICTS:
  PASS WITH NOTE:        1
  REWRITE REQUIRED:      5
  FATAL CONFLICT:        1
─────────────────────────────────────────────────────
HALLUCINATIONS CAUGHT:   5 catastrophic mapping errors.
  * BMAD fabricated names for existing primitive IDs.
  * The audit overrode the epic text and enforced the
    actual YAML registry definitions.
─────────────────────────────────────────────────────
CASCADE LOCK STATUS:     CLEAN
MANIFEST RULES:          7 canonical mandates produced
─────────────────────────────────────────────────────
TIMESTAMP:               2026-05-10T01:43:10+02:00
═══════════════════════════════════════════════════════
