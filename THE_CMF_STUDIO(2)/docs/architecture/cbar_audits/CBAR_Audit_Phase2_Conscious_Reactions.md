# CBAR Audit Manifest: Phase 2 Conscious Reactions

**Author:** CBAR Epic & Story Hardening SKILL
**Date:** 2026-05-10
**Target Epic:** `Phase2_Conscious_Reactions_Epics.md`
**Status:** Audit Complete

## Pre-Audit Load Summary

- **Primitives Audited:** `EXP-TRG-002`, `EXP-FRC-003`, `EXP-FBK-001`, `EXP-PRG-002`, `EXP-SOC-002`, `EXP-SOC-004`, `EXP-FRC-002`, `EXP-TRG-005`, `EXP-FRC-006`, `EXP-PER-003`
  - *Note: Multiple primitive hallucination errors detected in the source document. The following prefixes were hallucinated by the BMAD pipeline and do not exist in the registry:*
    - `EXP-TRB-004` & `EXP-TRB-003` -> (Should be `EXP-TRS`, Trust & Branding)
    - `EXP-SFR-004` & `EXP-SFR-002` -> (Should be `EXP-SAF`, Safe Failure & Recovery)
    - `EXP-SOC-007` -> (Does not exist. The SOC family currently terminates at 005)
- **PRD Modules Loaded:** `PRD_06_Conscious_Reactions.md` (Assumed context)
- **Protocol Evaluated:** `ERA3_Epic_and_Story_Writing_Protocol.md`

---

## Epic 1: The CORE Reaction Engine Foundation

### 1.1 Story: Context-Aware Topic Intake
**Mapped Primitive:** `EXP-TRG-002` (Hook Cycle Velocity)

**Part 1 — The Tension:**
The story sends a push notification when the topic hits peak entropy, but omits an urgency constraint on the intake. If the user can sit on the topic for 3 days before reacting, the Hook Cycle Velocity is broken, and the interaction devolves from a rapid daily habit loop into an asynchronous chore.
**Part 2 — The UX Failure Scenario:**
The user opens the app 48 hours later. The cultural relevance of the topic has faded, removing intrinsic urgency. They experience "blank page syndrome" despite the brief and abandon the recording.
**Part 3 — The Resolution Demand:**
`EXP-TRG-002` demands velocity compression. The architectural resolution is that the `ReactionTopicBrief` payload must contain an ephemeral TTL (Time-to-Live) parameter (e.g., expires 24 hours after the push notification). The UI must display a burning countdown timer to force immediate action.
**Part 4 — The Downstream Proof:**
Story 1.2 inherits this urgency; the strict 300s recording limit makes logical sense to the user because the topic itself is framed as highly ephemeral and urgent.
**Verdict: REWRITE REQUIRED**

### 1.2 Story: Constrained Voice Recording
**Mapped Primitive:** `EXP-FRC-003` (The B=MAP Friction Audit)

**Part 1 — The Tension:**
The drafted story triggers a 300s timer and "stores raw audio to sacred-audio bucket." If the frontend blocks the UI waiting for a 20MB WAV file to upload over a 4G connection before returning control to the user, this introduces massive physical wait friction.
**Part 2 — The UX Failure Scenario:**
The user hits stop and watches a spinning "Uploading..." wheel for 14 seconds. They tab out of Telegram to check an email. The mobile OS suspends the background process, the upload fails, and the take is lost. Huge friction penalty and trust loss.
**Part 3 — The Resolution Demand:**
`EXP-FRC-003` demands zero physical wait effort. The UI must optimistically return control to the user instantly after hitting stop, placing them into a loading/scoring state while a resilient background worker handles the `sacred-audio` upload with local client-side caching to prevent data loss.
**Part 4 — The Downstream Proof:**
Story 1.3 relies on this, as the user must feel they are instantly moving into the scoring phase without being bottlenecked by file transfer physics.
**Verdict: REWRITE REQUIRED**

### 1.3 Story: Instant Biometric Scoring Benchmark
**Mapped Primitive:** `EXP-FBK-001` (RIM Feedback Discipline)

**Part 1 — The Tension:**
The story relies on the NIM pipeline to return scores. `EXP-FBK-001` demands a strict 3-second maximum latency for "Immediate" feedback. However, transcribing a 300-second audio clip and running MoE biometric analysis on it will physically take longer than 3 seconds on standard GPU clusters if processed linearly at the end of the recording.
**Part 2 — The UX Failure Scenario:**
The user finishes a 5-minute reaction. The system takes 35 seconds to transcribe and score. The 'Immediate' mandate of RIM is shattered. The user leaves the app before the score arrives.
**Part 3 — The Resolution Demand:**
Backend processing physics conflict with the psychological immediacy mandate. The resolution requires an asynchronous chunking architecture. The frontend must stream 10-second audio chunks to the NIM pipeline *while* the user is recording, allowing the final score to be assembled and delivered <3 seconds after they hit stop. *(UNVERIFIED ASSUMPTION: NIM pipeline and Telegram Mini App WebRTC APIs support streaming chunk ingestion).*
**Part 4 — The Downstream Proof:**
Ensures the user stays in the app to receive the DPA output (Story 1.4).
**Verdict: FATAL CONFLICT (Rewrite Required)**

---

## Epic 2: Core Reaction Formats (Speaker Entry)

### 2.1 Story: Solo Reaction Deployment
**Mapped Primitive:** `EXP-PRG-002` (First Major Win-State)

**Part 1 — The Tension:**
The drafted story automatically routes the approved take to the CMF for extraction. But `EXP-PRG-002` dictates that major win-states (like a glossy CMF export) must not happen automatically for every minor or poor action; they require a hard-won victory.
**Part 2 — The UX Failure Scenario:**
The user records a low-effort, heavily hedged reaction. The system gives them a bad score, but still generates a glossy CMF video. The "reward" feels unearned and patronizing, cheapening the platform's prestige and breaking the Fiero loop.
**Part 3 — The Resolution Demand:**
CMF extraction must be gated behind a biometric threshold. If the take scores below the threshold, the system must NOT deploy it to CMF, but instead route the user to the Redemption Round. CMF generation is a reward for quality, not an entitlement for participation.
**Part 4 — The Downstream Proof:**
This preserves the social capital economy (Story 2.2) by ensuring only high-quality takes enter the public arena.
**Verdict: REWRITE REQUIRED**

### 2.2 Story: Debate Mode - Stance Selection
**Mapped Primitive:** `EXP-SOC-002` (Social Capital and Self-Esteem Economy)

**Part 1 — The Tension:**
The story allows selecting a stance before recording. But `EXP-SOC-002` requires verifiable status flexing. If the stance is just a hidden database flag, it generates no social capital when shared externally.
**Part 2 — The UX Failure Scenario:**
The user records an amazing counter-take, but when the CMF artifact is shared on LinkedIn, it looks exactly like a solo take. The audience doesn't know it's a debate or who they are debating. The user gains no adversarial status.
**Part 3 — The Resolution Demand:**
The CMF export architecture must explicitly inject the adversarial context. The Acceptance Criteria must mandate that Debate artifacts are rendered as a split-screen or "VS" visual artifact (the opponent's claim vs the user's counter-claim) to maximize tribal alignment and social stakes.
**Part 4 — The Downstream Proof:**
This directly feeds the duel voting mechanics (Story 2.3).
**Verdict: REWRITE REQUIRED**

### 2.3 Story: Reaction Duel Async Comparison
**Mapped Primitive:** `EXP-SOC-004` (Balanced Social Status Architecture)

**Part 1 — The Tension:**
The story generates a duel for audiences to vote. But if matchmaking is purely random, a veteran coach with huge audience gravity will be matched against a brand-new coach.
**Part 2 — The UX Failure Scenario:**
The new coach gets humiliated in public, losing the vote 99% to 1%. This violates the "Upward Mobility Guarantee" and "Safe Failure" principles, causing permanent churn.
**Part 3 — The Resolution Demand:**
`EXP-SOC-004` demands localized jurisdictions. The orchestration engine must enforce tier-based matchmaking for duels. Users can only be matched against peers in their same local bracket/tier to ensure the outcome is genuinely competitive and the failure is safe.
**Part 4 — The Downstream Proof:**
Ensures the jury voting (Story 3.1) isn't biased by massive status disparities.
**Verdict: REWRITE REQUIRED**

---

## Epic 3: Social Routing & Silent Referral

### 3.2 Story: Vote Then React Escalation
**Mapped Primitive:** `EXP-TRG-005` (First Major Win-State / Trigger Mapping)

**Part 1 — The Tension:**
The story prompts a user to "Defend my vote" immediately after clicking a voting button. Asking for a high-friction action (recording voice) immediately following a low-friction action (pressing an inline button) creates an ability/motivation mismatch.
**Part 2 — The UX Failure Scenario:**
The modal appears instantly after the vote. The user, who is in a passive scrolling state (System 1), feels ambushed by the request to perform (System 2). They dismiss the modal as spam.
**Part 3 — The Resolution Demand:**
The prompt must leverage consistency bias smoothly. The UI must transition seamlessly without opening a disruptive new window. It should frame the request not as a generic "Record a take," but specifically tethered to the side they just chose: "You voted for X. Hit record to tell the jury why you're right."
**Part 4 — The Downstream Proof:**
Provides the funnel for acquiring new speakers organically.
**Verdict: PASS WITH NOTE** *(Ensure UI copy explicitly tethers to their chosen stance).*

---

## Epic 6: High-Pressure Recall Content Experiences

### 6.1 Story: Alphabet Challenge Speed Run
**Mapped Primitive:** `EXP-FRC-006` (Poka-Yoke / Constraint as Focus)

**Part 1 — The Tension:**
The story demands the user speaks a valid term within 3 seconds. However, network latency for streaming audio to the STT engine can easily consume 1-2 seconds of that window.
**Part 2 — The UX Failure Scenario:**
The user answers correctly in 2 seconds, but network lag causes the system to register it at 4 seconds. The user is penalized for backend physics. The feeling of unfairness destroys trust and the user quits.
**Part 3 — The Resolution Demand:**
To enforce a fair Poka-Yoke constraint, the 3-second timer validation MUST be evaluated client-side (frontend timestamping) rather than server-side, preventing network latency from unfairly failing the user.
**Part 4 — The Downstream Proof:**
Protects the integrity of the pressure ladder in Story 6.2.
**Verdict: REWRITE REQUIRED**

---

## Constraint Resolution Manifest

1. **The Ephemeral Decay Mandate (Story 1.1):** Topic intake briefs must contain a 24-hour TTL (Time-to-Live). Topics expire to force Hook Cycle Velocity; they are not evergreen.
2. **The Background Upload Rule (Story 1.2):** UI state must return to the user instantly upon concluding a recording. Audio payloads must upload via resilient background client workers.
3. **The Streaming Audio SLA (Story 1.3):** To hit the 3-second RIM feedback SLA, the client must stream audio chunks to the NIM processing pipeline *during* the recording, rather than waiting until the end to begin transcription.
4. **The Earned Export Gate (Story 2.1):** CMF glossy video generation is a reward, not a default. It must be gated behind a passing biometric threshold to preserve platform status. Sub-threshold takes trigger Redemption mode.
5. **The Visual Adversary Rule (Story 2.2):** Debate artifacts must explicitly render as split-screen / VS formats. A debate take cannot visually resemble a solo take.
6. **The Bracket Matchmaking Rule (Story 2.3):** Asynchronous duels must pair coaches within the same progression tier/bracket to prevent blowout humiliation and preserve upward mobility.
7. **The Client-Side Timing Rule (Story 6.1):** High-velocity constraints (like 3-second answers) must timestamp and validate on the client device. Server-side latency must never penalize the user.

---
═══════════════════════════════════════════════════════
CBAR AUDIT COMPLETION RECEIPT
═══════════════════════════════════════════════════════
PHASE:                   Phase 2 — Conscious Reactions
EPIC COUNT:              6
STORY COUNT:             17 (8 sampled for deep audit)
─────────────────────────────────────────────────────
VERDICTS:
  PASS WITH NOTE:        1
  REWRITE REQUIRED:      6
  FATAL CONFLICT:        1
─────────────────────────────────────────────────────
PRIMITIVES AUDITED:      EXP-TRG-002, EXP-FRC-003, EXP-FBK-001, EXP-PRG-002, EXP-SOC-002, EXP-SOC-004, EXP-FRC-006
HALLUCINATIONS CAUGHT:   5 (TRB-004, TRB-003, SFR-004, SFR-002, SOC-007)
─────────────────────────────────────────────────────
UNVERIFIED ASSUMPTIONS:  1 — [NIM / WebRTC Streaming Ingestion]
CASCADE LOCK STATUS:     CLEAN
MANIFEST RULES:          7 canonical mandates produced
─────────────────────────────────────────────────────
TIMESTAMP:               2026-05-10T01:31:40+02:00
═══════════════════════════════════════════════════════
