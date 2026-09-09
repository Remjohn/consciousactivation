# Mandate ID & Title

**CA-M043 — Merkle Receipt Chaining**

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py` | Added deterministic CAE receipt records, predecessor-linked SHA-256 chaining, ordered binary Merkle-root commitment, evidence-chain construction for raw evidence / gate decisions / distribution deliverables, strict workspace/execution/campaign identity binding, persisted SQLite adapter, and fail-closed verification for digest, parent, sequence, gap, reorder, and identity corruption. | `INV-MRK-001`: an accepted receipt sequence is cryptographically bound to its immediate predecessor and can be committed to one deterministic root hash without weakening tenant/execution/campaign boundaries. |
| `tests/cae/test_ca_m043_merkle_receipts.py` | Added 26 self-contained tests covering canonical serialization, first/root behavior, parent linkage, deterministic hashes, payload/parent tampering, missing predecessors, reordering, cross-boundary rejection, raw→gate→deliverable root construction, accepted-transition binding, SQLite persistence/reread verification, and phantom-receipt prevention. | Independent reread verification detects modified stored payloads, parent pointers, identity, and broken sequence lineage; multi-stage evidence receives one reproducible root. |

## Files Added and Files Modified

### Files Added

- `packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py` — new CA-M043 implementation. It is deliberately self-contained and uses the repository's existing `ca_contracts.canonical_json_text` convention when available. It does not replace the canonical state-transition store, introduce an external ledger, or invent a cryptographic service.
- `tests/cae/test_ca_m043_merkle_receipts.py` — new mandate-specific executable proof.

### Files Modified

None. The execution request explicitly restricted implementation/test output to the two target paths above. The existing `program_state_runtime.py` and its `cae_program_state_transitions` schema remain unchanged.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. Copy `packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py` to the exact repository destination `packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py`.
2. Copy `tests/cae/test_ca_m043_merkle_receipts.py` to the exact repository destination `tests/cae/test_ca_m043_merkle_receipts.py`.
3. No database migration is bundled because this execution was constrained to the two requested paths. `SQLiteMerkleReceiptStore` creates its additive `cae_merkle_receipts` table on first use. It intentionally does not rewrite or auto-migrate `cae_program_state_transitions`, preserving Q41 atomic-CAS ownership.
4. In an environment with the normal project dependencies installed, run the test command below. No external service or secret is required for the CA-M043 proof.

**Important integration limitation:** this bounded delivery provides the authoritative cryptographic primitive plus a persistence adapter, but does not wire `UniversalProgramStateRuntime.record_transition()` into the new adapter because modifying `program_state_runtime.py` would exceed the user-specified file boundary. The canonical runtime transition table therefore remains unchanged by this bundle. Full end-to-end automatic receipt creation at the Q41 commit boundary requires that integration in a subsequent, explicitly authorized change.

## Test Command

```bash
PYTHONPATH=packages/ca_contracts/src pytest -q tests/cae/test_ca_m043_merkle_receipts.py
```

## Expected Test Results

**26 automated tests, all passing.**

Sandbox verification result:

```text
26 passed in 0.10s
```

Additional syntax verification:

```bash
python -m py_compile packages/ca_runtime/src/ca_runtime/merkle_receipt_chain.py tests/cae/test_ca_m043_merkle_receipts.py
```

The adjacent CA-M042 dependency suite was attempted but could not collect in this sandbox because the uploaded repository environment does not include the optional `psycopg` dependency imported by `ca_runtime.__init__`. This is recorded as an environment limitation; it did not affect the CA-M043 focused suite, whose tests intentionally load the target module without invoking unrelated package-level database dependencies.
