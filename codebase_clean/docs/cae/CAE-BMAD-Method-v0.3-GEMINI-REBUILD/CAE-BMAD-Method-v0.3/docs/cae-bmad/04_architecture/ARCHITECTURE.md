# Architecture Specification — Conscious Activation Engine Core Architecture

**Artifact ID:** CAE-ART-ARCH-001  
**Status:** APPROVED  

---

## 1. Subsystems

| Subsystem ID | Name | Responsibility | Bound Services |
|---|---|---|---|
| `SUB-WORLD-INTEL` | World Signal Ingestion Subsystem | Ingests raw media signals, verifies source provenance hashes, checks wire inflation, and normalizes telemetry. | `services/world-intelligence/` |
| `SUB-PIPELINE-ENGINE` | Deterministic Workflow & Compiler Subsystem | Compiles multi-agent DAGs, validates step schemas, and orchestrates deterministic state transitions. | `services/pipeline/` |
| `SUB-RUNTIME-CORE` | Conscious Activation Runtime Core | Provides JIT context capsules, CAS state machine runtimes, and typed agent invocation harnesses. | `packages/ca_runtime/` |
| `SUB-STUDIO-UI` | Operator Studio & Visual Telemetry Subsystem | Renders operator dashboards, telemetry monitors, and Atomic Harness visual syntax tokens. | `atomic_harnesses_visual_syntax/` |

---

## 2. Interface Boundaries

| Interface Name | Type | Contract Schema |
|---|---|---|
| `ResearchSignalIngestionAPI` | `REST_API` | `schemas/research_source.schema.json` |
| `WorkflowExecutionPlanInterface` | `INTERNAL_PYTHON_API` | `schemas/workflow_factory_map.schema.json` |
| `ProgramStateCASInterface` | `INTERNAL_PYTHON_API` | `docs/cae/constitutions/CA-CAN-02_STATE_AGGREGATE.yaml` |

---

## 3. Communication Protocols

- HTTP/2 REST
- Internal Asynchronous Python Callables
- CAS Optimistic Locking

---

## 4. Brownfield Integration Strategy

The architecture directly incorporates existing Python packages (ca_runtime) and microservices (world-intelligence, pipeline), wrapping them in typed schema boundaries rather than rewriting them.

---

## 5. Security & Governance Controls

All state transitions guarded by Compare-And-Swap version checks; all operator promotions require explicit gate ratification.
