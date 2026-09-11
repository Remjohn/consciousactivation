# TS-SKL-001 - Canonical Skills, Skill Composition Recipes, Steering Recipes, and Transformation Contracts

```yaml
spec_id: TS-SKL-001
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Atomic Harness Pipeline
primary_owner: Atomic Harness Pipeline
cross_product_semantic_owner: Activative Intelligence Runtime
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 3
controlling_story: ST-07.02
controlling_frs: [FR-031, FR-032, FR-033, FR-034, FR-035, FR-036]
```

This is a specification-only candidate. It does not authorize implementation, product adoption, a Development Capsule, production, certification, or `ACCEPTED_FOR_BUILD`.

## 1. Files and authorities read

The writer consumed two exact Wave 3 interface drafts under the mandatory label `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Upstream draft | State | SHA-256 | Role and revision impact |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-002.md` | `WRITTEN_PENDING_AUDIT` | `3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4` | Supplies the draft `AtomicHarnessDefinition` intake, Harness requirement projection, execution-binding, explicit `NOT_APPLICABLE`, transaction, replay, and selective-invalidation interfaces. A changed hash reopens sections 3, 5, 6, 8, 9, and 10. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-005.md` | `WRITTEN_PENDING_AUDIT` | `5dcf631efc4f68f40edd0991ca3ae4be9073da68aa441c52d37e874e70a43e49` | Supplies the draft Primitive Coalition, Coalition Signature, Edge Product, typed Steering Recipe candidate, eligibility, ownership, evaluation, and invalidation interfaces. A changed hash reopens sections 3, 5, 6, 8, 9, and 10. |

Neither draft is ratified or accepted authority. Current Constitution V1.1 and current product authorities remain binding. Prompt 02C authorizes candidate-specification work only.

| Source | Version/state | SHA-256 | Authority/dependency class | Specific fact used |
|---|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current pointer | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | required current authority | Constitution V1.1 takes precedence over subordinate drafts and implementations. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | highest-order authority | Builder declares the Harness, Pipeline executes it, and downstream execution cannot invent upstream Activative meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | candidate ownership | Pipeline owns workflow execution, bindings, JIT state, receipts, evaluation control, and selective repair; it does not own AIR semantic compilation or VAE production strategy. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | candidate object ownership | AIR owns semantic lifecycle and production-program meaning; Builder owns `AtomicHarnessDefinition`; Pipeline owns execution state and Visual Asset Demand emission. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../prd/features/F06-skills-skill-composition-recipes-steering-recipes-and-transformation-contracts.md` | `DRAFT_FOR_HUMAN_RATIFICATION` | `8cc1002a770b175d0f43dce6872098bea9eb3a5445c4e31f048900c339f954f4` | controlling candidate feature | Defines FR-031 through FR-036, separates stable procedure, conditional strategy, and creative boundary, and prohibits recipe authority inversion. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | controlling Story | ST-07.02 requires explicit Skill binding, eligibility/exclusion, replay, and selective recovery without mutating canonical Skills. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../planning/spec_assignments/TS-SKL-001.md` | assignment brief only | `7fb2fc59e234371f803f83c5d2bdf83a4153002efd6f0d8fce33007decab0f35` | bounded assignment | Fixes the six FRs, one Story, mandatory ten-section structure, and source IDs; it is not itself a Tech Spec. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/jit_capsule.py` | current Builder implementation | `6546b1e879961be6336b7e519590f380afe2a16f30768587c1686b8d3c47ee4e` | `SRC-CUR-009`; required current implementation | Existing phase-local capsule pins exact Skill package and Minimum Complete Context hashes, rejects unjustified or inapplicable context, carries locks and lineage, and remains non-production/non-certified. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/skill_registry.py` | current Builder implementation | `2671b5cf716b093e48e658c9aec9922619ee04a8da6da9680a515fcbaefd4da8` | brownfield contract evidence | Synthetic proof distinguishes canonical Skills, local adaptations, experiments, recipes, and capsules; undeclared Skill use fails closed; its empty registry is synthetic-only and cannot be generalized as current production truth. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/skills/necessity.py` | current Builder implementation | `484ee11bedcdbb4717b9a1adea72751695e956cab074ab19f72db732defe559a` | brownfield decision evidence | Skill necessity is an explicit governed decision and cannot be inferred from convenience or capability labels. |
| `02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md` | current VAE draft authority | `9acefd1eaa224cd9de3dd5d39fec7443dfd6edcbac32a1dfe97355e1b8230aa7` | `SRC-CUR-020`; required authority | VAE owns production-derived visual Steering Recipe evidence and lifecycle; authority/compatibility filters precede similarity and Minimum Complete Context excludes the full corpus by default. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | current | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | source disposition authority | `SRC-CUR-009` is required current implementation and `SRC-CUR-020` is required authority; both exact bytes are available. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery-authorized packet registry | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | frozen packet | Fixes output path, FRs, Story, dependencies, claim ceiling, and six downstream revision-impact sections. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only authorization | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | WRITE authorization | Writing and technical convergence are permitted while build, capsule, production, and certification authority remain false. |

The `...` prefix in three rows expands to `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED`. The target is authorized as `DIRECT_PRODUCT_SPEC_PATH`; no target-local or ancestor `AGENTS.md` applies to `05_ATOMIC_HARNESS_PIPELINE`. The historical assignment path under `04_ATOMIC_HARNESS_PIPELINE` does not grant path ownership and is superseded by the frozen recovery packet.

## 2. Problem, user outcome, solution, and scope

### Problem

A Workflow Node needs a stable procedure, a phase may need a reusable composition of procedures, a taste-bearing operation may need conditional evidence-backed Steering guidance, and an editing or composition action needs explicit creative boundaries. Collapsing these into one prompt, note, or provider configuration destroys authority and replay. It allows a local tweak to mutate a Canonical Skill, lets semantic similarity bypass lifecycle eligibility, makes a visual-production recipe look like AIR semantic truth, and permits an operation to weaken wrong-reading locks while claiming only to change execution details.

The current Builder synthetic proof establishes useful integrity patterns but contains an intentionally empty Skill registry scoped to a synthetic demonstration. Pipeline cannot interpret that empty fixture as a program-wide declaration that Skills never exist. Conversely, Pipeline cannot dynamically discover an undeclared Skill, infer `NOT_APPLICABLE`, or compile missing semantic meaning from recipe text.

### User and system outcome

A Harness runtime can resolve each learned or agentic node to one exact versioned Canonical Skill; apply a separately versioned Harness-local adaptation without changing the Skill; bind a durable Skill Composition Recipe to exact nodes, contracts, modules, references, and runtime embodiments; retrieve only authority-eligible Steering Recipes for the current coalition, archetype, composition state, category/profile, failure, and embodiment; and compile one immutable Transformation Contract for each editing or composition operation. Every decision is hash-pinned, denied or committed atomically, selectively invalidated, historically replayable, and attributable to its owning product.

### Bounded solution

Define a Pipeline subsystem that:

1. consumes Builder-declared Skill requirements and exact execution bindings without editing `AtomicHarnessDefinition`;
2. resolves Canonical Skills through an authority-scoped registry snapshot and validates exact package identity, lifecycle, compatibility, contracts, tool needs, and evidence;
3. binds separately versioned local adaptations whose delta is limited to declared adaptation points;
4. compiles immutable Skill Composition Recipes from exact Skills, modules, references, upstream semantic contracts, and runtime bindings;
5. queries owner-specific Steering Recipe registries after deterministic authority, lifecycle, lineage, compatibility, and failure filters;
6. compiles operation-specific Transformation Contracts from immutable upstream conditions, requested changes, declared creative degrees of freedom, and inherited wrong-reading locks;
7. emits append-only artifacts, dependency edges, decisions, events, and receipts with deterministic replay and selective invalidation.

### In scope

- FR-031 through FR-036 and ST-07.02.
- Canonical Skill reference and package validation, necessity parity, exact registry snapshots, and node binding.
- Harness-local Skill adaptation binding without Canonical Skill mutation.
- Skill Composition Recipe contracts and runtime binding.
- Steering Recipe query, deterministic eligibility, typed exclusion, bounded reranking, binding, and receipt.
- Transformation Contract compilation, lock inheritance, operation validation, supersession, invalidation, replay, and rollback.
- Exact proposed implementation paths, schemas, interfaces, failures, tests, and completion evidence.

### Out of scope and non-goals

- Creating or modifying `AtomicHarnessDefinition`; Builder remains its owner.
- Compiling Primitive, coalition, archetype, Final Script, Activation Transfer, Composition Intent, or other AIR meaning.
- Owning VAE Visual Production Plans, provider/model/LoRA selection, production evaluation, repair, or acceptance.
- Promoting AIR or VAE Steering Recipes, changing their lifecycle, or merging their distinct meanings into a generic recipe authority.
- Discovering new Skills, designing a missing Canonical Skill, or approving an adaptation without the separately governed authority path.
- Executing provider work, publishing, activating Format 02, beginning VAE Stage 5, claiming production eligibility/certification, or issuing a Development Capsule.
- Treating prompts, free-form notes, OKF projections, embeddings, caches, or model outputs as canonical Skill or recipe state.

## 3. Architecture traceability, existing backend integration, product ownership, and governing decisions

### Current versus candidate authority

Current Constitution V1.1 and current product authorities remain binding. The V2.1 ownership matrices, the AHP F06 feature, and both upstream specs are `CANDIDATE_NOT_CURRENT`. Their interfaces may guide this written draft because Prompt 02C explicitly authorizes specification work. This spec is `WRITTEN_PENDING_AUDIT`; build authority is false. Before attributable ratification, its maximum possible later state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

### Product and object ownership

| Object or decision | Authoritative owner | Pipeline responsibility | Pipeline prohibition |
|---|---|---|---|
| `AtomicHarnessDefinition`, node Skill requirement, adaptation declaration, required operation boundary | Atomic Harness Builder / Builder-generated Harness | Resolve exact immutable refs and prove parity. | Add, remove, reinterpret, or weaken Harness declarations. |
| Canonical Skill stable procedure and package release | Declared Skill owner under the governed registry; Pipeline for Pipeline-owned procedural Skills | Validate exact owner/version/hash/contracts and execute only through an eligible binding. | Acquire ownership through loading, caching, adaptation, or execution. |
| Harness-local adaptation authorization | Builder-generated Harness plus declared adaptation owner | Bind exact delta to allowed adaptation points and record evidence. | Patch Canonical Skill bytes or broaden authority/tools/side effects. |
| Primitive Coalition, Coalition Signature, Edge Product, archetype coalition, Final Script, Composition Intent, semantic Steering Recipe | Activative Intelligence Runtime | Filter, retrieve, bind, execute, evaluate, and invalidate exact refs within the Harness. | Rebuild semantic meaning, promote a candidate, or treat a recipe as its source. |
| Visual-production Steering Recipe and production evidence | Visual Asset Editor | Consume typed VAE recipe refs when a VAE-owned route declares them eligible. | Convert VAE production guidance into AIR semantic authority or direct VAE internals. |
| Skill Composition Recipe and runtime binding | Atomic Harness Pipeline | Compile procedure composition and execution order from exact declared inputs. | Use composition to rewrite semantic or Skill authority. |
| Transformation Contract execution artifact | Atomic Harness Pipeline, bounded by the Builder-declared operation and upstream semantic owners | Compile exact operation constraints and enforce them at every candidate/evaluation/repair handoff. | Relax upstream must-remain-true conditions, wrong-reading locks, source lineage, or Composition Intent. |
| Recipe/Skill lifecycle promotion and release | Owning product and Program Control as governed | Enforce current state and exact release. | Self-promote based on successful execution or similarity. |
| Independent evaluation receipt | Independent Evaluation | Request and consume the receipt; coordinate responsible repair. | Let a producer accept its own judgment-bearing output. |

`Activative Contract Compiler != Activative Intelligence Runtime`. Builder declares exact semantic dependencies and compiles a Harness structure; it does not create AIR semantic truth. Pipeline executes an approved Harness; it does not become Builder or AIR. VAE production realization does not become Pipeline or AIR authority.

### Governing decisions

1. **Stable procedure is not creative meaning.** A Canonical Skill specifies repeatable procedure, typed inputs/outputs, invariants, failure law, evidence, and tool envelope. It may consume semantic objects but cannot originate or silently mutate their meaning.
2. **Node binding is explicit.** Every learned or agentic Workflow Node has one exact Canonical Skill reference. Label similarity, package name, implementation import, or registry search is not a binding.
3. **Necessity precedes use.** A deterministic or human-only node may carry an explicit governed `NOT_APPLICABLE` Skill decision. Learned or agentic nodes cannot. Missing Skill evidence is a blocker, not permission for an inline prompt.
4. **Adaptation is a separate immutable delta.** A Harness-local adaptation names exact base Skill, adaptation points, changed values, rationale, authority, scope, evidence, compatibility, and rollback. Its presence never changes base bytes or global registry state.
5. **Composition is procedural.** A Skill Composition Recipe assembles exact Skills, modules, reference inputs, handoffs, and runtime binding constraints. It must not encode a replacement Primitive coalition, archetype, Final Script, Composition Intent, or VAE production strategy.
6. **Eligibility precedes ranking.** Registry owner, lifecycle state, validity, category/profile, coalition/archetype, composition state, failure code, embodiment, provider/tool compatibility, evidence, and known regressions are hard filters. Lexical/vector/image/composition similarity and VLM comparison can rank only the surviving set.
7. **Recipe kinds remain distinct.** `AIR_SEMANTIC_STEERING` and `VAE_VISUAL_PRODUCTION_STEERING` are different owner-scoped contracts. A generic projection may index both but cannot erase `recipe_kind`, `recipe_owner`, contract ID/version/hash, or lifecycle authority.
8. **A recipe operationalizes; it does not originate.** Steering guidance may help realize or repair an approved coalition and composition state. It cannot supply missing source evidence, Primitive/archetype meaning, Final Script, Composition Intent, or wrong-reading policy.
9. **Transformation Contract is canonical terminology.** New Pipeline artifacts and interfaces use `TransformationContract`. Legacy labels may appear only in migration input or historical traceability fields and cannot name current schema/API objects.
10. **Creative degrees of freedom are explicit.** Absence does not mean unrestricted mutation. A field may change only when the contract declares a typed permitted degree of freedom and the requested change stays within it.
11. **Wrong-reading inheritance is monotonic.** Every generative, composited, restyled, or semantically transformative operation carries all applicable parent locks and exact parent-lock evidence. A derivative may add stricter locks; it cannot remove or weaken inherited locks. Relaxation requires a newly authorized upstream demand/version.
12. **`NOT_APPLICABLE` is evidence-bearing.** It requires a condition/policy ref, source requirement ref, and evidence. Required, unknown, unevaluated, or unsupported behavior cannot become N/A.
13. **No parsing-only compatibility.** An adapter is compatible only when it preserves and behaviorally enforces every authority, lineage, Skill, recipe, Transformation Contract, lock, lifecycle, and evidence constraint.
14. **Determinism is portable.** Identity excludes current time, randomness, dictionary insertion, traversal order, process environment, machine paths, storage location, model nondeterminism, and provider response ordering.
15. **State and receipt parity is atomic.** No Skill/recipe/Transformation binding becomes current without command, event, dependency edges, artifact, and success receipt in one transaction. No success receipt exists without its exact artifacts.
16. **Historical truth survives current invalidation.** Supersession creates new immutable versions and marks only typed current descendants stale. Historical executions replay exact accepted versions and receipts.

### Brownfield integration and disposition

| Artifact | Useful evidence | Limitation | Disposition |
|---|---|---|---|
| Builder `jit_capsule.py` | Exact Skill/package/context hashes; explicit applicability; sorted inputs; lock/lineage requirements; machine-path rejection. | Builder-owned synthetic capsule, only `development_validated`, production/certification false; it is not the Pipeline runtime contract. | `ADAPT_INTERFACE`; preserve pins, applicability, portability, and claim ceiling; do not import Builder code. |
| Builder `skill_registry.py` | Closed classifications, maturity/plasticity distinctions, provenance, necessity decisions, invalidation, canonical hashes, no dynamic discovery. | Registry is deliberately empty and scoped `ACTIVE_SYNTHETIC_PROOF_ONLY`; operations such as execution and recipe compilation are prohibited in that proof. | `REUSE_AS_DENIAL_AND_INTEGRITY_EVIDENCE`; never generalize fixture contents or status. |
| Builder `necessity.py` | Ordered alternatives and explicit no-Skill conclusion. | Current service contains synthetic assumptions and one historic activative compiler Skill identifier. | `ADAPT_DECISION_SHAPE`; require governed owner/context evidence and no implicit default. |
| TS-AHP-002 draft | Exact imported Harness graph, Skill requirement projection, execution binding, `NOT_APPLICABLE`, atomic repository, replay/invalidation. | Not independently audited or accepted. | `CONSUME_HASH_PINNED_DRAFT`; no local fork; reopen six sections on hash change. |
| TS-AIR-005 draft | Exact owner/kind Steering Recipe candidate, coalition/signature/Edge pins, applicability, evidence, rollback, and invalidation. | Not independently audited or accepted; AIR candidate contract uses a field name retained only as an exact imported interface. | `CONSUME_HASH_PINNED_DRAFT`; adapt through owner-specific read model without changing AIR bytes. |
| VAE F17 | Visual Steering Recipe evidence lifecycle, authority-first filtering, hybrid retrieval, Minimum Complete Context, contradiction coverage. | Product feature draft does not provide a shared released Pipeline schema and cannot authorize VAE Stage 5. | `PRESERVE_PRODUCT_BOUNDARY`; consume exact VAE-owned refs through product contract only. |

No Pipeline source tree currently exists under `05_ATOMIC_HARNESS_PIPELINE`; the paths in section 7 are proposed future paths, not files created by this writing task.

## 4. Staged implementation plan with exact paths and migration dispositions

Implementation is prohibited until ratification/adoption, independent audit and acceptance, a bounded Development Capsule, and separate build authorization. If later authorized, stages proceed in order:

| Stage | Proposed exact paths | Deliverable and exit evidence |
|---|---|---|
| 1 - domain contracts | `05_ATOMIC_HARNESS_PIPELINE/src/conscious_activations_pipeline/domain/skills/canonical_skill.py`; `harness_local_skill_adaptation.py`; `skill_composition_recipe.py`; `steering_recipe_binding.py`; `transformation_contract.py`; `applicability.py` | Closed immutable objects, enums, canonical serialization, exact refs, explicit N/A, lock-inheritance proof, and pure invariant tests. |
| 2 - registry and compatibility ports | `.../ports/canonical_skill_registry.py`; `.../ports/steering_recipe_registry.py`; `.../ports/skill_recipe_repository.py`; `.../domain/skills/compatibility.py` | Owner-scoped interfaces; exact version/hash resolution; feature negotiation; no repository-specific path dependency. |
| 3 - Harness reconciliation | `.../services/skill_requirement_resolver.py`; `.../services/skill_adaptation_binding_service.py`; `.../adapters/builder_skill_requirement_adapter.py` | Exact TS-AHP-002 projection consumption, node-kind/necessity parity, no mutation of imported Builder bytes. |
| 4 - composition and transformation compilation | `.../services/skill_composition_compiler.py`; `.../services/transformation_contract_compiler.py`; `.../services/wrong_reading_lock_inheritance.py` | Procedure DAG and operation constraints compile deterministically; semantic parity and monotonic lock inheritance pass. |
| 5 - Steering retrieval and binding | `.../services/steering_recipe_query_service.py`; `.../services/steering_recipe_binding_service.py`; `.../adapters/air_steering_recipe_adapter.py`; `.../adapters/vae_visual_steering_recipe_adapter.py` | Owner-specific hard filters, bounded ranking, Minimum Complete Context, exclusions, and binding receipts. |
| 6 - persistence and lifecycle | `.../repositories/skill_recipe_repository.py`; `.../services/skill_recipe_invalidation_projector.py`; `.../services/skill_recipe_replay_service.py` | Atomic commit/rollback, idempotency, optimistic concurrency, cancellation, supersession, selective invalidation, and historical replay proof. |
| 7 - schemas and fixtures | `05_ATOMIC_HARNESS_PIPELINE/contracts/schemas/ca.pipeline.canonical-skill-ref.schema.json`; `ca.pipeline.harness-local-skill-adaptation.schema.json`; `ca.pipeline.skill-composition-recipe.schema.json`; `ca.pipeline.steering-recipe-binding.schema.json`; `ca.pipeline.transformation-contract.schema.json`; `ca.pipeline.skill-recipe-receipt.schema.json`; `contracts/fixtures/ts_skl_001/` | Schema/model parity and deterministic positive/negative vectors; no shared release bytes. |
| 8 - integration and evidence | tests listed in section 10; `05_ATOMIC_HARNESS_PIPELINE/docs/validation/TS-SKL-001_IMPLEMENTATION_VALIDATION.md` | Twice-fresh regression, compile/type checks, portability, failure injection, replay, invalidation, security, and independent evaluation evidence. |

`...` expands only to `05_ATOMIC_HARNESS_PIPELINE/src/conscious_activations_pipeline`. It is not an absolute path and must not appear in runtime artifacts.

Migration dispositions:

- Builder synthetic registry/capsule artifacts remain immutable historical evidence. Pipeline may import their exact identities through an adapter profile but cannot relabel `ACTIVE_SYNTHETIC_PROOF_ONLY` as a current production registry.
- A legacy Skill-like prompt becomes a Canonical Skill only when an attributable owner supplies complete procedure, contracts, invariants, evidence, compatibility, lifecycle, version, and hash. Otherwise migration returns `AHP_SKL_MIGRATION_SKILL_MEANING_MISSING`.
- A legacy local customization becomes a Harness-local adaptation only if exact base bytes, allowed adaptation points, delta, owner, authority, and rollback are evidenced. No diff inference from current output is allowed.
- A legacy generic recipe must be classified by owner and kind. Ambiguous ownership, missing lifecycle, missing applicability, missing known failures, missing evidence, or missing rollback blocks migration.
- A legacy operation instruction may map into a Transformation Contract only when source artifacts, upstream authority, must-remain-true conditions, required changes, creative degrees of freedom, and all parent locks are exact. Missing semantic constraints cannot be reconstructed from the output artifact.
- Every successful migration creates a new immutable candidate artifact with `migrated_from` and a receipt; old bytes remain readable and hash-verifiable.

## 5. Schemas, APIs, state transitions, commands, events, and receipts

All contracts are immutable, `additionalProperties: false`, and versioned. Required strings are non-empty. IDs, versions, and SHA-256 pins form typed refs; unknown fields/enums/owners/kinds/major versions fail. Set-semantic arrays are unique and sorted by canonical ref. Ordered execution steps retain explicit `order_key`. Identity-bearing numbers use integers or fixed-point micros; binary floats, NaN, and Infinity are forbidden.

### Schema identities and value ownership

| Schema | Candidate version | Value owner |
|---|---|---|
| `ca.pipeline.canonical-skill-ref` | `1.0.0-candidate` | Pipeline reference; Skill bytes and meaning remain declared Skill-owner property |
| `ca.pipeline.harness-local-skill-adaptation` | `1.0.0-candidate` | Builder-generated Harness declares authority; Pipeline owns execution binding |
| `ca.pipeline.skill-composition-recipe` | `1.0.0-candidate` | Atomic Harness Pipeline |
| `ca.pipeline.steering-recipe-binding` | `1.0.0-candidate` | Pipeline binding; recipe remains AIR- or VAE-owned |
| `ca.pipeline.transformation-contract` | `1.0.0-candidate` | Pipeline operation contract bounded by upstream semantic authority |
| `ca.pipeline.skill-recipe-decision-receipt` | `1.0.0-candidate` | Atomic Harness Pipeline |
| `ca.pipeline.skill-recipe-invalidation-receipt` | `1.0.0-candidate` | Atomic Harness Pipeline |

### `CanonicalSkillRef`

Required fields: `skill_id`, `skill_version`, `skill_package_sha256`, `registry_snapshot_ref`, `skill_owner_product`, `procedure_contract_ref`, `input_contract_ref`, `output_contract_ref`, `invariant_refs`, `failure_policy_ref`, `tool_requirement_refs`, `side_effect_envelope_ref`, `evidence_refs`, `compatibility_profile_refs`, `lifecycle_state`, `validity_state`, `supersedes_ref_or_not_applicable`, and `canonical_ref_hash`.

An eligible Skill is exact, non-revoked, non-invalidated, lifecycle-eligible for the run claim, compatible with the node contracts and implementation binding, and owned by the declared registry authority. Package display name, mutable URL, tag, embedding, or filesystem location is not identity. `CanonicalSkillRef` never copies editable procedure content into the Harness or binding.

### `SkillApplicabilityDecision`

Required fields: `decision_id`, `skill_requirement_ref`, `workflow_node_ref`, `node_actor_kind`, `necessity_decision_ref`, `verdict`, `basis_code`, `condition_ref_or_not_applicable`, `condition_evidence_refs`, `resolved_skill_ref_or_not_applicable`, `authority_ref`, `input_hashes`, and `canonical_hash`.

`verdict` is `REQUIRED`, `CONDITIONAL_REQUIRED`, `OPTIONAL_EXCLUDED`, `PROHIBITED`, or `NOT_APPLICABLE`. A learned or agentic node must resolve `REQUIRED` or a satisfied `CONDITIONAL_REQUIRED` to an eligible Skill. `NOT_APPLICABLE` is valid only when the Builder requirement and necessity decision both explicitly permit it and evidence proves the governed condition; it cannot represent unknown, missing, unsupported, or unevaluated capability.

### `HarnessLocalSkillAdaptation`

Required fields: `adaptation_id`, `adaptation_version`, `base_skill_ref`, `harness_definition_ref`, `skill_requirement_ref`, `workflow_node_refs`, `adaptation_owner`, `authority_ref`, `allowed_adaptation_point_refs`, sorted `delta_operations`, `preserved_invariant_refs`, `input_output_contract_parity_digest`, `tool_and_side_effect_parity_digest`, `applicability_envelope`, `evidence_refs`, `evaluation_profile_ref`, `rollback_ref`, `lifecycle_state`, `supersedes_ref_or_not_applicable`, and `canonical_hash`.

Each `delta_operation` is a typed replacement at one exact declared adaptation point with old-value hash, new-value hash, rationale evidence, and effect class. Deltas cannot modify Skill identity, owner, procedure invariants, input/output contract types, authority, semantic refs, wrong-reading locks, failure/rollback obligations, or tool/side-effect envelope unless the Canonical Skill explicitly declares that point adaptable and the governing authority authorizes the exact new value. The resulting execution view always retains both base and adaptation refs.

### `SkillCompositionRecipe`

Required fields: `recipe_id`, `recipe_version`, `harness_definition_ref`, `phase_or_path_ref`, `owner_product`, `authority_ref`, sorted `skill_step_bindings`, sorted `module_bindings`, `reference_input_bindings`, `runtime_binding_refs`, `entry_contract_ref`, `terminal_contract_ref`, `handoff_bindings`, `primitive_coalition_refs`, `archetype_contract_refs`, `final_script_ref_or_not_applicable`, `composition_state_ref_or_not_applicable`, `transformation_contract_refs`, `evaluation_requirements`, `failure_and_stop_conditions`, `rollback_program_ref`, `applicability_envelope`, `dependency_refs`, `lifecycle_state`, `supersedes_ref_or_not_applicable`, and `canonical_hash`.

A `skill_step_binding` contains `step_id`, `order_key`, `workflow_node_ref`, `canonical_skill_ref`, `adaptation_ref_or_not_applicable`, `input_contract_ref`, `output_contract_ref`, `implementation_binding_ref`, `context_manifest_ref`, `tool_grant_refs`, `validation_ref`, `evaluation_ref_or_not_applicable`, and `failure_owner`. The step graph is acyclic, all contracts are bilateral, and no hidden actor or undeclared tool appears. Primitive/archetype/Final Script refs are immutable context pins; the recipe does not compile their meaning.

### `SteeringRecipeBinding`

Required fields: `binding_id`, `workflow_node_ref`, `harness_definition_ref`, `query_ref`, `recipe_kind`, `recipe_owner`, `recipe_contract_id`, `recipe_version`, `recipe_sha256`, `recipe_lifecycle_state`, `coalition_ref`, `coalition_signature_ref`, `edge_product_ref`, `archetype_coalition_refs`, `final_script_ref_or_not_applicable`, `composition_state_refs`, `category_profile_refs`, `embodiment_refs`, `failure_code_refs`, `applicability_decision_ref`, `compatibility_decision_ref`, `known_failure_refs`, `intervention_program_ref`, `preservation_condition_refs`, `evidence_refs`, `observed_run_refs`, `control_comparison_refs`, `rollback_program_ref`, `ranking_evidence_ref`, `authority_ref`, `dependency_refs`, and `canonical_hash`.

For an AIR recipe, the imported AIR-005 candidate field `preserved_property_refs` is consumed as an exact external interface and projected to `preservation_condition_refs`; the adapter must prove one-to-one lossless parity and may not change the AIR object. For VAE recipes, the binding uses the VAE contract released/adopted for that route. `recipe_kind` and `recipe_owner` must agree with the resolved registry; an owner mismatch is a hard failure.

### `TransformationContract`

Required fields: `contract_id`, `contract_version`, `operation_id`, `operation_kind`, `harness_definition_ref`, `workflow_node_ref`, `source_artifact_refs`, `source_artifact_hashes`, `target_artifact_family`, `semantic_authority_refs`, `composition_intent_ref_or_not_applicable`, sorted `must_remain_true_conditions`, sorted `required_changes`, sorted `permitted_creative_degrees_of_freedom`, sorted `wrong_reading_locks`, sorted `parent_lock_evidence`, `feature_contract_refs`, `t_v_route_refs`, `source_lineage_refs`, `validation_profile_refs`, `evaluation_profile_refs`, `repair_boundary_ref`, `rollback_plan_ref`, `authority_ref`, `dependency_refs`, `supersedes_ref_or_not_applicable`, and `canonical_hash`.

Each must-remain-true condition contains `condition_id`, `condition_kind`, `source_authority_ref`, `subject_pointer`, `required_relation`, `expected_value_hash_or_rule_ref`, `failure_code`, and `evidence_refs`. Each required change contains target pointer/region, typed change predicate, success evidence, and responsible owner. Each permitted degree of freedom names a closed field/region, operation set, bounds, and disallowed interactions; it cannot be an open note. Each wrong-reading lock carries exact lock ID/version/hash, owner, inherited-from ref, applicability, severity, and validation/evaluation evidence requirements.

`operation_kind` includes `DETERMINISTIC_DERIVATIVE`, `GENERATIVE`, `COMPOSITED`, `RESTYLED`, and `SEMANTICALLY_TRANSFORMATIVE`. The last four require non-empty wrong-reading locks and parent-lock evidence. A deterministic non-semantic derivative inherits every applicable parent lock even when it does not invoke a model. An operation may add stricter locks but any removal, weakening, scope narrowing, or severity reduction requires a new authorized upstream demand/version; Pipeline cannot authorize it locally.

### Commands and deterministic workflows

#### Workflow A - resolve and bind a Skill

1. `ResolveNodeSkillCommand` names exact imported Harness definition, graph projection, execution-binding manifest, Skill requirement, node, registry snapshot, authority/status snapshot, actor, command ID, idempotency key, and expected aggregate version.
2. Resolver proves node kind, necessity decision, applicability, and exact requirement hash. It rejects any learned/agentic node with absent or N/A Skill.
3. Registry resolves exact Skill ID/version/hash and owner; validator checks package, lifecycle, contracts, compatibility, tool/side-effect envelope, evidence, and invalidation state.
4. If the Harness declares an adaptation, the adaptation service resolves its exact immutable delta and proves base identity and parity constraints.
5. Repository atomically appends decision, binding, dependency edges, event, and receipt. No Skill is executed by this command.

#### Workflow B - compile a Skill Composition Recipe

1. `CompileSkillCompositionRecipeCommand` names phase/path, exact node/edge subset, resolved Skill/adaptation bindings, module/reference/runtime bindings, semantic context refs, transformation refs, authority snapshot, and expected stream version.
2. Compiler verifies every step belongs to the Harness, every contract handoff matches, all dependencies are exact/current, and all semantic refs are read-only.
3. It topologically sorts by explicit graph edges and `order_key`, never dictionary or filesystem order, and computes graph and semantic-parity digests.
4. Cycles, hidden actors, missing steps, duplicate requirements, undeclared tools, conflicting side effects, or semantic override fields reject the command.
5. Recipe, event, dependencies, and receipt commit atomically.

#### Workflow C - retrieve and bind Steering Recipes

1. `QueryEligibleSteeringRecipesCommand` names recipe kind/owner, exact coalition/signature/Edge Product, archetype/Final Script/composition state, category/profile, embodiment, current failure codes, validity time as caller-supplied evidence, registry snapshot, query budget, and authority snapshot.
2. Deterministic filters exclude wrong owner/kind, stale/invalid/revoked lifecycle, incompatible category/profile/embodiment/provider/tool, mismatched semantic refs, absent evidence/control comparison/rollback/known failure, and unresolved contradiction.
3. Only eligible candidates enter bounded lexical, graph, multimodal, or VLM reranking under a pinned evaluator/profile. Scores cannot restore an excluded candidate.
4. Minimum Complete Context contains only exact relevant contract fields, intervention steps, exceptions, superseding knowledge, material negative evidence, and rollback. It records included, excluded, compressed, unavailable, and conflicting refs.
5. `BindSteeringRecipeCommand` binds one selected exact recipe or records no eligible candidate. Selection cannot promote lifecycle or mutate the owning registry.
6. Query, exclusions, ranking, binding, dependencies, events, and receipts commit atomically.

#### Workflow D - compile and enforce a Transformation Contract

1. `CompileTransformationContractCommand` names exact source artifacts, requested operation, Harness/Workflow refs, upstream semantic authority refs, Composition Intent if applicable, feature/T-V/source lineage, parent contracts/locks, and expected stream version.
2. Compiler derives operation-specific conditions only by projecting explicit upstream declarations. It cannot infer missing meaning from pixels, prompts, model response, recipe, or prior accepted output.
3. Lock service computes the complete inherited lock set, compares scope/severity/rules, and rejects any missing or weaker descendant lock. Added locks are recorded separately.
4. Contract compiler proves required changes and creative degrees of freedom are disjoint from must-remain-true fields unless a typed compatible relation is declared.
5. Candidate execution, evaluation, and repair services must cite the same Transformation Contract hash. A result violating any hard condition or lock is ineligible regardless of aggregate score.
6. Contract, inheritance evidence, event, dependencies, and receipt commit atomically before any side effect.

#### Workflow E - replay, supersession, cancellation, and invalidation

- Repeating an idempotency key with identical canonical command bytes returns the original receipt and exact artifact refs; different bytes return `AHP_SKL_IDEMPOTENCY_CONFLICT`.
- Optimistic concurrency compares the aggregate stream version. A stale version returns current-head refs and performs no partial write.
- Cancellation before commit emits a cancellation receipt and no current artifact. Cancellation after commit records `CANCELLATION_TOO_LATE` without erasing the accepted history.
- Superseding a Skill, adaptation, composition recipe, Steering Recipe, semantic dependency, implementation binding, or Transformation Contract appends a new version and traverses typed dependency edges. Only current descendants whose eligibility/parity is affected become stale.
- Replay loads exact historical registry, Harness, Skill, recipe, semantic, compatibility, evaluator, and authority snapshots. It never substitutes latest versions or reruns historical human decisions.

### States and events

```text
Skill binding:       PROPOSED -> RESOLVED -> ELIGIBLE -> BOUND
                    \-> DENIED | INVALIDATED | SUPERSEDED | REVOKED
Composition recipe: PROPOSED -> VALIDATED -> COMPILED -> ELIGIBLE
                    \-> DENIED | INVALIDATED | SUPERSEDED
Steering query:      REQUESTED -> HARD_FILTERED -> RANKED -> BOUND | NO_ELIGIBLE_RECIPE
                    \-> DENIED | CANCELLED
Transformation:      PROPOSED -> INHERITANCE_VERIFIED -> VALIDATED -> ACTIVE_FOR_OPERATION
                    \-> DENIED | INVALIDATED | SUPERSEDED | REVOKED
```

Events are `NodeSkillResolved`, `NodeSkillResolutionDenied`, `HarnessSkillAdaptationBound`, `SkillCompositionRecipeCompiled`, `SteeringRecipeQueryFiltered`, `SteeringRecipeBound`, `NoEligibleSteeringRecipeRecorded`, `TransformationContractCompiled`, `TransformationContractDenied`, `SkillRecipeDependenciesInvalidated`, `SkillRecipeArtifactSuperseded`, and `SkillRecipeCommandCancelled`.

### Repository and service APIs

- Registry ports: `get_skill_exact(ref)`, `get_registry_snapshot_exact(ref)`, `query_recipe_candidates(owner, kind, hard_filters, snapshot_ref)`, `get_recipe_exact(ref)`.
- Repository transaction: `append(expected_stream_version, command_record, artifacts, decisions, events, dependency_edges, receipts) -> CommitResult`.
- Reads: `get_exact(ref)`, `get_receipt(ref)`, `get_command(command_id)`, `find_by_idempotency_key(key)`, `list_dependencies(ref)`, `list_descendants(ref, edge_types)`, `replay(stream_id, through_version)`.
- Service outcomes are tagged unions: `Committed{artifact_refs, receipt_ref, stream_version}`, `Replayed{original_receipt_ref}`, `Blocked{blocker_receipt_ref}`, `Cancelled{receipt_ref}`, or `NoEligibleCandidate{query_receipt_ref}`. Exceptions are not the public semantic result.

### Canonical serialization

Canonical JSON is UTF-8 without BOM, Unicode NFC, lexicographically sorted object keys, no insignificant whitespace, lowercase SHA-256, explicit enums, integer/fixed-point measures, and one terminal newline. Arrays preserve declared semantic order; set-like arrays sort by canonical ref. Identity excludes evidence-only timestamps. All identity-bearing IDs are caller-supplied or content-derived. Absolute/drive/UNC paths, secrets, process environment, hostnames, clocks, random UUIDs, traversal order, ZIP metadata, model sampling order, and mutable URLs are forbidden in canonical payloads.

## 6. Backward compatibility, fallback, rollback, invalidation, and historical replay

### Compatibility law

- Compatibility is semantic and feature-based. Exact required features include owner/kind separation, immutable base/adaptation identity, explicit N/A evidence, authority-first recipe filtering, complete Transformation Contract fields, lock-inheritance parity, receipt parity, replay, and selective invalidation.
- Parse success without behavioral enforcement is incompatible. An adapter that drops an exclusion, lifecycle state, owner, known failure, control comparison, rollback, semantic ref, creative bound, lock, or evidence ref fails compatibility.
- Owner-specific schemas are consumed externally by exact contract ID/version/hash; Pipeline does not create local AIR or VAE schema forks.
- Active executions remain pinned to the registry, Skill, recipe, semantic objects, compatibility profile, evaluator, and Transformation Contract negotiated at binding. Deprecation blocks new bindings when governed but does not corrupt accepted historical runs.
- Unknown enums, fields, lifecycle states, recipe kinds, owner products, adaptation operations, operation kinds, category/profile identifiers, or compatibility features fail closed.

### Fallback

Fallback is permitted only when the Harness or governing policy declares an exact ordered alternative and the alternative independently passes authority, contracts, evidence, compatibility, and claim ceiling.

- A missing required Skill does not fall back to an inline prompt or larger general model.
- An invalid adaptation may fall back to the exact base Skill only when the Harness explicitly permits base-only execution and the base satisfies the same contracts and acceptance criteria.
- No eligible Steering Recipe may yield `NoEligibleCandidate`; the node may execute without recipe only when its Harness policy allows that path. It cannot use a wrong-owner, stale, incompatible, or similarity-only candidate.
- A rejected Transformation Contract cannot fall back to unconstrained operation. Deterministic no-op, bounded alternate operation, or human escalation must be declared in advance.
- A provider/runtime fallback cannot change semantic owner, contract, category/profile, creative bounds, locks, or evaluation requirements.

### Rollback and recovery

Service rollback binds new commands to a last-known-good implementation/profile without rewriting artifacts produced under another version. An operation rollback follows the exact `rollback_plan_ref`; it may restore a prior current projection or produce a compensating artifact but cannot erase event/receipt history. External irreversible side effects require a prior human-owned authorization and a compensation plan; this spec does not grant that authority.

Recovery validates parity across command, artifact, event, dependency edge, decision, and receipt stores. Orphan artifacts, success receipts missing targets, partial transaction fragments, or mismatched hashes are quarantined and never projected eligible. Recovery never fabricates absent recipe evidence, source classification, owner, or lock inheritance.

### Selective invalidation

Dependency edges are typed: `USES_SKILL`, `ADAPTS_SKILL`, `COMPOSES_STEP`, `CONSUMES_SEMANTIC_OBJECT`, `BINDS_STEERING_RECIPE`, `GOVERNS_OPERATION`, `INHERITS_WRONG_READING_LOCK`, `USES_IMPLEMENTATION`, `USES_EVALUATOR_PROFILE`, and `USES_COMPATIBILITY_PROFILE`.

- Skill revocation invalidates current bindings, adaptations, composition recipes, capsules, and uncompleted operations that depend on that exact version, but not unrelated Skills or historical receipts.
- Base Skill supersession does not automatically validate an adaptation against the successor. A new compatibility decision and immutable adaptation/binding version are required.
- AIR coalition/Edge/archetype/Final Script or VAE recipe invalidation marks only dependent current recipe bindings and operations stale. Pipeline cannot repair the upstream meaning.
- Transformation Contract supersession invalidates uncompleted candidates/results under the old current operation when the new version is authoritative; accepted historical output stays reproducible under the exact old version.
- A parent-lock change invalidates descendants whose inherited set or proof no longer matches. Stronger child locks are retained; no traversal may silently weaken them.
- Evaluation-profile invalidation affects judgment eligibility and may require reevaluation; it does not rewrite producer artifacts.

### Historical replay

Historical replay verifies exact bytes, hashes, versions, command order, registry snapshot, authority snapshot, compatibility decisions, exclusion set, ranking evidence, transformation/lock proof, events, receipts, and recorded human decisions. It returns the historical claim state, not today's eligibility. Missing external executors may block physical re-execution but not hash/lineage verification; that limitation is explicit in the replay receipt.

## 7. Implementation tasks and path ownership

All paths are proposed and remain uncreated. Each task requires a later bounded capsule.

| Task | Owned paths | Required outcome | Forbidden expansion |
|---|---|---|---|
| SKL-T01 contracts | `.../domain/skills/canonical_skill.py`, `applicability.py`, `harness_local_skill_adaptation.py` | Closed reference, applicability, N/A, adaptation, canonical identity, and parity rules. | Editing Builder source or inventing Skill authority. |
| SKL-T02 composition | `.../domain/skills/skill_composition_recipe.py`, `.../services/skill_composition_compiler.py` | Exact acyclic procedure composition with typed handoffs and no semantic overrides. | AIR compilation or hidden actor execution. |
| SKL-T03 Steering | `.../domain/skills/steering_recipe_binding.py`, registry ports, AIR/VAE adapters, query/binding services | Owner/kind-preserving hard filters, bounded ranking, exclusions, context, and receipts. | Recipe promotion, VAE Stage 5 work, or shared schema release. |
| SKL-T04 transformation | `.../domain/skills/transformation_contract.py`, `.../services/transformation_contract_compiler.py`, `wrong_reading_lock_inheritance.py` | Complete operation boundary and monotonic lock inheritance. | Relaxing upstream authority or performing visual production. |
| SKL-T05 repository | repository, replay, invalidation, and transaction modules from section 4 | Atomic parity, idempotency, concurrency, cancellation, supersession, selective invalidation, replay. | Deleting history or using latest dependencies during replay. |
| SKL-T06 contracts/fixtures | `05_ATOMIC_HARNESS_PIPELINE/contracts/schemas/ca.pipeline.*`; `contracts/fixtures/ts_skl_001/` | Model/schema parity and deterministic valid/invalid examples. | Publishing shared release bytes or forking AIR/VAE schemas. |
| SKL-T07 tests/evidence | exact section 10 test paths and validation report | Positive, denial, adversarial, portability, replay, security, and claim-ceiling proof. | Self-acceptance or production/certification claim. |

`...` again expands only to `05_ATOMIC_HARNESS_PIPELINE/src/conscious_activations_pipeline`. Product ownership tests must assert that imports flow from domain to ports/services/adapters without domain depending on repository, provider, VAE, AIR implementation, Studio UI, or Builder code.

## 8. Behavior-specific acceptance criteria, failures, and recovery evidence

### Acceptance criteria

1. **FR-031 / ST-07.02 - exact Canonical Skill binding.** Given a learned or agentic node and valid Harness binding, resolution emits one exact owner/ID/version/package hash with matching input/output, invariants, tools, side effects, evidence, lifecycle, and compatibility. A display-name match, unpinned package, or learned node marked N/A fails. Evidence: registry fixture, resolution decision/receipt, contract test, replay vector.
2. **FR-032 / ST-07.02 - immutable local adaptation.** Given an authorized Harness-local delta at declared points, binding retains exact base and adaptation identities and proves contract/invariant/tool/side-effect parity. A delta that patches base bytes, changes an undeclared point, or broadens authority fails. Evidence: base-before/after hash proof, allowed-point test, rollback and invalidation receipt.
3. **FR-033 / ST-07.02 - durable Skill Composition Recipe.** Given a phase/path with exact Skills, modules, references, semantic contexts, and runtime bindings, compilation emits an acyclic immutable recipe whose handoffs match the Harness. A missing step, hidden actor, undeclared tool, semantic override, or insertion-order-dependent hash fails. Evidence: graph parity test, canonical vectors, atomic commit receipt.
4. **FR-034 / ST-07.02 - eligible Steering Recipes only.** Given a taste-bearing node, deterministic filters run before ranking and bind only a recipe whose owner, kind, lifecycle, evidence, coalition/archetype/composition state, category/profile, embodiment, failure, compatibility, known failures, and rollback match. A highly similar wrong-category or stale recipe appears only in exclusions. Evidence: hard-negative retrieval suite, exclusion receipt, Minimum Complete Context receipt, bounded ranking trace.
5. **FR-035 / ST-07.02 - complete Transformation Contract.** Given any editing or composition operation, the contract contains exact source/artifact/authority refs, must-remain-true conditions, required changes, permitted creative degrees of freedom, inherited locks/evidence, validation/evaluation, repair boundary, and rollback. Missing or open-ended fields block operation. Evidence: schema/model parity, transformation validation, negative fixtures.
6. **FR-036 / ST-07.02 - canonical terminology.** Current Pipeline class, schema, API, event, docs, and receipt names use `TransformationContract`. Disallowed legacy naming is accepted only as explicitly labeled migration input or historical alias and cannot appear as a current schema or API identity. Evidence: governed terminology scan with allowlisted historical locations.
7. **ST-07.02 - evidence and replay.** Successful, denied, cancelled, no-candidate, superseded, and invalidated commands reconstruct exact inputs, decisions, exclusions, state transition, downstream handoff, and receipts. Replay using latest Skill/recipe/profile instead of the recorded pin fails.
8. **ST-07.02 - selective recovery.** A defect localized to one Skill, recipe, semantic ref, evaluator, or Transformation Contract invalidates only typed descendants; unrelated accepted work and all historical receipts remain intact. A global invalidation or missing descendant is a failure.
9. **Authority boundary.** Pipeline cannot promote AIR/VAE recipes, create missing semantic meaning, mutate Builder bytes, direct VAE internal strategy, or let a producer issue independent acceptance. Attempts emit typed authority failures before side effects.
10. **Wrong-reading-lock inheritance.** Generative, composited, restyled, and semantically transformative operations contain every applicable parent lock and evidence; deterministic derivatives inherit applicable locks; stricter additions pass; removal/weakening without a new authorized upstream version fails.
11. **N/A law.** `NOT_APPLICABLE` carries exact source requirement, condition/policy, evidence, and owner. Required, unknown, missing, unevaluated, or unsupported Skill/evaluation/repair/lock behavior cannot become N/A.
12. **Atomicity and determinism.** Fault injection at every commit boundary leaves no visible state/receipt mismatch. Identical canonical inputs in fresh processes and different insertion/traversal/environment conditions produce identical bytes/hashes; changed semantic input produces changed identity.
13. **Portability and security.** Bundles/receipts contain no absolute paths, traversal, secrets, environment values, hostnames, nondeterministic IDs, or unbounded source/model payloads. Archive or external reference handling rejects unsafe identities before materialization.
14. **Claim ceiling.** Written specs, later implementation evidence, and runtime projections keep production eligibility and certification false until separately authorized. Skill or `EVALUATE` capability presence cannot confer evaluator or product certification.

### Typed failures

| Code | Condition | Required outcome / owner |
|---|---|---|
| `AHP_SKL_DRAFT_INTERFACE_HASH_MISMATCH` | TS-AHP-002 or TS-AIR-005 differs from its pin. | Stop dependent writing/implementation and reopen sections 3, 5, 6, 8, 9, 10; Program Control owns resolution. |
| `AHP_SKL_REQUIREMENT_UNRESOLVED` | Harness Skill requirement, node, or necessity decision is missing/stale/ambiguous. | Deny before registry query; Builder/Harness owner corrects declaration. |
| `AHP_SKL_REQUIRED_SKILL_NOT_BOUND` | Required learned/agentic node has no exact eligible Skill. | Block node; no inline-prompt fallback. |
| `AHP_SKL_NA_INVALID` | N/A lacks condition/evidence or hides required/unknown/unsupported behavior. | Reject decision. |
| `AHP_SKL_REGISTRY_IDENTITY_MISMATCH` | Registry, owner, version, hash, or release identity differs. | Reject and retain exact mismatch evidence. |
| `AHP_SKL_LIFECYCLE_INELIGIBLE` | Skill/recipe is proposed, stale, invalidated, deprecated-for-new-use, retired, or revoked against policy. | Exclude or deny; never promote locally. |
| `AHP_SKL_ADAPTATION_BASE_MISMATCH` | Adaptation base ref/hash differs from the bound Skill. | Reject adaptation and any dependent recipe. |
| `AHP_SKL_ADAPTATION_AUTHORITY_EXPANSION` | Delta changes undeclared point, invariant, contract, semantic authority, tool, side effect, lock, or failure law. | Reject; adaptation owner must issue governed successor. |
| `AHP_SKL_COMPOSITION_GRAPH_INVALID` | Cycle, duplicate/missing step, bad handoff, hidden actor, or undeclared tool exists. | Reject composition; no partial recipe. |
| `AHP_SKL_RECIPE_OWNER_KIND_MISMATCH` | AIR/VAE kind and owner do not agree with exact registry/contract. | Exclude and issue authority blocker. |
| `AHP_SKL_RECIPE_HARD_FILTER_FAILED` | Any authority, lifecycle, lineage, category/profile, embodiment, failure, evidence, comparison, or rollback filter fails. | Exclude before similarity; record reason. |
| `AHP_SKL_RECIPE_AUTHORITY_INVERSION` | Recipe originates or overrides semantic meaning or VAE/Pipeline ownership. | Reject binding and attribute repair to requesting layer. |
| `AHP_SKL_TRANSFORMATION_INCOMPLETE` | Operation lacks any required constraint, change, freedom, lineage, lock, validation, evaluation, repair, or rollback field. | Deny operation. |
| `AHP_SKL_WRONG_READING_LOCK_WEAKENED` | Child omits, weakens, narrows, or reduces inherited lock without authorized successor. | Deny before side effect; upstream demand owner must authorize new version. |
| `AHP_SKL_TRANSFORMATION_CONSTRAINT_CONFLICT` | Required change conflicts with must-remain-true condition or creative bound. | Emit constraint-conflict blocker with owning authorities; do not guess priority. |
| `AHP_SKL_IDEMPOTENCY_CONFLICT` | Same key has different canonical command bytes. | Return conflict; no write. |
| `AHP_SKL_CONCURRENT_MODIFICATION` | Expected stream version is stale. | Return current-head ref; no partial write. |
| `AHP_SKL_ATOMIC_COMMIT_FAILED` | Artifact/decision/event/edge/receipt transaction fails. | Roll back all transaction writes and quarantine fragments. |
| `AHP_SKL_STALE_DEPENDENCY` | Any exact current dependency is superseded/invalidated/revoked. | Block current consumption; preserve historical replay. |
| `AHP_SKL_ADAPTER_SEMANTIC_LOSS` | Adapter parses but drops or weakens governed information/behavior. | Reject compatibility and migration. |
| `AHP_SKL_MIGRATION_SKILL_MEANING_MISSING` | Legacy Skill-like source lacks exact procedure authority/evidence. | Preserve old bytes and emit migration blocker; do not invent. |
| `AHP_SKL_NONDETERMINISTIC_IDENTITY` | Same canonical input yields different bytes/hash. | Quarantine output and fail determinism evidence. |
| `AHP_SKL_PORTABILITY_VIOLATION` | Canonical payload contains host/path/environment/secret/nondeterministic state. | Reject before persistence/export. |

## 9. Dependencies, source authority, licenses, providers, models, workers, and external products

### Dependency register

| Dependency | Stage | Pin/status | Use and boundary |
|---|---|---|---|
| TS-AHP-002 | WRITE interface | SHA `3e76ee...d3dccd4`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Consume imported Harness graph and execution-binding assumptions; never represent as accepted authority. |
| TS-AIR-005 | WRITE interface | SHA `5dcf63...a43e49`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Consume exact AIR Steering candidate/semantic lineage assumptions; never promote or fork. |
| Constitution V1.1 | current authority | current Program Control pointer | Governs authority, Activative lineage, visual semantics, and product boundaries. |
| AHP F06 / ST-07.02 | candidate requirement/Story | `CANDIDATE_NOT_CURRENT` | Controls six requirements under Prompt 02C specification authorization only. |
| Builder package and graph | runtime external product | exact imported package/definition/binding hashes | Declares Skill requirements, adaptations, nodes, contracts, locks, and necessity; Pipeline is read-only consumer. |
| AIR registries/contracts | runtime external product | exact ID/version/hash and lifecycle | Own semantic objects and AIR Steering Recipes. Pipeline retrieves/executes only. |
| VAE recipe/production contract | runtime external product | adopted exact contract required | Owns Visual Steering Recipes and visual production; current Stage 5 remains unauthorized. |
| Independent evaluator | judgment dependency | exact evaluator/profile/version/hash | Issues separate judgment receipts; producer self-approval prohibited. |
| Delegation Protocol | transport dependency when cross-product | exact current compatible release negotiated separately | Carries immutable messages and receipts; cannot interpret semantics. |

Acceptance prerequisites and build prerequisites are empty in the recovery packet for initial writing. That does not remove later ratification, independent audit/revision/re-audit, product adoption where applicable, Development Capsule, build authorization, or release evidence gates.

### Source authority and provenance

Every Skill, adaptation, recipe, transformation, and receipt preserves source and authority refs. Operator-supplied source authority, provenance, lineage, route scope, and attributable approvals remain explicit. This spec creates no generic creative-safety or content-rights approval authority. Technical security covers operational controls only and cannot replace semantic/source authority.

No unavailable source is used for a factual claim. Both assigned sources are byte-available and hash-locked. Historical assignment headings do not override the current source disposition ledger.

### Licenses and external content

Registry metadata must record package license/provenance, redistribution constraints, model/tool terms where applicable, and whether execution requires external bytes. Unknown or incompatible license status blocks packaging/use under the declared route; Pipeline does not infer rights from local file presence. Logs and receipts reference protected source/model assets by hashes and governed refs rather than embedding full content.

### Providers, models, tools, and workers

- A Canonical Skill may declare tools and side-effect envelopes; an implementation binding grants only the intersection with node-local Harness authority.
- A model or Agent Program is an embodiment of a Skill step, not the Skill owner or semantic authority. Its claim manifest, model/checkpoint/runtime hash, applicability, tool grants, budget, fallback, and evaluator profile must be exact.
- Steering retrieval may use embeddings or VLM reranking only after hard filters. Model scores are evidence, not authority or lifecycle promotion.
- Worker leases, retries, heartbeats, resource caps, and cancellation belong to runtime/operations specs. This subsystem records exact worker/runtime binding refs and refuses hidden side effects.
- VAE provider/model/LoRA/conditioning choices remain inside VAE. A Pipeline recipe binding can state required compatibility and expected contract, not select VAE internals.
- Secrets remain in approved runtime secret stores. They are never canonical payload fields, logs, receipts, test fixtures, or exported evidence.

## 10. Testing, evaluation, observability, security, performance, recovery, evidence, and release

### Required future test suites

| Proposed path | Coverage |
|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/tests/unit/domain/skills/test_canonical_skill_ref.py` | Exact identity, owner, lifecycle, contracts, unknown-field rejection, deterministic hash. |
| `.../test_skill_applicability.py` | Learned/agentic requirement, conditional evidence, optional exclusion, prohibited, and invalid N/A cases. |
| `.../test_harness_local_skill_adaptation.py` | Base immutability, allowed deltas, parity, authority/tool/side-effect/lock expansion denial, rollback. |
| `.../test_skill_composition_recipe.py` | DAG, handoffs, step order, hidden actors, missing/duplicate steps, semantic override denial. |
| `.../test_steering_recipe_binding.py` | Owner/kind separation, exact AIR/VAE refs, lifecycle, evidence, known failures, comparisons, rollback. |
| `.../test_transformation_contract.py` | Complete constraints/changes/freedoms, operation kinds, conflict detection, canonical terminology. |
| `.../test_wrong_reading_lock_inheritance.py` | Parent completeness, stricter addition, weakening/removal/scope narrowing/severity reduction denial. |
| `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_skill_binding_from_atomic_harness.py` | TS-AHP-002 graph and binding parity, no Builder mutation, node/necessity rules. |
| `.../test_skill_composition_and_jit_context.py` | Exact Skill/adaptation composition, Minimum Complete Context, context exclusions, downstream contracts. |
| `.../test_authority_first_steering_retrieval.py` | Hard negatives, contradiction coverage, eligible-only ranking, no-candidate behavior, receipts. |
| `.../test_air_vae_steering_recipe_authority.py` | AIR/VAE owner separation, no schema fork, no promotion, no semantic reconstruction. |
| `.../test_transformation_contract_execution_gate.py` | All operation classes, semantic parity, lock inheritance, feature/T-V/source lineage, pre-side-effect denial. |
| `.../test_skill_recipe_atomicity_replay_invalidation.py` | Commit fault injection, idempotency, concurrency, cancellation, replay, selective descendants, historical reproduction. |
| `05_ATOMIC_HARNESS_PIPELINE/tests/migration/test_legacy_skill_recipe_migration.py` | Evidence-backed immutable migration or typed block; no invented owner, classification, lifecycle, meaning, or locks. |
| `05_ATOMIC_HARNESS_PIPELINE/tests/architecture/test_skill_recipe_import_boundaries.py` | Domain purity and prohibition on Builder/AIR/VAE implementation imports. |
| `05_ATOMIC_HARNESS_PIPELINE/tests/security/test_skill_recipe_portability_and_secret_scan.py` | Absolute/UNC/traversal/environment/secret rejection and bounded payloads. |

`...` in test rows expands only to `05_ATOMIC_HARNESS_PIPELINE/tests/unit/domain/skills` or `05_ATOMIC_HARNESS_PIPELINE/tests/integration` according to the row prefix.

### Evaluation

Deterministic gates precede judgment. Skill identity, contracts, graph, owner, lifecycle, compatibility, N/A, lock inheritance, and hard exclusions are mechanically decidable. Independent evaluation is required for taste-bearing recipe selection, transformation fidelity, semantic preservation, composition, wrong-reading, and feature-contract dimensions when the Harness declares them. Findings remain separate; a fatal lock/authority/semantic failure cannot be compensated by an aggregate aesthetic score. `NOT_APPLICABLE` needs a condition and evidence.

The producer, retrieval ranker, and transformation executor cannot issue their own independent acceptance receipt. Evaluator capability presence or a declared `EVALUATE` feature does not imply evaluator certification. Current evaluator and production certification remain false unless separately evidenced and authorized.

### Observability

Structured telemetry records command/trace IDs, exact input refs/hashes, registry/authority/compatibility snapshots, node/Skill/adaptation/recipe/transformation refs, hard-filter inclusion/exclusion counts and codes, ranking profile/hash, context budget, lock inheritance counts, idempotent replay, stream version, commit outcome, invalidated descendant counts, responsible failure owner, and next admissible action. Metrics may aggregate latency, filter selectivity, no-candidate rate, adaptation rejection, lock failures, replay parity, and commit failures; metrics are not canonical evidence.

Logs redact source payloads, prompts, model content, identities where protected, credentials, and operator secrets. They exclude absolute paths and unbounded exception/model text. Every denial exposes a stable code and safe context sufficient to identify the owner and recovery action.

### Performance and budgets

- Exact registry resolution and hard filtering are bounded by the pinned snapshot and indexed typed facets; no unbounded corpus scan is permitted.
- Query commands declare maximum candidate count, bytes, tokens, model calls, latency, and cost. Budget exhaustion yields a receipt and no hidden continuation.
- Canonical hashing and graph validation scale with admitted payload/edges and enforce size/count limits before allocation.
- Minimum Complete Context has explicit field/section/token budgets and records exclusions/compression; the whole corpus is never a default fallback.
- Performance optimization cannot skip authority, lifecycle, compatibility, contradiction, lock, lineage, evaluation, or receipt gates.

### Security

Validate all package/member/reference identities before materialization; reject traversal, symlink/device ambiguity, case collisions, absolute/UNC paths, NULs, excess sizes, decompression abuse, and unmanifested bytes. Tool grants are typed, least privilege, node-local, and time/budget bounded. Network/provider access is denied until a separately authorized execution command. Canonical records and receipts are tamper-evident. Dependency/license/vulnerability scans are operational evidence and do not create creative or source authority.

### Recovery and adversarial matrix

Evidence must cover: missing learned-node Skill; unjustified N/A; empty synthetic registry misread as global truth; stale/unknown registry; owner/hash collision; missing Skill package; adaptation base drift; undeclared delta; contract/tool/side-effect expansion; recipe cycle; hidden actor; bad handoff; insertion-order drift; wrong-owner AIR/VAE recipe; invalid lifecycle; semantic-similarity-only candidate; missing known failure/control/rollback; coalition/archetype/composition mismatch; no eligible recipe; whole-corpus context; recipe authority inversion; incomplete Transformation Contract; open-ended creative freedom; missing/weak parent lock; constraint conflict; stale source/sequence/composition/result; evaluator self-approval; invalid N/A finding; partial commit at every boundary; orphan artifact/receipt; idempotency conflict; concurrent update; cancellation race; invalidation underreach/overreach; lossy migration; latest-version replay substitution; absolute path/environment/random/time leakage; secret exposure; unavailable provider; and false production/certification projection.

### Completion evidence and release posture

Future implementation evidence must include schema/model/type parity, canonical vectors, registry and owner hash matrix, exact source disposition, Skill necessity and binding receipts, adaptation/base parity, recipe eligibility/exclusion and Minimum Complete Context receipts, Transformation Contract/lock-inheritance evidence, authority-boundary tests, atomicity fault injection, replay/invalidation report, migration/compatibility report, security/portability scan, full test suite twice in fresh processes, source compilation/type checks, clean-context reproduction, and independent audit by an agent other than the writer.

This writing execution creates no code, schema, fixture, test, contract release, audit, revision, acceptance, build artifact, or Development Capsule. Final state is `WRITTEN_PENDING_AUDIT`; authority is `CANDIDATE_NOT_CURRENT`; specification work is authorized; build authority is false; later pre-ratification acceptance ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
