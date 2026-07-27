# Delegation 1.1.0-rc.2 Consumer Validation

Date: 2026-07-14  
Consumer: CMF Visual Asset Editor  
Candidate: `D:/Work/CONSCIOUS_ACTIVATIONS/CMF_PROGRAM_CONTROL/02_CROSS_REPO_CONTRACTS/delegation-contracts/1.1.0-rc.2`  
Release-adoption verdict: **PASS**  
Trust: `local_unsigned_release_candidate`  
Production authorization: **NO**

## Exact adopted identity

| Item | Pinned value |
|---|---|
| Package | `delegation-contracts@1.1.0-rc.2` |
| Protocol / Visual Asset Demand | `1.0` / `1.1` |
| Release digest | `sha256:d4958cd3d02f0acef9d66bf245078ea70dab36b727d0c1541031fdceb63f6e41` |
| Release receipt hash | `sha256:ff97185ec1dfd1c2eaf936beec318e28b583fd2e3da809df9b860f504c7b6cff` |
| Release manifest hash | `sha256:6e765eeef4ebed71d6e725cf11f49815f9cc0cafbe42ef157c8f189d8c7d582c` |
| Source manifest hash | `sha256:8a572d086397b4c781eac76fd7d81e4fdd128480de2a283d515634fde230a982` |
| Compatibility manifest hash | `sha256:d431e277a1de1cecb1f860226c37c44d8646c589b386f9ded0f6c4bef880f0c6` |
| Registry hash | `sha256:aa4b35d3f511d277a2f33797f55807be772693dec3ac020cf191dcc99d2b5915` |
| Compatibility profile | `cmf-delegation-compatibility@1.1.0-rc.2` |

The rejected `1.1.0-rc.1` candidate was not adopted. Its immutable VAE consumer report remains at `validation/DELEGATION_RC1_RELEASE_VALIDATION_2026-07-14.md`.

## Clean-consumer adoption gate

| Required check | Result | Evidence |
|---|---|---|
| Release receipt and every declared hash | PASS | Independent reconciliation found 145 declared and 145 actual files excluding the receipt; every byte count and SHA-256 matched |
| Release manifest consistency | PASS | 144 declared entries; manifest hash matches the receipt; released validator verifies the exact set |
| Clean extracted-layout validation | PASS | Release copied to an isolated temporary directory; released validation and both suites passed without producer source paths |
| Schemas and examples | PASS | 26 registered examples validate; public schemas are closed |
| Generated Python and TypeScript structures | PASS | Both expose typed `SourceKind` and mandatory `SourceProvenance` on Visual Asset Demand |
| Fixtures and migrations | PASS | 36 JSON fixtures parse; three migration declarations validate |
| Compatibility declarations | PASS | Lossless policy and all nine required semantic domains validate; parse-only is incompatible |
| Complete released validator suite | PASS | 61/61 |
| Complete protocol test evidence | PASS | 33/33 |
| Source discriminator and conditional interview provenance | PASS | Independent adversarial checks plus released tests enforce the mandatory typed discriminator and non-empty conditional references |

## Mandatory semantic behavior

The canonical discriminator is `/source_provenance/source_kind`. It is a mandatory closed enum owned by Content Harness. `interview_expression` requires at least one valid `/activative_semantic_lineage/reaction_receipt_refs` item and at least one valid `/activative_semantic_lineage/expression_moment_refs` item. A non-interview source such as `authored_source` validates when both arrays are absent. Empty supplied arrays remain invalid.

The released pre-discriminator migration returns `SOURCE_KIND_CLASSIFICATION_REQUIRED` until an authorized owner provides the classification. It returns `INTERVIEW_PROVENANCE_REQUIRED` rather than fabricating missing interview lineage. Lossy adapter changes and semantic capability claims that merely parse are rejected.

The VAE request mapping preserves all 24 canonical top-level fields and specifically protects Activative Intelligence Pack, Identity DNA, Context Premise, Resonance Map, Matrix of Edging product, Activative Call, Reaction Receipt, Expression Moment, Activation Contract, Visual Semantic Pack, Visual Narrative Program, Feature Contracts, T/V routes, wrong-reading locks and Composition Intent.

## H-003 and H-004 integration

- H-003: deterministic delivery variants and non-semantic derivatives must contain a superset of the accepted parent lock set. Stricter additions pass; removal fails. Relaxation passes only with a new authorized upstream demand version.
- H-004: Content Harness owns the typed, versioned, hash-pinned Feature Contract reference and semantic intent. VAE owns feasibility, production realization and realization receipts. The receipt preserves the exact authoritative reference; mutation is rejected. Infeasibility uses `constraint-conflict` and, when appropriate, `amendment-proposal`.

## Source-only manifest boundary

`SOURCE_ONLY_FILES.json` explicitly excludes `packages/contracts/source-manifest.json` from release validation. That file is absent from the 145-file receipt and the clean release, so it cannot expand the release trust claim. Its exact file hash is nevertheless pinned as source-only provenance.

The current mutable producer checkout no longer reconciles to five of the source manifest's 139 declarations (`contracts/package.json`, `contracts/pyproject.toml`, `validators/pyproject.toml`, `validators/run_release_validation.py`, and `validators/tests/test_contracts.py`). This checkout drift is recorded as a source-provenance concern, not treated as a defect in the independently exact released artifact. Production provenance still requires a signed release and immutable source attestation.

## Commands executed

```text
python -B validators/run_release_validation.py
python -B -m unittest discover -s validators/tests -q
python -B -m pytest protocol/tests -q -p no:cacheprovider
```

All three commands were run in the candidate and repeated from a clean extracted copy. Results were PASS, 61/61, and 33/33 in both layouts. An independent receipt/hash script, an adversarial schema/migration/adapter script, and the following VAE suite also passed:

```text
python -B -m unittest validation.tests.test_delegation_rc2_integration -v
```

VAE result: **12/12 PASS**.

## Adoption disposition

Batch B contract integration is **PASS** for this exact local unsigned candidate. The pin and VAE-owned integration artifacts may be used for architecture/readiness evidence. They do not confer production trust, publication, implementation authorization, or Stage 5 permission. Shared Delegation schemas and generated bindings remain unmodified and unforked.

