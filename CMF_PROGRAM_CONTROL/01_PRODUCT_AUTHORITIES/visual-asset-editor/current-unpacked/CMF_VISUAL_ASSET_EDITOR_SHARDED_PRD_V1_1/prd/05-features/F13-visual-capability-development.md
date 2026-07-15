---
title: F13 — Governed LoRA, Adapter, Control, and Workflow Capability Development
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F13
governing_decisions:
- D016
- D019
- D020
- D025
- D026
- D027
- D028
user_journeys:
- UJ-10
- UJ-11
- UJ-13
- UJ-16
functional_requirement_count: 8
---


# F13 — Governed LoRA, Adapter, Control, and Workflow Capability Development

**User outcome:** A recurring production gap can become a reusable, tested capability without training new resources for every difficult request.

## Description

Capability development is a separate evidence-driven workflow for reusable visual gaps, not an automatic fallback inside ordinary production.

## Brownfield baseline

Legacy University material anticipated LoRA and local-model work, while the current Builder architecture defines capability ownership and maturity. The Visual Editor PRD must connect those principles to production evidence and registry promotion.

## Required product delta

Define gap qualification, evidence sufficiency, dataset contracts, sandboxed training, baseline comparisons, evaluator coverage, contamination/regression tests, shadow use, promotion, rollback, and cost authorization.

## Traceability

- **Decisions:** D016, D019, D020, D025, D026, D027, D028
- **User journeys:** UJ-10, UJ-11, UJ-13, UJ-16
- **Cross-cutting NFRs:** NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-097 — Detect reusable capability gaps

**Requirement:** A gap may be proposed only when representative demands or repeated repairs show an unmet recurring identity, character, environment, visual-language, pose, motion, control, workflow, or evaluator capability.

**Consequences (testable):

- The proposal includes failed certified alternatives, expected reuse, and affected syntax contexts.

- One unattractive candidate or ordinary stochastic failure cannot trigger training.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-098 — Require evidence-sufficiency analysis

**Requirement:** Before training or adaptation, the system must assess reference count, diversity, quality, identity consistency, captions, rights/source policy class, duplicates, exclusions, and coverage of intended conditions.

**Consequences (testable):

- Insufficient evidence produces a typed blocker and collection plan.

- Training cannot begin from an undocumented or contradictory dataset.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-099 — Compile a typed Capability Development Plan

**Requirement:** The plan must declare capability goal, target base, dataset contract, preprocessing, training method, hyperparameter search, compute budget, baseline, evaluation profiles, promotion path, rollback, and prohibited use.

**Consequences (testable):

- Every training job traces to the approved plan.

- Ad hoc notebook training cannot create a registry-eligible production capability.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-100 — Prepare datasets in isolated, reproducible pipelines

**Requirement:** Dataset normalization, deduplication, captioning, cropping, quality inspection, train/validation splits, and manifests must execute in versioned sandboxes with immutable source references.

**Consequences (testable):

- The exact training dataset can be reconstructed and diffed.

- Untracked manual dataset edits invalidate the training receipt.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-101 — Benchmark against relevant controls

**Requirement:** New LoRAs, adapters, controls, workflows, or model adaptations must be compared with base model, current registered controls, existing stacks, and other credible alternatives on representative demands and syntax contexts.

**Consequences (testable):

- The benchmark measures intended improvement, responsiveness, diversity, overfitting, contamination, composition control, cost, latency, and regressions.

- A capability cannot be promoted solely from showcase outputs.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-102 — Detect contamination and compatibility regressions

**Requirement:** Evaluation must test identity drift, style leakage, prompt insensitivity, forbidden combinations, base-model incompatibility, unwanted memorization, composition degradation, and failure outside declared applicability.

**Consequences (testable):

- Critical regression blocks promotion and is linked to evidence.

- A capability that improves one target while breaking certified shared behavior cannot enter production silently.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-103 — Use staged registry promotion

**Requirement:** Successful capability candidates must move through experimental, benchmarked, shadow, limited-production, and production states with pinned versions and approved applicability.

**Consequences (testable):

- Shadow decisions are compared against the current baseline without controlling accepted assets.

- An experimental LoRA cannot be selected under production-only policy.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

### FR-104 — Preserve rollback and deprecation

**Requirement:** Every promoted capability must retain its predecessor, migration/compatibility notes, dependent paths, rollback procedure, and retirement criteria.

**Consequences (testable):

- A production regression can revert routing to the preceding certified version without losing run reproducibility.

- Deleting or replacing the only copy of a capability used by historical assets is prohibited.

**Traceability:** Decisions D016, D019, D020, D025, D026, D027, D028; journeys UJ-10, UJ-11, UJ-13, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
