---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-AIR-004
title: Primitive Family Registry and Primitive Binding
version: 2.1.0-candidate.1
product_owner: Activative Intelligence Runtime
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 1
controlling_frs: [AIR-FR-019, AIR-FR-020, AIR-FR-021, AIR-FR-022, AIR-FR-023, AIR-FR-024, FR-169, FR-170]
controlling_stories: [AIR-ST-04.01, AIR-ST-04.02, AIR-ST-04.03, ST-12.05]
---

# TS-AIR-004 — Primitive Family Registry and Primitive Binding

## 1. Files and authorities read

This is candidate specification work. V2.1 is `CANDIDATE_NOT_CURRENT`; WRITE is authorized, BUILD is not, and the maximum later state before ratification is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

| Source | SHA-256 | Authority / dependency state | Fact used |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/.../PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_01_DISPATCH_LOCK.yaml` | `2fa4102de472196fb05320e675ad6095316689e7c585bcba42f432f59ed98692` | controller dispatch authority | Admits exact AIR-001 draft hash for TS-AIR-004. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-001.md` | `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc` | `WRITTEN_PENDING_AUDIT`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | Supplies draft shared immutable references, authority/epistemic assertions, lifecycle, hashing, repository atomicity, and typed blocker interface. It is not ratified authority. |
| AIR bundle `specs/TS-AIR-004-primitive-family-registry-and-primitive-binding.md` | `9cd647036b7489142774856fede71ce5debc459ca8c4e48b0346ab32cf842d59` | full draft; `AMEND_TO_CURRENT_AUTHORITY` | Provides the existing implementation-grade baseline, exact objects, target paths, CBAR mandates, and acceptance cases. |
| AIR bundle `prd/features/F04-primitive-family-registry-and-primitive-binding.md` | `4d309831645365ddd06ad10d798521ac4fe72cd98d6b596d8a68ebc9a08819da` | candidate PRD feature | AIR owns exact Primitive query, binding, relations, stage coverage, and receipts. |
| AIR bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | candidate Story authority | AIR-ST-04.01–04.03 prohibit name-only selection and require exact YAML, conflict/misuse, replay, and selective invalidation. |
| AHP bundle `planning/EPICS_AND_VERTICAL_STORIES.md` | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | candidate cross-product Story | ST-12.05 requires Pipeline to query AIR rather than attach Primitive IDs after recipe/layout selection. |
| `sources/doctrine/MEANING_PRIMITIVE_REGISTRY_SPEC.md` | `1851f4e8e07beb6e1886e91f45d8bb12cf38d6fc8af8f20e314788d6d47d7e5f` | `REQUIRED_UNIQUE_EVIDENCE`, SRC-PRIM-001 / SRC-DOCT-007 | Meaning primitives steer, route, validate, and train output meaning; they are not experience-flow mechanics. |
| `sources/doctrine/EXPERIENCE_PRIMITIVE_REGISTRY_SPEC.md` | `5cb5f1b568c84e41bbbf2ccbb18b938ccee5de1c6cab5cbee96343d88adaee72` | `REQUIRED_UNIQUE_EVIDENCE`, SRC-PRIM-002 / SRC-DOCT-008 | Experience primitives shape participant/user state, adoption, trust, recovery, progression, and flow. |
| `sources/cmf_primitive_registry_snapshot` | `4a3423b0fce2b30c58e65275a656a0188693656406dd12269fe2e58d4d514447` | `REQUIRED_UNIQUE_EVIDENCE`, SRC-PRIM-003 | Exact Primitive YAML snapshot; names and summaries never substitute for byte-resolved definitions. |
| `sources/doctrine/MATRIX_OF_EDGING.md` | `7ba1858cd9238a63f32d28e9cc8e7bbe306ba82ac5fa5af4a0346128aa3b6ebb` | `REQUIRED_UNIQUE_EVIDENCE`, SRC-MOE-001 | Broad signals, candidate survival, coalition geometry, and Edge Products are distinct stages of controlled tension selection. |
| `PRM-BUS-001.yaml` | `9eebedc6b3c9bb55ab2ec85ae239394d9ebac629b9e44a579f5e11d3fc03db4e` | exact active Primitive evidence | Perception and Guidance Stack; requires attention/action routing and forbids dark-pattern or visual-noise misuse. |
| `PRM-BUS-006.yaml` | `6abfae7c921e5768d459ceeb57b073ba9ba2865ad03e907bcb3361a72b391133` | exact active Primitive evidence | Hierarchy as Attention Routing; forbids competing levels and arbitrary emphasis. |
| `PRM-PSY-001.yaml` | `77c09b403aca66e77b2c71b1faa4dbeacd410d9d6c69685f9c2222dc65bf8ca7` | exact active Primitive evidence | Matching Principle; requires active conversation-layer alignment and exposes inflexibility/performative-matching misuse. |
| `sources/doctrine/PRIMITIVE_COALITION_CONTRACT.py` | `990735d588e03004cbee780cea7e3623361a7fa70991e898ff13f173618cbf08` | `REQUIRED_UNIQUE_EVIDENCE`, SRC-DOCT-009; brownfield | Useful roles and compatibility adapter; random UUIDs, mutable lists/maps, implied thresholds, and coarse hashing require replacement. |
| `reference_implementation/activative_intelligence_v2/primitive_archetype_models.py` | `5c2eaf15168e0843938637ac23e25155ff6ae702a56217df4644a1c277e208b9` | candidate reference implementation | Strict/frozen binding, misuse, coalition, Edge Product and evaluation shapes can be adapted after authority and determinism correction. |
| `tests/test_v21_primitive_archetype_invariants.py` | `8d3a8ccbd3dd964d8d678596283beafd3495cf9593974a3fa27408654a44abb6` | candidate invariant evidence | Failed Primitive gates cannot pass, Final Script requires full lineage, and Format 02 cannot be activated by an animation package. |
| Program Control cross-product and semantic-object ownership matrices | current Prompt 01 candidate hashes | candidate authority | AIR owns Primitive/archetype/brand/Voice DNA/Visual DNA/Final Script/role-tension/Matrix/transfer semantic compilation; Pipeline consumes and executes without rebuilding meaning. |
| Prompt 02 ledgers, source disposition, source gaps, dependency classification, path registry, Prompt 02C authorization | committed Prompt 02 / Prompt 02C hashes | controlling workflow evidence | Eight FRs, four Stories, exact AIR path, write wave, required-source availability, and non-build ceiling are frozen. |

The AIR-001 draft controls shared interface assumptions only. If its audited bytes change, sections 3, 5, 6, 8, 9, and 10 of this document require downstream impact review before acceptance.

## 2. Problem, user outcome, solution, and scope

### Problem

A Primitive selected by label similarity or after a visual recipe has already been chosen is ceremonial metadata, not a behavioral recipe. Without exact registry and version resolution, a producer can silently omit core moves, suppression conditions, conflicts, Primitive Misuse Risks, and stage applicability. The immediate downstream failure is that coalition compilation receives a fluent but semantically incompatible binding, so the eventual psychological role, Edge Product, archetype route, Final Script, composition, or evaluation cannot be explained or repaired.

### User and system outcome

An Activative operator or Pipeline caller can query the governed Meaning and Experience Primitive registries using exact source evidence, epistemic state, Matrix of Edging state, psychological role inside a tension, category, archetype constraints, active Brand Context Version, and execution stage. AIR returns exact, versioned candidate references and accepts only explicit Primitive Bindings with applicability, local function, suppression, conflicts, misuse risks, and evaluation targets. Downstream systems consume the result without reconstructing Primitive meaning.

### Bounded solution

Implement an AIR-owned Primitive registry query and binding service with:

1. byte-resolved `PrimitiveFamilyReference` and `PrimitiveVersionReference` records;
2. deterministic eligibility filtering before learned ranking;
3. immutable `PrimitiveBinding` records tied to target object, role/tension, stage and evidence;
4. explicit `PrimitiveRelationSet`, `PrimitiveMisuseRisk`, and `PrimitiveCoverageRequirement` records;
5. atomic, idempotent `PrimitiveBindingReceipt` commits; and
6. typed query/bind/evaluate/supersede/replay APIs and handoff receipts.

### In scope

- AIR-FR-019–024 and FR-169–170.
- Meaning versus Experience plane discrimination and cross-plane relations.
- Exact Primitive ID, version, source-registry and source-byte resolution.
- Deterministic eligibility; bounded candidate ranking only after eligibility.
- Binding to source evidence, activation state, stage, role/tension, intended effect, execution surface, category/archetype constraints, allowed adaptation, suppression, conflicts, misuse, and evaluation.
- Stage-appropriate coverage for source activation, script formation, composition, experience and evaluation.
- Immutable receipts, optimistic concurrency, idempotency, replay, supersession and selective invalidation.
- AIR-to-Pipeline typed query/handoff boundary.

### Out of scope and non-goals

- Compiling the Primitive Coalition Contract, Coalition Signature, or Edge Product terminal object owned by TS-AIR-005; this spec supplies validated inputs.
- Selecting an archetype, writing/approving the Final Script, composing, rendering, or executing Pipeline/VAE work.
- Creating a second Primitive registry, modifying source Primitive YAMLs, or promoting brownfield code as current authority.
- Letting Pipeline, Builder, Studio, models, UI, or VAE reinterpret Primitive meaning.
- Inventing evaluator thresholds, using a model confidence as authority, or allowing `NOT_APPLICABLE` to hide missing required coverage.
- Activating Format 02, VAE Stage 5, implementation, production, or certification.

## 3. Governing decisions and constraints

### Product sovereignty

- AIR owns semantic interpretation, Primitive selection/binding, Primitive relationship semantics and the binding receipt.
- The governed Primitive registry authority owns each source Primitive definition and version. AIR references those bytes; it does not mutate them in place.
- Pipeline may request, cache, validate, retrieve, execute and invalidate AIR outputs, but it cannot select a recipe first and retrofit Primitive IDs or rewrite the returned local function.
- Builder declares exact AIR dependencies in `AtomicHarnessDefinition`; it does not compile Primitive meaning.
- Independent evaluation owns evaluation receipts; the producer cannot approve itself.
- Studio is a noncanonical projection and typed command surface. A human correction emits a `HumanResolutionEpisode`; it does not mutate hidden state.

### Semantic laws

1. Meaning Plane and Experience Plane are distinct. A Primitive may have an explicit cross-plane relation but never an ambiguous or inferred plane.
2. Source evidence, Context Premise, Resonance, Matrix of Edging, activation hypothesis, psychological role inside a tension, archetype/category constraints, Brand Context Version, Guest Voice DNA and Visual DNA are referenced by exact immutable IDs when applicable. Missing values remain absent and block claims that require them.
3. Primitive selection precedes coalition, archetype, Final Script, composition and layout selection. A downstream appearance or tool cannot backfill the recipe.
4. Every candidate resolves to exact source bytes before eligibility or ranking. Alias/name similarity is only a discovery aid and never proof of identity.
5. Activation/suppression conditions, `conflicts_with`, `synergizes_with`, core move and all misuse modes are loaded from the same Primitive version.
6. Applicability is contextual. No Primitive is universally required or universally safe.
7. Primitive Misuse Risk and fatal conflict are non-compensable: strength elsewhere cannot average them away.
8. `NOT_APPLICABLE` is legal only when the evaluation contract declares that dimension conditionally applicable and the receipt cites the condition and evidence. It cannot replace an unresolved required check.
9. AIR-001 shared authority/lifecycle types are `DRAFT_DEPENDENCY_NOT_ACCEPTED`; they may guide interface writing but cannot be represented as ratified law.
10. Operator-supplied source authority, provenance, lineage, attributable approvals, and product sovereignty are preserved. No generic creative-safety/content-rights approval authority is introduced.

### Claim ceiling

This specification is `WRITTEN_PENDING_AUDIT`, not adopted or build-ready. Until attributable ratification, independent audit/revision/re-audit may reach at most `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; no Development Capsule, product code, production claim or certification may be issued.

## 4. Current brownfield architecture

No current `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/` tree exists. All implementation paths below are prospective.

| Exact source | Current behavior | Disposition | Migration constraint |
|---|---|---|---|
| AIR V2.1 source Primitive YAML snapshot | 191 Meaning and 50 Experience Primitive records with families, conditions, risks and relations; exact snapshot digest is locked. | `ACTIVATE` as immutable registry source after ratification | Preserve bytes and source hashes; do not normalize historical content in place. |
| `sources/doctrine/MEANING_PRIMITIVE_REGISTRY_SPEC.md` | Defines steering/routing/validation/training plane and metadata. | `ACTIVATE` as candidate registry contract | Replace absolute dependency paths in runtime artifacts with governed relative refs. |
| `sources/doctrine/EXPERIENCE_PRIMITIVE_REGISTRY_SPEC.md` | Defines adoption/state/flow plane and metadata. | `ACTIVATE` as candidate registry contract | Preserve plane distinction and do not flatten UI mechanics into meaning semantics. |
| `sources/doctrine/PRIMITIVE_COALITION_CONTRACT.py` | Pydantic brownfield contract with roles, conflicts, coverage and a legacy-triad adapter. | `ADAPT` | Remove random IDs, implicit default thresholds, open dictionaries, float-dependent identity, and incomplete evidence enforcement. Do not treat its schema IDs as current. |
| `reference_implementation/.../primitive_archetype_models.py` | Strict/frozen prospective models, exact binding version/hash, misuse risk, coalition/evaluation gates. | `ADAPT` | Split TS-AIR-004 binding objects from TS-AIR-005 coalition objects; replace untyped `dict` fields and pin shared types to adopted AIR-001 bytes. |
| `tests/test_v21_primitive_archetype_invariants.py` | Proves a failed binding/gate cannot pass and protects downstream lineage boundaries. | `REUSE` as regression seed | Add exact registry, query, N/A, concurrency, migration, replay and cross-product cases. |
| old CMF Studio primitive registries and coalition contract | Predecessor evidence and compatibility shapes. | `ARCHIVE` as historical evidence; selectively `ADAPT` after file-level review | Historical IDs/receipts remain replayable; no automatic authority promotion or guessed plane/version. |
| AIR-001 draft shared types and repository law | Draft immutable ref, authority, epistemic, lifecycle and atomic persistence interface. | `ADAPT` as hash-pinned draft interface | Sections named in the draft receipt reopen if the audited AIR-001 hash changes. |

The current full TS-AIR-004 draft is amended rather than rewritten for stylistic uniformity: its object boundaries, source paths, active Primitive CBAR cases and prospective module paths remain, while current Program Control ownership, dependency status, eight-FR coverage, deterministic contracts and claim ceiling are added.

## 5. Proposed architecture and workflows

### Components

| Component | Responsibility | Forbidden behavior |
|---|---|---|
| `PrimitiveRegistryPort` | Resolve snapshot, registry, family, Primitive ID/version/hash and supersession. | Name-only resolution, mutable source updates, implicit latest version. |
| `PrimitiveEligibilityService` | Apply plane, family, source, role/tension, stage, category/archetype, activation/suppression and authority gates. | Learned ranking before deterministic eligibility. |
| `PrimitiveCandidateRanker` | Rank only eligible candidates and preserve rejected candidates/rationale. | Authority, hard-gate or acceptance decisions. |
| `PrimitiveBindingService` | Validate explicit local function, evidence, adaptation, relations, risks and coverage; commit immutable binding plus receipt. | Coalition compilation, downstream execution, self-evaluation. |
| `PrimitiveBindingRepository` | Atomically append binding, relations, dependency edges, command and receipt; maintain current-head projection. | Update/delete history or store state without receipt. |
| `PrimitiveBindingEvaluatorPort` | Obtain independent judgment under a pinned evaluation profile. | Producer identity, threshold invention or silent N/A. |
| `PrimitiveHandoffAdapter` | Emit public query and binding handoff to TS-AIR-005 and Pipeline. | Flatten source, role/tension, risk, exclusions or authority into notes. |

### Workflow A — query

1. Caller submits `QueryPrimitiveCandidatesCommand` with exact activation/context refs and a pinned registry snapshot.
2. Service validates authority, source existence, epistemic eligibility, stage/category/archetype constraints, and request hash.
3. Registry port loads exact Primitive bytes and constructs immutable version references.
4. Eligibility service classifies candidates as eligible, suppressed, conflicting, inapplicable, stale, or unresolved with reason/evidence.
5. Optional ranker orders only eligible candidates. Deterministic filters and all rejected records remain visible.
6. Repository appends query result and receipt atomically; Pipeline receives references, never reconstructed definitions.

### Workflow B — bind and evaluate

1. `CreatePrimitiveBindingCommand` pins one query result, exact Primitive reference, target object, stage, psychological role/tension, intended effect, execution surface, local function and evidence.
2. Service resolves source bytes again, checks expected version, activation/suppression, relationships and misuse coverage.
3. A deterministic binding validation receipt is committed with the proposed binding.
4. Independent evaluator evaluates the exact binding hash using a pinned profile. Required dimensions cannot be N/A.
5. On pass, AIR emits an immutable accepted binding receipt and typed downstream handoff. On failure/insufficient evidence, it emits a blocker/repair receipt and no downstream-eligible binding.

### Commands, events and states

Commands: `QueryPrimitiveCandidatesCommand`, `CreatePrimitiveBindingCommand`, `SupersedePrimitiveBindingCommand`, `EvaluatePrimitiveBindingCommand`, and `ReplayPrimitiveBindingCommand`.

Events: `PrimitiveQueryRecorded`, `PrimitiveBindingProposed`, `PrimitiveBindingValidated`, `PrimitiveBindingRejected`, `PrimitiveBindingSuperseded`, `PrimitiveBindingDescendantsInvalidated`, and `PrimitiveBindingHandoffEmitted`.

State machine: `proposed -> validated -> independently_evaluated -> downstream_eligible`; side states are `rejected`, `superseded`, `cancelled`, and `stale`. Only exact current bytes plus pass receipts can enter `downstream_eligible`.

### Atomicity, idempotency, replay and cancellation

- `command_id` plus canonical payload hash is the idempotency identity. Same ID/same hash returns the original receipt; same ID/different hash returns `AIR_PRIM_IDEMPOTENCY_CONFLICT`.
- `expected_prior_ref` enforces optimistic concurrency. Stale writes commit only a denial receipt.
- Binding, relationship set, dependency edges, command record and receipt commit in one transaction; partial visibility is forbidden.
- Cancellation before commit produces `AIR_PRIM_CANCELLED_NO_COMMIT`; after commit the stored receipt wins and history remains.
- Replay uses recorded registry snapshot, Primitive bytes, evaluator profile and command payload, never mutable “latest” state.
- Supersession creates new immutable versions and invalidates only typed descendants; source evidence and unrelated bindings remain replayable.

## 6. Data models, contracts, schemas, and APIs

All schemas use `additionalProperties: false`, non-empty strings, exact enums, immutable records and explicit optionality. Canonical serialization uses UTF-8 I-JSON, Unicode NFC, lexicographically sorted object keys, no insignificant whitespace, `Z` timestamps, and no NaN/Infinity. Arrays with semantic order preserve it; arrays defined as sets are deduplicated and sorted by canonical reference URI. Generated IDs are derived from canonical payload bytes, not clocks, randomness, traversal order, local paths, or environment. Source Primitive identity is always the SHA-256 of exact source bytes.

### Shared `ImmutableRef`

The hash-pinned AIR-001 draft defines `{object_id, version, sha256}` and draft authority/epistemic types. TS-AIR-004 imports them by exact schema ref and hash; it does not copy/fork them. Until AIR-001 is audited and accepted, every such use is labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`.

### `PrimitiveVersionReference` — `ca.air.primitive-version-reference/2.1.0`

| Field | Type | Required | Owner / rule |
|---|---|---|---|
| `primitive_ref_id` | content-derived non-empty string | yes | AIR reference identity. |
| `primitive_id` | governed Primitive ID | yes | Primitive registry authority; exact YAML value. |
| `primitive_version` | non-empty version string | yes | Registry authority; no implicit latest. |
| `primitive_sha256` | lowercase hex64 | yes | Exact source bytes. |
| `registry_ref` | `ImmutableRef` | yes | Registry authority. |
| `snapshot_ref` | `ImmutableRef` | yes | Exact frozen snapshot. |
| `plane` | `meaning_plane` or `experience_plane` | yes | Registry definition; never guessed. |
| `family` | governed non-empty family ID | yes | Registry definition. |
| `core_move` | non-empty string | yes | Exact versioned definition. |
| `activation_conditions` | ordered tuple of non-empty strings | yes | May be empty only when exact source declares empty. |
| `suppression_conditions` | ordered tuple of non-empty strings | yes | Same-source version. |
| `misuse_modes` | ordered tuple of non-empty strings | yes | Same-source version. |
| `synergizes_with` | sorted unique tuple of Primitive IDs | yes | Same-source version. |
| `conflicts_with` | sorted unique tuple of Primitive IDs | yes | Same-source version. |
| `supersession_state` | `current`, `deprecated`, `superseded`, `revoked` | yes | Registry authority. |
| `supersedes_ref` | `ImmutableRef` or null | yes | Required when superseded. |

### `PrimitiveQueryContext` — `ca.air.primitive-query-context/2.1.0`

Required fields: `context_id`, `source_evidence_refs`, `epistemic_state_ref`, `context_premise_ref`, `matrix_of_edging_ref`, `activation_hypothesis_ref`, `psychological_role_tension_ref`, `execution_stage`, `category_id`, `archetype_constraint_refs`, `brand_context_ref`, `voice_dna_ref`, `visual_dna_ref`, `requested_planes`, `requested_functions`, `authority_ref`, and `canonical_hash`.

Nullable context fields are explicit `ImmutableRef | null`; a null is allowed only when the request declares the corresponding applicability code. The service rejects a claim that requires a missing field. `execution_stage` is one of `source_activation`, `script_formation`, `composition`, `experience`, `evaluation`. `requested_planes` is a non-empty sorted unique tuple.

### `PrimitiveCandidateDecision`

Fields: `primitive_ref`, `decision` (`eligible`, `suppressed`, `conflicting`, `not_applicable`, `stale`, `unresolved`), `reason_codes`, `evidence_refs`, `matched_activation_conditions`, `matched_suppression_conditions`, `conflict_refs`, `misuse_risk_refs`, and optional `rank_micros` integer `0..1000000`. `rank_micros` is comparative evidence only and cannot override deterministic denial.

### `PrimitiveBinding` — `ca.air.primitive-binding/2.1.0`

| Field | Type | Required | Owner / rule |
|---|---|---|---|
| `binding_id` | content-derived non-empty string | yes | AIR. |
| `binding_version` | semantic version | yes | AIR; immutable. |
| `primitive_ref` | `ImmutableRef` | yes | Exact registry version. |
| `target_object_ref` | `ImmutableRef` | yes | Owning producer. |
| `query_context_ref` | `ImmutableRef` | yes | AIR. |
| `stage` | five-stage enum | yes | AIR. |
| `role_tension_ref` | `ImmutableRef` | yes | AIR. |
| `role` | governed Primitive-binding role enum | yes | AIR; includes semantic/experience/suppression roles, never free-form. |
| `local_function` | non-empty string | yes | AIR; explains what the exact Primitive does here. |
| `intended_effect` | non-empty string | yes | AIR; evidence-bearing hypothesis, not guaranteed result. |
| `execution_surface` | governed surface ID | yes | Consumer-declared, AIR-validated. |
| `activation_evidence_refs` | non-empty tuple of `ImmutableRef` | yes | Source/evidence owners. |
| `allowed_adaptations` | sorted unique tuple of governed adaptation codes | yes | AIR. Empty means no adaptation. |
| `suppression_conditions` | ordered tuple | yes | Exact source plus contextual additions with provenance. |
| `relation_set_ref` | `ImmutableRef` | yes | AIR. |
| `misuse_risk_refs` | tuple of `ImmutableRef` | yes | AIR; one per applicable source misuse plus contextual risks. |
| `evaluation_profile_ref` | `ImmutableRef` | yes | Independent Evaluation. |
| `epistemic_state` | AIR-001 epistemic enum | yes | Usually planned/inferred until observed evaluation. |
| `authority_ref` | AIR-001 authority ref | yes | Program Control. |
| `lifecycle_state` | binding-state enum | yes | AIR. |
| `supersedes_ref` | `ImmutableRef` or null | yes | AIR. |
| `canonical_hash` | lowercase hex64 | yes | Deterministic serialization. |

### Relations, risks and coverage

`PrimitiveRelationSet` requires binding ref, `reinforces`, `suppresses`, `conflicts`, and `fatal_conflicts`, each a sorted unique tuple of `{other_primitive_ref, relation_reason, evidence_refs}`. The same pair/direction cannot appear under contradictory relation types without an explicit `PrimitiveRelationConflict` blocker.

`PrimitiveMisuseRisk` requires `risk_id`, `primitive_ref`, `misuse_mode`, `trigger_condition`, `probable_wrong_reading`, severity (`low`, `moderate`, `high`, `fatal`), `prevention_gate`, and evidence refs. Fatal applicable risks block eligibility.

`PrimitiveCoverageRequirement` requires stage, required function, applicability condition, required plane(s), minimum evidence classes, evaluation dimension ID and owning evaluator profile. It contains no invented numeric threshold; any threshold is held in the independently governed evaluation-profile version.

### `PrimitiveBindingReceipt` — `ca.air.primitive-binding-receipt/2.1.0`

Fields: `receipt_id`, `command_id`, `payload_sha256`, `prior_ref`, `binding_ref` or null, `query_result_ref`, `registry_snapshot_ref`, `deterministic_gate_results`, `independent_evaluation_receipt_ref` or null, `coverage_results`, `relation_decisions`, `misuse_decisions`, `exclusion_refs`, `downstream_consumers`, `decision` (`accepted`, `repair_required`, `blocked`, `superseded`), `blocker` or null, `actor_ref`, `authority_ref`, `validator_refs`, `recorded_at_utc`, and `canonical_hash`.

Each coverage result is `pass`, `fail`, or `not_applicable`. `not_applicable` requires `applicability_condition_id`, non-empty reason, and evidence refs; it is forbidden for an unconditional required dimension. An accepted receipt requires all hard gates pass, no applicable fatal risk, no unresolved/fatal conflict and a distinct evaluator pass.

### Public APIs

- `POST /v2.1/primitive-queries` accepts `QueryPrimitiveCandidatesCommand`; returns query result/receipt or typed blocker.
- `POST /v2.1/primitive-bindings` accepts `CreatePrimitiveBindingCommand`; returns proposed/validated binding receipt.
- `POST /v2.1/primitive-bindings/{binding_id}/evaluations` accepts exact binding/evaluator refs; producer identity is rejected.
- `POST /v2.1/primitive-bindings/{binding_id}/supersessions` creates a successor; no in-place update.
- `GET /v2.1/primitive-bindings/{binding_id}/versions/{version}` returns immutable bytes and receipts.
- `POST /v2.1/primitive-bindings/{binding_id}/replay` replays a recorded snapshot.

### Examples

Positive: PRM-PSY-001 resolves by exact hash, binds to an emotional-layer source activation stage, cites source spans and role/tension, records layer-shift suppression, performative-matching misuse, evaluation profile and Pipeline consumer. It may become downstream-eligible only after deterministic and independent gates pass.

Negative: a caller asks for “Matching Principle” by name, omits the source YAML version, and marks all misuse checks `not_applicable`. The service returns `AIR_PRIM_VERSION_UNRESOLVED` and `AIR_PRIM_NA_REQUIRED_DIMENSION`; no binding artifact is committed.

## 7. Implementation stages and exact target paths

These are future paths only; ratification, independent acceptance and a bounded Development Capsule are required before creation.

| Stage | Exact target paths | FR / Story coverage |
|---|---|---|
| 1 — strict domain contracts | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/primitive_registry.py`; `domain/primitive_binding.py`; `contracts/schemas/primitive_version_reference.schema.json`; `primitive_query_context.schema.json`; `primitive_binding.schema.json`; `primitive_binding_receipt.schema.json` | AIR-FR-019–024, FR-169–170; all four Stories. |
| 2 — deterministic registry and serialization | `.../registries/primitive_registry.py`; `.../serialization/canonical.py`; `.../adapters/primitive_snapshot_adapter.py` | AIR-FR-019/020, FR-169; AIR-ST-04.01, ST-12.05. |
| 3 — query/binding services | `.../services/primitive_query_service.py`; `.../services/primitive_binding_service.py`; `.../repositories/primitive_binding_repository.py` | all eight FRs; query, binding, atomic receipt and replay. |
| 4 — relations, coverage and evaluation | `.../services/primitive_relation_service.py`; `.../evaluation/primitive_binding_evaluator.py` | AIR-FR-022–024; AIR-ST-04.02/03. |
| 5 — public and Pipeline adapters | `.../api/primitive_routes.py`; `.../adapters/primitive_handoff.py` | FR-169/170, ST-12.05; consumer denial proof. |
| 6 — migration and recovery | `.../migrations/primitive_v2_to_v21.py`; `.../invalidation/primitive_descendants.py` | all supersession/replay/recovery cases. |
| 7 — exact tests and evidence | Paths in section 10 | Every acceptance criterion and claim-ceiling boundary. |

TS-AIR-005 consumes the accepted public binding interface in a later wave. Pipeline receives references/contracts only. No product-local implementation is authorized here.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Retry / repair | Responsible owner and next action |
|---|---|---|
| `AIR_PRIM_PLANE_AMBIGUOUS` | deterministic repair | Registry authority supplies exact plane/version; AIR never guesses. |
| `AIR_PRIM_VERSION_UNRESOLVED` | new evidence required | Supply exact Primitive ID, version, registry and hash. |
| `AIR_PRIM_SOURCE_HASH_MISMATCH` | correct immutable bytes | Reconcile snapshot/source lock; no “latest” fallback. |
| `AIR_PRIM_CONTEXT_INCOMPLETE` | repair query | Caller supplies required source/role/tension/stage/category context. |
| `AIR_PRIM_SUPPRESSED` | context change or different candidate | Preserve decision; do not rank the suppressed candidate. |
| `AIR_PRIM_FATAL_CONFLICT` | bounded semantic repair or human escalation | AIR resolves/suppresses explicitly; no averaging. |
| `AIR_PRIM_MISUSE_GATE_FAILED` | repair local function or candidate | Preserve risk evidence and failed receipt. |
| `AIR_PRIM_NA_REQUIRED_DIMENSION` | correct evaluation | Required dimension must pass; no N/A waiver. |
| `AIR_PRIM_SELF_EVALUATION` | independent evaluator required | Route exact binding hash to a distinct evaluator. |
| `AIR_PRIM_STALE_EXPECTED_VERSION` | retry against current head | Re-read and submit a new immutable successor command. |
| `AIR_PRIM_IDEMPOTENCY_CONFLICT` | new command ID required | Preserve original command/receipt. |
| `AIR_PRIM_MIGRATION_AMBIGUOUS` | attributable mapping required | Do not infer plane, version, relation or evidence. |
| `AIR_PRIM_LATE_EVALUATION` | evaluate current exact hash | Historical result is stored but cannot change current head. |

Deterministic failures are not blindly retried. Transient storage/transport failures retry with the same command ID. Semantic quality repair uses a new command referencing the failed receipt. Learned ranker failure falls back to deterministic eligible ordering or an explicitly pinned stronger path; silent model substitution is prohibited.

### Migration and compatibility

- V2.1 migration creates new immutable artifacts that cite exact legacy bytes and mapping decision. It never edits legacy objects.
- Legacy `meaning`/`experience` values map only when unambiguous; unknown plane, missing version/hash, open `dict` relationships, random IDs and default thresholds block migration.
- Legacy triad-to-coalition adaptation belongs to TS-AIR-005. TS-AIR-004 may migrate only each exact binding and its evidence.
- Historical source float fields are preserved in exact source bytes. Derived decisions use fixed integers/strings and are excluded from source identity.
- Consumers negotiate schema and feature versions; adapters may add explicit evidence but cannot remove constraints or flatten relations/misuse into notes.
- Active handoffs remain pinned to the schema, registry snapshot and evaluator profile accepted at submission.

### Rollback, recovery and invalidation

Rollback rebinds service/adapter/evaluator to a last-known-good version and emits a receipt; artifacts created under the failed binding remain reproducible. Recovery rebuilds current heads and eligibility projections from immutable artifacts/events and compares canonical hashes. Superseding a Primitive version marks bindings that reference it stale and invalidates only typed descendants. A late evaluation or handoff for a stale binding is historical evidence only. Repository fault injection must prove no artifact without receipt and no receipt referencing an absent artifact.

### Observability

Metrics include query candidates by decision, plane/family, source-hash failures, suppression/conflict/misuse codes, N/A decisions, stage coverage failures, idempotent replay, stale-version conflict, invalidated descendants, evaluation latency and handoff rejection. Structured logs carry IDs, versions, hashes, authority, actor, reason codes and receipt refs but no raw private source text. Alerts fire for orphan state/receipts, self-evaluation, replay mismatch, required N/A, source drift, or a downstream consumer receiving a stale binding.

## 9. Behavior-specific acceptance criteria

1. **AIR-FR-019 / AIR-ST-04.01 — plane distinction.** Given exact Meaning and Experience registry entries, when a query runs, then each candidate declares exactly one plane and every cross-plane relation is explicit. Given ambiguous plane metadata, then `AIR_PRIM_PLANE_AMBIGUOUS` blocks it. Failure example: an experience-flow safeguard is applied as content meaning. Evidence: query/denial receipts. Layer: schema + integration.
2. **AIR-FR-020 / AIR-ST-04.01 — exact version resolution.** Given PRM-BUS-001 ID/version/hash and current snapshot, when resolved, then the returned reference matches exact bytes and includes family, risks, relations and supersession. Given label-only or hash drift, no candidate is eligible. Failure example: the system loads a different “Perception” core move. Evidence: source lock and resolver receipt. Layer: unit + contract.
3. **AIR-FR-021 / AIR-ST-04.02 — explicit binding.** Given eligible PRM-BUS-006 and complete role/tension/stage/source context, when bound, then target, local function, effect, surface, evidence, adaptations, suppression and evaluation are explicit. Given Primitive IDs are attached after layout choice, the command is blocked. Failure example: hierarchy becomes decorative emphasis. Evidence: binding and blocker fixtures. Layer: integration.
4. **AIR-FR-022 / AIR-ST-04.02 — relation hard gates.** Given a reinforcing pair and one contextual conflict, when evaluated, then relation direction, rationale and resolution are recorded. Given an unresolved fatal conflict, no binding becomes downstream-eligible. Failure example: PRM-PSY-001 alignment and premature high-contrast conflict are averaged into a pass. Evidence: relation set and denial. Layer: domain + evaluator.
5. **AIR-FR-023 / AIR-ST-04.03 — stage coverage.** Given category/archetype requirements for source activation, script, composition, experience and evaluation, when coverage runs, then every applicable dimension passes or has a typed failure. Given a required dimension is marked N/A, `AIR_PRIM_NA_REQUIRED_DIMENSION` blocks acceptance. Evidence: coverage matrix and evaluation receipt. Layer: contract + integration.
6. **AIR-FR-024 / AIR-ST-04.03 — complete receipt.** Given all gates pass, when AIR accepts a binding, then the receipt records registry/snapshot, exact version/hash, applicability, source evidence, exclusions, relation/risk decisions and downstream consumers. Given a missing exclusion or consumer, commit fails atomically. Evidence: receipt hash and fault-injection trace. Layer: repository integration.
7. **FR-169 / ST-12.05 — Pipeline query boundary.** Given Pipeline supplies source evidence, role/tension, archetype/category, Brand Context and stage, when it queries AIR, then it receives eligible/rejected exact refs and rationales without rebuilding meaning. Given Pipeline sends a chosen visual recipe and requests matching Primitive IDs, AIR rejects it. Failure example: primitives become post-hoc labels. Evidence: producer/consumer conformance receipt. Layer: cross-product integration.
8. **FR-170 / ST-12.05 — complete candidate binding.** Given a selected candidate, when AIR creates a binding, then plane, family, role, activation reason, source evidence, suppression, conflicts, misuse and evaluation targets are explicit. Given source evidence is generic notes, `AIR_PRIM_CONTEXT_INCOMPLETE` blocks it. Evidence: schema and handoff receipts. Layer: contract + integration.
9. **CBAR active Primitive preservation.** Given PRM-BUS-001, PRM-BUS-006 or PRM-PSY-001, when used in its controlling Story, then its exact source core move and applicable misuse/suppression evidence are loaded. Given only the name/summary is supplied, no binding passes. Failure example: arbitrary emphasis, visual noise or performative matching survives. Evidence: exact YAML hashes and adversarial fixtures. Layer: reference-slice evaluation.
10. **Independent evaluation.** Given deterministic checks pass and a distinct evaluator passes the exact hash, when eligibility is requested, then transition may proceed. Given producer/evaluator identities match, `AIR_PRIM_SELF_EVALUATION` blocks it. Failure example: fluent producer output approves itself. Evidence: actor/evaluator receipt pair. Layer: architecture + integration.
11. **Idempotency and atomic rollback.** Given the same command twice, when handled, then one artifact and one stored receipt exist. Given a receipt write fails, binding, relations, edges and command record are all absent. Failure example: stored binding has no trust receipt. Evidence: transaction trace. Layer: repository integration.
12. **Supersession and selective recovery.** Given a Primitive version is superseded, when dependency traversal runs, then referencing bindings/descendants become stale while unrelated bindings and all historical versions remain replayable. Failure example: global invalidation or silent use of stale bytes. Evidence: invalidation graph and replay hashes. Layer: recovery.
13. **Migration and portability.** Given an unambiguous legacy binding, when migrated in a clean checkout, then a new artifact cites source bytes and decision and hashes identically across paths/processes. Given plane/version is missing or an absolute path leaks, migration blocks. Evidence: migration and clean-room matrices. Layer: migration + portability.
14. **Claim ceiling.** Given all writing-time structure checks pass while ratification is pending, when status is projected, then this spec remains `WRITTEN_PENDING_AUDIT`, `CANDIDATE_NOT_CURRENT`, build false, and later acceptance cannot exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. Failure example: a Development Capsule is issued. Evidence: lifecycle validation. Layer: architecture.

## 10. Testing and completion evidence

Future authorized implementation must create:

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_primitive_version_reference.py`: plane/family/version/hash/supersession and strict-field cases.
- `.../tests/unit/domain/test_primitive_binding.py`: local function, evidence, adaptation, relation and misuse invariants.
- `.../tests/unit/serialization/test_primitive_canonical_hash.py`: key order, set order, Unicode, time, random state, environment and machine-path independence.
- `.../tests/contract/test_primitive_schemas.py`: valid, missing, unknown, contradictory, N/A and stale fixtures.
- `.../tests/integration/test_primitive_query_and_binding.py`: AIR-FR-019–024 and AIR-ST-04.01–04.03.
- `.../tests/integration/test_pipeline_primitive_handoff.py`: FR-169/170 and ST-12.05 producer/consumer boundary.
- `.../tests/integration/test_primitive_atomic_commit.py`: duplicate/conflicting command, optimistic concurrency and injected partial-write failure.
- `.../tests/architecture/test_primitive_product_boundaries.py`: AIR ownership, Pipeline no-reinterpretation, independent evaluator, Studio projection only.
- `.../tests/evaluation/test_primitive_coverage_and_misuse.py`: exact active YAMLs, fatal conflict, required N/A denial, no threshold invention.
- `.../tests/migration/test_primitive_v2_to_v21.py`: unambiguous mapping and ambiguity blocker without invention.
- `.../tests/recovery/test_primitive_replay_and_invalidation.py`: byte-identical replay, descendant-only invalidation, rollback and late results.
- `.../tests/clean_environment/test_primitive_portability.py`: no absolute paths, filesystem-order or process-environment dependence.
- affected regression `tests/test_v21_primitive_archetype_invariants.py`, unchanged, plus TS-AIR-001 public-contract conformance pinned to the accepted successor hash.

Completion evidence requires generated schemas/fixtures, full suite twice in fresh processes, Python compilation/type checks, exact Primitive snapshot/file hash matrix, canonical serialization vectors, query and binding receipts, conflict/misuse/coverage report, independent evaluator receipt, atomicity/concurrency trace, migration report, replay/invalidation report, cross-product conformance report, clean-environment proof, and an independent audit by an agent other than this writer.

A future Build Receipt must bind ratified authority, accepted TS-AIR-001 and TS-AIR-004 hashes, exact Development Capsule, source snapshot, implementation/test commit, evaluator profile, migration evidence and maximum claim. This document issues none. Final writer state: `WRITTEN_PENDING_AUDIT`; authority `CANDIDATE_NOT_CURRENT`; specification work authorized; build authority false; later acceptance ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
