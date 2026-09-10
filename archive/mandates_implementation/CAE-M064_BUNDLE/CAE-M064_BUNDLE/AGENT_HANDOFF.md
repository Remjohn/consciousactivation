# CAE-M064 — Asset Selection, Production Binding and Lineage Handoff

## Mandate ID & Title

**Mandate ID:** CAE-M064 (repository canonical mandate: CAE-M0064)  
**Mandate Title:** Asset Selection, Production Binding and Lineage Handoff  
**Requirement / Invariant:** INV-ASSET-LINEAGE-001  
**Implementation commit (local execution fingerprint):** `7e10318aba38c01e85891d8ef534563045158770`  
**Source archive SHA-256:** `aaab6d5e1ee293ba841f9ecc07dd717ecbc61feaf4619747a6dda8dc2f43fb19`  

The supplied repository archive did not contain `.git` metadata, so no pre-existing upstream commit SHA could be truthfully captured. A local Git repository was initialized only to fingerprint the post-implementation tree; the commit above is **not** asserted to be an upstream repository commit.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/production-program/src/cae_production_program/composition_asset_pack.py` | Added typed explicit-selection receipt, candidate identity snapshot, `CompositionAssetBinding`, `CompositionAssetPack`, deterministic lineage-DAG hashing, binding resolver, pack validation/invalidation, and projection into the existing `SemanticProgram`/`CompositionHandoffReceipt` chain. | Exact selected asset ID, scene, workspace, source version/hash, interval, semantic/insert role, rights, provenance, selection authority, upstream receipt and program reference remain bound and tamper-evident; no downstream re-selection is performed. |
| `services/production-program/src/cae_production_program/__init__.py` | Exported the new production binding API. | The binding boundary is part of the existing production-program public surface rather than a parallel runtime-only path. |
| `packages/ca_runtime/src/ca_runtime/composition_asset_handoff.py` | Added runtime handoff resolver and receipt verifier that accepts only a `BOUND` `CompositionAssetPack` and emits exact runtime asset inputs carrying the same binding/root lineage. | Runtime inputs are a typed projection of the already-selected bound assets; asset-set substitution or tampered handoff receipts are rejected. |
| `packages/ca_runtime/src/ca_runtime/__init__.py` | Exported the runtime handoff API. | The verified handoff is reachable through the canonical runtime package surface. |
| `tests/production_program/test_m0064_asset_selection_binding_lineage.py` | Added 14 self-contained tests covering selection, binding, projection, runtime handoff, tampering, invalidation, substitution, determinism, program-reference mismatch and scene-set mismatch. | Required false-proof and lineage-invalidation cases fail closed, while valid selection→binding→runtime flow passes. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

`services/production-program/src/cae_production_program/composition_asset_pack.py`  
Rationale: implements the missing selection→production binding boundary and preserves the governed candidate snapshot plus upstream selection evidence in a tamper-evident pack.

`packages/ca_runtime/src/ca_runtime/composition_asset_handoff.py`  
Rationale: converts only a validated bound pack into executable runtime asset inputs and preserves the lineage root through the final runtime handoff receipt.

`tests/production_program/test_m0064_asset_selection_binding_lineage.py`  
Rationale: provides the M0064 production-bound fixture and invalidation/false-proof verification suite.

### Files Modified

`services/production-program/src/cae_production_program/__init__.py`  
Rationale: exposes the new production binding types/functions without changing unrelated production-program behavior.

`packages/ca_runtime/src/ca_runtime/__init__.py`  
Rationale: exposes the new runtime handoff types/functions without changing unrelated runtime behavior.

No unrelated repository files were modified.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

From the repository root, copy the bundle contents into the exact paths listed above, preserving existing files and replacing only the two modified `__init__.py` files. The bundle contains complete files, not patches or truncations.

No database migration, schema migration, registry migration, seed script, or generated-artifact update is required for this implementation. The feature is purely typed Python behavior and test coverage.

Recommended post-apply verification:

```bash
cd <repository-root>
PYTHONPATH='services/production-program/src:services/asset-intelligence/src:packages/ca_runtime/src' pytest -q tests/production_program tests/asset_intelligence tests/cae/test_asset_demand_resolution_runtime.py
```

The focused mandate test may be run independently with:

```bash
cd <repository-root>
PYTHONPATH='services/production-program/src:services/asset-intelligence/src:packages/ca_runtime/src' pytest -q tests/production_program/test_m0064_asset_selection_binding_lineage.py
```

## Test Command (exact pytest/test command to verify)

```bash
PYTHONPATH='services/production-program/src:services/asset-intelligence/src:packages/ca_runtime/src' pytest -q tests/production_program tests/asset_intelligence tests/cae/test_asset_demand_resolution_runtime.py
```

Focused command:

```bash
PYTHONPATH='services/production-program/src:services/asset-intelligence/src:packages/ca_runtime/src' pytest -q tests/production_program/test_m0064_asset_selection_binding_lineage.py
```

## Expected Test Results (number of automated tests, all passing)

**59 automated tests: 59 passed, 0 failed.**  
Focused M0064 suite: **14 passed, 0 failed.**  
Python byte-compilation of the new/modified implementation and test modules also passed.

## Evidence and verification fidelity

**State transition proven:** `CANDIDATE_SELECTED → BOUND → RUNTIME_READY|BLOCKED`.

- **Actor:** the explicit selection authority supplies the selection receipt; the bounded production resolver performs binding; the runtime handoff resolver performs final executable-input validation.
- **Preconditions:** explicit selection receipt is internally hash-valid; selected candidate set is exact; candidate workspace/candidate identity is in scope; source hash, source version, interval, semantic role, insert role, rights and provenance are present; the production-program reference is exact and hash-valid.
- **Validators:** candidate identity snapshots, `CompositionAssetPack` model validation, lineage-root recomputation, pack digest verification, current-candidate snapshot comparison, current selection-receipt comparison, current program-reference comparison, and runtime handoff digest verification.
- **Postconditions:** `CompositionAssetPack.state == BOUND`; all bindings derive from the explicit selection only; a deterministic lineage root covers each binding, candidate snapshot, selection receipt and program reference; runtime input fields are exact projections of those bindings.
- **Receipt:** `ExplicitSelectionReceipt`, `CompositionAssetPack.pack_sha256`, `CompositionAssetPack.lineage_root_sha256`, and the runtime `RuntimeAssetHandoff.handoff_sha256` provide tamper-evident evidence through the boundary.
- **Error route:** lineage mismatches raise `AssetLineageValidationError`/`AssetBindingInvalidatedError`; runtime mismatches raise `RuntimeAssetLineageError`. These fail closed as `BLOCKED` rather than silently substituting another asset.
- **Recovery:** invalidate only the newly produced bound package/version. The original bound pack is immutable and is retained; a corrected selection must produce a new receipt/binding/pack lineage.

**What the verifier actually measures:** exact governed field equality and digest equality across the selection, source identity, source version/hash, timestamps, roles, rights, provenance, program reference, binding hashes and runtime handoff.

**What it does not measure:** it does not independently open media files and recompute their byte hashes; it trusts the authoritative `source_sha256` supplied by the governed retrieval candidate. It also does not make a legal determination that a rights snapshot is substantively correct. Those remain upstream authority responsibilities.

**False-proof countercase:** tests mutate a candidate's `source_sha256`, timestamp, semantic role, rights or provenance while keeping the asset otherwise equivalent-looking. Each mutation invalidates binding. The suite also rejects asset-set substitution, extra selected scenes, and a changed program reference.

**Environment-fidelity requirement:** the production binding tests execute the real production-program models and the real asset-intelligence candidate contract. The supplied sandbox lacks the `psycopg` dependency needed for importing the full `ca_runtime` package, so the M0064 runtime module is loaded directly in the test to verify its real code without importing unrelated database infrastructure. Deployment environments that import `ca_runtime` normally must provide the package's existing dependency set.

**Operator validation required:** **Yes.** The implementation stops at M0064. No automatic approval or promotion to M0065 is performed. The required operator decision remains: **“Do you accept M0064 and authorize M0065?”**

## Control-state limitation

The provided archive contains the governing M0064 mandate but no dedicated M0064 campaign-control-state record that can be updated without widening the mandate file boundary. No unrelated global control-state document was modified. This handoff records the implementation evidence and explicitly flags that limitation for the operator/control-plane authority.

## Stop condition

M0064 implementation, bounded verification, evidence capture and bundle preparation are complete. No M0065 work was started.
