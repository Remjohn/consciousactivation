# ST-01.02 Builder-First Readiness Re-evaluation

Date: 2026-07-15  
Active mode: `SYNTHETIC_DEFINITION`  
Verdict: `READY`  
Implementation authorized: `false`

This report supersedes the earlier Format 02-only readiness conclusion for the
active Builder Core path. The earlier BD-004 audit remains valid historical
evidence for `REAL_PROFILE`; it is not a dependency of this amended mode.

## Outcome under evaluation

An authorized category-neutral Builder run accepts the exact governed,
repository-owned synthetic task definition, diagnoses it without mutation, and
commits a portable immutable Source Lock with deterministic identity,
provenance, authority, failures, observability, and receipt evidence.

This outcome does not compile or execute an Atomic Harness. It is the evidence
lock consumed by the next `DECLARED_BOUNDARY` Story mode.

## Independent dependency validation

### Original ST-01.01

- Completion receipt:
  `development-capsules/ST-01.01/STORY_COMPLETION_RECEIPT.yaml`
- File SHA-256:
  `ec3e425cb562c16a6b31e427046962687b2dbfb781856b677593520635cffd7b`
- Canonical receipt payload expected/observed:
  `d82529f484971ef80bbd94ea29f685c9adfe3e50969aaf78367472695ea8add9`
- Root file manifest expected/observed:
  `5ef0480e11e26363f918049bad584b69e43428b620e6086e435faea7460990d2`
- Capsule input validation: `PASS_16_OF_16`
- Fresh regression: `PASS_20_OF_20`
- Receipt verdict: `PASS`

The historical manifest has two expected current-byte differences:
`domain/target_profile.py` and `adapters/__init__.py`. They are exactly the two
authorized supplemental files. Their historical hashes equal the supplemental
manifest's `previous_sha256` values, and their current hashes equal its
`current_sha256` values. The original receipt remains separate; its identity was
not rewritten.

### ST-01.01-SYNTHETIC-PROOF

- Completion receipt:
  `development-capsules/ST-01.01-SYNTHETIC-PROOF/completion/STORY_COMPLETION_RECEIPT.yaml`
- File SHA-256:
  `58ae069c277e4256633db258a639e4901b44cdeb3d5e36b06464aa80d2700418`
- Canonical receipt payload expected/observed:
  `62bec99526a72fe83cefbd5dd30bab77f29b8d45556bfa83feaf73486314bdf9`
- File-change manifest expected/observed:
  `4d64b9ba8552b0e8e6757928fca9136582236f8365f800d229037ae75aea3f3d`
- Capsule manifest expected/observed:
  `4917fbce9295255f8a71f61eb9031679cd2d9dd1729cf15a771f3da24be6174f`
- Capsule bundle digest expected/observed:
  `2e15bb0d795813e927bc60190a79978c675e0abae3037b7529f914d4e6f70ff3`
- Capsule input validation: `PASS_20_OF_20`
- Fresh regression: `PASS_18_OF_18`
- Receipt verdict: `PASS`

The receipts have distinct paths, types, payload hashes, scopes, manifests, and
effects. Both validation procedures reproduce independently; the supplemental
manifest supplies the exact additive source-state lineage between them.

### Empty-skill registry and prohibited changes

- Policy, schema, fixture hashes: `PASS_3_OF_3`
- Validation receipt SHA-256:
  `79164fa7418d3750ffefee116264b1ca44533c8073afb5485b84089ebd945ee1`
- JSON Schema and governed-empty semantics: `PASS`
- Out-of-scope supplemental paths: none
- Prohibited files modified: none
- External dependencies added: none

The empty registry is a validated dependency of the synthetic target profile;
ST-01.02 does not add or broaden its BD-010 disposition.

## Owned obligations and dependencies

Primary obligations remain exactly:
`ADR-007`, `D005`, `FR-009`–`FR-013`, `NFR-PORT-001`, `NFR-SEC-001`, and
`NFR-SEC-002` (10/10, no ownership change).

The sole direct dependency in this mode is the supplemental PASS receipt. The
original ST-01.01 PASS receipt remains its verified foundation. No later Story
is required.

## Blocker activation

Applicable semantic/evidence/human/external blockers: **none**.

- `BD-004` stays active for `REAL_PROFILE` source corpora only.
- `BD-014` stays active for external-product handoff modes only.
- `HD-006` stays active for conversational Human Reaction evidence only.
- Format 02 corpus/provider baselines, VAE or Delegation runtime, GPU,
  evaluator certification, conversational policy, and production certification
  are not intrinsic to this outcome and were not reintroduced.

The remaining human action is the bounded implementation authorization gate,
not a Story-semantic blocker.

## Exact implementation scope

The validated capsule authorizes, only after explicit human approval, a
standard-library implementation of versioned source profiles, read-only
file/directory/ZIP diagnostics, immutable descriptors/Source Lock, atomic run
binding through `SOURCE_DIAGNOSTIC -> SOURCE_LOCKED`, authority, idempotency,
typed failures, observability, rollback, and tests.

It permits three new source modules, six narrowly constrained extensions to the
existing run foundation, seven test files, and six completion-evidence files.
No schema, dependency, API, database/CAS production adapter, category/target
registry, compiler, or external runtime is included. The exact list is in
`development-capsules/ST-01.02/ALLOWED_FILE_SCOPE.yaml`.

## Capsule gate

- Capsule immutable inputs: `PASS_18_OF_18`
- Bundle digest:
  `99eaf7fc9285b6683c2562c519bda4131b72c5fd91a7f79a30113c5661680808`
- Manifest SHA-256:
  `a06b4bae7c92a6e33e0a10030ebd811983b52837bdf60914bc89f3787180b923`
- GWT criteria: `PASS_10_OF_10_EXECUTABLE`
- Tests/observability/rollback/file scope: `PASS_COMPLETE`
- Bounded implementation readiness: `PASS`
- Human authorization required: `true`

Exact authorization phrase:

`AUTHORIZE BUILDER ST-01.02 SYNTHETIC-DEFINITION BOUNDED IMPLEMENTATION`

Full Release 1 and full-product readiness remain `FAIL`. No implementation was
started during this re-evaluation.
