---
type: technical_specification
spec_id: TS-AIR-001
title: Constitutional Authority, Activation Domains, and Epistemic State
product: Activative Intelligence Runtime
version: 2.1.0-candidate
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
document_class: CANDIDATE_CANONICAL_TECH_SPEC
output_path_class: DIRECT_PRODUCT_SPEC_PATH
gate: GATE_A_CONSTITUTIONAL_AND_CONTRACT_FOUNDATION
writing_wave: 0
controlling_frs:
  - AIR-FR-001
  - AIR-FR-002
  - AIR-FR-003
  - AIR-FR-004
  - AIR-FR-005
  - AIR-FR-006
controlling_stories:
  - AIR-ST-01.01
  - AIR-ST-01.02
  - AIR-ST-01.03
---

# TS-AIR-001 — Constitutional Authority, Activation Domains, and Epistemic State

This candidate specification is authorized for writing by `CA-P02C-SPEC-WORK-AUTH-2026-07-22`. The V2.1 authority package remains `CANDIDATE_NOT_CURRENT`; this document does not adopt that candidate as current authority, authorize implementation, issue a Development Capsule, or confer production or certification status.

## 1. Files and authorities read

| Authority class | Exact path | Version/state | SHA-256 | Use |
|---|---|---|---|---|
| Candidate constitutional authority | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/doctrine/00_ACTIVATIVE_INTELLIGENCE_LIFECYCLE_CONSTITUTION_V2_1.md` | `2.1.0-draft`, pending ratification | `abdb79fa6a59b4651332cd86cf51f796a4468110c917c126c62760e3f1d58a85` | Activation domains, epistemic states, immutable history, evidence ceilings, and product sovereignty. |
| Candidate authority pointer | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CURRENT_AUTHORITY.md` | `DRAFT_FOR_HUMAN_RATIFICATION` | `493fd0f21661ca136e72e1136586703be9c48e443a4dd5056d0413ba18501bf0` | Confirms candidate status and separate implementation authorization. |
| Controlling PRD feature | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/prd/features/F01-constitutional-authority-activation-domains-and-epistemic-state.md` | `2.1.0-draft` | `f37dee0f59abecb8f975a8a69cce796d7ca6cea30165972e18de443740fd6a76` | AIR-FR-001 through AIR-FR-006 and the F01 terminal condition. |
| Controlling Stories | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/planning/EPICS_AND_VERTICAL_STORIES.md` | `2.1.0-draft` | `b74fa0d6e4357662b021d92e45e2436b25005c88d4c45bdb8df2010592fd7da0` | AIR-ST-01.01 through AIR-ST-01.03, adversarial and recovery behavior. |
| Source draft/assignment | `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/specs/TS-AIR-001-constitutional-authority-activation-domains-and-epistemic-state.md` | `DRAFT_AFTER_PRD_PENDING_RATIFICATION` | `96e2f2b5233372c3bc7c133ac980943b2ae8bd1fd171866c8b6130ca346643c5` | Brownfield proposal amended to the V3.3 ten-section contract. |
| Cross-product authority | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | AIR owns semantic lifecycle; Interview Expression owns live evidence; Pipeline executes. |
| Semantic ownership | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | One authoritative owner per semantic object or field. |
| Source disposition | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_RECONCILIATION/SOURCE_DISPOSITION_LEDGER.yaml` | validated | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | Required sources are available; deferred references cannot support claims. |
| Specification-work authorization | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active, specification only | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | Authorizes WRITE and later technical review, but not build. |
| Authority-stage decision | `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/AUTHORITY_STAGE_DECISION.yaml` | ratification pending | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | Sets the pre-ratification ceiling. |
| Exact Primitive source | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/psychological_diagnostics/PRM-PSY-008.yaml` | `PRM-PSY-008` | `1f63263ab6e0178e3c62feda7bfc5951ea02f1dd8bdafa96b15efd0a0381cfeb` | Dignity-preserving correction and its misuse modes. |
| Exact Primitive source | `.../sources/cmf_primitive_registry_snapshot/meaning_plane/visual_sonic_guidance/PRM-VSG-003.yaml` | `PRM-VSG-003` | `2be2e140588e23e43b4461c9443884b09401f6541ea29bdbae8e945e4672e30c` | Intent-governed representation and anti-laziness constraint. |
| Exact Primitive source | `.../sources/cmf_primitive_registry_snapshot/experience_plane/feedback_scoring/EXP-FBK-001.yaml` | `EXP-FBK-001` | `ef888d832e745444a7fcf80192548f89a40abadc77e9653bd7c76ff966cae8ec` | Relevant, immediate, meaningful transition feedback. |
| Brownfield implementation | `.../reference_implementation/activative_intelligence_v2/lifecycle.py` | predecessor | `74ea3fb8d1ccad2aea76c9b2b2947aa2bc863001149e97d7977dd6746fe2b79b` | Global lifecycle graph and transition denial. |
| Brownfield implementation | `.../reference_implementation/activative_intelligence_v2/models.py` | predecessor | `d75529f08416db1648e95e6762c273aa18fd9f56bbe6c4a6805efbae3909a3b3` | Frozen Pydantic models and the current domain/epistemic enumerations. |
| Brownfield tests | `.../tests/test_invariants.py` | predecessor | `406259921ae8086059dc867c8a4cddb45f32741f773279689859293c34501803` | Transition and non-compensable-gate evidence; no F01 end-to-end proof. |

The `...` paths in the last six rows expand beneath `CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE/CONSCIOUS_ACTIVATIONS_ACTIVATIVE_INTELLIGENCE_RUNTIME_V2_1_FULL_BUNDLE`. The writer used no upstream spec draft: Wave 0 has no `upstream_write_inputs`. Deferred external sources were not used and support no factual claim in this document.

## 2. Problem, user outcome, solution, and scope

### Problem and outcome

Without F01, a planned brief field can be passed downstream as if it were observed human truth, a relationship inference can be consumed as audience evidence, or a semantic update can overwrite the history it depends on. The operator must instead be able to inspect every material claim's activation domain, epistemic state, owner, evidence, version, and lifecycle consequence before a consumer uses it.

### Bounded solution

Implement an immutable F01 domain kernel and service that:

1. declares exactly one primary domain from `source`, `relationship`, `audience`, `campaign`, or `derivative`;
2. attaches field-level epistemic assertions without flattening object fields into one status;
3. creates additive semantic object versions and explicit supersession edges;
4. rejects observed-state claims without direct source evidence;
5. preserves typed cross-domain lineage; and
6. issues deterministic and independent evaluation receipts before downstream eligibility.

### In scope

- typed immutable domain, assertion, version, command, event, and receipt contracts;
- canonical serialization and SHA-256 identity;
- optimistic concurrency, idempotent commands, atomic object/edge/receipt commits;
- descendant-only invalidation and historical replay;
- exact authority and actor attribution;
- migration from the named V2 predecessor models without inventing missing classifications;
- typed handoff eligibility for F02 and named cross-product consumers.

### Out of scope and non-goals

- ratifying the V2.1 candidate or issuing build authority;
- live interviewing, Reaction Observation, Reaction Receipt, or Expression Moment resolution;
- Primitive, archetype, Final Script, composition, rendering, VAE production, Pipeline execution, or Studio canonical-state ownership;
- a generic agent that owns validation, evaluation, authorization, and mutation;
- activation of Format 02 or VAE Stage 5;
- treating the Activative Contract Compiler as the Activative Intelligence Runtime;
- inferring production effectiveness from schema, unit, or synthetic evidence.

## 3. Governing decisions and constraints

### Product sovereignty and ownership

Program Control owns ratification, cross-product status, and release claims. AIR owns semantic activation lifecycle meaning, but the authorized human remains the canonical value owner of Coach/Guest Identity DNA. Interview Expression owns live source observations and resolved Reaction Receipts/Expression Moments. Builder declares semantic dependencies; Pipeline executes approved programs; Delegation transports typed messages; VAE realizes typed visual demands; Studio projects state and captures attributed `HumanResolutionEpisode` objects. None may silently repair an AIR-owned semantic object.

`Activative Contract Compiler != Activative Intelligence Runtime` is a hard identity invariant.

### Epistemic and lineage laws

- Every material assertion is exactly one of `planned`, `observed`, `inferred`, `operator_confirmed`, `rejected`, or `superseded`.
- `observed` requires direct admitted evidence. A Brief, hypothesis, intended role, model score, or planned tag cannot satisfy it.
- `operator_confirmed` requires an attributable human-resolution reference and cannot retroactively convert invented history into observation.
- `rejected` and `superseded` records remain retrievable as negative or historical evidence.
- A handoff preserves source object refs, transformation refs, owner, evaluation receipt, limitations, and invalidation edges.
- Missing imported history is `absent`; migration must not guess domain or epistemic state.

### Primitive application

`PRM-PSY-008` governs blocker language: identify the defective assertion or transition, never label the person. `PRM-VSG-003` requires every projection field to serve truth-state inspection rather than visual ceremony. `EXP-FBK-001` requires a transition denial or success receipt to state why the action mattered and the next admissible action; it does not authorize vanity scores or interrupt a live recording path.

### Claim ceiling and forbidden behavior

The output state is `WRITTEN_PENDING_AUDIT`. Candidate authority is `CANDIDATE_NOT_CURRENT`, specification work is authorized, build authority is false, and the pre-ratification ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`. No acceptance, Development Capsule, implementation, production, or certification claim is created here.

## 4. Current brownfield architecture

| Exact predecessor path | Actual behavior | Disposition | Reason and migration constraint |
|---|---|---|---|
| `.../reference_implementation/activative_intelligence_v2/models.py::ActivationDomain` | Frozen enum contains only `source`, `relationship`, and `audience`. | `ADAPT` | Preserve wire values; add `campaign` and `derivative` in the V2.1 contract. Do not coerce unknown legacy values. |
| `.../models.py::EpistemicState` | Defines all six candidate states. | `REUSE` | Preserve exact wire values; strengthen evidence conditions in the F01 validator. |
| `.../models.py::StrictModel` | Pydantic `extra=forbid`, frozen models. | `REUSE` | Keep strict/frozen behavior; canonical hash rules remain separate and explicit. |
| `.../models.py::ImmutableRef` | Object ID, version, lowercase SHA-256 shape, derived URI. | `REUSE` | Continue validating references; reference equality includes all three fields. |
| `.../lifecycle.py::_ALLOWED` and `require_transition` | One global lifecycle state graph with typed denial. | `ADAPT` | Keep deterministic denial but separate F01 object eligibility from unrelated production states. |
| `.../lifecycle.py::TransitionReceipt` | Frozen receipt with object, prior/next state, reason, evidence refs, actor, timestamp. | `ADAPT` | Add command ID, expected version, authority, result hash, blocker, and canonical receipt hashing; timestamp is supplied, not generated inside deterministic compilation. |
| `.../tests/test_invariants.py` | Proves some invalid transitions and non-compensable evaluation behavior. | `ACTIVATE` | Retain as predecessor regression; add exact F01 schema, concurrency, replay, migration, and boundary tests. |
| Historical prose/prompt summaries | May describe intended semantics without executable identity. | `ARCHIVE` | Preserve as evidence only; they cannot become source or current authority. |

No current `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/` tree exists. Paths below are proposed implementation targets only; this specification does not create them and is not a path allowlist for build.

## 5. Proposed architecture and workflows

### Components

| Component | Responsibility | Must not do |
|---|---|---|
| `domain/authority.py` | Typed domains, epistemic assertions, object versions, actor/authority refs. | Read providers, infer evidence, or mutate storage. |
| `serialization/canonical.py` | UTF-8 canonical JSON, sorted keys, normalized enums/decimals, SHA-256. | Include local paths, clocks, random values, or environment data. |
| `services/semantic_authority_service.py` | Validate commands, optimistic version, domain, epistemic evidence, lifecycle legality, and downstream eligibility. | Self-evaluate or bypass repository transaction. |
| `repositories/semantic_object_repository.py` | Atomic append of artifact, command, edges, receipt, and idempotency record. | Update or delete historical versions. |
| `evaluation/f01_evaluator.py` | Independent domain-fit, epistemology, lineage, lifecycle, and claim-ceiling receipt. | Produce or mutate the evaluated object. |
| `invalidation/descendant_projector.py` | Traverse typed dependency edges and append stale projections. | Invalidate unrelated or historical evidence. |
| `adapters/v2_semantic_adapter.py` | Convert supported V2 objects and block ambiguous ones. | Invent `campaign`, `derivative`, evidence, or absent epistemic state. |

### Commands, events, and state transitions

- `DeclareSemanticObjectCommand` creates version 1 only when `expected_prior_version_ref` is absent and `command_id` has no different prior payload.
- `SupersedeSemanticObjectCommand` requires the exact current version, a changed canonical content hash, and reasons/evidence for every changed material field.
- `EvaluateSemanticObjectCommand` is handled by the independent evaluator identity; producer identity equality is rejected.
- Successful transactions append `SemanticObjectDeclared`, `SemanticObjectSuperseded`, `DescendantsInvalidated`, and/or `DownstreamEligibilityGranted` events with one `LifecycleTransitionReceipt`.
- A failed precondition appends a typed command-result receipt without storing a new semantic artifact.

The F01 lifecycle is `proposed -> validated -> evaluated -> downstream_eligible`, with terminal branches `rejected`, `superseded`, and `cancelled`. Only `evaluated -> downstream_eligible` is allowed after every non-compensable gate passes. Supersession never rewrites a prior state.

### Atomicity, idempotency, replay, and cancellation

The repository commits the new version, assertions, dependency edges, command record, and transition receipt in one transaction. If any write fails, none becomes visible. Replaying the same `command_id` and payload hash returns the original receipt; the same ID with a different hash returns `AIR_F01_IDEMPOTENCY_CONFLICT`. Optimistic concurrency compares `expected_prior_version_ref` to the current head. Cancellation before commit emits `AIR_F01_CANCELLED_NO_COMMIT`; cancellation after commit returns the committed receipt and cannot erase state. Replay rebuilds projections from immutable artifacts and events, never from mutable cache.

## 6. Data models, contracts, schemas, and APIs

All schemas use `additionalProperties: false`; arrays that express sets are sorted by canonical reference URI and unique; empty strings are invalid. Schema identities are prospective until ratification and build authorization.

### Shared types

| Type | Exact shape and owner |
|---|---|
| `ImmutableRef` | `{object_id: NonEmptyString, version: SemVer, sha256: LowerHex64}`; owning object producer. |
| `AuthorityRef` | `{authority_id: NonEmptyString, authority_version: NonEmptyString, authority_sha256: LowerHex64, authority_state: current | candidate_not_current}`; Program Control. |
| `ActorRef` | `{actor_id: NonEmptyString, actor_type: deterministic_module | model_program | human, product_id: NonEmptyString, workflow_role: hunter | analyst | composer | commander | evaluator | operator}`; invoking product. |
| `EvidenceRef` | `{ref: ImmutableRef, evidence_class: direct_source | operator_resolution | deterministic_validation | independent_evaluation | historical_negative, source_span: NonEmptyString?}`; evidence owner. |

### `ActivationDomainDeclaration` — `ca.air.activation-domain-declaration/2.1.0`

| Field | Type | Owner / validation |
|---|---|---|
| `declaration_id` | `NonEmptyString` | AIR-generated stable identity. |
| `semantic_object_ref` | `ImmutableRef` | Producer-owned object; hash must resolve. |
| `primary_domain` | `source | relationship | audience | campaign | derivative` | AIR F01; exactly one. |
| `cross_domain_handoffs` | `tuple<CrossDomainHandoffRef>` | Each target domain differs from primary and has a typed contract ref. |
| `owner_product_id` | `NonEmptyString` | Must match the ownership registry. |
| `authority_ref` | `AuthorityRef` | Candidate state must remain visible. |
| `declared_by` | `ActorRef` | Attributed producer. |

`CrossDomainHandoffRef` is `{target_domain, handoff_contract_ref, transformation_receipt_ref}`. A second primary domain, unknown domain, or untyped domain mention is rejected.

### `EpistemicAssertion` — `ca.air.epistemic-assertion/2.1.0`

| Field | Type | Validation |
|---|---|---|
| `assertion_id` | `NonEmptyString` | Unique within the semantic object version. |
| `subject_ref` | `ImmutableRef` | Exact object version being asserted. |
| `field_pointer` | RFC 6901 JSON Pointer | Resolves to one material field. |
| `value_sha256` | `LowerHex64` | Hash of the canonical field value. |
| `epistemic_state` | six-state enum | Exactly one state. |
| `evidence_refs` | `tuple<EvidenceRef>` | Nonempty for `observed` and `operator_confirmed`; direct source required for `observed`. |
| `confidence_micros` | integer `0..1000000` or null | Required only for `inferred`; fixed integer avoids float serialization drift. |
| `operator_resolution_ref` | `ImmutableRef?` | Required only for `operator_confirmed`. |
| `supersedes_assertion_ref` | `ImmutableRef?` | Required for `superseded`. |
| `rejection_reason_code` | `NonEmptyString?` | Required for `rejected`. |

An object-level lifecycle state cannot substitute for these field assertions. A direct-source evidence record carries the source authority and span; a model-produced interpretation remains `inferred` even when confidence is high.

### `SemanticObjectVersion` — `ca.air.semantic-object-version/2.1.0`

Required fields are `object_id`, `version`, `content_sha256`, `schema_id`, `schema_version`, `domain_declaration_ref`, nonempty `epistemic_assertion_refs`, `source_refs`, `transformation_refs`, `owner_product_id`, `authority_ref`, `produced_by`, `lifecycle_state`, `evaluation_receipt_refs`, `supersedes_ref`, and `created_at_utc`. `supersedes_ref` is absent only at version 1. `created_at_utc` is caller-supplied RFC 3339 UTC evidence and is excluded from semantic content identity but included in the receipt identity.

### Commands and receipts

`DeclareSemanticObjectCommand` and `SupersedeSemanticObjectCommand` require `command_id`, `payload_sha256`, `expected_prior_version_ref`, `candidate_object`, `actor`, `authority_ref`, and `submitted_at_utc`. `LifecycleTransitionReceipt` requires command and payload hashes, prior/result refs, transition, gate results, committed artifact/edge refs, typed blocker or null, evaluator ref, authority ref, and receipt hash.

`TypedBlocker` is `{code, responsible_owner, failed_invariant, evidence_refs, next_admissible_action}`. Codes include `AIR_F01_DOMAIN_AMBIGUOUS`, `AIR_F01_DOMAIN_UNKNOWN`, `AIR_F01_EPISTEMIC_STATE_MISSING`, `AIR_F01_OBSERVED_WITHOUT_DIRECT_EVIDENCE`, `AIR_F01_OPERATOR_CONFIRMATION_UNATTRIBUTED`, `AIR_F01_STALE_EXPECTED_VERSION`, `AIR_F01_IDEMPOTENCY_CONFLICT`, `AIR_F01_SELF_EVALUATION`, `AIR_F01_LINEAGE_GAP`, and `AIR_F01_MIGRATION_AMBIGUOUS`.

Canonical serialization is I-JSON UTF-8 with lexicographically sorted object keys, preserved array order unless the schema declares set semantics, no insignificant whitespace, Unicode NFC, enums as exact wire strings, timestamps normalized to `Z`, and no NaN/Infinity. `content_sha256` is computed over the object with identity/hash and receipt-only time fields omitted. Positive example: a `planned` field with a Brief evidence ref remains planned. Negative example: the same Brief presented as evidence for `observed` returns `AIR_F01_OBSERVED_WITHOUT_DIRECT_EVIDENCE` and creates no semantic version.

## 7. Implementation stages and exact target paths

These paths are proposed for a future, separately authorized build.

| Stage | Exact target paths | FR / Story evidence |
|---|---|---|
| 1. Strict contracts | `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/src/cmf_activative_intelligence/domain/authority.py`; `.../contracts/schemas/activation_domain_declaration.schema.json`; `.../epistemic_assertion.schema.json`; `.../semantic_object_version.schema.json` | AIR-FR-001–003; AIR-ST-01.01–02; schema fixtures. |
| 2. Canonical identity | `.../src/cmf_activative_intelligence/serialization/canonical.py` | AIR-FR-003/005; deterministic cross-process hash tests. |
| 3. Service/repository | `.../services/semantic_authority_service.py`; `.../repositories/semantic_object_repository.py` | AIR-FR-003–005; concurrency, idempotency, atomicity, replay. |
| 4. Independent evaluation | `.../evaluation/f01_evaluator.py` | AIR-FR-006; producer/evaluator separation and non-compensable gates. |
| 5. Invalidation/handoffs | `.../invalidation/descendant_projector.py`; `.../adapters/f01_handoff.py` | AIR-FR-005; typed lineage and descendant-only invalidation. |
| 6. Migration | `.../adapters/v2_semantic_adapter.py`; `.../migrations/v2_to_v21_f01.py` | AIR-FR-002–004; no guessed domain or evidence. |
| 7. Evidence suite | exact paths in section 10 | All six FRs, all three Stories, and F02 downstream denial proof. |

Every stage remains `NOT_BUILD_READY` until ratification or attributable product adoption, independent audit/re-audit, and a separately issued Development Capsule name exact files and evidence.

## 8. Failure, migration, rollback, recovery, and observability

Deterministic validation failures are not retried. Transient repository unavailability may be retried with the same command ID; quality repair uses a new command ID and preserves the failed receipt. Late evaluator results are accepted only for the exact evaluated object hash and evaluator contract version. A cancellation racing with commit resolves from the transaction record as defined in section 5.

The V2 adapter preserves known enum values and hashes the exact source bytes. V2 `ActivationDomain` supports only three values, so campaign/derivative classification must be provided by an attributable migration decision; otherwise migration emits `AIR_F01_MIGRATION_AMBIGUOUS`. Missing field epistemic states remain absent and block downstream eligibility. Migration creates new immutable V2.1 artifacts and migration receipts; it never changes V2 bytes.

Rollback switches service, schema, or adapter bindings to the last known-good version while retaining every artifact and incident produced under the failed binding. Recovery rebuilds current-head, eligibility, and stale projections from artifacts/events, verifies receipt hashes, and compares the rebuilt projection hash with the stored checkpoint. Superseding an upstream object appends invalidation receipts for reachable typed descendants only; historical results remain reproducible with their original dependency versions.

Required observability includes counters for blocker code, domain, epistemic state, migration outcome, idempotent replay, stale-version conflict, and invalidated-descendant count; histograms for validation/commit/evaluation latency; and append-only structured logs with command, object, version, authority, actor, evaluator, and receipt refs. Logs exclude raw private source content. Alerts fire on orphan artifact/receipt pairs, hash mismatch, self-evaluation attempts, failed replay equivalence, or an observed assertion lacking direct evidence.

## 9. Behavior-specific acceptance criteria

1. **AIR-FR-001 / AIR-ST-01.01 — one domain.** Given a derivative object declaring `primary_domain: derivative` and a typed source handoff, when declaration validation runs, then one version and receipt commit. Given both `source` and `derivative` are presented as primary, then `AIR_F01_DOMAIN_AMBIGUOUS` commits only a denial receipt. Evidence: contract fixtures and integration receipt; layer: schema + integration.
2. **AIR-FR-002 / AIR-ST-01.01 — field epistemology.** Given planned premise text and observed pause evidence on separate field pointers, when validated, then both states remain distinct. Given the object has only one aggregate `observed` status, then `AIR_F01_EPISTEMIC_STATE_MISSING` denies eligibility. Evidence: assertion map and negative fixture; layer: unit + contract.
3. **AIR-FR-003 / AIR-ST-01.02 — additive supersession.** Given version 1 and its exact expected ref, when a supported semantic change is submitted, then version 2 points to version 1 and both replay. Given stale version 1 is submitted after version 2 exists, then `AIR_F01_STALE_EXPECTED_VERSION` creates no artifact. Evidence: repository transaction log and replay hash; layer: integration.
4. **AIR-FR-004 / AIR-ST-01.02 — no manufactured observation.** Given a Brief says a guest would express fear but no direct source span exists, when `observed` is requested, then `AIR_F01_OBSERVED_WITHOUT_DIRECT_EVIDENCE` blocks it. A high model confidence does not change this. Evidence: adversarial fixture and blocker receipt; layer: contract + integration.
5. **AIR-FR-005 / AIR-ST-01.03 — cross-domain lineage.** Given a source object handed to a derivative program, when the handoff is compiled, then all origin and transformation refs, owner, authority, and invalidation edges survive. Given a generic note replaces a required ref, then `AIR_F01_LINEAGE_GAP` blocks the handoff. Evidence: producer/consumer conformance receipt; layer: integration.
6. **AIR-FR-006 / AIR-ST-01.03 — independent receipt.** Given deterministic gates pass and a distinct evaluator passes domain fit, epistemology, lifecycle, and claim ceiling, when eligibility is requested, then `downstream_eligible` is emitted. Given producer and evaluator identities match or any hard gate fails, then `AIR_F01_SELF_EVALUATION` or the gate-specific blocker prevents eligibility. Evidence: evaluator receipt pair; layer: architecture + integration.
7. **Recovery boundary.** Given an upstream object is superseded, when dependency traversal runs, then only reachable typed descendants become stale and unrelated products remain eligible. Evidence: graph fixture, invalidation receipt, old/new replay hashes; layer: recovery.
8. **Idempotency and atomic rollback.** Given an identical command is delivered twice, when handled, then both calls return one stored receipt and one artifact. Given the receipt write fails during a transaction, then artifact, assertions, edges, and command record are all absent. Evidence: fault-injection transaction test; layer: repository integration.
9. **Migration boundary.** Given a V2 source object with no attributable campaign/derivative classification, when migrated, then the adapter blocks instead of guessing. Given an exact supported domain and field evidence are supplied, then a new V2.1 artifact cites both original bytes and migration decision. Evidence: migration fixtures and receipt; layer: migration.
10. **Claim ceiling.** Given all local tests pass while ratification is pending, when status is projected, then it may report implementation evidence only after build authorization and can never report `ACCEPTED_FOR_BUILD`, production, or certification from this spec. Evidence: status-boundary test; layer: architecture.

Every criterion includes positive, negative, boundary, recovery, or observability evidence; none grants acceptance during this writing prompt.

## 10. Testing and completion evidence

Future authorized implementation must create these exact tests:

- `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/tests/unit/domain/test_activation_domain_declaration.py`: all five domains, exactly-one rule, typed handoff.
- `.../tests/unit/domain/test_epistemic_assertion.py`: six states, direct-source evidence, operator attribution, fixed-point confidence.
- `.../tests/unit/serialization/test_f01_canonical_hash.py`: key-order, Unicode, timestamp, environment, and process independence.
- `.../tests/contract/test_air_f01_schemas.py`: valid/unknown/missing/extra/stale fixtures and generated-schema stability.
- `.../tests/integration/test_constitutional_authority_activation_domains_and_epistemic_state.py`: AIR-FR-001 through AIR-FR-006.
- `.../tests/integration/test_f01_atomic_commit_and_idempotency.py`: duplicate, conflicting duplicate, concurrent writer, injected commit failure.
- `.../tests/architecture/test_air_product_boundaries.py`: AIR does not own live observations, Pipeline execution, VAE production, or Studio canonical state; producer cannot self-evaluate.
- `.../tests/migration/test_air_v2_to_v21_f01.py`: supported mappings and ambiguity blockers without invention.
- `.../tests/recovery/test_air_f01_replay_and_invalidation.py`: replay equivalence, selective invalidation, rollback, and historical reproduction.
- `.../tests/clean_environment/test_air_f01_portability.py`: no absolute paths or environment-dependent output.
- `.../tests/reference_slice/test_f01_to_f02_denial.py`: F02 can reject a bad F01 object from public contract and receipts alone.

Completion evidence requires generated schemas and fixtures, two fresh-process full-suite passes, source compilation/type checks, canonical hash matrix, migration report, clean-environment report, architecture-boundary report, replay/invalidation report, and an independent evaluation receipt. A future Build Receipt must bind the ratified authority, accepted spec hash, Development Capsule, exact implementation/test hashes, and claim ceiling; this document does not issue it.

Final writer state: `WRITTEN_PENDING_AUDIT`. Post-write gate: `RATIFICATION_OR_PRODUCT_ADOPTION_REQUIRED`. Build authority and production eligibility remain false.
