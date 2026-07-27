---
type: tech_spec_assignment
spec_id: TS-AHP-003
title: "Source-Backed Content Batch, Archetype Routing, and Derivative Job Contracts"
product_owner: "Atomic Harness Pipeline"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-AHP-003.md"
---

# TS-AHP-003 — Source-Backed Content Batch, Archetype Routing, and Derivative Job Contracts

## Controlling product requirements and Stories

**Functional Requirements:** FR-133, FR-134, FR-135, FR-136  
**Primary Stories:** ST-03.02, ST-03.03

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-AM-001` | CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1(2).zip | AMENDMENT_INPUT | Format 02 deferral, HumanResolutionEpisode, supervisory Studio, autonomy modes, timeline adoption, and Revision Compiler. |
| `SRC-AM-002` | PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip | AMENDMENT_INPUT | Parallel Pipeline, temporal, static, VAE, Interview Expression, GNM, and retrieval/model-program activation lanes. |
| `SRC-INT-001` | THE_CMF_STUDIO(2).zip::05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md | ADAPT | Interview-first source-to-asset product model and Complete Expression Session concepts. |
| `SRC-INT-003` | THE_CMF_STUDIO(2).zip::CCP V9.1 Expression Capture & Archetype Routing Update.md | ADAPT | Expression Moment and archetype-routing refinements. |
| `SRC-CUR-004` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py | REFERENCE | Canonical AtomicHarnessDefinition structure and execution-free status. |
| `SRC-CUR-007` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/category_runtime_rules.py | REFERENCE | Category-native runtime plan requirements, evaluation dimensions and repair units. |
| `SRC-EXT-023` | github://SamurAIGPT/AI-Youtube-Shorts-Generator | REFERENCE | Long-video chunking with overlap, deduplication, caching, structured JSON, and vertical crop patterns. |

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
