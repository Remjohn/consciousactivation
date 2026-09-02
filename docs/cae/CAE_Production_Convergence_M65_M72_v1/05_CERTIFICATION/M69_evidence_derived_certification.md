# M69 — Evidence-Derived Certification

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Repair the M64 certification implementation so PASS/FAIL/BLOCKED results are calculated from actual evidence, with no unconditional PASS construction.

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
`factory_certification.py` around `run_full_certification`, `BenchmarkTraceSummary`, `AdversarialAttackVector`, and `CriterionEvaluation`.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Certification evaluator, criterion evidence contracts, report generation and countertests.

## 5. Required Implementation Behavior

Define for each certification criterion:
- required evidence;
- observed evidence refs;
- status;
- reason;
- execution count;
- trace/report digest.

Run evidence collection first. Evaluate second. Report third.

A criterion with missing mandatory reality-contact evidence is BLOCKED, not PASSED. READY requires all required criteria PASSED plus explicit production authorization and valid real benchmark evidence.

## 6. Verification and Evidence

Prove PASS, FAIL and BLOCKED outcomes using controlled fixtures. Prove no unconditional `CriterionEvaluation(status=PASSED...)` remains in the evaluator. Prove synthetic command success cannot satisfy the domain benchmark criterion.

## 7. Completion / Stop Condition

M69 closes when certification is evidence-derived and the old auto-pass false proof is impossible.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

Revert evaluator changes only.

## 9. Operator Decision

Operator accepts the evidence model. M71 supplies the first real evidence set.

## 10. False-Proof / Reward-Hacking Defense

`total_runs=3` is meaningless without authoritative run/receipt evidence. A generated report is not its own evidence.

## 11. Out-of-Scope but Recorded

Production deployment and golden run execution.
