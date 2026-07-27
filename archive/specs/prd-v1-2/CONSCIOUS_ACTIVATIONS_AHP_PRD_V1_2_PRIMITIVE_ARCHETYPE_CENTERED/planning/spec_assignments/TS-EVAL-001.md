---
type: tech_spec_assignment
spec_id: TS-EVAL-001
title: "Deterministic and Independent Evaluation Profiles"
product_owner: "Atomic Harness Pipeline + Evaluation Authority"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-EVAL-001.md"
---

# TS-EVAL-001 — Deterministic and Independent Evaluation Profiles

## Controlling product requirements and Stories

**Functional Requirements:** FR-091, FR-092  
**Primary Stories:** ST-09.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-018` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F14-visual-evaluation-profiles.md | REFERENCE | Independent visual evaluation profiles. |
| `SRC-CUR-019` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md | REFERENCE | Typed visual repair and bounded reruns. |
| `SRC-LEG-019` | src/ccp_studio/contracts/render_qa.py | FORK | Technical QA contracts and receipts. |
| `SRC-LEG-020` | src/ccp_studio/services/render_qa_service.py | FORK_ADAPT | Add Visual Syntax reparse and separate technical vs creative evaluation. |
| `SRC-LEG-021` | src/ccp_studio/services/ffprobe_validation_service.py | FORK_ACTIVATE | Technical media validation. |
| `SRC-LEG-022` | src/ccp_studio/services/frame_sampling_service.py | FORK_ACTIVATE | Deterministic frame sampling for review/evaluation. |
| `SRC-LEG-023` | src/ccp_studio/services/audio_level_analysis_service.py | FORK_ACTIVATE | Audio-level evidence. |

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
