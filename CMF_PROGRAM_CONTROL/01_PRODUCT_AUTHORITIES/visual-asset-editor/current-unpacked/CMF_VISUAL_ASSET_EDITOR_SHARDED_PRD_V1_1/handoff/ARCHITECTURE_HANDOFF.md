# Visual Asset Editor Architecture Handoff

## Authorized next phase

This PRD authorizes Architecture design only. The Architecture must preserve [`../governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml`](../governance/ARCHITECTURE_PRESERVATION_CONTRACT.yaml), implement every FR/NFR, and prepare the evidence required by the Implementation Authorization Gate.

## Required Architecture views

### 1. System context and authority

- Content Harness, Visual Asset Editor, downstream composition, Builder, Delegation Contract, operator, model providers, compute workers, object storage, and knowledge systems.
- Field-level authority and amendment boundaries.
- Threat and untrusted-input boundaries.

### 2. Canonical data model

- Visual Asset Demand;
- Visual Production Plan IR;
- provider bindings;
- execution graph;
- asset/version/lineage;
- geometry;
- evaluation;
- repair;
- budget;
- memory/usage/recurrence;
- steering knowledge;
- compatibility and release records.

### 3. Workflow runtime

- node/executor model;
- scheduler and queue;
- event store and state projection;
- checkpoints and idempotency;
- infrastructure retry versus quality repair;
- cancellation, backpressure, timeout and circuit breaker;
- dependency-safe parallelism;
- human-exception state.

### 4. Dynamic specialist workcell

- authority manifests;
- activation;
- JIT Skills and Execution Capsules where needed;
- deterministic policy services;
- independent evaluator isolation;
- Asset Commander implementation boundary.

### 5. Visual capability architecture

- registry schemas and services;
- workflow/model/VAE/LoRA/control/runtime compatibility;
- provider-neutral capability query;
- maturity, promotion, shadow and rollback;
- capability-development subsystem.

### 6. ComfyUI/provider compilation

- Visual Production Plan compiler;
- ComfyUI workflow template or graph compiler;
- parameter binding and validation;
- custom-node lock management;
- input preparation;
- result and receipt extraction;
- dry-run validation.

### 7. Visual Compute Fabric

- local/self-hosted and cloud worker profiles;
- Docker/OCI images;
- model/LoRA mounts and cache;
- GPU scheduling;
- API protocol;
- health, heartbeat, cancellation and failover;
- cost and telemetry;
- sandbox isolation and least privilege.

### 8. Evaluation and repair

- deterministic validators;
- asset/composition/syntax/temporal VLM programs;
- evaluator registry and labeled datasets;
- verdict synthesis;
- causal repair compiler;
- invalidation and selective rerun;
- three-round enforcement;
- evaluator disagreement/arbitration.

### 9. Visual Asset Memory and knowledge

- canonical operational memory store;
- usage receipts and syntax fingerprints;
- embeddings and typed knowledge graph;
- recurrence evaluator;
- CMF-OKF projection;
- hybrid retrieval and VLM reranking;
- context compiler and retrieval receipts.

### 10. Service and storage

- asynchronous API and events;
- idempotency;
- object-store URI/hashing;
- authorization;
- public/internal contract boundary;
- result packaging;
- compatibility and deprecation.

### 11. Control Tower and UX contract

- run overview;
- plan and node graph;
- candidate/evaluation comparison;
- geometry/evidence overlays;
- lineage and recurrence;
- GPU/worker operations;
- budget menu;
- exception package;
- release/capability/benchmark views;
- accessibility.

### 12. Release and operations

- product and capability versioning;
- compatibility manifests;
- CI promotion and rollback;
- benchmark runner;
- incident and hotfix workflows;
- backup, retention, and audit;
- readiness evidence collection.

## Mandatory architecture artifacts

```text
ARCHITECTURE.md
AUTHORITY_AND_DELEGATION_MODEL.md
VISUAL_PRODUCTION_PLAN_IR.md
EVENT_AND_WORKFLOW_RUNTIME.md
CAPABILITY_REGISTRY_ARCHITECTURE.md
COMFYUI_COMPILER_ARCHITECTURE.md
VISUAL_COMPUTE_FABRIC.md
VLM_EVALUATION_AND_REPAIR.md
VISUAL_ASSET_MEMORY_AND_RETRIEVAL.md
CMF_OKF_PROFILE_ARCHITECTURE.md
SERVICE_AND_CONTRACT_ARCHITECTURE.md
CONTROL_TOWER_UX_CONTRACT.md
SECURITY_AND_ISOLATION.md
VERSIONING_MIGRATION_ROLLBACK.md
FORMAT02_REFERENCE_ARCHITECTURE.md
ADRs/
```

## Architecture validation

Architecture is not complete until:

- every FR and NFR maps to a component, contract, state, interface, test seam, or operational mechanism;
- no upstream architecture collision remains;
- the Format 02 reference flow is complete end-to-end;
- at least one local and one cloud compute proof plan exists;
- representative contracts can be validated;
- failure, repair, resume, amendment, and rollback are explicit;
- implementation Epics can be vertical and independently valuable.


## Constitutional alignment requirements

Technical specifications must implement the amended Visual Asset Demand and Visual Quality Evaluation contracts, preserve Expression Moment and Activative Intelligence lineage, enforce non-empty wrong-reading locks, and prove that the VAE consumes rather than invents Visual Semantics, Visual Narrative, Feature Contracts, and T/V requests.
