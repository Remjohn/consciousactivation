---
type: tech_spec_assignment
spec_id: TS-CAS-004
title: "Source-to-Batch Control Tower, Category Workbenches, Evidence, Health, and Audit Export"
product_owner: "Conscious Activations Studio"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "CONSCIOUS_ACTIVATIONS_STUDIO/docs/architecture/TS-CAS-004.md"
---

# TS-CAS-004 — Source-to-Batch Control Tower, Category Workbenches, Evidence, Health, and Audit Export

## Controlling product requirements and Stories

**Functional Requirements:** FR-109, FR-110, FR-112, FR-113, FR-114  
**Primary Stories:** ST-10.06

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-AM-001` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | AMENDMENT_INPUT | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-AM-002` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | AMENDMENT_INPUT | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-INT-001` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | ADAPT | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-MIG-001` | CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1(1).md | REFERENCE | Defines brownfield reuse/adapt/rewrite/archive treatment for the CMF Studio predecessor. |
| `SRC-EXT-021` | github://openvideodev/video-editor | REFERENCE_LICENSE_REVIEW | Multi-track timeline, drag/split/trim/snapping, interactive canvas, client-side preview/export patterns. |
| `SRC-EXT-022` | github://lineCode/ai-video-editor | REFERENCE_LICENSE_REVIEW | AI Copilot controlling scripts, visuals, and timeline; UI pattern only. |
| `SRC-CUR-020` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md | REFERENCE | CMF-OKF, Steering Recipes, hybrid retrieval and Minimum Complete Context. |
| `SRC-EXT-027` | github://GoogleCloudPlatform/knowledge-catalog/okf | REFERENCE | Portable Markdown/YAML knowledge representation with progressive disclosure and links; base for CMF-OKF profile. |
| `SRC-EXT-028` | hf://nvidia/Nemotron-3-Embed | REFERENCE_BENCHMARK | Candidate text/code embedding ranker after deterministic eligibility; not visual or authority layer. |
| `SRC-EXT-018` | github://remotion-dev/remotion | REFERENCE_LICENSE_REVIEW | React/frame source-of-truth rendering, Player, batch rendering, and editor integration. |
| `SRC-EXT-019` | github://heygen-com/hyperframes | REFERENCE | Deterministic HTML/CSS/GSAP motion blocks, skills, registry, Studio, and Player. |
| `SRC-EXT-026` | github://google/GNM | REFERENCE | Apache-2.0 parametric 3D head geometry with identity, expression, pose, gaze, and internal anatomy controls; VAE-only bounded route. |

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
