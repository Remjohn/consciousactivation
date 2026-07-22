---
type: tech_spec_assignment
spec_id: TS-PM-001
title: "Programmed Model Artifact, Claim, Model Program, Lifecycle, and Resolver"
product_owner: "Atomic Harness Pipeline"
gate: GATE_B
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-PM-001.md"
---

# TS-PM-001 — Programmed Model Artifact, Claim, Model Program, Lifecycle, and Resolver

## Controlling product requirements and Stories

**Functional Requirements:** FR-037, FR-038, FR-039, FR-040, FR-041, FR-042  
**Primary Stories:** ST-07.03

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-008` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py | REFERENCE | Current broad Capability Ownership graph and explicit handoff evidence. |
| `SRC-CUR-015` | 02_VISUAL_ASSET_EDITOR/prd/05-features/F08-visual-capability-registry.md | REFERENCE | Versioned models, LoRAs, controls, workflows and runtime capability registry. |
| `SRC-EXT-001` | file:///mnt/data/Agentic Prompt Enhancer for Image Generation and.pdf | REFERENCE | Trainable small prompt enhancers; router–rewriter–composer and downstream-output reward. |
| `SRC-EXT-002` | https://huggingface.co/openbmb/MiniCPM5-1B | REFERENCE | 1.08B candidate for compact structured Programmed Models; benchmark before adoption. |
| `SRC-EXT-003` | https://huggingface.co/Qwen/Qwen3.5-4B | REFERENCE | 4B multimodal candidate for visual planning and diagnosis. |
| `SRC-EXT-004` | https://huggingface.co/Qwen/Qwen3.6-27B | REFERENCE | 27B multimodal teacher and difficult-case reference. |
| `SRC-EXT-006` | https://github.com/cactus-compute/needle | REFERENCE | Late compression candidate for stable atomic operation routing. |

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
