---
title: F12 — Hybrid Containerized Visual Compute Fabric
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
feature_id: F12
governing_decisions:
- D011
- D013
- D015
- D019
- D021
- D023
- D025
- D027
user_journeys:
- UJ-02
- UJ-05
- UJ-08
- UJ-14
- UJ-16
functional_requirement_count: 8
---


# F12 — Hybrid Containerized Visual Compute Fabric

**User outcome:** A production plan can run reproducibly on compatible local or cloud compute without dependency drift or operator-managed GPU sessions.

## Description

The compute fabric schedules immutable runtime profiles, model mounts, caches, jobs, health, artifacts, and failover across approved worker classes.

## Brownfield baseline

Current bundles describe provider routing but do not supply the product requirements for ComfyUI containers, GPU APIs, custom-node locks, local/cloud parity, autoscaling, and queue operations.

## Required product delta

Define runtime profiles, scheduler inputs, containers, model storage, API job control, health, isolation, caching, local/cloud execution, external fallback, telemetry, and recovery.

## Traceability

- **Decisions:** D011, D013, D015, D019, D021, D023, D025, D027
- **User journeys:** UJ-02, UJ-05, UJ-08, UJ-14, UJ-16
- **Cross-cutting NFRs:** NFR-REL-001, NFR-REL-002, NFR-REL-003, NFR-REL-004, NFR-REL-005, NFR-PERF-001, NFR-PERF-002, NFR-PERF-003, NFR-PERF-004, NFR-PERF-005, NFR-COST-001, NFR-COST-002, NFR-COST-003, NFR-COST-004, NFR-COST-005, NFR-OBS-001, NFR-OBS-002, NFR-OBS-003, NFR-OBS-004, NFR-OBS-005, NFR-SEC-001, NFR-SEC-002, NFR-SEC-003, NFR-SEC-004, NFR-SEC-005, NFR-COMPUTE-001, NFR-COMPUTE-002, NFR-COMPUTE-003, NFR-COMPUTE-004, NFR-COMPUTE-005

## Functional Requirements

### FR-089 — Support a hybrid compute pool

**Requirement:** The scheduler must support certified local workstation GPUs, self-hosted GPU servers, cloud GPU instances, autoscaled temporary workers, and approved external providers through common job contracts.

**Consequences (testable):

- The plan can route according to capability, policy, queue, cost, and availability.

- No single permanent ComfyUI server is required as a product assumption.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-090 — Use immutable container runtime profiles

**Requirement:** Self-hosted jobs must run from digest-pinned OCI images containing approved ComfyUI, Python/CUDA, custom-node lockfile, compiler adapter, API executor, health probes, and telemetry agent.

**Consequences (testable):

- Execution receipts identify the exact image and environment.

- Mutable in-place package installation on a production worker invalidates certification.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-091 — Manage models and LoRAs as versioned mounted resources

**Requirement:** Weights must be hash-verified, registered, mounted or cached separately from container images, and associated with storage, compatibility, and eviction policy.

**Consequences (testable):

- The scheduler confirms every required weight is available or transferable before job start.

- Unverified model files cannot be loaded by production workers.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-092 — Expose a uniform asynchronous worker API

**Requirement:** Certified worker adapters must support submit, status, heartbeat/progress, cancel, result retrieval, logs/receipts, and failure classification.

**Consequences (testable):

- The runtime can replace one compatible worker without changing the canonical plan.

- A worker requiring manual desktop interaction is outside autonomous production scope.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-093 — Route by capability and expected value

**Requirement:** Scheduling must consider workflow/model/control requirements, VRAM, GPU class, queue delay, warm model cache, data locality, expected runtime, cost, privacy policy, maturity, and fallback.

**Consequences (testable):

- The selected runtime and alternatives are preserved in the plan receipt.

- Fastest-available routing cannot bypass compatibility or certification.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-094 — Enforce worker and job isolation

**Requirement:** Jobs must not mutate canonical workflows, model weights, accepted assets, registry state, other jobs, or authoritative demands; experimental custom nodes run in isolated profiles.

**Consequences (testable):

- Fault-injection tests prove cross-job and registry containment.

- A compromised or failed worker can be quarantined without corrupting stored artifacts.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-095 — Recover from worker and provider failure

**Requirement:** The fabric must detect missed heartbeats, container crashes, unavailable GPUs, corrupted caches, API timeouts, and partial uploads, then retry or fail over according to profile policy.

**Consequences (testable):

- Recovery resumes from committed workflow checkpoints and preserves quality-round counts.

- The operator is not required to restart routine failed jobs.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

### FR-096 — Prove local and cloud reference execution

**Requirement:** Implementation authorization requires one self-hosted/local and one cloud container profile to execute representative Format 02 workflows with equivalent contracts, receipts, recovery, and benchmark behavior.

**Consequences (testable):

- The proof pins hardware, image, nodes, weights, workflow, and results.

- Architecture cannot claim a hybrid fabric based only on design documents.

**Traceability:** Decisions D011, D013, D015, D019, D021, D023, D025, D027; journeys UJ-02, UJ-05, UJ-08, UJ-14, UJ-16.

## Feature-specific failure conditions

- A requirement passes structurally but cannot be traced to authoritative demand, plan, event, registry, evidence, or evaluation state.

- A provider or model implementation is treated as the product source of truth.

- The feature weakens semantic sovereignty, category/format authority, or the frozen Atomic Harness Builder architecture.

## Explicitly out of scope

- Detailed implementation technology and file paths, except where needed to define product compatibility or Release 1 proof.

- Shared delegation schema ownership, which belongs to the separate Content Harness ↔ Visual Asset Editor Delegation PRD.
