---
title: Cross-Cutting Non-Functional Requirements
product: CMF Visual Asset Editor
version: 0.2.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
nfr_count: 70
---


# Cross-Cutting Non-Functional Requirements

These requirements apply across feature boundaries. Feature shards reference the full applicable groups through stable IDs.

## Semantic and Activative Integrity (`NFR-SEM`)

### NFR-SEM-001 — Preserve demand authority

**Requirement:** The system must not change authorized semantic intent, Activative function, sequence role, composition role, identity, continuity, or wrong-reading constraints outside a new approved demand version.

### NFR-SEM-002 — Separate observation from inference

**Requirement:** Visual observations, derived geometry, VLM interpretations, generated proposals, and human-authorized decisions must remain explicitly typed and traceable.

### NFR-SEM-003 — Hard-gate meaning failures

**Requirement:** A technically attractive asset with failed semantic or Activative fidelity must be ineligible for acceptance.

### NFR-SEM-004 — Preserve category and format context

**Requirement:** Evaluation, memory, and routing must retain the requesting category, format profile, atomic harness, and Visual Syntax role.

### NFR-SEM-005 — Prevent silent demand degradation

**Requirement:** Budget, queue pressure, provider failure, or workflow fallback must not lower semantic or composition quality thresholds without a typed amendment.

## Reliability and Recovery (`NFR-REL`)

### NFR-REL-001 — Idempotent submissions

**Requirement:** Identical demand versions and idempotency keys must not create duplicate production runs.

### NFR-REL-002 — Resumable workflows

**Requirement:** Committed nodes must resume from checkpoints after interruption without replaying valid work.

### NFR-REL-003 — Bounded quality repair

**Requirement:** Quality repair must stop after three rounds and transition to a typed terminal or exception state.

### NFR-REL-004 — Failure containment

**Requirement:** A node or worker failure must not mutate unrelated jobs, accepted assets, canonical registries, or authoritative contracts.

### NFR-REL-005 — Rollback readiness

**Requirement:** Certified releases and capability versions must support rollback with preserved asset and execution lineage.

## Performance and Latency (`NFR-PERF`)

### NFR-PERF-001 — Budget-class latency targets

**Requirement:** Each Budget Program must define expected queue, production, evaluation, and total wall-clock envelopes.

### NFR-PERF-002 — Node-level timing

**Requirement:** Every production and evaluation node must emit start, completion, duration, queue, and wait telemetry.

### NFR-PERF-003 — Efficient checkpoint reuse

**Requirement:** Repairs and resumes must reuse non-invalidated deterministic work, references, controls, and accepted intermediate assets.

### NFR-PERF-004 — Adaptive early stopping

**Requirement:** Candidate exploration may stop when a passing candidate exceeds configured confidence and expected additional value is low.

### NFR-PERF-005 — No hidden latency degradation

**Requirement:** Model, workflow, container, or evaluator updates must be benchmarked for p50 and p95 latency changes before promotion.

## Cost and Compute Governance (`NFR-COST`)

### NFR-COST-001 — Pre-execution estimate

**Requirement:** Every production plan must estimate GPU time, candidate count, evaluator depth, storage, and monetary cost before execution.

### NFR-COST-002 — Hard budget enforcement

**Requirement:** Runs must block or request approval before exceeding the selected Budget Program or caller authorization.

### NFR-COST-003 — Cost-per-accepted-asset accounting

**Requirement:** Receipts must report total and marginal cost, failed candidate cost, repair cost, and accepted-output cost.

### NFR-COST-004 — Compute-value routing

**Requirement:** The router must select the least costly certified capability expected to meet required quality and latency.

### NFR-COST-005 — Learning budget separation

**Requirement:** Exploration and capability-learning compute must be labeled separately from ordinary production cost.

## Traceability and Reproducibility (`NFR-TRACE`)

### NFR-TRACE-001 — Immutable execution identity

**Requirement:** Each run must pin demand, plan, workflow, model, VAE, LoRA, control, custom-node, container, evaluator, and runtime identities and hashes.

### NFR-TRACE-002 — Asset lineage completeness

**Requirement:** Every Production Asset and delivery variant must trace to source evidence, parent versions, transformations, candidates, evaluations, and promotion events.

### NFR-TRACE-003 — Contract-to-output traceability

**Requirement:** Every accepted asset must trace to the exact demand fields and quality gates it satisfies.

### NFR-TRACE-004 — Knowledge provenance

**Requirement:** Every CMF-OKF concept and Steering Recipe must reference canonical records, evidence, benchmarks, authority class, and validity.

### NFR-TRACE-005 — Published-version preservation

**Requirement:** Published compositions must remain linked to the exact asset versions they used even after supersession.

## Observability and Control Tower (`NFR-OBS`)

### NFR-OBS-001 — Event completeness

**Requirement:** Every meaningful lifecycle transition, blocker, repair, amendment, cost change, and promotion must emit a typed event.

### NFR-OBS-002 — Evidence-backed status

**Requirement:** The Control Tower must show why a status exists and link to the governing contract, node, receipt, and evidence.

### NFR-OBS-003 — Operational drill-down

**Requirement:** Operators must inspect demand, plan, memory retrieval, candidate, evaluation, repair, compute, and delivery state without accessing hidden reasoning.

### NFR-OBS-004 — Cross-run analytics

**Requirement:** The product must aggregate completion, failure, repair, cost, latency, intervention, recurrence, and capability-gap metrics.

### NFR-OBS-005 — Human action receipts

**Requirement:** Every operator exception, budget authorization, degraded acceptance, cancellation, or promotion action must be receipted.

## Security and Isolation (`NFR-SEC`)

### NFR-SEC-001 — Least privilege

**Requirement:** Nodes and workers receive only declared sources, object-store paths, credentials, tools, models, network destinations, and write permissions.

### NFR-SEC-002 — Sandboxed experimental capability

**Requirement:** Uncertified workflows, nodes, models, LoRAs, or custom nodes must run in isolated experimental environments.

### NFR-SEC-003 — Secret hygiene

**Requirement:** Secrets must never be embedded in demands, plans, capsules, events, OKF concepts, artifacts, or logs.

### NFR-SEC-004 — Untrusted input handling

**Requirement:** Natural-language notes, reference files, workflow metadata, and retrieved knowledge must be treated as data and cannot override system authority.

### NFR-SEC-005 — Asset and model integrity

**Requirement:** Downloaded or mounted models, LoRAs, custom nodes, and containers must be hash-verified against approved registry records.

## Compatibility and Versioning (`NFR-COMPAT`)

### NFR-COMPAT-001 — Versioned service contracts

**Requirement:** Demand, event, result, geometry, evaluation, repair, budget, and exception contracts must declare semantic versions.

### NFR-COMPAT-002 — Backward-compatible minor evolution

**Requirement:** Minor releases may add optional fields or capabilities without breaking declared compatible callers.

### NFR-COMPAT-003 — Explicit major migrations

**Requirement:** Breaking contract, lifecycle, hard-gate, or authority changes require major versions, migration plans, compatibility tests, and rollback.

### NFR-COMPAT-004 — Pinned run dependencies

**Requirement:** An active run may not silently adopt newer registry, workflow, model, evaluator, or runtime versions.

### NFR-COMPAT-005 — Compatibility manifest

**Requirement:** Every product release must publish tested Builder profile, delegation contract, category profile, registry, and runtime compatibility.

## Evaluation and Certification (`NFR-EVAL`)

### NFR-EVAL-001 — Independent evaluation

**Requirement:** The production model or materializer cannot be the sole approver of its own output.

### NFR-EVAL-002 — Profile-specific hard gates

**Requirement:** Each asset family and production route must use a certified evaluation profile with explicit thresholds and failure codes.

### NFR-EVAL-003 — Evaluator calibration

**Requirement:** VLM evaluators must be tested for failure recall, false rejection, failure-code accuracy, responsible-layer accuracy, recurrence judgment, and confidence calibration.

### NFR-EVAL-004 — Protected release benchmarks

**Requirement:** Certification must include representative, adversarial, mutation, repair, recurrence, recovery, and compatibility cases not exposed as runtime hints.

### NFR-EVAL-005 — No average compensation

**Requirement:** Aggregate scores cannot compensate for failed semantic, Activative, composition, technical-validity, reproducibility, or evaluator hard gates.

## Memory and Knowledge Retrieval (`NFR-MEM`)

### NFR-MEM-001 — Contextual usage memory

**Requirement:** Memory must store rendered use, Visual Syntax role, Activative function, composition relationships, recurrence intent, and VLM verdict.

### NFR-MEM-002 — Authority-aware retrieval

**Requirement:** Retrieval must filter knowledge by lifecycle status, authority class, compatibility, category, format, asset family, and current contract.

### NFR-MEM-003 — Hybrid multimodal retrieval

**Requirement:** Search must support lexical, semantic, image, composition, syntax-fingerprint, and graph signals.

### NFR-MEM-004 — Contradiction and exception coverage

**Requirement:** Context compilation must include applicable counterexamples, exceptions, superseding knowledge, and material contradictions.

### NFR-MEM-005 — Minimum Complete Context

**Requirement:** Retrieval must compile the smallest sufficient knowledge package and record included, excluded, and compressed resources.

## Visual Compute Fabric (`NFR-COMPUTE`)

### NFR-COMPUTE-001 — Immutable runtime profiles

**Requirement:** Self-hosted jobs must use digest-pinned container images, ComfyUI versions, custom-node lockfiles, and system dependencies.

### NFR-COMPUTE-002 — Capability-aware scheduling

**Requirement:** Jobs must route by required workflow, model, control, VRAM, queue, cache locality, cost, latency, and certified fallback.

### NFR-COMPUTE-003 — Worker health and recovery

**Requirement:** Workers must expose health checks, job heartbeats, cancellation, timeout, artifact extraction, and replacement behavior.

### NFR-COMPUTE-004 — Resource isolation

**Requirement:** Concurrent jobs must not mutate models, workflows, assets, caches, or execution state belonging to other jobs.

### NFR-COMPUTE-005 — Local-cloud equivalence testing

**Requirement:** Certified local and cloud profiles must pass equivalent representative demand, output-contract, and recovery tests.

## Supervisory Experience and Accessibility (`NFR-UX`)

### NFR-UX-001 — Policy-first controls

**Requirement:** The primary UI must expose budgets, priorities, experiment policies, exceptions, and authorization rather than requiring node-level production work.

### NFR-UX-002 — Clear exceptional decisions

**Requirement:** Human-review packages must explain trigger, attempted repairs, preserved state, unresolved dimensions, choices, and consequences.

### NFR-UX-003 — Visual evidence inspection

**Requirement:** Operators must inspect candidate comparisons, BBOX evidence, VLM evidence regions, composition renders, lineage, and recurrence contexts.

### NFR-UX-004 — Accessible Control Tower

**Requirement:** Core supervisory surfaces must support keyboard navigation, readable status language, sufficient contrast, and non-color-only state cues.

### NFR-UX-005 — No routine approval burden

**Requirement:** Passing routine jobs must complete without operator approval, manual candidate selection, prompt editing, or job restart.

## Workflow Runtime (`NFR-WORKFLOW`)

### NFR-WORKFLOW-001 — Typed production nodes

**Requirement:** Every node must declare actor type, inputs, outputs, dependencies, validators, timeouts, retries, checkpoint, invalidation, and events.

### NFR-WORKFLOW-002 — Deterministic orchestration

**Requirement:** Routing, dependency resolution, contract validation, lifecycle transitions, and budget enforcement must be code-owned.

### NFR-WORKFLOW-003 — Infrastructure-quality separation

**Requirement:** Infrastructure retries and quality repairs must be independently classified, metered, and limited.

### NFR-WORKFLOW-004 — Dependency-safe parallelism

**Requirement:** Parallel candidates or preparation nodes require proven independence, bounded concurrency, cancellation, and merge semantics.

### NFR-WORKFLOW-005 — Workflow integration testing

**Requirement:** Tests must verify gating, resume, selective invalidation, service events, compute failover, and terminal-state correctness.

## Governance and Authority (`NFR-GOV`)

### NFR-GOV-001 — Upstream architecture preservation

**Requirement:** The product must not alter the validated Atomic Harness Builder architecture or shared Activative authority model.

### NFR-GOV-002 — Demand-owner authority

**Requirement:** Only the owning Content Harness may approve demand-level semantic, Activative, sequence, or composition amendments.

### NFR-GOV-003 — Registry promotion governance

**Requirement:** Capabilities and knowledge move through explicit experimental, benchmarked, shadow, limited, production, deprecated, and retired states.

### NFR-GOV-004 — Implementation authorization

**Requirement:** Architecture and implementation may proceed only through the formal readiness gates and receipts defined by the product.

### NFR-GOV-005 — Certified-scope honesty

**Requirement:** The product must clearly distinguish structurally represented, experimental, limited-production, and fully certified asset families and profiles.
