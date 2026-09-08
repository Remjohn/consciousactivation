# CA-M032 — Governed Memory Write-Back

## Mandate ID & Title

**Mandate ID:** CA-M032  
**Mandate Title:** Governed Memory Write-Back  
**Requirement / Invariant:** INV-MEM-001

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/memory_writeback.py` | Added the authoritative SQLite-backed governed memory write-back boundary: strict `LearningCandidate` schema, explicit evidence/attribution/confidence policy, hash-bound merge consensus, version-checked promotion, provenance persistence, durable promotion receipts, idempotency, and explicit raw-observation rejection. | Raw observations cannot cross the durable boundary; only schema-conformant, attributed, threshold-qualified candidates with consensus may promote; stale writers are rejected fail-closed. |
| `tests/wave05/test_ca_m032_memory_writeback.py` | Added 9 self-contained pytest cases covering positive promotion, raw overwrite rejection, false-proof dict rejection, confidence failure, consensus failure, stale-version conflict, idempotency/conflict, persistence, and two-writer concurrency. | Executable evidence at the real SQLite persistence boundary, including negative/fail-closed cases and the concurrency race that would expose lost-update behavior. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

`packages/ca_runtime/src/ca_runtime/memory_writeback.py`  
Rationale: The supplied repository archive did not contain the mandated runtime module, so this file establishes the named canonical write-back boundary without changing unrelated stores or manifests.

`tests/wave05/test_ca_m032_memory_writeback.py`  
Rationale: The supplied repository archive did not contain the mandated CA-M032 test surface, so this file supplies the required self-contained executable proof.

### Files Modified

None.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. From the repository root, copy:
   - `CA-M032_BUNDLE/packages/ca_runtime/src/ca_runtime/memory_writeback.py` → `packages/ca_runtime/src/ca_runtime/memory_writeback.py`
   - `CA-M032_BUNDLE/tests/wave05/test_ca_m032_memory_writeback.py` → `tests/wave05/test_ca_m032_memory_writeback.py`
2. No migration or external schema script is required. The runtime module initializes its three SQLite tables (`memory_items`, `memory_provenance`, `memory_writeback_receipts`) with `CREATE TABLE IF NOT EXISTS` at store initialization.
3. Install the repository's normal Python dependencies before running the repository-wide suite. The CA-M032 test itself uses direct module loading so it can execute in the supplied sandbox even though the archive's top-level `ca_runtime` package import currently requires the unavailable `psycopg` dependency.
4. Run the exact mandate test command below.

## Test Command (exact pytest/test command to verify)

```bash
PYTHONPATH=packages/ca_contracts/src:packages/ca_runtime/src pytest -q tests/wave05/test_ca_m032_memory_writeback.py
```

## Expected Test Results (number of automated tests, all passing)

**9 automated tests — all passing.**

Observed result in the supplied sandbox:

```text
.........                                                                [100%]
9 passed in 0.22s
```

### Evidence locators

- `memory_writeback.py:193-307` — strict `LearningCandidate` schema and conversion.
- `memory_writeback.py:310-327` — explicit configurable promotion policy; attribution and consensus cannot be disabled.
- `memory_writeback.py:421-469` — durable SQLite schema for memory, provenance, and receipts.
- `memory_writeback.py:471-487` — atomic `BEGIN IMMEDIATE` transaction boundary.
- `memory_writeback.py:496-522` — evidence, attribution, confidence, and consensus validation.
- `memory_writeback.py:605-710` — authoritative promotion path and stale-version conflict rejection.
- `memory_writeback.py:711-748` — persisted evidence and attribution provenance.
- `memory_writeback.py:750-780` — durable promotion receipt.
- `memory_writeback.py:781-786` — explicit raw-observation rejection.
- `test_ca_m032_memory_writeback.py:93-112` — positive governed promotion, provenance, and receipt.
- `test_ca_m032_memory_writeback.py:114-132` — raw-overwrite rejection and false-proof dict rejection.
- `test_ca_m032_memory_writeback.py:135-143` — confidence threshold failure.
- `test_ca_m032_memory_writeback.py:145-164` — merge-consensus rejection.
- `test_ca_m032_memory_writeback.py:166-192` — stale-writer conflict / no lost update.
- `test_ca_m032_memory_writeback.py:194-204` — candidate idempotency and mutated-candidate conflict.
- `test_ca_m032_memory_writeback.py:206-222` — persistence across store instances.
- `test_ca_m032_memory_writeback.py:225-256` — two concurrent SQLite writers; exactly one promotion succeeds.

## Limitations / residual claims

- The supplied archive is not a git checkout, so no repository commit SHA is available for capture in this handoff.
- The referenced `docs/cae/CAE_Product_Brief/17_Memory_Writeback.md` source file is not present in the supplied archive. The implementation was therefore grounded in the present CA-M032 mandate, the Q32 decision ledger, `Architecture.md`, `FUNCTIONAL_REQUIREMENTS.md`, and the Stage 15/17 operating-model text that is present.
- The repository's top-level `ca_runtime` package import fails in this sandbox because `psycopg` is not installed. The CA-M032 tests load only the mandated module directly to keep proof isolated; a normal repository environment with declared dependencies should run the module through the package import path.
- The implementation makes the confidence/evidence thresholds explicit and configurable rather than claiming a missing canonical numeric threshold. The acceptance suite uses `8000/10000` confidence and two evidence references as its test policy.

## Operator Decision

The evidence package is ready for Operator review. **Approve or reject CA-M032 based on whether the executable proof satisfies INV-MEM-001 at the canonical memory write-back boundary.**
