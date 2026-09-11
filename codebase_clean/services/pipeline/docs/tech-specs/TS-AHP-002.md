# TS-AHP-002 - AtomicHarnessDefinition Intake and HarnessExecutionBindingManifest

```yaml
spec_id: TS-AHP-002
document_class: CANDIDATE_CANONICAL_TECH_SPEC
product: Atomic Harness Pipeline
primary_owner: Atomic Harness Pipeline
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
post_write_gate: INDEPENDENT_AUDIT_REQUIRED
writing_wave: 1
controlling_story: ST-03.01
controlling_frs: [FR-007, FR-008, FR-009, FR-010, FR-011, FR-012]
```

This is a specification-only candidate. It does not authorize implementation, a Development Capsule, product adoption, production, certification, or `ACCEPTED_FOR_BUILD`.

## 1. Files and authorities read

The writer consumed two Wave 0 drafts under the mandatory label `DRAFT_DEPENDENCY_NOT_ACCEPTED`:

| Upstream draft | State | SHA-256 | Role and revision impact |
|---|---|---|---|
| `05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs/TS-AHP-001.md` | `WRITTEN_PENDING_AUDIT` | `5e7fc914dbcfa330ffd903c318158639ca74dc8fcb68eafd9a172772aca89444` | Supplies the draft authority/status/source-admission interface. If it changes during audit, revisit sections 3, 5, 6, 8, 9, and 10. |
| `04_ACTIVATIVE_INTELLIGENCE_RUNTIME/docs/tech-specs/TS-AIR-001.md` | `WRITTEN_PENDING_AUDIT` | `622b32dc08259bc8148c60f5865359c6a76de37037103789ff1fda0f842c6cbc` | Supplies draft typed semantic-reference, domain, epistemic-state, lineage, lifecycle, and invalidation expectations. If it changes during audit, revisit sections 3, 5, 6, 8, 9, and 10. |

Neither draft is ratified authority. Settled current authority remains Constitution V1.1 and current product PRDs. The drafts are readable interface inputs for dependency-safe writing only.

| Source | Version/state | SHA-256 | Authority/dependency class | Specific fact used |
|---|---|---|---|---|
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/CONSTITUTIONAL_AUTHORITY.md` | current pointer | `f3c4da2a890a682b6f2882ef69949a2bca5d9fcc4923ec74edf0426754e3927b` | required current authority | Constitution V1.1 wins over subordinate implementation or legacy doctrine. |
| `CMF_PROGRAM_CONTROL/00_CONSTITUTION/current-v1.1/docs/00_ACTIVATIVE_SYSTEM_CONSTITUTION.md` | V1.1 | `21c2286c700332ca81166a9e70e4ae7066f2695b383e7b8a73876c028549d70b` | highest-order authority | Builder compiles Harnesses, Pipeline executes them, and neither may replace the Activation Compiler or invent upstream meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | candidate pending ratification | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | candidate ownership | Builder owns `AtomicHarnessDefinition`; Pipeline executes approved Harnesses; VAE, Interview Expression, AIR, Delegation, and Studio retain their own authority. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | candidate pending ratification | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | candidate object ownership | Pipeline references AIR and Interview objects and cannot become their value owner. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py` | current Builder implementation | `8d4d174eb3c54f152a099053302dd631f686c27b070b7dde989c4901afd8e4c6` | `SRC-CUR-004`; required current implementation | Builder's detailed synthetic definition is immutable, canonical-hashed, execution-free, explicitly non-production/non-certified, and carries 20 governed sections plus lineage and invalidation. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/portable_export.py` | current Builder implementation | `30350ca3749de43bd484b826820900d12970e3068e39e22094ec64e4c269f52b` | directly applicable current implementation | The productized portable definition uses the same schema ID/version but a different compiler profile and exact content shape; it rejects machine-local paths and preserves structured Activative references. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/export_service.py` | current Builder implementation | `930bfbac02dbbd1c8ec98c6490bff574fe095fa37a26225eb22ea1948d30d074` | directly applicable current implementation | Export produces a deterministic ZIP containing `atomic_harness_definition.json`, `package_manifest.json`, `export_receipt.json`, and `SHA256SUMS`, with production/certification false. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py` | current Builder implementation | `14ba709cf693c117560cb4f326b9a5708391475aabe1c2030ce69b20283ee36e` | `SRC-CUR-008`; required current implementation | Capability decisions use explicit owner kinds and require evidence, authority boundaries, and ordered participants/handoff responsibility for non-code owners. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py` | current Builder implementation | `9dc8aaf8aa2085aff66adda56faf891fc260287e04e0ca0c35681934126e4399` | `SRC-CUR-010`; required current implementation | Workflow nodes have one explicit actor kind/owner, typed handoffs, validations, failure ownership, cancellation behavior, and no external execution. |
| `01_ATOMIC_HARNESS_BUILDER/tests/productization/integration/test_pz04_end_to_end.py` | current Builder test | `a1ae85f11ce989a1bb3f2032d66198ab2fdc95034982458a05c772bea4761c46` | current behavior evidence | Generic/Activative definitions are deterministic; exported packages are byte-identical and portable; altered definition bytes fail closed; failed export preserves the historical destination. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_07_02/test_replay_invalidation_and_receipt.py` | current Builder test | `764aeb785adc30e9411ecf1181fd1157d1a47d342d8efce6ac88b8917f6d7ba4` | current behavior evidence | Repeated compile is payload-safe, upstream reopen invalidates the active definition, and historical definition bytes remain reproducible. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_09_01/test_actor_explicit_workflow.py` | current Builder test | `1996273d226da7f2f233912b2dafa7626e3acc3d1beaa006e5f20aa05ac9fce9` | current behavior evidence | Mixed ownership, hidden external execution, unvalidated handoffs, cycles, and human-decision replay fail closed. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/studio_pipeline_recipe_harness.py` | predecessor source | `fd9a613463c71c9e0f1a0ce3b4ba0cd479b7553ead53a50d6d678d72386e81b8` | `SRC-LEG-001`; required unique evidence | Legacy recipe/run types are useful compatibility evidence but contain old route IDs, random IDs, clock defaults, and open fields, so they cannot define current Harness meaning. |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | active specification-only authorization | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | WRITE authorization | Writing and technical convergence are allowed while implementation/build/production/certification remain forbidden. |

The exact output path is authorized as `DIRECT_PRODUCT_SPEC_PATH`. No target-local or ancestor `AGENTS.md` exists. The older assignment path under `04_ATOMIC_HARNESS_PIPELINE` is superseded by the Prompt 02 canonical path under `05_ATOMIC_HARNESS_PIPELINE`.

## 2. Problem, user outcome, solution, and scope

### Problem

Builder emits an immutable, execution-free `AtomicHarnessDefinition`; Pipeline must select concrete runtime embodiments without creating a second Harness truth. A naive deserializer could accept altered package bytes, flatten lineage, silently choose one of two current Builder compiler profiles sharing the same schema ID, resolve an ambiguous capability to an arbitrary actor, import legacy recipe semantics, or change purpose, phases, creative degrees of freedom, and wrong-reading locks while claiming to perform implementation binding. That would produce duplicate jobs, stale source grants, hidden actors, conflicting outputs, and untraceable production spend.

### User and system outcome

A Pipeline operator can ingest an exact portable Builder package, prove all package and Harness identities, reconcile every required graph element, and compile one immutable `HarnessExecutionBindingManifest` that maps requirements to eligible implementations without copying or mutating semantic authority. Unresolved, stale, invalidated, incompatible, or ownership-ambiguous inputs fail before any side effect. Accepted and denied decisions are replayable by exact bytes.

### Bounded solution

Define an intake and binding subsystem that:

1. safely opens the portable package and verifies its manifest, sums, export receipt, definition envelope, content identity, authority, category/profile, lineage, and invalidation state;
2. selects an exact `HarnessDefinitionCompilerProfile` using schema ID, schema version, compiler ID, and compiler version together, never schema ID alone;
3. projects the immutable Harness graph into typed requirement references without changing values;
4. resolves each executable requirement to exactly one eligible deterministic module, Model Program, Agent Program, human gate, external-product route, or runtime embodiment;
5. verifies contracts, capability ownership, actor identity, context, Skill, evaluation, repair, cancellation, idempotency, and side-effect boundaries;
6. atomically emits a versioned binding manifest and compilation receipt while leaving Builder-owned bytes unchanged.

### In scope

- FR-007 through FR-012 and ST-03.01.
- Portable package safety, identity, and compatibility-profile validation.
- Complete graph reconciliation and immutable execution-binding compilation.
- Capability/actor/product ownership resolution and pre-side-effect denial.
- Supersession, revocation, migration impact, invalidation, replay, rollback, and historical reproduction.
- Exact proposed contracts, source paths, and tests.

### Out of scope and non-goals

- Editing, recompiling, or improving `AtomicHarnessDefinition` in Pipeline.
- AIR semantic compilation, live source/reaction evidence creation, Builder compilation, VAE production planning, Delegation transport, Studio correction, or provider/renderer execution.
- Treating the binding as a new source of purpose, phase semantics, Primitive/archetype meaning, approved Final Script, Composition Intent, Feature Contract intent, T/V routes, or wrong-reading locks.
- Running any bound implementation during intake or binding compilation.
- Activating Format 02, VAE Stage 5, production, certification, signing, publication, or external spend.
- Maintaining backward compatibility through silent coercion or guessed defaults.

## 3. Governing decisions and constraints

### Current versus candidate authority

Current Constitution V1.1 and current product PRDs remain binding. V2.1 authority/ownership material and both upstream specs are `CANDIDATE_NOT_CURRENT`. Their interfaces may guide this draft because specification work is explicitly authorized, but any audit change to their recorded hashes reopens sections 3, 5, 6, 8, 9, and 10. The spec remains `WRITTEN_PENDING_AUDIT`; build authority is false and the pre-ratification acceptance ceiling is `TECHNICALLY_ACCEPTED_PENDING_RATIFICATION`.

### Product sovereignty

- Builder is the sole owner/compiler of `AtomicHarnessDefinition`. Pipeline stores an exact imported copy/reference and a binding; it never becomes Builder.
- AIR owns semantic lifecycle and production-program meaning: epistemic state, Matrix of Edging, psychological role inside a tension, exact Primitive IDs/Bindings, Primitive Coalition Contract, Coalition Signature, Edge Product, Primitive Misuse Risk, archetype coalition, approved Final Script, Activation Transfer Contract, Composition Intent, Brand Context Version, Guest Voice DNA, Visual DNA, and other governed semantic objects.
- Interview Expression owns live source, Reaction Receipts, Expression Moments, and the Canonical Interview Source Package.
- Pipeline owns implementation selection, execution state, scheduler/runtime handoff, evaluation/repair coordination, and receipts, subject to the Harness.
- VAE owns visual-production strategy and realization. Delegation transports immutable messages. Studio projects state and issues typed commands. External models/renderers are embodiments, never sources of meaning.
- `Activative Contract Compiler != Activative Intelligence Runtime`.

### Immutable semantic boundary

The binding contains typed references and implementation choices, not copied editable Harness semantics. It must not introduce an override field for goal, purpose, success condition, atomic boundary, category/profile, phase meaning, acceptance tests, creative degrees of freedom, authority chain, semantic lineage, wrong-reading locks, evaluation requirements, or repair law. A `semantic_projection_digest` is recomputed from the imported definition and stored only as an equality guard. Any competing value causes `AHP_BIND_SEMANTIC_MUTATION_ATTEMPT`.

Content-bearing Harnesses retain exact AIR and Interview semantic refs, including epistemic state and lineage. Pipeline validates presence/version/hash and ownership but does not upgrade planned/inferred content to observed/operator-confirmed, reconstruct missing Reaction Receipts or Expression Moments, choose new Primitive coalitions/archetypes, or rewrite the Final Script.

### Exact compiler-profile dispatch

Builder currently has two distinct shapes under `cmf-builder-atomic-harness-definition/v1@1.0.0`:

- compiler `cmf-builder/generic-atomic-content-harness-compiler@1.0.0`: detailed synthetic core definition;
- compiler `cmf-builder/productized-manifest-compiler@1.0.0`: portable generic/Activative productized definition.

Pipeline must pin the four-part discriminator `(schema_id, schema_version, compiler_id, compiler_version)` and exact validator version. Unknown combinations fail. No union branch may be chosen by field guessing. The productized package is the F02 primary intake; the detailed synthetic form is permitted only as a named development compatibility profile, never as production or certification evidence.

### Package and side-effect safety

- Reject absolute, drive-letter, UNC, backslash, NUL, `..`, duplicate, case-colliding, symlink, device, and unmanifested members.
- Enforce exact member set, per-member byte/hash limits, total extracted bytes, compression ratio, deterministic names/order, canonical JSON, and UTF-8.
- Verify `SHA256SUMS`, package manifest, export receipt, definition record hash, definition content hash, package hash, and authority/admission snapshot before persistence.
- Unknown fields, enum values, schema majors, owners, categories, profiles, contract features, or capability kinds are rejected; no defaults are inferred.
- No provider, renderer, model, worker, network, filesystem-output, VAE, or Delegation side effect is allowed until a distinct later execution command consumes an eligible binding.

## 4. Current brownfield architecture

| Exact path/symbol | Actual current behavior | Disposition | Migration constraint |
|---|---|---|---|
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/atomic_harness_definition.py::AtomicHarnessDefinition` | Detailed frozen synthetic definition with canonical hash, 20 required sections, graphs, lineage, false production/certification flags, and invalidation record. | `REUSE` | Consume by exact bytes/profile through a read-only adapter. Do not import Builder code into Pipeline or generalize synthetic constants into current category rules. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/portable_export.py::PortableAtomicHarnessDefinition` | Productized generic/Activative portable projection; strict envelope/content keys; canonical JSON; rejects altered identity and host paths. | `REUSE` | Make this the primary F02 input profile. Verify package-level evidence in addition to object-level validation. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/application/export_service.py::DeterministicPortableExportService` | Deterministic stored ZIP with fixed metadata, exact relative members, manifest, receipt, and sums; atomic replace on export. | `REUSE` | Reproduce the consumer-side verification contract, not the exporter implementation. Never trust ZIP metadata or filename alone. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/domain/capability_ownership.py::CapabilityOwnershipDecision` | Explicit `CODE`, `AGENT`, `HUMAN`, `EXTERNAL`, `HYBRID` decisions, evidence, authority boundaries, and handoff participants. | `ADAPT` | Map Builder ownership declarations to Pipeline binding candidates; add versioned implementation refs, eligibility state, contract features, and runtime side-effect class. |
| `01_ATOMIC_HARNESS_BUILDER/src/cmf_builder/workflow/actor_explicit_contracts.py` | Execution-free DAG with one owner per node, typed edges, validation refs, cancellation/failure policy, deterministic identity, and invalidation receipt. | `ADAPT` | Preserve graph/actor/edge invariants while binding nodes to implementations; Pipeline may not modify the source graph. |
| `THE_CMF_STUDIO(2)/src/ccp_studio/contracts/studio_pipeline_recipe_harness.py` | Legacy recipe IDs, step kinds, artifacts, gates, blockers, and run objects, with open dictionaries, random IDs, current-time defaults, and legacy format routes. | `ADAPT` | Use only as migration fixtures for step/run vocabulary. Replace old route semantics, random/time identities, open maps, and implicit defaults. No recipe may become current Harness authority. |
| `01_ATOMIC_HARNESS_BUILDER/tests/productization/integration/test_pz04_end_to_end.py` | Proves deterministic portable package, path portability, rollback, altered-byte denial, and durable fresh-context inspection. | `ACTIVATE` | Re-express as consumer conformance fixtures plus adversarial archive cases; a Builder test PASS is evidence, not Pipeline acceptance. |
| `01_ATOMIC_HARNESS_BUILDER/tests/stories/st_07_02/test_replay_invalidation_and_receipt.py` | Proves repeat safety, active invalidation, and historical definition reproduction. | `ACTIVATE` | Extend across imported definition, binding descendants, and cross-process Pipeline storage. |

There is no Pipeline implementation yet. This specification does not create it.

## 5. Proposed architecture and workflows

### Components

| Component | Responsibility | Forbidden responsibility |
|---|---|---|
| `PortableHarnessPackageReader` | Safe bounded archive inventory and exact member extraction. | Following links, materializing unverified members, or running archive content. |
| `HarnessPackageVerifier` | Verify sums, package manifest, export receipt, package identity, and canonical bytes. | Accepting partial or extra package members. |
| `HarnessDefinitionProfileRegistry` | Resolve exact four-part compiler profile to a pinned validator/adapter. | Shape guessing or fallback to a “closest” schema. |
| `AtomicHarnessDefinitionIntake` | Validate definition identity, receipt, authority, lineage, category/profile, claim ceiling, and invalidation state. | Mutating Builder-owned content. |
| `HarnessGraphReconciler` | Verify capabilities, responsibility modules, phases, workflow nodes/edges, context manifests, Skills, evaluation requirements, and repair laws form one complete consistent graph. | Adding missing semantic nodes or hidden roles. |
| `ImplementationEligibilityRegistry` | Project current versioned implementation candidates and required features/evidence. | Acting as semantic authority or provider chooser outside a binding command. |
| `HarnessExecutionBindingCompiler` | Resolve each required executable element to one eligible embodiment and emit an immutable manifest/receipt. | Executing a node or altering Harness intent. |
| `BindingRepository` | Atomically persist command, imported package identity, binding, graph edges, receipt, and idempotency record. | In-place update or history deletion. |
| `BindingInvalidationProjector` | Mark only dependent binding/run projections stale on upstream change. | Global invalidation or historical byte deletion. |

### Intake and compile workflow

1. `ImportHarnessPackageCommand` supplies package bytes hash, authority/admission snapshot ref from draft TS-AHP-001, requested compiler profile, actor, command ID, and expected aggregate version.
2. Reader inventories without extraction, enforces archive limits/path law, and extracts only exact expected members into an isolated in-memory buffer.
3. Verifier checks canonical member set, member hashes, sums, package manifest, export receipt, package hash, and definition record/content identity.
4. Profile registry resolves the exact compiler discriminator and invokes the pinned read-only validator.
5. Intake verifies Builder ownership, current authority/status, package admission, category/profile compatibility, production/certification flags, lineage refs, and non-invalidated state.
6. Graph reconciler produces a read-only `HarnessRequirementGraphProjection` whose IDs/hashes point back to the definition; it does not fill gaps.
7. `CompileHarnessExecutionBindingCommand` names an exact imported definition and a frozen eligibility-registry snapshot.
8. Compiler resolves every executable requirement exactly once, validates cross-product ownership and contracts, computes semantic parity, and denies any unresolved or conflicting mapping.
9. Repository atomically commits manifest, compilation receipt, dependency edges, command/idempotency record, and current-head projection.
10. Later scheduling can consume only a non-stale binding with a separate execution authorization. Compilation itself has no external side effects.

### States and events

```text
Imported definition: RECEIVED -> PACKAGE_VERIFIED -> GRAPH_VERIFIED -> ELIGIBLE_FOR_BINDING
                    \-> DENIED | REVOKED | SUPERSEDED
Binding:             PROPOSED -> RESOLVING -> COMPILED -> ELIGIBLE_FOR_EXECUTION
                    \-> DENIED | INVALIDATED | SUPERSEDED | REVOKED
```

`ELIGIBLE_FOR_EXECUTION` means contractually complete under the binding's claim ceiling, not production-authorized. Events are `HarnessPackageVerified`, `HarnessImportDenied`, `HarnessGraphReconciled`, `HarnessBindingCompiled`, `HarnessBindingDenied`, `HarnessBindingInvalidated`, `HarnessBindingSuperseded`, and `HarnessHistoricalReplayVerified`.

### Idempotency, concurrency, cancellation, replay, compensation

- Command identity is SHA-256 over command type, canonical payload, exact authority/admission snapshot, and requested aggregate version.
- Identical command and payload returns the stored receipt without new state/event. Same command ID with different payload yields `AHP_BIND_IDEMPOTENCY_CONFLICT`.
- Optimistic concurrency compares the imported-definition/binding aggregate version before commit.
- Cancellation before commit yields a denial/cancellation receipt and no imported current head or binding. Cancellation after commit returns the committed receipt plus `CANCELLATION_TOO_LATE` observation.
- Archive verification and compilation are deterministic and synchronous. Human approval or external-product eligibility evidence is asynchronous and keeps the binding `DENIED_PENDING_EVIDENCE`; no background result mutates the old command.
- A failed atomic commit leaves no visible manifest without receipt and no success receipt without manifest. Verified temporary bytes are quarantined or discarded; historical accepted bytes remain unchanged.
- Replay loads exact package, registry snapshot, authority/admission snapshot, and compiler profile versions. It recomputes receipt digests and never substitutes latest dependencies.

## 6. Data models, contracts, schemas, and APIs

All objects are immutable, `additionalProperties: false`, and versioned. Set-semantic arrays are unique and sorted by canonical ID. No `Any`, open dictionaries, implied defaults, or untyped notes are permitted.

### Schema identities

| Schema | Candidate version | Value owner |
|---|---|---|
| `ca.pipeline.harness-package-import` | `1.0.0-candidate` | Pipeline |
| `ca.pipeline.harness-definition-compiler-profile` | `1.0.0-candidate` | Pipeline compatibility registry; Builder identifiers remain Builder-owned |
| `ca.pipeline.harness-requirement-graph-projection` | `1.0.0-candidate` | Pipeline projection of Builder bytes |
| `ca.pipeline.implementation-eligibility-snapshot` | `1.0.0-candidate` | owning product per candidate; Pipeline snapshot |
| `ca.pipeline.harness-execution-binding-manifest` | `1.0.0-candidate` | Pipeline |
| `ca.pipeline.harness-execution-binding-receipt` | `1.0.0-candidate` | Pipeline |

### `HarnessPackageImport`

Required fields: `import_id`, `package_sha256`, `package_bytes`, `member_count`, sorted typed `members`, `package_manifest_ref`, `export_receipt_ref`, `definition_record_ref`, `definition_content_ref`, `compiler_profile_ref`, `authority_snapshot_ref`, `source_admission_receipt_ref`, `category_id_or_not_applicable`, `profile_id_or_not_applicable`, `claim_ceiling`, `invalidation_state`, `imported_by`, and `imported_at_utc`. A member is `{relative_path, bytes, sha256, media_type}`. `imported_at_utc` is evidence-only and excluded from semantic identity.

### `HarnessDefinitionCompilerProfile`

| Field | Type and rule |
|---|---|
| `profile_id` | stable non-empty ID |
| `schema_id` / `schema_version` | exact Builder strings |
| `compiler_id` / `compiler_version` | exact Builder strings; completes the discriminator |
| `validator_ref` | versioned/hash-pinned deterministic validator |
| `required_envelope_fields` | sorted non-empty field-name array |
| `required_content_fields` | sorted non-empty field-name array |
| `semantic_guard_fields` | sorted non-empty JSON-pointer array |
| `supported_category_profile_registry_refs` | versioned/hash-pinned refs |
| `maximum_claim` | exact claim enum; cannot exceed imported Builder flags |
| `status` | `ACTIVE`, `DEPRECATED_FOR_NEW_BINDINGS`, `HISTORICAL_ONLY`, or `REVOKED` |

Profile resolution requires equality on all four discriminator fields. Unknown or multiple matches fail.

### `HarnessRequirementGraphProjection`

Required typed arrays are:

- `capability_requirements`: `{capability_id, source_pointer, source_value_hash, owner_requirement_ref, required}`;
- `responsibility_modules`: `{module_id, source_pointer, source_value_hash, capability_ids}`;
- `workflow_nodes`: `{node_id, actor_kind, owner, input_contract_ref, output_contract_ref, authority_requirement_ref, dependency_node_ids, validation_ref, evaluation_ref_or_not_applicable, repair_law_ref_or_not_applicable, cancellation_policy_ref}`;
- `workflow_edges`: `{source_node_id, target_node_id, payload_contract_ref, condition_ref, validated_output_required}`;
- `context_manifests`: `{context_manifest_id, source_pointer, source_value_hash, phase_or_node_id, minimum_complete_context_hash}`;
- `skill_requirements`: `{skill_requirement_id, source_pointer, source_value_hash, applicability, skill_ref_or_not_applicable, necessity_decision_ref}`;
- `evaluation_requirements`: `{evaluation_requirement_id, source_pointer, source_value_hash, evaluator_owner, hard_gate}`;
- `repair_laws`: `{repair_law_id, source_pointer, source_value_hash, allowed_scope, invalidation_rule_ref}`.

The projection additionally requires exact `definition_ref`, `definition_receipt_ref`, `package_import_ref`, `authority_chain_refs`, `semantic_lineage_refs`, `category_id`, `profile_id`, `graph_digest`, and `semantic_projection_digest`. Every pointer resolves; every source hash equals the canonical pointed value. Graph validation requires unique IDs, declared bilateral typed handoffs, no cycle, exact entry/terminal sets, no required orphan, and no hidden actor.

### `ImplementationBinding`

Each executable requirement has one record:

| Field | Type / ownership |
|---|---|
| `binding_id` | content-addressed Pipeline ID |
| `requirement_kind` | `CAPABILITY`, `WORKFLOW_NODE`, `HUMAN_GATE`, `EXTERNAL_PRODUCT_ROUTE`, `MODEL_PROGRAM`, `AGENT_PROGRAM`, `DETERMINISTIC_MODULE`, `RUNTIME_ADAPTER` |
| `requirement_id` | exact Builder-defined ID |
| `source_requirement_hash` | exact projection hash |
| `embodiment_kind` | `DETERMINISTIC_CODE`, `MODEL_PROGRAM`, `AGENT_PROGRAM`, `HUMAN`, `EXTERNAL_PRODUCT`, `RUNTIME` |
| `implementation_ref` | `{implementation_id, version, sha256}` owned by implementation product |
| `primary_owner_product` | exactly one governed product ID |
| `actor_ref` | exact actor identity and role; no mixed owner string |
| `input_contract_ref` / `output_contract_ref` | versioned/hash-pinned contracts matching Harness edges |
| `required_feature_refs` | sorted versioned/hash-pinned compatibility features |
| `eligibility_evidence_refs` | non-empty for any active binding |
| `authority_requirement_ref` | exact Harness authority requirement |
| `tool_grants` | typed least-privilege grants; empty tuple when not applicable |
| `side_effect_class` | `NONE`, `LOCAL_REVERSIBLE`, `EXTERNAL_REVERSIBLE`, `EXTERNAL_IRREVERSIBLE`, `HUMAN_DECISION` |
| `idempotency_policy_ref`, `cancellation_policy_ref`, `retry_policy_ref`, `failure_owner` | required typed refs/owner |
| `validation_ref`, `evaluation_ref_or_not_applicable`, `repair_law_ref_or_not_applicable` | exact graph requirements |

`required=true` requirements cannot map to `NOT_APPLICABLE`. `NOT_APPLICABLE` is a governed literal object with `basis_code` and source requirement ref, never null or omission.

### `HarnessExecutionBindingManifest`

Required fields are `manifest_id`, `schema_id`, `schema_version`, `manifest_version`, `definition_ref`, `definition_receipt_ref`, `package_import_ref`, `compiler_profile_ref`, `authority_snapshot_ref`, `source_admission_receipt_ref`, `eligibility_registry_snapshot_ref`, `category_id`, `profile_id`, `semantic_projection_digest`, `graph_digest`, sorted `implementation_bindings`, sorted `handoff_bindings`, sorted `contract_feature_pins`, `claim_ceiling`, `production_eligible`, `certified`, `supersedes_manifest_ref_or_not_applicable`, `dependency_edges_digest`, and `manifest_hash`.

The manifest never embeds semantic overrides. `production_eligible` and `certified` are logical AND of all upstream ceilings and current authorization; under this prompt both are false. Manifest identity is SHA-256 of canonical content excluding `manifest_id` and `manifest_hash`.

### Canonical serialization and examples

Canonical JSON is UTF-8, Unicode NFC, lexicographically sorted keys, no insignificant whitespace, no NaN/Infinity, exact enum strings, fixed integer units instead of binary floats, UTC `Z` timestamps, and one terminal newline. Arrays retain semantic order unless declared as sets. Host paths, environment values, clocks, random IDs, traversal order, and ZIP metadata cannot affect identities.

Positive binding excerpt:

```json
{
  "requirement_kind": "EXTERNAL_PRODUCT_ROUTE",
  "requirement_id": "visual_asset_realization",
  "source_requirement_hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "embodiment_kind": "EXTERNAL_PRODUCT",
  "implementation_ref": {"implementation_id": "visual-asset-editor", "version": "1.1", "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
  "primary_owner_product": "Visual Asset Editor",
  "actor_ref": {"actor_id": "vae-product-boundary", "actor_kind": "EXTERNAL_BOUNDARY_NODE"},
  "input_contract_ref": {"contract_id": "visual-asset-demand", "version": "1.1.0-rc.4", "sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},
  "output_contract_ref": {"contract_id": "visual-asset-result", "version": "1.1.0-rc.4", "sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},
  "required_feature_refs": [],
  "eligibility_evidence_refs": ["receipt:vae-contract-compatibility"],
  "authority_requirement_ref": "owner:visual-asset-editor",
  "tool_grants": [],
  "side_effect_class": "EXTERNAL_REVERSIBLE",
  "idempotency_policy_ref": "policy:delegation-idempotency",
  "cancellation_policy_ref": "policy:delegation-cancellation",
  "retry_policy_ref": "policy:delegation-retry",
  "failure_owner": "Visual Asset Editor",
  "validation_ref": "validator:visual-asset-demand",
  "evaluation_ref_or_not_applicable": "NOT_APPLICABLE:external-product-owned",
  "repair_law_ref_or_not_applicable": "NOT_APPLICABLE:external-product-owned"
}
```

The hashes above are illustrative field-shape values, not active release claims or a binding seed.

Negative example: a record with `primary_owner_product: "Pipeline|VAE"`, a free-form `semantic_overrides` map, missing `implementation_ref.sha256`, or an unknown capability is rejected before persistence.

### Compatibility, supersession, and migration

- Compatibility is semantic and feature-based, not merely parse success. Exact required features and compiler profile are pinned at binding acceptance.
- A minor manifest version may add optional evidence fields only. Changes to required fields, meanings, ownership, enum values, hashing, or compatibility behavior require a major version.
- Adapters cannot remove authority, lineage, epistemic state, category/profile, Feature Contract refs, T/V routes, Composition Intent, wrong-reading locks, evaluation, or repair constraints.
- Migration emits a new immutable import/projection/binding plus a typed migration receipt; original bytes remain.
- If two current Builder forms share an identifier but differ in shape, migration selects by exact compiler profile. It does not merge forms or infer missing fields.
- Active runs stay pinned to their accepted binding versions. Deprecation does not invalidate historical runs; revocation blocks new consumption and selectively invalidates affected descendants.

## 7. Implementation stages and exact target paths

All paths are prospective and require later ratification/adoption, independent acceptance, and a bounded Development Capsule.

| Stage | Exact future paths | FR / ST-03.01 mapping | Evidence |
|---|---|---|---|
| 1. Package and profile contracts | `05_ATOMIC_HARNESS_PIPELINE/contracts/harness_package_import.schema.json`; `contracts/harness_definition_compiler_profile.schema.json`; `src/cmf_pipeline/intake/archive_reader.py`; `intake/package_verifier.py`; `intake/compiler_profile_registry.py` | FR-007; AC1/AC2/AC3 | safe-archive corpus, Builder golden packages, profile discriminator tests |
| 2. Graph projection and validation | `contracts/harness_requirement_graph_projection.schema.json`; `src/cmf_pipeline/intake/definition_intake.py`; `intake/graph_reconciler.py`; `intake/semantic_parity.py` | FR-007, FR-008, FR-010; AC1/AC2/AC4 | exact graph/semantic digest and mutation denials |
| 3. Eligibility registry | `contracts/implementation_eligibility_snapshot.schema.json`; `src/cmf_pipeline/bindings/eligibility_registry.py`; `bindings/ownership_resolver.py`; `bindings/compatibility.py` | FR-008, FR-009, FR-011; AC1/AC2 | complete ownership and feature-negotiation matrix |
| 4. Binding compiler | `contracts/harness_execution_binding_manifest.schema.json`; `contracts/harness_execution_binding_receipt.schema.json`; `src/cmf_pipeline/bindings/compiler.py`; `bindings/failures.py` | FR-009-FR-011; AC1-AC4 | accepted/denied manifests and receipts |
| 5. Atomic persistence | `src/cmf_pipeline/repositories/binding_repository.py`; `repositories/sqlite_binding_repository.py`; `migrations/0002_harness_intake_and_binding.sql` | FR-009, FR-012; AC3/AC5 | atomicity, concurrency, idempotency, rollback evidence |
| 6. Invalidation/replay | `src/cmf_pipeline/bindings/invalidation.py`; `bindings/replay.py`; `application/revoke_harness_binding.py` | FR-012; AC3/AC5 | selective invalidation and historical replay matrix |
| 7. Application/CLI boundary | `src/cmf_pipeline/application/import_harness_package.py`; `application/compile_execution_binding.py`; `cli/harness.py` | all FRs; AC1-AC5 | no-side-effect end-to-end reference-slice receipt |

No task may edit Builder-owned definition bytes, AIR semantic objects, VAE, Delegation RC4, Studio predecessor, Program Control authority, or historical receipts.

## 8. Failure, migration, rollback, recovery, and observability

### Typed failures

| Code | Trigger | Owner / next admissible action |
|---|---|---|
| `AHP_INTAKE_UNSAFE_ARCHIVE` | traversal, absolute, duplicate/case collision, symlink/device, size/ratio breach | package producer; produce a safe canonical package |
| `AHP_INTAKE_MEMBER_SET_MISMATCH` | missing or extra member | Builder/exporter; re-export exact package |
| `AHP_INTAKE_HASH_MISMATCH` | sums, manifest, receipt, package, record, or content hash differs | Builder/source custodian; restore exact bytes or issue new version |
| `AHP_INTAKE_COMPILER_PROFILE_UNKNOWN` | four-part discriminator has no exact profile | compatibility owner; register an authorized profile |
| `AHP_INTAKE_COMPILER_PROFILE_AMBIGUOUS` | more than one exact profile | Pipeline compatibility owner; resolve registry collision |
| `AHP_INTAKE_AUTHORITY_OR_ADMISSION_STALE` | TS-AHP-001 draft interface or Program Control snapshot does not match | Program Control/Pipeline; reconcile and issue new admission |
| `AHP_INTAKE_DEFINITION_INVALIDATED` | Builder or Program Control marks definition stale/revoked | Builder/Program Control; select eligible replacement |
| `AHP_GRAPH_INCOMPLETE` | required capability/module/node/context/Skill/eval/repair item missing | Builder; compile a new complete Harness version |
| `AHP_GRAPH_CYCLE_OR_HANDOFF_MISMATCH` | cycle, undeclared edge, or contract mismatch | Builder; correct and recompile Harness |
| `AHP_BIND_SEMANTIC_MUTATION_ATTEMPT` | binding differs from semantic projection or embeds override | Pipeline requestor; remove override and preserve exact refs |
| `AHP_BIND_OWNER_UNRESOLVED` | no single eligible owner/route/gate | owning product/Program Control; supply authoritative ownership evidence |
| `AHP_BIND_IMPLEMENTATION_INELIGIBLE` | version, hash, feature, authority, evidence, or claim ceiling fails | implementation owner; publish eligible immutable candidate |
| `AHP_BIND_SIDE_EFFECT_BEFORE_ACCEPTANCE` | binding compilation attempts execution | Pipeline; hard stop and incident receipt |
| `AHP_BIND_STALE_EXPECTED_VERSION` | optimistic concurrency mismatch | requestor; reload and issue new command |
| `AHP_BIND_IDEMPOTENCY_CONFLICT` | same command ID, different payload | requestor; new command ID after review |
| `AHP_BIND_LOSSY_MIGRATION_BLOCKED` | required constraint/reference cannot be preserved | migration owner; block or obtain new upstream artifact |

Deterministic validation failures are not retried. Transient storage errors retry with the same command identity. Quality/compatibility repair creates a new version and preserves the failed receipt. Late external evidence applies only to the exact pending request and registry snapshot; otherwise it is stored historically and a new command is required.

### Supersession, invalidation, rollback, and recovery

- New Builder definition, compiler profile, authority/admission snapshot, eligibility record, implementation version, contract feature, or ownership evidence creates an immutable new version.
- Descendants are discovered through exact dependency edges. Only bindings/runs that include the superseded or revoked version become `STALE_NOT_CONSUMABLE`; unrelated work remains eligible.
- Historical imported packages, graph projections, bindings, receipts, and run results remain readable by identity after invalidation.
- A run accepted under a deprecated version remains reproducible; revocation prevents new use and records the reason/replacement.
- Schema migration writes new artifacts and `migrated_from` refs. Lossy or ambiguous migration blocks.
- Deployment rollback selects the prior reader/compiler version and rebuilds current projections from immutable rows. It never rolls database history backward destructively.
- Storage failure rolls back import, manifest, receipt, command, and edges together. Temporary extracted content is never marked admitted.

### Observability and degraded behavior

Emit structured events listed in section 5 with package, definition, compiler profile, graph, binding, authority, actor, command, receipt, and blocker refs. Metrics include archive denial code, profile resolution result, graph element counts, unresolved ownership count, compatibility mismatch, semantic-parity failure, binding latency, idempotent replay, concurrency conflict, rollback count, invalidation fan-out, and replay mismatch. Alert on orphan manifest/receipt, success receipt without dependency edges, stale binding consumption, self-owned external boundary, semantic override, or external side effect during compile.

Logs exclude raw source content, secrets, credentials, model prompts, absolute local paths, and private human data. If the eligibility registry is unavailable, intake may verify and retain a non-executable imported package, but binding compilation remains denied; no cached owner is guessed.

## 9. Behavior-specific acceptance criteria

1. **FR-007 / ST-03.01 AC1 - exact portable intake.** Given a Builder package whose four members, sums, manifest, receipt, definition, authority/admission, category/profile, and invalidation state all match, when import runs, then one immutable `HarnessPackageImport` and receipt commit. Given one altered definition byte, then `AHP_INTAKE_HASH_MISMATCH` commits only a denial receipt. Evidence: import hash matrix; test layer: contract/integration.
2. **FR-007 / AC2 - archive safety.** Given a ZIP with `../escape`, `C:/drive`, backslash, symlink, case-colliding duplicate, or unmanifested member, when inventory runs, then `AHP_INTAKE_UNSAFE_ARCHIVE` or member-set mismatch occurs before extraction/persistence. Failure example: a traversal member writes outside quarantine. Evidence: safe-archive report; layer: security integration.
3. **FR-007, FR-008 / AC1 - exact compiler profile.** Given two definition shapes sharing schema ID/version but distinct compiler IDs, when intake resolves a profile, then the four-part discriminator selects exactly one validator. Given compiler ID is absent or unknown, no shape guessing occurs. Evidence: profile-resolution receipt; layer: contract/unit.
4. **FR-008 / AC1-AC3 - complete graph.** Given capabilities, modules, phases, nodes, edges, contexts, Skills, evaluations, and repair laws with matching hashes, when reconciliation runs, then one graph digest is emitted. Given an undeclared edge, missing required context, unknown Skill applicability, or cycle, then `AHP_GRAPH_INCOMPLETE` or handoff mismatch denies binding. Evidence: graph conformance matrix; layer: domain/integration.
5. **FR-009 / AC1 - complete binding.** Given every required graph item has one eligible implementation/human/external route and matching contracts/features, when compilation runs, then every requirement appears exactly once and the manifest/receipt commit atomically. Failure example: a required capability is omitted. Evidence: binding coverage ledger; layer: integration/property.
6. **FR-009, FR-011 / AC2/AC4 - explicit actor and owner.** Given a HYBRID capability with ordered participants and explicit handoff, when resolved, then one primary failure owner and each actor remain typed. Given `Pipeline|VAE`, anonymous owner, hidden agent, or a human gate replayed as new authority, then binding is denied before side effect. Evidence: ownership receipt; layer: architecture/contract.
7. **FR-010 / AC2/AC4 - no semantic mutation.** Given a binding changes purpose, phase meaning, creative degrees of freedom, wrong-reading lock, Primitive/archetype/Final Script ref, Composition Intent, category/profile, evaluation, or repair law, when parity runs, then `AHP_BIND_SEMANTIC_MUTATION_ATTEMPT` denies it. Evidence: semantic pointer diff and denial receipt; layer: architecture/integration.
8. **FR-011 / AC2 - unresolved ownership.** Given a required capability has no eligible deterministic module, Model/Agent Program, human gate, external route, or runtime, when compile runs, then `AHP_BIND_OWNER_UNRESOLVED` identifies requirement, responsible owner, evidence gap, and next admissible action; no provider/model/worker call occurs. Evidence: side-effect spy plus denial receipt; layer: integration.
9. **FR-012 / AC3/AC5 - selective invalidation.** Given one implementation version is revoked, when dependency traversal runs, then only bindings and runs pinned to it become stale; unrelated bindings and historical receipts remain unchanged. Failure example: all runs are globally invalidated. Evidence: old/new dependency matrix; layer: recovery/property.
10. **FR-012 / AC3 - historical replay.** Given a superseded definition and binding, when replay uses their exact package/profile/registry/authority versions, then original digests reproduce without making them current. Given replay substitutes a latest dependency, then it fails. Evidence: historical replay receipt; layer: replay integration.
11. **FR-009, FR-012 / AC3 - idempotency and atomicity.** Given identical command delivery twice, when compiled, then one manifest and one receipt exist and both calls return it. Given fault injection after manifest write but before receipt/edges, then nothing becomes visible. Evidence: transaction trace; layer: persistence integration.
12. **FR-007-FR-012 / AC4 - deterministic portability.** Given two fresh processes, shuffled input maps, different roots/timezones/environment/random seeds, when importing and binding the same bytes, then package, projection, manifest, and receipt hashes are identical with no absolute paths. Evidence: two-process hash matrix; layer: clean environment.
13. **FR-011 / AC2 - external boundary.** Given a VAE, Delegation, provider, model, or renderer route, when binding compiles, then only typed references and tool/side-effect policy are emitted; any actual call yields `AHP_BIND_SIDE_EFFECT_BEFORE_ACCEPTANCE`. Evidence: network/provider/worker spies; layer: architecture/integration.
14. **FR-007-FR-012 / Definition of Done - claim ceiling.** Given all local tests pass while ratification and product authorization are absent, when status is projected, then quality remains at most technical acceptance pending ratification and production/certification remain false. Failure example: package PASS becomes production-ready. Evidence: claim-boundary receipt; layer: status architecture.

## 10. Testing and completion evidence

Future authorized implementation must create these exact test suites:

- `05_ATOMIC_HARNESS_PIPELINE/tests/contracts/test_harness_package_import_schema.py`: exact members, types, unknown fields/versions, claim ceiling.
- `05_ATOMIC_HARNESS_PIPELINE/tests/security/test_harness_archive_safety.py`: traversal, absolute/UNC/drive/backslash/NUL, symlink/device, duplicates/case collisions, size/ratio, extra members.
- `05_ATOMIC_HARNESS_PIPELINE/tests/contracts/test_builder_compiler_profile_registry.py`: both current compiler profiles, unknown/ambiguous profile, schema-ID collision without guessing.
- `05_ATOMIC_HARNESS_PIPELINE/tests/domain/test_harness_requirement_graph_projection.py`: all graph families, hash pointers, unique IDs, cycles, bilateral handoffs, entry/terminal sets, required `NOT_APPLICABLE` law.
- `05_ATOMIC_HARNESS_PIPELINE/tests/domain/test_binding_semantic_parity.py`: every forbidden semantic override, lineage flattening, wrong-reading weakening, category/profile mutation.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_builder_portable_package_intake.py`: Builder generic/Activative golden packages, altered byte, receipt/manifest/sums mismatch, invalidation state.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_harness_execution_binding_compiler.py`: all embodiment kinds, complete coverage, ownership, feature compatibility, external/human gates, no side effects.
- `05_ATOMIC_HARNESS_PIPELINE/tests/integration/test_binding_repository_atomicity.py`: manifest/receipt/edge/command transaction, idempotency conflict, optimistic concurrency, injected failures.
- `05_ATOMIC_HARNESS_PIPELINE/tests/recovery/test_binding_supersession_invalidation_replay.py`: descendant-only invalidation, revocation, deprecation, migration, rollback, historical reproduction.
- `05_ATOMIC_HARNESS_PIPELINE/tests/architecture/test_builder_pipeline_authority_boundary.py`: Pipeline cannot import Builder compilers as authority or expose semantic override fields.
- `05_ATOMIC_HARNESS_PIPELINE/tests/architecture/test_cross_product_binding_boundaries.py`: AIR/Interview/VAE/Delegation/Studio ownership and no call during compilation.
- `05_ATOMIC_HARNESS_PIPELINE/tests/clean_environment/test_binding_determinism_and_portability.py`: two roots/processes, shuffled order/environment, byte-identical hashes, no local paths/secrets.
- `05_ATOMIC_HARNESS_PIPELINE/tests/reference_slices/test_st03_01_ingest_and_bind.py`: primary, denial, evidence/replay, CBAR, selective recovery, and claim-ceiling evidence.

Completion evidence for a later build consists of schema/generated-model parity; Builder producer-to-Pipeline consumer conformance; archive adversarial report; graph coverage ledger; ownership/compatibility matrix; semantic parity report; atomicity/concurrency/idempotency traces; supersession/invalidation/replay matrix; two fresh-process full-regression results; source compilation/type checks; clean extracted-layout proof; exact changed-file manifest; and independent evaluator receipt.

A future Build Receipt must cite ratified/adopted authority, independently accepted spec hash, bounded Development Capsule, exact Builder input profile/version/hashes, implementation/test hashes, evidence results, and maximum claim. The receipt cannot infer production, Format 02 certification, VAE Stage 5, provider authority, or product certification from local tests. This writer issues no Build Receipt and no acceptance.
