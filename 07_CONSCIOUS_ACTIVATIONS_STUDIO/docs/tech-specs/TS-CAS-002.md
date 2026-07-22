---
spec_id: TS-CAS-002
document_class: CANDIDATE_CANONICAL_TECH_SPEC
title: Direct Manipulation Command Adapter and Selective Rerun
product: Conscious Activations Studio
primary_owner: Conscious Activations Studio
quality_state: WRITTEN_PENDING_AUDIT
authority_state: CANDIDATE_NOT_CURRENT
specification_work_authorized: true
build_authority: false
later_acceptance_ceiling_before_ratification: TECHNICALLY_ACCEPTED_PENDING_RATIFICATION
writing_wave: 17
output_path_class: DIRECT_PRODUCT_SPEC_PATH
output_path: 07_CONSCIOUS_ACTIVATIONS_STUDIO/docs/tech-specs/TS-CAS-002.md
controlling_frs: ['FR-152', 'FR-154']
controlling_stories: ['ST-10.04']
upstream_draft_dependencies: ['TS-CAS-001']
---

# TS-CAS-002 - Direct Manipulation Command Adapter and Selective Rerun

This is an implementation-grade candidate Tech Spec for the Studio command, projection, correction, HumanResolution, campaign and publish-routing surface. It was written under the Prompt 02C specification-work authorization and ends at `WRITTEN_PENDING_AUDIT`. It does not authorize implementation, product adoption, build, release bytes, production use, certification, VAE Stage 5, or a Development Capsule.

## 1. Files and authorities read

### 1.1 Frozen packet and source controls

| Source | SHA-256 | Bytes | Availability |
|---|---|---:|---|
| `RECONCILIATION_INPUT_HASH_LOCK.yaml` | `ea28bcab299e74adb87f3bce8ab8a1d20093d4d8699e9e10c5d387383363c456` | `24593` | available |
| `CANONICAL_SPEC_LEDGER.csv` | `acb0bd4b9d941c389b9a816ae00922770eafc9eafcab1ccf924f0e9b84dcbe2c` | `23269` | available |
| `CANONICAL_FR_LEDGER.csv` | `bb6313076b9119a222ef9909dadba017d293abb3a369eab409e45bc244ffa91b` | `104516` | available |
| `FR_OWNER_STORY_SPEC_TRACEABILITY.csv` | `5c3a8dda79a4d06cf71828c8581ebbf2799ef09454b2158dcfe04f9828aa0ab6` | `236715` | available |
| `SPEC_DEPENDENCY_DAG.yaml` | `1cf4299781e76c9c80f4489291a92b0a5e1f666f91b8cf9476307a03da5257eb` | `9178` | available |
| `PATH_OWNERSHIP_REGISTRY.yaml` | `f260e400384a67f837b67a8a8981a4b773cd8792135eeca20c94f065468296a7` | `11589` | available |
| `../V2_1_AUTHORITY_CONVERGENCE/CROSS_PRODUCT_AUTHORITY_MATRIX.yaml` | `cd92d291b04950cb0188558f4ea18afc4ef62791196e47e86bbeec6836301c39` | `4289` | available |
| `../V2_1_AUTHORITY_CONVERGENCE/SEMANTIC_OBJECT_OWNERSHIP_MATRIX.yaml` | `232a9153f7ef8a6c3835eaaa94e292a855680c89981fe8c4b86ed8e4501c7275` | `4263` | available |
| `SOURCE_DISPOSITION_LEDGER.yaml` | `d74dc34690b9a927868b372ccb8c2adce4dd322fe6dff972a3cbfe97491967e3` | `134201` | available |
| `SOURCE_GAP_NOTICE.yaml` | `ee8db798cd3b82c4ed9c22061e8b120ef3137e411b89d3f0d00310fe3e142886` | `17743` | available |
| `SPEC_DEPENDENCY_EDGE_CLASSIFICATION.yaml` | `4d4a30f4001bf5051ac74c361a921603442021e0c43270e35390e20b5afcb4f8` | `107141` | available |
| `SPEC_WRITING_WAVE_DAG.yaml` | `24b26b9820a0f2cab0cd01ab4c46e9aca476219f496644c063533ee602ccff60` | `5260` | available |
| `AUTHORITY_STAGE_DECISION.yaml` | `9897a6bd3426b63a2c49567f08db80c4e5bd9a257808067ab416babeed8d2f52` | `1221` | available |
| `SPECIFICATION_WORK_AUTHORIZATION_RECEIPT.yaml` | `4b4b32b29e8e1e47ddad27d4ea2eb144313e5e06c2575f25de2e1102afac1e25` | `1462` | available |
| `SPEC_PACKET_WRITE_AUTHORITY_MATRIX.csv` | `3fa4793ea2baca46dcfbf8e123d039a59ab2467e5814471d49b3daf65e588a73` | `18768` | available |
| `CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/V2_1_SPEC_WRITING_RECOVERY/ONE_SPEC_EXECUTION_PACKETS_RECOVERY.yaml` | `ff5fa32389458a94e437c2af06a7ce7c1ce2ab9b30cd8da53010f11b7503d345` | `316012` | available |

### 1.2 Upstream draft dependencies

| Edge | Upstream spec | Path | Quality state | SHA-256 | Label |
|---|---|---|---|---|---|
| `SDE-093` | `TS-CAS-001` | `07_CONSCIOUS_ACTIVATIONS_STUDIO/docs/tech-specs/TS-CAS-001.md` | `WRITTEN_PENDING_AUDIT` | `66afd1423145e6cb050ebcf188181649a35dfc2b0a1c4e01859cbf648ecfb7dc` | `DRAFT_DEPENDENCY_NOT_ACCEPTED` |

The upstreams are admitted only as hash-pinned draft interfaces. They are not accepted authority, not build prerequisites for writing, and not evidence that candidate V2.1 authority is current.

## 2. Problem, user outcome, solution, and scope

The problem is that `Direct Manipulation Command Adapter and Selective Rerun` must be implemented later without collapsing semantic authority, source provenance, category/profile support, evaluation evidence or lifecycle state into informal notes. The user outcome is a replayable and reviewable product boundary where every command, output, denial and repair points back to exact source, owner, version and receipt evidence.

The solution scope is the Studio command, projection, correction, HumanResolution, campaign and publish-routing surface. The spec defines required inputs, state transitions, output artifacts, validation receipts, failure handling, migration behavior, rollback boundaries and test obligations. It excludes implementation source code, provider credentials, generated types, schemas, release packages, production signing and certification.

## 3. Governing decisions and non-authority boundaries

- `Conscious Activations Studio` owns only the behavior explicitly assigned by the Prompt 02 ledger and this packet.
- AIR semantic lifecycle, Interview Expression source evidence, VAE visual production, Delegation transport, Studio projection/correction and Program Control status authority remain separate.
- Candidate V2.1 authority is `CANDIDATE_NOT_CURRENT`; writing is authorized, but build and production are false.
- `NOT_APPLICABLE` is a governed value for excluded categories, profiles, routes or evidence types. It must not be omitted or replaced by null when the distinction affects behavior.
- Any upstream hash or accepted-interface change reopens downstream revision-impact sections before later acceptance.

## 4. Functional behavior and invariants

| FR | Primary owner | Spec binding | Claim ceiling |
|---|---|---|---|
| `FR-152` | `Conscious Activations Studio` | `TS-CAS-002` | `SPECIFICATION_ONLY_NO_IMPLEMENTATION_NO_PRODUCTION_NO_CERTIFICATION` |
| `FR-154` | `Conscious Activations Studio` | `TS-CAS-002` | `SPECIFICATION_ONLY_NO_IMPLEMENTATION_NO_PRODUCTION_NO_CERTIFICATION` |

| Story | Spec binding | Current quality state |
|---|---|---|
| `ST-10.04` | `TS-CAS-002` | `WRITTEN_PENDING_AUDIT` |

Invariants: immutable versions for all commands and outputs; deterministic serialization and hashing; exact source and authority references; explicit wrong-reading-lock preservation where applicable; stale-version denial; no guessed source kind; no producer self-approval; and separate states for production acceptance, downstream consumption acknowledgement and certification.

## 5. Proposed architecture and workflows

The central implementation object is `TS_CAS_002_RuntimeContract`. It consumes TS-CAS-001, the Prompt 02C packet, the authority-stage decision and the writing-wave lock. It emits one of three outcomes: a valid artifact package, a typed denial, or a scoped repair/escalation request.

Workflow:

1. Validate authority state, packet identity, source availability, upstream hashes and idempotency key.
2. Load only typed inputs from the owning product boundary and reject ambiguous ownership.
3. Build deterministic internal state from sorted, canonical data.
4. Validate category/profile, source-kind, lineage, wrong-reading-lock and `NOT_APPLICABLE` obligations.
5. Persist artifact and receipt references atomically in the later implementation.
6. Expose replay, rollback, invalidation and audit projections without mutating historical evidence.

## 6. Data models, contracts, schemas, and APIs

This spec proposes implementation targets only:

| Contract | Required fields | Notes |
|---|---|---|
| `TS_CAS_002_Command` | `command_id`, `idempotency_key`, `caller`, `target_version`, `source_refs`, `authority_refs`, `operation` | Reject before side effects when authority or version is stale. |
| `TS_CAS_002_State` | `state_id`, `version`, `lifecycle_state`, `pinned_dependencies`, `not_applicable_fields`, `lineage` | Immutable per version and deterministically serialized. |
| `TS_CAS_002_Receipt` | `receipt_id`, `command_id`, `result`, `artifact_refs`, `hashes`, `failure_context` | Receipt storage without artifact or denial context is invalid. |
| `TS_CAS_002_Invalidation` | `reason`, `owner`, `affected_descendants`, `replacement_refs`, `historical_replay_policy` | Descendant-only unless upstream authority issues a new demand/version. |

APIs must reject absolute-path leakage, unsafe archive members, environment-derived identity, current-time identity, random identity and dictionary-order-dependent output.

## 7. Security, authority, privacy, and operational constraints

Technical security controls cover sandboxing, archive extraction, provider secrets, file paths, replay inputs and command idempotency. They do not create generic creative-safety/content-rights authority and do not supersede operator-supplied source authority, provenance, lineage, approvals or product sovereignty.

All portable artifacts must use relative paths, content hashes, versioned references and declared environment contracts. Historical outputs remain reproducible after invalidation, revocation, replacement or migration.

## 8. Failure, migration, rollback, recovery, and observability

Failures must record failed object, owner, lifecycle state, upstream hashes, expected/observed behavior, denial reason and permitted next action. Migration creates new immutable artifacts and never rewrites historical evidence. Rollback points to a prior immutable version and records why the newer version cannot be consumed.

Recovery follows ownership: semantic meaning returns to AIR or source owners; visual realization returns to VAE; transport/compatibility issues return to Delegation; Studio may route and project corrections; Pipeline may rerun execution descendants only when their dependencies changed.

Observability must include command records, artifact hashes, receipt indexes, dependency snapshots, denial counts, stale-read attempts, `NOT_APPLICABLE` counts, replay checks and source-lineage checks.

## 9. Acceptance criteria

- Ten required sections are present and bound to the frozen Prompt 02C packet.
- All FRs, Stories, output path, owner and writing wave match the canonical ledger.
- Upstream drafts are hash-pinned and labeled `DRAFT_DEPENDENCY_NOT_ACCEPTED`.
- Build, production, certification, product adoption and Development Capsule authority remain false.
- Authority boundaries are explicit and no product silently reconstructs another product's meaning.
- Determinism, idempotency, rollback, invalidation and historical reproducibility have concrete future test obligations.

## 10. Testing and completion evidence

Future build tests must cover deterministic serialization, replay/idempotency, stale-version denial, path portability, unsafe archive rejection, explicit `NOT_APPLICABLE`, ownership denial, selective invalidation, rollback, migration, failure context and historical reproduction.

Prompt 03 evidence is limited to writing: target hash, files-read receipt, source traceability receipt, draft-dependency receipt, writer manifest and wave completion receipt. Independent audit, revision, re-audit, acceptance and build remain later lifecycle stages.
