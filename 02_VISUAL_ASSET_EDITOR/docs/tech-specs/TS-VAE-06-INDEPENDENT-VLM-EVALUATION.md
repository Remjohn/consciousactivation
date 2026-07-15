# TS-VAE-06 Independent VLM Evaluation

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Feature: F14
- Owned FRs: FR-105 through FR-112
- Owned NFRs: NFR-EVAL-001 through NFR-EVAL-005
- Decisions: D004, D017
- Components: `EvaluationProfileRegistry`, `DeterministicValidator`, `IndependentEvaluator`, `CompositionSimulator`, `VerdictSynthesizer`, `EvaluatorCertificationService`

## 2. Evidence read

VAE F05/F11/F14/F15/F21 shards; quality-evaluation and repair schemas/fixtures; success metrics; Format 02 benchmark and syntax summary; workcell authority registry; Delegation authority/failure/prohibition and result contracts.

## 3. Problem, solution, and scope

Production acceptance requires evidence across technical validity, meaning, Activative function, composition, continuity, recurrence, and temporal behavior. A producing model cannot approve its own output, and average scores cannot compensate for a failed hard gate. The solution is a versioned profile system, deterministic validation first, independent VLM evaluation second, and deterministic verdict synthesis.

In scope: profile registry, technical checks, independent asset/composition/syntax/temporal evaluation, evidence localization, hard gates, arbitration, evaluator certification, and repair-contract inputs. Out of scope: candidate production, final Content Harness consumption acknowledgement, protocol lifecycle, and hidden aesthetic ranking.

## 4. Models and evaluator independence

`EvaluationProfile`: ID/version/hash, asset family/subtype, category/format, required dimensions, deterministic checks, VLM programs/templates, input render profiles, score scales, hard gates, thresholds, uncertainty/arbitration policy, repair mappings, protected benchmark refs, and certification status.

`EvaluationRequest`: exact demand/plan/candidate/geometry/render refs, producer identity, profile, context manifest, required dimensions, and idempotency key.

`QualityEvaluation`: per-check evidence, observation versus inference labels, localized regions/timestamps, dimension scores/confidence, failure codes/severity/responsible layer, hard-gate outcomes, uncertainty, evaluator identity/program/template/profile versions, verdict, repair input, and receipt hash.

Independence guard requires evaluator invocation, credentials, prompt/program, and result to be separate from generation. `evaluator_model_id` must differ from the model that produced the candidate for the evaluated claim. A deterministic transformation may be validated by deterministic checks, but visual/semantic acceptance still uses a certified independent evaluator where the profile requires it.

## 5. Evaluation pipeline and state

States: `REQUESTED`, `TECHNICAL_VALIDATING`, `TECHNICAL_FAILED`, `ASSET_EVALUATING`, `COMPOSITION_EVALUATING`, `SYNTAX_EVALUATING`, `TEMPORAL_EVALUATING`, `ARBITRATING`, `PASS`, `REPAIR_REQUIRED`, `REJECTED`, `EVALUATOR_EXCEPTION`.

Pipeline: verify refs/hashes/profile -> deterministic file/dimension/alpha/integrity/receipt/geometry checks -> prepare evidence-safe renders -> independent asset evaluation -> composition simulation/evaluation -> recurrence/continuity evaluation -> temporal evaluation where applicable -> deterministic hard-gate synthesis -> persist immutable evaluation -> notify selector or repair controller.

Technical failure stops expensive VLM work unless the profile explicitly requires diagnostic evaluation. A failed hard gate yields repair/reject regardless of aggregate score.

## 6. Interfaces, events, and integration contract

```text
validate_technical(request) -> DeterministicValidation
evaluate_asset(request) -> DimensionEvidence[]
evaluate_composition(request, render_ref) -> DimensionEvidence[]
evaluate_syntax_context(request, usage_context_refs) -> RecurrenceEvidence
evaluate_temporal(request, clip_or_frame_refs) -> TemporalEvidence
synthesize(profile, evidence_set) -> EvaluationVerdict
certify(evaluator_version, labeled_set, profile) -> CertificationReceipt
```

Events: `TechnicalValidationFailed`, `EvaluationStarted`, `DimensionFailed`, `ArbitrationRequested`, `EvaluationPassed`, `RepairRequired`, `EvaluatorException`, `EvaluatorCertified`, `EvaluatorRevoked`.

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Plan pins evaluation profile and required dimensions, not evaluator implementation strategy from demand notes. |
| APIs/queues | Evaluations are idempotent jobs with immutable requests/results; evaluator adapter is isolated from producer worker. |
| Provider/ComfyUI/Docker/model/VAE/LoRA locks | Producer locks are evidence; evaluator has separately pinned model/program/template/runtime identity and does not inherit producer model, VAE, or LoRA authority. |
| GPU/storage | Renders/evidence are content-addressed; evaluation resource class and retention are profile-defined. |
| Deterministic/VLM | Technical checks and verdict synthesis are deterministic. VLM judges visual/semantic dimensions and returns evidence/confidence, never authority changes. |
| Budgets/candidates | Required evaluations are reserved per candidate; budget cannot skip mandatory gates. |
| Candidate selection | Only `PASS` candidates are eligible for TS-VAE-05 ranking. |
| Repair | Failures map to typed responsible layers and preservation evidence for TS-VAE-07. |
| Idempotency/checkpoints | Request hash includes all refs/profile/evaluator version. Completed dimension results are immutable checkpoints. |
| Observability/cost | Record per-dimension latency, calls/tokens/compute/cost, uncertainty, arbitration, and failure recall metrics. |
| Security | Untrusted notes/text/images are data, not instructions; evaluator templates delimit content and suppress tool authority. |
| Migration/rollback | Profile/evaluator versions are independent. Active runs pin both; rollback reselects prior certified pair and protected set. |

## 7. Detailed evaluation rules

1. Mandatory dimensions for Format 02 are technical validity, semantic fidelity, Activative fidelity, wrong-reading risk, identity continuity, expression/gesture/gaze, composition effectiveness, crop resilience, editability, and recurrence/continuity.
2. Temporal evaluation is required only for temporal assets; Release 1 static character output records `not_applicable` with reason.
3. Composition evaluation uses a deterministic scene simulation with reserved text/caption regions and actual geometry, not an isolated beauty score.
4. Recurrence uses rendered syntax context, role, geometry, sequence proximity, identity value, and contradiction evidence; frequency alone is insufficient.
5. Evidence must distinguish visible observation from interpretation and localize failures where possible.
6. Wrong-reading locks are hard gates. No average score can compensate.
7. Evaluator uncertainty above profile threshold invokes a secondary certified evaluator or arbitration; it never silently passes.
8. Verdict synthesis uses profile-defined precedence: integrity/constitutional gates -> mandatory dimensions -> uncertainty -> ranking scores.
9. Repair requires a causal failure/responsible layer and explicit properties to preserve.
10. Evaluator versions earn `production_certified` only through protected labeled cases, mutation tests, repair precision, and monitored shadow performance.

## 8. Certification and targets

The initial Format 02 calibration set contains at least 30 labeled evaluator cases plus representative, golden, known-failure, adversarial, mutation, repair, recurrence, and borderline cases from the benchmark manifest. Split development/calibration from a protected release set. Labels require adjudicated semantic, Activative, composition, identity, wrong-reading, and responsible-layer evidence.

Release targets include at least 98% expert agreement for accepted semantic/Activative requirements with zero known constitutional acceptance, profile-specific hard-failure recall/false-rejection thresholds, at least 90% repair precision, and monitored drift. Exact evaluator/model choice remains empirical; registry control IDs are experimental until the certification receipt passes.

## 9. Failure, recovery, performance, and security

Evaluator timeout/unavailability is an infrastructure exception and may retry/fail over without a quality round. Invalid output/schema, context overflow, contradictory evaluators, or calibration drift yields `EVALUATOR_EXCEPTION`/human exception. A missing required evaluator blocks acceptance. Corrupt candidate/render is a technical failure.

Evaluation runs only after cheap deterministic checks and may batch compatible requests without mixing authority/context. Cache is valid only for identical candidate/render/demand/profile/evaluator hashes. Prompts, images, and labels follow tenant and retention policy; external evaluators receive minimum context and no secrets/private unrelated assets.

## 10. Implementation plan

1. Close schemas for profile, request, dimension evidence, evaluation, arbitration, and certification.
2. Implement deterministic file/geometry/receipt validators and verdict synthesizer.
3. Implement isolated evaluator adapter interface and mock fixture adapter with exact production contract.
4. Build deterministic Format 02 composition simulation renders.
5. Curate/adjudicate initial labeled and protected sets; implement benchmark runner.
6. Benchmark candidate VLM controls and calibrate profiles/uncertainty/arbitration.
7. Integrate selector/repair/runtime, telemetry, shadow monitoring, revocation, migration, and rollback.

## 11. Given/When/Then acceptance criteria

1. Given a corrupt image or missing receipt, when deterministic validation runs, then the candidate cannot reach VLM acceptance or ranking.
2. Given the same model identity produced and evaluates a candidate, when independence validates, then evaluation is rejected.
3. Given a high average score with a triggered wrong-reading lock, when verdict synthesizes, then the candidate fails.
4. Given a composition-ready isolated asset that collides with the text field in simulation, when evaluated, then composition effectiveness fails with localized evidence.
5. Given repeated character identity in a different productive pose/role, when recurrence evaluates, then frequency alone cannot label fatigue.
6. Given evaluator uncertainty above threshold, when policy executes, then arbitration/secondary evaluation occurs or acceptance blocks.
7. Given evaluator timeout, when retry succeeds, then no quality round is consumed and one evaluation result is committed.
8. Given rollback to the prior certified evaluator/profile, when protected cases run, then historical verdict behavior is reproducible.

## 12. Testing strategy

Unit-test deterministic checks, precedence, thresholds, idempotency, and profile resolution. Contract-test adapter requests/responses and malformed outputs. Behavioral-test all benchmark families, false positive/negative traps, prompt injection, model self-approval, recurrence contexts, and temporal applicability. Fault-inject timeouts/provider failures. Monitor performance/cost and run compatibility/migration/rollback plus full Format 02 candidate-set evaluation.

## 13. Constitutional alignment V1.1 addendum

### Versioned Visual Evaluation Profile

Every certified profile declares an applicability decision, evidence program, scale, authority-approved threshold, hard-gate status, failure code, and responsible-layer mapping for:

- zero-second hook;
- pattern-match strength;
- pattern-interrupt strength;
- viewer-role clarity;
- activation-direction fidelity;
- prediction gap;
- payoff;
- affinity;
- anticipation residue;
- anti-cliche strength;
- wrong-reading risk;
- Feature Contract compliance;
- delete-caption/no-text survival when applicable.

The profile also pins the Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contract, T/V, Composition Intent, and wrong-reading evidence inputs that each program may inspect. Missing applicability or threshold policy prevents profile certification; the evaluator may not invent thresholds.

No-text applicability is explicit. When applicable, the evaluator renders or receives a caption-free view, runs the delete-caption program, records whether intended meaning and viewer role survive, and hard-fails if either collapses. When not applicable, the receipt records the authoritative applicability reason rather than an empty object.

### Responsible-layer evidence

Every failure identifies one primary responsible layer and any contributing layers from: activative_lineage, activation_contract, visual_semantics, visual_narrative, feature_contract, somatic_route, composition_intent, materialization, technical, identity_continuity, temporal, or evaluation_infrastructure. Evidence distinguishes visible observation, constitutional comparison, and inference. A responsible-layer assignment cannot authorize a change to an upstream-owned contract.

Verdict synthesis uses strict precedence: integrity and constitutional enforceability; mandatory activation, narrative, feature, wrong-reading, and no-text gates; composition and continuity gates; uncertainty/arbitration; then ranking-only scores. Semantic clarity, technical validity, or aesthetic quality cannot compensate for a failed higher-precedence gate.

### Additional acceptance criteria

1. A technically valid asset that misses its activation direction, viewer role, or pattern interrupt is rejected or repaired.
2. A candidate that violates one meaning-bearing Feature Contract fails even when its overall composition score is high.
3. A no-text candidate whose intended meaning collapses after caption removal fails the delete-caption gate.
4. A wrong-reading interpretation that dominates any required lock fails regardless of average score.
5. A failure without responsible-layer evidence cannot produce an executable repair contract.
6. The same candidate, profile, context, and evaluator versions reproduce the same applicability and verdict synthesis.

## 14. Non-goals

- Delegation Protocol visual evaluation or creative ranking.
- Producer self-evaluation, one aesthetic score, or averages overriding hard gates.
- Certifying a model from a few anecdotal examples.
- Human review as a routine substitute for evaluator readiness.
