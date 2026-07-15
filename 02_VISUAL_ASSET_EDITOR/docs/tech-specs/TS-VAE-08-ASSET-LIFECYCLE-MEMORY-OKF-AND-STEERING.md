# TS-VAE-08 Asset Lifecycle, Memory, OKF, and Steering

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Features: F03, F04, F11, F17
- Owned FRs: FR-017 through FR-032; FR-081 through FR-088; FR-129 through FR-136
- Owned NFRs: NFR-MEM-001 through NFR-MEM-005
- Decisions: D006, D007, D008, D014, D020
- Components: `AssetRepository`, `AssetLifecycleService`, `VariantService`, `UsageReceiptService`, `VisualAssetMemory`, `RetrievalPipeline`, `OKFProjector`, `SteeringRecipeRegistry`

## 2. Evidence read

VAE F03/F04/F11/F17 shards; asset family registry; memory, result, geometry, steering and compatibility schemas; OKF profile; Format 02 seed registries and recurrence benchmarks; Delegation result/acknowledgement/invalidation/revocation/replacement contracts and post-completion lifecycle.

## 3. Problem, solution, and scope

The VAE must keep references distinct from production assets, preserve immutable lineage, reuse valid work, understand contextual recurrence, and learn safely across runs. The solution is an append-only asset/lineage store with a current-state projection, one usage receipt per rendered use, authority-aware multimodal retrieval, non-authoritative OKF projection, and evidence-gated Steering Recipe promotion.

In scope: eight-family ontology, represented/certified scope, reference/production separation, immutable versions/variants, lineage/supersession, memory and usage, recurrence, retrieval, OKF, Steering Recipes, lifecycle notifications, and rollback. Out of scope: becoming a media DAM for unrelated assets, using vector search as truth, final sequence/composition authority, or automatic learning from one run.

## 4. Canonical models and storage

`AssetIdentity`: asset ID, immutable version, family/subtype, role bindings, content hash, master object ref, producer plan/execution/candidate refs, created principal/time, and certification profile.

`ReferenceEvidence`: reference ID/version/hash/URI, owner/source/provenance, permitted use, role (identity/pose/style/evidence), integrity state, and promotion status. It is never a production asset without explicit derived asset/version and acceptance.

`ProductionAssetVersion`: identity, master, delivery variants, geometry, masks/depth, evaluation/production/budget receipts, lifecycle state, lineage edges, limitations, and production authorization. It does not contain downstream consumption authorization.

`DerivationEdge`: typed `derived_from`, `variant_of`, `repaired_from`, `supersedes`, `replaces`, `uses_reference`, or `compiled_from` edge with source/target versions, plan/node, transformation, evidence, and hash.

`VisualUsageReceipt`: exact asset/version/variant, consuming harness/sequence/scene/composition versions, syntax role, Activative function, geometry, neighboring assets/text, render ref/hash, timestamp, and acknowledgement/invalidation state.

`MemoryRecord`: asset/usage/lineage/evaluation summaries, visual and syntax fingerprints, current lifecycle projection, compatibility/certification, contradiction/supersession refs, and authority labels.

`SteeringRecipe`: versioned applicability, intervention, preserve/prohibit rules, evidence cohort, control comparison, compatibility, maturity, benchmark, limitations, and rollback/deprecation.

Canonical operational records live in transactional metadata/event storage with immutable media in object storage. Embeddings, indexes, caches, and OKF documents are rebuildable projections.

## 5. Lifecycle and state

Internal asset states: `REFERENCE`, `CANDIDATE`, `TECHNICALLY_VALID`, `EVALUATED`, `PRODUCTION_ACCEPTED`, `SUPERSEDED`, `INVALIDATED`, `REVOKED`, `RETIRED`. Delivery variants inherit master validity but have independent hashes/technical checks. Illegal transitions reject and receipt.

Promotion to `PRODUCTION_ACCEPTED` requires exact demand/plan/candidate lineage, passing evaluation, complete receipts, geometry when required, and certified capability/profile. A new accepted version never overwrites the old one. Delegation acknowledgement changes external consumption state, not VAE production acceptance.

Supersession notifies known consumers through Delegation. Invalidation requires revalidation; revocation blocks new/active use. Replacement creates a new result/asset link and awaits downstream acknowledgement. History and negative evidence remain reproducible.

## 6. Retrieval, recurrence, and steering flow

Retrieval order is deterministic authority/task resolution -> lifecycle/certification/compatibility hard filters -> typed graph traversal -> lexical/structured search -> multimodal similarity -> image/composition/syntax matching -> independent VLM rerank -> contradiction/exception/supersession inclusion -> Minimum Complete Context compilation -> retrieval receipt.

Recurrence classes are `beneficial_continuity`, `productive_variation`, `neutral_reuse`, `redundant_repetition`, `fatiguing_similarity`, and `contradictory_use`. Inputs include role, sequence distance, geometry, pose/expression/gaze, visual neighborhood, identity value, prior outcomes, and syntax context. Count alone cannot determine class.

Steering flow: collect immutable outcomes -> group comparable cases -> require minimum evidence/control -> draft recipe -> sandbox benchmark -> shadow -> limited production -> production certification. Promotion is human/policy governed and registry receipted; one success cannot promote.

## 7. Interfaces, events, and integration contract

```text
register_reference(reference) -> ReferenceRef
record_candidate(candidate_manifest) -> CandidateRef
promote(candidate_ref, evaluation_ref, receipts) -> AcceptedAssetRef
derive_variant(master_ref, transform_profile) -> VariantRef
supersede(old_ref, new_ref, reason) -> SupersessionReceipt
record_usage(usage_receipt) -> UsageRef
retrieve(task_context, constraints, budget) -> RetrievalBundleRef
project_okf(record_refs, profile_version) -> OKFArtifactRef
propose_recipe(evidence_cohort, intervention) -> RecipeRef
promote_recipe(recipe_ref, benchmark_receipt, target_state) -> PromotionReceipt
```

Events: `ReferenceRegistered`, `CandidateRecorded`, `AssetPromoted`, `VariantCreated`, `AssetSuperseded`, `AssetInvalidated`, `AssetRevoked`, `UsageRecorded`, `MemoryProjected`, `RetrievalCompleted`, `RecipePromoted`, `RecipeRolledBack`.

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Retrieval refs and selected asset versions are immutable plan inputs; memory cannot mutate demand/plan. |
| APIs/queues | Lifecycle writes are transactional; projections/retrieval indexing use idempotent events and checkpoints. |
| Provider adapters/ComfyUI/Docker locks | Asset lineage records exact provider adapter, compiled artifact, OCI image, bundle, runtime, model, VAE, LoRA, and control identities. |
| GPU/storage | Masters/evidence are content-addressed; derivative compute goes through TS-VAE-04; retention classes are explicit. |
| Deterministic/VLM | Authority/filter/graph/context compilation is deterministic. VLM classifies/reranks visual/syntax suitability with evidence. |
| Budget/candidates | Reuse is considered before production; retrieval and rerank consume bounded plan budget. |
| Evaluation | Reuse requires current applicable evaluation/certification; stale assets revalidate. |
| Repair | Repair outcomes append lineage/evidence and can seed recipe cohorts only after controls. |
| Idempotency/checkpoints | Asset hash/version, usage identity, projection event, and recipe promotion keys prevent duplicates. |
| Observability/cost | Record reuse rate, retrieval contribution, recurrence accuracy, index lag, projection failures, quality/cost delta. |
| Security | Tenant/authority filters precede similarity; signed URLs are scoped; sensitive references/embeddings follow access/retention policy. |
| Migration/rollback | Ontology, memory, index, OKF, and recipe versions migrate through immutable jobs. Index/OKF rebuild; rollback selects prior projection/recipe without changing history. |

## 8. Detailed behavioral rules

1. All eight families are represented, but Release 1 certifies only declared Format 02 AF-02 scope and limited dependencies.
2. Family/subtype records require harness role, Activative function, syntax role, composition slot, and capability requirements.
3. Reference evidence and production assets use distinct IDs, states, schemas, and promotion authority.
4. Accepted masters are immutable; delivery variants are deterministic or receipted derivatives linked to a master.
5. Reuse requires exact version, current lifecycle, compatible demand/profile, role/geometry suitability, and applicable evaluation.
6. Every rendered use creates one usage receipt; planned or retrieved use is not rendered use.
7. Superseded/revoked records remain historical evidence and are excluded from current retrieval unless explicitly requested as negative evidence.
8. Authority and compatibility filters execute before vector/image similarity.
9. Minimum Complete Context includes supporting, contradictory, exceptional, and superseding evidence with source refs.
10. OKF documents cannot drive live state transitions, locks, queues, budgets, or contract validation.
11. Steering evidence must compare intervention and baseline under compatible conditions and disclose confounders.
12. Recipe application is itself receipted and version-pinned; active runs never adopt recipe updates.

## 9. Failure, recovery, performance, and security

Hash/lineage/receipt gaps block promotion. Projection/index failure does not corrupt canonical records; rebuild from events. Retrieval with unavailable index falls back to deterministic graph/structured retrieval and declares degradation; it cannot skip authority filters. Conflicting lifecycle notices fail safe and require resolution. Revocation propagation is urgent and audited.

Metrics: promotion completeness, lineage integrity, variant reuse, usage receipt completeness, retrieval precision/contribution, recurrence confusion matrix, contradiction coverage, context size, OKF/index lag, recipe uplift/regression, and cost per accepted/reused asset.

Access is object/tenant/principal scoped. External references are integrity/provenance checked. Embeddings and previews inherit source classification. Deletion/legal hold and negative-evidence quarantine are explicit; secrets never enter OKF.

## 10. Implementation plan

1. Close ontology, reference, asset, variant, lineage, usage, memory, retrieval, OKF, recipe, and lifecycle schemas.
2. Implement append-only repositories, current projections, content addressing, and lifecycle guards.
3. Implement promotion/variant/supersession/invalidation/revocation/replacement integration.
4. Implement usage receipt and syntax fingerprint generation.
5. Build authority-aware hybrid retrieval and Minimum Complete Context receipts.
6. Build OKF projector and rebuildable index pipeline.
7. Implement Steering Recipe evidence, benchmark, promotion, application, deprecation, and rollback.
8. Add recurrence/retrieval benchmarks, security/retention tests, migration, and rollback.

## 11. Given/When/Then acceptance criteria

1. Given reference evidence, when production delivery is requested, then it cannot ship without a distinct derived production asset and passing acceptance.
2. Given an accepted master, when a delivery crop is derived, then both hashes and lineage are preserved and the master is unchanged.
3. Given a superseded asset, when ordinary retrieval runs, then it is excluded while its negative/historical evidence remains queryable.
4. Given repeated character identity in productive varied contexts, when recurrence evaluates, then count alone cannot produce fatigue.
5. Given a semantically similar asset owned by another tenant, when retrieval runs, then authority filtering excludes it before similarity.
6. Given an OKF/index outage, when lifecycle writes occur, then canonical state remains correct and projections can rebuild.
7. Given one successful repair, when recipe promotion is requested, then promotion is rejected for insufficient controlled evidence.
8. Given a revoked recipe/asset during an active run, when policy applies, then unsafe future use blocks and historical run identity remains reproducible.

## 12. Testing strategy

Unit-test state transitions, immutability, lineage, variants, filters, context compilation, and recipe guards. Contract-test Delegation result/acknowledgement/notices. Integration-test event projection, object storage, indexing, OKF rebuild, retrieval, supersession, and revocation. Behavioral-test recurrence and retrieval against benchmark controls. Adversarially test cross-tenant leakage, stale assets, frequency-only fatigue, poisoned evidence, and OKF-as-authority. Run performance, migration, rollback, and Format 02 continuity/reuse tests.

## 13. Constitutional alignment V1.1 addendum

Every selected or promoted asset must be traceable through immutable typed edges to the canonical demand, Activative Intelligence Pack, Identity DNA, Context Premise, Resonance, Matrix of Edging, source evidence, and applicable Reaction Receipt and Expression Moment references. Generic provenance text, filenames, embeddings, or OKF summaries do not satisfy this trace.

ProductionAssetVersion and MemoryRecord preserve the canonical reference IDs, owner/version/hash evidence, source-kind applicability result, Composition Asset Pack reference, evaluation-profile version, and the evaluation and production receipts that selected the asset. Delivery variants inherit this lineage from the accepted master and record the deterministic transform; they do not duplicate or reinterpret upstream meaning.

When the canonical demand declares interview-derived source, missing Reaction Receipt or Expression Moment lineage blocks promotion. When it declares not applicable, the authoritative applicability evidence is retained. When it supplies neither, VAE fails closed and does not infer the source class.

Retrieval may use the new layers as authority filters and relevance features, but it cannot merge contradictory Activation Contracts, replace a selected recognition carrier, or treat a semantically similar asset as lineage-equivalent. Reuse requires the new demand to be compatible with the prior asset's constitutional bindings and current evaluation profile.

An additional lineage acceptance test starts from an accepted asset and resolves every edge back to its Activative Intelligence Pack and, when applicable, its Reaction Receipt and Expression Moment without consulting free-form notes.

## 14. Non-goals

- A vector database, OKF document, or embedding as canonical operational truth.
- Automatic production learning from one outcome.
- Certification claims for all represented asset families.
- Final sequence/composition authority or broad media-library replacement.
