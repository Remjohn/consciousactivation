---
type: tech_spec_assignment
spec_id: TS-VAE-BOUND-001
title: "VAE Provider Ownership for SAM3, Lucida, Layered Generation, ComfyUI, and Google GNM"
product_owner: "Visual Asset Editor"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "02_VISUAL_ASSET_EDITOR/docs/architecture/TS-VAE-BOUND-001.md"
---

# TS-VAE-BOUND-001 — VAE Provider Ownership for SAM3, Lucida, Layered Generation, ComfyUI, and Google GNM

## Controlling product requirements and Stories

**Functional Requirements:** FR-087, FR-088, FR-089  
**Primary Stories:** ST-08.02

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-013` | 02_VISUAL_ASSET_EDITOR/prd/index.md | REFERENCE | VAE 22-feature PRD index. |
| `SRC-CUR-015` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F08-visual-capability-registry.md | REFERENCE | Versioned models, LoRAs, controls, workflows and runtime capability registry. |
| `SRC-CUR-016` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F09-visual-production-plan-ir.md | REFERENCE | Visual Production Plan IR and provider-specific compilation. |
| `SRC-MIG-001` | CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1(1).md | REFERENCE | Defines brownfield reuse/adapt/rewrite/archive treatment for the CMF Studio predecessor. |
| `SRC-EXT-026` | github://google/GNM | REFERENCE | Apache-2.0 parametric 3D head geometry with identity, expression, pose, gaze, and internal anatomy controls; VAE-only bounded route. |
| `SRC-AM-002` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | AMENDMENT_INPUT | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |

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
