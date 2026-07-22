---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-DEL-001
title: Source-Grounded Visual Asset Demand, Asset Result, Geometry, and Usage Acknowledgement
product: Atomic Harness Pipeline
version: 2.1.0-candidate
date: 2026-07-22
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 12
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_C_EXTERNAL_PRODUCT_BOUNDARY
controlling_frs: [FR-085, FR-086, FR-090]
controlling_stories: [ST-08.01]
upstream_draft_dependencies:
  - {spec_id: TS-AHP-002, quality_state: WRITTEN_PENDING_AUDIT, sha256: 3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
  - {spec_id: TS-AIR-017, quality_state: WRITTEN_PENDING_AUDIT, sha256: 0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81, label: DRAFT_DEPENDENCY_NOT_ACCEPTED}
---

# TS-DEL-001 - Source-Grounded Visual Asset Demand, Asset Result, Geometry, and Usage Acknowledgement

This specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`. This document does not make candidate authority current, authorize implementation, create or alter Delegation release bytes, issue a Development Capsule, authorize VAE Stage 5, or grant build, production, publication, evaluator-certification, Format 02, or product-certification authority.

`TS-AHP-002` and `TS-AIR-017` are hash-pinned upstream drafts in `WRITTEN_PENDING_AUDIT`. Each is `DRAFT_DEPENDENCY_NOT_ACCEPTED`: its interface is admitted for dependency-safe writing but is not represented as ratified or accepted law. A hash change reopens sections 3, 5, 6, 8, 9, and 10.

## 1. Files and authorities read

### 1.1 Packet, lifecycle, and authority inputs

| Class | Exact path | State / bytes / SHA-256 | Fact used |
|---|---|---|---|
| Writer law | `CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/CONSCIOUS_ACTIVATIONS_SPECS_WORKFLOW_V3_3/skills/CA_TECH_SPEC_WRITE_SKILL.md` | V3.3; 9,624; `191d8d1b7fc41aef94a366a79f632c65a8c2d1af7a7030c8bfc3a29dc81d4520` | One-spec scope, ten required sections, claim ceiling, receipts, and draft-dependency law. |
| Recovery packet | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | 316,012; `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | Packet `CA-P03-WRITE-TS-DEL-001-RECOVERY` freezes path, product, FRs, Story, wave, and two interface dependencies. |
| Wave lock | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/PROMPT_03_FACTORY_RUN/wave-receipts/WAVE_12_DISPATCH_LOCK.yaml` | `DISPATCHED`; 2,678; `96f655bbf67a40a38a5cf233cfa9ad3f954466a8dae80ff68dfa87a2a5c9e5a7` | Freezes the exact upstream states and hashes. |
| Assignment | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/planning/spec_assignments/TS-DEL-001.md` | 3,364; `742dbfd7e56b5608c11fb25d254d071ef128615088f0056b5725cbcc628b8927` | Fixes the visual-demand/result/geometry/usage boundary and Story `ST-08.01`. |
| Controlling feature | `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/prd/features/F15-visual-asset-editor-delegation-and-gnm-boundary-integration.md` | 18,207; `eb65e84b126369a3067464a0dc9bd7c0dec72ebd168111cdb7f1fdef69333f44` | FR-085/086/090: immutable source-grounded demand, result/geometry admission, and acknowledgement before composition. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | 134,201; `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Required sources are available; `SRC-AM-002` is deferred and cannot support an attributed claim. |

The target path has no applicable repository-root or ancestor `AGENTS.md`. VAE and Delegation `AGENTS.md` were read because their repositories supply boundary evidence; neither repository is modified by this writer.

### 1.2 Admitted upstream drafts

| Edge | Exact path | State / bytes / SHA-256 | Interface consumed | Revision impact |
|---|---|---|---|---|
| SDE-056 | `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-002.md` | `WRITTEN_PENDING_AUDIT`; 50,071; `3e76ee7e4ec8f3b288a58bb8b8eb886195d9ad17097c67ded613c22fbb3dccd4`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `HarnessExecutionBindingManifest`, exact external-product route, immutable semantic refs, product sovereignty, execution eligibility, idempotency, replay, and no-side-effect-before-authorization law. | Sections 3, 5, 6, 8, 9, 10. |
| SDE-057 | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-017.md` | `WRITTEN_PENDING_AUDIT`; 67,346; `0e87466a326eac865a66609d2609a1fc8006f5b32a5a847bd01e36e488363a81`; `DRAFT_DEPENDENCY_NOT_ACCEPTED` | `VisualActivationHandoff`, AIR-owned semantic intent, Pipeline-owned exact execution/VAD boundary, Feature Contracts, T/V requests, Composition Intent, and production-acceptance versus consumption-acknowledgement separation. | Sections 3, 5, 6, 8, 9, 10. |

The drafts are read-only interface inputs. This spec neither copies their schemas into a local fork nor expands their authority.

### 1.3 Product and shared-contract sources

| Source ID / class | Exact path | Bytes / SHA-256 | Fact used |
|---|---|---|---|
| `SRC-CUR-014` | `02_VISUAL_ASSET_EDITOR/prd/05-features/F05-composition-intent-image-conditioned-geometry.md` | 7,065; `10cf37d637aa85a9efa40ae236a801322025b3757825469c3923a9a8c96e49e6` | VAE checks feasibility and returns measured geometry without changing requested role/function. |
| `SRC-CUR-016` | `02_VISUAL_ASSET_EDITOR/prd/05-features/F09-visual-production-plan-ir.md` | 7,019; `db7ece2ec153f144dc55bf00fdcd96c7941f527839db90f9a4ced23536dba47a` | VAE owns the provider-neutral Visual Production Plan and provider-specific compilation. |
| `SRC-CUR-018` | `02_VISUAL_ASSET_EDITOR/prd/05-features/F14-visual-evaluation-profiles.md` | 7,179; `03bd9c1c918a4602e396095a5dd60e2b5221af0eca03bd213a588839f4db6dd8` | Deterministic validation precedes independent asset/composition/continuity/temporal evaluation; certification is separate. |
| `SRC-CUR-019` | `02_VISUAL_ASSET_EDITOR/prd/05-features/F15-repair-invalidation-reruns.md` | 6,834; `79b40d744ea93a35716224a4df6849ed33f58ecb2c63e86cc329b05def05effc` | Repairs preserve successful properties, rerun only invalidated nodes, and cannot disguise demand amendment. |
| `SRC-CUR-022` | `03_DELEGATION_PROTOCOL/README.md` | 6,910; `14b5a21b3dbdc65d07b2043ac7711625519ea192e0c88979d910c37ef28cb6b2` | Stable protocol boundary: validation, compatibility, routing, lifecycle, audit; no visual meaning or production strategy. Its RC2 banner is stale and is not used as release identity. |
| `SRC-INT-001` | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/sources/doctrine/CCP_V9_INTERVIEW_FIRST_EXPRESSION_ENGINE.md` | 43,321; `c9014d284080b0d927fc496f292f6c58220790bdb63aff70a004d8a42c997007` | Recorded human expression and extracted Expression Moments remain source evidence; the backend is deterministic and receipt-driven. |
| Deferred | `SRC-AM-002` / `PA_AM_001_SEVEN_DAY_PARALLEL_PRODUCTION_ACTIVATION_V1_1(2).zip` | `DEFERRED_REFERENCE`; `c522c93b0f980c71354ac7e22cd37b935d6273d409403c38629b42c92cd1bef2` | Retained in research backlog; no claim in this spec is attributed to it. |
| RC4 release receipt | `CMF_PROGRAM_CONTROL/02_CROSS_REPO_CONTRACTS/delegation-contracts/1.1.0-rc.4/RELEASE_RECEIPT.json` | 31,856; `042ab1ad99a4e5a4f8ff3a08c559b410db9c17cbade48ef05e92d6170dddc25f` | Package `1.1.0-rc.4`, release digest `c614a4d9...`, protocol 1.0, VAD 1.1, derivative-lock relationship 1.0, unsigned/non-production. |
| RC4 compatibility | `.../1.1.0-rc.4/compatibility/manifest.json` | 11,223; `51667cd6c346c6794c2b648d0369b6961fc9519fd2d5e52ac03589a2a24d32cd` | Semantic compatibility, lossless adapters, required preserve/enforce/evaluate modes, and portable derivative-lock enforcement. |
| RC4 VAD schema | `.../1.1.0-rc.4/contracts/schemas/visual-asset-demand.schema.json` | 48,815; `d23cdfd520538adc0d7769e7fefa9a9cf8af63880446efd8a8c95d5dbfb67c5e` | Closed `visual-asset-demand@1.1` field names, owners, conditionals, composition, semantic lineage, Feature Contract and lock fields. |
| RC4 result schema | `.../1.1.0-rc.4/contracts/schemas/asset-result-contract.schema.json` | 17,506; `ab7dc74b92c77e5ccb487f034fea96941f1c7f41fb659e6ee6e99b96bc3fb877` | VAE-owned result identity, exact demand, artifact, completion, provenance and evaluation findings. |
| RC4 acknowledgement schema | `.../1.1.0-rc.4/contracts/schemas/result-acknowledgement.schema.json` | 13,849; `f1d59cac8c3fc4f4ab3f584460978652f364c84ec8a9c36d422ff1d9161bb88d` | Content Harness/Pipeline-owned decision and `consumption_authorized`. |
| RC4 lock schema | `.../1.1.0-rc.4/contracts/schemas/derivative-lock-inheritance.schema.json` | 26,033; `a1b8ca8c2fdcc67719b141c4feca93527553f821dc62cc9648f62f295d440d08` | Portable parent evidence, derivation classification, exact/stricter lock comparison, and authorized-new-demand relaxation. |

VAE integration declarations were also read: exact RC4 pin `779679fb...`, compatibility `66d22de2...`, boundary manifest `bc6c0e28...`, inbound request mapping `8d13ffc1...`, outbound result mapping `b64853e7...`, and derivative mapping `e953c288...`. They confirm lossless mapping, no shared-schema fork, required `EVALUATE` capability, evaluator `specified_not_certified`, and production false.

## 2. Problem, user outcome, solution, and scope

### 2.1 Concrete failure and desired outcome

A Pipeline can possess a correct AIR handoff and still lose trust at the visual boundary. Common failures include a demand with a guessed source kind, missing interview provenance, flattened semantic lineage, a provider hint that displaces Composition Intent, a derivative crop that omits parent-lock evidence, a beautiful result unrelated to the requested demand, or a production-accepted asset that is consumed without verifying geometry, artifact integrity, evaluation, lifecycle, and supersession. Because Delegation messages are syntactically valid, such failures can be hidden behind a successful parse or transport receipt.

The required outcome is one deterministic, inspectable chain:

`eligible AIR handoff + eligible Harness binding -> immutable Pipeline Visual Asset Demand -> Delegation validation/routing -> VAE plan/production/evaluation/acceptance -> immutable Asset Result + geometry/evaluation evidence -> Pipeline conformance decision -> Result Acknowledgement -> exact composition binding`.

Every transition preserves identity, owner, source provenance, semantic lineage, category/profile, Feature Contracts, Composition Intent, wrong-reading locks, evaluator state, and lifecycle-at-use. An attractive but untraceable asset blocks composition.

### 2.2 Bounded solution

The Pipeline validates exact upstream refs and an eligible `HarnessExecutionBindingManifest`, compiles a closed `PipelineVisualDemandSourceSet`, maps it losslessly into the externally owned RC4 `visual-asset-demand@1.1`, validates it locally with the exact released validators, and submits it through a transport port bound to Delegation. It persists the demand bytes, release pin, submission/admission receipts, idempotency identity, and dependency edges atomically.

When VAE returns `asset-result-contract@1.0`, the Pipeline validates the released schema, exact request/version, VAE owner, artifact hash and media facts, completion/limitations, production/evaluation evidence, required image-conditioned geometry, Feature Contract realization, derivative-lock evidence, and current lifecycle. It then emits the externally owned `result-acknowledgement@1.0`. Only an acknowledgement with an eligible decision and `consumption_authorized: true` may create a Pipeline-owned `ProductionAssetBinding` consumed by composition. Production acceptance alone is insufficient.

### 2.3 In scope

- FR-085, FR-086, FR-090 and ST-08.01;
- exact RC4 package/profile/schema/hash pin and semantic capability negotiation;
- demand compilation from exact upstream semantic and execution refs;
- governed source-kind and interview-expression provenance enforcement;
- Activative Intelligence, Identity DNA, Context Premise, Resonance, Matrix/Edge Product, Activative Call, Reaction Receipt and Expression Moment lineage;
- Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, T/V route, Composition Intent, identity continuity, reference evidence and wrong-reading locks;
- portable derivative-lock inheritance relationship compilation/validation;
- submission, admission, asynchronous result correlation, partial-result treatment, constraint conflict, amendment proposal, cancellation, supersession, invalidation, revocation and replacement;
- VAE result, evaluation, geometry and artifact conformance;
- separate downstream acknowledgement, asset binding, selective invalidation and historical replay;
- deterministic identity, atomicity, idempotency, optimistic concurrency, portability and typed observability.

### 2.4 Out of scope and non-goals

- compiling or revising AIR semantic meaning, Final Script, Composition Intent or Feature Contract intent;
- owning interview source, Reaction Receipt or Expression Moment evidence;
- choosing VAE workflow, provider, model, LoRA, conditioning, candidate, repair method, production acceptance or delivery strategy;
- interpreting or creatively repairing payload meaning in Delegation;
- creating a local fork of RC4 schemas, generated types, validators, fixtures, migrations or release bytes;
- VAE Stage 5, provider execution, real compute, evaluator certification, Format 02 activation, production trust/publication, or product certification;
- generic creative-safety/content-rights approval authority. Operator source authority, provenance, lineage, technical security and product sovereignty remain explicit.

## 3. Governing decisions and constraints

### 3.1 Authority and claim ceiling

1. Current Constitution V1.1 and current product PRDs remain binding. V2.1 candidate authority and both upstream specs are admitted only for authorized specification work.
2. Candidate ownership records may define the intended interface but do not authorize current adoption, implementation, release publication or production use.
3. This document remains `WRITTEN_PENDING_AUDIT`, authority `CANDIDATE_NOT_CURRENT`, build false, and later pre-ratification ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
4. The Delegation README's RC2 banner conflicts with current release/status evidence. Stable protocol boundary statements are used; release identity is taken from immutable Program Control RC4 bytes and current status exports. Independent audit must verify this explicit resolution.

### 3.2 Product sovereignty

- AIR owns semantic lifecycle and production-program meaning, including semantic intent, Activative purpose, Composition Intent, Feature Contract intent, T/V route request and wrong-reading locks.
- Interview Expression owns live source, transcript/media evidence, Reaction Receipts, Expression Moments and source authorization.
- Builder owns `AtomicHarnessDefinition`; Pipeline consumes an exact eligible definition/binding without becoming Builder.
- Pipeline owns exact category-native execution, authoritative immutable Visual Asset Demand emission, result conformance for downstream use, consumption acknowledgement, composition binding, run state and execution receipts.
- VAE owns Visual Production Plan, route, workflow/model/LoRA/conditioning choice, candidate generation, production evaluation, bounded repair, production acceptance, asset lineage and delivery.
- Delegation owns contract validation, authority enforcement, compatibility negotiation, lifecycle projection, idempotency/replay protection, immutable routing, audit receipts and shared failure semantics. It owns no creative meaning and cannot rewrite a payload.
- Studio projects state and issues typed correction/amendment commands; it does not mutate canonical objects through UI state.
- `Activative Contract Compiler != Activative Intelligence Runtime`.

### 3.3 Shared release and compatibility law

The only active dependency is `delegation-contracts@1.1.0-rc.4`, release digest `sha256:c614a4d9b705e382456f4d6cd1cd6b7bcbc892517a22b358950db7404e3b4c44`, release receipt `042ab1ad...`, manifest `7a23c089...`, profile `cmf-delegation-compatibility-profile-1-0@1.0`, protocol 1.0, VAD 1.1, and derivative-lock relationship 1.0. Trust is `local_unsigned_release_candidate`; production eligibility is false.

Compatibility is semantic. Parse success without required preserve/enforce/evaluate behavior fails. The Pipeline negotiates exact required features and modes; it cannot silently downgrade evaluation, source provenance, lineage, Feature Contracts, T/V, Composition Intent, locks or derivative evidence. Active delegations remain pinned to the versions negotiated at admission. RC1-RC3 may appear only as historical rejection/migration evidence.

### 3.4 Source and lineage law

`source_provenance.source_kind` is mandatory and owned upstream. Allowed RC4 values are `interview_expression`, `public_comment`, `direct_message_reply`, `authored_source`, `live_premise`, `research_synthesis`, `operator_supplied`, and `legacy_migrated`. Unknown or ambiguous values fail; Pipeline, Delegation and VAE do not guess.

For `interview_expression`, at least one non-empty `reaction_receipt_refs` and at least one non-empty `expression_moment_refs` are required. For non-interview kinds they are optional but validated when supplied; migrations never invent them. Required lineage is represented by typed exact refs or exact RC4 fields, never generic notes. Epistemic state and source owner cannot be promoted by downstream processing.

### 3.5 Composition, Feature Contract and evaluation law

AIR owns semantic Composition Intent; Pipeline compiles exact composition execution and emits the VAD; VAE may adjust realized geometry only within declared tolerance or request amendment. VAE cannot accept its own out-of-tolerance semantic change. Feature Contract intent remains upstream-owned and immutable; VAE owns feasibility/realization findings. Pipeline verifies exact references and realization evidence but does not duplicate visual evaluation.

RC4 requires `EVALUATE` modes for the applicable semantic domains. VAE currently declares capability based on specification and deterministic contract tests, while evaluator state remains `specified_not_certified`. Capability presence does not imply certification. Unsupported required evaluation profiles fail compatibility; no threshold is invented to force readiness.

### 3.6 Wrong-reading-lock and derivative law

Generative, composited, restyled or semantically transformative demands carry non-empty wrong-reading locks. Every deterministic or non-semantic derivative inherits all parent locks; every semantic derivative also preserves them unless a new authorized upstream demand version explicitly changes the authoritative set. A derivative may add stricter locks but may not remove, reinterpret, narrow scope, change meaning hash, or reduce enforcement strength.

Every derivative relationship supplies the RC4 fields `authoritative_parent_ref`, `parent_contract_version`, `governing_authoritative_demand_ref`, `parent_lock_evidence`, `derivative_ref`, `derivative_wrong_reading_locks`, `derivation_type`, `derivative_semantics`, and `authoritative_lock_authorization`. Missing parent evidence or guessed derivation class fails before composition.

### 3.7 Determinism and security

Canonical identity excludes wall clock, random state, process environment, absolute machine paths, filesystem traversal order and dictionary insertion accidents. Timestamps are evidence-only. External refs are version/hash pinned. Secrets and private source content are not copied into logs. Transport authentication/signing is an operational Delegation concern; current unsigned RC4 cannot be represented as production-trusted.

## 4. Current brownfield architecture

| Exact artifact | Observed behavior | Disposition | Constraint |
|---|---|---|---|
| RC4 `visual-asset-demand.schema.json` | Closed shared VAD 1.1 with Content Harness-owned semantic fields and source-kind conditional enforcement. | `REUSE_EXTERNALLY_OWNED` | Consume released bytes; no Pipeline-local fork or field renaming. |
| RC4 `asset-result-contract.schema.json` | Closed VAE-owned result with exact demand/execution, artifact, partial status, provenance and evaluation findings. | `REUSE_EXTERNALLY_OWNED` | Geometry is conveyed by typed referenced evidence, not by adding a Pipeline field to the shared schema. |
| RC4 `result-acknowledgement.schema.json` | Content Harness-owned decision and `consumption_authorized`. | `REUSE_EXTERNALLY_OWNED` | Acknowledgement is downstream consumption authority, not duplicate production evaluation. |
| RC4 `derivative-lock-inheritance.schema.json` and validator | Portable parent-evidence and lock-strength enforcement introduced in RC4. | `REUSE_EXTERNALLY_OWNED` | Invoke exact validator; parsing the relationship is insufficient. |
| `02_VISUAL_ASSET_EDITOR/contracts/integration/VISUAL_ASSET_DEMAND_REQUEST_MAPPING.yaml` | Exact-name/value immutable mapping of all VAD fields; source conditionals and no synthesis. | `VERIFY_CONSUMER_CONFORMANCE` | Pipeline emitted bytes must be consumable without adapter loss. |
| `02_VISUAL_ASSET_EDITOR/contracts/integration/ASSET_RESULT_MAPPING.yaml` | VAE result maps feature realization and derivative evidence through provenance/evaluation refs; cannot grant consumption. | `VERIFY_PRODUCER_CONFORMANCE` | Pipeline must resolve the referenced resources and exact demand identity. |
| VAE local `ASSET_RESULT_CONTRACT.schema.yaml` | Older local projection includes `composition_geometry_ref` and `authorized_for_composition`. | `HISTORICAL_OR_INTERNAL_ONLY` | Shared RC4 result is canonical at boundary; local `authorized_for_composition` must not grant downstream authority. |
| VAE `PROGRAM_STATUS_EXPORT.yaml` | RC4 bounded integration passes; evaluator `specified_not_certified`; Stage 5 unauthorized; production false. | `PRESERVE_STATUS_TRUTH` | No design or synthetic fixture may upgrade readiness. |
| Delegation `PROGRAM_STATUS_EXPORT.yaml` | RC4 current local unsigned, frozen, locally validated, production false. | `PRESERVE_STATUS_TRUTH` | Release bytes remain immutable. |
| Delegation `README.md` | Stable boundary doctrine but stale RC2 banner/validation command. | `USE_BOUNDARY_ONLY_RECORD_CONFLICT` | Do not use its banner as active identity or rewrite it in this prompt. |
| `TS-AHP-002` | Candidate Pipeline intake/binding interface with exact external-product route and no semantic overrides. | `ADMIT_DRAFT_INTERFACE` | Hash-pinned, non-accepted, sections reopened on change. |
| `TS-AIR-017` | Candidate visual handoff and ownership boundary. | `ADMIT_DRAFT_INTERFACE` | Hash-pinned, non-accepted, no claim of ratified authority. |

There is no authorized Pipeline implementation for this specification. Brownfield VAE and Delegation artifacts are evidence and external interfaces, not code to import or modify.

## 5. Proposed architecture and workflows

### 5.1 Components and responsibility boundaries

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `VisualDemandSourceAdmitter` | Admit exact eligible AIR handoff, Builder binding, source package, category/profile and authority snapshots. | Reconstructing missing semantic or interview meaning. |
| `VisualAssetDemandCompiler` | Compile Pipeline-owned demand identity and exact RC4 VAD payload from admitted refs. | Selecting VAE provider/workflow/model or changing Composition Intent. |
| `DelegationReleaseRegistry` | Resolve exact package/profile/schema/generated-type/validator hashes and trust state. | Treating a mutable README or latest alias as a release pin. |
| `DemandSemanticConformanceValidator` | Run RC4 schema, authority, source conditional, lineage, profile, Feature Contract, T/V and lock validation. | Parse-only compatibility or default inference. |
| `DerivativeLockRelationshipCompiler` | Emit portable parent evidence and classify the derivative from authoritative execution facts. | Guessing classification or authorizing lock relaxation. |
| `DelegationSubmissionPort` | Submit immutable envelope/payload and receive admission/audit/lifecycle messages. | Interpreting creative meaning or bypassing Delegation receipts. |
| `VisualDelegationRepository` | Atomically persist command, demand, pins, receipts, events, edges, idempotency and current projections. | Orphan state/receipt or destructive history rewrite. |
| `AssetResultAdmitter` | Validate exact result schema/owner/demand/artifact/provenance/lifecycle. | Treating VAE production acceptance as downstream use. |
| `GeometryEvidenceResolver` | Resolve VAE-owned geometry evidence: subject/face/hands/gesture/object/focal BBOXes, masks, vectors, negative space, crops, depth/layers and collisions as applicable. | Fabricating unavailable geometry or moving semantics outside tolerance. |
| `FeatureAndLockRealizationVerifier` | Check exact Feature Contract refs, evaluation findings, derivative ancestry and wrong-reading evidence. | Mutating authoritative Feature Contracts or recertifying the evaluator. |
| `ResultAcknowledgementService` | Emit RC4 acknowledgement and, when authorized, an immutable Pipeline asset binding. | Duplicating VAE evaluation or granting use on stale/partial evidence. |
| `VisualDependencyInvalidationProjector` | Selectively stale affected demands, results, bindings and compositions. | Deleting history or invalidating unrelated descendants. |

### 5.2 Demand compilation workflow

1. `CompileVisualAssetDemandCommand` names the exact `HarnessExecutionBindingManifest`, `VisualActivationHandoff`, source package, Composition IR context, category/profile, RC4 release pin, budget authorization, actor and expected aggregate version.
2. Admission verifies owner, lifecycle-at-use, version/hash, source kind, interview provenance condition, semantic lineage, category/profile support, Feature Contracts, evaluation profile, Composition Intent, identity continuity, reference evidence and inherited locks.
3. Compiler creates `PipelineVisualDemandSourceSet`; it cannot replace exact refs with prose. The source set binds every RC4 field to its upstream owner and pointer.
4. Compiler emits canonical RC4 `visual-asset-demand@1.1`. `request_id` and `version` are immutable; `supersedes` is explicit; all required top-level fields are present. No VAE plan/provider field is permitted.
5. If the requested asset is a derivative, the relationship compiler emits `derivative-lock-inheritance@1.0` using authoritative parent evidence and the exact released validator. Exact or stricter inheritance alone passes.
6. Compatibility negotiation checks RC4 package/profile/protocol/message versions and semantic capability modes. Missing `EVALUATE`, unsupported profile, or parse-only support blocks before submission.
7. Repository atomically commits command, VAD canonical bytes/hash, release/schema/validator pins, relationship if applicable, dependency edges, outbox message, compilation receipt and idempotency record.
8. Delegation returns submission/admission/audit receipts and lifecycle events. The Pipeline records them without changing payload meaning.

### 5.3 Result admission and composition workflow

1. `RegisterVisualAssetResultCommand` supplies exact RC4 envelope/result bytes, Delegation audit trail, VAE production acceptance evidence, artifact bytes or immutable content ref, and expected delegation aggregate version.
2. Validator checks schema, envelope/message/package pin, principal/owner, exact demand identity, current lifecycle, result version, execution identity, artifact hash/media/dimensions, completion status, unresolved roles, cost/attempts, provenance and evaluation findings.
3. `GeometryEvidenceResolver` resolves the typed VAE-owned geometry resource referenced by result provenance. Required geometry is conditional on asset family, role, Composition Intent and downstream composition profile. Missing applicable geometry blocks; it is not `NOT_APPLICABLE` by omission.
4. Feature/lock verifier checks exact Feature Contract refs and realization findings, wrong-reading outcomes, derivative RC4 validator evidence, requested-versus-realized geometry, tolerance consumption, composition-context evaluation and evaluator identity/profile state.
5. If status is `PARTIAL`, every unresolved role and downstream impact is explicit. Partial output may be retained or used only when the original demand/profile explicitly permits partial consumption and all remaining hard gates pass; otherwise acknowledgement rejects consumption.
6. `AcknowledgeVisualAssetResultCommand` compares exact demand/result, eligible lifecycle, geometry, evaluation, limitations, supersession and artifact integrity. It emits `result-acknowledgement@1.0` with `ACCEPTED`, `ACCEPTED_WITH_CONCERNS`, or `REJECTED` and an explicit `consumption_authorized` boolean.
7. Only `consumption_authorized: true` atomically creates `ProductionAssetBinding` for the exact Composition IR node/sequence. Acknowledgement does not redo VAE aesthetic judgment; it checks downstream contract fitness and freshness.
8. Composition emits a later syntax/usage receipt referencing demand, result, acknowledgement, asset binding and exact rendered use. It does not mutate the VAE result.

### 5.4 Conflict, amendment, cancellation and repair workflow

- VAE infeasibility returns `constraint-conflict@1.0` with evidence and nonbinding options. The original demand remains immutable.
- A semantic, identity, out-of-tolerance geometry, lock or category/profile change requires `amendment-proposal@1.0` and upstream owner authorization. Pipeline cannot approve an AIR-owned semantic change; VAE cannot approve its own proposal.
- VAE-internal route/workflow/model/control changes within demand freedoms create new VAE plan versions, not demand versions.
- Repair uses a typed VAE repair contract, preserves accepted properties and reruns the smallest invalidated subgraph. Repair evidence returns through result provenance/evaluation findings.
- Cancellation is serialized by expected version. A late result is historical non-consumable evidence unless the exact lifecycle permits its registration.
- A new demand version links `supersedes`; old results/bindings become stale only through typed dependencies and remain reproducible.

### 5.5 Idempotency, concurrency, atomicity and replay

Command identity is SHA-256 over command type, canonical payload, exact upstream refs, RC4 release/profile/schema pins and expected aggregate version. Identical retry returns the stored receipt. Same idempotency key with different canonical payload fails. Optimistic concurrency permits one winner; losers reload before issuing a new command.

Demand compilation atomically commits demand, lock relationship, edges, receipt, command/idempotency and outbox. Result admission atomically commits result, resolved evidence snapshot, findings, edges, receipt and lifecycle projection. Acknowledgement atomically commits acknowledgement, authorized binding when applicable, edges and outbox. No success receipt may exist without its artifact; no current artifact may exist without its receipt.

Historical replay loads exact VAD/result/acknowledgement bytes, RC4 release validators, compatibility decision, source/handoff/binding refs, geometry/evaluation evidence and event versions. It never substitutes `latest`, current evaluator thresholds, mutable paths or rebuilt source meaning.

## 6. Data models, contracts, schemas, and APIs

All Pipeline-owned objects are immutable, closed, versioned and canonically serialized. Externally owned RC4 payloads are validated against exact released bytes and retained byte-for-byte. No `Any`, untyped extension map, implied default, free-form authority override or absolute host path is allowed.

### 6.1 External contract identities

| Contract | Version / schema | Value owner | Pipeline behavior |
|---|---|---|---|
| Delegation package | `delegation-contracts@1.1.0-rc.4`, digest `c614a4d9...` | Delegation Protocol | Exact unsigned local pin; never copied or mutated. |
| Envelope | protocol `1.0` | Delegation Protocol | Validate identity, type, principal, integrity, causation and replay semantics. |
| Visual Asset Demand | `visual-asset-demand@1.1`, schema `https://contracts.cmf.dev/delegation/visual-asset-demand/1.1/schema.json` | Content Harness / Pipeline for values; Delegation for contract | Compile exact shared payload and preserve canonical bytes. |
| Derivative lock relationship | `derivative-lock-inheritance@1.0` | Signing principal/upstream authority for values; Delegation for contract | Compile or admit exact evidence and invoke released behavior. |
| Asset Result | `asset-result-contract@1.0` | VAE for values; Delegation for contract | Validate and admit without adding consumption authority. |
| Result Acknowledgement | `result-acknowledgement@1.0` | Content Harness / Pipeline for values; Delegation for contract | Emit downstream decision and explicit authorization. |

### 6.2 `DelegationContractPin` - `ca.pipeline.delegation-contract-pin/1.0.0-candidate`

Required fields: `package_name`, `package_version`, `release_digest`, `release_receipt_sha256`, `release_manifest_sha256`, `compatibility_manifest_sha256`, `compatibility_profile_id`, `compatibility_profile_version`, `compatibility_profile_sha256`, `protocol_version`, typed `message_versions`, typed `schema_refs`, typed `generated_binding_refs`, typed `validator_refs`, `signature_status`, `trust_status`, `production_eligible`, `production_authorized`, `pinned_at`, and `content_sha256`.

For this spec the signature is `UNSIGNED`, trust is `local_unsigned_release_candidate`, and both production booleans are false. `pinned_at` is evidence-only. Any release identity mismatch fails; no mutable directory name alone is sufficient.

### 6.3 `PipelineVisualDemandSourceSet`

Required fields are `source_set_id`, `harness_binding_ref`, `visual_activation_handoff_ref`, `source_package_refs[1..n]`, `source_kind`, conditional `reaction_receipt_refs`, conditional `expression_moment_refs`, `activative_intelligence_pack_ref`, `identity_dna_ref`, `context_premise_ref`, `resonance_map_ref`, `matrix_edge_product_ref`, `activative_call_refs[1..n]`, `source_evidence_refs[1..n]`, `activation_contract_ref_or_projection`, `visual_semantic_pack_ref_or_projection`, `visual_narrative_program_ref_or_projection`, `feature_contract_refs[1..n]`, `somatic_route_request_ref_or_projection`, `composition_intent_ref`, `identity_continuity_refs`, `reference_evidence_refs[1..n]`, `evaluation_profile_ref`, `budget_authorization_ref`, `wrong_reading_lock_set_ref`, `category_profile_ref`, `format_profile_ref`, `authority_snapshot_ref`, `limitations`, and `content_sha256`.

Every field records `value_owner`, `source_pointer`, exact version/hash and lifecycle-at-use through its typed ref. Projection is permitted only where RC4 embeds a closed value object rather than a resource ref; the source ref remains alongside it. Missing values are blocked, not flattened into `notes`.

### 6.4 RC4 `VisualAssetDemand` compilation

The compiler emits all required RC4 top-level fields exactly: `request_id`, `version`, `supersedes`, `content_harness_ref`, `category_profile`, `format_profile`, `asset_classification`, `source_provenance`, `activative_semantic_lineage`, `activation_contract`, `semantic_intent`, `visual_semantic_pack`, `visual_narrative_program`, `feature_contracts`, `somatic_route_request`, `activative_function`, `wrong_reading_locks`, `composition_intent`, `identity_continuity`, `reference_evidence`, `delivery`, `evaluation_policy`, `execution_policy`, and `notes`.

Important cross-field rules:

- `source_provenance.source_kind` is one governed enum and never inferred;
- interview expression requires non-empty Reaction Receipt and Expression Moment refs; other kinds permit omission but forbid synthesis;
- `activative_semantic_lineage` preserves AIP, Identity DNA, Context Premise, Resonance Map, Matrix/Edge Product, Activative Calls and source evidence;
- each Feature Contract has exact `contract_ref`, `feature`, and `required_for_meaning` and remains upstream-owned;
- T and V codes plus intended body effect remain explicit;
- Composition Intent owns exact canvas, intended region, tolerance, layer role, visual weight, reserved regions and gaze direction at the shared boundary;
- `wrong_reading_locks` is non-empty; a derivative relationship adds portable ancestry evidence rather than replacing the demand locks;
- `evaluation_policy.profile_ref`, maximum rounds and hard gates are explicit; capability compatibility is checked before submission;
- `notes` may carry nonauthoritative limitations only and cannot substitute for any required field.

### 6.5 `DerivativeLockBinding`

Pipeline stores the exact RC4 relationship bytes plus `validator_ref`, `validator_result`, `validated_parent_lock_set_hash`, `validated_derivative_lock_set_hash`, and `validated_at`. The RC4 payload's required fields are preserved verbatim. `validated_at` is evidence-only.

Valid outcomes prove every parent lock by `lock_id`, `meaning_hash`, `scope_paths`, and `enforcement_level`; additions are stricter. Invalid outcomes include `PARENT_LOCK_REMOVED`, `PARENT_LOCK_WEAKENED`, `PARENT_LOCK_EVIDENCE_REQUIRED`, `DERIVATION_CLASSIFICATION_REQUIRED`, and `UNAUTHORIZED_LOCK_RELAXATION`. For semantic relaxation, `authoritative_lock_authorization` points to a new authoritative demand and evidence; it never authorizes in-place mutation.

### 6.6 `AssetResultAdmission`

Required fields: `admission_id`, `delegation_contract_pin_ref`, `envelope_ref`, `result_ref`, `result_bytes_sha256`, `demand_ref`, `execution_ref`, `producer_principal_ref`, `artifact_ref`, `artifact_bytes_sha256`, `artifact_media_type`, `artifact_width_px`, `artifact_height_px`, `completion_status`, `unresolved_roles`, `provenance_refs`, `evaluation_findings`, `production_acceptance_receipt_ref`, `geometry_pack_ref_or_evidenced_not_applicable`, `feature_realization_receipt_refs`, `derivative_lock_validation_ref_or_evidenced_not_applicable`, `cost_consumed`, `attempts_consumed`, `lifecycle_state_at_use`, `limitations`, `validation_findings`, `admitted_at`, and `content_sha256`.

`EvidencedNotApplicable` is `{basis_rule_ref, evaluated_condition, evidence_refs, claim_limit}`. It is not null, an empty string, or omission. Demand identity, source/semantic lineage, Composition Intent, required locks, required Feature Contracts, artifact integrity, and required evaluation can never become N/A.

### 6.7 `ImageConditionedGeometryPack`

This is a VAE-owned immutable referenced resource, not a new shared Delegation field. Required fields are `geometry_pack_id`, `asset_result_ref`, `demand_ref`, `artifact_ref`, `coordinate_profile_ref`, `canvas_profile_ref`, typed `subject_boxes`, `face_boxes`, `hand_boxes`, `gesture_boxes`, `object_boxes`, `focal_boxes`, `gaze_vectors`, `motion_vectors`, `negative_space_regions`, `safe_crops`, `mask_refs`, `depth_layers`, `collision_findings`, `requested_geometry_ref`, `realized_geometry`, `tolerance_consumption`, `detector_or_measurement_refs`, `limitations`, and `content_sha256`.

Each geometry item states applicability and confidence/evidence. Required boxes use governed basis-point or pixel coordinates tied to the exact canvas; conversions are deterministic and receipted. A missing applicable pack, mismatched artifact hash, out-of-range coordinate, unapproved out-of-tolerance relocation, removed protected region, or crop that removes required action/source evidence blocks consumption.

### 6.8 `ResultConformanceDecision` and `ProductionAssetBinding`

`ResultConformanceDecision` requires exact demand/result/admission refs, current lifecycle/supersession refs, geometry decision, artifact-integrity decision, Feature Contract realization decisions, wrong-reading/derivative decisions, evaluation-profile and evaluator-state refs, completion/limitation decision, overall result, typed findings, responsible owner per failure, and hash.

`ProductionAssetBinding` requires `binding_id`, `acknowledgement_ref`, `demand_ref`, `result_ref`, `artifact_ref`, `geometry_pack_ref`, `composition_ir_ref`, `composition_node_id`, `sequence_role`, `asset_role`, `crop_or_variant_ref`, `feature_realization_refs`, `lock_validation_ref`, `lifecycle_state_at_bind`, `limitations`, `consumption_authorized: true`, `supersedes_binding_ref_or_not_applicable`, and hash. It contains no semantic override and no provider configuration.

### 6.9 Commands, events and ports

Commands are `CompileVisualAssetDemand`, `SubmitVisualAssetDemand`, `RegisterDelegationLifecycleMessage`, `RegisterVisualAssetResult`, `AcknowledgeVisualAssetResult`, `BindProductionAsset`, `CancelVisualDelegation`, `RegisterDemandSupersession`, `RegisterPostCompletionInvalidation`, and `ReplayVisualDelegation`.

Events are `VisualAssetDemandCompiled`, `VisualAssetDemandDenied`, `DerivativeLockInheritanceValidated`, `VisualAssetDemandSubmitted`, `VisualAssetDemandAdmitted`, `VisualConstraintConflictRegistered`, `VisualAssetResultRegistered`, `VisualAssetResultDenied`, `VisualAssetResultAcknowledged`, `ProductionAssetBound`, `VisualDemandSuperseded`, `ProductionAssetBindingInvalidated`, `VisualResultRevoked`, and `VisualDelegationReplayVerified`.

Public ports are typed: `VisualDemandCommandPort`, `DelegationTransportPort`, `DelegationLifecycleReadPort`, `AssetResultCommandPort`, `GeometryEvidencePort`, `VisualAcknowledgementPort`, `ProductionAssetBindingReadPort`, and `VisualDelegationHistoryPort`. Adapters depend on exact released external contracts and local ports; they do not import VAE or Delegation internal modules.

### 6.10 Canonical serialization, compatibility and migration

Canonical JSON is UTF-8, Unicode NFC, lexicographically ordered object keys, no insignificant whitespace, no NaN/Infinity, fixed integer units, and one terminal newline. Set-like arrays sort by full immutable identity; narrative/reading/evidence sequences retain declared order. Content identity excludes timestamps, storage paths and runtime metadata.

Adapters are lossless. They cannot drop, weaken, synthesize, flatten or reinterpret. Migrations write new immutable artifacts and a receipt with source/target hashes, field mapping, adapter/version, owner, omissions, limitations and `LOSSLESS` or `BLOCKED`. Source kind is never guessed. A predecessor that cannot supply required interview provenance, lock ancestry, Composition Intent, profile/evaluation or geometry is blocked. Historical delegations remain replayable under their accepted versions; deprecation does not rewrite them.

## 7. Implementation stages and exact target paths

The following are future targets only. They require ratified/adopted authority, independent spec acceptance, a bounded Development Capsule and explicit build authorization before creation.

| Stage | FR / Story | Exact future paths | Completion evidence |
|---|---|---|---|
| 0 source and release lock | all | `05_ATOMIC_HARNESS_PIPELINE/development-capsules/TS-DEL-001/SOURCE_LOCK.yaml` | Ratified authority, accepted upstream hashes, exact RC4 trust/profile/schema/validator pins. |
| 1 strict domain models | FR-085/086/090 | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/domain/visual_delegation.py`; `.../domain/visual_asset_demand.py`; `.../domain/asset_result_admission.py`; `.../domain/production_asset_binding.py` | Closed models, canonical vectors, schema/ref/owner invariants. |
| 2 release and compatibility | FR-085 | `.../compatibility/delegation_release_registry.py`; `.../adapters/delegation_rc4_contracts.py` | Exact release identity, no schema fork, semantic negotiation and parse-only denial. |
| 3 demand compile | FR-085; ST-08.01 | `.../services/visual_asset_demand_compiler.py`; `.../services/visual_demand_admission_service.py` | Full field crosswalk, source/interview conditionals, no VAE production choices. |
| 4 derivative locks | FR-085/090 | `.../services/derivative_lock_binding_service.py` | RC4 portable validator, exact/stricter pass and all negative cases. |
| 5 Delegation lifecycle | FR-085/090 | `.../services/visual_delegation_service.py`; `.../adapters/delegation_transport.py` | Submission/admission/audit, cancellation, conflict, amendment, supersession and replay. |
| 6 result and geometry | FR-086; ST-08.01 | `.../services/asset_result_admission_service.py`; `.../services/geometry_evidence_resolver.py` | Exact result correlation, artifact proof, required geometry and VAE-owned evidence. |
| 7 acknowledgement and binding | FR-090; ST-08.01 | `.../services/result_acknowledgement_service.py`; `.../services/production_asset_binding_service.py` | Production acceptance separated from consumption; stale assets blocked. |
| 8 persistence/recovery | all | `.../repositories/visual_delegation_repository.py`; `.../projections/visual_delegation.py` | Atomic parity, idempotency, concurrency, selective invalidation and historical replay. |
| 9 contracts/tests | all | `05_ATOMIC_HARNESS_PIPELINE/contracts/pipeline/visual-delegation/`; `05_ATOMIC_HARNESS_PIPELINE/tests/` | Pipeline-local schemas only; external RC4 bytes referenced, not copied. |

No source, schema, release, fixture, test or capsule path in this table is created by this writing prompt.

## 8. Failure, migration, rollback, recovery, and observability

### 8.1 Typed failures and ownership

| Code | Trigger | Responsible owner / next action |
|---|---|---|
| `PIPELINE_VISUAL_RELEASE_IDENTITY_MISMATCH` | Package/profile/schema/receipt/manifest hash differs from the exact pin. | Pipeline/Program Control; restore exact bytes or issue a separately governed release. |
| `PIPELINE_VISUAL_RELEASE_NOT_PRODUCTION_TRUSTED` | A production command uses unsigned/unpublished RC4. | Program Control/Delegation; obtain signing/publication authority. |
| `PIPELINE_VISUAL_SOURCE_KIND_REQUIRED` | Missing, unknown or ambiguous discriminator. | Upstream source/semantic owner; issue corrected immutable source/demand version. |
| `PIPELINE_VISUAL_INTERVIEW_PROVENANCE_REQUIRED` | Interview kind lacks Reaction Receipt or Expression Moment ref. | Interview Expression/AIR; provide exact evidence; no inference. |
| `PIPELINE_VISUAL_LINEAGE_FLATTENED` | Required semantic lineage reduced to notes or incomplete projection. | Upstream producer; recompile exact handoff/demand. |
| `PIPELINE_VISUAL_AUTHORITY_VIOLATION` | Pipeline mutates AIR meaning, VAE mutates demand, or Delegation interprets payload. | Violating product; deny and preserve evidence. |
| `PIPELINE_VISUAL_COMPATIBILITY_FEATURE_UNSUPPORTED` | Required preserve/enforce/evaluate mode or profile unavailable. | Consumer/product owner; supply compatible version or reject. |
| `PIPELINE_VISUAL_DERIVATIVE_PARENT_EVIDENCE_REQUIRED` | Derivative lacks portable parent-lock evidence or classification. | Derivative producer/Pipeline compiler; provide exact RC4 relationship. |
| `PIPELINE_VISUAL_WRONG_READING_LOCK_WEAKENED` | Parent lock removed, meaning/scope changed or strength reduced. | Upstream authority; new authorized demand version required for relaxation. |
| `PIPELINE_VISUAL_RESULT_IDENTITY_MISMATCH` | Result request/version/execution does not equal active demand. | VAE/Delegation producer; return correct immutable result. |
| `PIPELINE_VISUAL_ARTIFACT_INTEGRITY_FAILED` | Bytes/hash/media/dimensions differ or artifact unavailable. | VAE delivery owner; redeliver exact artifact/evidence. |
| `PIPELINE_VISUAL_GEOMETRY_REQUIRED` | Applicable geometry pack absent/incomplete/mismatched. | VAE; return measured geometry or conflict. |
| `PIPELINE_VISUAL_GEOMETRY_OUT_OF_TOLERANCE` | Realized geometry violates authoritative tolerance/protected region. | VAE proposes amendment; upstream owner decides. |
| `PIPELINE_VISUAL_EVALUATION_INCOMPLETE` | Required deterministic/VLM/composition/Feature/lock evidence absent or profile unsupported. | VAE evaluation owner; provide valid evidence; Pipeline does not invent pass. |
| `PIPELINE_VISUAL_EVALUATOR_NOT_CERTIFIED` | A production eligibility claim depends on current specified-only evaluator. | VAE/Program Control; certify separately; current consumption remains non-production. |
| `PIPELINE_VISUAL_PARTIAL_RESULT_NOT_CONSUMABLE` | Partial result leaves required roles/hard gates unresolved. | VAE/Pipeline; retain historically or request bounded completion. |
| `PIPELINE_VISUAL_RESULT_STALE` | Demand/result/composition/version superseded, invalidated, revoked or cancelled. | Owning lifecycle product; select eligible replacement. |
| `PIPELINE_VISUAL_CONSUMPTION_NOT_ACKNOWLEDGED` | Composition attempts use without authorized acknowledgement. | Pipeline; block binding. |
| `PIPELINE_VISUAL_ATOMIC_COMMIT_FAILED` | Any artifact/receipt/event/edge/idempotency member fails. | Pipeline repository; roll back all staged members. |
| `PIPELINE_VISUAL_IDEMPOTENCY_CONFLICT` | Same key with byte-different payload. | Caller; investigate and use new command after review. |
| `PIPELINE_VISUAL_STALE_EXPECTED_VERSION` | Optimistic concurrency mismatch. | Caller; reload current aggregate. |
| `PIPELINE_VISUAL_REPLAY_DIVERGENCE` | Historical recomputation differs. | Pipeline; stop at first divergent object and pin. |

Deterministic, semantic, authority, lifecycle and evaluation failures are not blindly retried. Transport/storage transients may retry the exact command identity. Production repair belongs to VAE; semantic amendment belongs to upstream authority; transport recovery belongs to Delegation.

### 8.2 Supersession, invalidation and post-completion governance

Every demand and result version is immutable. Supersession links old to new; cancellation and revocation are additive records. Typed dependency edges include `USES_HARNESS_BINDING`, `USES_VISUAL_HANDOFF`, `USES_SOURCE_PACKAGE`, `USES_COMPOSITION_INTENT`, `USES_FEATURE_CONTRACT`, `INHERITS_LOCK`, `SUBMITS_DEMAND`, `REALIZES_DEMAND`, `PROVIDES_GEOMETRY_FOR`, `EVALUATES_RESULT`, `ACKNOWLEDGES_RESULT`, `BINDS_ASSET_TO_COMPOSITION`, `SUPERSEDES`, `INVALIDATES`, `REVOKES`, and `REPLACES`.

Material source, handoff, demand, geometry, result, evaluator/profile, artifact or composition changes traverse only affected edges. Stale bindings cannot be consumed. Historical demands/results/assets/acknowledgements and their accepted validators remain retrievable and reproducible after invalidation or revocation. Revocation blocks new use but does not delete evidence.

### 8.3 Rollback and recovery

Deployment rollback selects a prior Pipeline service/adapter for new commands and rebuilds projections from immutable records. It never rewrites external release bytes or accepted history. Outbox/inbox processing is deduplicated by canonical message identity. Response loss returns the original receipt on retry. Cancellation/result and supersession/acknowledgement races serialize by expected version; the losing command returns typed stale state.

If Delegation or VAE is unavailable, a compiled but unsubmitted demand may remain durable and non-admitted. A submitted demand remains pinned; no alternate provider route is guessed. If geometry or evaluation resource retrieval fails, the result remains registered but non-consumable. Recovery resumes from exact checkpoints and hashes.

### 8.4 Observability and degraded behavior

Structured events record command/transaction/delegation/request/result/acknowledgement/binding IDs; package/profile/schema hashes; owner/principal; source kind; interview provenance counts; lineage/Feature/T-V/lock counts; category/profile; derivative parent hash and validator outcome; artifact/geometry/evaluation refs; completion/consumption decisions; lifecycle/stream version; idempotent replay; invalidation fan-out and failure owner.

Logs exclude raw private source text, credentials, prompts, signed tokens and absolute local paths. Metrics include release mismatch, source-kind/interview denial, semantic field loss, parse-only incompatibility, missing `EVALUATE`, lock ancestry failure, VAD admission, constraint conflicts, result identity/artifact failures, geometry missing/out-of-tolerance, evaluator unavailable/uncertified, partial-result denial, acknowledgement decision, stale-consumption denial, atomic rollback, concurrency conflict, late message and replay divergence. Metrics are operational evidence, not semantic truth or certification.

## 9. Behavior-specific acceptance criteria

### AC-01 - FR-085 / ST-08.01: exact source-grounded demand

**Given** an eligible Harness binding and AIR handoff for a carousel portrait cutout, **when** demand compilation runs, **then** RC4 VAD 1.1 contains exact source-time/keyframe evidence, source kind, semantic lineage, asset/sequence role, intended composition region, tolerance, identity, locks, Feature Contracts, T/V route, evaluation and delivery requirements. Missing source anchor or provider/model fields in the demand fail. **Evidence:** field crosswalk, canonical demand/hash, negative fixture. **Layer:** contract/integration.

### AC-02 - source-kind and interview provenance

**Given** `interview_expression`, **when** admission runs, **then** non-empty Reaction Receipt and Expression Moment refs exist and resolve. Given a non-interview kind, omission is valid but supplied refs still validate. Unknown kind, guessed migration, or invented provenance fails. **Evidence:** RC4 conditional suite plus source owner receipts. **Layer:** schema/contract.

### AC-03 - semantic lineage and authority preservation

**Given** upstream AIP, Identity DNA, Context Premise, Resonance, Matrix/Edge Product, Activative Call, Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, T/V and Composition Intent, **when** the VAD is compared, **then** every required value/ref and owner is preserved. A generic `semantic_notes` substitution or Pipeline rewrite fails. **Evidence:** pointer/hash crosswalk. **Layer:** architecture/contract.

### AC-04 - VAE/Delegation boundary

**Given** a valid demand, **when** routing occurs, **then** Delegation validates/transports without creative interpretation and VAE alone compiles its Visual Production Plan and provider bindings. A Delegation semantic fallback or Pipeline-selected LoRA fails. **Evidence:** import/command boundary spies. **Layer:** architecture.

### AC-05 - semantic compatibility and EVALUATE

**Given** RC4 required modes, **when** negotiation runs, **then** all preserve/enforce/evaluate features and exact profile refs are supported. Parse-only support, missing `EVALUATE`, or unsupported evaluation profile fails. Current evaluator status remains `specified_not_certified`; capability presence cannot produce certification. **Evidence:** compatibility decision and status assertion. **Layer:** contract/governance.

### AC-06 - portable derivative locks

**Given** a deterministic crop derived from an accepted portrait, **when** the RC4 relationship validates, **then** parent ref/hash, inline/ref lock evidence, derivation type/semantics and every lock identity/meaning/scope/strength are present; stricter additions pass. Missing parent evidence, removed/weakened lock, ambiguous classification or unauthorized relaxation fails. **Evidence:** released RC4 vectors and Pipeline binding receipt. **Layer:** contract/property.

### AC-07 - FR-086: exact result correlation and artifact integrity

**Given** a VAE result, **when** admission runs, **then** result/execution/demand identity, producer, artifact hash/media/dimensions, completion, provenance, evaluation, cost/attempts and lifecycle match the active demand. A beautiful asset missing demand identity or evaluator evidence fails. **Evidence:** result conformance report and artifact hash matrix. **Layer:** integration/adversarial.

### AC-08 - image-conditioned geometry

**Given** a result whose role requires geometry, **when** admission resolves evidence, **then** applicable subject/face/hands/gesture/object/focal boxes, gaze/motion, negative space, safe crops, masks, depth/layers, collisions, canvas coordinates and tolerance are bound to exact artifact/demand. Missing geometry or crop removing required evidence fails. **Evidence:** geometry pack and rendered composition fixture. **Layer:** contract/integration.

### AC-09 - Feature Contract realization without mutation

**Given** upstream gaze/expression/negative-space contracts, **when** result evidence is checked, **then** VAE realization refs preserve exact authoritative contract hashes and report support/outcome. Changed `required_state`, semantic job, locks or required-for-meaning flag fails. **Evidence:** before/after hashes and realization receipts. **Layer:** cross-product contract.

### AC-10 - production acceptance versus acknowledgement

**Given** a production-accepted VAE result, **when** no Pipeline acknowledgement exists, **then** composition remains blocked. When all downstream conformance gates pass, one separate RC4 acknowledgement may set `consumption_authorized: true` and create one exact binding. **Evidence:** three-stage lifecycle fixture. **Layer:** lifecycle/integration.

### AC-11 - partial result and limitation behavior

**Given** `PARTIAL`, **when** unresolved roles intersect a required role/feature/geometry/hard gate, **then** consumption is rejected. Only demand/profile-authorized partial use with complete remaining evidence may be acknowledged, and limitations propagate. **Evidence:** partial matrix. **Layer:** domain/contract.

### AC-12 - conflict and amendment ownership

**Given** out-of-tolerance geometry or infeasible composition, **when** VAE returns a conflict/proposal, **then** the original demand remains immutable and VAE cannot self-approve amendment. Pipeline routes semantic changes to the authoritative upstream owner. **Evidence:** conflict/proposal/response chain. **Layer:** authority/lifecycle.

### AC-13 - supersession, invalidation and stale denial

**Given** a successor demand or post-completion revocation, **when** dependency projection runs, **then** only affected results/bindings/compositions become stale, none can be consumed, and historical bytes remain reproducible. Global deletion or unrelated invalidation fails. **Evidence:** fan-out graph and replay receipt. **Layer:** recovery/property.

### AC-14 - idempotency, concurrency and atomicity

**Given** duplicate delivery, byte-different key collision, two expected-version writers and fault injection at every commit member, **when** commands execute, **then** exact retry returns the original receipt, collision fails, one writer wins, and artifact/receipt/event/edge/idempotency/outbox members commit all-or-none. **Evidence:** repository fault matrix. **Layer:** persistence integration.

### AC-15 - deterministic portability

**Given** identical logical inputs in fresh processes and extracted roots with changed clock, random seed, environment, locale, map order and traversal order, **when** demand/admission/acknowledgement compile, **then** canonical bytes/hashes match and contain no absolute machine paths. **Evidence:** two-process hash matrix and path scan. **Layer:** clean environment.

### AC-16 - migration and historical replay

**Given** legacy demand/result data, **when** migration runs, **then** every required field maps losslessly into new immutable artifacts or migration blocks; source class, provenance, lineage, profile, geometry and locks are never guessed. Historical active work remains pinned. **Evidence:** migration receipts and replay corpus. **Layer:** migration/recovery.

### AC-17 - category/profile and Format 02 truth

**Given** any category/profile, **when** compatibility resolves, **then** exact structural support and certification state are reported. Format 02 remains deferred/currently only contract-compatible where recorded; no conversational/interview profile inherits certification. **Evidence:** category/profile matrix and status assertion. **Layer:** governance/contract.

### AC-18 - claim ceiling

**Given** all structural and synthetic tests pass, **when** status is reported, **then** this spec remains `WRITTEN_PENDING_AUDIT`, authority `CANDIDATE_NOT_CURRENT`, RC4 unsigned/non-production, VAE evaluator `specified_not_certified`, VAE Stage 5 unauthorized, build false and production/certification false. **Evidence:** lifecycle and status assertions. **Layer:** governance.

## 10. Testing and completion evidence

### 10.1 Exact future test paths

| Exact path | Required tests and evidence |
|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/tests/contracts/test_delegation_rc4_release_pin.py` | Package/digest/receipt/manifest/profile/schema/generated-type/validator identities; RC1-RC3 historical only; unsigned trust ceiling. |
| `.../tests/contracts/test_visual_asset_demand_compilation.py` | All RC4 required fields, owners, closed schema, exact upstream crosswalk, no provider/VAE plan fields. |
| `.../tests/contracts/test_visual_source_kind_and_interview_provenance.py` | Eight source kinds, unknown denial, interview conditional, non-interview optional refs, no synthesis/migration guessing. |
| `.../tests/contracts/test_visual_semantic_lineage_preservation.py` | AIP/DNA/Context/Resonance/Matrix/Call/Reaction/Expression/Activation/VSP/VNP/Feature/T-V/Composition exact preservation. |
| `.../tests/contracts/test_delegation_semantic_compatibility.py` | Preserve/enforce/evaluate modes, parse-only denial, unsupported profile, no adapter loss. |
| `.../tests/contracts/test_derivative_lock_inheritance_rc4.py` | Exact/stricter pass; missing evidence, ambiguous class, remove, weaken, semantic shortcut and unauthorized relaxation fail. |
| `.../tests/integration/test_visual_demand_submission.py` | Compile/validate/atomic commit/outbox/admission/audit with transport spy; Delegation cannot interpret meaning. |
| `.../tests/integration/test_asset_result_admission.py` | Exact demand/execution/artifact/provenance/evaluation correlation, partial behavior and attractive-untraceable denial. |
| `.../tests/integration/test_image_conditioned_geometry.py` | Applicable geometry, coordinate/canvas transform, tolerance, safe crop, protected regions, collision and missing-pack denial. |
| `.../tests/integration/test_feature_and_lock_realization.py` | Exact Feature Contract refs, VAE-owned realization, no mutation, evaluator state and lock evidence. |
| `.../tests/integration/test_result_acknowledgement_and_binding.py` | Production acceptance separate from acknowledgement; binding only on explicit authorized consumption. |
| `.../tests/integration/test_visual_delegation_repository.py` | All-or-none persistence, receipt/artifact parity, idempotent retry/collision, optimistic concurrency and outbox. |
| `.../tests/lifecycle/test_visual_delegation_lifecycle.py` | Submission/admission/result/reject/cancel/conflict/amend/supersede/invalidate/revoke/replace and race ordering. |
| `.../tests/recovery/test_visual_asset_selective_invalidation_replay.py` | Typed fan-out, stale denial, late evidence, exact historical reproduction and first divergence. |
| `.../tests/migration/test_visual_delegation_lossless_or_blocked.py` | New immutable artifacts, no guessed source/provenance/profile/geometry/lock/owner and active-version pinning. |
| `.../tests/architecture/test_visual_product_authority_boundaries.py` | AIR/Interview/Builder/Pipeline/VAE/Delegation/Studio ownership and no internal cross-product imports. |
| `.../tests/architecture/test_no_local_delegation_schema_fork.py` | Released schemas/validators referenced only; no copied/altered local shared schema. |
| `.../tests/clean_environment/test_visual_delegation_determinism.py` | Two processes/roots, clock/random/env/order independence, portable paths and byte-identical outputs. |
| `.../tests/reference_slices/test_st08_01_visual_demand_result_geometry.py` | Carousel portrait cutout with source keyframe/time, exact role/region, result/evaluator denial case, acknowledgement, usage and selective invalidation. |
| `.../tests/governance/test_visual_boundary_claim_ceiling.py` | Candidate authority, unsigned RC4, specified-not-certified evaluator, Stage 5/build/production/certification false. |

### 10.2 Adversarial corpus

Required cases include stale RC2 banner treated as current; release directory accepted without hashes; active RC1-RC3 pin; unknown source kind; guessed legacy classification; interview source without Reaction Receipt or Expression Moment; non-interview refs invented by migration; flattened semantic lineage; missing Matrix/Resonance/Identity/Context; provider/model/LoRA in VAD; VAE mutation of Composition Intent or Feature Contract; Delegation creative interpretation; parse-only compatibility; missing `EVALUATE`; capability mistaken for evaluator certification; unsupported evaluation profile; empty locks; missing parent evidence; ambiguous derivation; lock removal/weakening; semantic derivative represented as deterministic crop; demand relaxation in place; mismatched result/demand/execution; artifact hash mismatch; result without evaluator; required geometry missing; geometry tied to another artifact/canvas; out-of-tolerance relocation; unsafe crop; partial result with required role unresolved; VAE acceptance inferred as consumption; acknowledgement without current lifecycle; stale/superseded/revoked use; over-invalidation; destructive rollback; orphan receipt/artifact; idempotency collision; concurrency race; current time/random/env/path identity; lossy migration; Format 02 certification inference; Stage 5/build/production claim.

### 10.3 Later completion evidence and Build Receipt

A later authorized builder must provide ratified/adopted authority and independently accepted hashes for this spec and its upstream interfaces; a bounded Development Capsule; exact RC4 package/profile/schema/generated-type/validator and trust pins; no-local-fork scan; requirement-to-code/test/receipt traceability; source/interview conditional vectors; complete semantic-lineage crosswalk; VAE consumer and Delegation conformance; portable derivative-lock vectors; exact result/artifact/geometry/evaluation proof; Feature Contract realization proof; acknowledgement/usage lifecycle proof; atomic fault/idempotency/concurrency matrix; cancellation/supersession/invalidation/replay evidence; two fresh-process hash matrix; clean extracted-layout proof; status/claim-ceiling assertions; and unresolved limitations.

The Build Receipt, if separately authorized, must distinguish structural implementation, synthetic proof, external consumer/producer conformance, evaluator certification, compute/recovery proof, release signing/publication, production eligibility, Format 02 certification and product authorization. None is inferred from another. This writer issues no Build Receipt, Development Capsule, contract release, audit or acceptance.

Final writer state: `WRITTEN_PENDING_AUDIT`; authority `CANDIDATE_NOT_CURRENT`; specification work authorized; build authority false; later pre-ratification ceiling `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. The next admissible lifecycle action is independent Tech Spec audit by a different agent.
