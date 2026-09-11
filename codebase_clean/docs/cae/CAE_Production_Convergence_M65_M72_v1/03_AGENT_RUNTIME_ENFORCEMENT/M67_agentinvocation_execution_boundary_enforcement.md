# M67 — AgentInvocation Execution Boundary Enforcement

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Enforce the existing AgentInvocation boundary for production Agent work and prevent the deterministic fallback path from becoming certification evidence.

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
`packages/ca_runtime/src/ca_runtime/agent_invocation.py` around `AgentInvocationCompiler` and `AgentInvocationRuntime.execute`.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Trace all production Agent-callers. Add the minimum execution-mode classification required to distinguish test hooks from production execution. Fail closed in production when no real governed inference path is present.

## 5. Required Implementation Behavior

Reuse AgentInvocationCompiler/Runtime. Preserve test hooks under explicit test classification. Production executions must produce AgentInvocationReceipt evidence tied to invocation/package/capsule/model/provider data. Direct ModelReasoningEngine calls must not bypass AgentInvocation for production Agent work.

## 6. Verification and Evidence

Required countertests:
- missing production executor/provider blocks;
- deterministic fallback cannot satisfy production evidence;
- invocation tamper fails;
- unauthorized tool fails;
- invalid output fails;
- provider-backed invocation emits receipt.

Produce static caller graph and runtime trace for one genuine invocation.

## 7. Completion / Stop Condition

M67 closes when every production Agent path is either demonstrably governed by AgentInvocation or explicitly classified as deterministic non-Agent work.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

Rollback execution-boundary changes only.

## 9. Operator Decision

Operator accepts the boundary proof.

## 10. False-Proof / Reward-Hacking Defense

A receipt generated via test `inference_fn` is integration evidence only, never production-provider evidence.

## 11. Out-of-Scope but Recorded

Program adapter and deployment.
