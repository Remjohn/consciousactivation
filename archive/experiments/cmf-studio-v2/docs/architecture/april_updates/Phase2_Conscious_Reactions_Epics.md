# Conscious Reactions (Phase 2) - Epic Breakdown

**Author:** PM John (BMAD)
**Date:** 2026-05-08
**Project Level:** Module Implementation (PRD-06)
**Target Scale:** 11 Mini App Surfaces & CORE Engine

---

## Overview

This document provides the complete epic and story breakdown for the **Conscious Reactions** module (Phase 2 of Era 3), decomposing the requirements from `PRD_06_Conscious_Reactions.md` and the Experience Orchestration Architecture into implementable, user-value-driven stories. 

**Living Document Notice:** This document is generated via the `*create-epics-and-stories` BMAD workflow. It serves as the definitive structural input for the Era 3 Tech Spec Writing Protocol. It ensures every FastAPI route and Supabase schema defined downstream is anchored in a concrete user story and rigidly governed by Experience Primitive Quality Standards.

---

## Functional Requirements (FR) Inventory

*   **FR-06-01 (Core Reaction Loop):** User receives a briefed topic, records a constrained reaction, and receives a branded output.
*   **FR-06-02 (Biometric Scoring):** System scores conviction, pacing, and hedges via DSPy/NIM.
*   **FR-06-03 (Solo Reaction Mode):** Single-user core loop.
*   **FR-06-04 (Debate with Jury Mode):** Multi-user For/Against reaction chaining.
*   **FR-06-05 (Reaction Duel Mode):** Side-by-side async reaction battle.
*   **FR-06-06 (Audience Jury Role):** Non-speakers can vote and judge.
*   **FR-06-07 (Supervisor Pairing Role):** Soft entry via accountability pairing.
*   **FR-06-08 (Vote Then React Mechanic):** Silent referral staircase from voting to speaking.
*   **FR-06-09 (Redemption Round):** Comeback loop for poor scores.
*   **FR-06-10 (Tierlist Authority):** Voice-driven element ranking.
*   **FR-06-11 (Audience Mirror Quiz):** Answering audience-specific tensions.
*   **FR-06-12 (Blind Rank Reveal):** Pre-context judgment and defense.
*   **FR-06-13 (Alphabet Challenge):** Timed letter-based conceptual recall.
*   **FR-06-14 (Last One Standing):** Sequential option elimination.
*   **FR-06-15 (Authority Quiz):** Escalating stakes pressure ladder.
*   **FR-06-16 (Ranking Quiz Co-Creation):** Collaborative/competitive list sorting.
*   **FR-06-17 (DPA Branding):** Dynamic visual injection based on coach archetype.

---

## Epic 1: The CORE Reaction Engine Foundation
**Goal:** Establish the shared orchestration engine (`FR-ERA3-05-CORE`) that handles topic intake, biometric scoring, and DPA branding. This invisible engine powers all 10 subsequent Mini App modes.

### Story 1.1: Context-Aware Topic Intake
As a Coach, I want to receive a culturally relevant, 15-second voice-briefed topic, so that I don't suffer from blank-page syndrome and know exactly what tension to react to.
**Acceptance Criteria:**
*   **Given** a high-charge topic is selected by SCRE,
*   **When** the Mini App initializes,
*   **Then** the UI displays the `ReactionTopicBrief` payload including the `source_url` and plays the `briefing_audio_path`.
*   **And** the UI must display a burning countdown timer based on an ephemeral TTL (e.g., 24 hours after push notification) to force immediate action.
**Technical Notes:** Pulls from `ReactionTopicBrief` schema. The payload must contain a strict TTL parameter.

**Primitive Quality Constraints (EXP-TRG-002: Hook Cycle Velocity & Contextual Timing):**
*   **Quality Standard (Velocity):** The push notification and topic intake must occur within 24 hours of the news event hitting peak cultural entropy to ensure relevance.
*   **Quality Standard (Curiosity Gap):** The alert copy must omit the conclusion, forcing the coach to open the app to hear the full 15-second briefing.
*   **Anti-Pattern Prevention:** Do not send generic, evergreen topics. Topics must have a `charge_level > 0.7` to prevent centroid, boring reactions.

### Story 1.2: Constrained Voice Recording
As a Coach, I want to record my reaction within a strict time limit, so that my delivery remains concise and high-conviction.
**Acceptance Criteria:**
*   **Given** the topic brief is complete,
*   **When** I press record,
*   **Then** a countdown timer (e.g., 300s) begins, forcing a hard stop if breached.
*   **And** when I stop recording, the UI must optimistically return control instantly, moving me to a loading/scoring state without blocking.
**Technical Notes:** Generates `ReactionArtifact` with `status: processing`. A resilient background worker handles the `sacred-audio` upload with local client-side caching to prevent data loss over weak connections.

**Primitive Quality Constraints (EXP-FRC-003: The B=MAP Friction Audit):**
*   **Quality Standard (Physical Effort):** The entire UI architecture must support a maximum of 2 clicks from the Telegram prompt to active recording (`OneTapRecordCore`).
*   **Quality Standard (Brain Cycles):** The system must not require the user to formulate a headline or opening statement. The topic context is pre-loaded visually.
*   **Anti-Pattern Prevention:** Do not build multi-step web portal logins. Utilize Telegram seamless authorization so the user never sees a login screen.

### Story 1.3: Instant Biometric Scoring Benchmark
As a Coach, I want to receive an immediate score on my delivery (conviction, pacing, hedging), so that I know exactly how authoritative I sounded.
**Acceptance Criteria:**
*   **Given** my reaction is submitted,
*   **When** the NIM pipeline completes processing,
*   **Then** I receive a score card showing conviction metrics within a strict 3-second maximum latency.
**Technical Notes:** Relies on FR61 / `trait_scoring_engine.py`. To achieve the 3-second SLA, the frontend must stream 10-second audio chunks to the NIM pipeline *while* the user is recording. Updates `ReactionArtifact` status to `scored`.

**Primitive Quality Constraints (EXP-FBK-001: RIM Feedback Discipline):**
*   **Quality Standard (Latency SLA):** The backend `scoring_engine` must enforce a maximum 3-second latency on all audio processing. If the AI is too slow, the game is broken.
*   **Quality Standard (Meaning):** The score must explicitly explain *why* the action mattered (e.g., "+1 Resonance on Pacing"), not just a generic vanity metric.
*   **Anti-Pattern Prevention:** Ban delayed, disconnected batch scoring (e.g., weekly emails). The feedback must arrive while the emotional context of the recording is still fresh.

### Story 1.4: Dynamic Whitelabel Experience (DPA)
As a Coach, I want the reaction interface and output to match my specific brand archetype, so that I look like a premium authority.
**Acceptance Criteria:**
*   **Given** I am in the Mini App,
*   **When** the UI renders,
*   **Then** it dynamically applies the `ResolvedPalette` from the `dpa_engine.py` (colors, typography).
**Technical Notes:** Calls `DPAEngine.resolve(coach_id)`.

**Primitive Quality Constraints (EXP-TRS-004: Attractive Things Work Better):**
*   **Quality Standard (Premium Aesthetics):** The visual injection must feel highly curated, using smooth gradients and modern typography that matches the coach's PAD vector.
*   **Anti-Pattern Prevention:** Do not use generic, unbranded gray UI components. The interface itself must act as a Trust Anchor before the coach even speaks.

---

## Epic 2: Core Reaction Formats (Speaker Entry)
**Goal:** Enable coaches to record standalone takes, debate peers, and duel asynchronously using the standalone Mini Apps (`FR-ERA3-05a, 05b, 05c`).

### Story 2.1: Solo Reaction Deployment
As a Coach, I want to record a standalone reaction and extract it as a branded asset, so that I can easily post high-quality content to my audience.
**Acceptance Criteria:**
*   **Given** I complete the CORE loop,
*   **When** I approve the take,
*   **Then** it is evaluated against a biometric threshold. If passed, it is routed to the CMF for glossy extraction (`deployed_to_cmf`). If it fails, the system does NOT deploy it and instead routes me to the Redemption Round.

**Primitive Quality Constraints (EXP-PRG-002: First Major Win-State):**
*   **Quality Standard (Tangible Reward):** The extracted CMF asset (short/meme) must be delivered within 20 minutes to close the loop on their effort.
*   **Anti-Pattern Prevention:** Do not leave the user hanging without a tangible export. The system must automatically package the asset.

### Story 2.2: Debate Mode - Stance Selection & Counter-Take
As a Coach, I want to formally declare myself "For" or "Against" a peer's reaction and record a counter-take, so that I can defend my philosophy and generate social proof.
**Acceptance Criteria:**
*   **Given** I receive a Debate artifact,
*   **When** I tap "Counter-React",
*   **Then** I must select a stance before recording my opposing voice note.
*   **And** the resulting CMF artifact must explicitly render as a split-screen or "VS" visual format to maximize tribal alignment and social stakes.

**Primitive Quality Constraints (EXP-SOC-002: Identity-Driven Social Proof):**
*   **Quality Standard (Tribal Alignment):** The For/Against stance must be visually distinct and permanently bind the user to that argument.
*   **Anti-Pattern Prevention:** Do not allow "neutral" stances. The UI must force a polarized choice to maximize social stakes.

### Story 2.3: Reaction Duel Async Comparison
As a Coach, I want my reaction compared side-by-side with a rival's reaction to the same topic, so that the audience can vote on who held frame better.
**Acceptance Criteria:**
*   **Given** two coaches react to the same duel topic,
*   **When** both artifacts hit `scored` status,
*   **Then** a unified Duel asset is generated allowing audiences to vote.
*   **And** the matchmaking engine must enforce tier-based brackets, only pairing coaches within their same local bracket/tier to ensure safe failure.

**Primitive Quality Constraints (EXP-SOC-004: Collaborative Superpowers):**
*   **Quality Standard (Async Safety):** The duel must be asynchronous to prevent the live anxiety of a real-time debate, allowing the coach to record in their own controlled environment.

---

## Epic 3: Social Routing & Silent Referral (Low-Friction Entry)
**Goal:** Enable users who aren't ready to speak to participate, judge, and eventually convert. These are features of the CORE engine.

### Story 3.1: Audience Jury Voting
As an Audience Member, I want to vote on reactions without recording audio myself, so that I can participate with zero performance pressure.
**Acceptance Criteria:**
*   **Given** a Debate or Duel is shared to me,
*   **When** I listen to the takes,
*   **Then** I can cast a vote for the strongest argument in Telegram.

**Primitive Quality Constraints (EXP-FRC-002: Friction-Zero Ability):**
*   **Quality Standard (No Registration):** Voting must occur via native Telegram inline buttons without requiring the user to open a Mini App or register an account.

### Story 3.2: Vote Then React Escalation
As a Voter, I want to be prompted to record my own take after I vote, so that my passive engagement translates into active ecosystem participation.
**Acceptance Criteria:**
*   **Given** I cast a vote as an Audience Jury member,
*   **When** the vote is registered,
*   **Then** a modal appears offering me the chance to defend my vote.
*   **And** the UI copy must explicitly tether to my chosen stance seamlessly (e.g., "You voted for X. Hit record to tell the jury why you're right.").

**Primitive Quality Constraints (EXP-TRG-005: External to Internal Trigger Mapping):**
*   **Quality Standard (Staircase of Commitment):** The prompt to speak must only arrive *after* the user has invested the small effort of voting, leveraging consistency bias.

### Story 3.3: Supervisor Accountability Pairing
As a Friend/Mentor, I want to be assigned as an accountability witness for a coach, so that I receive notifications of their progress and can offer support.
**Acceptance Criteria:**
*   **Given** a coach invites me,
*   **When** they record a reaction,
*   **Then** I receive a summary of their biometric improvements.

**Primitive Quality Constraints (EXP-SOC-005: Recruit Your Allies):**
*   **Quality Standard (Soft Entry):** The notifications must act as a soft, continuous demonstration of the platform's value to the supervisor, acting as a slow-burn acquisition channel.

---

## Epic 4: Safe Failure & Progression
**Goal:** Prevent churn from bad scores by turning failure into structured coaching (CORE feature).

### Story 4.1: Redemption Round Trigger
As a Coach who received a poor biometric score, I want immediate coaching cues and a chance to try again, so that I don't feel humiliated by the system.
**Acceptance Criteria:**
*   **Given** my reaction receives a `status: redemption_required`,
*   **When** the score is revealed,
*   **Then** I am presented with 2 specific vocal cues and a button to re-record.

**Primitive Quality Constraints (EXP-SAF-004: Richter Rescue):**
*   **Quality Standard (Behavioral Forgiveness):** The system must intercept a terrible score before it reaches the social layer and frame the failure as a private diagnostic baseline.
*   **Anti-Pattern Prevention:** Do not publicly shame low scores. The Redemption Round must feel like a supportive coach stepping in.

---

## Epic 5: Ranking & Sorting Content Experiences
**Goal:** Provide high-velocity TikTok-style ranking games to test authority. These are standalone Mini Apps (`FR-ERA3-05d, 05f, 05h, 05j`).

### Story 5.1: Tierlist Authority Verbal Ranking
As a Coach, I want to rank elements (S, A, B, C) verbally and have the UI update, so that I can produce engaging visual content without manual editing.
**Acceptance Criteria:**
*   **Given** a set of 5 elements,
*   **When** I say "[Element] goes in S Tier",
*   **Then** the UI visually moves the element to the S row.

**Primitive Quality Constraints (EXP-FBK-004: Signature Moment):**
*   **Quality Standard (Visual Payoff):** The snap of the element into the tier row must be visually satisfying, providing immediate micro-feedback during the recording.

### Story 5.2: Blind Rank Reveal Defense
As a Coach, I want to be forced to rank items one at a time before seeing the full list, so that my genuine instincts are captured on camera.
**Acceptance Criteria:**
*   **Given** an unknown list of 5 items,
*   **When** Item 1 appears, I must assign it a slot (1-5) permanently before Item 2 is revealed.

**Primitive Quality Constraints (EXP-SAF-002: Practical Play and Safe Failure):**
*   **Quality Standard (Engineered Tension):** The humor and tension comes from the inability to change past choices, making the failure state highly entertaining rather than damaging.

### Story 5.3: Last One Standing Elimination
As a Coach, I want to eliminate options sequentially until one remains, so that I build natural tension toward my ultimate conclusion.
**Acceptance Criteria:**
*   **Given** 8 starting options,
*   **When** I speak, I must eliminate one option per 10-second round.

**Primitive Quality Constraints (EXP-PRG-004: Long Loops):**
*   **Quality Standard (Pacing Escalation):** The visual timer must become more aggressive as the options dwindle, enforcing a faster cadence.

### Story 5.4: Ranking Quiz Co-Creation
As a Coach, I want to challenge my audience to reorder my ranking, so that we generate high-volume comment interactions.
**Acceptance Criteria:**
*   **Given** I publish a completed Tierlist,
*   **When** a user views it, they can drag-and-drop to propose their own order.

**Primitive Quality Constraints (EXP-SOC-001: Social Treasures + Group Quests):**
*   **Quality Standard (Interactive Dispute):** The ability for the audience to literally alter the visual layout creates a sense of co-authorship and dispute, driving engagement far higher than passive watching.

---

## Epic 6: High-Pressure Recall Content Experiences
**Goal:** Test the coach's ability to retrieve knowledge instantly under stress (`FR-ERA3-05e, 05g, 05i`).

### Story 6.1: Alphabet Challenge Speed Run
As a Coach, I want to race a clock answering questions that start with specific letters, so that I can demonstrate raw domain mastery.
**Acceptance Criteria:**
*   **Given** the timer starts,
*   **When** a letter appears, I must speak a valid industry term within 3 seconds.
*   **And** this 3-second timer validation MUST be evaluated client-side (frontend timestamping) to ensure network latency does not unfairly fail me.

**Primitive Quality Constraints (EXP-FRC-006: Poka-Yoke):**
*   **Quality Standard (Constraint as Focus):** The extreme constraint removes the burden of structuring a long thought, forcing pure instinctual retrieval.

### Story 6.2: Authority Quiz Pressure Ladder
As a Coach, I want to answer escalating-stakes questions like a game show, so that the audience feels the tension of my performance.
**Acceptance Criteria:**
*   **Given** I answer correctly,
*   **When** the next question appears, the visual intensity increases.

**Primitive Quality Constraints (EXP-TRS-003: Visceral Hooking):**
*   **Quality Standard (Ambient Feedback):** The DPA background mood token must darken or intensify with each level, mapping the visual tension to the difficulty.

### Story 6.3: Audience Mirror Quiz
As a Coach, I want to answer questions derived directly from my audience's `tribe_soul` data, so that they feel deeply understood.
**Acceptance Criteria:**
*   **Given** the system reads my CMM (Cultural Memory Map),
*   **When** the quiz generates, it asks me to resolve specific tensions my audience has previously complained about.

**Primitive Quality Constraints (EXP-PER-003: Tailoring & Suggestion):**
*   **Quality Standard (Identity Reflection):** The questions must not be generic; they must cite actual verbiage extracted from the coach's historical CRM/audience data to prove deep system intelligence.

---

## Canonical CBAR Mandates

1. **The Ephemeral Decay Mandate (Story 1.1):** Topic intake briefs must contain a 24-hour TTL (Time-to-Live). Topics expire to force Hook Cycle Velocity; they are not evergreen.
2. **The Background Upload Rule (Story 1.2):** UI state must return to the user instantly upon concluding a recording. Audio payloads must upload via resilient background client workers.
3. **The Streaming Audio SLA (Story 1.3):** To hit the 3-second RIM feedback SLA, the client must stream audio chunks to the NIM processing pipeline *during* the recording, rather than waiting until the end to begin transcription.
4. **The Earned Export Gate (Story 2.1):** CMF glossy video generation is a reward, not a default. It must be gated behind a passing biometric threshold to preserve platform status. Sub-threshold takes trigger Redemption mode.
5. **The Visual Adversary Rule (Story 2.2):** Debate artifacts must explicitly render as split-screen / VS formats. A debate take cannot visually resemble a solo take.
6. **The Bracket Matchmaking Rule (Story 2.3):** Asynchronous duels must pair coaches within the same progression tier/bracket to prevent blowout humiliation and preserve upward mobility.
7. **The Client-Side Timing Rule (Story 6.1):** High-velocity constraints (like 3-second answers) must timestamp and validate on the client device. Server-side latency must never penalize the user.

---

## FR Coverage Matrix

| FR ID | Feature | Mapped Epic & Story |
| :--- | :--- | :--- |
| FR-06-01 | Core Reaction Loop | Epic 1 (Stories 1.1, 1.2) |
| FR-06-02 | Biometric Scoring | Epic 1 (Story 1.3) |
| FR-06-03 | Solo Reaction Mode | Epic 2 (Story 2.1) |
| FR-06-04 | Debate with Jury Mode | Epic 2 (Story 2.2) |
| FR-06-05 | Reaction Duel Mode | Epic 2 (Story 2.3) |
| FR-06-06 | Audience Jury Role | Epic 3 (Story 3.1) |
| FR-06-07 | Supervisor Pairing Role| Epic 3 (Story 3.3) |
| FR-06-08 | Vote Then React | Epic 3 (Story 3.2) |
| FR-06-09 | Redemption Round | Epic 4 (Story 4.1) |
| FR-06-10 | Tierlist Authority | Epic 5 (Story 5.1) |
| FR-06-11 | Audience Mirror Quiz | Epic 6 (Story 6.3) |
| FR-06-12 | Blind Rank Reveal | Epic 5 (Story 5.2) |
| FR-06-13 | Alphabet Challenge | Epic 6 (Story 6.1) |
| FR-06-14 | Last One Standing | Epic 5 (Story 5.3) |
| FR-06-15 | Authority Quiz | Epic 6 (Story 6.2) |
| FR-06-16 | Ranking Quiz Co-Creation | Epic 5 (Story 5.4) |
| FR-06-17 | DPA Branding | Epic 1 (Story 1.4) |
