---
type: tech_spec_assignment
spec_id: TS-RET-001
title: "Authority-First Hybrid Retrieval and JIT Execution Capsule Compiler"
product_owner: "Atomic Harness Pipeline"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-RET-001.md"
---

# TS-RET-001 — Authority-First Hybrid Retrieval and JIT Execution Capsule Compiler

## Controlling product requirements and Stories

**Functional Requirements:** FR-019, FR-020, FR-021, FR-022, FR-023, FR-024  
**Primary Stories:** ST-07.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-009` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/jit_capsule.py | REFERENCE | Existing phase-local JIT Execution Capsule taxonomy and integrity rules. |
| `SRC-CUR-020` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md | REFERENCE | CMF-OKF, Steering Recipes, hybrid retrieval and Minimum Complete Context. |
| `SRC-EXT-005` | https://huggingface.co/nvidia/Nemotron-3-Embed-1B-BF16 | REFERENCE | Text/code dense retrieval candidate after deterministic eligibility filtering. |

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
