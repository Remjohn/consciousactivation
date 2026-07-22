---
type: tech_spec_assignment
spec_id: TS-REL-001
title: "Format 02 Deferral, Historical Evidence Isolation, and Future Activation Gate"
product_owner: "Program Control"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "CMF_PROGRAM_CONTROL/docs/architecture/TS-REL-001.md"
---

# TS-REL-001 — Format 02 Deferral, Historical Evidence Isolation, and Future Activation Gate

## Controlling product requirements and Stories

**Functional Requirements:** FR-079, FR-080, FR-081, FR-082, FR-083, FR-084  
**Primary Stories:** ST-11.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-AM-001` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | AMENDMENT_INPUT | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-CUR-006` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/format_profiles.py | REFERENCE | Current edited-video, Format 02 and conversational profile identities. |
| `SRC-CUR-021` | 02_VISUAL_ASSET_EDITOR/CURRENT_PROJECT_STATUS.md | REFERENCE | Public VAE implementation/evidence status and Stage 5 gate. |
| `SRC-MIG-001` | CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1(1).md | REFERENCE | Defines brownfield reuse/adapt/rewrite/archive treatment for the CMF Studio predecessor. |
| `SRC-EXT-018` | github://remotion-dev/remotion | REFERENCE_LICENSE_REVIEW | React/frame source-of-truth rendering, Player, batch rendering, and editor integration. |
| `SRC-EXT-019` | github://heygen-com/hyperframes | REFERENCE | Deterministic HTML/CSS/GSAP motion blocks, skills, registry, Studio, and Player. |
| `SRC-EXT-025` | github://MangoLion/stretchystudio | REFERENCE | Layered PSD rigging, mesh deformation, keyframe timeline, shape keys, and 2D animation embodiment. |

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
