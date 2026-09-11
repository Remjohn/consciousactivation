# M72 — Final Production Gate + CURRENT Synchronization

**Status:** EXECUTABLE — OPERATOR REVIEW REQUIRED
**Execution model:** Gemini, one mandate at a time

## 1. Decision / Objective

Reconcile implementation truth, certification evidence and deployment reality into one final production decision. Update `docs/PRD/CURRENT.md` in the same session. Do not manufacture READY.

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
Deployment/infra runbooks and current production configuration.
M65–M71 evidence manifests, receipts and reports.

Gemini must record the exact paths and symbols read.

## 4. Exact Scope

Final readiness gate only. No new architecture.

## 5. Required Implementation Behavior

Verify:
- M69 evidence-derived certification;
- M71 golden run;
- persistent state in deployed composition;
- operator access and tenant isolation;
- provider/secret configuration;
- backup/restore;
- restart/replay;
- health checks;
- observability;
- rollback;
- exact deployment commit;
- `production_authorized` and `certified` status are consistent across runtime and documentation.

Update CURRENT.md with implementation truth, target truth, limitations, and exact commit SHA.

## 6. Verification and Evidence

Required final evidence package:
- certification report;
- golden-run manifest;
- deployment smoke test;
- persistence/restart proof;
- backup/restore proof;
- operator gate receipt;
- unresolved blocker list.

Final status must be exactly one of READY / READY-WITH-EXPLICIT-LIMITATIONS / NOT-READY.

## 7. Completion / Stop Condition

M72 closes only after explicit Operator decision and synchronized current-state records.

STOP if the required authority is ambiguous, the current implementation differs materially from the mandate assumptions, a new canonical object appears necessary, or required reality-contact evidence cannot be obtained.

## 8. Rollback / Recovery

Rollback only deployment/config changes introduced in this mandate. Preserve evidence.

## 9. Operator Decision

Operator must explicitly choose the final production status. No automatic promotion.

## 10. False-Proof / Reward-Hacking Defense

Documentation saying READY, a green local suite, or a certificate object is never sufficient.

## 11. Out-of-Scope but Recorded

Any new architecture work, VAE Stage 5 activation, Format 02 activation without separate authorization.
