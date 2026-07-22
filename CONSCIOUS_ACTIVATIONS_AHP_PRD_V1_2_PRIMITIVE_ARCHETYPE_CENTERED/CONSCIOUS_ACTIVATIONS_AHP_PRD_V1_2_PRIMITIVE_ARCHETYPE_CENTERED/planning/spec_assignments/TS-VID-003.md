---
type: tech_spec_assignment
spec_id: TS-VID-003
title: "Captions, Audio, Evidence, B-Roll, Reframing, and Motion-Slot Planning"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-VID-003.md"
---

# TS-VID-003 — Captions, Audio, Evidence, B-Roll, Reframing, and Motion-Slot Planning

## Controlling product requirements and Stories

**Functional Requirements:** FR-070, FR-142  
**Primary Stories:** ST-04.03

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-EXT-017` | github://browser-use/video-use | REFERENCE | Packed phrase transcript, word-boundary EDL, FFmpeg correctness, rendered cut evaluation, bounded repair, and project memory. |
| `SRC-EXT-018` | github://remotion-dev/remotion | REFERENCE_LICENSE_REVIEW | React/frame source-of-truth rendering, Player, batch rendering, and editor integration. |
| `SRC-EXT-019` | github://heygen-com/hyperframes | REFERENCE | Deterministic HTML/CSS/GSAP motion blocks, skills, registry, Studio, and Player. |
| `SRC-EXT-021` | github://openvideodev/video-editor | REFERENCE_LICENSE_REVIEW | Multi-track timeline, drag/split/trim/snapping, interactive canvas, client-side preview/export patterns. |
| `SRC-EXT-022` | github://lineCode/ai-video-editor | REFERENCE_LICENSE_REVIEW | AI Copilot controlling scripts, visuals, and timeline; UI pattern only. |
| `SRC-LEG-008` | src/ccp_studio/services/video_timeline_service.py | FORK | Deterministic timeline construction. |
| `SRC-LEG-009` | src/ccp_studio/services/video_audio_service.py | FORK | Audio plan and mix metadata. |
| `SRC-LEG-010` | src/ccp_studio/services/video_caption_service.py | FORK | Caption planning contract; renderer-specific realization stays in adapters. |
| `SRC-CUR-014` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F05-composition-intent-image-conditioned-geometry.md | REFERENCE | Composition intent, feasibility, geometry and composition-context evaluation. |

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
