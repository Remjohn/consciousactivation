---
type: tech_spec_assignment
spec_id: TS-AHP-002
title: "AtomicHarnessDefinition Intake and HarnessExecutionBindingManifest"
product_owner: "Atomic Harness Pipeline"
gate: GATE_A
status: CANDIDATE_PENDING_STORY_AND_AUTHORITY_ACCEPTANCE
target_path: "04_ATOMIC_HARNESS_PIPELINE/docs/architecture/TS-AHP-002.md"
---

# TS-AHP-002 — AtomicHarnessDefinition Intake and HarnessExecutionBindingManifest

## Controlling product requirements and Stories

**Functional Requirements:** FR-007, FR-008, FR-009, FR-010, FR-011, FR-012  
**Primary Stories:** ST-03.01

This assignment is not the Tech Spec and grants no path ownership. The writer must use `governance/CURRENT_WRITING_PROFILE.md` and the accepted Story/CBAR mandates.

## Mandatory files and sources to read

| Source ID | Exact path or reference | Disposition | Why it matters |
|---|---|---|---|
| `SRC-CUR-004` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py | REFERENCE | Canonical AtomicHarnessDefinition structure and execution-free status. |
| `SRC-CUR-008` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py | REFERENCE | Current broad Capability Ownership graph and explicit handoff evidence. |
| `SRC-CUR-010` | 01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py | REFERENCE | Execution-free Workflow Node, edge, authority and validation contracts. |
| `SRC-LEG-001` | src/ccp_studio/contracts/studio_pipeline_recipe_harness.py | ADAPT | Old recipe/step contracts become a compatibility input to Workflow IR; they cannot define current meaning. |

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
