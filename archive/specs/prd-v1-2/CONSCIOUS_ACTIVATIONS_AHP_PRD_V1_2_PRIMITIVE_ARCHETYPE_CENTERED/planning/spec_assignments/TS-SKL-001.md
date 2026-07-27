---
type: tech_spec_assignment
spec_id: TS-SKL-001
title: "Canonical Skills, Skill Composition Recipes, Steering Recipes, and Transformation Contracts"
product_owner: "Atomic Harness Pipeline"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-SKL-001.md"
---

# TS-SKL-001 — Canonical Skills, Skill Composition Recipes, Steering Recipes, and Transformation Contracts

## Controlling product requirements and Stories

**Functional Requirements:** FR-031, FR-032, FR-033, FR-034, FR-035, FR-036  
**Primary Stories:** ST-07.02

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-009` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/jit_capsule.py | REFERENCE | Existing phase-local JIT Execution Capsule taxonomy and integrity rules. |
| `SRC-CUR-020` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md | REFERENCE | CMF-OKF, Steering Recipes, hybrid retrieval and Minimum Complete Context. |

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
