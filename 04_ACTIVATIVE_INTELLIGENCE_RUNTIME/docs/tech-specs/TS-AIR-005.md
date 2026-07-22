---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-005
title: Primitive Coalition Contract, Coalition Signature, Edge Product, and Steering Recipes
product: Activative Intelligence Runtime
version: 2.1.0-candidate
date: 2026-07-22
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 2
output_path_class: DIRECT_PRODUCT_SPEC_PATH
controlling_frs:
  - AIR-FR-025
  - AIR-FR-026
  - AIR-FR-027
  - AIR-FR-028
  - AIR-FR-029
  - AIR-FR-030
  - FR-164
  - FR-171
  - FR-172
  - FR-173
  - FR-174
controlling_stories:
  - AIR-ST-05.01
  - AIR-ST-05.02
  - AIR-ST-05.03
  - ST-12.01
  - ST-12.06
  - ST-12.07
  - ST-12.08
draft_dependencies:
  - spec_id: TS-AIR-002
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: 258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
  - spec_id: TS-AIR-004
    quality_state: WRITTEN_PENDING_AUDIT
    sha256: c30b656d288f4e781564f2cdf9a39acab79c14e6cdace02d88df14869f9edf58
    label: DRAFT_DEPENDENCY_NOT_ACCEPTED
---

# TS-AIR-005 — Primitive Coalition Contract, Coalition Signature, Edge Product, and Steering Recipes

This specification is authorized for writing under the Prompt 02C recovery chain. It is not current authority, build authority, production authority, or a Development Capsule. Its two upstream interfaces are exact hash-pinned drafts. Both are `DRAFT_DEPENDENCY_NOT_ACCEPTED`; neither is represented as ratified or accepted.

## 1. Files and authorities read

| Class | Exact file | State / SHA-256 | Use |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten sections, evidence and lifecycle ceiling. |
| Frozen packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery authorized; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Exact FRs, Stories, output path, dependencies and path authority. |
| Dispatch lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_02_DISPATCH_LOCK.yaml` | dispatched; `3bfa468af8f2be9e89160c4ec3beebe47e87c90397efe18d309c6095d4c78585` | Admits only AIR-002 and AIR-004 as upstream draft interfaces. |
| Authority stage | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending; `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Candidate remains non-current; no build or capsule. |
| Write authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | specification work only; `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes writing and later technical review only. |
| Candidate ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | pending ratification; `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | AIR owns Primitive coalition, signature and Edge Product meaning. |
| Candidate authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | pending ratification; `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | Pipeline executes without semantic reinterpretation; VAE realizes demands. |
| Upstream interface draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-002.md` | `WRITTEN_PENDING_AUDIT`; `258c711d84dbbf2e8abc79e910d825cb8370dd0b7e0940e81d91d8a93e1b43e5`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Context Premise, Matrix of Edging, Broad Signal, tension-site, candidate-survival and Edge Product handoff assumptions. |
| Upstream interface draft | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-004.md` | `WRITTEN_PENDING_AUDIT`; `c30b656d288f4e781564f2cdf9a39acab79c14e6cdace02d88df14869f9edf58`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Exact Primitive registry, version, query, binding, relations, risks and coverage assumptions. |
| Primary draft | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-005-primitive-coalition-signature-edge-product-and-steering-recipes.md` | full candidate draft; `fcda639eb120be4ed53d7f6c5f86cb803ae5cb13a031dd3092de608b995676ed` | Existing implementation-grade baseline amended to current ownership, deterministic and dependency law. |
| Controlling feature | `.../prd/features/F05-primitive-coalition-signature-edge-product-and-steering-recipes.md` | candidate; `bc70dca360bab177370d815fbf574299191bfe96c2125b772b9107959ffe3fbf` | AIR-FR-025–030 and F05 terminal contract. |
| AIR Stories | `.../planning/EPICS_AND_VERTICAL_STORIES.md` | candidate; `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-05.01–05.03 including CBAR, replay and selective invalidation. |
| AHP Stories | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/EPICS_AND_VERTICAL_STORIES.md` | candidate; `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | ST-12.01, ST-12.06–12.08 and FR-164, FR-171–174. |
| Required evidence | `.../sources/doctrine/F29-primitive-first-coalition-composition-and-evaluation.md` | SRC-AHP-F29-001; `80be79e53616e28b0e86604f9e6f6d94ffd02308aa0618766ea912c62c9e03bc` | Primitive-first composition, coalition and independent evaluation boundaries. |
| Required evidence | `.../sources/doctrine/MATRIX_OF_EDGING.md` | SRC-MOE-001; `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | Broad-first, survival, coalition, routeability, fatality and anti-centroid laws. |
| Required evidence | `.../sources/doctrine/MEANING_PRIMITIVE_REGISTRY_SPEC.md` | SRC-PRIM-001; `1851f4e8e07beb6e1886e91f45d8bb12cf38d6fc8af8f20e314788d6d47d7e5f` | Meaning Primitive plane. |
| Required evidence | `.../sources/doctrine/EXPERIENCE_PRIMITIVE_REGISTRY_SPEC.md` | SRC-PRIM-002; `5cb5f1b568c84e41bbbf2ccbb18b938ccee5de1c6cab5cbee96343d88adaee72` | Experience Primitive plane. |
| Brownfield contract | `.../sources/doctrine/PRIMITIVE_COALITION_CONTRACT.py` | SRC-DOCT-009; `990735d588e03004cbee780cea7e3623361a7fa70991e898ff13f173618cbf08` | Useful role/conflict shape; random IDs, floats, defaults and open fields require adaptation. |
| Required evidence | `.../sources/doctrine/CCV_COMBINATORIAL_CONTROLLED_VARIATION.md` | SRC-DOCT-005; `0869ff50e4bdaba3dc1854183100826d0de9568b9ed5558bf68b4590834a62c4` | Axis-labelled variation, weighted geometry, fatality and routeability. |
| Product boundary evidence | `02_VISUAL_ASSET_EDITOR/prd/05-features/F17-steering-intelligence-cmf-okf-retrieval.md` | SRC-CUR-020; `9acefd1eaa224cd9de3dd5d39fec7443dfd6edcbac32a1dfe97355e1b8230aa7` | VAE owns production-derived Visual Steering Recipes; it does not own AIR coalition meaning. |
| Deferred reference | SRC-EXT-027 | `DEFERRED_REFERENCE`; exact bytes unavailable | No factual claim in this spec depends on it; non-blocking by current source disposition. |
| Candidate implementation | `.../reference_implementation/activative_intelligence_v2/primitive_archetype_models.py` | `5c2eaf15168e0843938637ac23e25155ff6ae702a56217df4644a1c277e208b9` | Strict/frozen model seed requiring field and ownership correction. |
| Candidate tests | `.../tests/test_v21_primitive_archetype_invariants.py` | `8d3a8ccbd3dd964d8d678596283beafd3495cf9593974a3fa27408654a44abb6` | Failed Primitive gates cannot pass and full semantic lineage is required. |

The `...` prefix in AIR bundle rows expands to `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE`. The active CBAR Primitive files are PRM-PRS-002 SHA `4fba8edcb439c296a610b53a45ce76b9a002b4a128338e3302ddbb1cc49e242e`, PRM-PRS-009 SHA `91acef681584ee72d14be51159ac5ed6d0683168dc71a95369b56d9956268caa`, and PRM-PRS-015 SHA `b05b6aabef1d48f0a3bf07f5b4a43febe2fb53445df5e1a8524a6ba0f78f48d5`.

AIR-002 and AIR-004 control interface assumptions in sections 3, 5, 6, 8, 9 and 10. A byte change to either pin reopens all six sections for downstream revision-impact review before this document may advance.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

A list of individually relevant Primitives is not a creative recipe. Without an explicit coalition contract, individually useful moves can cancel one another, overload the audience, flatten productive tension, or produce an unroutable Edge Product. A high-scoring single Primitive can also conceal missing roles, misuse, redundancy or coalition fatality. The operator needs a reproducible AIR-owned semantic object that explains which bindings are primary, supportive, suppressive or conflicting; measures the surviving geometry; names the emergent pressure/role/tension/consequence; and preserves exact evidence for downstream denial, repair and replay.

### Bounded solution

AIR compiles exact AIR-004 Primitive Bindings and AIR-002 Matrix/Broad Signal refs into an immutable `PrimitiveCoalitionContract`. Deterministic gates establish role coverage, compatibility, conflict, overload, suppression and misuse legality before any ranking or model judgment. The compiler derives a versioned `CoalitionSignature`, then an `EdgeProduct` distinct from the pre-coalition Broad Signal. An independent evaluator issues a `PrimitiveEvaluationReceipt`. Only evidence-backed, coalition-specific `SteeringRecipeCandidate` objects may be proposed; they never originate Primitive or coalition meaning and remain candidates until a separately governed promotion path acts.

### In scope

- exact coalition roles, exclusions, relations, thresholds-by-profile and dependency lineage;
- stable weighted coalition geometry, synergy, redundancy, routeability and fatality evidence;
- Edge Product compilation after candidate survival;
- deterministic and independent evaluation with valid `NOT_APPLICABLE` semantics;
- candidate Steering Recipe retrieval/creation bounded by coalition, archetype, composition state and known failure;
- immutable commands, atomic repository commits, replay, supersession and descendant invalidation;
- typed handoff for downstream AIR, Pipeline, evaluation and Studio projections.

### Out of scope and non-goals

- redefining Primitive registry entries, Matrix meaning, Identity DNA, source evidence, archetype or Final Script authority;
- allowing Pipeline, VAE, Studio, Delegation, a renderer or a model to reconstruct or mutate AIR-owned meaning;
- executing a composition, visual production workflow, model, LoRA, render, repair or delivery;
- promoting a VAE production recipe into AIR semantic authority;
- creating a shared contract release, source code, schema bytes, Development Capsule, build approval, production claim or certification;
- activating Format 02 or VAE Stage 5.

## 3. Governing decisions and constraints

1. **AIR owns coalition semantics.** Under the candidate ownership matrix, AIR owns `PrimitiveCoalitionContract`, `CoalitionSignature`, `EdgeProduct` and their semantic lifecycle. Pipeline may retrieve, validate, execute, evaluate and invalidate exact versions; it may not rebuild their meaning. VAE owns visual production planning and production-derived visual recipe evidence, not AIR coalition semantics.
2. **Draft inputs remain drafts.** AIR-002 and AIR-004 are hash-pinned writing interfaces labelled `DRAFT_DEPENDENCY_NOT_ACCEPTED`. This specification cannot elevate them, claim adoption, or proceed past the pre-ratification ceiling.
3. **Broad Signal is not Edge Product.** AIR-002's Broad Signal represents a pre-coalition pressure field. `EdgeProduct` is emitted only after exact Primitive candidates survive, receive functional roles and form a valid coalition geometry.
4. **Bindings precede coalitions.** Every coalition member resolves to one exact AIR-004 `PrimitiveBinding` and underlying Primitive ID/version/hash. Labels, embeddings, summaries or recipe matches cannot substitute for exact resolution.
5. **Roles are explicit and total.** Every admitted binding has exactly one coalition role: `PRIMARY`, `SUPPORT`, or `SUPPRESSION`. Conflicting candidates are represented in explicit conflict decisions and are not silently admitted. Every exclusion has a typed reason.
6. **Fatal conflicts are not averaged.** Fatal conflict, unresolved suppression, role collapse, overload, missing required coverage or misuse beyond the pinned profile is a hard blocker. A favorable aggregate score cannot compensate.
7. **No invented thresholds.** Coverage, misuse, fatality and routeability requirements are exact immutable references to a governed evaluator profile accepted with the command. The service has no hidden default. Missing or unknown profiles block compilation.
8. **Coalition Signature is stable geometry.** It preserves ordered roles plus canonically sorted set-like relations and integer-micro weights. It measures family/candidate geometry, synergy, redundancy, routeability and surviving interaction without collapsing to a list or centroid.
9. **Edge Product remains inspectable.** It states distinctive pressure, viewer role, live tension, usable creative consequence, transfer invariants, counteractivation risks and exact provenance. It is not a slogan or visual treatment.
10. **Steering Recipes operationalize; they do not originate.** A recipe candidate must be specific to the exact coalition and applicability envelope, cite evidence and known failures, name preserved properties and rollback, and remain subordinate to Primitive, Matrix, Voice/Visual DNA, Final Script and composition authority.
11. **Producer and evaluator are independent.** The authority context that compiles a coalition may run deterministic pre-gates but cannot issue the independent evaluation verdict that makes the result eligible.
12. **Evaluation dimensions remain separate.** Primitive presence, local function, interaction, misuse, coalition integrity, Edge Product fidelity, routeability and failure attribution are individual findings. No aesthetic average can hide a fatal dimension.
13. **`NOT_APPLICABLE` is conditional, not missing.** It is legal only when the pinned evaluator profile declares the dimension conditional, the receipt identifies the condition, and evidence proves it. Required, unknown, unevaluated and unsupported dimensions cannot become N/A.
14. **Historical truth is immutable.** Supersession adds a successor; invalidation marks only typed descendants stale. It never overwrites accepted artifacts, evaluation evidence or operator resolution history.
15. **Canonical identity is portable.** Hashes exclude absolute paths, process environment, current time, randomness, traversal order and storage location. All identity-bearing values are caller-supplied or content-derived.
16. **Activative Contract Compiler is not AIR.** This service produces AIR semantic programs; it does not become the Pipeline compiler or execute a harness.

## 4. Current brownfield architecture

| Artifact | Useful evidence | Defect / risk | Disposition |
|---|---|---|---|
| `PRIMITIVE_COALITION_CONTRACT.py` | Roles, conflicts, evaluation targets, coverage result and legacy triad concept. | UUID4 identity, float hashing, implicit `0.86`/`0.18` defaults, mutable lists/maps, coarse string signature, permissive provenance. | `ADAPT`; never use as current schema or authority. |
| `primitive_archetype_models.py` | Strict/frozen bindings, risks, coalition and evaluation shapes. | TS-AIR-004 and TS-AIR-005 objects are colocated; open dictionaries and prospective authority assumptions remain. | `ADAPT_AND_SPLIT` at the future paths below. |
| AIR-002 draft | Broad-first Matrix, tension-site, survival and Edge Product interface. | Not audited or accepted; its coalition/Edge shapes are an upstream draft interface. | `CONSUME_HASH_PINNED_DRAFT`; reopen six sections on change. |
| AIR-004 draft | Exact Primitive version, query, binding, relation, risk and coverage interface. | Not audited or accepted. | `CONSUME_HASH_PINNED_DRAFT`; no copied local fork. |
| F29 / Matrix / CCV doctrine | Coalition laws, anti-centroid rule, fatality and routeability. | Narrative doctrine does not itself define deterministic runtime bytes. | `ACTIVATE_AS_GOVERNING_EVIDENCE`; implement only through closed typed contracts. |
| VAE F17 | Production-derived Visual Steering Recipe lifecycle and retrieval filters. | Same generic name can obscure distinct product ownership. | `PRESERVE_BOUNDARY`; use typed recipe kind/owner and never merge semantic and visual-production recipes. |
| Candidate invariant tests | Failing Primitive gates cannot receive pass; semantic lineage is mandatory. | Does not cover canonicalization, repository atomicity, concurrency, replay or all active Primitive CBAR cases. | `REUSE_AS_REGRESSION_SEED` and extend per section 10. |

The prior `simple_triad_to_coalition` adapter cannot invent coalition roles, thresholds, source classification, signature geometry or Edge Product meaning. A migration either supplies those values from attributable historical evidence and emits new immutable V2.1 artifacts, or returns a typed migration blocker while preserving the old bytes.

## 5. Proposed architecture and workflows

### Components

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `CoalitionInputResolver` | Resolve exact AIR-002 Matrix/Broad Signal and AIR-004 binding refs, snapshots, source and evaluator profile. | Guess missing Primitive, source kind, role or threshold. |
| `CoalitionRoleCompiler` | Validate one primary, explicit support/suppression roles, exclusions, relation decisions and required coverage. | Rank away fatal conflicts or alter bindings. |
| `CoalitionGeometryCompiler` | Produce stable weighted `CoalitionSignature`, synergy, redundancy, routeability and fatality projections. | Smooth productive contradictions into a centroid. |
| `EdgeProductCompiler` | Derive the post-coalition pressure/role/tension/consequence with transfer invariants. | Copy a topic label, slogan or visual recipe into the Edge Product. |
| `SteeringRecipeCandidateService` | Retrieve or propose coalition-specific candidates after semantic compilation; preserve contradictions and provenance. | Originate coalition, Primitive, archetype, Voice/Visual DNA or Final Script meaning. |
| `PrimitiveCoalitionEvaluator` | Independently evaluate exact candidate bytes under a pinned profile. | Compile or mutate the evaluated candidate. |
| `PrimitiveCoalitionRepository` | Atomic immutable artifact/command/event/edge/receipt persistence and replay. | Overwrite history or store state without receipt parity. |

### Workflow A — compile coalition and signature

1. Accept `CompilePrimitiveCoalitionCommand` with caller-supplied `command_id`, `idempotency_key`, `expected_stream_version`, actor/authority refs, exact AIR-002 Matrix/Broad Signal refs, AIR-004 binding refs, evaluator profile ref, registry snapshot ref and requested coalition ID/version.
2. Resolve every ref by ID/version/SHA-256. Reject stale, superseded, unknown, duplicate or invalidated inputs; never silently switch to a current version.
3. Validate that each binding is eligible for the requested target/stage and source context. Preserve every included and excluded candidate decision.
4. Classify admitted bindings as primary, support or suppression; emit explicit relation/conflict decisions for all material pairs. Reject no-primary, multiple-unresolved-primary, fatal conflict, overload, role collapse, missing required coverage or unproved suppression.
5. Derive the signature from canonical binding refs, role assignments, fixed-point weights, interaction decisions, family/candidate geometry, redundancy, synergy and routeability findings. The fingerprint is a content hash, not a prose label.
6. Atomically append command record, coalition contract, signature, dependency edges, event and compile receipt under optimistic concurrency. A fault before commit leaves none of them visible.

### Workflow B — compile the Edge Product

1. Load the exact stored coalition/signature and its AIR-002 Broad Signal/Matrix lineage.
2. Prove candidate survival and non-compensable gates from the pinned profile; do not reuse a passing score from another coalition or context.
3. Derive distinct pressure, viewer role, live tension, usable creative consequence, must-survive transfer invariants and counteractivation risks.
4. Reject a topic-only, slogan-only, generic-aesthetic, unroutable or centroid-smoothed output.
5. Atomically append the Edge Product, dependency edges, event and receipt; the coalition artifact remains unchanged.

### Workflow C — independent evaluation and recipe candidacy

1. A separately identified evaluator loads exact coalition, signature, Edge Product, binding, source, registry and profile bytes.
2. Deterministic gates run first. Independent judgment records separate findings for presence, function, interaction, misuse, coalition integrity, Edge fidelity, routeability and attribution.
3. Every finding is `PASS`, `FAIL`, or governed `NOT_APPLICABLE`; a fatal `FAIL` makes overall eligibility fail regardless of aggregate evidence.
4. A recipe query filters first by owner, lifecycle, exact coalition/archetype/composition refs, category, stage, failure code, profile compatibility and validity, then performs bounded retrieval/reranking. Similarity alone is ineligible.
5. Each result remains a `SteeringRecipeCandidate` until separately promoted. VAE visual-production recipes enter only as typed external evidence and never replace AIR semantic recipes.
6. Evaluation and candidate receipts append atomically without mutating coalition meaning.

### Workflow D — idempotency, concurrency, cancellation and replay

- Repeating the same idempotency key and canonical command hash returns the original receipt and artifact hashes. Reusing the key with different bytes emits `AIR_COAL_IDEMPOTENCY_CONFLICT`.
- `expected_stream_version` mismatch emits `AIR_COAL_CONCURRENT_MODIFICATION`; no partial record is visible.
- Cancellation before commit records a terminal cancellation receipt only. Cancellation after the commit boundary cannot erase output and is reported as already committed.
- Replay loads exact historical versions and events, recomputes canonical hashes, and may project old schema versions through a pinned adapter without rewriting their bytes.
- Supersession appends a successor plus dependency-analysis receipt. Only descendants reachable through typed semantic edges become stale; unrelated branches remain eligible.

## 6. Data models, contracts, schemas, and APIs

All contracts reject unknown fields, require non-empty semantic strings, use immutable tuples, exact enums and explicit optionality. Canonical serialization is UTF-8 without BOM, Unicode NFC, LF newlines, lexicographically sorted object keys, declared tuple order, lowercase SHA-256 and no insignificant whitespace. Set-like collections are deduplicated and sorted by canonical ref URI. Ratios and scores are integer micros in `[0, 1_000_000]`; NaN, Infinity and binary floats are forbidden in identity-bearing payloads.

AIR-002 and AIR-004 shared refs are imported by exact schema reference and draft hash; they are not copied into local forks.

### `PrimitiveCoalitionContract` — `ca.air.primitive-coalition-contract/2.1.0-candidate`

Required fields:

- `coalition_id`, `version`, `canonical_hash`, `lifecycle_state`, `authority_ref`, `produced_by`, `created_at` (caller-supplied), `source_context_refs`, `matrix_of_edging_ref`, `broad_signal_ref`, `activation_hypothesis_ref`, `psychological_role_tension_ref`, `registry_snapshot_ref`, `evaluator_profile_ref`;
- `coalition_intent`, `binding_assignments`, `excluded_binding_decisions`, `pairwise_relation_decisions`, `coverage_policy_ref`, `misuse_policy_ref`, `fatality_policy_ref`, `signature_ref`, `dependency_refs`, `supersedes_ref`.

`binding_assignments` contains exact `primitive_binding_ref`, role enum, role rationale evidence refs, weight micros and order key. It has exactly one admitted primary unless the evaluator profile explicitly supports a typed multi-primary geometry. `SUPPRESSION` assignments name the property/risk suppressed and evidence; they are not negative weights. Conflict candidates remain in `pairwise_relation_decisions` with `REINFORCES`, `SUPPRESSES`, `CONTRADICTS`, `FATAL_CONFLICT`, or `NOT_APPLICABLE` plus evidence.

### `CoalitionSignature` — `ca.air.coalition-signature/2.1.0-candidate`

Required fields: `signature_id`, `version`, `coalition_ref`, `ordered_role_vector`, `family_weight_vector`, `candidate_weight_vector`, `synergy_findings`, `redundancy_findings`, `routeability_findings`, `fatality_hypotheses`, `surviving_tension_refs`, `preserved_contradiction_refs`, `geometry_fingerprint`, `authority_ref`, `dependency_refs`, `canonical_hash`.

The vectors use exact IDs plus integer micros. The fingerprint is derived from the full canonical geometry, never from insertion order or display text. Signature comparison returns typed per-dimension deltas; it cannot silently normalize different registry snapshots or evaluator profiles.

### `EdgeProduct` — `ca.air.edge-product/2.1.0-candidate`

Required fields: `edge_product_id`, `version`, `coalition_ref`, `coalition_signature_ref`, `matrix_ref`, `broad_signal_ref`, `source_evidence_refs`, `distinctive_pressure`, `viewer_role`, `live_tension`, `usable_creative_consequence`, `transfer_invariants`, `counteractivation_risks`, `routeability_decisions`, `epistemic_assertions`, `authority_ref`, `evaluation_profile_ref`, `dependency_refs`, `canonical_hash`.

The contract proves that Broad Signal and Edge Product are different refs and lifecycle stages. `transfer_invariants` state what later scripts/compositions must preserve; they do not prescribe VAE production methods.

### `PrimitiveMisuseRisk`

Required fields: `risk_id`, `primitive_binding_refs`, `coalition_ref`, `risk_code`, `trigger_condition`, `affected_role_or_interaction`, `severity`, `fatal`, `evidence_refs`, `mitigation_constraint`, `evaluator_profile_ref`, `status`, `canonical_hash`. `severity` is a governed enum or profile-defined integer micros. Absence of evidence cannot produce low risk.

### `PrimitiveEvaluationReceipt` — `ca.air.primitive-evaluation-receipt/2.1.0-candidate`

Required fields: `receipt_id`, `subject_ref`, `subject_type`, `evaluator_actor_ref`, `evaluator_authority_ref`, `evaluator_profile_ref`, `producer_actor_ref`, `input_refs`, `findings`, `fatal_findings`, `overall_eligibility`, `failure_attribution`, `repair_owner`, `event_ref`, `canonical_hash`.

Each finding contains `dimension`, `applicability`, `verdict`, `evidence_refs`, `observed_value`, `required_policy_ref`, and `reason_code`. `NOT_APPLICABLE` additionally requires `conditional_rule_ref` and `condition_evidence_refs`; otherwise schema validation fails. Producer/evaluator actor equality fails independence unless the profile explicitly proves isolated authority contexts and Program Control later approves that exception.

### `SteeringRecipeCandidate` — `ca.air.steering-recipe-candidate/2.1.0-candidate`

Required fields: `candidate_id`, `recipe_kind`, `recipe_owner`, `coalition_ref`, `coalition_signature_ref`, `edge_product_ref`, `archetype_coalition_refs`, `composition_state_refs`, `applicability_envelope`, `known_failure_refs`, `intervention_program`, `preserved_property_refs`, `evidence_refs`, `observed_run_refs`, `control_comparison_refs`, `compatibility_refs`, `rollback_program`, `lifecycle_state`, `authority_ref`, `canonical_hash`.

`recipe_kind` distinguishes `AIR_SEMANTIC_STEERING` from external types including `VAE_VISUAL_PRODUCTION_STEERING`. External recipes remain evidence or proposed interventions under their owner; they cannot be promoted through this AIR contract. Free-form taste notes, missing rollback, missing known failure, similarity-only selection or absent coalition pin is invalid.

### Commands, events, repository and APIs

- Commands: `CompilePrimitiveCoalitionCommand`, `CompileEdgeProductCommand`, `EvaluatePrimitiveCoalitionCommand`, `QuerySteeringRecipeCandidatesCommand`, `SupersedePrimitiveCoalitionCommand`, `CancelPrimitiveCoalitionCommand`.
- Events: `PrimitiveCoalitionCompiled`, `CoalitionSignatureDerived`, `EdgeProductCompiled`, `PrimitiveCoalitionEvaluated`, `SteeringRecipeCandidatesReturned`, `PrimitiveCoalitionSuperseded`, `CoalitionDescendantsInvalidated`, `CoalitionCommandCancelled`.
- Repository transaction: `append(expected_stream_version, command_record, artifacts, events, dependency_edges, receipts) -> CommitResult`.
- Read APIs: `get_exact(ref)`, `get_receipt(ref)`, `get_command(command_id)`, `list_dependencies(ref)`, `list_descendants(ref, edge_types)`, `replay(stream_id, through_version)`, `find_by_idempotency_key(key)`.
- Service APIs return tagged unions: `Committed{artifact_refs, receipt_ref, stream_version}`, `Replayed{original_receipt_ref}`, `Blocked{blocker_receipt_ref}`, or `Cancelled{cancellation_receipt_ref}`. Exceptions are not the public semantic outcome.

No state artifact may commit without its command, event, dependency edges and receipt; no success receipt may commit without every referenced artifact.

## 7. Implementation stages and exact target paths

These are proposed future paths only. Creation requires ratified/adopted authority, independent acceptance, a bounded Development Capsule and separate build authorization.

| Stage | Exact future paths | Completion boundary |
|---|---|---|
| 1 — domain kernel | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/primitive_coalition.py`; `domain/coalition_signature.py`; `domain/edge_product.py`; `domain/steering_recipe.py` | Closed immutable contracts and pure invariants; no I/O. |
| 2 — schemas and fixtures | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/contracts/schemas/air.primitive-coalition-contract.schema.json`; `air.coalition-signature.schema.json`; `air.edge-product.schema.json`; `air.primitive-evaluation-receipt.schema.json`; `air.steering-recipe-candidate.schema.json`; `contracts/fixtures/air_f05/` | Model/schema parity and valid/invalid deterministic fixtures; no release bytes. |
| 3 — ports and repository | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/ports/primitive_coalition_repository.py`; `repositories/primitive_coalition_repository.py` | Atomicity, parity, idempotency, optimistic concurrency, replay and selective invalidation. |
| 4 — compiler services | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/services/primitive_coalition_service.py`; `services/edge_product_service.py` | Workflows A, B and D; no independent-evaluator authority. |
| 5 — evaluator and recipe candidates | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/evaluation/primitive_coalition_evaluator.py`; `services/steering_recipe_candidate_service.py` | Workflow C, N/A law, independence, retrieval filters and candidate-only lifecycle. |
| 6 — adapters and migration | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/adapters/pipeline_primitive_coalition_adapter.py`; `adapters/vae_visual_recipe_evidence_adapter.py`; `migrations/cmf_primitive_coalition_v1_to_air_f05.py` | Lossless translation or typed block; no local schema fork or ownership transfer. |
| 7 — tests and evidence | Exact paths in section 10 | Every FR/Story, CBAR, claim ceiling, replay and clean-environment case. |

No stage implements Pipeline execution, VAE production realization, Studio canonical state, Delegation transport or Format 02 activation.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Condition | Required outcome |
|---|---|---|
| `AIR_COAL_DRAFT_INTERFACE_HASH_MISMATCH` | AIR-002 or AIR-004 bytes differ from the recorded pin. | Stop and reopen the six revision-impact sections. |
| `AIR_COAL_BINDING_UNRESOLVED` | Binding or Primitive ID/version/hash cannot resolve exactly. | Reject before coalition compilation. |
| `AIR_COAL_ROLE_INCOMPLETE` | Admitted binding lacks one role, rationale or evidence. | Reject; never infer the role. |
| `AIR_COAL_FATAL_CONFLICT` | A fatal pairwise conflict is present. | Reject regardless of aggregate score. |
| `AIR_COAL_OVERLOAD_OR_ROLE_COLLAPSE` | Profile gate detects overload or loss of required role. | Reject and attribute repair to coalition selection. |
| `AIR_COAL_THRESHOLD_PROFILE_MISSING` | Required policy/profile ref is absent, stale or unknown. | Reject; never use brownfield defaults. |
| `AIR_COAL_SIGNATURE_NONDETERMINISTIC` | Same inputs/profile yield different canonical geometry/hash. | Quarantine output and fail determinism evidence. |
| `AIR_COAL_EDGE_NOT_DISTINCT_FROM_BROAD_SIGNAL` | Edge Product is the same object/stage or only repeats broad/topic text. | Reject Edge Product. |
| `AIR_COAL_EDGE_UNROUTABLE` | No approved route preserves required properties. | Retain evidence, emit blocker, no eligibility. |
| `AIR_COAL_NA_INVALID` | Required/unknown/unevaluated finding is marked N/A. | Reject receipt. |
| `AIR_COAL_EVALUATOR_NOT_INDEPENDENT` | Producer and evaluator authority contexts are not independent. | Reject eligibility receipt. |
| `AIR_COAL_RECIPE_AUTHORITY_INVERSION` | Recipe is used to originate or override coalition meaning. | Reject candidate/handoff. |
| `AIR_COAL_IDEMPOTENCY_CONFLICT` | Same key is reused with different command bytes. | Return typed conflict, no write. |
| `AIR_COAL_CONCURRENT_MODIFICATION` | Expected stream version is stale. | Return current version ref, no partial write. |
| `AIR_COAL_ATOMIC_COMMIT_FAILED` | Artifact/event/edge/receipt transaction fails. | Roll back the complete transaction. |
| `AIR_COAL_STALE_DEPENDENCY` | Any exact upstream ref is invalidated/superseded for current use. | Block current consumption; retain historical replay. |
| `AIR_COAL_MIGRATION_MEANING_MISSING` | Legacy bytes lack required roles, evidence or policy. | Preserve source and emit migration blocker. |

### Migration and compatibility

- Legacy V1 objects remain readable and hash-verifiable. Migration creates new immutable V2.1 candidate artifacts linked by `migrated_from`; it never edits old bytes.
- The legacy triad adapter may map only exact historically evidenced bindings and roles. It cannot invent source classification, suppression, conflict, thresholds, signature geometry, Edge Product or evaluator evidence.
- Adapters preserve every required field and constraint. Parsing without behavioral enforcement is incompatible.
- Active handoffs remain pinned to the versions/profile negotiated at acceptance. Deprecation does not invalidate historical replay.
- AIR, Pipeline and VAE consume externally owned schemas by exact refs; no local fork is permitted.

### Rollback, recovery and invalidation

Deployment rollback selects a last-known-good service/profile/registry binding for new commands but leaves outputs and receipts produced under the failed binding reproducible. Recovery verifies repository parity: every committed state has command/event/receipt/dependency records and every receipt target exists. Orphan or partial records are quarantined and never projected as eligible. Supersession adds successors and a deterministic invalidation traversal receipt. Repair reruns only the responsible layer and its typed descendants.

### Observability

Structured telemetry records command/trace IDs, input refs/hashes, evaluator profile, binding/role counts, hard-gate codes, signature hash, Edge Product hash, recipe filter counts, idempotent replay, stream version, commit outcome, invalidation count and responsible repair layer. Logs redact source payloads and exclude absolute machine paths, secrets, environment values and unbounded model text. Metrics may aggregate codes and latency but are never canonical evidence.

## 9. Behavior-specific acceptance criteria

1. **AIR-FR-025 / AIR-ST-05.01 — role-complete coalition.** Given eligible exact AIR-004 bindings and source/Matrix lineage, compilation emits a contract where every admitted binding is primary, support or suppression with evidence and every exclusion/conflict is explicit. A list lacking functional roles is blocked.
2. **AIR-FR-026 / AIR-ST-05.01 — stable signature.** Reordering set-like input, changing process environment or replaying in a fresh process yields identical canonical bytes and signature hash. Changing any binding version, role, weight, relation, registry snapshot or profile changes the hash.
3. **AIR-FR-027 / AIR-ST-05.02 — conflict and misuse hard gates.** Fatal conflict, overload, unaddressed active-Primitive misuse, role collapse or missing coverage blocks eligibility before model ranking. A favorable average cannot compensate.
4. **AIR-FR-028 / AIR-ST-05.02 — Edge Product.** The accepted object states distinctive pressure, viewer role, live tension and usable consequence, traces to survived coalition geometry, and differs from its Broad Signal. Topic-only or unroutable output fails.
5. **AIR-FR-029 / AIR-ST-05.03 — coalition-based Steering Recipe.** Every candidate pins coalition/signature/Edge Product, applicability, intervention, preserved properties, evidence, known failures, comparison and rollback. Similarity-only or taste-note output fails; candidate presence does not imply promotion.
6. **AIR-FR-030 / AIR-ST-05.03 — independent receipt.** The receipt separately reports presence, function, interaction, misuse, coalition integrity, Edge fidelity, routeability and attribution under an independent authority context. Any fatal finding makes overall eligibility fail.
7. **FR-164 / ST-12.01 — broad signal versus Edge Product.** The contract preserves the pre-expression/broad pressure signal as an exact upstream ref and emits the post-survival Edge Product as a distinct versioned object. Flattening them or losing role/tension lineage fails.
8. **FR-171 / ST-12.06 — complete coalition contract.** Primary/support/suppression/conflict bindings, intent, signature, coverage/misuse policy refs, source context and canonical hash are all required before recipe selection. Missing policy refs never receive legacy defaults.
9. **FR-172 / ST-12.06 — measurable geometry.** Signature evidence contains weighted family/candidate geometry plus separate synergy, redundancy, routeability and Edge Product objects. A single winning Primitive or centroid-smoothed vector fails.
10. **FR-173 / ST-12.07 — recipe sovereignty.** Retrieval filters by exact coalition, archetype coalition, composition state, embodiment and known failure before similarity/reranking. A recipe may guide execution but cannot originate or mutate semantic meaning.
11. **FR-174 / ST-12.08 — per-layer evaluation.** Script, composition, provider plan, render, sequence and repair evaluations pin the same coalition lineage and separately measure coverage, misuse, integrity and Edge survival, attributing failure to the responsible layer.
12. **Active Primitive CBAR.** PRM-PRS-002 preserves real tension/release and blocks unresolved or exhausting oscillation; PRM-PRS-009 preserves a grounded inciting disruption and blocks false jeopardy/stranded disequilibrium; PRM-PRS-015 preserves evidence-grounded What Is/What Could Be tension and blocks utopian overclaim or demoralizing pain saturation.
13. **`NOT_APPLICABLE`.** Given a profile-declared conditional dimension with condition evidence, N/A validates. Given a required, unknown, absent or merely inconvenient dimension, N/A fails with `AIR_COAL_NA_INVALID`.
14. **Atomicity and replay.** Injected failure at each commit boundary leaves no partial artifact/receipt pair. Exact command replay returns original hashes; conflicting key reuse and stale expected version write nothing.
15. **Supersession and historical reproduction.** Upstream supersession invalidates only typed descendants. Historical coalition, evaluation and recipe-candidate paths remain byte-reproducible after invalidation.
16. **Cross-product authority.** Contract tests prove Pipeline cannot rewrite coalition/Edge meaning, VAE cannot mutate upstream semantic authority, AIR cannot claim VAE production acceptance, and Studio projections cannot become canonical state.
17. **Claim ceiling.** While ratification is pending, every status projection remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, specification work authorized, build false, with maximum later status `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; no capsule is issuable.

## 10. Testing and completion evidence

### Required future suites

| Exact future path | Required evidence |
|---|---|
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_primitive_coalition.py` | Roles, exclusions, conflicts, misuse, profile refs, no defaults and invalid N/A. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_coalition_signature.py` | Fixed-point vectors, order independence, synergy/redundancy, anti-centroid and signature determinism. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_edge_product.py` | Broad/Edge distinction, pressure/role/tension/consequence, routeability and transfer invariants. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/contract/test_air_f05_schemas.py` | Closed schemas, generated-type parity, exact refs, tagged outcomes and additional-property rejection. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_primitive_coalition_signature_edge_product_and_steering_recipes.py` | All eleven FRs, seven Stories and producer/evaluator separation end to end. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_air_f05_repository.py` | Atomic commit/rollback, state-receipt parity, idempotency, optimistic concurrency and cancellation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/integration/test_air_f05_cross_product_authority.py` | Pipeline/VAE/Studio/Delegation ownership denial and exact-schema consumption. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/migration/test_cmf_primitive_coalition_v1_to_air_f05.py` | Lossless evidence mapping or typed block; no invented classification, roles, threshold or Edge Product. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/replay/test_air_f05_replay_invalidation.py` | Historical reproduction, typed descendant invalidation and unrelated-branch preservation. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/cbar/test_air_f05_active_primitives.py` | Exact PRM-PRS-002/009/015 hashes, core moves, activation, misuse and suppression/inapplicability cases. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/determinism/test_air_f05_portability.py` | Fresh-process equality across time, random state, env, insertion/traversal order and machine paths. |

### Adversarial matrix

Evidence includes: unresolved/label-only Primitive; stale Matrix or binding; missing source; no primary; conflicting primaries; fatal pair; unproved suppression; role collapse; overload; legacy default threshold; float drift; random UUID/time; insertion-order drift; broad/Edge aliasing; topic-only Edge; centroid flattening; unroutable Edge; visual-similarity-only recipe; VAE recipe authority inversion; invalid N/A; producer self-evaluation; aggregate compensation; partial commit at every boundary; orphan receipt/artifact; idempotency conflict; concurrent update; cancellation race; invalidation overreach/underreach; lossy migration; absolute path leakage; and unauthorized capsule/build projection.

### Completion evidence contract

Future implementation evidence must include generated schema/type parity, canonical vectors, exact source/Primitive hash matrix, command/event/artifact/receipt parity report, independent evaluation profiles and receipts, migration report, compatibility report, atomicity/failure-injection traces, replay/invalidation proof, clean-environment proof, full suite twice in fresh processes, Python compilation/type checks and independent audit by an agent other than the writer. Any behavior depending on SRC-EXT-027 remains unclaimed until exact bytes are supplied and hash-locked.

This writing execution issues no audit, revision, acceptance, build receipt, release, code, schema or Development Capsule. Final state: `WRITTEN_PENDING_AUDIT`; authority `CANDIDATE_NOT_CURRENT`; specification work authorized; build authority false; later acceptance ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
