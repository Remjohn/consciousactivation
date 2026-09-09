# CA-M031 — External Distribution Delivery

## Mandate ID & Title

**Mandate ID:** CA-M031  
**Mandate Title:** External Distribution Delivery  
**Requirement / Invariant:** FR-DIST-001  
**Canonical question:** Q30  
**Wave:** 04

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/distribution_delivery.py` | Added the execution-only external distribution boundary: sealed-release verification before transmission, immutable byte-only adapter input, explicit allow-listed technical transforms (`IDENTITY`, `CONTAINER`, `CODEC`), independent semantic fingerprint comparison, deterministic idempotency keys, exponential backoff, retry history, immutable receipt history, and HMAC-SHA256 signed delivery receipts. | `FR-DIST-001`: distribution consumes the exact sealed release identity, refuses invalid/mutated releases, blocks semantic transformations, retries with one stable idempotency key, and emits verifiable delivery evidence. |
| `tests/wave04/test_ca_m031_distribution_delivery.py` | Added self-contained repository-native integration tests for positive delivery, idempotent replay, exponential retry/backoff, failed-delivery recovery, manifest mutation rejection, semantic rewrite rejection, semantic projection mismatch, idempotency conflict, exact release attribution across releases in one campaign, receipt tamper detection, and backoff capping. | The negative/fail-closed and contrastive false-proof cases are executable, not documentation-only or mock-call assertions. |

## Files Added and Files Modified

### Files Added

1. `packages/ca_runtime/src/ca_runtime/distribution_delivery.py`  
   Rationale: the requested distribution-delivery runtime surface did not exist in the supplied codebase. This is the smallest direct implementation boundary for CA-M031.

2. `tests/wave04/test_ca_m031_distribution_delivery.py`  
   Rationale: the requested mandate-specific acceptance test surface did not exist. Tests are self-contained and exercise the delivery boundary against the existing `ReleaseManifestBuilder` / `ReleaseManifest.verify()` contract.

### Files Modified

None.

No migration, API router, UI, database schema, or unrelated runtime file was changed.

## Exact paste instructions and post-apply commands

1. From the repository root, extract/copy the bundle while preserving the paths inside `CA-M031_BUNDLE/`.
2. Copy `CA-M031_BUNDLE/packages/ca_runtime/src/ca_runtime/distribution_delivery.py` to exactly:
   `packages/ca_runtime/src/ca_runtime/distribution_delivery.py`
3. Copy `CA-M031_BUNDLE/tests/wave04/test_ca_m031_distribution_delivery.py` to exactly:
   `tests/wave04/test_ca_m031_distribution_delivery.py`
4. Copy `CA-M031_BUNDLE/AGENT_HANDOFF.md` to the repository root only if the receiving workflow requires a local handoff record; it is not a production runtime dependency.
5. No migrations or setup scripts are required by this bounded change.
6. The runtime implementation depends only on the existing `ca_contracts` canonical JSON/hash primitives and the existing `ReleaseManifest` boundary.
7. Recommended post-apply checks from the repository root:

```bash
python -m py_compile packages/ca_runtime/src/ca_runtime/distribution_delivery.py
pytest -q tests/wave04/test_ca_m031_distribution_delivery.py tests/wave04/test_ca_m030_release_manifest.py
```

## Test Command

Exact verification command from repository root:

```bash
pytest -q tests/wave04/test_ca_m031_distribution_delivery.py tests/wave04/test_ca_m030_release_manifest.py
```

Focused mandate-only command:

```bash
pytest -q tests/wave04/test_ca_m031_distribution_delivery.py
```

## Expected Test Results

- Mandate-only tests: **11 automated tests, all passing**.
- CA-M030 regression + CA-M031: **25 automated tests, all passing**.
- Latest sandbox result: **25 passed in 0.10s**.
- Latest focused CA-M031 result: **11 passed in 0.12s**.

## Evidence / Proof Notes

- `EXECUTABLE`: `distribution_delivery.py` calls `ReleaseManifest.verify()` before adapter execution, re-reads the sealed artifact bytes, and blocks transmission on digest/seal failure.
- `EXECUTABLE`: adapters receive `SealedReleasePackage` / `SealedReleaseArtifact` values containing immutable `bytes`; filesystem paths are not exposed to the adapter.
- `EXECUTABLE`: only explicit technical transformation classes are accepted; unknown or `SEMANTIC*` transformations fail closed before publish.
- `EXECUTABLE`: semantic equivalence is checked independently over source and delivered bytes through the injected semantic fingerprint function, and the adapter's declared semantic projections must agree with that verifier.
- `EXECUTABLE`: the same deterministic idempotency key is supplied to every retry; successful replays return the original signed receipt without a second publish.
- `TEST`: tests cover the mandate-specific contrastive false-proof case where a destination-accepted semantic rewrite is rejected before any publish call.
- `TEST`: release identity is bound to `release_id` and `release_manifest_sha256`; two releases under one campaign produce distinct delivery identities, avoiding campaign-name/latest-release joins.
- `TEST`: receipt digest/signature tampering is detected.

## Residual limitations / explicit stop conditions

- No live third-party publishing platform or CDN was contacted in the sandbox. The proof is repository-native through the concrete adapter boundary and in-process publishing endpoint behavior.
- The provided runtime surface has no existing durable distribution-receipt schema compatible with CA-M031's destination/release identity shape, and file-boundary restrictions prohibit adding one here. `DeliveryLedger` therefore provides thread-safe immutable local receipt history; production integration should persist these receipts through the repository's existing canonical receipt/persistence owner without changing release identity.
- Current authorization is represented by and verified within the sealed Release Manifest. This bounded module does not introduce a second live authorization registry or outcome attribution path.
- No semantic transformation has been invented or implemented beyond the explicitly enumerated technical transformation classes.

## Reconstructed-source commit SHA

The supplied archive contained no `.git` metadata, so no upstream commit SHA could be recovered. For reproducibility, the supplied archive was reconstructed into an isolated local Git repository and the CA-M031 additions were committed there.

**Baseline snapshot commit:** `85b6a8a256ac361a3feb3f45414eeb0e64e9a6f9`  
**CA-M031 implementation commit:** `a0d9a89d63eefbd017140f690f2afb73b25e1af9`

The CA-M031 commit contains exactly these two additions:

```text
A  packages/ca_runtime/src/ca_runtime/distribution_delivery.py
A  tests/wave04/test_ca_m031_distribution_delivery.py
```

## Operator decision

**Approve or reject CA-M031 based on executable evidence at the canonical release-to-distribution boundary.** Per the mandate, no approval is inferred from the green tests alone.
