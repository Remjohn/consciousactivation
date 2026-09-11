# M71 — Real Domain Program Golden Run + Benchmark

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Execute and measure the first genuinely end-to-end representative domain Program using the canonical Program, State, Workflow, Context, AgentInvocation, Gate and Receipt authorities.

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
`programs/research_canonicalization_program/` and its `CAE.md`, manifest and Skills.
`program_operator_runtime.py` run/trace methods.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Run the representative `research_canonicalization_program` through the authoritative runtime established by M66–M70. Perform at least three runs: normal success, induced bounded repair, and a negative case that must stop before unsafe progression.

## 5. Required Implementation Behavior

Every run must produce an evidence manifest linking operator command, aggregate, program/version, state history, workflow transitions, context refreshes, AgentInvocation hashes, receipts, gates, and replay.

Benchmark phase/receipt counts from observed records only. Do not infer counts from labels.

## 6. Verification and Evidence

Acceptance:
- aggregate exists in durable store;
- transitions are persisted;
- AgentInvocation receipts exist for Agent work;
- gates execute;
- repair is bounded;
- negative run stops safely;
- replay after restart reproduces the authoritative transition history;
- benchmark digest is derived from evidence.

## 7. Completion / Stop Condition

M71 closes when the evidence manifest shows one continuous authoritative execution chain and the benchmark survives inspection without synthetic events.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

No production deployment. Clean only temporary test fixtures.

## 9. Operator Decision

Operator decides ACCEPT / ACCEPT-WITH-LIMITATIONS / REJECT / STOP-BLOCKED.

## 10. False-Proof / Reward-Hacking Defense

A successful operator command, synthetic trace, mock model response or hard-coded phase count cannot satisfy golden-run acceptance.

## 11. Out-of-Scope but Recorded

Final deployment authorization.
