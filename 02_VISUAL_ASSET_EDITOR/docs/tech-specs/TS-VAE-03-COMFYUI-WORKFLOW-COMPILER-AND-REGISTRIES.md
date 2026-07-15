# TS-VAE-03 ComfyUI Workflow Compiler and Registries

Status: draft for architecture validation  
Implementation authorization: no

## 1. Specification identity

- Feature: F08
- Owned FRs: FR-057 through FR-064
- Owned NFRs: NFR-COMPAT-001 through NFR-COMPAT-005
- Decisions: D011, D027
- Components: `CapabilityRegistry`, `CompatibilityResolver`, `WorkflowCompiler`, `CompiledArtifactValidator`, `RegistryPromotionService`

## 2. Evidence read

VAE F08/F09/F12/F13 shards; plan and compatibility schemas; asset-family, Budget Program, readiness, and Format 02 seed registries; reference plan; preservation/prohibition contracts; Delegation compatibility policy/manifests/cases and contract ownership findings.

## 3. Problem, solution, and scope

The VAE must bind provider-neutral plan stages to reproducible ComfyUI execution without making workflow JSON canonical or allowing mutable models/nodes to alter an in-flight run. The solution is a versioned capability registry and deterministic compiler that emits an immutable `CompiledWorkflowArtifact` plus complete lock manifest.

In scope: workflow/model/VAE/LoRA/control/runtime registry records; compatibility graph; maturity/certification; deterministic ComfyUI API graph compilation; graph validation; impact analysis; promotion/deprecation/rollback. Out of scope: plan ownership, scheduling, model training, manual workflow operation, and provider-specific fields in public Delegation contracts.

## 4. Canonical registries and models

Every record has stable ID, semantic version, content hash, lifecycle/maturity, owner, source/provenance, compatibility edges, evidence refs, category/profile certification, security classification, and deprecation/rollback metadata.

| Record | Required provider details |
|---|---|
| `WorkflowProfile` | Provider, template hash, compiler version range, required node classes, typed inputs/outputs, capability claims, parameter domains, failure mappings. |
| `ModelProfile` | Architecture/family, weight digest, format, source/license, precision, VRAM class, supported tasks, VAE/LoRA/control compatibility. |
| `VaeProfile` | Digest, model compatibility, precision, decode constraints, known color/alpha behavior. |
| `LoraProfile` | Digest, base-model compatibility, trigger/weight domain, intended capability, training evidence, prohibited use, contamination/license status. |
| `ControlProfile` | Control type, preprocessor, node/version, model digest, coordinate/input contract, strength domain. |
| `RuntimeProfile` | OCI image digest, ComfyUI commit, Python/CUDA/driver constraints, custom-node lock, resource limits, network policy, health probes. |
| `CompatibilityEdge` | Source/target IDs and versions, relation, constraints, evidence, verdict, expiry. |
| `CapabilityBundle` | Immutable resolved set of workflow, model, VAE, LoRA, controls, runtime, compiler, evaluator requirements, and bundle hash. |

Maturity states are `represented`, `experimental`, `benchmarked`, `shadow`, `limited_production`, `production_certified`, `deprecated`, and `retired`. Production routes require category/profile certification, not merely structural representation.

## 5. Compiler contract

Input: exact `ProductionPlan` version/hash, plan stage, `CapabilityBundle`, typed runtime inputs, seed policy, and registry snapshot hash.

Output `CompiledWorkflowArtifact`:

- artifact ID/version/hash and compiler ID/version/hash;
- source plan/stage and capability bundle refs;
- provider `comfyui` and API-format workflow JSON as an opaque compiled payload;
- deterministic input/output port map and object refs;
- seed(s), parameter bindings, mutable repair slots, and preserved binding checks;
- model/VAE/LoRA/control filenames resolved only from digest-pinned registry mounts;
- OCI image digest, ComfyUI commit, custom-node names/commits/hashes;
- graph allowlist verdict, static resource estimate, security policy, and compile receipt.

Compilation pipeline: validate plan -> resolve exact bundle -> expand registered template -> bind typed values -> resolve mounted resources -> canonicalize node ordering/IDs -> validate graph/dataflow/allowlist -> estimate resources -> hash payload and manifest -> persist immutably.

## 6. Interfaces, state, APIs, and events

```text
resolve(requirements, category_profile, budget, registry_snapshot) -> CapabilityBundleRef
compile(plan_stage_ref, bundle_ref, input_refs) -> CompiledWorkflowArtifactRef
validate_artifact(artifact_ref) -> CompilationValidationReceipt
assess_change(old_record, new_record) -> CompatibilityImpact
promote(record_ref, evidence_bundle, target_maturity) -> PromotionReceipt
```

Registry states: `DRAFT`, `VALIDATED`, `EXPERIMENTAL`, `BENCHMARKED`, `SHADOW`, `LIMITED_PRODUCTION`, `PRODUCTION_CERTIFIED`, `DEPRECATED`, `RETIRED`, `REJECTED`. Promotion is monotonic except governed rollback/deprecation; evidence is immutable.

Events: `CapabilityRegistered`, `CompatibilityResolved`, `CompilationCompleted`, `CompilationRejected`, `CapabilityPromoted`, `CapabilityDeprecated`, `ImpactDetected`. Events include exact old/new versions and affected active/new-run policy.

## 7. Cross-cutting production contract

| Concern | Required behavior |
|---|---|
| Visual Production Plan IR | Compiler consumes an exact plan stage and cannot add semantic goals or undeclared mutable bindings. |
| APIs/queues | Compilation is a deterministic control-plane command; execution artifact refs are queued to TS-VAE-04. |
| Provider adapters | `WorkflowCompiler` is provider-pluggable; Release 1 certifies only the ComfyUI adapter. |
| Docker/custom-node locking | OCI digest, ComfyUI commit, every custom-node repository commit/hash, and Python dependency lock are mandatory. Mutable tags and startup installs are forbidden. |
| Model/VAE/LoRA registries | Every mounted resource resolves by digest and compatibility edge; arbitrary filesystem names are invalid. |
| GPU/storage | Runtime profile declares VRAM/compute/storage class; artifacts and resources use content-addressed object refs/mounts. |
| Deterministic/VLM | Compilation, validation, compatibility, and promotion gates are deterministic. Models do not design graphs. |
| Budgets/candidates | Resource estimate and supported parallelism feed TS-VAE-05; compiler cannot raise ceilings. |
| Evaluation/repair | Artifact exposes evaluator output refs and only declared repair slots. Evaluator is never embedded as producer self-approval. |
| Idempotency/checkpoints | Same plan/bundle/compiler/input hashes yield same artifact hash. Compiled artifact is a checkpoint. |
| Observability/cost | Receipt includes compile duration, graph/node counts, resource estimate, cache status, and lock identities. |
| Security | Node classes are allowlisted; arbitrary code, shell, network fetch, dynamic install, path traversal, and unregistered output paths are blocked. |
| Migration/rollback | New registry/compiler versions affect new bundles only. Historical artifacts remain executable only in their pinned runtime; rollback selects prior certified bundle. |

## 8. Detailed behavioral rules

1. ComfyUI JSON is generated, immutable, and provider-private; it cannot be submitted as a plan or edited during a certified run.
2. Templates contain symbolic registry IDs, never environment-specific model paths.
3. All graph nodes and extension versions must be present in the runtime lock and allowlist.
4. Graph validation checks acyclicity where required, typed ports, required outputs, no orphan critical output, bounds, seed policy, and plan-preservation assertions.
5. A LoRA must declare base model, intended function, validated weight interval, and evidence; unsupported combinations fail resolution.
6. A runtime cannot claim a capability solely because a model file is mounted.
7. Active runs never adopt registry updates. The bundle hash is part of execution identity.
8. Patch/minor/major classification follows behavioral compatibility, not file-format similarity.
9. Promotion requires benchmark, recovery, evaluator, security, and rollback evidence appropriate to maturity.
10. Impact analysis identifies affected workflows, profiles, tests, runs, assets, and rollback routes before a record changes status.

## 9. Failure and recovery

Compilation failures use stable codes: `PLAN_BINDING_INVALID`, `CAPABILITY_UNRESOLVED`, `INCOMPATIBLE_BUNDLE`, `NODE_NOT_ALLOWED`, `CUSTOM_NODE_MISSING`, `MODEL_INTEGRITY_FAILED`, `PORT_TYPE_MISMATCH`, `RESOURCE_ESTIMATE_EXCEEDS_PROFILE`, and `NONDETERMINISTIC_COMPILE`.

Registry or object-store outage is retryable with the same snapshot. Hash mismatch, unallowlisted node, or incompatible model is non-retryable until a new registry/plan version exists. A compiler crash leaves no visible partial artifact. Provider execution failures are owned by TS-VAE-04; quality failures by TS-VAE-07.

## 10. Performance, security, and compatibility

Compilation should be CPU-bound, cacheable by complete input hash, and finish before GPU reservation. Cache entries are immutable and tenant/policy scoped. Registry reads use signed snapshots. Resource downloads occur during image/resource preparation, never from an active workflow.

Registry APIs require separate read, submit, validate, promote, deprecate, and emergency-revoke roles. Weight/node provenance and license policy are mandatory. Secrets are injected at runtime and excluded from artifacts.

Stage 3 Delegation compatibility manifests declare only supported product/protocol/profile behavior; internal model/workflow details remain VAE-private. Major registry schema changes require migration fixtures and historical read support.

## 11. Implementation plan

1. Define closed schemas and repository ports for all registry records, edges, snapshots, bundles, artifacts, and receipts.
2. Build deterministic compatibility resolution with explainable rejection paths.
3. Implement ComfyUI template format and compiler with canonical serialization.
4. Implement graph/node/resource security validator and lock verification.
5. Create one Format 02 workflow profile and unresolved physical model/evaluator control IDs marked experimental until empirical proof.
6. Implement promotion, impact, deprecation, revocation, and rollback flows.
7. Add registry/compiler compatibility, mutation, security, reproducibility, and golden-graph tests.

## 12. Given/When/Then acceptance criteria

1. Given the same plan, bundle, inputs, and compiler, when compiled twice, then artifact hashes are identical.
2. Given an unregistered model filename, when graph binds, then compilation fails before GPU reservation.
3. Given a mutable container tag or startup node install, when runtime profile validates, then it is rejected.
4. Given a LoRA incompatible with the selected base model, when resolving, then no bundle is produced.
5. Given an unallowlisted custom node or network-fetch node, when validating, then execution is blocked and audited.
6. Given a production-certified bundle update, when a run is active, then the run retains the old bundle while new runs may select the new version.
7. Given a registry rollback, when the prior bundle is selected, then its exact graph/runtime/resource hashes are restored.
8. Given raw ComfyUI JSON submitted as canonical product state, when intake validates, then it is rejected.

## 13. Testing strategy

Use schema and repository unit tests, property tests for deterministic resolution/serialization, golden ComfyUI graph tests, node allowlist and malicious graph tests, model/hash corruption tests, compatibility matrix tests, migration/rollback fixtures, concurrent snapshot tests, and an end-to-end compile of the Format 02 reference plan without executing GPU work.

## 14. Constitutional alignment V1.1 addendum

The compiler materializes a plan; it does not recover upstream semantics. A CompiledWorkflowArtifact must contain a deterministic binding receipt from each applicable Composition Asset Pack obligation to a typed provider input, control, mask, geometry instruction, evaluator input, or explicit preflight rejection.

Required compiler inputs include the selected recognition carrier, Visual Narrative Program, Feature Contracts, T/V request, Composition Intent, wrong-reading locks, and the Semiotic MCDA receipt reference. The Semiotic MCDA receipt is preservation evidence for the selected carrier; the compiler does not rerun semiotic selection.

Feature Contracts are enforced through registered capability slots for meaning-bearing gaze, hands, posture, witness relations, object punctum, negative space, contact, distance, crop, motion, light, and sequence when applicable. A model default is not an implementation of a Feature Contract. Unsupported required features produce CAPABILITY_UNRESOLVED or PLAN_BINDING_INVALID before GPU reservation.

T/V instructions may bind texture, camera, proximity, stillness, weight, breath, or environment controls only after the plan has frozen carrier and narrative. Provider prompts and graph parameters are derived artifacts with source pointers; they cannot add a viewer role, recognition carrier, narrative beat, wrong-reading lock, or activation direction.

Golden compiler tests must prove full binding coverage, reject dropped constitutional fields, reject graph templates that depend on model defaults for required features, and reproduce identical artifacts for identical Composition Asset Pack and registry snapshots.

## 15. Non-goals

- A visual node editor or routine manual graph maintenance path.
- Supporting every ComfyUI node, model family, provider, or asset family in Release 1.
- Training LoRAs or certifying evaluator behavior.
- Exposing internal capability details through Delegation messages.
