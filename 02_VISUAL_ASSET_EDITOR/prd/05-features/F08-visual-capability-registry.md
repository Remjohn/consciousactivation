---
title: F08 — Visual Capability Registry for Workflows, Models, LoRAs, Controls, and
  Runtimes
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F08
governing_decisions:
- D011
- D015
- D016
- D017
- D019
- D025
- D027
user_journeys:
- UJ-02
- UJ-10
- UJ-11
- UJ-13
- UJ-14
functional_requirement_count: 8
---


# F08 — Visual Capability Registry for Workflows, Models, LoRAs, Controls, and Runtimes

**User outcome:** A production plan can select only capabilities whose purpose, compatibility, quality, cost, and failure behavior are known and tested.

## Description

The registry is the governed discovery and compatibility layer for ComfyUI and other visual production resources.

## Brownfield baseline

V2.1 anticipates provider routing and adapters but does not define the full versioned capability catalog needed for autonomous local-model production.

## Required product delta

Create registry schemas, status and maturity, compatibility edges, benchmark evidence, parameter envelopes, runtime binding, experimental promotion, and change impact.

## Traceability

- **Decisions:** D011, D015, D016, D017, D019, D025, D027
- **User journeys:** UJ-02, UJ-10, UJ-11, UJ-13, UJ-14
- **Cross-cutting NFRs:** NFR-TRACE-001, NFR-TRACE-002, NFR-TRACE-003, NFR-TRACE-004, NFR-TRACE-005, NFR-COMPAT-001, NFR-COMPAT-002, NFR-COMPAT-003, NFR-COMPAT-004, NFR-COMPAT-005, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004, NFR-EVAL-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005, NFR-GOV-001, NFR-GOV-002, NFR-GOV-003, NFR-GOV-004, NFR-GOV-005

## Functional Requirements

### FR-057 — Register ComfyUI workflow profiles

**Requirement:** Every workflow profile must declare version, status, supported operations and asset families, required controls, compatible models and runtime profiles, geometry features, expected resources, benchmarks, known failures, and compiler adapter.

**Consequences (testable):

- The router can prove a workflow satisfies the plan’s capability requirements.

- Ad hoc workflow JSON cannot run as a production profile.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-058 — Register models, checkpoints, and VAEs

**Requirement:** Model records must pin architecture, hash, supported resolutions and operations, compatible text encoders/VAEs/workflows, VRAM, strengths, weaknesses, licensing/source policy class, benchmarks, and certified scope.

**Consequences (testable):

- Production binding fails when a required model relationship is incompatible.

- A filename alone cannot identify a production model.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-059 — Register LoRAs and adapters

**Requirement:** LoRA and adapter records must define base-model compatibility, intended capabilities, strength envelope, prohibited combinations, known failures, benchmark evidence, training provenance, and maturity.

**Consequences (testable):

- The compiler validates every stack and strength before execution.

- An experimental or incompatible LoRA cannot silently enter a production run.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-060 — Register conditioning and control profiles

**Requirement:** ControlNet, IP-Adapter, pose, depth, edge, mask, identity, regional prompting, camera, motion, and other controls must declare required inputs, applicable workflows, controllability, limits, and evaluator requirements.

**Consequences (testable):

- Plans can request capabilities independent of provider-specific node names.

- A missing control dependency creates a capability blocker rather than best-effort improvisation.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-061 — Register compute runtime profiles

**Requirement:** Runtime profiles must pin container digest, ComfyUI and Python/CUDA compatibility, custom-node lockfile, hardware class, model mounts, API, health checks, concurrency, timeouts, cache behavior, and certification.

**Consequences (testable):

- The scheduler chooses only profiles compatible with every bound capability.

- A worker with an unregistered environment cannot receive production jobs.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-062 — Maintain typed compatibility relationships

**Requirement:** The registry must model requires, compatible-with, conflicts-with, supersedes, validated-on, and prohibited-with relationships across workflows, models, VAEs, LoRAs, controls, nodes, evaluators, and runtimes.

**Consequences (testable):

- Registry validation catches broken or cyclic mandatory dependencies.

- Compatibility cannot be inferred only from names or human memory.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-063 — Promote capabilities through maturity states

**Requirement:** New or changed capabilities must move through experimental, benchmarked, shadow, limited-production, production, deprecated, and retired states with evidence and rollback.

**Consequences (testable):

- Production routing excludes capabilities below the requested policy level.

- Registry edits cannot change an active run’s pinned bindings.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

### FR-064 — Expose capability evidence and change impact

**Requirement:** The Control Tower and architecture tools must show benchmark results, cost and latency envelopes, known limitations, dependent plans/harnesses, and required regression suites for each capability.

**Consequences (testable):

- A proposed registry update calculates its blast radius before promotion.

- A capability with unknown dependent certified paths cannot be removed.

**Traceability:** Decisions D011, D015, D016, D017, D019, D025, D027; journeys UJ-02, UJ-10, UJ-11, UJ-13, UJ-14.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
