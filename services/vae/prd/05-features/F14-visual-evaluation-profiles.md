---
title: F14 — Visual Evaluation Profiles and Independent VLM Quality System
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F14
governing_decisions:
- D004
- D010
- D017
- D018
- D020
- D025
- D027
user_journeys:
- UJ-03
- UJ-04
- UJ-07
- UJ-09
- UJ-13
functional_requirement_count: 8
---


# F14 — Visual Evaluation Profiles and Independent VLM Quality System

**User outcome:** A candidate is judged against the right family, composition, syntax, continuity, and temporal criteria rather than by a universal aesthetic score.

## Description

Evaluation profiles compile deterministic checks and independent VLM programs into a typed, versioned acceptance system.

## Brownfield baseline

V2.1 defines evaluation and readiness but not the required multimodal product, composition, recurrence, temporal, and evaluator-certification system.

## Required product delta

Define evaluation profile registry, deterministic validation, asset/composition/syntax/temporal VLM programs, failure taxonomy, evidence regions, hard gates, confidence, arbitration, profile versioning, and evaluator benchmarks.

## Traceability

- **Decisions:** D004, D010, D017, D018, D020, D025, D027
- **User journeys:** UJ-03, UJ-04, UJ-07, UJ-09, UJ-13
- **Cross-cutting NFRs:** NFR-SEM-001, NFR-SEM-002, NFR-SEM-003, NFR-SEM-004, NFR-SEM-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-MEM-001, NFR-MEM-002, NFR-MEM-003, NFR-MEM-004, NFR-MEM-005

## Functional Requirements

### FR-105 — Register asset-family-aware evaluation profiles

**Requirement:** Each certified asset family, subtype, route, and composition context must map to an evaluation profile declaring deterministic validators, VLM programs, required contexts, dimensions, thresholds, hard gates, failure codes, repair mappings, and applicability.

**Consequences (testable):

- The plan compiler selects the exact profile before candidate production.

- A universal unversioned evaluator cannot approve every asset class.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-106 — Run deterministic technical validation first

**Requirement:** Code-owned validators must check file integrity, dimensions, aspect ratio, duration/frame rate, codec, alpha, masks, blank/corrupt output, metadata, receipt completeness, and budget before semantic evaluation.

**Consequences (testable):

- Technical failures are localized without spending VLM evaluation unnecessarily.

- A candidate failing a technical hard gate cannot be promoted by VLM preference.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-107 — Run independent asset-level VLM evaluation

**Requirement:** The evaluator must compare the isolated candidate with required subject, action, expression, pose, gesture, gaze, identity, environment, visual properties, semantic intent, Activative function, wrong-reading locks, and artifact quality.

**Consequences (testable):

- Failures include evidence regions/time ranges and calibrated confidence.

- The producing model’s self-description cannot substitute for independent inspection.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-108 — Run composition-level VLM evaluation

**Requirement:** Applicable candidates must be rendered inside their intended BBOX, layers, text reservations, neighboring elements, sequence role, and feed/viewing profile before composition-effectiveness approval.

**Consequences (testable):

- Evaluation checks hierarchy, focal visibility, negative space, crop safety, gaze/motion direction, collision, and Activative function.

- Standalone beauty or correctness cannot compensate for a failed composed use.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-109 — Run syntax-aware recurrence and continuity evaluation

**Requirement:** The evaluator must compare the candidate’s proposed rendered use against relevant Visual Usage Receipts, syntax fingerprints, identities, environments, sequence roles, and recurrence intent.

**Consequences (testable):

- It classifies recurrence and explains whether continuity or progression is helped or harmed.

- Raw usage frequency cannot be the sole fatigue signal.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-110 — Run temporal evaluation where applicable

**Requirement:** Motion and video profiles must evaluate frame-to-frame identity, motion, gesture completion, camera continuity, flicker, artifacts, loop integrity, duration, and timing against sequence purpose.

**Consequences (testable):

- Temporal failures include time ranges and responsible production layers.

- A passing first frame cannot approve a failing animation.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-111 — Synthesize verdicts with hard-gate precedence

**Requirement:** The evaluation contract must preserve per-layer verdicts, dimensions, evidence, failure codes, repair owner, and confidence; acceptance requires all applicable hard gates.

**Consequences (testable):

- Weighted rankings are calculated only among eligible passing candidates.

- High technical or aesthetic scores cannot hide a failed semantic, Activative, or composition gate.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

### FR-112 — Certify evaluator versions independently

**Requirement:** VLM programs and threshold profiles must pass labeled accepted/rejected/borderline, recurrence, temporal, responsible-layer, and repair usefulness benchmarks before shadow and production promotion.

**Consequences (testable):

- Acceptance receipts pin evaluator model, program, profile, thresholds, and context hashes.

- A newer model version cannot replace the production evaluator without regression evidence.

**Traceability:** Decisions D004, D010, D017, D018, D020, D025, D027; journeys UJ-03, UJ-04, UJ-07, UJ-09, UJ-13.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
