# TS-VAE-11 LoRA and Capability Development

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Feature: F13
- Owned FRs: FR-097 through FR-104
- Owned NFR: NFR-GOV-003
- Decision: D016
- Components: `CapabilityGapAnalyzer`, `CapabilityDevelopmentPlanner`, `DatasetSnapshotService`, `ExperimentRunner`, `CapabilityBenchmark`, `CapabilityPromotionService`

## 2. Evidence read

VAE F08/F13/F17/F21, model/LoRA/control/runtime requirements, Steering Recipe schema, Budget Programs, benchmark/success/readiness artifacts, Format 02 target, source/provenance rules, and Delegation capability-gap/budget/compatibility contracts.

## 3. Problem, solution, and scope

Recurring production gaps may justify a new workflow, control, adapter, evaluator, Steering Recipe, or LoRA, but one failed demand never justifies training. The solution is an isolated evidence-driven lifecycle with immutable datasets, declared controls, reproducible experiments, contamination/compatibility tests, staged registry promotion, and rollback.

In scope: gap aggregation, evidence sufficiency, typed development plan, datasets, experiments, LoRA/workflow/control development, control comparisons, contamination/security/license checks, promotion/deprecation/rollback, and one Format 02 proof cycle. Out of scope: automatic training from ordinary production, general LoRA factory, unreviewed external datasets, or experimental capability in certified production.

## 4. Canonical models and states

`CapabilityGapCohort`: stable gap code/layer, affected demand/profile/route refs, frequency, severity, failed controls, repair outcomes, business/quality impact, confounders, and evidence sufficiency.

`CapabilityDevelopmentPlan`: capability type/objective, target profile, hypothesis, baseline/control, dataset specification, train/validation/protected test split, provenance/license/privacy, method/hyperparameter search bounds, runtime/budget, success/failure thresholds, compatibility/security tests, promotion target, rollback/deprecation, and owner approvals.

`DatasetSnapshot`: immutable manifest of item refs/hashes, labels, provenance/license/consent, split assignment, dedup/contamination results, transformations, preparation code/runtime hash, exclusions, and retention.

`ExperimentRun`: exact plan/dataset/base model/VAE/LoRA/control/workflow/runtime/compiler/seeds/config, outputs, metrics, costs, logs, failure and receipt.

`CapabilityCandidate`: resulting registry record, digest, compatibility edges, benchmark comparison, limitations, maturity, and rollback artifact.

Lifecycle: `GAP_OBSERVED`, `EVIDENCE_ACCUMULATING`, `PLAN_PROPOSED`, `AUTHORIZED`, `DATASET_FROZEN`, `EXPERIMENTING`, `BENCHMARKED`, `REJECTED`, `SHADOW`, `LIMITED_PRODUCTION`, `PRODUCTION_CERTIFIED`, `DEPRECATED`, `REVOKED`, `ROLLED_BACK`.

## 5. Release 1 proof target

Use a recurring `CHAR-GUIDE-001` identity/Minimal Coach Theatre visual-language gap only after the benchmark cohort demonstrates that certified reuse/generation/control/repair routes fail the same responsible layer across sufficient independent cases. The development plan may choose LoRA, workflow/control improvement, or Steering Recipe based on comparative evidence; it must not preselect LoRA as the answer.

One governed cycle must produce either a promoted limited capability or a well-evidenced rejection. A rejected experiment still satisfies process proof when receipts, controls, and learning are complete; it does not satisfy capability readiness.

## 6. Interfaces, events, and integration contract

```text
analyze_gaps(evidence_query, target_profile) -> CapabilityGapCohortRef
propose_plan(cohort_ref, candidate_methods) -> CapabilityDevelopmentPlanRef
freeze_dataset(plan_ref, source_refs) -> DatasetSnapshotRef
run_experiment(plan_ref, dataset_ref, variant) -> ExperimentRunRef
benchmark(candidate_ref, controls, protected_set) -> CapabilityBenchmarkRef
promote(candidate_ref, evidence_bundle, target_maturity) -> PromotionReceipt
deprecate_or_rollback(capability_ref, reason, replacement_ref) -> GovernanceReceipt
```

Events: `CapabilityGapAccumulated`, `DevelopmentPlanAuthorized`, `DatasetFrozen`, `ExperimentCompleted`, `ContaminationDetected`, `CapabilityBenchmarked`, `CapabilityPromoted`, `CapabilityRejected`, `CapabilityRevoked`, `CapabilityRolledBack`.

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Experiments consume explicit plans but never modify production plans/demands; promoted capability becomes eligible only via registry versions. |
| APIs/queues | Capability Lab is isolated from production queues/credentials/storage namespaces; all work is asynchronous and receipted. |
| Provider adapters/ComfyUI/Docker locks | Training/inference workflows, provider adapters, OCI images, nodes, base model, VAE, LoRA, controls, and compiler are digest-pinned. |
| Model/VAE/LoRA registries | Candidate cannot be used until compatibility edges, evidence, maturity, weight domain, limitations, and rollback exist. |
| GPU/storage | Uses sandboxed runtime profiles, separate learning budget, immutable datasets/checkpoints, and controlled egress. |
| Deterministic/VLM | Data integrity/splits/contamination/metrics/promotion gates are deterministic. VLM may label/adjudicate only with independent review/calibration. |
| Budget/candidates | Capability Learning/authorized Exploration program; production budget cannot fund hidden training. |
| Evaluation | Compare relevant certified controls on held-out/protected sets using independent evaluator and expert labels. |
| Repair | Gap evidence includes failed targeted repairs; one failure/repair cannot trigger development. |
| Idempotency/checkpoints | Dataset and experiment identities are complete hashes; retries resume exact runs and cannot overwrite results. |
| Observability/cost | Track dataset lineage, experiments, metrics, cost/GPU, contamination, compatibility, promotion, shadow drift, incidents. |
| Security | Untrusted data scanning, provenance/license/consent, secret isolation, no production data leakage, model artifact signing. |
| Migration/rollback | Promotion creates a new registry version; active runs remain pinned. Deprecation/revocation impact analysis and prior certified fallback are mandatory. |

## 7. Evidence and promotion rules

1. A reusable gap requires repeated comparable failures with stable responsible layer after valid routes/repairs, not one normal demand failure.
2. Evidence sufficiency considers case diversity, severity, frequency, confounders, controls, expected transfer, cost, and available non-training alternatives.
3. Dataset items require source, rights/provenance policy, hashes, labels, split, privacy, and permitted use.
4. Identity or near-duplicate contamination across train/validation/protected sets blocks the benchmark.
5. Compare against reuse, prompt/control/workflow/repair and existing capability controls where relevant.
6. Success must improve target quality without semantic, composition, identity, diversity, security, cost, or compatibility regression beyond thresholds.
7. Promotion stages require increasing evidence: sandbox -> benchmark -> shadow -> limited production -> production certified.
8. Shadow outputs cannot be returned as accepted assets.
9. Registry promotion is a governed deterministic decision over signed evidence; the training model cannot promote itself.
10. Drift, incident, license issue, or compatibility regression can deprecate/revoke; rollback is rehearsed before limited production.

## 8. Failure, recovery, performance, and security

Insufficient evidence returns `DEVELOPMENT_NOT_JUSTIFIED`; data/provenance/license failure blocks dataset; contamination invalidates affected split/run; infrastructure failures resume exact checkpoints without changing experiment identity; metric/regression failure rejects candidate; security/integrity issue quarantines artifacts and may revoke descendants.

Learning runs have hard GPU/cost/time/storage ceilings and early-stop criteria. Cost is separated from production and reported per experiment/candidate. Dataset/model access is role-scoped, encrypted, audited, and isolated. External code/nodes/data are scanned and pinned; no dynamic install or arbitrary egress.

## 9. Implementation plan

1. Close schemas for gap cohort, development plan, dataset, experiment, benchmark, candidate, promotion, and rollback.
2. Implement evidence aggregation and sufficiency policy over immutable production outcomes.
3. Implement isolated dataset preparation, dedup/contamination, provenance, and split pipeline.
4. Implement experiment orchestration through TS-VAE-03/04 with exact locks and Capability Learning budgets.
5. Implement independent benchmark/control comparison and compatibility/security regression suite.
6. Integrate registry promotion, shadow/limited-production policy, impact, deprecation, revocation, and rollback.
7. Execute one Format 02 identity/visual-language capability cycle and publish complete receipts.

## 10. Given/When/Then acceptance criteria

1. Given one ordinary failed demand, when development is proposed, then it is rejected for insufficient recurring evidence.
2. Given a recurring identity gap with successful cheaper workflow/control alternative, when methods compare, then LoRA is not selected without superior evidence.
3. Given duplicate identities across train/protected sets, when contamination runs, then benchmarking/promotion blocks.
4. Given an experiment retry after worker failure, when resumed, then dataset/config/run identity remains exact and prior results are not overwritten.
5. Given a candidate improving identity but harming composition/wrong-reading gates, when benchmarked, then promotion fails.
6. Given a passing candidate, when promoted to shadow, then production routes cannot return its outputs as accepted assets.
7. Given limited-production regression, when revocation triggers, then new use blocks, active/historical runs remain traceable, and prior certified capability is restored.
8. Given one complete rejected capability cycle, when process evidence is audited, then it proves governance execution but does not claim production capability.

## 11. Testing strategy

Unit-test sufficiency, dedup, split, contamination, promotion, and rollback guards. Integration-test dataset/object store, experiment runtime, budgets, registries, evaluator, shadow routing, and revocation. Behavioral-test control comparisons and transfer. Adversarially test poisoned data, prompt injection in labels, license/provenance gaps, metric gaming, production-data leakage, dynamic code, and self-promotion. Run performance/cost, compatibility, migration, rollback, and Format 02 capability-cycle tests.

## 12. Constitutional alignment V1.1 addendum

Capability development evaluates the same constitutional profile as production plus declared capability-specific controls. Promotion fails on any regression in activation direction, pattern match or interrupt, viewer-role clarity, prediction/payoff/affinity/anticipation, anti-cliche strength, wrong-reading risk, Feature Contract compliance, or applicable delete-caption survival.

Datasets and benchmark cases preserve Activative lineage and applicable Reaction Receipt/Expression Moment provenance. Training labels, generated captions, or evaluator explanations cannot replace authoritative Activation Contracts, selected recognition carriers, Visual Narrative Programs, Feature Contracts, T/V requests, Composition Intent, or locks.

Gap cohorts aggregate responsible-layer evidence. A recurring visual symptom assigned to an upstream-owned layer is not a VAE training mandate; it routes to owner review. A model or workflow improvement may be promoted only when held-out and protected cases show no constitutional regression and the prior certified capability remains rollback-ready.

## 13. Non-goals

- Training because one demand or repair failed.
- A universal or automatic LoRA factory.
- Production use of experimental/shadow capabilities.
- Treating registry size, training loss, or one attractive output as production evidence.
