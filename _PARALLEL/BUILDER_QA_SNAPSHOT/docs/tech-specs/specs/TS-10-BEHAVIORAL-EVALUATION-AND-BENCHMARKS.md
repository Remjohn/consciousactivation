# TS-10: Behavioral Evaluation And Benchmark Maturity

Status: `EMPIRICAL_SPEC_COMPLETE_PENDING_BD-004_BD-008`

## Traceability

- Owned: FR-103 through FR-116; NFR-TRACE-003, NFR-EVAL-001, NFR-EVAL-002, NFR-EVAL-003, NFR-EVAL-004.
- Supports deferred FR-169 general Builder certification.
- Decisions: D003, D021, D022, D023, D024, D026, D027, D028, D032, D033.

## Responsibility And Authority

Own evaluation plans for skills/adaptations/recipes/capsules/phases/workflows, no-guidance controls, repeated trials, case generation, maturity receipts, exact artifact identity, benchmark portfolio/corpus, controlled mutations, protected cases, multidimensional scorecards, hard gates, stability, and downstream result ingestion.

Deterministic code owns case assignment, identity, split protection, aggregation, thresholds, and receipts. Generators and evaluators are isolated. Human evaluation governance owns protected labels, rubric changes, threshold ratification, and exceptional release decisions.

## Modules And Components

`evaluation/{corpus,cases,runner,evaluators,scorecard,maturity,hard_gates,downstream}.py`, `application/evaluation_commands.py`, and `adapters/evaluator_provider.py`.

## Canonical Data Structures

- `BenchmarkCase { case_id, version, target_scope, category, input_refs, hidden_labels_ref?, expected_invariants, mutation_parent?, access_class }`
- `CorpusManifest { corpus_id, version, public_cases, development_cases, protected_cases, authority, hash }`
- `EvaluationPlan { subject_ref/hash, control_ref?, cases, repetitions, generator_policy, evaluator_policy, metrics, gates }`
- `TrialReceipt { case_ref, repetition, fresh_context_id, subject_hash, output_hash, evaluator_hashes, scores, failures, cost, latency }`
- `Scorecard { dimensions, distributions, confidence_intervals, stability, hard_gates, comparison_to_control, decision }`
- `MaturityReceipt { subject_hash, level, corpus_hash, plan_hash, scorecard_hash, approved_by, expires_or_revalidate_on }`

## APIs, Commands, Events, Persistence

- Commands: `RegisterCorpus`, `CreateEvaluationPlan`, `RunEvaluation`, `ScoreTrials`, `PromoteMaturity`, `RevokeMaturity`, `IngestDownstreamResult`.
- Events: `CorpusRegistered`, `EvaluationStarted`, `TrialCompleted`, `EvaluationScored`, `HardGateFailed`, `MaturityPromoted`, `MaturityRevoked`, `DownstreamResultIngested`.
- Persistence: labels encrypted and access-controlled separately; case inputs/outputs/receipts in CAS; plans and scorecards in relational projections; ledger events authoritative.
- Idempotency: trial key includes plan, case, repetition, subject, provider policy, and seed where applicable. Fresh context prevents state reuse while preserving identity.

## Dependency, Invalidation, Checkpoints, Resume

Any subject, corpus, rubric, evaluator, or threshold change invalidates the relevant maturity receipt. Runs checkpoint per trial and resume missing trials only. Protected cases are assigned by a service that does not reveal labels to generator nodes. General certification is deferred until the portfolio spans ratified transfer targets.

## Security And Isolation

Protected labels use separate credentials, store, and audit stream. Generator nodes cannot query case membership or labels. Evaluators receive output plus rubric-required context, not generator chain-of-thought or recommendation history. Export redacts labels and secrets.

## Observability, Cost, And Performance

Report pass distribution, confidence intervals, first-pass rate, repeated-run variance, control lift, quality dimensions, hard-gate outcomes, cost/latency, provider failures, and human disagreement. Thresholds are not invented; BD-008 requires calibration and human ratification.

## Failures And Recovery

Leakage invalidates the corpus version and every dependent receipt. Evaluator disagreement records dimension-level uncertainty and routes to adjudication. Partial provider outage resumes missing trials. A scorecard cannot average away a hard-gate failure.

## Acceptance Tests

1. Every evaluated subject hash matches the artifact used by production.
2. No-guidance control and repeated fresh-context trials are enforced.
3. Protected labels are inaccessible to generators and ordinary operators.
4. Leakage revokes dependent maturity receipts.
5. Hard-gate failure blocks promotion regardless of aggregate score.
6. Resume never duplicates completed trial identity.
7. Format 02 metrics include category-native visual and sequence fidelity.
8. Downstream results trace to exact Development Capsule and harness version.

## Implementation Tasks

1. Ratify corpus governance, access model, rubrics, and threshold process.
2. Define case, corpus, plan, trial, scorecard, and maturity schemas.
3. Implement assignment, runner, evaluator isolation, aggregation, and receipts.
4. Implement protected-store and leakage audit controls.
5. Build Format 02 positive, adversarial, incomplete, mutation, and protected cases.
6. Add statistical, identity, isolation, resume, and hard-gate tests.

## V1.2 Constitutional Alignment Patch

| Requirement | Implementation owner | Component boundary | Data or contract | Failure behavior | Test seam | Acceptance criteria | Migration / compatibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Evaluate constitutional conversational and visual dimensions | evaluation_orchestrator_owner | Builder runs isolated evaluation; human governance owns labels, rubrics, and thresholds | `ConstitutionalEvaluationReceipt` dimensions for activation, role, reaction, expression, visual recognition, narrative, wrong-reading, lineage, syntax, and boundary | Any non-compensable failure or missing protected policy blocks promotion | protected conversational cases, fresh-context repetitions, leakage, and hard-gate tests | Scorecard exposes every dimension and cannot average away a failed gate | Extends BD-008 and keeps HD-007 open; existing Format 02 evaluation remains valid and non-regressed |

## Non-Goals And Migration

No claim of universal quality, no single scalar score, no V2.1 benchmark compatibility, and no production label access by generator agents.
