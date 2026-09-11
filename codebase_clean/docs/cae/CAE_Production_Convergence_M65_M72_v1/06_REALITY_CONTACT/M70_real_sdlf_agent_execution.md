# M70 — Real SDLF Agent Execution

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Wire SDLF Agent-labelled phases through the real AgentInvocation boundary while retaining deterministic code functions for deterministic phases.

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
`sdlf_factory.py` around `run`, `_execute_scout`, `_execute_plan`, `_execute_build`, `_execute_quality`, `_execute_review`, `_execute_repair`, `_execute_document`.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

SCOUT, PLAN, BUILD, REVIEW, REPAIR and DOCUMENT Agent phases; preserve sandbox controls, Quality deterministic gate, INTEGRATE/SHIP/OBSERVE semantics.

## 5. Required Implementation Behavior

For each Agent phase:
Agent resolution → package/context compilation → AgentInvocation → real governed execution → typed output validation → receipt → phase result.

QUALITY remains deterministic code. BUILD retains sandbox/path constraints. REVIEW cannot auto-approve without Agent evidence. REPAIR remains bounded and revalidated.

## 6. Verification and Evidence

Run one real SDLF execution with:
- AgentInvocation evidence for every Agent phase;
- deterministic evidence for code phases;
- sandbox test;
- unauthorized model/tool test;
- quality failure test;
- bounded repair test;
- operator ship gate test.

No fake inference hook counts as production-provider evidence.

## 7. Completion / Stop Condition

M70 closes only when the SDLF trace contains genuine AgentInvocation receipts for Agent phases and truthful deterministic evidence for code phases.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

Rollback SDLF Agent adapter changes.

## 9. Operator Decision

Operator accepts real SDLF Agent execution.

## 10. False-Proof / Reward-Hacking Defense

`work_unit_kind=AGENT_CALL` plus `success=True` is insufficient evidence.

## 11. Out-of-Scope but Recorded

Domain Program certification and deployment.
