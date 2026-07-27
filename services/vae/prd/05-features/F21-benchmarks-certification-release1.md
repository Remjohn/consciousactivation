---
title: F21 — Benchmark Portfolio, Staged Certification, and Release 1 Format 02 Slice
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F21
governing_decisions:
- D004
- D017
- D018
- D019
- D020
- D025
- D026
- D027
- D028
user_journeys:
- UJ-03
- UJ-04
- UJ-07
- UJ-08
- UJ-09
- UJ-11
- UJ-13
- UJ-14
- UJ-16
functional_requirement_count: 8
---


# F21 — Benchmark Portfolio, Staged Certification, and Release 1 Format 02 Slice

**User outcome:** A release can prove exactly which visual capabilities are reliable and avoid claiming support for untested asset families.

## Description

The certification system evaluates end-to-end production, evaluators, repairs, recurrence, infrastructure, compatibility, and the real Format 02 reference path.

## Brownfield baseline

The Builder PRD already uses staged reference benchmarks and hard gates. The Visual Editor requires multimodal production datasets, evaluator labels, GPU recovery, and one fully consumed Atomic Harness asset path.

## Required product delta

Define corpus layers, dimensions, evaluator benchmark, fault tests, promotion, release receipts, Format 02 reference fixtures, limited scope, local/cloud proof, and one capability-development cycle.

## Traceability

- **Decisions:** D004, D017, D018, D019, D020, D025, D026, D027, D028
- **User journeys:** UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-161 — Maintain a layered visual benchmark corpus

**Requirement:** The portfolio must contain representative real demands, behavior goldens, known failures, adversarial cases, controlled mutations, incomplete/conflicting demands, recurrence contexts, repair cases, capability-transfer cases, and out-of-distribution cases.

**Consequences (testable):

- Each case declares expected behavior, hard gates, scoring, and protected labels.

- Showcase assets alone cannot certify the system.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-162 — Score independent dimensions with hard gates

**Requirement:** Certification must report semantic fidelity, Activative fidelity, composition effectiveness, syntax conformance, identity/continuity, technical validity, temporal stability where applicable, provenance/reproducibility, repair precision, evaluator accuracy, cost, latency, and intervention.

**Consequences (testable):

- A failed constitutional dimension blocks promotion regardless of average.

- One composite score cannot replace the full scorecard.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-163 — Benchmark the VLM evaluator itself

**Requirement:** The evaluator set must include accepted, rejected, borderline, identity drift, wrong action, composition failure, beneficial recurrence, fatiguing recurrence, temporal failure, repairable and nonrepairable cases.

**Consequences (testable):

- Metrics include hard-failure recall, false rejection, failure-code and responsible-layer accuracy, recurrence judgment, repair usefulness, and confidence calibration.

- An evaluator cannot certify its own benchmark labels.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-164 — Test repair precision and preservation

**Requirement:** Repair benchmarks must verify root-cause layer, allowed binding changes, frozen properties, selective invalidation, improvement, regression absence, and three-round stop behavior.

**Consequences (testable):

- Before/after assets and receipts are retained.

- A repair process that routinely redoes the whole asset or drifts identity cannot pass.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-165 — Test compute and workflow recovery

**Requirement:** Certification must inject container crash, GPU loss, API timeout, model-cache corruption, missing node, queue interruption, worker replacement, checkpoint restore, and provider fallback failures.

**Consequences (testable):

- State, lineage, and quality-round counts remain correct after recovery.

- Manual worker intervention cannot be required for the certified routine path.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-166 — Use staged capability and product promotion

**Requirement:** Workflows, models, LoRAs, evaluators, Steering Recipes, runtime profiles, and product releases must move through experimental, benchmarked, shadow, limited-production, and certified-production stages with rollback.

**Consequences (testable):

- The release receipt identifies authorized scope and unresolved limitations.

- Passing unit tests alone cannot authorize production.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-167 — Prove the complete Format 02 vertical slice

**Requirement:** Release 1 must process real Minimal Coach Theatre demands for character identity, pose, expression, gesture, gaze, environment, composition, continuity, syntax role, Activative function, wrong-reading locks, candidates, repair, geometry, result, and downstream composition consumption without routine manual work.

**Consequences (testable):

- The reference slice runs on one local/self-hosted and one cloud Docker GPU profile.

- A good standalone image that is not consumed and evaluated in the Format 02 composition does not complete the slice.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

### FR-168 — Represent broader scope honestly

**Requirement:** All eight asset families may have schemas, registries, interfaces, and benchmark placeholders, but only capabilities that pass their required portfolio and release receipt may be routed as production-certified.

**Consequences (testable):

- UI and compatibility manifests expose limited and uncertified scope.

- Release 1 cannot imply full video, documentary retrieval, advanced diagrams, UI reconstruction, or other uncertified production support.

**Traceability:** Decisions D004, D017, D018, D019, D020, D025, D026, D027, D028; journeys UJ-03, UJ-04, UJ-07, UJ-08, UJ-09, UJ-11, UJ-13, UJ-14, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
