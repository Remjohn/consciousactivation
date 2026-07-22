# CBAR Audit Manifest: Phase 4 Pipelines & Engines

**Author:** CBAR Epic & Story Hardening SKILL
**Date:** 2026-05-10
**Target Epic:** `Phase4_Pipelines_and_Engines_Epics.md`
**Status:** Audit Complete

## Pre-Audit Load Summary

- **Primitives Audited:** `EXP-PER-003`, `EXP-TRS-004`, `EXP-PRG-001`, `EXP-FRC-006`, `EXP-FBK-001`, `EXP-TRS-003`, `EXP-PRG-004`
- **CRITICAL REGISTRY & HALLUCINATION ERRORS CAUGHT:** 
  The mapping collapse observed in Phase 3 is fully present in Phase 4. The BMAD pipeline hallucinates both primitive names and prefixes.
  - `EXP-TRB-004` -> Hallucinated prefix AND name. The epic calls it "Attractive Things Work Better," but the registry dictates it is `EXP-TRS-004` (Epic Meaning Framing).
  - `EXP-PRG-001` -> Hallucinated name. The epic calls it "Discover->Master->Replay," but the registry dictates it is "Hook Cycle Velocity."
  - `EXP-TRB-003` -> Hallucinated prefix AND name. The epic calls it "Visceral Hooking," but the registry dictates it is `EXP-TRS-003` (Reflective Social Proof).
  - `EXP-PRG-004` -> Hallucinated name. The epic calls it "Flow Through Grinding," but the registry dictates it is "Long Loops for Habit Formation."

For this audit, the CBAR engine will evaluate against the **actual registry definitions** of the provided IDs, enforcing the true physics of the platform rather than the hallucinated names.

---

## Epic 1: AFFiNE Studio Block Orchestration (FR-ERA3-07)

### 1.1 Story: Operator Intervention and Dashboard Review
**Mapped Primitive:** `EXP-PER-003` (Tailoring & Suggestion)

**Part 1 — The Tension:**
The story dictates a "one-click Intercept Button" for operators. If the system surfaces a red flag but provides zero contextual intelligence as to *why* the user failed, the operator cannot tailor their intercept message.
**Part 2 — The UX Failure Scenario:**
The dashboard flags a user for "Low Confidence." The operator clicks intercept and sends: "Hey, saw you struggled, keep going!" The client realizes the coach is just reading an automated alert and didn't actually listen to their audio. The illusion of deep personalization is shattered, and trust is broken.
**Part 3 — The Resolution Demand:**
The `Red Flag Feed` must explicitly include a qualitative transcription excerpt or diagnostic summary of exactly *why* the flag was raised (e.g., "Client paused for 4 seconds after mentioning pricing"). The UI must enforce that the operator reviews this excerpt *before* the intercept voice recorder unlocks, ensuring flawless tailoring.
**Part 4 — The Downstream Proof:**
This preserves the ultra-premium "Coach OS" illusion, justifying the $99/mo continuity tier.
**Verdict: REWRITE REQUIRED**

---

## Epic 2: CMF Arc-Governed Rendering (FR-ERA3-12)

### 2.1 Story: Narrative Geometry Translation
**Mapped Primitive:** `EXP-TRS-004` (Epic Meaning Framing - corrected from TRB)

**Part 1 — The Tension:**
The CMF pipeline translates meaning into specific beat clusters. If the rendering logic optimizes purely for "clean, functional" video layouts, it fails the "Epic Meaning / Crusade Narrative" mandate of `EXP-TRS-004`.
**Part 2 — The UX Failure Scenario:**
A coach records a passionate, paradigm-shifting defense of their industry. The CMF renders it as a bland, brightly lit, corporate SaaS tutorial video with generic stock music. The "Crusade" framing is lost, the artifact feels cheap, and the coach refuses to publish it.
**Part 3 — The Resolution Demand:**
The `Narrative Rendering Model` must explicitly map the `Coalition Script Spine` to Epic Meaning visual grammar. The Acceptance Criteria must dictate that CMF outputs utilize high-contrast lighting, cinematic pacing, and intense sonic beds to ensure the artifact looks like a high-stakes manifesto, not a corporate explainer.
**Part 4 — The Downstream Proof:**
This gives the user the requisite social capital to share the artifact externally.
**Verdict: REWRITE REQUIRED**

---

## Epic 3: Four-Surface Async Skill Ladder (FR-ERA3-13)

### 3.1 Story: Voice-First Asynchronous Progression
**Mapped Primitive:** `EXP-PRG-001` (Hook Cycle Velocity - corrected)

**Part 1 — The Tension:**
The backend routes practice into four different surfaces (Law28, Webinar, Networking, Social). If the async routing logic relies on batch processing (e.g., moving the data to the Webinar bucket overnight), Hook Cycle Velocity is broken.
**Part 2 — The UX Failure Scenario:**
The user submits a voice note. The system says "Processing..." and promises to compile it later. The user receives no immediate feedback. The neurological link between the action and the reward is severed, and they do not return the next day.
**Part 3 — The Resolution Demand:**
The `ExperienceStatePacket` routing MUST be executed inline. The architecture must guarantee that the user is returned to the next logical step (the reward, the scorecard, or the rebuttal prompt) instantly (< 3 seconds), regardless of which of the four complex backend surfaces they just interacted with.
**Part 4 — The Downstream Proof:**
This allows the CBCS Four-Engine Runtime to update state dynamically during a single session.
**Verdict: REWRITE REQUIRED**

---

## Epic 4: Trigger-First Execution Guard (FR-ERA3-15)

### 4.1 Story: The Blank-Page Prevention Block
**Mapped Primitive:** `EXP-FRC-006` (Poka-Yoke / Constraint as Focus)

**Part 1 — The Tension:**
The system rejects content generation without an authentic reaction. If the Execution Guard simply throws a static "Error: No reaction found" alert, this is a dumb wall (Friction), not a true Poka-Yoke (which intuitively guides the user to the correct behavior).
**Part 2 — The UX Failure Scenario:**
The coach clicks "Generate LinkedIn Post" in AFFiNE. The system says "Blocked: Authenticated Source Required." The coach doesn't know how to authenticate a source, gets frustrated, and assumes the app is broken.
**Part 3 — The Resolution Demand:**
The Execution Guard must transform the hard block into a frictionless path to compliance. When generation is blocked, the UI must *instantly* pop up the Telegram Voice recording modal with a specific, provocative prompt derived from their initial intent (e.g., "Tell me why your competitors are wrong about this").
**Part 4 — The Downstream Proof:**
The block becomes the trigger, feeding the Archetype Container Runtime immediately.
**Verdict: REWRITE REQUIRED**

---

## Epic 5: Archetype Container Runtime (FR-ERA3-16)

### 5.1 Story: Psychological Container Formatting
**Mapped Primitive:** `EXP-FBK-001` (RIM Feedback Discipline)

**Part 1 — The Tension:**
The system generates a container and passes it to the Anti-Centroid Validator. If the Validator flags the take as "generic sludge" but fails to provide specific RIM feedback, the coach cannot improve.
**Part 2 — The UX Failure Scenario:**
The coach's take is rejected. The system responds: "Your reaction is too generic. Try again." The coach doesn't know what specific part of their 3-minute recording failed the algorithm. They feel judged by a black box and churn.
**Part 3 — The Resolution Demand:**
The `CCFRoutingRecommendation` failure state MUST be actionable. The response payload must return the exact transcript sentences that triggered the centroid collapse, along with specific coaching feedback (e.g., "Your stance on X matches 90% of the industry. Inject a specific client anecdote here to pass the gate").
**Part 4 — The Downstream Proof:**
This enables the Safe Failure / Redemption Round mechanics to function properly.
**Verdict: REWRITE REQUIRED**

---

## Epic 6: Voice Prompt Engine (FR-ERA3-17)

### 6.1 Story: Emotional Job Routing
**Mapped Primitive:** `EXP-TRS-003` (Reflective Social Proof - corrected from TRB)

**Part 1 — The Tension:**
The voice engine dynamically selects an emotional job (Orient, Celebrate, etc.). If the backend relies on a cheap, robotic TTS model to deliver a "Celebrate" job, it generates zero Reflective Social Proof because the user feels embarrassed by the low fidelity.
**Part 2 — The UX Failure Scenario:**
The coach achieves an Epic Win, and the system delivers a congratulations message using a generic, robotic Siri-like voice. The coach cringes. The premium illusion of the platform is destroyed, and they definitely do not share their victory.
**Part 3 — The Resolution Demand:**
The `VoicePromptPacket` MUST enforce strict sonic quality gates. It must mandate the use of the premium, latency-optimized `ConsciousVoice` TTS model (or pre-recorded human coach audio) for all emotional jobs. The sonic delivery must be elite enough that the user is proud to be associated with it.
**Part 4 — The Downstream Proof:**
Ensures the system's voice is trusted enough to deliver the CBCS feedback payloads.
**Verdict: REWRITE REQUIRED**

---

## Epic 7: CBCS Four-Engine Runtime (FR-ERA3-18)

### 7.1 Story: Continuous Voice Evidence Routing
**Mapped Primitive:** `EXP-PRG-004` (Long Loops for Habit Formation - corrected)

**Part 1 — The Tension:**
The engine extracts scores and updates tomorrow's drill (the short loop). If the system only ever focuses on modifying tomorrow's drill, the macro-progression (Long Loop) remains invisible, violating `EXP-PRG-004`.
**Part 2 — The UX Failure Scenario:**
The user fails a drill. The Diagnostic Engine accurately downgrades their capacity track, making tomorrow's drill easier. But the user only sees that they are "going backward." They lose the Long Loop perspective and churn out of shame.
**Part 3 — The Resolution Demand:**
When the Diagnostic Engine downgrades a capacity track or assigns an easier ritual, the `Relationship Engine` MUST intercept the notification and contextualize it against the Long Loop. The UI must explicitly frame the downgrade positively (e.g., "We are stepping back to solidify your pause architecture, but you are still up 20% over the last 14 days").
**Part 4 — The Downstream Proof:**
Protects retention by transforming a local failure into a strategic pause.
**Verdict: REWRITE REQUIRED**

---

## Constraint Resolution Manifest

1. **The Intelligence-Gated Intercept Rule (Story 1.1):** Operators cannot execute an intercept without first reviewing the specific diagnostic excerpt that triggered the red flag, ensuring flawless tailoring.
2. **The Cinematic Meaning Rule (Story 2.1):** The CMF rendering engine must map scripts to high-contrast, intense visual grammar to preserve the Epic Meaning/Crusade narrative, banning flat "corporate SaaS" aesthetic outputs.
3. **The Inline Routing SLA (Story 3.1):** Async routing across the four backend surfaces must execute inline (< 3 seconds) to preserve Hook Cycle Velocity; batched or delayed routing is banned.
4. **The Frictionless Block Rule (Story 4.1):** The execution guard must not display static error walls. A blocked generation request must instantly trigger a voice recording modal pre-loaded with a provocative prompt.
5. **The Actionable Rejection Rule (Story 5.1):** Anti-Centroid Validator rejections must highlight the exact transcript sentences that failed and provide a specific, actionable fix.
6. **The Sonic Prestige Rule (Story 6.1):** All dynamic voice prompts must pass through the premium `ConsciousVoice` TTS model; generic robotic TTS is strictly banned as it destroys Reflective Social Proof.
7. **The Long Loop Framing Rule (Story 7.1):** Any algorithm-driven downgrade in difficulty must be explicitly framed by the Relationship Engine against the user's positive 30-day macro trend to prevent shame-based churn.

---
═══════════════════════════════════════════════════════
CBAR AUDIT COMPLETION RECEIPT
═══════════════════════════════════════════════════════
PHASE:                   Phase 4 — Pipelines & Engines
EPIC COUNT:              7
STORY COUNT:             7 (100% audited)
─────────────────────────────────────────────────────
VERDICTS:
  PASS WITH NOTE:        0
  REWRITE REQUIRED:      7
  FATAL CONFLICT:        0
─────────────────────────────────────────────────────
HALLUCINATIONS CAUGHT:   4 catastrophic mapping errors.
  * BMAD fabricated names and prefixes across 4 primitives.
  * Audit overrode Epic text, enforcing true YAML physics.
─────────────────────────────────────────────────────
CASCADE LOCK STATUS:     CLEAN
MANIFEST RULES:          7 canonical backend mandates
─────────────────────────────────────────────────────
TIMESTAMP:               2026-05-10T01:54:10+02:00
═══════════════════════════════════════════════════════
