---
type: tech_spec_assignment
spec_id: TS-STA-001
title: "Composition IR, PRETEXT, Geometry, Annotation, and Skia Runtime"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-STA-001.md"
---

# TS-STA-001 — Composition IR, PRETEXT, Geometry, Annotation, and Skia Runtime

## Controlling product requirements and Stories

**Functional Requirements:** FR-049, FR-050, FR-051, FR-052, FR-053, FR-054  
**Primary Stories:** ST-05.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-014` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F05-composition-intent-image-conditioned-geometry.md | REFERENCE | Composition intent, feasibility, geometry and composition-context evaluation. |
| `SRC-LEG-004` | src/ccp_studio/contracts/composition_runtime.py | FORK | Reuse Composition IR primitives, BBOX, layers and scene relationships under current taxonomy. |
| `SRC-LEG-005` | src/ccp_studio/services/composition_runtime_service.py | FORK_ADAPT | Retain deterministic geometry; replace placeholder visual providers and old authority assumptions. |
| `SRC-LEG-028` | src/ccp_studio/contracts/asset_program_compilers.py | FORK_ADAPT | Retain typed PRETEXT/SAM3/Rough/Skia bindings; replace placeholders. |
| `SRC-LEG-029` | src/ccp_studio/services/asset_program_compiler_service.py | FORK_ADAPT | Compile current transformation contracts into runtime-neutral plans. |
| `SRC-LEG-033` | docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md | RETAIN_EVIDENCE | Existing execution-spine audit. |
| `SRC-LEG-036` | docs/tech-specs/TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md | RETAIN_AND_ADAPT | Static visual runtime specification. |
| `SRC-EXT-008` | https://github.com/chenglou/pretext | REFERENCE | Deterministic multiline text measurement and layout. |
| `SRC-EXT-009` | https://roughnotation.com/ | REFERENCE | Typed hand-drawn annotation cue implementation reference. |
| `SRC-EXT-015` | https://api.skia.org/ | REFERENCE | 2D static graphics reference embodiment. |

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
