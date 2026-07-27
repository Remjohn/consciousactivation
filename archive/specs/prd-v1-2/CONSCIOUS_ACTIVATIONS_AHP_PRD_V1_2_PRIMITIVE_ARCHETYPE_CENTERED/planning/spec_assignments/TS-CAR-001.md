---
type: tech_spec_assignment
spec_id: TS-CAR-001
title: "Source-Grounded Carousel Runtime and Export Package"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-CAR-001.md"
---

# TS-CAR-001 — Source-Grounded Carousel Runtime and Export Package

## Controlling product requirements and Stories

**Functional Requirements:** FR-055, FR-056, FR-057, FR-058, FR-059, FR-060, FR-145  
**Primary Stories:** ST-05.02

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-007` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py | REFERENCE | Category-native runtime plan requirements, evaluation dimensions and repair units. |
| `SRC-LEG-024` | src/ccp_studio/services/carousel_engine_service.py | FORK_ADAPT | Map to current Carousel category laws and future ratified format profiles. |
| `SRC-LEG-025` | src/ccp_studio/services/carousel_render_service.py | REPLACE_ACTIVATE | Replace synthetic references with actual Skia artifacts. |
| `SRC-LEG-037` | docs/tech-specs/TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md | RETAIN_AND_ADAPT | Carousel sequence specification. |
| `SRC-LEG-038` | docs/tech-specs/TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md | RETAIN_AND_ADAPT | Carousel compiler and Skia export specification. |
| `SRC-LEG-039` | docs/tech-specs/TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md | RETAIN_AS_CANDIDATE_EVIDENCE | Candidate profile and training/benchmark evidence only. |
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
