---
title: F22 — Independent Versioning, Architecture Preservation, Readiness, and Development
  Capsule
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F22
governing_decisions:
- D001
- D003
- D021
- D023
- D025
- D026
- D027
- D028
user_journeys:
- UJ-01
- UJ-13
- UJ-14
- UJ-16
functional_requirement_count: 8
---


# F22 — Independent Versioning, Architecture Preservation, Readiness, and Development Capsule

**User outcome:** The Visual Asset Editor can evolve independently while preserving upstream Builder authority, cross-product compatibility, and a verifiable path from PRD to implementation.

## Description

This feature governs product/version relationships, architecture protection, compatibility manifests, migration, readiness states, and the implementation handoff.

## Brownfield baseline

The Atomic Harness Builder architecture and V2.1 target profile are already validated. The new product must preserve them, add the editor-specific delta, and defer shared delegation schemas to a separate PRD.

## Required product delta

Define architecture-preservation contract, version taxonomy, compatibility manifest, pinned runs, migrations, readiness states, compute/evaluator proof, Development Capsule, rollback, and implementation prohibitions.

## Traceability

- **Decisions:** D001, D003, D021, D023, D025, D026, D027, D028
- **User journeys:** UJ-01, UJ-13, UJ-14, UJ-16
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-169 — Preserve the validated Atomic Harness Builder architecture

**Requirement:** The product must treat the Builder lifecycle, Harness IR, Capability Ownership Map, Phase/Context/Contract graphs, JIT Skill architecture, Workflow Runtime, Control Tower, Repair doctrine, Development Capsule, category constitutions, and Content Harness semantic authority as frozen upstream contracts.

**Consequences (testable):

- The preservation contract maps each editor feature to compatible upstream mechanisms.

- An editor implementation cannot redesign these systems without a governed upstream amendment.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-170 — Version product and internal capability layers independently

**Requirement:** The editor product, public contracts, Visual Production Plan IR, capability registries, evaluation profiles, compute profiles, CMF-OKF profile, and category certifications must each declare versions and compatibility.

**Consequences (testable):

- Active runs pin exact versions and hashes.

- A registry update cannot silently alter an in-flight run.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-171 — Publish a release compatibility manifest

**Requirement:** Every release must declare supported Builder target profiles, delegation contract versions, plan IR, category/format profiles, registries, runtimes, certified scope, migration need, and rollback support.

**Consequences (testable):

- Compatibility tests cover every claimed combination.

- Undeclared compatibility cannot be inferred from successful manual use.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-172 — Classify patch, minor, and major change behavior

**Requirement:** Patch changes fix implementation without contract behavior change; minor changes add backward-compatible optional behavior; major changes alter mandatory contracts, lifecycle, authority, hard gates, or canonical IR and require migration.

**Consequences (testable):

- Release tooling validates the declared class against actual schema and behavior changes.

- Breaking changes cannot ship under patch or minor version.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-173 — Run representative compatibility and rollback tests

**Requirement:** Before release, the system must execute current and declared older demand fixtures, Format 02 reference cases, result parsing, geometry, events/exceptions, registry bindings, and rollback to the preceding certified release.

**Consequences (testable):

- Results appear in the release receipt.

- A release with an untested claimed compatibility path cannot be certified.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-174 — Enforce implementation readiness states

**Requirement:** The lifecycle must distinguish PRD_DRAFT, PRD_APPROVED, ARCHITECTURE_IN_PROGRESS, ARCHITECTURE_VALIDATED, CONTRACT_FIXTURES_READY, REFERENCE_SLICE_READY, IMPLEMENTATION_AUTHORIZED, LIMITED_PRODUCTION_CERTIFIED, and PRODUCTION_CERTIFIED.

**Consequences (testable):

- Each state has typed evidence and transition gates.

- PRD_APPROVED cannot be interpreted as implementation authorization.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-175 — Generate a traceable Visual Asset Editor Development Capsule

**Requirement:** Implementation authorization must package approved PRD, decisions, requirements, Architecture, preservation contract, public/internal schemas, representative fixtures, Format 02 reference slice, benchmarks, compatibility, epics/stories, feature specs, and readiness receipt with source traceability.

**Consequences (testable):

- Every generated implementation artifact maps to requirements and architecture nodes.

- A folder of ungoverned scaffolding does not satisfy the capsule.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

### FR-176 — Enforce binding implementation prohibitions

**Requirement:** Readiness must block monolithic general-agent workflows, producer self-approval, blind retries, more than three quality rounds, frequency-only fatigue, OKF as operational truth, uncontrolled high-budget generation, one-failure LoRA training, silent demand relaxation, uncertified scope claims, routine manual ComfyUI operation, or upstream architecture mutation.

**Consequences (testable):

- The readiness report names each prohibition and evidence of compliance.

- Any known violation forces a blocked authorization result.

**Traceability:** Decisions D001, D003, D021, D023, D025, D026, D027, D028; journeys UJ-01, UJ-13, UJ-14, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
