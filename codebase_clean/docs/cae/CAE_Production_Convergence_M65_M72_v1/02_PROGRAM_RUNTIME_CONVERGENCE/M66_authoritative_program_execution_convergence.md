# M66 — Authoritative Program Execution Convergence

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Replace any duplicate/synthetic factory Program execution path with the existing authoritative Program/State runtime, after M65 proves the exact seam.

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
`packages/ca_runtime/src/ca_runtime/factory_observability.py` in full; `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` around `run_program`, `dispatch_chat_command`, and trace projection.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Only Program RUN/LIST/INSPECT/control/REPLAY dispatch and projection. Reuse ProgramOperatorRuntimeService and UniversalProgramStateRuntime. No new Program engine.

## 5. Required Implementation Behavior

Where M65 confirms duplication:
- inject the existing authoritative Program operator/runtime dependency;
- eliminate mutable duplicate run/replay authority;
- have RUN return the real aggregate/run ID;
- have inspection/replay/floor projections resolve the same canonical state;
- preserve CAS, lane, receipt and tenant rules;
- use persistent state in production composition.

If M65 discovers the existing command surface can already satisfy the requirement, make the smallest integration correction instead of rewriting it.

## 6. Verification and Evidence

Prove:
1. `RUN PROGRAM` produces a real aggregate in authoritative state;
2. returned ID equals stored aggregate ID;
3. replay is built from authoritative transitions;
4. cross-tenant access fails;
5. pause/resume/approve/reject/repair use existing state operations;
6. process restart preserves run state when persistent storage is configured;
7. synthetic-run countertest cannot pass.

No fabricated context hash, phase event or receipt may remain on a production route.

## 7. Completion / Stop Condition

M66 closes when the factory command surface is a pure dispatch/projection boundary over authoritative Program state.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

Rollback only the integration/projection changes. Preserve failing traces.

## 9. Operator Decision

Operator accepts the convergence proof.

## 10. False-Proof / Reward-Hacking Defense

A command returning success without a persisted aggregate/transition/receipt is false proof.

## 11. Out-of-Scope but Recorded

Agent runtime enforcement, certification scoring, deployment.
