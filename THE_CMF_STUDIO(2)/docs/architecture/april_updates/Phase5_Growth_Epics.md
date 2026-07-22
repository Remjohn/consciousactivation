# Growth (Phase 5) - Epic Breakdown

**Author:** PM John (BMAD)
**Date:** 2026-05-08
**Hardened:** 2026-05-11 (CBAR Audit Resolution Applied)
**Project Level:** Phase 5 Growth
**Target Scale:** 3 Core Growth and Outbound Engines

---

## Overview

This document provides the complete epic and story breakdown for the **Phase 5 Growth** module. It implements the aggressive commercial architecture defined in PRD-09 (Silent Referral & OFO) and PRD-01. The strategy enforces the rule that commercial growth must come from "proof, participation, and trust transfer," not from generic SaaS explanation or explicit affiliate begging.

**Living Document Notice:** This document is generated via the `*create-epics-and-stories` BMAD workflow. It serves as the definitive structural input for the Era 3 Tech Spec Writing Protocol, ensuring that outbound marketing, referral mechanics, and the Stealth Course progression are tied directly to Experience Primitives.

**CBAR Hardening Status:** All stories have been reconciled against the CBAR Audit Manifest (2026-05-10). Three catastrophic BMAD primitive mapping hallucinations have been purged. One fatal conflict (premature escalation physics in Story 1.2) has been resolved. Five canonical CBAR Mandates are now enforced in acceptance criteria.

---

## Canonical CBAR Mandates

These five mandates are binding constraints derived from the CBAR Audit and must be enforced across all implementation work in Phase 5. Any Tech Spec or PR that violates a mandate is automatically rejected.

1.  **The Verifiable Artifact Rule (Story 1.1):** All shareable score objects (User Cards) must include verifiable backend cryptographic validation (session ID, timestamp, biometric hash) to prevent spoofing and protect the platform's status economy. A peer clicking a Silent Referral link must see tamper-proof proof of the sender's claim.
2.  **The Earned Escalation Rule (Story 1.2):** An invited peer CANNOT be asked to record a reaction immediately after voting. The system must first deliver an Ephemeral Win-State (validating their vote with data, e.g., "Your industry intuition matches the top 10%") to earn the right to trigger the recording request. Premature escalation is a fatal UX violation.
3.  **The OFO Ego-Defense Rule (Story 2.1):** Unsolicited OFO audits must use the "Crusade Narrative" (Epic Meaning Framing) to position the critique as a defense of the target's legacy against algorithmic compression. Framing the audit as clinical criticism bypasses zero ego-defense mechanisms and kills the acquisition funnel.
4.  **The Inline Capture Hook (Story 2.2):** The first accountability challenge offered to an OFO target must be executable immediately inline within the Telegram chat (60-second voice correction), completing the Hook Cycle before session exit. Scheduling the next step for "tomorrow" or requiring a context switch fatally destroys Hook Cycle Velocity.
5.  **The 1-Tap Paywall Rule (Story 3.1):** All continuity subscription upgrades within the Stealth Course flow must use native Telegram 1-tap payment infrastructure (Apple Pay / Google Pay via Telegram Bot API). The payment action must require the same physical and cognitive effort as swiping a flashcard, preserving Friction-Zero momentum and eliminating cart abandonment.

---

## Functional Requirements (FR) Inventory

*   **FR-ERA3-03 (Silent Referral Architecture):** The system that turns user participation and Challenge scores into shareable social objects that drive organic acquisition without explicit affiliate loops (PRD-09).
*   **FR-ERA3-04 (OFO Engine):** The Object-First Outreach engine that generates high-end proof assets as a Trojan Horse wedge for acquiring new high-value coaches (PRD-09).
*   **FR-ERA3-14 (B2B2C Commercial Ladder & Stealth Course):** The 4-tier pricing progression and Stealth Course transition that silently converts users from the $0 Proof Layer to continuity subscriptions (PRD-09).

---

## Epic 1: Silent Referral Architecture (FR-ERA3-03)
**Goal:** Replace explicit referral friction with an organic loop where sharing is driven by the desire for social support, debate, and status validation, treating growth as a natural byproduct of product participation (PRD-09).

### Story 1.1: Shareable Score Object Generation
As a Participant, I want my Reaction or Challenge score packaged into a premium, cryptographically verifiable visual object, so that I can post it to my social channels knowing it carries authentic, tamper-proof status.
**Acceptance Criteria:**
*   **Given** a user achieves a high score, completes a challenge layer, or records a powerful Conscious Reaction,
*   **When** the artifact is processed,
*   **Then** the system generates a branded, status-bearing link (e.g., a Prismatic User Card) that:
    *   Includes a backend-verifiable cryptographic hash binding the specific session ID, timestamp, and biometric data that generated the score.
    *   Opens directly into the Telegram Mini App for the receiver.
    *   Presents a tamper-proof validation panel on the landing page, proving the sender's claim is authentic and not spoofed.
*   **CBAR Mandate Enforced:** The Verifiable Artifact Rule.

**Primitive Quality Constraints (EXP-SOC-001: Social Treasures):**
*   **Quality Standard (Self-Esteem Economy):** The shared object must validate the user's effort and status through verifiable proof. The share mechanism must feel like sharing a personal victory backed by cryptographic evidence, not spamming a link for cashback. The viral loop is protected because the card is unfakeable — sharing it signals elite performance, not platform gullibility.

### Story 1.2: Vote Then React Escalation
As an Invited Friend, I want to be able to vote on my friend's reaction without logging in, receive validation that my vote was insightful, and only then be invited to try it myself, so that my entry into the ecosystem earns my engagement rather than demanding it.
**Acceptance Criteria:**
*   **Given** I click a friend's shared Reaction link,
*   **When** I cast my vote (For/Against),
*   **Then** the system:
    1.  Delivers an **Ephemeral Win-State** first: validating the vote with data (e.g., "You correctly identified the winning side! Your industry intuition matches the top 10%").
    2.  **Only after** the Win-State has landed and the dopamine hit is delivered, the system surfaces the expansion trigger: "Want to defend your vote? Record your own 60-second take."
*   The system MUST NOT present the recording prompt before or simultaneously with the vote result. The Ephemeral Win-State is a mandatory prerequisite.
*   **CBAR Mandate Enforced:** The Earned Escalation Rule.

**Primitive Quality Constraints (EXP-TRG-005: First Major Win-State):**
*   **Quality Standard (Earned Fiero Gate):** The expansion trigger (recording prompt) is gated behind an authentic Win-State delivery. The system leverages consistency bias only after the user has experienced Fiero from their vote validation — never before. Premature escalation is treated as a fatal UX violation equivalent to a broken growth funnel.

---

## Epic 2: OFO Engine - Object First Outreach (FR-ERA3-04)
**Goal:** Deploy the B2B2C Trojan Horse acquisition strategy by delivering undeniable, high-value proof assets to coach targets before ever making a sales pitch (PRD-09).

### Story 2.1: The 4-Asset Proof Package Delivery
As an Outreach Target, I want to receive a high-end visual audit of my communication style completely for free, framed as a defense of my expertise against algorithmic compression, so that I immediately recognize the platform as an ally rather than a critic.
**Acceptance Criteria:**
*   **Given** an identified high-value coach target,
*   **When** the OFO Engine processes their public content,
*   **Then** it generates the 4-asset package (Carousel, Storytelling Video, Reels Explainer, Animated Video Audit) and stages it for delivery via Telegram.
*   The Animated Video Audit must:
    *   Frame the biometric analysis using the **Crusade Narrative**: positioning the platform as defending the coach's legacy and nuance against algorithmic flattening (e.g., "You have elite ideas, but generic social algorithms are compressing your authority. Here is the exact biometric data on how to restore it.").
    *   Never frame the audit as clinical criticism or unsolicited correction of their life's work.
*   **CBAR Mandate Enforced:** The OFO Ego-Defense Rule.

**Primitive Quality Constraints (EXP-TRS-004: Epic Meaning Framing):**
*   **Quality Standard (Crusade Narrative Bypass):** The audit must wrap the critique in Epic Meaning to bypass ego-defense mechanisms. The quality must be so high that ignoring it feels like an act of "Obvious Stupidity," but the framing must ensure the target feels defended, not attacked. Clinical critique framing kills the funnel by triggering defensive blocking.

### Story 2.2: Stealth Course Accountability Hook
As a Target reviewing my audit, I want the system to offer me an immediate, inline chance to improve my score right now, so that I experience the transformation engine firsthand before I have time to disengage.
**Acceptance Criteria:**
*   **Given** I enter the bot to view my OFO audit,
*   **When** I interact with the feedback,
*   **Then** the agent seamlessly transitions into Challenge Mode within the same session, inviting me to record a **60-second voice correction** to my audited audio immediately inline within the Telegram chat.
*   The accountability hook MUST complete the entire Hook Cycle (trigger → action → reward → investment) before I close the app. Scheduling the next step for a future session is a fatal violation.
*   **CBAR Mandate Enforced:** The Inline Capture Hook.

**Primitive Quality Constraints (EXP-PRG-001: Hook Cycle Velocity):**
*   **Quality Standard (Same-Session Conversion):** The system must sell the Coach OS not through a brochure, but by letting the target experience the transformation engine firsthand as a client would — completing the full Hook Cycle within a single Telegram session. Any context switch or deferred scheduling destroys velocity and loses the target.

---

## Epic 3: B2B2C Commercial Ladder & Stealth Course (FR-ERA3-14)
**Goal:** Implement the Fladlien-inspired Stealth Course commercial progression, mapping the user journey tightly to the newly established 4-tier pricing model to ensure maximum conversion without standard SaaS sales tactics (PRD-09).

### Story 3.1: Stealth Course Transition
As a Free User on the $0 Proof Layer, I want my onboarding challenge to naturally introduce advanced concepts and convert me seamlessly with a single tap, so that I transition into the paid continuity tier without breaking my flow state.
**Acceptance Criteria:**
*   **Given** I am participating in the free Lead Magnet layer,
*   **When** I hit the transition boundary (e.g., unlocking the 'Structure' Adaptive Layer),
*   **Then** the system deploys the "Stealth Course" mechanic, locking advanced FR61 insight and higher-tier capability behind the Tier 1 ($39.99/mo) Speaking & Learning subscription.
*   The payment action MUST use **Telegram's native 1-tap payment infrastructure** (Apple Pay / Google Pay via Telegram Bot API).
*   The cognitive and physical effort required to complete payment must be equivalent to swiping a flashcard — zero context switch, zero external browser redirect, zero manual card entry.
*   **CBAR Mandate Enforced:** The 1-Tap Paywall Rule.

**Primitive Quality Constraints (EXP-FRC-002: Friction-Zero Ability):**
*   **Quality Standard (Proof-Based Expansion):** The system must never ask for payment before the user has tangibly felt the product's value and received an actionable biometric score. The transition must feel like a logical deepening of an already established habit. The payment itself must preserve Friction-Zero momentum via native Telegram payments — any break in flow (external redirect, manual card entry, authentication wall) is a fatal conversion killer.

---

## FR Coverage Matrix

| FR ID | Feature | Mapped Epic & Story |
| :--- | :--- | :--- |
| FR-ERA3-03 | Silent Referral Architecture | Epic 1 (Stories 1.1, 1.2) |
| FR-ERA3-04 | OFO Engine | Epic 2 (Stories 2.1, 2.2) |
| FR-ERA3-14 | Commercial Ladder & Stealth Course | Epic 3 (Story 3.1) |

---

## CBAR Audit Resolution Log

| Story | Original Primitive Tag | Error Type | Corrected Primitive Tag | Audit Verdict | Resolution |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1.1 | `EXP-SOC-001: Social Treasures` | Valid ID, missing constraint | `EXP-SOC-001: Social Treasures` | REWRITE REQUIRED | Added cryptographic verification mandate to AC |
| 1.2 | `EXP-TRG-005: External to Internal Trigger Mapping` | **Hallucinated name** (registry: First Major Win-State) | `EXP-TRG-005: First Major Win-State` | FATAL CONFLICT | Inserted mandatory Ephemeral Win-State gate before escalation |
| 2.1 | `EXP-TRB-004: Attractive Things Work Better` | **Hallucinated prefix AND name** (registry: EXP-TRS-004, Epic Meaning Framing) | `EXP-TRS-004: Epic Meaning Framing` | REWRITE REQUIRED | Enforced Crusade Narrative framing to bypass ego-defense |
| 2.2 | `EXP-PRG-001: Discover→Master→Replay` | **Hallucinated name** (registry: Hook Cycle Velocity) | `EXP-PRG-001: Hook Cycle Velocity` | REWRITE REQUIRED | Enforced same-session inline Telegram capture |
| 3.1 | `EXP-FRC-002: Friction-Zero Ability` | Valid ID, missing enforcement | `EXP-FRC-002: Friction-Zero Ability` | REWRITE REQUIRED | Mandated 1-Tap Telegram payment infrastructure |
