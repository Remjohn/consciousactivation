# TS-VAE-07 Repair, Invalidation, and Bounded Reruns

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Feature: F15
- Owned FRs: FR-113 through FR-120
- Owned NFRs: NFR-REL-001 through NFR-REL-005
- Decision: D018
- Components: `RepairController`, `CausalBindingResolver`, `InvalidationPlanner`, `RepairPlanCompiler`, `RepairEffectivenessRecorder`

## 2. Evidence read

VAE F04/F05/F09/F10/F14/F15/F20/F21; repair/evaluation/plan schemas and fixtures; three-round Budget limit; preservation contract; Format 02 repair benchmarks; Delegation failure, supersession, selective invalidation, amendment, cancellation, and resilience contracts.

## 3. Problem, solution, and scope

Quality failures must be corrected without destroying valid work, mutating demand authority, or launching blind retries. The solution converts certified evaluation failures into immutable repair contracts, validates a causal binding delta, computes the smallest invalidation set, creates a new plan version, and enforces at most three autonomous quality rounds.

In scope: repair contracts, preservation/mutable bindings, hierarchy, causal validation, invalidation graph, checkpoint reuse, rerun limits, escalation, and effectiveness evidence. Out of scope: infrastructure retry, demand amendment approval, evaluator certification, or arbitrary prompt tweaking.

## 4. Canonical models

`RepairContract`: repair ID/version/hash, candidate/evaluation/plan/demand refs, quality round, failure code/severity/responsible layer/evidence, preserved properties with verification method, permitted/prohibited changes, proposed binding deltas, invalidated nodes, reusable outputs, success criteria, budget reservation, evaluator/profile refs, and expiry.

`InvalidationPlan`: prior/new plan refs, changed bindings, causal dependency edges, invalidated nodes/artifacts/evaluations/geometry, reusable checkpoints with hash/compatibility proof, rerun topological order, cost estimate, and receipt.

`RepairOutcome`: resulting candidates/evaluations, property-preservation checks, success/failure, changed layer, collateral changes, cost/time, round, effectiveness label, and steering evidence ref.

## 5. State machine and flow

States: `FAILURE_RECEIVED`, `CAUSE_RESOLVED`, `CONTRACT_COMPILED`, `INVALIDATION_PLANNED`, `AUTHORIZED`, `RERUNNING`, `REEVALUATING`, `SUCCEEDED`, `FAILED_ROUND`, `MAX_ROUNDS_REACHED`, `AMENDMENT_REQUIRED`, `CANCELLED`.

Flow: receive immutable evaluation -> validate hard failure/responsible layer -> choose least-disruptive repair level -> compile repair contract -> verify binding ownership/domain -> calculate invalidation -> reserve budget -> create new plan version -> rerun invalidated nodes only -> reevaluate all affected gates plus preserved properties -> record outcome -> stop/pass/next round/escalate.

Repair hierarchy: deterministic local correction -> parameter/control binding -> regional inpaint/composite -> workflow fallback -> route replan -> demand-level amendment proposal. Each step requires evidence that lower levels are insufficient or failed.

## 6. Interfaces, events, and integration contract

```text
compile_repair(evaluation_ref, plan_ref, round) -> RepairContractRef
plan_invalidation(repair_ref, event_graph, checkpoint_manifest) -> InvalidationPlanRef
apply_binding_delta(plan_ref, repair_ref) -> NewProductionPlanRef
execute_repair(invalidation_ref, budget_reservation) -> RepairExecutionRef
record_outcome(repair_ref, evaluations) -> RepairOutcomeRef
```

Events: `RepairContractCreated`, `RepairRejected`, `NodesInvalidated`, `RepairStarted`, `RepairSucceeded`, `RepairRoundFailed`, `RepairLimitReached`, `DemandAmendmentRequired`.

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Every repair creates a new plan version with explicit binding delta; demand snapshot is unchanged. |
| APIs/queues | Only invalidated node commands are enqueued; reused checkpoints are exact refs/hashes. |
| Provider adapters/ComfyUI/Docker/model/VAE/LoRA locks | TS-VAE-03 recompiles affected stages only; provider, OCI image, model, VAE, LoRA, or bundle changes require compatible fallback and new locks. |
| GPU/storage | TS-VAE-04 executes reruns; successful immutable artifacts remain frozen. |
| Deterministic/VLM | Causality/ownership/invalidation/round guards are deterministic. VLM evaluation identifies visual failure evidence but cannot authorize changes. |
| Budget/candidates | Repair reserves a bounded portfolio/round budget; denial pauses or escalates without degradation. |
| Evaluation | TS-VAE-06 independently reevaluates failure, preserved properties, and applicable regressions. |
| Idempotency/checkpoints | Repair key is evaluation + plan + round + delta hash; duplicate delivery returns the existing contract/outcome. |
| Observability/cost | Trace changed bindings/nodes, reuse, preservation, quality delta, collateral damage, time, and cost. |
| Security | Binding deltas are allowlisted and schema/range checked; model-authored free text cannot become an executable mutation. |
| Migration/rollback | Repair contracts/plans are immutable. Rollback restores prior plan/bundle/checkpoints but never erases failed evidence. |

## 7. Detailed behavioral rules

1. Every quality rerun requires one typed repair contract linked to an independent evaluation.
2. `preserve` properties are executable assertions, not prose only.
3. Changes outside `permitted_changes`, within `prohibited_changes`, or outside VAE authority fail before execution.
4. The causal layer must match failure evidence and dependency graph; random seed/prompt changes without a hypothesis are invalid.
5. Invalidate the changed node and all dependent outputs/evaluations; do not invalidate independent valid work.
6. Reuse requires exact input/binding/compatibility hashes and no invalidated dependency.
7. Quality rounds are numbered 1..3 across the demand execution; workflow fallback does not reset the count.
8. Infrastructure retries are tracked separately and cannot alter bindings.
9. A demand-level conflict creates a Delegation amendment proposal; the VAE cannot apply it.
10. Repair success requires the failed gate to pass and all preserved/hard-gate regressions to pass.
11. After round three, unresolved quality enters typed human/capability/amendment exception; no fourth autonomous round.
12. Repair outcomes may inform Steering Recipes only after controlled aggregation/promotion, never from one success.

## 8. Failure, cancellation, recovery, and performance

Invalid repair contract, causal mismatch, unauthorized binding, stale plan, or incompatible checkpoint is terminal for that repair proposal. Worker/provider failure retries through TS-VAE-04 and resumes the same round. Cancellation freezes committed evidence and blocks late output promotion. Supersession stops old-plan repair and invokes demand impact analysis.

The invalidation plan should minimize expected rerun cost while preserving correctness. Metrics include repair rounds, nodes reused/rerun, quality delta, preservation pass, collateral regressions, success by failure/layer, cost/time, and max-round exceptions. Median repair rounds target at or below one for mature routes; repair precision target is at least 90%.

## 9. Implementation plan

1. Close repair, invalidation, outcome, assertion, and binding-delta schemas.
2. Build causal dependency and invalidation traversal over plan/event/artifact lineage.
3. Implement deterministic ownership/domain/round/idempotency guards.
4. Implement plan version delta and affected-stage recompilation.
5. Integrate budget, runtime, evaluation, cancellation, supersession, and Delegation amendment ports.
6. Implement preservation/regression assertions and effectiveness evidence.
7. Add repair benchmark runner, fault injection, migration, and rollback tests.

## 10. Given/When/Then acceptance criteria

1. Given `WEAK_VISIBLE_ACTION` localized to pose conditioning, when repair compiles, then identity, expression, gaze, geometry, palette, and alpha are preserved while only allowed pose bindings change.
2. Given a proposed semantic-intent change, when repair validates, then it is rejected and a demand amendment path is offered.
3. Given reusable identity reference and scene template, when invalidation runs, then they remain checkpoints while dependent pose/generation/evaluation nodes rerun.
4. Given a worker crash during round one, when resumed, then it remains round one and uses the same repair contract.
5. Given an unchanged random retry request, when validated, then it is rejected for missing causal delta.
6. Given a successful local correction, when reevaluated, then the original failure and all preservation assertions pass before selection.
7. Given three failed quality rounds, when another autonomous repair is requested, then it is blocked and a typed exception is emitted.
8. Given rollback, when the prior plan is restored, then failed repair evidence remains historically queryable.

## 11. Testing strategy

Unit-test ownership, ranges, causal matching, graph invalidation, checkpoint eligibility, round counting, and idempotency. Integration-test plan/compiler/runtime/evaluator/budget flow, restart, cancellation, supersession, and late outputs. Behavioral-test all repair benchmark families, preservation and collateral mutation. Fault-inject infrastructure failure. Run performance/cost and compatibility/migration/rollback tests plus the Format 02 targeted gesture repair.

## 12. Constitutional alignment V1.1 addendum

Repair begins only from an independent evaluation with responsible-layer evidence. The repair controller maps the primary layer to the smallest VAE-owned mutable binding; it cannot use a downstream visual symptom to rewrite Activative lineage, the Activation Contract, Visual Semantic Pack, Semiotic MCDA decision, Visual Narrative Program, Feature Contracts, T/V request, Composition Intent, or wrong-reading locks.

All constitutional demand layers are explicit preserved properties. A repair may adjust VAE-owned materialization or exact geometry only within the authoritative Feature Contracts and Composition Intent. If the failure is caused by an upstream contract contradiction or missing meaning, repair stops and emits the governed amendment/conflict path.

The invalidation graph includes activation, narrative, feature, wrong-reading, and no-text evaluation nodes. Repair success requires the original failed gate, all affected constitutional gates, and every preserved-property assertion to pass. A caption or explanatory text cannot be added to repair a no-text failure.

Additional tests cover incorrect responsible-layer assignment, attempted recognition-carrier substitution, attempted viewer-role change, Feature Contract regression, T/V overreach, wrong-reading-lock weakening, and delete-caption failure after an otherwise successful visual repair.

## 13. Non-goals

- Blind retries, whole-pipeline reruns by default, or resetting quality rounds after fallback.
- Demand mutation, evaluator self-approval, or human approval of routine repairs.
- Turning one successful repair into a production Steering Recipe.
