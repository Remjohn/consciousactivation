# TS-07: Ownership, Phase, Context, Contract, Reference, Loading, And Repair Graphs

Status: `SPEC_RATIFIED_PENDING_STORY_MAPPING`

## Traceability

- Owned: FR-060 through FR-080; NFR-ARCH-001.
- Decisions: D003, D007, D012, D013, D014, D015, D016, D017, D018, D019, D020, D021, D025, D026, D030, D033.
- Supporting: NFR-ARCH-002, NFR-PORT-002, NFR-REL-004, NFR-TEST-001, NFR-MAINT-002, NFR-PERF-002, NFR-PERF-003, NFR-SEC-002, NFR-TRACE-001.

## Responsibility And Authority

Own Capability Ownership Map, responsibility-centered modules, Phase Graph, Context Graph, Contract Graph, Reference Graph, Loading Graph, shared dependency/invalidation primitives, and the schema substrate used by the Repair Graph. TS-13 owns repair decisions and authorization. This spec does not execute generated harness phases.

Deterministic code validates graph integrity, compatibility, budgets, and dependency impact. Agents may propose ownership/graph topology with evidence. Humans ratify creative authority, irreversible module boundaries, reference influence, and exceptions.

## Modules And Components

`domain/graphs/{base,capability,phase,context,contract,reference,loading,repair}.py`, `domain/modules.py`, `application/graph_commands.py`, `compilers/graph_views.py`, and `evaluation/graph_integrity.py`.

## Canonical Data Structures

- `Capability { capability_id, outcome, inputs, outputs, invariants, failure_modes, quality_risks }`
- `OwnershipAssignment { capability_ref, owner_kind, owner_ref, rationale, cost_reliability_score, authority, evaluator_ref, fallback }`
- Owner kind: deterministic module, typed model program, JIT skill, reference, human decision, independent evaluator, provider adapter, or hybrid pipeline.
- `Module { module_id, responsibility, owned_capabilities, public_contracts, invariants, exclusions, dependencies, failure_owner, test_seams }`
- `PhaseNode { phase_id, purpose, actor, entry_contracts, exit_contracts, context_policy_ref, skill_recipe_refs, evaluator_refs }`
- `Contract { contract_id, version, producer, consumers, schema_ref, semantic_invariants, compatibility, rewrite_policy=PROHIBITED }`
- `ContextPolicy { phase_ref, required, conditional, prohibited, precedence, budget, overflow=BLOCK }`
- `Reference { reference_id, version, authority, loading_policy, influence_boundary, integrity_hash }`
- `Graph<TNode, TEdge> { graph_id, version, nodes, edges, invariants, source_ir_paths }`

Phase and dependency graphs are acyclic. Repair feedback edges are allowed only with owner, bounded retries, invalidation set, and terminal escalation.

## APIs, Commands, Events, Persistence

- Commands: `AssignCapabilityOwner`, `CompileModules`, `CompilePhaseGraph`, `CompileContextGraph`, `RegisterContract`, `RegisterReference`, `CompileLoadingGraph`, `ValidateGraphSet`.
- Queries: owner lookup, phase predecessors/successors, contract compatibility, context manifest, reference influence, impact closure.
- Events: `CapabilityOwnerAssigned`, `ModuleCompiled`, `GraphCompiled`, `ContractRegistered`, `ReferenceRegistered`, `GraphValidationFailed`.
- Persistence: graph sections in Harness IR; generated graph JSON/Graphviz/Mermaid views as artifacts; compatibility and validation receipts in CAS.

## Dependency, Invalidation, Idempotency, Resume

Graph nodes expose stable IDs and versions. Any owner, contract, context, or reference change computes forward impact through typed edges and invalidates exact phases, recipes, evaluations, and artifacts. Graph compilation is content-addressed. Resume reuses unaffected node validation receipts.

## Security And Isolation

Loading policies are allowlists. `PROHIBITED` references and must-not-influence rules are enforced before context assembly. Contract consumers receive validated payloads, not producer internals. Provider adapters and evaluators cannot acquire semantic authority through topology.

## Observability, Cost, And Performance

Report node/edge counts, orphan/unreachable nodes, ownership ambiguity, contract compatibility, context budget, invalidation fan-out, critical path, parallel-ready sets, and per-phase estimated cost. Graph validation is linear in nodes plus edges and must support at least 10,000 nodes in scale tests.

## Failures And Recovery

Missing ownership, cycles, orphan outputs, duplicate authority, incompatible contracts, unbounded repair loops, or context overflow block compilation. A failed graph revision preserves the prior validated revision. Contradictions route to the owning IR path and decision.

## Acceptance Tests

1. Every required capability has exactly one primary authority assignment.
2. Every module exposes a public contract, failure owner, and test seam.
3. Phase graphs reject cycles and undeclared parallel dependencies.
4. Context overflow blocks; required context is never silently truncated.
5. Downstream payloads cannot rewrite producer-owned fields.
6. Must-not-influence references never appear in phase manifests.
7. A contract change yields exact impact and targeted invalidation.
8. Repair feedback edges require bounds and terminal escalation.

## Implementation Tasks

1. Implement generic typed graph and stable identity library.
2. Define capability, ownership, module, phase, contract, context, reference, loading, and repair schemas.
3. Implement integrity, compatibility, critical-path, and impact algorithms.
4. Implement graph compilers and deterministic views.
5. Add property, scale, security, and invalidation tests.
6. Bind graph outputs into Harness IR, Workflow IR, Control Tower, and TS-13 repair.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Encode source, Builder, human-identity, and downstream execution ownership | graph_and_contract_owner | Builder compiles/validates/receipts; source product captures; human merges identity; downstream executes | ownership edges for Reaction Receipt, Expression Moment, Identity DNA proposal, T/V route, Delegation handoff | Reject ownerless edge, circular authority, or Builder external-runtime capability | authority graph and minimal-repair fixtures | Each cross-product contract has one producer, consumer, authority, failure owner, and repair route | Extends graphs without changing existing phase IDs; new edges invalidate only proven dependents |

## Non-Goals And Migration

No universal creative state machine, external target runtime, or V2.1 graph import is included.
