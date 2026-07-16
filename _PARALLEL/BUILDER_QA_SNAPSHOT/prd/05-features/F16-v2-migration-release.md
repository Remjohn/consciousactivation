---
title: F16 — Controlled V2.1 Migration, Compatibility, and Release Governance
product: CMF Atomic Harness Builder Next
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F16
governing_decisions:
- D003
- D022
- D024
- D028
- D032
- D033
user_journeys:
- UJ-11
- UJ-12
functional_requirement_count: 10
---

# F16 — Controlled V2.1 Migration, Compatibility, and Release Governance

**User outcome:** Builder Maintainers can evolve the proven V2.1 baseline in measurable increments, preserve valuable behavior, and limit production claims to demonstrated transfer.

## Description

This feature prevents a greenfield rewrite from discarding working saturation, Genesis, ratification, OpenSpec, and readiness logic. Each architectural increment must prove its value through tests and the reference harness.

## Brownfield baseline

V2.1 is executable and tested and already implements several core mechanisms. It also has portability, source-configuration, embedded-reference, generic profile, and production-depth limitations identified during prior analysis.

## Required product delta

Create capability inventory, baseline fixtures, old-to-new mappings, dual compilation, compatibility layers, deprecation governance, migration receipts, staged release claims, and reference-harness continuous integration.

## Traceability

- **Decisions:** D003, D022, D024, D028, D032, D033
- **User journeys:** UJ-11, UJ-12
- **Cross-cutting NFRs:** NFR-COMPAT-001, NFR-COMPAT-002, NFR-REL-001, NFR-EVAL-003, NFR-TRACE-002

## Functional Requirements

### FR-160 — Inventory V2.1 capabilities and artifacts

**Requirement:** Before modification, the project must produce a machine-readable inventory of V2.1 commands, schemas, decision nodes, prompts, references, tests, artifacts, workflows, and known limitations.

**Consequences (testable):**

- Each item has a retain, adapt, replace, deprecate, or remove-after-evidence classification.
- The inventory is versioned against the exact V2.1 source hash.

**Traceability:** Decisions D028; journeys UJ-12.

### FR-161 — Map V2.1 concepts into the next architecture

**Requirement:** The migration plan must map existing source saturation, atomicity, Genesis, ratification, OpenSpec, readiness, and Pi assets into Harness IR, target profiles, graphs, skill ecology, benchmarks, and authorization.

**Consequences (testable):**

- Unmapped behavior is explicitly reviewed rather than silently lost.
- One-to-many and deprecated mappings include rationale.

**Traceability:** Decisions D028; journeys UJ-12.

### FR-162 — Support baseline and candidate dual compilation

**Requirement:** During migration, the same eligible target must be compilable through the retained V2.1 baseline and candidate Builder for comparison.

**Consequences (testable):**

- The comparison uses locked inputs and declares unavoidable schema or profile differences.
- Candidate improvements and regressions are visible per dimension.

**Traceability:** Decisions D022, D028; journeys UJ-12.

### FR-163 — Require evidence for retention, adaptation, or deprecation

**Requirement:** A working V2.1 behavior may be changed or removed only with a documented product rationale, replacement path, tests, migration effect, and benchmark evidence proportional to its risk.

**Consequences (testable):**

- Aesthetic preference alone cannot justify removing a proven workflow.
- Deprecated behavior remains available through the declared compatibility window.

**Traceability:** Decisions D028; journeys UJ-12.

### FR-164 — Run regression suites at every migration increment

**Requirement:** Each increment must add failing tests or benchmark cases for the intended delta, implement the minimum correction, and rerun V2.1 compatibility plus reference-harness suites.

**Consequences (testable):**

- A migration increment cannot rely solely on code review.
- Regression results are stored in the release ledger.

**Traceability:** Decisions D021, D028; journeys UJ-12.

### FR-165 — Define compatibility and alias policy

**Requirement:** The Architecture must define which V2.1 CLI commands, configuration fields, artifact names, and status values remain supported, aliased, migrated, or rejected.

**Consequences (testable):**

- Compatibility behavior is explicit and testable.
- Aliases do not hide materially different semantics.

**Traceability:** Decisions D028; journeys UJ-11, UJ-12.

### FR-166 — Generate migration and deprecation receipts

**Requirement:** Every migrated run, artifact, schema, skill, or configuration must record source version, target version, transformations, warnings, losses, and validation results.

**Consequences (testable):**

- Operators can audit what changed during migration.
- Irreversible or lossy migrations require explicit approval.

**Traceability:** Decisions D025, D028; journeys UJ-09, UJ-12.

### FR-167 — Prove Release 1 through one complete reference path

**Requirement:** Release 1 must implement the complete Builder spine and use it to specify, implement, evaluate, repair, and certify one Atomic Content Harness vertical slice.

**Consequences (testable):**

- The release report includes downstream harness results, not only Builder unit tests.
- The reference harness remains a continuous integration target for later releases.

**Traceability:** Decisions D003, D022, D032; journeys UJ-11, UJ-12.

### FR-168 — Limit certification of unproven categories and targets

**Requirement:** Release 1 may include structural profiles for other categories, Visual Asset Editor, and Delegation Contract, but must mark them uncertified until their required benchmarks and transfer gates pass.

**Consequences (testable):**

- The Control Tower and documentation distinguish structural support from production certification.
- Uncertified profiles cannot issue full production authorization.

**Traceability:** Decisions D004, D032, D033; journeys UJ-12.

### FR-169 — Require portfolio evidence for general Builder certification

**Requirement:** The Builder may claim general production readiness only after successful transfer across materially different atomic harnesses, all five category constitutions, the Visual Asset Editor, and the Delegation Contract according to their target gates.

**Consequences (testable):**

- The certification statement lists the exact portfolio and versions passed.
- A new unsupported category or target remains outside the claim.

**Traceability:** Decisions D022, D032, D033; journeys UJ-12.

## Known failure and edge conditions

- V2.1 is deleted before parity and benchmark comparison.
- A new architecture is declared better because it has more artifacts.
- An alias maps an old command to materially different behavior without warning.
- Release 1 claims all five categories are production-certified.

## Explicitly out of scope

- Maintaining every historical artifact forever.
- Guaranteeing zero migration effort for unsupported private extensions.
- Changing the product boundary to preserve accidental V2.1 behavior.
