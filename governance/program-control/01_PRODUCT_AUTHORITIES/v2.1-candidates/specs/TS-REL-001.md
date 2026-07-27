---
document_class: CANDIDATE_CANONICAL_TECH_SPEC
spec_id: TS-REL-001
title: Format 02 Deferral, Historical Evidence Isolation, and Future Activation Gate
version: 2.1.0-candidate.1
product_owner: Program Control
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
build_state: NOT_BUILD_READY
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 0
controlling_frs: [FR-079, FR-080, FR-081, FR-082, FR-083, FR-084]
controlling_stories: [ST-11.01]
---

# TS-REL-001 — Format 02 Deferral, Historical Evidence Isolation, and Future Activation Gate

## 1. Files and authorities read

This specification is candidate work only. The V2.1 candidate authority is `CANDIDATE_NOT_CURRENT`; specification work is explicitly authorized, implementation and build are not. The maximum later pre-ratification state is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

| Source | Version / SHA-256 | Authority or dependency class | State and fact used |
|---|---|---|---|
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | `conscious-activations-specification-work-authorization-receipt/v1` | specification-work authorization | `ACTIVE_SPECIFICATION_WORK_ONLY`; WRITE is authorized and BUILD is forbidden. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | `conscious-activations-authority-stage-decision/v1` | claim-ceiling authority | V2.1 remains pending ratification; `ACCEPTED_FOR_BUILD` and Development Capsules are forbidden. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | recovery packet `CA-P03-WRITE-TS-REL-001-RECOVERY` | frozen writer packet | Wave 0; exact direct Program Control path; no upstream writing dependency. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_SPEC_LEDGER.csv` | Prompt 02 committed ledger | canonical queue | TS-REL-001 title, owner, path, Gate A, six FRs, and one Story. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/CANONICAL_FR_LEDGER.csv` and `FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | Prompt 02 committed ledgers | controlling requirements | FR-079–FR-084 are owned by Program Control through ST-11.01 and TS-REL-001. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SPEC_DEPENDENCY_DAG.yaml` | Prompt 02 committed DAG | lifecycle dependency context | TS-REL-001 has no upstream spec and is an authority dependency of TS-REL-002. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/PATH_OWNERSHIP_REGISTRY.yaml` | Prompt 02 committed registry | path authority | Reserves this exact output path to Program Control. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | V2.1 candidate | candidate authority | Program Control owns cross-product authority, canonical status, release and claim authority; Builder owns `AtomicHarnessDefinition`; Pipeline executes; VAE realizes visual demands. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | V2.1 candidate | candidate semantic ownership | The Builder is the authoritative value owner for `AtomicHarnessDefinition`; no downstream product may invent that object. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../prd/features/F14-deferred-format-02-historical-reconciliation.md` | AHP PRD V1.2 candidate feature F14 | candidate product requirement | Format 02 is inactive; evidence is historical; future specs are regenerated from an independently validated current Harness. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../planning/EPICS_AND_VERTICAL_STORIES.md` | ST-11.01 | controlling Story | An absent current Harness forces exclusion from the active campaign and emits reconstructable denial evidence. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../planning/spec_assignments/TS-REL-001.md` | SHA-256 `465194f948da11c5a2233b58c5dc8db66ba3017efbf970599266fed672a90a3f` | assignment brief, not a Tech Spec | Supplies scope and source list but grants no path or build authority. |
| `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/.../sources/brownfield/CONSCIOUS_ACTIVATIONS_STUDIO_ARCHITECTURE_AMENDMENT_V2_1.zip` | SHA-256 `9059fe3cad98c5d6ca0f9584f091ac503a5e5a9279a4a476821db816dc7603b8` | `REQUIRED_AUTHORITY` candidate amendment | `01_FORMAT02_SCOPE_CORRECTION.yaml` defines canonical profile ID, deferred state, no active implementation/surface, and the activation gate. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/format_profiles.py` | SHA-256 `084f28c593cee4fc8df4947ea3678336c8aab4a1ee76ff68d12fa3a1759be8b0` | `REQUIRED_CURRENT_IMPLEMENTATION` | Emits canonical `format02_minimal_coach_theatre`, maps the historical alias, requires 13 registry references when bound, and keeps benchmark/certification false. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_06_02/test_profile_compilation.py` and `test_profile_failures.py` | exact current test files | current behavior evidence | Tests category isolation, alias resolution, 13-registry completeness, hash drift rejection, and false certification denial. |
| `02_VISUAL_ASSET_EDITOR/CURRENT_PROJECT_STATUS.md` | SHA-256 `383b31d94b3623cf7884d5b4d6297d860444b865cc92d3fc3ad2226dc461f95a` | `REQUIRED_UNIQUE_EVIDENCE` | Format 02 is only reference/structural/contract-compatible; evaluator is not certified; Stage 5 is not authorized. |
| `CONSCIOUS_ACTIVATIONS_AHP_PRD_V1_2_PRIMITIVE_ARCHETYPE_CENTERED/.../sources/CMF_STUDIO_PREDECESSOR_MIGRATION_AUDIT_V1.md` | SHA-256 `5912930b2abfb376aef67c140bb745845ede054b07ad6aa0e9bb77f9a06301d7` | `REQUIRED_UNIQUE_EVIDENCE` | The predecessor has valuable registries, schemas, tests, and dry-run patterns but is neither current authority nor production-ready. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/FORMAT02_PROFILE_ALIAS_REGISTRY.yaml` | `cmf-format-profile-alias-registry/v1` | current Program Control compatibility registry | Canonical ID is `format02_minimal_coach_theatre`; aliases are read/migration-only and cannot inherit certification. |
| `SRC-EXT-018`, `SRC-EXT-019`, `SRC-EXT-025` in `SOURCE_DISPOSITION_LEDGER.yaml` and `SOURCE_GAP_NOTICE.yaml` | exact bytes unavailable | `DEFERRED_REFERENCE` | Non-blocking research backlog only; this spec makes no factual implementation or capability claim from them. |

There is no upstream spec dependency in Wave 0. `DRAFT_DEPENDENCY_NOT_ACCEPTED` therefore does not apply to a consumed draft in this specification.

## 2. Problem, user outcome, solution, and scope

### Problem

Current repositories contain useful Format 02 identifiers, structural profile code, compatibility fixtures, predecessor registries, dry-run adapters, tests, and historical release material. Without a single enforceable Program Control gate, a planner or release process could mistake one of those artifacts for a current executable Harness, an active Pipeline lane, a Studio surface, a benchmark, or production certification. That would violate FR-079–FR-084 and cause the ST-11.01 downstream failure: implementation effort and public claims would proceed without the current Builder-owned semantic contract.

### User and system outcome

Program Control can inventory and replay historical Format 02 evidence while every active planning, binding, routing, benchmark, release, and certification decision fails closed until an exact, current `AtomicHarnessDefinition` is produced by Builder and independently validated. A denied request returns a typed reason, the missing prerequisites, the owner of each prerequisite, and immutable evidence; it does not erase or rewrite history.

### Bounded solution

Define four Program Control records and one deterministic decision function:

1. a canonical `Format02DeferralRecord`;
2. an immutable `Format02HistoricalEvidenceManifest`;
3. an append-only `Format02ActivationEvidenceSet`;
4. a `Format02GateDecisionReceipt` for every evaluation; and
5. `evaluate_format02_gate(request, current_state) -> receipt`, a pure, fail-closed decision whose only successful transition is from deferred to activation-eligible after every governed prerequisite passes.

The gate protects the profile ID `format02_minimal_coach_theatre`. It does not design or compile the missing Harness.

### In scope

- FR-079: exclusion from active implementation, campaigns, routes, benchmarks, and claims.
- FR-080: immutable inventory of the 13 historical character-performance registry families.
- FR-081: historical retention of `CharacterPerformanceProgram` candidate schemas and fixtures.
- FR-082: historical staging, camera, scene-reading, relationship-visibility, composition, and wrong-reading evidence.
- FR-083: nonbinding temporal-embodiment research with no active renderer binding.
- FR-084: historical/synthetic classification, isolation, replay, and claim-ceiling checks.
- Canonical identifier and read-only historical alias behavior.
- Supersession, replay, selective invalidation, denial, and release/status projection rules.

### Out of scope and non-goals

- Creating a Format 02 `AtomicHarnessDefinition` or altering Builder behavior.
- Creating Pipeline runtime nodes, Studio surfaces, renderer bindings, VAE jobs, or Stage 5 work.
- Selecting Remotion, HyperFrames, Stretchy/Spine, or another embodiment runtime.
- Promoting predecessor schemas or test fixtures to current canonical contracts.
- Benchmarking, production certification, release authorization, or external publication.
- Rewriting historical receipts, assets, releases, rejection records, or aliases.
- Creating generic creative-safety or content-rights approval authority.

## 3. Governing decisions and constraints

### Product sovereignty and ownership

- Program Control owns the deferral state, activation decision, cross-repository status truth, and release/claim ceiling.
- Atomic Harness Builder alone owns the authoritative `AtomicHarnessDefinition`. `Activative Contract Compiler != Activative Intelligence Runtime` remains true.
- AIR owns semantic lifecycle and production-program meaning; this gate never recompiles Primitive, archetype, Matrix of Edging, Final Script, or Composition Intent meaning.
- Atomic Harness Pipeline may consume a validated Harness only after activation. It cannot activate Format 02 by possessing historical code or a renderer.
- VAE owns visual realization but cannot provide the missing Harness, evaluator certification, or Stage 5 authority.
- Studio projects state and emits typed commands; it cannot mutate canonical deferral state directly.
- Independent validation is separate from Builder and from Program Control release projection. A producing component cannot accept itself.

### Protected invariants

1. `current_state == DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS` until every activation prerequisite passes in one consistent evidence snapshot.
2. New active emissions use only `format02_minimal_coach_theatre`. Aliases remain readable for history/migration and emit an alias-resolution receipt.
3. Historical evidence is immutable, hash-addressed, classified, and never treated as current authority.
4. The 13 registry families are reconciliation requirements, not active runtime registry values.
5. A predecessor `CharacterPerformanceProgram` remains a candidate migration artifact; the current schema must be regenerated from the validated current Harness.
6. Renderer/tool capability does not satisfy Harness, evaluation, compatibility, evidence, or authority prerequisites.
7. A synthetic URI, dry-run result, fake adapter success, old approval flag, or historical receipt cannot support real-output, readiness, benchmark, production, or certification claims.
8. Operator-supplied source authority, provenance, lineage, attributable approvals, and product sovereignty remain intact. Technical security is operational, not creative authority.
9. Any hash or version change in an activation prerequisite invalidates that evidence and its dependent decision, not unrelated historical evidence.
10. While V2.1 ratification is pending, this document cannot pass beyond `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`; build authority remains false.

### Activation prerequisites

An `ACTIVATION_ELIGIBLE` decision requires all of the following in the same request:

- a Builder-issued current Format 02 `AtomicHarnessDefinition` with immutable ID, version, canonical hash, and Builder issuance receipt;
- explicit category `2d_character_animation` and canonical profile `format02_minimal_coach_theatre`;
- complete current category, 13-registry, workflow, context, capability, evaluation, compatibility, binding, lineage, and wrong-reading-lock requirements inside or referenced immutably by the Harness;
- independent validation of Harness completeness, authority, deterministic serialization, and semantic preservation;
- current product-adoption receipts for every affected product-local specification;
- current compatibility evidence for Pipeline, Studio projection, VAE boundary where demanded, and Delegation transport where used;
- current evaluation identity and evidence sufficient for the claimed scope;
- attributable Program Control ratification of the activation decision and claim ceiling; and
- regeneration and independent re-audit of any runtime or Studio specification that was based on historical Format 02 assumptions.

Missing, stale, ambiguous, unowned, internally inconsistent, or self-attested evidence produces `DENIED_DEFERRED`; the decision function never guesses.

## 4. Current brownfield architecture

| Exact path / component | Actual current behavior | Disposition | Constraint |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/format_profiles.py` | Compiles a deterministic structural profile registry, canonicalizes one alias, lists 13 registry kinds, and explicitly keeps readiness/certification false. | `REUSE` as current structural evidence | It does not create the missing current Harness or activation authority. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_06_02/test_profile_compilation.py` | Confirms canonical category/profile mapping and false benchmark/certification. | `REUSE` as regression evidence | Structural/contract compatibility is not activation. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_06_02/test_profile_failures.py` | Rejects hash drift, category mismatch, unknown IDs, incomplete 13-registry state, and false certification. | `ADAPT` into Program Control boundary tests | Do not copy Builder-owned implementation into Program Control. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/FORMAT02_PROFILE_ALIAS_REGISTRY.yaml` | Governs canonical ID and two historical aliases; aliases are not emitted for new active writes. | `REUSE` | Alias resolution never changes authority or certification. |
| Studio amendment `01_FORMAT02_SCOPE_CORRECTION.yaml` inside SHA-locked `SRC-AM-001` | Defines deferred state, no active implementation/surface, historical retention, and activation prerequisites. | `ACTIVATE` as candidate gate input after ratification | Candidate amendment is not current authority yet. |
| Predecessor Format 02 object spine, registries, schemas, tests, dry-run adapters, synthetic outputs | Provides migration and future benchmark evidence. | `ARCHIVE` as historical evidence; selectively `ADAPT` only after future reconciliation | No direct current route, schema, or success claim. |
| VAE Format 02 reference slice and current status | Structural/contract fixture evidence; evaluator, compute, recovery, Stage 5, and production remain unready. | `REUSE` only as truthful status/evidence | VAE fixture passage cannot activate Format 02. |
| Historical Delegation Format 02 fixtures/releases | Transport and compatibility history. | `ARCHIVE` older release records; `REUSE` only current contract compatibility evidence | Contract compatibility does not prove production execution. |
| External runtime locators `SRC-EXT-018/019/025` | Exact bytes unavailable and no unique requirement depends on them. | `ARCHIVE` in research backlog until separately hash-locked | No factual claim, adoption, binding, or license conclusion is made here. |

Migration is additive: historical artifacts keep their original bytes, identifiers, timestamps, and receipts. The new manifest points to them by digest and adds classification; it never moves, rewrites, or normalizes their content.

## 5. Proposed architecture and workflows

### Components

1. **Format 02 evidence registrar** — accepts `RegisterFormat02HistoricalEvidence`; verifies digest, locator, artifact class, provenance, and uniqueness; appends a manifest entry.
2. **Alias resolver** — consumes the governed alias registry; resolves read/migration inputs to the canonical ID and emits `Format02AliasResolutionReceipt`; rejects unknown or ambiguous IDs.
3. **Deferral gate evaluator** — performs deterministic prerequisite checks over an immutable evaluation snapshot and emits exactly one decision receipt.
4. **Status projector** — projects the authoritative Program Control decision into status exports. It cannot change the decision.
5. **Claim validator** — rejects active-route, benchmark, real-output, production, or certification claims while state is deferred or the requested claim exceeds evidence.
6. **Historical replay reader** — reconstructs a prior inventory/gate decision from versioned records without consulting mutable current files except to verify explicitly requested drift.

### Commands, events, and state transitions

| Command | Preconditions | Event / receipt | State effect |
|---|---|---|---|
| `RegisterFormat02HistoricalEvidence` | Canonical or resolvable historical profile ID; readable bytes; digest; class; provenance | `Format02HistoricalEvidenceRegistered` | Appends one immutable manifest entry; no activation effect. |
| `RecordFormat02SourceGap` | Expected family/fixture is absent or unreadable | `Format02SourceGapRecorded` | Adds a gap tied to an inventory version; remains deferred. |
| `EvaluateFormat02Activation` | Exact deferral version plus evidence-set version | `Format02GateDecisionReceipt` | `DENIED_DEFERRED` or `ACTIVATION_ELIGIBLE`; no direct runtime mutation. |
| `ProjectFormat02Status` | Existing decision receipt hash | `Format02StatusProjectionReceipt` | Updates only a mutable projection with source decision identity. |
| `SupersedeFormat02Evidence` | New immutable replacement entry and authority | `Format02EvidenceSuperseded` | Marks the prior entry superseded for current evaluation but replayable. |
| `InvalidateFormat02ActivationEvidence` | Hash/version/authority drift proven | `Format02ActivationEvidenceInvalidated` | Invalidates the evidence and descendant eligibility decision; returns projection to deferred. |

State machine:

```text
DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS
  -- Register evidence / gaps --> DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS
  -- Evaluate with any failed prerequisite --> DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS
  -- Evaluate with all prerequisites + attributable Program Control ratification
       --> ACTIVATION_ELIGIBLE
ACTIVATION_ELIGIBLE
  -- evidence drift / revocation / supersession --> DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS
```

`ACTIVATION_ELIGIBLE` authorizes only the separately stated activation scope. It does not itself start Pipeline work, VAE Stage 5, a Studio surface, production, or certification. Those require their own adopted specifications and bounded authorization.

### Idempotency, concurrency, replay, and compensation

- Command idempotency key is `sha256(command_type || canonical_payload_without_receipt_time)`; duplicate keys return the original receipt.
- Every mutation supplies `expected_record_version`; a version mismatch returns `FORMAT02_CONCURRENT_UPDATE` without partial writes.
- Manifest entry identity is content-derived from canonical JSON bytes; traversal order and wall clock cannot affect it.
- A gate evaluation pins every evidence record version and hash. A concurrent update cannot enter the in-flight snapshot.
- Registration and receipt append are one atomic commit. Neither an unreceipted record nor a receipt without its referenced record is valid.
- Replay uses the recorded snapshot and validator version; it never substitutes current evidence silently.
- A failed projection is retriable because the canonical decision already exists. Projection rollback cannot roll back or delete the canonical decision.

## 6. Data models, contracts, schemas, and APIs

All persisted records use UTF-8 canonical JSON: lexicographically sorted object keys, arrays retained in declared semantic order, no insignificant whitespace, no floating-point numbers, RFC 3339 UTC timestamps supplied by the command envelope but excluded from content-derived identity where stated, and SHA-256 over the final bytes plus LF. Unknown fields fail closed for major version 1.

### `Format02DeferralRecord` — schema `ca-program-control-format02-deferral/v1`

| Field | Type | Required | Owner and rule |
|---|---|---|---|
| `record_id` | non-empty string | yes | Program Control; stable `format02-deferral`. |
| `record_version` | positive integer | yes | Program Control; optimistic concurrency version. |
| `profile_id` | literal `format02_minimal_coach_theatre` | yes | Builder-origin identity, governed by Program Control alias registry. |
| `category_id` | literal `2d_character_animation` | yes | Builder-origin category; cross-category reuse rejected. |
| `state` | enum `DEFERRED_AWAITING_CURRENT_ATOMIC_HARNESS`, `ACTIVATION_ELIGIBLE` | yes | Program Control. |
| `active_implementation_authority` | boolean | yes | Must be false while deferred. |
| `active_studio_surface_authority` | boolean | yes | Must be false while deferred. |
| `benchmark_authorized` | boolean | yes | Must be false while deferred. |
| `production_authorized` | boolean | yes | Must remain false unless separately ratified; activation alone cannot set true. |
| `certification_state` | enum `reference_profile`, `structurally_supported`, `contract_compatible`, `benchmarked`, `limited_production_certified`, `production_certified` | yes | Program Control claim projection; monotonic only with exact evidence. Current value `contract_compatible`. |
| `evidence_set_id` | immutable ID or null | yes | Program Control; null is allowed only while deferred. |
| `latest_decision_receipt_id` | immutable receipt ID | yes | Program Control. |
| `supersedes_record_version` | positive integer or null | yes | Program Control; null only at version 1. |

### `Format02HistoricalEvidenceEntry` — schema `ca-program-control-format02-historical-evidence/v1`

| Field | Type | Required | Owner and rule |
|---|---|---|---|
| `evidence_id` | `sha256:<64 lowercase hex>` | yes | Content-derived; immutable. |
| `source_locator` | workspace-relative path or governed archive-member locator | yes | Program Control records; absolute machine paths rejected. |
| `source_sha256` | `sha256:<64 lowercase hex>` | yes | Registrar verifies bytes before commit. |
| `source_bytes` | non-negative integer | yes | Exact byte count. |
| `artifact_class` | enum `HISTORICAL_REGISTRY`, `HISTORICAL_SCHEMA`, `HISTORICAL_FIXTURE`, `HISTORICAL_TEST`, `HISTORICAL_DRY_RUN_ADAPTER`, `HISTORICAL_SYNTHETIC_OUTPUT`, `STAGING_EVIDENCE`, `CAPABILITY_RESEARCH` | yes | Program Control classification. |
| `registry_family` | one of the 13 registry family IDs or null | yes | Required for `HISTORICAL_REGISTRY`; forbidden otherwise. |
| `historical_identifier` | non-empty string | yes | Original ID preserved verbatim. |
| `authority_state` | literal `HISTORICAL_EVIDENCE_NOT_CURRENT_AUTHORITY` | yes | Cannot be promoted in place. |
| `execution_eligibility` | literal `HISTORICAL_REPLAY_ONLY` | yes | Active JIT/runtime binding prohibited. |
| `observed_facts` | ordered array of non-empty strings | yes | Only source-observed facts; empty array allowed for opaque bytes. |
| `inferred_rules` | ordered array of non-empty strings | yes | Must be separately labeled; cannot satisfy current Harness requirements. |
| `provenance_refs` | non-empty ordered array of immutable references | yes | Operator/source authority and chain of custody. |
| `superseded_by_evidence_id` | immutable ID or null | yes | Supersession preserves replay. |

The 13 allowed `registry_family` values are: `character_identity`, `pose`, `expression`, `gesture`, `gaze`, `prop_and_attachment`, `animation_primitive`, `character_state`, `scene_relationship`, `camera_and_framing`, `transition`, `sonic_cue`, and `compatibility`.

### `Format02ActivationEvidenceSet` — schema `ca-program-control-format02-activation-evidence/v1`

Required fields are: `evidence_set_id`, `evidence_set_version`, `profile_id`, `atomic_harness_definition_id`, `atomic_harness_definition_version`, `atomic_harness_definition_sha256`, `builder_issuance_receipt_id`, `builder_issuance_receipt_sha256`, `required_registry_families` (exactly the 13 allowed values, once each), `workflow_contract_refs`, `context_contract_refs`, `capability_contract_refs`, `evaluation_contract_refs`, `compatibility_contract_refs`, `binding_contract_refs`, `semantic_lineage_refs`, `wrong_reading_lock_contract_refs`, `independent_validation_receipt_id`, `independent_validation_receipt_sha256`, `product_adoption_receipts`, `ratification_receipt_id`, `ratification_receipt_sha256`, and `canonical_hash`.

Every `*_refs` field is a non-empty ordered array of `{id: non-empty string, version: non-empty string, sha256: sha256 digest, owner: governed product enum}`. Empty values, duplicates, unknown owners, alias profile IDs, self-validation, and unpinned references are rejected.

### `Format02GateDecisionReceipt` — schema `ca-program-control-format02-gate-decision/v1`

Required fields are: `receipt_id`, `idempotency_key`, `decision` (`DENIED_DEFERRED` or `ACTIVATION_ELIGIBLE`), `deferral_record_version`, `evidence_set_id` or null, `evidence_set_sha256` or null, `validator_id`, `validator_version`, `validator_sha256`, `evaluated_checks` (ordered typed check results), `failed_check_codes`, `invalidated_descendant_refs`, `authority_actor`, `command_id`, `canonical_hash`, and `recorded_at`. `authority_actor` identifies Program Control; `recorded_at` is receipt metadata, not an input to decision identity.

### Positive example

```json
{"artifact_class":"HISTORICAL_FIXTURE","authority_state":"HISTORICAL_EVIDENCE_NOT_CURRENT_AUTHORITY","evidence_id":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","execution_eligibility":"HISTORICAL_REPLAY_ONLY","historical_identifier":"SCN-01","inferred_rules":[],"observed_facts":["fixture parses under its historical schema"],"provenance_refs":["SRC-MIG-001"],"registry_family":null,"source_bytes":431,"source_locator":"99_ARCHIVE/format02/fixtures/SCN-01.json","source_sha256":"sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","superseded_by_evidence_id":null}
```

This entry is valid historical evidence and has no activation effect.

### Negative examples

- `profile_id: minimal_coach_theatre` in a new active emission: reject `FORMAT02_ALIAS_NOT_ALLOWED_FOR_ACTIVE_EMISSION`; migration may resolve it only with an alias receipt.
- `artifact_class: HISTORICAL_SYNTHETIC_OUTPUT` with `execution_eligibility: ACTIVE`: reject `FORMAT02_HISTORICAL_PROMOTION_FORBIDDEN`.
- An evidence set with 12 registry families: reject `FORMAT02_REGISTRY_FAMILY_INCOMPLETE`.
- A renderer demo without a Builder Harness: deny `FORMAT02_CURRENT_HARNESS_MISSING`.
- A Builder-issued Harness validated only by Builder: deny `FORMAT02_INDEPENDENT_VALIDATION_MISSING`.
- Any absolute `C:\...` or `D:\...` source locator: reject `FORMAT02_NONPORTABLE_LOCATOR`.

## 7. Implementation stages and exact target paths

No implementation is authorized by this document. After ratification and a bounded Development Capsule, work is staged as follows.

| Stage | Exact target paths | FR / Story mapping | Completion evidence |
|---|---|---|---|
| 1 — schemas and seed state | `CMF_PROGRAM_CONTROL/01_PRODUCT_AUTHORITIES/format02/schemas/format02_deferral.schema.json`; `format02_historical_evidence.schema.json`; `format02_activation_evidence.schema.json`; `format02_gate_decision_receipt.schema.json`; `CMF_PROGRAM_CONTROL/01_PRODUCT_AUTHORITIES/format02/FORMAT02_DEFERRAL_STATE.yaml` | FR-079–FR-084 / ST-11.01 | Schema validation and seed-state canonical-hash receipt. |
| 2 — historical inventory | `CMF_PROGRAM_CONTROL/01_PRODUCT_AUTHORITIES/format02/FORMAT02_HISTORICAL_EVIDENCE_MANIFEST.yaml`; `CMF_PROGRAM_CONTROL/01_PRODUCT_AUTHORITIES/format02/FORMAT02_SOURCE_GAPS.yaml` | FR-080–FR-084 / ST-11.01 | File-level SHA manifest, 13-family coverage/gap report, no-active-authority assertions. |
| 3 — deterministic validator | `CMF_PROGRAM_CONTROL/scripts/format02_gate.py`; `CMF_PROGRAM_CONTROL/scripts/validate_format02_evidence.py` | FR-079–FR-084 / ST-11.01 | Pure decision tests, canonical serialization tests, typed denial receipts. |
| 4 — status projection | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/FORMAT02_ACTIVATION_GATE_STATUS.yaml`; affected repository `PROGRAM_STATUS_EXPORT.yaml` projections only under separate path authority | FR-079 / ST-11.01 | Projection hashes reference the same canonical decision; no repository redefines it. |
| 5 — regression and replay | `CMF_PROGRAM_CONTROL/tests/format02/test_deferral_gate.py`; `test_historical_evidence.py`; `test_aliases.py`; `test_claim_ceiling.py`; `test_replay_and_invalidation.py`; `fixtures/` | FR-079–FR-084 / ST-11.01 | Positive, negative, drift, concurrency, replay, portability, and claim tests. |

Product-local Builder, Pipeline, VAE, Studio, and Delegation paths are not assigned here. Any future adoption must be separately authorized by the applicable product and re-audited against the exact adopted bytes.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Retry class | Owner / next admissible action |
|---|---|---|
| `FORMAT02_CURRENT_HARNESS_MISSING` | not retryable without new evidence | Builder must issue the current Harness; remain deferred. |
| `FORMAT02_HARNESS_HASH_MISMATCH` | retry after correct immutable bytes | Evidence submitter supplies exact bytes matching the receipt. |
| `FORMAT02_REGISTRY_FAMILY_INCOMPLETE` | repair evidence set | Builder supplies all 13 governed requirements; no defaults are invented. |
| `FORMAT02_INDEPENDENT_VALIDATION_MISSING` | not retryable by producer self-attestation | Independent validation owner issues a receipt. |
| `FORMAT02_ALIAS_NOT_ALLOWED_FOR_ACTIVE_EMISSION` | deterministic correction | Emit canonical ID and preserve alias resolution evidence. |
| `FORMAT02_HISTORICAL_PROMOTION_FORBIDDEN` | policy denial | Keep artifact historical; create a new current artifact under proper owner if authorized. |
| `FORMAT02_NONPORTABLE_LOCATOR` | deterministic correction | Replace machine path with a workspace-relative or archive-member locator. |
| `FORMAT02_STALE_EVIDENCE_SET` | retry with newly versioned set | Re-pin changed evidence; old set remains replayable. |
| `FORMAT02_CONCURRENT_UPDATE` | safe retry | Re-read current record version and submit a new command. |
| `FORMAT02_CLAIM_CEILING_EXCEEDED` | authority/evidence blocker | Reduce claim or supply and ratify the missing evidence. |
| `FORMAT02_SELF_ACCEPTANCE_FORBIDDEN` | authority denial | Route to the independent validator/auditor. |

### Migration and compatibility

- Historical aliases are resolved only on read/migration; original bytes and identifiers remain unchanged.
- Historical evidence enters the manifest as a new immutable classification record. Migration never changes source classification based on guesses.
- Duplicate bytes with different historical locators may share a source digest but have separate provenance records; duplicate semantic identity with contradictory classifications fails reconciliation.
- Deprecated historical schemas remain readable by their recorded validator version. They do not become supported current write formats.
- A future v2 schema migration emits a new artifact and receipt, preserves v1 bytes, and declares lossless mappings or blocks the migration.

### Rollback, recovery, and invalidation

- Because evidence and decisions are immutable, rollback changes only the current pointer/projection to the last independently validated decision.
- Revoking or superseding one evidence item invalidates only activation evidence sets and gate decisions that reference it. Unrelated inventory entries and historical receipts remain valid.
- If an `ACTIVATION_ELIGIBLE` decision is invalidated after downstream planning, Program Control returns the canonical projection to deferred and emits descendant invalidation targets for unconsumed planning artifacts. It never deletes executed history.
- Late status projections referencing an invalidated receipt are rejected as stale.
- A partial manifest import commits neither entries nor receipt unless the entire atomic batch validates; callers may retry item-by-item with stable idempotency keys.

### Observability

Required metrics: gate decisions by code, evidence registration success/failure, unresolved registry families, alias reads, claim-ceiling denials, stale evidence-set denials, projection lag, replay mismatches, and invalidated descendants. Logs contain IDs, versions, hashes, owners, and failure codes but not unbounded source content. Events and receipts are append-only and support correlation by command, evidence set, decision, and downstream projection.

## 9. Behavior-specific acceptance criteria

1. **FR-079 / ST-11.01 — absent Harness denies activation.** Given a planning request for `format02_minimal_coach_theatre` with no current Builder Harness, when the gate evaluates it, then it emits `DENIED_DEFERRED` with `FORMAT02_CURRENT_HARNESS_MISSING`, leaves active route/surface/benchmark/production flags false, and records the exact input snapshot. Failure example: a historical golden-path fixture creates an active campaign lane. Evidence: gate receipt plus absence scan. Test layer: Program Control integration and architecture-boundary tests.
2. **FR-079 / ST-11.01 — complete independent evidence becomes eligible, not executable.** Given all exact activation prerequisites and attributable Program Control ratification, when the gate evaluates one immutable snapshot, then it emits `ACTIVATION_ELIGIBLE` while production and product-local implementation remain separately unauthorized. Failure example: eligibility starts a Pipeline run automatically. Evidence: decision receipt and zero product mutation diff. Test layer: integration/authority.
3. **FR-080 / ST-11.01 — preserve all 13 families.** Given historical registry artifacts, when inventory runs, then each family is represented exactly once or has an explicit gap, with source hash and `HISTORICAL_EVIDENCE_NOT_CURRENT_AUTHORITY`. Failure example: `sonic_cue` is silently omitted or a historical pose becomes active registry state. Evidence: inventory coverage report. Test layer: schema/unit.
4. **FR-081 / ST-11.01 — candidate program cannot become current.** Given a predecessor `CharacterPerformanceProgram` schema and passing historical fixtures, when a caller requests current schema registration, then the gate returns `FORMAT02_HISTORICAL_PROMOTION_FORBIDDEN`. Failure example: fixture passage produces a current schema ID. Evidence: denial receipt and unchanged registry. Test layer: contract/architecture.
5. **FR-082 / ST-11.01 — observed staging facts remain distinct from inferred rules.** Given a historical visual, when it is registered, then observed facts and inferred rules are separate, and neither alone can support active rendering or a valid-reference-output claim. Failure example: “render completed” is recorded as semantic/evaluation validity. Evidence: evidence-entry JSON and claim denial. Test layer: schema/adversarial.
6. **FR-083 / ST-11.01 — embodiment attractiveness is nonbinding.** Given a renderer demonstration or capability note, when no current Harness exists, then the artifact is stored as `CAPABILITY_RESEARCH` and no binding is emitted. Failure example: keyframe support selects a current engine. Evidence: deferred binding receipt. Test layer: authority boundary.
7. **FR-084 / ST-11.01 — synthetic evidence cannot support real claims.** Given an old synthetic URI or dry-run success flag, when a release/readiness projection is requested, then `FORMAT02_CLAIM_CEILING_EXCEEDED` is returned and the artifact stays historical synthetic. Failure example: synthetic output increments a real-render count. Evidence: claim-validation receipt. Test layer: release regression.
8. **FR-079/080 / ST-11.01 CBAR — speed cannot bypass authority.** Given an urgent release request and complete-looking predecessor evidence, when the current Harness or independent validation is missing, then the exact missing prerequisite blocks the request. Failure example: convenience bypasses the authority check. Evidence: typed denial, owner, and next action. Test layer: adversarial integration.
9. **FR-079 / ST-11.01 — alias behavior is deterministic.** Given historical `minimal_coach_theatre`, when migration reads it, then it resolves to the canonical ID and emits an alias receipt; given the same alias in a new active write, it is rejected. Failure example: two active profile identities are emitted. Evidence: alias receipts and registry count. Test layer: unit/contract.
10. **FR-079–FR-084 / ST-11.01 — hash drift selectively invalidates.** Given an eligible decision whose independent-validation receipt is revoked, when invalidation runs, then that decision and its descendant projections become stale, state returns to deferred, and unrelated historical records remain replayable. Failure example: all archive evidence is deleted or the stale decision stays consumable. Evidence: invalidation receipt and before/after graph. Test layer: recovery/replay.
11. **FR-084 / ST-11.01 — historical replay is exact.** Given a prior decision receipt, when replay uses its recorded validator and input hashes, then decision, failed codes, and canonical hash match byte-for-byte. Failure example: current files are substituted silently. Evidence: replay receipt. Test layer: clean-environment/replay.
12. **FR-079 / ST-11.01 — concurrent projection cannot corrupt state.** Given two updates with the same expected version, when one commits first, then the second fails `FORMAT02_CONCURRENT_UPDATE` with no partial record/receipt pair. Failure example: state references a receipt whose record never committed. Evidence: atomicity test trace. Test layer: repository/concurrency.
13. **FR-079–FR-084 / ST-11.01 — portability.** Given a clean checkout at a different absolute path, when manifests and decisions validate, then hashes and decisions match. Failure example: a `D:\Work\...` locator changes the hash or passes validation. Evidence: clean-room matrix. Test layer: portability.
14. **FR-079 / claim ceiling — candidate authority is not current.** Given this written specification before ratification, when quality status is projected, then it is `WRITTEN_PENDING_AUDIT`, authority is `CANDIDATE_NOT_CURRENT`, build authority is false, and later acceptance cannot exceed `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. Failure example: a Development Capsule is issued. Evidence: lifecycle registry validation. Test layer: lifecycle/architecture.

## 10. Testing and completion evidence

After separately authorized implementation, the required test suite is:

- `CMF_PROGRAM_CONTROL/tests/format02/test_deferral_gate.py`
  - `test_missing_harness_denies_activation`
  - `test_complete_evidence_yields_eligibility_without_execution`
  - `test_self_validation_is_rejected`
  - `test_stale_evidence_set_is_rejected`
- `CMF_PROGRAM_CONTROL/tests/format02/test_historical_evidence.py`
  - `test_thirteen_families_complete_or_explicit_gap`
  - `test_historical_program_cannot_become_current`
  - `test_observation_and_inference_are_distinct`
  - `test_registration_and_receipt_commit_atomically`
- `CMF_PROGRAM_CONTROL/tests/format02/test_aliases.py`
  - `test_historical_alias_resolves_with_receipt`
  - `test_new_active_alias_emission_is_rejected`
  - `test_unknown_and_ambiguous_aliases_fail_closed`
- `CMF_PROGRAM_CONTROL/tests/format02/test_claim_ceiling.py`
  - `test_synthetic_output_cannot_support_real_output_claim`
  - `test_contract_compatibility_cannot_imply_certification`
  - `test_activation_eligibility_cannot_imply_production`
- `CMF_PROGRAM_CONTROL/tests/format02/test_replay_and_invalidation.py`
  - `test_replay_is_byte_identical`
  - `test_revocation_selectively_invalidates_descendants`
  - `test_unrelated_history_remains_reproducible`
  - `test_concurrent_update_has_no_partial_commit`
- `CMF_PROGRAM_CONTROL/tests/format02/test_portability.py`
  - `test_absolute_paths_are_rejected`
  - `test_clean_checkout_preserves_hashes_and_decisions`
- affected Builder regression: `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_06_02/test_profile_compilation.py` and `test_profile_failures.py`, run unchanged;
- architecture scan proving no active Pipeline/Studio/VAE route, binding, benchmark, production, or certification claim exists while deferred;
- migration validation proving every imported historical artifact retains original bytes, ID, receipt, and class;
- clean-environment execution with only manifest-declared inputs and no machine-specific environment variables.

Completion evidence must include: test-result JSON, exact source and test hash matrix, 13-family inventory/gap report, canonical serialization vectors, concurrency/atomicity trace, replay matrix, selective-invalidation graph, alias receipts, claim-ceiling denials, architecture absence scan, and an independent audit report from an agent other than the writer.

A later Build Receipt, if ever authorized, must name the ratified authority, adopted spec hash, Development Capsule, implementation commit, test hashes, independently validated Harness, exact activation scope, unresolved blockers, and maximum claim. This specification issues none of those artifacts. Its current terminal state is `WRITTEN_PENDING_AUDIT`; `CANDIDATE_NOT_CURRENT`; `specification_work_authorized: true`; `build_authority: false`; `later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.
