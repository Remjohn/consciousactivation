---
type: tech_spec_assignment
spec_id: TS-DEL-001
title: "Source-Grounded Visual Asset Demand, Asset Result, Geometry, and Usage Acknowledgement"
product_owner: "Delegation + Pipeline + VAE"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "03_DELEGATION_PROTOCOL/docs/architecture/TS-DEL-001.md"
---

# TS-DEL-001 — Source-Grounded Visual Asset Demand, Asset Result, Geometry, and Usage Acknowledgement

## Controlling product requirements and Stories

**Functional Requirements:** FR-085, FR-086, FR-090  
**Primary Stories:** ST-08.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-014` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F05-composition-intent-image-conditioned-geometry.md | REFERENCE | Composition intent, feasibility, geometry and composition-context evaluation. |
| `SRC-CUR-016` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F09-visual-production-plan-ir.md | REFERENCE | Visual Production Plan IR and provider-specific compilation. |
| `SRC-CUR-022` | 03_DELEGATION_PROTOCOL/README.md | REFERENCE | Harness↔VAE product boundary and contract package. |
| `SRC-AM-002` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | AMENDMENT_INPUT | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-INT-001` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | ADAPT | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-CUR-018` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F14-visual-evaluation-profiles.md | REFERENCE | Independent visual evaluation profiles. |
| `SRC-CUR-019` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md | REFERENCE | Typed visual repair and bounded reruns. |

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
