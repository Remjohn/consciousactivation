# M68 — State + Observability + Persistence Convergence

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Make persistent Program state the sole operational truth and ensure StateM-aligned context/transition behavior and observability all project that authority.

## 2. Governing Doctrine and Authority

Subordinate to the current CAE Constitution, `docs/PRD/CURRENT.md`, M49–M64 authority map, StateM alignment contract, current Program/State/Workflow/Agent/Skill/Receipt constitutions, and applicable `AGENTS.md` files. Reuse existing canonical authorities. External references are patterns only; they are never CAE authority.

The governing laws are:
- existing CAE constitutional precedence remains highest authority;
- Program/State/Workflow/Agent/Skill/Receipt authorities are reused, not replaced;
- implementation claims require brownfield evidence;
- code owns deterministic control flow; Agents own bounded reasoning;
- state is a context-and-contract boundary;
- certification cannot create evidence it did not observe.

## 3. Mandatory Reading Before Action

`docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md`
`governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml`
`docs/PRD/CURRENT.md`
`services/pipeline/AGENTS.md`
`packages/ca_runtime/src/ca_runtime/agent_invocation.py`
`packages/ca_runtime/src/ca_runtime/agent_registry.py`
`packages/ca_runtime/src/ca_runtime/context_capsule.py`
`packages/ca_runtime/src/ca_runtime/program_registry.py`
`packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
`packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
`packages/ca_runtime/src/ca_runtime/factory_observability.py`
`packages/ca_runtime/src/ca_runtime/factory_certification.py`
`packages/ca_runtime/src/ca_runtime/sdlf_factory.py`
`services/pipeline/src/cmf_pipeline/application.py`
`services/pipeline/src/cmf_pipeline/workflow/application/compiler.py`
`services/pipeline/src/cmf_pipeline/workflow/application/run_service.py`
Current M49–M64 bundle, especially its authority map, StateM contract, M52, M57–M60, M63 and M64.
`program_state_runtime.py` around `UniversalProgramStateRuntime`, SQLite store, `set_lifecycle`, `repair_state`, `get_local_context`, and transition persistence.
`program_operator_runtime.py` around `project_execution_trace`.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Production composition of Program state, operator projections, replay, state-local context and transition evidence.

## 5. Required Implementation Behavior

Required:
- explicitly compose durable state for production runs;
- preserve CAS and transition receipt generation;
- verify state-local context is recomputed at boundaries;
- failed blocking checks keep the source state;
- observability reads aggregate/transition/context authority;
- no second mutable run/replay store;
- state version/hash remains continuous across repair and retry.

## 6. Verification and Evidence

Demonstrate:
- run creation;
- state transition;
- context refresh;
- operator inspect;
- process restart and re-read;
- replay;
- failed transition remains in source state;
- tenant isolation.

Countertests must detect stale-context reuse and synthetic replay.

## 7. Completion / Stop Condition

M68 closes when one persisted Program aggregate can be controlled, inspected, context-refreshed and replayed through the same authority.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

Rollback only composition/projection changes.

## 9. Operator Decision

Operator accepts the persistent/state-observability convergence.

## 10. False-Proof / Reward-Hacking Defense

A UI string, cached trace or in-memory list is not authoritative evidence.

## 11. Out-of-Scope but Recorded

Certification scoring and deployment.
