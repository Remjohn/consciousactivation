---
type: tech_spec_assignment
spec_id: TS-AHP-001
title: "Program Authority, Current-State Reconciliation, and Brownfield Source Admission"
product_owner: "Atomic Harness Pipeline"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-AHP-001.md"
---

# TS-AHP-001 — Program Authority, Current-State Reconciliation, and Brownfield Source Admission

## Controlling product requirements and Stories

**Functional Requirements:** FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-117  
**Primary Stories:** ST-01.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-001` | CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md | REFERENCE | Constitutional precedence and current product-authority pointer. |
| `SRC-CUR-002` | CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md | REFERENCE | Activation First, Visual Syntax First, product topology and semantic lineage. |
| `SRC-CUR-003` | CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md | REFERENCE | Public repository convergence and authorization status observed 2026-07-15. |
| `SRC-CUR-011` | 01_ATOMIC_HARNESS_BUILDER/CURRENT_PROJECT_STATUS.md | REFERENCE | Public Builder status snapshot; must be reconciled with newer operator-local receipts before implementation. |
| `SRC-LEG-033` | docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md | RETAIN_EVIDENCE | Existing execution-spine audit. |
| `SRC-LEG-034` | docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md | RETAIN_EVIDENCE | Legacy editing/composition/rendering intent. |
| `SRC-STATE-001` | CURRENT_STATE_RECONCILIATION(1).md | REFERENCE | Requires public and operator-local Builder/VAE/Delegation status reconciliation before implementation. |
| `SRC-MIG-001` | CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1(1).md | REFERENCE | Defines brownfield reuse/adapt/rewrite/archive treatment for the CMF Studio predecessor. |
| `SRC-MIG-002` | EXACT_SOURCE_REUSE_CROSSWALK(1).csv | REFERENCE | Exact current, predecessor, and external source paths, hashes, dispositions, and proposed targets. |

The writer must also read the exact current source and tests at the target product paths, the current product status, relevant contracts, and every predecessor file named by the exact source reuse crosswalk.

## Required 10-section Tech Spec structure

1. Files and authorities read.
2. Problem, solution, scope, and non-goals.
3. Architecture traceability, existing backend integration, product ownership, and governing decisions.
4. Staged implementation plan with exact paths and migration dispositions.
5. Schemas, APIs, state transitions, commands, events, and receipts.
6. Backward compatibility, fallback, rollback, invalidation, and historical replay.
7. Implementation tasks and path ownership.
8. Behavior-specific acceptance criteria, each with a failure example and Story/CBAR reference.
9. Dependencies, source authority, licenses, providers, models, workers, and external products.
10. Testing, evaluation, observability, security, performance, recovery, evidence, and release.

## Completion law

The spec is accepted only when all controlling FRs and Stories are covered, no second canonical object or product owner is introduced, exact existing code integration is named, negative and downstream failure cases are testable, and the implementation authority issues a bounded Development Capsule.
