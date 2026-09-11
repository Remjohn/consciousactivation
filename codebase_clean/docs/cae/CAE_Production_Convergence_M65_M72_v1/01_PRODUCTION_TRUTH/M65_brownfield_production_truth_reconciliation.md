# M65 — Brownfield Production Truth Reconciliation

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Produce the definitive current execution map for the live repository and prove or falsify the suspected production-truth defects before any implementation begins.

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

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Read-only inspection and evidence collection. Inspect exact callers, constructors, imports, persistence paths, tests, CLI/API routes and certification code. No production code modification.

## 5. Required Implementation Behavior

Trace:
`operator → Program → state → workflow → state-local context → AgentInvocation → model → output contract → gate → transition → receipt → replay`.

Separately trace the factory command route and SDLF route. Identify where paths converge and diverge.

Produce:
- execution graph;
- authority map;
- synthetic-evidence register;
- production/test execution-mode matrix;
- persistent-store composition matrix;
- M66–M72 implementation dependency plan.

## 6. Verification and Evidence

For every edge provide exact file, symbol, caller, callee, test, persistence authority and claim class.

Explicitly inspect:
- `UnifiedFactoryCommandEngine._live_runs` / `_replays`;
- `FactoryCertificationRunner.run_full_certification`;
- `AgentInvocationRuntime.execute`;
- `SDLFFactoryEngine` Agent-labelled phases;
- `UniversalProgramStateRuntime.__init__`;
- `ProgramOperatorRuntimeService.dispatch_chat_command` and `run_program`;
- PipelineApplication composition.

Build counterexamples for every defect claim.

## 7. Completion / Stop Condition

M65 closes only when the Operator has a source-backed reconciliation sufficient to implement M66–M72 without guessing.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

No source-code changes permitted. Preserve all evidence and contradiction findings.

## 9. Operator Decision

Operator chooses ACCEPT, ACCEPT-WITH-LIMITATIONS, REJECT, or STOP-BLOCKED.

## 10. False-Proof / Reward-Hacking Defense

File existence, README claims, test fixture success, hard-coded phase success and certificate objects are explicitly not proof.

## 11. Out-of-Scope but Recorded

Implementation, provider migration, deployment.
