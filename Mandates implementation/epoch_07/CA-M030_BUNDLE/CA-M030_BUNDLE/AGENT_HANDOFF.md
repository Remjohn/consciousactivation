# Mandate ID & Title

**Mandate ID:** CA-M030  
**Mandate Title:** Immutable Release Manifest  
**Requirement / Invariant:** FR-REL-001 / INV-REL-001 — immutable digest-backed release boundary.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/release_manifest.py` | Added deterministic release-manifest builder, immutable artifact declarations, license metadata, recursive provenance trees, SHA-256 Merkle-root calculation, manifest SHA-256 identity, HMAC-SHA256 cryptographic seal, persistence/reload, real filesystem artifact verification, lineage checks, and overwrite protection for sealed manifests. | A sealed release is independently re-verifiable; declared artifact bytes are re-hashed from disk; any artifact or manifest mutation fails closed; lineage/policy mismatches fail closed. |
| `tests/wave04/test_ca_m030_release_manifest.py` | Added 14 focused acceptance/negative/false-proof tests using real temporary filesystem artifacts and persisted JSON manifests. | Positive sealing, deterministic identity, byte mutation detection, manifest tamper detection, missing lineage, policy mismatch, wrong secret, missing artifact mapping, Merkle identity change, immutable persistence, and the required top-level-hash-only false proof are exercised. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

- `packages/ca_runtime/src/ca_runtime/release_manifest.py` — smallest direct runtime implementation needed for CA-M030. No pre-existing runtime module existed at this requested destination.
- `tests/wave04/test_ca_m030_release_manifest.py` — self-contained mandate proof suite. No pre-existing M030 test module existed at this requested destination.

### Files Modified

None. The supplied repository snapshot was not altered outside the two mandate-scoped additions above.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

Copy these bundle paths into the repository preserving the exact relative destinations:

```text
CA-M030_BUNDLE/packages/ca_runtime/src/ca_runtime/release_manifest.py
CA-M030_BUNDLE/tests/wave04/test_ca_m030_release_manifest.py
```

No database migration is required by these two files. The signing secret is intentionally external to the manifest and must be supplied by the governed release authority at runtime; do not persist it in the manifest or repository.

Post-apply verification:

```bash
PYTHONPATH=packages/ca_contracts/src pytest -q tests/wave04/test_ca_m030_release_manifest.py
PYTHONPATH=packages/ca_contracts/src python -m py_compile packages/ca_runtime/src/ca_runtime/release_manifest.py tests/wave04/test_ca_m030_release_manifest.py
```

The implementation does not execute external distribution. A downstream release/distribution integration should call `ReleaseManifest.verify(...)` against the actual artifact paths before permitting shipment.

## Test Command (exact pytest/test command to verify)

```bash
PYTHONPATH=packages/ca_contracts/src pytest -q tests/wave04/test_ca_m030_release_manifest.py
```

## Expected Test Results (number of automated tests, all passing)

**14 automated tests — 14 passing, 0 failing.**

Focused result observed in the execution sandbox:

```text
14 passed in 0.09s
```

### Evidence and limitations

- **TEST / EXECUTABLE:** `tests/wave04/test_ca_m030_release_manifest.py` exercises real temporary files, persisted JSON, cryptographic verification, and negative mutation cases.
- **FALSE-PROOF TEST:** `test_false_proof_top_level_manifest_hash_without_real_artifact_verification_fails` demonstrates that a correct stored manifest hash is insufficient after post-seal artifact-byte mutation; verification re-reads the actual file and fails closed.
- **SCHEMA collision:** the repository already contains `packages/ca_release/src/ca_release/schemas/release_manifest.schema.json`, while the requested M030 runtime surface did not previously exist. This bundle intentionally does not modify that shared schema because M030's mandate file boundary prohibits unrelated/shared-surface expansion. Full production-path schema integration therefore remains an explicit follow-up/integration decision rather than an ungoverned change here.
- **RUNTIME integration limitation:** the supplied environment cannot collect the existing release/API integration tests because repository dependencies are incomplete (`ca_release` is not installed; the API path also requires `psycopg`). The M030-focused proof remains green and self-contained.
- **AUTHORITY/sealing limitation:** the repository's existing cryptographic receipt convention uses HMAC-SHA256. This implementation uses the same external-secret model for the manifest seal and labels the guarantee precisely as an HMAC cryptographic seal, not a public-key signature.
- **COMMIT SHA:** not captured. The supplied repository snapshot contains no `.git` directory, so an exact commit SHA cannot be truthfully reported.
