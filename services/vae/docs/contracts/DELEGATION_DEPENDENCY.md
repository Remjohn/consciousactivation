# Delegation Contract Dependency

**Stage:** 3 - Contract integration  
**Dependency status:** Delegation `1.1.0-rc.2` adopted for bounded VAE integration as a local unsigned release candidate  
**Recorded:** 2026-07-14  
**VAE implementation authorization:** not granted

## Current bounded adoption — Delegation 1.1.0-rc.2

The VAE independently validated and pinned the program-control release at `D:/Work/CONSCIOUS_ACTIVATIONS/CMF_PROGRAM_CONTROL/02_CROSS_REPO_CONTRACTS/delegation-contracts/1.1.0-rc.2`. This supersedes the dependency conclusion below for current Batch B work, while preserving the earlier draft and `1.0.0-rc.2` analysis as historical evidence.

| Attribute | Adopted value |
|---|---|
| Package version | `1.1.0-rc.2` |
| Release digest | `sha256:d4958cd3d02f0acef9d66bf245078ea70dab36b727d0c1541031fdceb63f6e41` |
| Receipt hash | `sha256:ff97185ec1dfd1c2eaf936beec318e28b583fd2e3da809df9b860f504c7b6cff` |
| Release-manifest hash | `sha256:6e765eeef4ebed71d6e725cf11f49815f9cc0cafbe42ef157c8f189d8c7d582c` |
| Source-manifest hash | `sha256:8a572d086397b4c781eac76fd7d81e4fdd128480de2a283d515634fde230a982` (source-only provenance; not distributed or receipt-covered) |
| Compatibility profile | `cmf-delegation-compatibility@1.1.0-rc.2` |
| Trust | `local_unsigned_release_candidate`; not production trusted or authorized |
| Consumer verdict | PASS for bounded local contract integration; no Stage 5 authorization |

The clean extracted release validates 26 examples, closed schemas, generated Python and TypeScript structures, 36 fixtures, three migrations, 144 release-manifest entries and 145 receipt entries. The complete released suites pass 61 validator and 33 protocol tests. VAE adds 12 passing boundary tests for exact pins, typed source provenance, conditional interview lineage, complete lossless mapping, no-guess migration, parse-only rejection, H-003 lock inheritance, H-004 Feature Contract ownership, result authority, and the unsigned trust boundary.

The exact VAE-owned pin, request/result mappings, compatibility declaration, fixtures, and tests are under `contracts/integration/` and `validation/`. No shared Delegation schema or generated binding is copied or rewritten. The rejected `1.1.0-rc.1` report remains historical consumer evidence.

## Purpose

This record defines how the CMF Visual Asset Editor (VAE) consumes the separately owned Content Harness <-> Visual Asset Editor Delegation package. It is an architecture and test boundary, not a copied contract release, generated binding, runtime adapter, or authorization to implement production code.

The Delegation repository owns public schema shapes, message and protocol versions, compatibility classifications, public lifecycle semantics, integrity rules, and conformance fixtures. Content Harness owns Visual Asset Demand meaning. VAE owns production planning, execution, evaluation, repair, and production acceptance. A production model cannot approve its own output, and VAE cannot grant downstream composition authorization.

## Historical Stage 3 dependency identity

| Attribute | Pinned Stage 3 value |
|---|---|
| Package | `CMF_CONTENT_HARNESS_VISUAL_ASSET_EDITOR_DELEGATION_SHARDED_PRD_V1` |
| Local audit source | `D:\Work\Conscious Activations\CMF_CONTENT_HARNESS_VISUAL_ASSET_EDITOR_DELEGATION_SHARDED_PRD_V1\CMF_CONTENT_HARNESS_VISUAL_ASSET_EDITOR_DELEGATION_SHARDED_PRD_V1` |
| Product version | `0.1.0-draft` |
| Artifact status | `draft_for_review` |
| Registry/lifecycle version | `1.0.0-draft` |
| Manifest SHA-256 | `06d8d38df9c144492d67e25b918ea7362ea80b905b9554e83f39cb5bb6394c1b` |
| Message registry SHA-256 | `9e32ba1131a5eb9e571fe779d0a1c919af8fee00eee68bd3ca5b347943d3f0de` |
| Lifecycle machine SHA-256 | `96e8b928d5ced30f7ee108a6a999471b7b9a6222648d3f73c87426f70369e930` |
| Registered contract checks | 25 schemas, 25 examples, 25 registry messages, 56 declarative conformance cases, and 10 Format 02 scenarios are present; schema/example checks report no errors |
| Release provenance | unavailable; the supplied directories contain no `.git` metadata and no published package coordinate |

The Stage 3 manifest digest is a reproducible historical pin for the listed draft files only. It is not a substitute for a published package version, signatures, or release provenance.

## Current RC dependency and reconciliation

The mutable sibling workspace advanced after the Stage 3 matrix was written:

| Attribute | Current observed value |
|---|---|
| Contract package | `cmf-delegation-contracts` `1.0.0-rc.2` in package/compatibility manifests |
| Status | coherent `RELEASE_CANDIDATE`, local, unsigned, not published |
| Root manifest SHA-256 | `8ca1957c2a7a0dd76231a041ef3f3b2670d3a1e05ce6ee79c92c7102a893cead` |
| RC release-manifest SHA-256 | `49d4befe0fd90fffbbe7cb00c0a5401eee6858f5493a502da9a1a1ff6df7de19` |
| RC registry SHA-256 | `7941af57b60c307ae077b9944761da844944b0416727b444d04db7ee083ba0a8` |
| RC lifecycle SHA-256 | `621a745042886a57cff7f31f1d4696ebdaa43c35b8f5cea78bc1a1e90bad51e2` |
| RC authority SHA-256 | `51929735589119c7afc0015f04f9bbdc4d862251bf5d5fad881309291214f3dc` |
| RC contents | 26 schemas/examples/messages plus generated Python and TypeScript bindings |
| Receipt change | Draft `submission_receipt` is replaced by `submission-validation-receipt` and `admission-receipt` |
| Validation | Package validator PASS; validator test suite 42 passed |

`CONTRACT_COMPATIBILITY_MATRIX.yaml` now enumerates all 26 RC2 registry messages against exact schema hashes and registered producer/consumer arrays. RC2 fixes the RC1 producer conflicts. One required path remains `INCOMPATIBLE`: `amendment-response` is Content Harness-owned but VAE is missing from its registered consumers, contrary to the Delegation ownership specification and VAE proposal workflow. Reconciliation must be repeated against the published signed release, and production dependency resolution must reject this unsigned local RC.

## Ownership and immutability rules

1. VAE imports a published Delegation contract package; it never republishes or edits shared schemas.
2. An accepted demand is immutable. VAE may derive an internal production plan or emit `constraint_conflict` and `amendment_proposal`; only Content Harness may issue an amended/superseding demand.
3. Every related message must retain exact demand identity: request ID, demand version, payload hash, and canonical reference once ADR-DLG-006 is resolved.
4. VAE emits production acceptance in `asset_result_contract`. Content Harness emits downstream acceptance/rejection in `result_acknowledgement`.
5. Envelope/audit metadata owns message identity, occurrence time, sequence, correlation, causation, principal, integrity, and replay evidence. VAE internal workflow states never become public lifecycle states.
6. Unknown required semantics, unsupported authority, illegal lifecycle transitions, hash failures, and unresolved migrations fail closed before internal work is admitted.
7. Internal VAE contracts remain provider-neutral. The Delegation adapter cannot expose ComfyUI graphs, worker details, evaluator prompts, candidate ranking, or repair-loop state.

## Adapter boundary

The future implementation shall use four explicit layers. Stage 3 defines them; it does not create runtime code.

| Layer | Responsibility | May not do |
|---|---|---|
| 1. Boundary validation | Resolve the pinned registry; validate envelope, payload schema, version, principal, hash, signature, lifecycle, idempotency, and replay status | Parse by best effort, infer missing identity, or route an invalid message |
| 2. Delegation bindings | Represent canonical Delegation payloads generated from the published package | Add VAE-owned fields or hand-maintain a schema fork |
| 3. VAE adapter | Deterministically and losslessly map canonical payloads to/from VAE boundary facts | Change demand meaning, hide mandatory fields, or translate public state into private workflow state |
| 4. VAE application ports | Admit immutable facts/commands and emit production facts without transport concerns | Receive raw unvalidated maps or make protocol authority decisions |

### Planned components

| Component | Contract-only responsibility |
|---|---|
| `DelegationSchemaRegistry` | Load one published package, verify its release digest, resolve canonical schema IDs and message versions, and reject drift |
| `DelegationInboundPort` | Accept only `ValidatedDelegationMessage<T>` values from the boundary service |
| `DelegationOutboundPort` | Accept typed VAE facts and create canonical payload plus envelope inputs for boundary validation and emission |
| `DelegationMapper` | Apply named, versioned, deterministic mappings with no implicit defaults for mandatory semantics |
| `DelegationConformanceHarness` | Run producer, consumer, adapter, lifecycle, authority, resilience, and Format 02 fixtures against the exact pin |

### Boundary data types

These are internal architecture types, not additions to Delegation payloads:

- `ValidatedDelegationMessage<T>`: immutable canonical payload plus negotiated versions, validated principal, correlation/causation IDs, integrity receipt, idempotency result, and lifecycle decision.
- `DemandIdentity`: request ID, demand version, payload hash, and canonical reference. Construction fails when any required part is absent.
- `VaeAdmissionFact`: accepted/rejected admission fact produced by VAE after protocol validation; it does not decide protocol-level rejection authority.
- `VaeProductionResultFact`: demand identity, accepted assets, production/evaluation/budget receipts, geometry, limitations, and partial-result evidence. It has no downstream authorization field.
- `VaePublicEventFact`: stable lifecycle fact only; message ID, occurrence time, and sequence remain envelope/audit metadata.
- `VaeConflictFact`: infeasibility evidence only. Proposed field changes map separately to `amendment_proposal`.

## Message direction inventory

The complete field-level classification and schema hashes are in `CONTRACT_COMPATIBILITY_MATRIX.yaml`.

| VAE interaction | Messages |
|---|---|
| Consume under RC2 | `visual-asset-demand`, `submission-validation-receipt`, `delegation-set`, `budget-authorization`, `budget-escalation-response`, `cancellation-request`, `demand-supersession`, `result-acknowledgement`, `invalidation-notice`, `delegation-audit-receipt`, `contract-migration` |
| Produce under RC2 | `admission-receipt`, `visual-asset-event`, `budget-escalation-request`, `cancellation-receipt`, `constraint-conflict`, `amendment-proposal`, `asset-result-contract` |
| Bidirectional/routed copy under RC2 | `delegation-envelope`, `selective-invalidation-receipt`, `revocation-notice`, `replacement-notice`, `delegation-failure`, `compatibility-manifest` |
| Protocol-observed, not a direct VAE payload | `visual-asset-submission` |
| Required consumer omitted by RC2 | `amendment-response` |

The RC split of draft `submission_receipt` into protocol-owned `submission-validation-receipt` and VAE-owned `admission-receipt` resolves the ambiguous producer. RC2 also aligns VAE proposal, invalidation evidence, revocation, replacement and product compatibility authority. The RC2 `asset-result-contract` excludes VAE-issued downstream authorization but requires an explicit migration from the local comparison fixture. The missing VAE consumer on `amendment-response` remains blocking.

## VAE provisional snapshots and fixtures

The following local files predate the Delegation package. They are retained only as PRD representative comparison fixtures:

| Local snapshot | Canonical draft comparison | Required adapter disposition |
|---|---|---|
| `contracts/schemas/VISUAL_ASSET_DEMAND.schema.yaml` | `visual-asset-demand.schema.yaml` | Top-level shape currently aligns; canonical Delegation schema still wins |
| `contracts/schemas/VISUAL_ASSET_SUBMISSION.schema.yaml` | `visual-asset-submission.schema.yaml` | Preserve canonical `demand_hash`; map the local contract-version concept to negotiated envelope/profile evidence |
| `contracts/schemas/VISUAL_ASSET_EVENT.schema.yaml` | `visual-asset-event.schema.yaml` | Move local event ID, occurrence time, and sequence to envelope/audit; emit only stable public state |
| `contracts/schemas/ASSET_RESULT_CONTRACT.schema.yaml` | `asset-result-contract.schema.yaml` | Replace local result shape with canonical demand/editor/authorization split; never emit `authorized_for_composition` |
| `contracts/schemas/CONSTRAINT_CONFLICT.schema.yaml` | `constraint-conflict.schema.yaml` | Keep execution references as evidence; emit proposed changes through `amendment_proposal` |

Representative local examples under `contracts/examples/` and `reference-slice/FORMAT02_MINIMAL_COACH_THEATRE/contracts/` inherit the same provisional status. They cannot be imported as a production protocol package, used to generate public bindings, or cited as proof of interoperability.

## Publication transition

When Delegation publishes an approved release:

1. Replace the local audit path with an immutable package coordinate, release digest, canonical schema IDs, and provenance.
2. Verify the release manifest and compare every registered schema hash against this Stage 3 matrix.
3. Classify every delta using only the Delegation compatibility verdicts.
4. Resolve migration-required entries before accepting traffic; never silently update in-flight delegations.
5. Generate bindings from the published schemas into a build artifact, not this source-owned contract directory.
6. Execute every claimed producer, consumer, adapter, lifecycle, authority, resilience, deprecated-version, and Format 02 fixture.
7. Publish VAE's compatibility manifest only after test evidence and the applicable readiness gates pass.
8. Quarantine the provisional snapshots from build/package inputs; retain them only as historical comparison evidence.

## Blocking decisions and cross-repository inputs

| Gate | Effect on VAE Stage 3 |
|---|---|
| RC2 amendment response consumer | Blocks delivery of Content Harness disposition to the VAE proposal originator |
| RC result migration | Blocks replacement of the local comparison fixture and executable result-adapter evidence |
| Published Delegation release | Blocks production pin, generated bindings, and executable cross-product conformance |
| Format 02 producer/consumer fixtures | Blocks end-to-end geometry and downstream acknowledgement proof |

## Stage 3 disposition

The architecture dependency and adapter boundary are reconciled against the exact coherent local RC2 registry. Stage 4 analysis can use this evidence, but the contract gate is **FAIL** for implementation because the package is unsigned/unpublished and one required consumer path is `INCOMPATIBLE`. Contract freeze, production bindings, implementation, and interoperability claims remain blocked until the Delegation owner fixes the consumer registration and publishes a signed immutable release.
