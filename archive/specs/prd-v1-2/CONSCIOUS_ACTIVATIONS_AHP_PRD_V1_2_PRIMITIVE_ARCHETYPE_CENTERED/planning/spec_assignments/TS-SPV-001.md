---
type: tech_spec_assignment
spec_id: TS-SPV-001
title: "Source-Grounded SuperVisual Runtime and Export Package"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-SPV-001.md"
---

# TS-SPV-001 — Source-Grounded SuperVisual Runtime and Export Package

## Controlling product requirements and Stories

**Functional Requirements:** FR-061, FR-062, FR-063, FR-064, FR-065, FR-066, FR-146  
**Primary Stories:** ST-05.03

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-007` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py | REFERENCE | Category-native runtime plan requirements, evaluation dimensions and repair units. |
| `SRC-LEG-026` | src/ccp_studio/services/supervisual_runtime_service.py | FORK_ADAPT | Map to current SuperVisual category laws and ratified profiles. |
| `SRC-LEG-027` | src/ccp_studio/services/supervisual_project_service.py | FORK_ADAPT | Project/version lifecycle for static compositions. |
| `SRC-LEG-040` | docs/tech-specs/TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md | RETAIN_AND_ADAPT | SuperVisual runtime specification. |
| `SRC-LEG-041` | docs/tech-specs/TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md | RETAIN_AS_CANDIDATE_EVIDENCE | Candidate composition-family evidence. |
| `SRC-INT-001` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | ADAPT | Interview-first source-to-asset product model and Complete Expression Session concepts. |

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
