# TS-AHP-001 - Program Authority, Current-State Reconciliation, and Brownfield Source Admission

```yaml
spec_id: TS-AHP-001
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Atomic Harness Pipeline
primary_owner: Atomic Harness Pipeline
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED
writing_wave: 0
controlling_story: ST-01.01
controlling_frs: [FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-117]
```

This specification is complete enough for independent technical audit, but its V2.1 authority package is `CANDIDATE_NOT_CURRENT`. It does not authorize implementation, production, certification, a Development Capsule, or `ACCEPTED_FOR_BUILD`.

## 1. Files and authorities read

The writer used the recovery packet `CA-P03-WRITE-TS-AHP-001-RECOVERY`. It has no upstream Tech Spec dependency; consequently, no non-accepted upstream draft was used.

| Source | Version or state | SHA-256 | Authority / dependency class | Specific fact used |
|---|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current pointer | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | `REQUIRED_AUTHORITY`; current | Constitution V1.1 wins over local PRDs, specs, schemas, examples, code, or legacy doctrine on Activative and visual-semantic behavior. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | `REQUIRED_AUTHORITY`; highest order | Activation First governs runtime meaning; predecessor machinery, Builder, Pipeline, VAE, and Delegation may not invent or reinterpret upstream meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/MASTER_STATUS.md` | status 2026-07-22 | `71d7fdac3c9498c42133c95e141b31241b0fa613426417d9fd81b3d1d656f491` | `REQUIRED_UNIQUE_EVIDENCE`; current | V2.1 authorities remain candidates; Builder is 69/69 offline implemented but only 27/69 full-evidence closed; implementation, production, and certification authority remain false. |
| `01_ATOMIC_HARNESS_BUILDER/CURRENT_PROJECT_STATUS.md` | current Builder status | `7653473dfd9a38e5fb231938dad2cf0eab1b29412840c3c9cf16a726bfa352f0` | `REQUIRED_UNIQUE_EVIDENCE`; current product status | Builder is a locally usable development product, not a production Builder; production readiness and certification are false. |
| `01_ATOMIC_HARNESS_BUILDER/docs/implementation/offline-development/OFFLINE_IMPLEMENTATION_TERMINAL_SUMMARY.yaml` | OD-AM-005 | current bytes read 2026-07-22 | current implementation evidence | Offline implementation coverage is 69/69 while full evidence remains 27/69 or higher only from real evidence; production and certification are false. |
| `01_ATOMIC_HARNESS_BUILDER/docs/implementation/offline-development/MODEL_NEUTRAL_HANDOFF.yaml` | v5 | current bytes read 2026-07-22 | current implementation evidence | No confirmed Builder implementation Story remains, but external evidence and production gates remain open; implementation receipts are not Story completion receipts. |
| `01_ATOMIC_HARNESS_BUILDER/docs/evidence-closure/TERMINAL_STATE_RECONCILIATION_RECEIPT.yaml` | EC-AM-001 | current bytes read 2026-07-22 | current evidence-closure receipt | Reconciliation passed with a historical RC1 packaging finding and did not close BD-007, BD-008, external-product, human-evidence, production, or certification gates. |
| `01_ATOMIC_HARNESS_BUILDER/docs/release/CURRENT_SUPPORTED_CLAIMS.yaml` | derived 2026-07-17 | current bytes read 2026-07-22 | current claim evidence | Its embedded RC1 packaging status is an older repository-local release projection; Program Control's later status governs the current program claim. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../prd/features/F01-product-authority-brownfield-baseline-and-source-reconciliation.md` | AHP V1.2 draft | `9f18036d0868ed8047ddd09077fddced7f2f3696cdaf279be5edafd76f565bcc` | candidate product requirement | FR-001 through FR-006 require authority checks, status reconciliation, explicit migration disposition, exact provenance, and replacement justification. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../prd/features/F20-source-first-release-1-expansion-and-implementation-readiness.md` | AHP V1.2 draft | `68a709a04acbe21e3e0ee459d0bc1f81bc4e194abf6619498e292da70ee0611f` | candidate product requirement | FR-117 prohibits implementation until repository and operator-local truth is reconciled into one Program Control status without rewriting history. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../planning/EPICS_AND_VERTICAL_STORIES.md` | V1.2 planning | `c7ea3757b6497bd45674222341fa4125009e3d3f8b140c3ce9a6855284fe1cb7` | candidate Story | ST-01.01 requires the accepted or denied decision to remain reconstructable and selective recovery to preserve unaffected accepted work and historical receipts. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../sources/CURRENT_STATE_RECONCILIATION.md` | source `SRC-STATE-001` | `6e9478a31b5b3db3e4c83e86a9275ba4fe05676bb95e206dd62411af1352e905` | `REQUIRED_UNIQUE_EVIDENCE`; migration input | Builder terminal, handoff, evidence-closure, and release records must be reconciled into Program Control before implementation. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../sources/CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1.md` | source `SRC-MIG-001` | `5912930b2abfb376aef67c140bb745845ede054b07ad6aa0e9bb77f9a06301d7` | `REQUIRED_UNIQUE_EVIDENCE`; migration evidence only | The predecessor contains valuable runtime machinery and tests, but is neither current authority nor a restartable production monolith. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../sources/EXACT_SOURCE_REUSE_CROSSWALK.csv` | source `SRC-MIG-002` | `c8c97f5d2003d070180a7061484609b2f9c8ef990efa116914f05b4e400e7820` | `REQUIRED_UNIQUE_EVIDENCE`; source crosswalk | Current, predecessor, and evidence sources have explicit source IDs, paths, observed hashes, authority, disposition, and proposed targets. |
| `THE_CMF_STUDIO(2)/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | source `SRC-LEG-033` | `402b57e027aecd3daba2dced3add91bcc1d2b107c5dc2166adec8ea3678740af` | `REQUIRED_UNIQUE_EVIDENCE`; historical | The legacy audit identifies a real deterministic composition path, but later audit must distinguish documented architecture from current runnable proof. |
| `THE_CMF_STUDIO(2)/docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` | source `SRC-LEG-034` | `d8a65762d077ac553fe8d2ccf0e149fb79cc61d116628397f0d2453369667dba` | `REQUIRED_UNIQUE_EVIDENCE`; historical intent | It records source lineage, provider-job, render, evaluation, and approval concepts; those concepts do not supersede present ownership. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/studio_pipeline_recipe_harness.py` | predecessor source | current bytes read 2026-07-22 | migration evidence only | It has useful typed recipes, steps, artifacts, gates, blockers, and receipts, but uses current time, random UUID-derived IDs, `Any`, and old route semantics. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/studio_pipeline_recipe_harness.py` | predecessor source | current bytes read 2026-07-22 | migration evidence only | Its independent in-memory dictionaries do not supply transactional consistency, durable replay, or cross-store atomicity. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_pipeline_recipe_orchestration_spine_integration_v1.py` | predecessor test | current bytes read 2026-07-22 | migration evidence only | The test usefully denies provider and renderer actions in the mapped orchestration spine, but proves only legacy contract integration. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | V2.1 candidate | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | candidate ownership authority | Pipeline executes approved Harnesses and emits Visual Asset Demands; it may not reinterpret source, Edge Product, Primitive coalition, Final Script, or VAE strategy. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | V2.1 candidate | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | candidate ownership authority | AIR owns semantic lifecycle objects, Interview Expression owns live source/reaction evidence, Builder owns `AtomicHarnessDefinition`, and Pipeline owns execution state. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only authorization | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | WRITE authorization | WRITE through technical convergence is allowed; build, implementation, production, certification, VAE Stage 5, and Development Capsules are forbidden. |

`05_ATOMIC_HARNESS_PIPELINE` did not exist when this packet was frozen. There is no current Pipeline implementation or target-local `AGENTS.md` to inspect. Program Control explicitly authorized only this direct candidate spec path. The older assignment's `04_ATOMIC_HARNESS_PIPELINE/...` path is superseded by the Prompt 02 canonical path and is not used.

## 2. Problem, user outcome, solution, and scope

### Problem

An execution binding can appear structurally valid while relying on a stale authority pointer, an unreconciled repository-local status, or predecessor code whose technical behavior is useful but whose semantics, product boundary, and claim state are obsolete. Without one deterministic admission boundary, the Pipeline could execute the wrong category/profile, import old Format 02 assumptions, represent implementation coverage as evidence closure, or treat historical provider and visual policies as current authority. Every derivative would then inherit invalid lineage.

### User and system outcome

Program Control and a Pipeline operator can prove, before any binding becomes executable, exactly which current authority, status snapshot, source bytes, ownership decision, and migration disposition were admitted. An accepted or denied decision is immutable, replayable, and explainable. A localized source or status conflict blocks only dependent admissions and does not rewrite historical receipts.

### Bounded solution

Define a deterministic `AuthorityAndSourceAdmission` boundary that:

1. verifies Program Control authority and status snapshot identities;
2. distinguishes current authority, unratified candidate authority, current implementation evidence, migration evidence, and historical evidence;
3. requires one `REUSE`, `ADAPT`, `ACTIVATE`, `REPLACE`, or `ARCHIVE` decision for every admitted predecessor source;
4. requires exact archive identity, path, bytes, SHA-256, dependency provenance, and migration justification;
5. verifies that an execution binding references only admitted, ownership-compatible sources and current contract identities;
6. emits immutable acceptance or denial receipts whose semantic IDs do not depend on time, random state, environment, or absolute machine paths.

### In scope

- FR-001 through FR-006 and FR-117; ST-01.01.
- Authority/status/source-admission domain objects and deterministic validation.
- A Program Control status projection port and immutable local admission repository contract.
- Brownfield disposition and replacement-justification rules.
- Admission of an execution binding to the later Pipeline runtime, not execution itself.
- Conflict, supersession, invalidation, replay, and selective recovery rules.
- Exact future source, contract, and test paths.

### Out of scope and non-goals

- Implementing any file named in this candidate specification.
- Compiling Activative meaning, Primitive coalitions, archetypes, Matrix of Edging, Final Script, Composition Intent, or `AtomicHarnessDefinition`.
- Running providers, renderers, VAE, Interview Expression, Delegation, or Builder.
- Activating Format 02, VAE Stage 5, production, publication, or certification.
- Rewriting or deleting historical receipts, statuses, or rejected release evidence.
- Declaring predecessor tests or package validation to be current production evidence.
- Creating a generic creative-safety or content-rights authority. Operator-supplied source authority, provenance, attributable approval, product sovereignty, and technical security remain distinct.

## 3. Governing decisions and constraints

### Authority precedence and claim ceiling

The current authority remains Constitution V1.1 and current product PRDs. The V2.1 AIR/AHP/ownership package is `CANDIDATE_NOT_CURRENT`; this spec may be written and independently audited under `CA-P02C-SPEC-WORK-AUTH-2026-07-22`, but cannot become build authority before attributable ratification and any required product adoption. The current maximum state for this spec is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`, and its present state is `WRITTEN_PENDING_AUDIT`.

### Product sovereignty

- Program Control owns constitutional precedence, current cross-product authority, canonical program status, release identity, and candidate-to-current transitions.
- AIR owns semantic lifecycle and production-program meaning, including epistemic state, Matrix of Edging interpretation, psychological role inside a tension, exact Primitive Bindings, Primitive Coalition Contract, Coalition Signature, Edge Product, Primitive Misuse Risk, archetype coalition, approved Final Script, Activation Transfer Contract, Composition Intent, Brand Context Version, Guest Voice DNA, and Visual DNA where applicable.
- Interview Expression owns live source admission, Reaction Observations/Receipts, Expression Moments, and the Canonical Interview Source Package.
- Builder owns immutable `AtomicHarnessDefinition` compilation and declares exact AIR and Interview dependencies. `Activative Contract Compiler != Activative Intelligence Runtime`.
- Pipeline owns execution-binding admission, runtime state, retrieval/execution/evaluation coordination, receipts, and authoritative Visual Asset Demand emission. It consumes semantic objects without rebuilding or reinterpreting them.
- VAE owns Visual Production Plans and visual realization. Delegation transports and enforces shared envelopes. Studio projects state and sends typed correction commands.

### Source fidelity and admission law

- A path or filename is not identity. Identity is archive/package ID plus normalized relative member path plus byte length plus SHA-256.
- Absolute machine paths may appear only in local evidence locators; portable contracts store a repository-relative or archive-member path and an independent archive identity.
- Missing or hash-drifted `REQUIRED_AUTHORITY`, `REQUIRED_CURRENT_IMPLEMENTATION`, or `REQUIRED_UNIQUE_EVIDENCE` blocks admission. Optional/deferred references do not block and may not be cited for facts while absent.
- The system never guesses source classification, ownership, or status. Ambiguity produces a typed blocker.
- Migration evidence cannot promote itself to current semantic authority.
- A `REPLACE` decision requires at least one typed reason: `BEHAVIOR_GAP`, `CONTRACT_INCOMPATIBILITY`, `SECURITY_BOUNDARY`, `PORTABILITY_FAILURE`, `DURABILITY_FAILURE`, or `BOUNDED_COST_JUSTIFICATION`, with evidence references.
- `REUSE`, `ADAPT`, and `ACTIVATE` require license/dependency review and exact provenance. `ARCHIVE` remains reproducible but cannot be admitted to active execution.

### Explicitly forbidden behavior

- Accepting an execution binding against an authority or status snapshot whose hash differs from Program Control.
- Treating `OFFLINE_IMPLEMENTATION_COMPLETE` as Story/evidence closure, production readiness, or certification.
- Importing old route IDs, four-format assumptions, hidden personas, generic role prompts, provider pins, or predecessor semantics as current law.
- Manufacturing source history, Reaction Receipts, Expression Moments, identity approval, or operator consent.
- Accepting randomly generated IDs, current timestamps, dictionary insertion order, filesystem traversal order, absolute host paths, or process environment as semantic-hash inputs.
- Mutating an admitted record in place. Amendments produce a new immutable version and explicit supersession edges.

No draft dependency caveat applies to Wave 0: `upstream_write_inputs` is empty.

## 4. Current brownfield architecture

There is no current `05_ATOMIC_HARNESS_PIPELINE` implementation. The following predecessor artifacts are evidence candidates, not current components.

| Exact predecessor path | Observed behavior | Disposition | Reason and migration constraint |
|---|---|---|---|
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/studio_pipeline_recipe_harness.py` | Typed recipes, steps, gates, artifacts, blockers, runs, and receipts; validates duplicate/missing dependencies and gate references. | `ADAPT` | Preserve bounded enum and validation ideas. Replace `Any`, random UUID IDs, current-time defaults, old route/category IDs, and implicit version defaults with current typed contracts and canonical hash identities. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/repositories/studio_pipeline_recipe_harness.py` | Separate in-memory dictionaries and unconstrained `upsert/get`. | `REPLACE` | It has no atomic cross-store commit, optimistic concurrency, durable command record, or replay proof. Replacement is justified by durability and authority-boundary gaps; fixtures may preserve its simple lookup cases. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/services/pipeline_recipe_registry_service.py` | Hard-coded legacy recipe catalogue, including `format02_golden_path`. | `ARCHIVE` | Recipe shapes can inform tests, but hard-coded old profiles cannot be active current authority. Format 02 remains deferred and `contract_compatible`, not production-certified. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/composition_runtime.py` | Typed composition objects, validation, renderer targets, and source-lineage references, alongside open dictionaries and random/time defaults. | `ADAPT` | Later category/runtime specs may reuse bounded geometry and receipt concepts. This spec admits only the source record; it does not import composition authority. |
| `THE_CMF_STUDIO(2)/tests/cmf_studio/test_pipeline_recipe_orchestration_spine_integration_v1.py` | Proves legacy recipe-to-spine mapping and denies provider/renderer calls in stage plans. | `REUSE` | Preserve as migrated behavior fixtures after current contract IDs replace legacy types; a passing legacy test is not current acceptance. |
| `THE_CMF_STUDIO(2)/docs/audits/CMF_VISUAL_GEOMETRICS_SKIA_SAM3_PRETEXT_AUDIT_2026-06-24.md` | Documents Skia/SAM3/PRETEXT and visual-production gaps. | `ARCHIVE` | Retain exact bytes as evidence; do not represent the audit as executable current behavior. |
| `THE_CMF_STUDIO(2)/docs/prd/modules/PRD_CMF_07_Editing_Composition_Rendering.md` | Historical provider, composition, render, lineage, and approval intent. | `ARCHIVE` | Retain for traceability. Current product boundaries and later category/VAE specs decide adoption. |
| `01_ATOMIC_HARNESS_BUILDER/docs/implementation/offline-development/OFFLINE_IMPLEMENTATION_TERMINAL_SUMMARY.yaml` and `MODEL_NEUTRAL_HANDOFF.yaml` | Current Builder implementation evidence and its explicit claim ceilings. | `REUSE` | Consume through a read-only status adapter; do not copy or reinterpret Builder state into Pipeline-owned truth. Program Control remains canonical cross-product status. |

Migration must preserve original path, bytes, hash, archive identity, original authority class, disposition decision, decision actor, decision evidence, and any extracted target hash. Extracted code receives the Pipeline namespace and current interfaces; it does not retain authority through ancestry.

## 5. Proposed architecture and workflows

### Components and responsibilities

1. `AuthoritySnapshotVerifier` reads a pinned Program Control authority snapshot and verifies constitutional/product/candidate states. It cannot ratify candidates.
2. `ProgramStatusReconciler` compares Program Control status with repository projections and evidence receipts. It records conflicts; Program Control is the only canonical status publisher.
3. `BrownfieldSourceRegistry` stores immutable source identities and one governed disposition per source version.
4. `SourceAdmissionPolicy` validates required evidence, provenance, ownership, dependency/license decisions, and replacement justification.
5. `ExecutionBindingAdmissionService` verifies that a proposed binding references the accepted authority/status/source set and contains no cross-product ownership violation.
6. `AdmissionReceiptStore` atomically commits request, decision, blockers, evidence references, supersession edges, and command/idempotency record. No admitted state exists without a corresponding receipt, and no success receipt exists without committed state.
7. `ProgramControlStatusPort` is a read-only adapter for signed or hash-pinned Program Control snapshots. It never writes Program Control.

### Entry and exit objects

- Entry: `ReconcileProgramStateCommand`, `RegisterBrownfieldSourceCommand`, `DecideSourceDispositionCommand`, and `EvaluateExecutionBindingAdmissionCommand`.
- Exit: immutable `ProgramStateReconciliationReceipt`, `SourceAdmissionReceipt`, or `ExecutionBindingAdmissionReceipt` with decision `ACCEPTED` or `DENIED`.
- A denial is a complete result, not an exception without context. It includes blocker code, owning repository/product, affected object IDs, retry class, and next admissible action.

### State transitions

```text
Program snapshot: OBSERVED -> VERIFIED | CONFLICTED -> SUPERSEDED
Source version:    DISCOVERED -> HASH_VERIFIED -> DISPOSITIONED -> ADMITTED | ARCHIVED | BLOCKED
Binding version:   PROPOSED -> VALIDATING -> ACCEPTED | DENIED -> SUPERSEDED | INVALIDATED
```

Only a new immutable object version can move from a terminal state into a new decision. `SUPERSEDED` and `INVALIDATED` retain the old bytes and receipts.

### Synchronous and asynchronous behavior

Hashing, schema validation, authority comparison, status comparison, and admission decisions are synchronous and deterministic. External source acquisition, license review, or attributable human disposition approval may be asynchronous; the command remains `BLOCKED_PENDING_EVIDENCE` and cannot create an executable binding while waiting. No background completion may silently change the original command's receipt.

### Idempotency, replay, cancellation, and compensation

- `idempotency_key = sha256(command_type + canonical_payload + authority_snapshot_id)`.
- Repeating an identical command returns the existing receipt. Reusing the key with different canonical bytes yields `IDEMPOTENCY_CONFLICT`.
- Replay loads exact input versions and recomputes deterministic validation. It compares the recomputed decision digest with the stored receipt and emits a replay receipt; it does not mutate history.
- Cancellation before atomic commit records `CANCELLED_NO_STATE_CHANGE`. Cancellation racing with a completed commit returns the committed receipt and a `CANCELLATION_TOO_LATE` observation.
- If commit fails, request, decision, state projection, receipt, and command record all roll back. External copied bytes created before failure are quarantined by hash and never become admitted state.

### Main handoff

```text
Program Control authority/status snapshot
  + repository status/evidence projections
  + source archive/member bytes
  + owner-approved migration disposition
  + proposed immutable execution binding
        -> deterministic reconciliation and admission
        -> ACCEPTED receipt and admitted-source set
        -> later Pipeline intake may execute
```

The accepted receipt authorizes only admission under its claim ceiling. It does not authorize a provider call, renderer call, VAE request, production use, or certification.

## 6. Data models, contracts, schemas, and APIs

### Schema identities

| Schema | Version | Owner | Mutability |
|---|---|---|---|
| `ca.pipeline.authority_snapshot` | `1.0.0-candidate` | Program Control value; Pipeline projection | immutable |
| `ca.pipeline.program_status_projection` | `1.0.0-candidate` | source repository value; Pipeline projection | immutable |
| `ca.pipeline.brownfield_source_record` | `1.0.0-candidate` | Atomic Harness Pipeline | immutable per source version |
| `ca.pipeline.source_disposition_decision` | `1.0.0-candidate` | Program Control or attributable target-product authority | immutable |
| `ca.pipeline.execution_binding_admission_request` | `1.0.0-candidate` | Atomic Harness Pipeline | immutable |
| `ca.pipeline.execution_binding_admission_receipt` | `1.0.0-candidate` | Atomic Harness Pipeline | immutable |

### Typed fields

`AuthoritySnapshot`:

| Field | Type | Required | Owner / rule |
|---|---|---|---|
| `schema_id` | literal `ca.pipeline.authority_snapshot` | yes | Pipeline contract |
| `schema_version` | semver string | yes | Pipeline contract |
| `snapshot_id` | `sha256:<64 lowercase hex>` | yes | derived from canonical content |
| `constitution_id` | non-empty string | yes | Program Control |
| `constitution_version` | non-empty string | yes | Program Control |
| `constitution_sha256` | SHA-256 | yes | observed bytes |
| `product_authorities` | sorted non-empty array of `AuthorityRef` | yes | Program Control |
| `candidate_authorities` | sorted array of `CandidateAuthorityRef` | yes | Program Control; each has `CANDIDATE_NOT_CURRENT` or a ratification receipt |
| `canonical_program_status_id` | SHA-256 identity | yes | Program Control |
| `issued_by` | non-empty authority ID | yes | Program Control |
| `issued_at` | RFC 3339 UTC | yes | evidence only; excluded from semantic ID |

`BrownfieldSourceRecord`:

| Field | Type | Required | Owner / rule |
|---|---|---|---|
| `source_record_id` | SHA-256 identity | yes | derived |
| `archive_id` | SHA-256 identity or `repository:<repo>@<commit>` | yes | source custodian |
| `relative_path` | normalized POSIX relative path | yes | no drive letter, UNC prefix, `..`, NUL, or absolute root |
| `byte_length` | unsigned 64-bit integer | yes | observed bytes |
| `sha256` | SHA-256 | yes | observed bytes |
| `source_class` | enum `CURRENT_AUTHORITY`, `CURRENT_IMPLEMENTATION`, `UNIQUE_EVIDENCE`, `OPTIONAL_REFERENCE`, `DEFERRED_REFERENCE`, `SUPERSEDED`, `HISTORICAL` | yes | Source Disposition authority |
| `origin_repository` | governed product/repository ID | yes | source custodian |
| `license_evidence_refs` | sorted array of typed artifact IDs | yes, may be empty only for internal current sources | reviewing authority |
| `dependency_manifest_ref` | typed artifact ID or explicit `NOT_APPLICABLE` | yes | reviewing authority |
| `disposition_decision_id` | typed decision ID | yes before active admission | disposition owner |

`SourceDispositionDecision`:

| Field | Type | Required | Owner / rule |
|---|---|---|---|
| `decision_id` | SHA-256 identity | yes | derived |
| `source_record_id` | typed ID | yes | Pipeline reference |
| `disposition` | enum `REUSE`, `ADAPT`, `ACTIVATE`, `REPLACE`, `ARCHIVE` | yes | attributable authority |
| `target_paths` | sorted relative-path array | required for all except `ARCHIVE` | Pipeline path authority |
| `replacement_reason` | typed enum | required only for `REPLACE` | decision authority |
| `behavior_preservation_refs` | sorted typed artifact IDs | required for `REUSE`, `ADAPT`, `ACTIVATE` | decision authority |
| `authority_exclusions` | non-empty sorted string array | yes | must deny semantic inheritance from migration evidence |
| `decided_by` | non-empty actor/authority ID | yes | attributable authority |
| `evidence_refs` | non-empty sorted typed artifact IDs | yes | immutable evidence |

`ExecutionBindingAdmissionRequest` requires `request_id`, `binding_id`, `binding_version`, `binding_sha256`, `atomic_harness_definition_ref`, `authority_snapshot_id`, `program_status_id`, sorted `source_record_ids`, sorted `contract_refs`, `category_id`, `profile_id`, `requested_claim`, and `idempotency_key`. All references are typed and versioned. It contains no embedded semantic notes and no provider/runtime decision.

`ExecutionBindingAdmissionReceipt` requires `receipt_id`, exact `request_id`, `decision` (`ACCEPTED` or `DENIED`), `authority_snapshot_id`, `program_status_id`, `binding_sha256`, sorted validated source/contract refs, sorted `blockers`, `maximum_claim`, `supersedes_receipt_id` or explicit `NOT_APPLICABLE`, `decision_digest`, `created_at`, and `actor_id`. `ACCEPTED` requires zero blockers; `DENIED` requires at least one blocker.

### Canonical serialization and hashing

1. Validate types and normalize relative paths before serialization.
2. Serialize UTF-8 JSON with lexicographically sorted object keys, arrays sorted only where the schema declares set semantics, no insignificant whitespace, no NaN/Infinity, integers in base-10, booleans lowercase, and timestamps normalized to UTC `Z`.
3. Exclude evidence-only `created_at`/`issued_at` fields from semantic identity while retaining them in the receipt bytes.
4. Compute `sha256` over the canonical semantic payload and prefix the lowercase hex with `sha256:`.
5. Reject unknown fields. Schema version changes require a registered compatible reader or an explicit migration.

Filesystem order, dictionary insertion order, locale, current time, random state, environment variables, and host paths cannot influence semantic bytes.

### Compatibility, supersession, and migration

- Minor schema versions may add only optional evidence fields that do not change admission semantics. Any required field, enum, normalization, ownership, or decision change is a major version.
- Readers reject unknown major versions and unknown enum values.
- Migration emits a new immutable artifact with `migrated_from_id`, `migration_id`, old/new hashes, field map, and losslessness result. It never edits an original artifact.
- A migration that cannot preserve source classification, authority state, path/hash identity, disposition, or blockers returns `LOSSY_MIGRATION_BLOCKED`.
- Active accepted bindings remain pinned to the versions accepted. Supersession invalidates only bindings whose dependency closure contains the superseded version.

### Positive example

```json
{
  "schema_id": "ca.pipeline.source_disposition_decision",
  "schema_version": "1.0.0-candidate",
  "source_record_id": "sha256:402b57e027aecd3daba2dced3add91bcc1d2b107c5dc2166adec8ea3678740af",
  "disposition": "ARCHIVE",
  "target_paths": [],
  "replacement_reason": "NOT_APPLICABLE",
  "behavior_preservation_refs": [],
  "authority_exclusions": ["not_current_product_authority", "not_production_evidence"],
  "decided_by": "program-control:migration-authority",
  "evidence_refs": ["source:SRC-LEG-033"]
}
```

### Negative example

```json
{
  "source_record_id": "legacy-audit",
  "relative_path": "D:\\Work\\old\\audit.md",
  "disposition": "REPLACE",
  "replacement_reason": "",
  "authority_exclusions": []
}
```

The negative example is rejected for untyped identity, absolute path leakage, absent archive/hash/byte identity, missing replacement justification, and absent authority exclusions.

## 7. Implementation stages and exact target paths

These are proposed future build targets. They are not an implementation allowlist and may be used only after ratification/adoption and a bounded Development Capsule.

| Stage | Exact target paths | FR / Story mapping | Completion evidence |
|---|---|---|---|
| 1. Freeze contracts | `05_ATOMIC_HARNESS_PIPELINE/contracts/authority_snapshot.schema.json`; `contracts/program_status_projection.schema.json`; `contracts/brownfield_source_record.schema.json`; `contracts/source_disposition_decision.schema.json`; `contracts/execution_binding_admission_request.schema.json`; `contracts/execution_binding_admission_receipt.schema.json` | FR-001, FR-002, FR-003, FR-005, FR-006; ST-01.01 AC1-AC3 | schema tests, canonical examples, negative corpus |
| 2. Implement domain validation | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/authority/authority_snapshot.py`; `authority/program_status.py`; `authority/source_admission.py`; `authority/failures.py`; `domain/canonical_hash.py` | FR-001-FR-006; ST-01.01 AC1-AC4 | deterministic unit tests and ownership denials |
| 3. Implement application boundary | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/application/reconcile_program_state.py`; `application/register_brownfield_source.py`; `application/evaluate_execution_binding_admission.py` | FR-001, FR-002, FR-117; ST-01.01 AC1-AC3 | integration receipt bundle |
| 4. Implement read-only adapters | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/adapters/program_control/status_reader.py`; `adapters/builder/status_reader.py`; `adapters/legacy_cmf/source_inventory.py` | FR-001-FR-005, FR-117; ST-01.01 AC1-AC3 | adapter contract and path-safety tests |
| 5. Implement atomic persistence | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/repositories/admission_repository.py`; `repositories/sqlite_admission_repository.py`; `migrations/0001_authority_source_admission.sql` | FR-002, FR-005, FR-117; ST-01.01 AC3/AC5 | transaction, concurrency, replay, migration, rollback evidence |
| 6. Wire intake gate | `05_ATOMIC_HARNESS_PIPELINE/src/cmf_pipeline/application/admit_execution_binding.py`; `src/cmf_pipeline/cli/authority.py` | FR-001, FR-004, FR-117; ST-01.01 AC1/AC2/AC4 | end-to-end accepted/denied binding fixtures |
| 7. Preserve predecessor evidence | `05_ATOMIC_HARNESS_PIPELINE/governance/source_admission_registry.yaml`; `governance/predecessor_disposition_register.yaml`; `docs/migration/CMF_STUDIO_SOURCE_ADMISSION.md` | FR-003-FR-006; ST-01.01 DoD | file-level disposition and provenance receipt |

Each implementation task must cite the exact FR, ST-01.01 acceptance criterion, accepted spec hash, ratification/adoption receipt, and bounded Development Capsule. No task may edit Builder, AIR, Interview Expression, VAE, Delegation, Studio predecessor, immutable release, or Program Control authority bytes.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Condition | Owner | Retry / recovery |
|---|---|---|---|
| `AUTHORITY_HASH_MISMATCH` | observed authority bytes differ from pinned snapshot | Program Control/source custodian | non-retryable until a governed snapshot or correct bytes are supplied |
| `CANDIDATE_AUTHORITY_NOT_RATIFIED` | requested claim requires current V2.1 authority | Program Control/human ratifier | blocked; specification work may continue, execution/build may not |
| `STATUS_CONFLICT` | repository projection contradicts Program Control canonical status | originating repository plus Program Control | reconcile and publish a new superseding status; never edit history |
| `REQUIRED_SOURCE_UNAVAILABLE` | required source bytes cannot be read | source custodian | supply exact hash-locked bytes |
| `SOURCE_HASH_MISMATCH` | bytes/path/archive identity drift | source custodian | register a new source version or restore expected bytes |
| `SOURCE_CLASS_AMBIGUOUS` | source authority/disposition cannot be determined | Program Control | explicit disposition required; never guess |
| `REPLACEMENT_JUSTIFICATION_MISSING` | `REPLACE` lacks a typed reason/evidence | migration owner | supply attributable decision evidence |
| `SEMANTIC_AUTHORITY_IMPORT_ATTEMPT` | predecessor would override AIR/Interview/Builder/VAE meaning | requesting product | hard denial; redesign at correct owner |
| `ABSOLUTE_PATH_NOT_PORTABLE` | portable artifact contains drive, UNC, absolute, or traversal path | Pipeline | normalize to governed relative locator or deny |
| `IDEMPOTENCY_CONFLICT` | same key, different canonical payload | Pipeline | do not retry with same key; issue a new command identity |
| `OPTIMISTIC_CONCURRENCY_CONFLICT` | expected aggregate version differs | Pipeline | reload current state and resubmit a new command |
| `ATOMIC_COMMIT_FAILED` | any request/state/receipt/command write fails | Pipeline | roll back all stores, quarantine copied bytes, retry only when storage healthy |
| `LOSSY_MIGRATION_BLOCKED` | required semantics/provenance cannot be preserved | migration owner | block migration or create an explicitly new source classification |

Failures do not collapse into free-form messages. Each includes `failure_id`, `code`, `owner`, `affected_refs`, `evidence_refs`, `retry_class`, and `next_admissible_action`.

### Invalidation and selective recovery

- A changed authority, status, source hash, disposition, contract, or ownership record creates a new version and a dependency-graph invalidation event.
- Descendants whose acceptance digest included the changed reference become `STALE_NOT_CONSUMABLE`; unrelated accepted admissions remain valid.
- Historical source bytes, decisions, bindings, and receipts remain addressable by hash for reproduction even after revocation.
- A source-field correction reruns source verification, its disposition decision if relevant, and only dependent binding admissions. It does not rerun unrelated source records.
- Post-completion revocation records a typed reason and replacement reference. It cannot erase prior evidence.

### Rollback and compensation

Database schema rollout uses a forward-only migration plus verified backup. Application rollback may restore the earlier reader while retaining newly written immutable rows. A major-schema write is disabled until both old and new readers pass fixture replay. Source copies that fail final commit move to a non-admitted quarantine path keyed by hash; no destructive delete is required for logical rollback.

### Observability

Emit structured events `authority_snapshot_verified`, `program_status_conflicted`, `source_hash_verified`, `source_disposition_decided`, `binding_admission_accepted`, `binding_admission_denied`, `admission_invalidated`, and `admission_replayed`. Metrics include decisions by code/owner, status conflicts by repository, source hash failures, idempotent replays, atomic rollback count, invalidation fan-out, and replay digest mismatches. Logs carry typed IDs and hashes, never source content, secrets, operator credentials, or absolute local paths. Every event points to its immutable receipt.

## 9. Behavior-specific acceptance criteria

1. **Current precedence - FR-001 / ST-01.01 AC1.** Given a binding pinned to the current Constitution V1.1 and current Program Control status, when admission runs, then it verifies both hashes and emits `ACCEPTED` only if every product boundary matches. Failure example: the binding cites a predecessor PRD as higher authority. Evidence: `execution_binding_admission_receipt.json`. Test layer: integration.
2. **Candidate ceiling - FR-001 / ST-01.01 AC2.** Given an unratified V2.1 candidate and a request for build or production authority, when admission runs, then it returns `CANDIDATE_AUTHORITY_NOT_RATIFIED` with no executable state. Failure example: `CANDIDATE_NOT_CURRENT` is serialized as current. Evidence: denial receipt. Test layer: domain and integration.
3. **Status reconciliation - FR-002, FR-117 / ST-01.01 AC1-AC3.** Given Builder's 69/69 offline coverage and 27/69 evidence closure plus Program Control's current status, when reconciliation runs, then both dimensions remain separate and the later Program Control status is canonical. Failure example: a repository-local older RC1 projection overrides Program Control. Evidence: status conflict/reconciliation receipt. Test layer: adapter integration.
4. **Historical immutability - FR-002, FR-117 / ST-01.01 AC3.** Given a newer status, when it supersedes an older projection, then old bytes and hash remain readable and a supersession edge is recorded. Failure example: the earlier receipt is overwritten. Evidence: before/after manifest plus supersession receipt. Test layer: persistence and migration.
5. **Complete disposition - FR-003 / ST-01.01 DoD.** Given a predecessor inventory, when source admission completes, then every member is assigned exactly one of `REUSE`, `ADAPT`, `ACTIVATE`, `REPLACE`, or `ARCHIVE`. Failure example: a module is both `REUSE` and `ARCHIVE`, or absent. Evidence: coverage report with unique count. Test layer: contract/property.
6. **No semantic import - FR-004 / ST-01.01 AC2/AC4.** Given the legacy `format02_golden_path` recipe, when admission checks ownership, then old route semantics are archived and cannot override AIR, Builder, current category/profile, wrong-reading locks, or Format 02 deferral. Failure example: the hard-coded recipe is accepted as current product meaning. Evidence: `SEMANTIC_AUTHORITY_IMPORT_ATTEMPT` receipt. Test layer: architecture boundary.
7. **Exact provenance - FR-005 / ST-01.01 AC3.** Given an adapted predecessor file, when registered, then archive identity, relative member path, bytes, SHA-256, dependency provenance, decision, and target path are all present and hash-valid. Failure example: only a Windows absolute path is stored. Evidence: source-admission receipt and portable artifact scan. Test layer: schema/integration.
8. **Replacement justification - FR-006 / ST-01.01 AC2.** Given the in-memory legacy repository is marked `REPLACE`, when the decision is validated, then a durability/atomicity contract mismatch and evidence refs are required. Failure example: reason is `cleaner code`. Evidence: disposition-decision receipt. Test layer: unit/contract.
9. **Unknown and unavailable sources - FR-003, FR-005 / ST-01.01 AC2.** Given an unknown source class or unavailable required bytes, when admission runs, then it denies without guessing; an unavailable optional reference is recorded as a gap and not cited. Failure example: filename inference promotes it to current authority. Evidence: typed blocker and gap notice. Test layer: adversarial integration.
10. **Determinism - FR-005 / ST-01.01 AC3.** Given the same logical source and binding in two fresh processes with shuffled input maps, traversal order, timezone, environment, and random seeds, when canonicalization runs, then semantic IDs and decision digests are byte-identical. Failure example: timestamps change the source ID. Evidence: two-process hash matrix. Test layer: deterministic clean-environment.
11. **Atomicity and idempotency - FR-001, FR-005 / ST-01.01 AC2-AC3.** Given a storage failure between state and receipt writes, when commit runs, then neither becomes visible; replaying the same command after recovery creates exactly one state and one receipt. Failure example: accepted state exists without receipt. Evidence: fault-injection transaction log. Test layer: persistence integration.
12. **Selective recovery - FR-117 / ST-01.01 AC5.** Given one source version is superseded, when invalidation runs, then only admissions in its dependency closure become stale and unrelated accepted admissions remain consumable. Failure example: global invalidation removes unrelated history. Evidence: dependency/invalidation matrix. Test layer: graph/property integration.
13. **Historical reproduction - FR-005, FR-117 / ST-01.01 AC3/AC5.** Given a revoked old source and binding, when historical replay is requested with exact IDs, then the system reconstructs its decision digest without making it current or consumable. Failure example: replay reads latest source bytes. Evidence: historical replay receipt. Test layer: replay integration.
14. **Claim separation - FR-002, FR-117 / ST-01.01 DoD.** Given all admission tests pass, when status is projected, then the strongest claim is source/binding admission readiness under the candidate ceiling, not implementation, production, certification, or Format 02 readiness. Failure example: schema PASS yields `production_ready: true`. Evidence: claim-ceiling test receipt. Test layer: architecture/status integration.

## 10. Testing and completion evidence

### Exact proposed test paths and cases

- `05_ATOMIC_HARNESS_PIPELINE/tests/contracts/test_authority_snapshot_schema.py`: unknown fields, unknown versions, missing hashes, candidate/current distinction, positive canonical fixture.
- `05_ATOMIC_HARNESS_PIPELINE/tests/contracts/test_brownfield_source_record_schema.py`: path traversal, drive/UNC path, byte/hash mismatch, absent disposition, duplicate dispositions, typed replacement reason.
- `05_ATOMIC_HARNESS_PIPELINE/tests/domain/test_canonical_hash.py`: shuffled dictionaries and sets, Unicode normalization, environment/time/random independence, two-process stable digest.
- `05_ATOMIC_HARNESS_PIPELINE/tests/domain/test_source_admission_policy.py`: all five dispositions, missing unique evidence, optional gap behavior, license/dependency evidence, semantic-authority denial.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_program_status_reconciliation.py`: Program Control versus Builder/VAE/Delegation projections, separate implementation/evidence/production/certification dimensions, historical supersession.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_execution_binding_admission.py`: accepted current binding, stale authority denial, unratified build denial, old Format 02/profile denial, owner mismatch, exact receipt linkage.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_admission_repository_atomicity.py`: fail before/after each write, no orphan state or receipt, optimistic concurrency, idempotent replay, idempotency conflict.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_source_invalidation.py`: descendant-only invalidation, stricter replacement, stale binding non-consumption, historical reproducibility.
- `05_ATOMIC_HARNESS_PIPELINE/tests/migration/test_predecessor_source_migration.py`: lossless source identity mapping, blocked lossy migration, old in-memory repository replacement justification, legacy receipt preservation.
- `05_ATOMIC_HARNESS_PIPELINE/tests/architecture/test_product_authority_boundaries.py`: Pipeline cannot import AIR semantic compilers, Builder definition compilers, VAE production strategy, or Program Control mutation ports.
- `05_ATOMIC_HARNESS_PIPELINE/tests/clean_environment/test_portable_admission_bundle.py`: extracted-layout run, no absolute machine path/secret/environment leakage, byte-identical manifest in two roots.
- `05_ATOMIC_HARNESS_PIPELINE/tests/reference_slices/test_st01_01_authority_source_admission.py`: complete ST-01.01 accepted, denial, evidence/replay, CBAR, and selective-recovery proof.

### Required completion evidence for a later build

A later, separately authorized build must produce: schema validation results; unit/integration/architecture/migration/replay/fault-injection results; two-fresh-process determinism hashes; a portable extracted-layout report; full predecessor inventory coverage; Program Control status reconciliation receipt; source admission manifest; exact changed-file manifest; and an independent Build Receipt. The Build Receipt must cite the ratified/adopted authority hash, this accepted spec hash, a bounded Development Capsule, all FR/Story evidence, and the maximum supported claim.

Passing these tests would support only the claim explicitly granted by that later receipt. It cannot by itself grant production readiness, provider authority, VAE Stage 5, Format 02 certification, or product certification. This writer issues no Build Receipt and no acceptance.
