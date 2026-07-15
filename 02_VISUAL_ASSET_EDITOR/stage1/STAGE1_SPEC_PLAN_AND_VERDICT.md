# Stage 1 Technical Specification Plan And Verdict

Generated: 2026-07-14

## Missing technical specifications

Architecture handoff requires, but this repo does not yet contain, the following technical specs/artifacts:

- System architecture and authority/delegation model.
- Canonical data model and Visual Production Plan IR.
- Event/workflow runtime, state machines, idempotency, checkpoints, cancellation, repair, and rollback.
- Capability registry, compatibility manifests, ComfyUI/provider compiler, and visual compute fabric.
- VLM evaluation, repair, evaluator datasets, benchmark runner, and certification gates.
- Visual Asset Memory, CMF-OKF projection, retrieval receipts, and steering recipe lifecycle.
- Async service/API, object storage, security/isolation, observability, Control Tower UX contract, migrations, Development Capsule.

## Proposed feature-spec authoring order

1. Foundation specs: F01, F02, F03, F04, F22.
2. Planning/runtime specs: F05, F06, F07, F08, F09, F10, F12, F19.
3. Evaluation/repair/governance specs: F14, F15, F20, F21.
4. Memory/learning/budget/control specs: F11, F13, F16, F17, F18.

## Feature inventory

- F01: F01 — Product Constitution, Semantic Sovereignty, and Autonomous Authority
- F02: F02 — Visual Asset Demand Contract, Intake, and Authority Validation
- F03: F03 — Canonical Asset Ontology and Reference/Production Separation
- F04: F04 — Immutable Asset Lifecycle, Lineage, Supersession, and Delivery Variants
- F05: F05 — Composition Intent, Feasibility, and Image-Conditioned Geometry
- F06: F06 — Governed Multi-Method Resolution and Strategy Routing
- F07: F07 — Dynamic Specialist Workcell and Authority Boundaries
- F08: F08 — Visual Capability Registry for Workflows, Models, LoRAs, Controls, and Runtimes
- F09: F09 — Visual Production Plan IR and Provider-Specific Compilation
- F10: F10 — Event-Sourced, Resumable Visual Production Runtime
- F11: F11 — Visual Asset Memory, Syntax-Aware Reuse, and Contextual Recurrence
- F12: F12 — Hybrid Containerized Visual Compute Fabric
- F13: F13 — Governed LoRA, Adapter, Control, and Workflow Capability Development
- F14: F14 — Visual Evaluation Profiles and Independent VLM Quality System
- F15: F15 — Typed Visual Repair, Invalidation, and Bounded Reruns
- F16: F16 — Budget Programs, Candidate Portfolios, and Quality-First Selection
- F17: F17 — Visual Steering Intelligence, CMF-OKF Knowledge, and Smart Retrieval
- F18: F18 — Control Tower Specialization and Supervisory Console
- F19: F19 — Asynchronous Visual Asset Service and Delegation Boundary
- F20: F20 — Constraint Conflicts, Feasibility Evidence, and Amendment Proposals
- F21: F21 — Benchmark Portfolio, Staged Certification, and Release 1 Format 02 Slice
- F22: F22 — Independent Versioning, Architecture Preservation, Readiness, and Development Capsule

## Proceed-to-spec verdict

FAIL

Reason: Stage 1 cannot satisfy the user's prerequisite because AGENTS.md is absent, the current validator fails source integrity in this checkout, and there is no brownfield implementation repository available to verify actual code/test coverage or existing V2.1 mechanisms. Specification authoring should wait until these evidence inputs are restored or explicitly waived.