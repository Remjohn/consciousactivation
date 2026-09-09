# CA-M026 — Durable Authorization Decision Receipts

## Mandate ID & Title

**Mandate ID:** CA-M026  
**Title:** Durable Authorization Decision Receipts  
**Requirement / Invariant:** FR-AUTH-001  
**Status:** Implementation complete; focused executable proof passed 18/18 tests.

## Summary Table (File changed | What changed | Invariant proven)

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py` | Added a durable SQLite-backed authorization receipt ledger with GRANT, DENY, and OPERATOR_OVERRIDE outcomes; required actor/reason/policy/timestamp fields; exact resource revision/state binding; SHA-256 receipt identity; HMAC-SHA256 signature; predecessor hash chaining; append-only SQLite triggers; fresh-read verification APIs. | Every receipt recorded through the ledger is cryptographically bound to actor identity, decision reason, policy hash, timestamp, and inspected resource revision/state. Content, signature, and chain tampering fail verification. |
| `tests/wave04/test_ca_m026_auth_receipts.py` | Added 18 self-contained tests covering positive outcomes, required fields, hash chaining, persistence/reopen, tampering, wrong-key verification, append-only enforcement, revision binding, duplicate conflicts, and the false-proof countercase. | Executable proof that the CA-M026 receipt contract is durable, tamper-evident, fail-closed on malformed input, and independently verifiable after reopen. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

1. `packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py`
   - Adds the CA-M026 receipt authority.
   - No existing repository files are required to be modified.
   - Uses only Python standard-library facilities, so the receipt cryptographic and durable ledger behavior does not introduce a new dependency.
   - The signing key is intentionally external to the receipt database. Losing/changing the key causes signature verification to fail rather than silently accepting forged records.

2. `tests/wave04/test_ca_m026_auth_receipts.py`
   - Adds mandate-specific executable verification at the requested Wave 04 path.
   - Tests the actual durable SQLite ledger rather than a mock or parser-only representation.

### Files Modified

None.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

From the repository root, copy the two bundled files to these exact destinations, preserving their contents:

```text
CA-M026_BUNDLE/packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py
    -> packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py

CA-M026_BUNDLE/tests/wave04/test_ca_m026_auth_receipts.py
    -> tests/wave04/test_ca_m026_auth_receipts.py
```

No repository migration is required. The receipt ledger creates its own SQLite schema, indexes, metadata row, and append-only UPDATE/DELETE guards when `AuthorizationDecisionReceiptStore` is initialized.

Runtime setup requires a signing key supplied by the canonical authorization runtime, for example:

```python
from ca_runtime.auth_decision_receipts import AuthorizationDecisionReceiptStore

store = AuthorizationDecisionReceiptStore(
    "/path/to/authorization.sqlite3",
    signing_key=trusted_runtime_signing_key,
)
```

Use the same trusted signing key when reopening the durable store for independent verification. Do not persist the signing key inside the receipt database.

Post-apply verification:

```bash
python -m py_compile packages/ca_runtime/src/ca_runtime/auth_decision_receipts.py tests/wave04/test_ca_m026_auth_receipts.py
pytest -q tests/wave04/test_ca_m026_auth_receipts.py
```

The normal repository test command requires the repository's declared runtime dependencies to be installed. In the supplied sandbox, the repository package initializer attempted to import `psycopg`, which was not installed. To isolate and prove this new standard-library-only subsystem, the focused suite was run with a temporary import shim that bypassed the unrelated package initializer. That isolated execution passed 18/18 tests.

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/wave04/test_ca_m026_auth_receipts.py
```

## Expected Test Results (number of automated tests, all passing)

**18 automated tests; 18 passing (100%).**

The focused suite proves:

- GRANT receipt creation.
- DENY receipt creation.
- OPERATOR_OVERRIDE receipt creation.
- Required actor identity, reason, policy hash, and timestamp.
- SHA-256 receipt integrity.
- HMAC-SHA256 cryptographic attribution.
- Hash-chain predecessor binding.
- Durable persistence across close/reopen.
- Tamper detection after direct database modification.
- Wrong signing-key rejection.
- Append-only UPDATE/DELETE rejection.
- Fail-closed validation of required fields.
- Invalid policy-hash rejection.
- Exact resource revision/state binding.
- Conflicting duplicate receipt protection.
- False-proof countercase rejection.

### Evidence classification

- `EXECUTABLE`: receipt creation, validation, hashing, signing, chain verification.
- `MIGRATION/SCHEMA`: SQLite schema and append-only trigger creation performed by the implementation.
- `TEST`: all 18 focused tests.
- `PERSISTENCE`: close/reopen verification against the durable SQLite file.
- `CRYPTOGRAPHIC_INTEGRITY`: content-hash and HMAC verification.
- `FALSE_PROOF`: forged actor/decision content is rejected despite valid-looking strings.

### False-proof countercase

A browser/parser-style implementation could display a valid actor and `GRANT` decision without proving that the durable receipt was authentic. CA-M026 explicitly mutates persisted actor content after creation and verifies that the ledger rejects it. This test passes, proving the implementation does not trust display strings alone.

### Residual limitation

This bounded file change establishes and proves the durable receipt ledger API. It does not silently retrofit every pre-existing authorization caller because that would require modifying the canonical caller surfaces outside the mandate's explicitly bounded target files. The consuming canonical authorization boundary must route every consequential grant, denial, and operator override through `AuthorizationDecisionReceiptStore`.

### Operator decision

**Requested Operator decision:** Approve or reject CA-M026 based on the evidence above. No downstream canonical question was started.
