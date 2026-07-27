# TS-VAE-10 Format 02 Release 1 Vertical Slice

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Features: F01, F21, F22
- Owned FRs: FR-001 through FR-008; FR-161 through FR-176
- Owned NFRs: NFR-TRACE-001 through NFR-TRACE-005; NFR-GOV-001, NFR-GOV-002, NFR-GOV-004, NFR-GOV-005
- Decisions: D001, D025, D026, D028
- Reference target: Format 02 Minimal Coach Theatre, category `2d_character_animation`, AF-02 character/scene path

## 2. Evidence read

Complete VAE PRD/governance/handoff package; all Stage 2 specs; Format 02 syntax summary, six seed registries, six VAE contract fixtures, benchmark manifest; Delegation 25-schema package, negotiated profile, product manifests, 10 scenarios, 56 conformance cases, lifecycle/authority/compatibility/readiness artifacts.

## 3. Release promise, scope, and non-goals

Release 1 proves one complete autonomous character-and-scene production spine from an immutable Format 02 demand through production-accepted asset, composition geometry, and downstream acknowledgement, with one targeted repair and exact provenance.

Canonical first slice is `VAD-F02-0001`: `CHAR-GUIDE-001` skeptical-listener reaction, restrained skepticism rather than contempt, leftward gaze/gesture, foreground-right geometry, protected face/hands, reserved text/caption regions, transparent character output, Standard budget, independent evaluation, and at most three repairs.

In scope: AF-02 identity, pose, expression, gesture, gaze, simple prop/environment dependency, transparent cutout, image-conditioned geometry, continuity/recurrence, local/cloud runtime proof, async Delegation, candidate portfolio, evaluation, one repair, immutable result, and Remotion consumption receipt.

Out of certification scope: broad documentary sourcing, long-form video, full UI reproduction, advanced diagrams, complex multi-character temporal continuity, lip sync, general LoRA factory, all providers, all families, and universal editing. Represented scope must be labeled uncertified.

## 4. End-to-end architecture

The slice composes the components owned by TS-VAE-01 through TS-VAE-11 through their production APIs and queues; it does not bypass those interfaces with fixture-only shortcuts.

```text
Delegation demand/submission/profile
-> VAE admission fact and immutable DemandSnapshot
-> Composition feasibility and ProductionPlan v1
-> Workcell + route + capability bundle
-> Compiled ComfyUI artifact
-> Standard portfolio (4 initial, max 10)
-> local or cloud compute worker
-> deterministic validation
-> independent asset + composition + recurrence evaluation
-> targeted repair plan v2 when gesture fails
-> reevaluation and quality-first selection
-> immutable AcceptedAssetVersion + variants + geometry
-> VAE production result through Delegation
-> Content Harness/Remotion validation and acknowledgement
-> usage receipt and Control Tower projection
```

Release 1 reference deployment is one modular control plane, one local GPU adapter, one cloud GPU adapter, content-addressed object storage, transactional event/metadata store, independent evaluator adapter, Delegation adapter, and existing Control Tower projection port. Exact deployable/image/provider versions are pinned in the release compatibility manifest after empirical proof.

## 5. Canonical release bundle

`Format02ReleaseBundle` pins:

- VAE product/build, all internal schema/compiler/runtime versions and source revision;
- Atomic Harness Builder target profile and extension points;
- published Delegation package/profile/message versions and generated bindings;
- category/format profile, syntax doctrine, demand/scene/Remotion fixture versions;
- asset/character/pose/expression/gesture/animation/scene registry snapshots;
- plan, workflow, capability, model, VAE, LoRA/control, runtime, evaluator, budget and Steering Recipe versions;
- local/cloud OCI image digests, custom-node locks, object-store/queue/runtime bindings;
- benchmark/protected-set versions, migrations, rollback bundle, and known limitations.

No field may be `latest`, mutable, unresolved, or architecture-pending in an implementation-authorized bundle.

## 6. State and acceptance authority

The VAE private execution follows TS-VAE-09. Delegation public lifecycle follows its `LIFECYCLE_MACHINE.yaml`. Production acceptance requires:

1. exact demand/plan/profile identity and no demand mutation;
2. passing technical integrity and required receipts;
3. passing semantic, Activative, wrong-reading, identity, expression/gesture/gaze, composition, crop, continuity/recurrence gates;
4. accepted master plus deterministic/receipted delivery variants;
5. composition geometry containing canvas/profile, subject/face/gesture/object BBOXes, gaze vector, negative space, safe crops, masks/depth/collision evidence;
6. complete production/evaluation/repair/budget/lineage receipts;
7. production authorization by VAE.

Downstream composition authorization is absent from VAE result. Completion requires a separate Delegation result acknowledgement from the Content Harness/composition runtime against current demand, sequence, composition, dependencies, and result.

## 7. Interfaces, events, provider adapters, and mocks

All interfaces are the production ports defined in TS-VAE-01 through TS-VAE-11. Stage 5 may start with:

- a `MockComfyUIAdapter` that consumes the exact `CompiledWorkflowArtifact` and returns fixture candidates/receipts;
- a `FixtureIndependentEvaluatorAdapter` that consumes the exact `EvaluationRequest` and returns signed fixture evaluations under an identity distinct from the producer;
- an in-process/durable test `WorkflowRuntimePort` only when the pinned Builder adapter is unavailable.

Mocks are explicitly `fixture_only`, cannot receive production certification, and cannot change interface shapes. A real local and cloud ComfyUI path, certified evaluator, and downstream composition consumer are required before limited production.

Public events use Delegation contracts; internal node events never leak. Required evidence includes async submission receipt/admission, execution progress, one quality repair, result readiness, acknowledgement, audit chain, and usage receipt.

## 8. Mandatory cross-cutting behavior

| Concern | Release 1 rule |
|---|---|
| Visual Production Plan IR | Provider-neutral canonical plan with preserved/mutable bindings and exact stage DAG. |
| ComfyUI graph | Compiled artifact only, digest-pinned and graph-validated; no manual production edits. |
| Docker/nodes/models/VAE/LoRA | Every artifact/resource is registry-resolved, content-hashed, compatible, and pinned. |
| GPU/storage | One local/self-hosted and one cloud profile pass execution/recovery; all media/receipts are content-addressed. |
| Deterministic/VLM | Deterministic integrity/geometry/policy/lifecycle plus independent VLM visual judgment. |
| Budget/candidates | Standard profile, 4 initial/10 max, two parallel jobs, cost/time/GPU ceilings, no gate reduction. |
| Selection | Hard-gate filter then registered quality-first ranking; first/fastest candidate cannot win by default. |
| Repair | At least one fixture path changes pose/gesture bindings only, preserves identity/expression/gaze/geometry/palette/alpha, and reruns invalidated nodes. |
| Idempotency/checkpoints | Duplicate submission, restart, out-of-order event, worker loss, and late output are safe and receipted. |
| Observability/cost | Full Control Tower evidence, traces, SLOs, cost per candidate/accepted asset, and audit links. |
| Security/isolation | Signed Delegation facts, least privilege, sandboxed untrusted inputs, isolated workers/evaluator, integrity and replay checks. |
| Migration/rollback | Old demand/result/plan/profile fixtures remain testable; runtime/workflow/evaluator rollback is rehearsed. |

## 9. Benchmark and certification architecture

Materialize the benchmark manifest minimums: 12 representative, 8 golden, 12 known failures, 8 adversarial, 12 mutations, 10 repairs, 12 recurrence, 8 infrastructure recovery, 30 evaluator calibration, and 8 compatibility/rollback cases. Cases may overlap only when each required label/evidence is explicit. Maintain a protected release set inaccessible to optimization prompts/training.

Certification stages are `represented`, `experimental`, `benchmarked`, `shadow`, `limited_production`, and `production_certified`. Product certification requires passing authority, schema, lifecycle, compatibility, resilience, security, evaluator, repair, compute, migration, rollback, and Format 02 end-to-end suites. A single happy path is insufficient.

Primary targets: >=90% autonomous completion after limited-production learning; >=98% expert-labeled semantic/Activative correctness for accepted assets with no known constitutional failure; >=92% composition pass without regeneration; >=99% recoverable-failure success; 100% reproducibility; >=90% repair precision; <=3 repair rounds; and declared evaluator hard-failure thresholds.

## 10. Failure, degradation, recovery, and rollback

Contract/authority/compatibility/integrity failures reject before admission. Feasibility conflict emits amendment proposal without mutation. Capability/budget gaps checkpoint and route typed exceptions. Infrastructure failures retry/fail over without quality rounds. Quality failures use causal repair. Evaluator uncertainty blocks/arbitrates. After three quality rounds, emit human/capability/amendment exception.

No declared mandatory feature may degrade. Optional degradation requires Delegation verdict and owner authorization and remains visible in result limitations. Cancellation/supersession/revocation fences stale promotion/consumption and preserves evidence.

Rollback bundle restores prior control-plane build, schemas/upcasters, registry snapshots, compiler, runtime images, workflow/model/VAE/LoRA/control/evaluator profiles, migration state, and projection version. Historical objects/events remain immutable. Backup/restore and rollback must pass before promotion.

## 11. Security and authority

Run Delegation authority, signature, hash, expiry, idempotency/replay, and lifecycle conformance. Prompt injection in notes/references cannot alter demand, tools, or evaluator policy. Workers are isolated and receive scoped objects/secrets. Producer/evaluator identity separation is enforced. Uncertified assets/capabilities cannot be claimed. Audit completeness is 100% for state-changing actions.

## 12. Implementation plan and units

1. Freeze published Delegation dependency and resolve its XRI-003/004/006/009/010 issues for VAE messages.
2. Pin Builder runtime/control-tower integration and release compatibility manifest.
3. Implement typed internal schemas/ports and provisional fixture adapters for exact Stage 5 interfaces.
4. Execute demand -> plan -> mock compiler/portfolio -> deterministic validation -> independent fixture evaluation -> one repair -> accepted asset -> geometry -> result.
5. Replace mocks with one real ComfyUI workflow, local GPU runtime, then cloud runtime under identical ports.
6. Build labeled evaluator/repair/recurrence sets and certify initial profiles.
7. Integrate real Delegation conformance and Content Harness/Remotion acknowledgement/usage path.
8. Complete Control Tower, security, resilience, compatibility, migration, rollback, metrics, and release receipts.

## 13. Given/When/Then acceptance criteria

1. Given VAD-F02-0001, when submitted twice after a timeout, then one execution runs and the existing receipt returns.
2. Given the demand notes contain prompt injection, when planning/evaluating, then authoritative fields and policies remain unchanged.
3. Given the initial portfolio includes contempt, centered gaze, identity drift, hand artifact, and one compliant candidate, when evaluated, then only hard-gate-pass candidates are eligible.
4. Given candidate C03 fails visible gesture while identity/expression/gaze/geometry pass, when repaired, then only allowed pose bindings and invalidated descendants rerun.
5. Given successful repair, when promoted, then accepted master, transparent variant, geometry, evaluation, production, budget, lineage, and limitation receipts are immutable and complete.
6. Given a VAE result, when Content Harness acknowledgement is absent, then Delegation remains `RESULT_READY`, not `COMPLETED`.
7. Given local worker failure after checkpoint, when cloud failover runs, then the same plan/artifact/bindings resume and no quality round is consumed.
8. Given cancellation or supersession racing with completion, when fencing applies, then stale output cannot promote or enter composition.
9. Given a request for an uncertified family/temporal/lip-sync feature, when compatibility resolves, then unsupported scope is blocked and not claimed.
10. Given deployment rollback, when reference/conformance suites rerun, then the previous certified release restores without historical-state loss.

## 14. Testing strategy

Execute unit and schema tests for every internal/public contract; workflow integration for every stage; Delegation authority/lifecycle/compatibility/resilience suites; evaluator/visual golden/adversarial/mutation/repair/recurrence tests; compute fault injection and local/cloud equivalence; service load/SLO/cost tests; security/isolation/replay tests; migration/backup/restore/rollback; accessibility and Control Tower evidence; and all 10 Delegation Format 02 scenarios plus the complete VAE benchmark portfolio.

## 15. Constitutional alignment V1.1 addendum

The Format 02 reference slice must prove the complete constitutional path without replacing its existing production, recovery, or downstream-consumption evidence:

1. canonical demand admission preserves Activative lineage, source applicability, Activation Contract, Visual Semantic Pack, Semiotic MCDA receipt, Visual Narrative Program, Feature Contracts, T/V request, Composition Intent, and non-empty locks;
2. the Composition Asset Pack reaches planning, routing, materialization, evaluation, repair, and accepted-asset lineage without semantic reconstruction;
3. interview-derived applicability requires Reaction Receipt and Expression Moment references, while not-applicable status is authoritative and explicit;
4. the materializer cannot infer recognition carrier, viewer role, narrative beat, meaning-bearing feature, or somatic route from free-form intent;
5. evaluation covers zero-second hook, pattern match, pattern interrupt, viewer-role clarity, activation direction, prediction gap, payoff, affinity, anticipation residue, anti-cliche strength, wrong-reading risk, Feature Contract compliance, and applicable delete-caption survival;
6. every failure includes responsible-layer evidence and repair changes only VAE-owned bindings;
7. selected-asset lineage resolves to the Activative Intelligence Pack and applicable Expression Moment;
8. a parseable but behaviorally unenforceable contract is rejected.

The benchmark adds negative cases for missing locks, missing lineage, missing interview provenance, carrier inference, viewer-role inference, feature-default drift, T/V narrative overreach, technical-pass/activation-fail, dominant wrong reading, and no-text caption dependence. These are specification and fixture requirements, not implementation authorization.

## 16. Readiness and non-goals

Stage 2 specification completion does not authorize implementation. Stage 4 must prove all Release 1 requirements owned, published Delegation version pinned, local/cloud strategies executable, evaluator tests and labeled set approved, fixtures complete, recovery/rollback testable, epics/stories complete, and Development Capsule ready.

Non-goals: every asset family, universal ComfyUI/provider support, final edited shorts, lip sync, manual graph operation, self-approval, or any production claim beyond the certified Format 02 character/scene slice.
