---
type: tech_spec_assignment
spec_id: TS-VID-005
title: "Remotion, HyperFrames, FFmpeg Render, QA, and Export Adapters"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-VID-005.md"
---

# TS-VID-005 — Remotion, HyperFrames, FFmpeg Render, QA, and Export Adapters

## Controlling product requirements and Stories

**Functional Requirements:** FR-073, FR-074, FR-075, FR-076, FR-077, FR-078  
**Primary Stories:** ST-04.05

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-LEG-013` | src/ccp_studio/contracts/deterministic_rendering.py | FORK | Renderer-neutral render requests/results. |
| `SRC-LEG-014` | src/ccp_studio/services/deterministic_rendering_service.py | FORK_ADAPT | Separate technical rendering from semantic acceptance. |
| `SRC-LEG-015` | src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py | FORK_SPLIT | Split combined adapter into independent runtime packages. |
| `SRC-LEG-016` | src/ccp_studio/services/remotion_render_adapter_service.py | FORK_ADAPT | Activate against a verified Remotion composer project. |
| `SRC-LEG-017` | src/ccp_studio/services/ffmpeg_finish_adapter_service.py | FORK_ACTIVATE | First-class media editing and post-production. |
| `SRC-LEG-018` | src/ccp_studio/services/remotion_ffmpeg_render_orchestrator_service.py | REPLACE_WITH_PIPELINE_BINDING | The Pipeline binding, not legacy orchestration, chooses an authorized runtime. |
| `SRC-EXT-007` | https://github.com/calesthio/OpenMontage | REFERENCE | Agentic production/editing reference; AGPL review required before code reuse. |
| `SRC-EXT-012` | https://www.remotion.dev/ | REFERENCE | React-based programmatic temporal composition reference. |
| `SRC-EXT-013` | https://hyperframes.video/docs | REFERENCE | HTML/CSS/GSAP deterministic temporal composition reference. |
| `SRC-EXT-014` | https://www.ffmpeg.org/documentation.html | REFERENCE | Media processing, editing, finishing and technical inspection. |

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
