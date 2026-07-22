---
type: tech_spec_assignment
spec_id: TS-REL-002
title: "Source-First Release Evidence, Expansion Claims, and Implementation Handoff"
product_owner: "Program Control + Pipeline"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "CMF_PROGRAM_CONTROL/docs/architecture/TS-REL-002.md"
---

# TS-REL-002 — Source-First Release Evidence, Expansion Claims, and Implementation Handoff

## Controlling product requirements and Stories

**Functional Requirements:** FR-115, FR-116, FR-118, FR-119, FR-120  
**Primary Stories:** ST-11.02, ST-11.03, ST-11.04

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-INT-001` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | ADAPT | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-AM-001` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | AMENDMENT_INPUT | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-AM-002` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | AMENDMENT_INPUT | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-EXT-017` | github://browser-use/video-use | REFERENCE | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-MIG-001` | CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1(1).md | REFERENCE | Defines brownfield reuse/adapt/rewrite/archive treatment for the CMF Studio predecessor. |
| `SRC-CUR-018` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F14-visual-evaluation-profiles.md | REFERENCE | Independent visual evaluation profiles. |
| `SRC-CUR-019` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md | REFERENCE | Typed visual repair and bounded reruns. |
| `SRC-CUR-003` | CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md | REFERENCE | Public repository convergence and authorization status observed 2026-07-15. |
| `SRC-CUR-021` | 02_VISUAL_ASSET_EDITOR/CURRENT_PROJECT_STATUS.md | REFERENCE | Public VAE implementation/evidence status and Stage 5 gate. |
| `SRC-MIG-002` | EXACT_SOURCE_REUSE_CROSSWALK(1).csv | REFERENCE | Exact current, predecessor, and external source paths, hashes, dispositions, and proposed targets. |
| `SRC-TREE-001` | PROPOSED_TARGET_FILE_TREE(1).md | REFERENCE | Proposed fourth-product repository tree and ownership boundary. |
| `SRC-SPEC-001` | Specs_Builder_Library(1).zip | ADAPT_METHOD | PRD module, Epic/Story, CBAR hardening, and Tech Spec writing protocols; legacy product constants are not current authority. |

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
