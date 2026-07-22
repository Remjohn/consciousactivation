---
type: tech_spec_assignment
spec_id: TS-VID-004
title: "Temporal Embodiment Binding and FFmpeg Production-Correctness"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-VID-004.md"
---

# TS-VID-004 — Temporal Embodiment Binding and FFmpeg Production-Correctness

## Controlling product requirements and Stories

**Functional Requirements:** FR-071, FR-072  
**Primary Stories:** ST-04.04

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-EXT-018` | github://remotion-dev/remotion | REFERENCE_LICENSE_REVIEW | React/frame source-of-truth rendering, Player, batch rendering, and editor integration. |
| `SRC-EXT-019` | github://heygen-com/hyperframes | REFERENCE | Deterministic HTML/CSS/GSAP motion blocks, skills, registry, Studio, and Player. |
| `SRC-EXT-025` | github://MangoLion/stretchystudio | REFERENCE | Layered PSD rigging, mesh deformation, keyframe timeline, shape keys, and 2D animation embodiment. |
| `SRC-LEG-013` | src/ccp_studio/contracts/deterministic_rendering.py | FORK | Renderer-neutral render requests/results. |
| `SRC-LEG-014` | src/ccp_studio/services/deterministic_rendering_service.py | FORK_ADAPT | Separate technical rendering from semantic acceptance. |
| `SRC-LEG-015` | src/ccp_studio/contracts/remotion_ffmpeg_render_adapter.py | FORK_SPLIT | Split combined adapter into independent runtime packages. |
| `SRC-EXT-017` | github://browser-use/video-use | REFERENCE | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-LEG-011` | src/ccp_studio/services/video_media_probe_service.py | FORK | Media inspection via ffprobe. |
| `SRC-LEG-012` | src/ccp_studio/services/video_source_asset_service.py | FORK_ADAPT | Source media registry and lineage. |

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
