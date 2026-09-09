# CA-M045 — Worker Restart and Zombie Lease Reconciliation

## Mandate ID & Title

**Mandate ID:** `CA-M045`  
**Mandate Title:** `Worker Restart and Zombie Lease Reconciliation`  
**Requirement / Invariant:** `INV-REC-001`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/zombie_reconciler.py` | Added a durable SQLite startup reconciler, CA-M045 lease schema extension (`lease_worker_id`, `lease_expires_at`), strict expiry/state/workspace predicates, atomic aggregate+lease+transition recovery, deterministic audit receipts, and idempotent startup aliases. | An expired `RUNNING` lease is reclaimed exactly once and moved to `PAUSED` without duplicate transition/run creation; unexpired, terminal/non-running, and foreign-workspace leases remain untouched. |
| `tests/cae/test_ca_m045_zombie_reconciler.py` | Added 9 self-contained durable SQLite tests covering positive recovery, unexpired preservation, non-running safety, startup idempotency, workspace fencing, state-hash integrity, receipt evidence, invalid expiry fail-closed behavior, and concurrent reconciliation. | The acceptance path is exercised against persisted SQLite state rather than a direct lifecycle mutation helper. |

## Files Added and Files Modified

**Files Added**

1. `packages/ca_runtime/src/ca_runtime/zombie_reconciler.py`  
   Rationale: The requested CA-M045 runtime surface did not exist in the supplied repository. The file contains the smallest bounded implementation of worker-lease expiry reconciliation and startup entry points.

2. `tests/cae/test_ca_m045_zombie_reconciler.py`  
   Rationale: The requested CA-M045 proof surface did not exist. The tests exercise the real SQLite lease/aggregate/transition boundary.

**Files Modified**

None. The supplied repository had no pre-existing CA-M045 target files, so no unrelated source files were changed.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. Copy the two bundled files into the exact repository paths shown above.

2. The reconciler owns the minimum durable schema extension because the supplied repository has no CA-M045 migration file and its existing `cae_program_execution_leases` table lacks `lease_worker_id` and `lease_expires_at`. On the first reconciler invocation, `ensure_schema()` adds those columns and the expiry index without altering existing row semantics.

3. Wire the provided startup entry point into the existing application lifecycle at the point where the canonical `SqliteProgramStateStore` database path is already known:

```python
from ca_runtime.zombie_reconciler import reconcile_on_startup

reconcile_on_startup(store=canonical_sqlite_program_state_store)
```

Or, when only the canonical SQLite path is available:

```python
from ca_runtime.zombie_reconciler import reconcile_on_startup

reconcile_on_startup(canonical_state_db_path)
```

The supplied archive's `api/main.py` does not instantiate the canonical CAE `SqliteProgramStateStore`, so adding a guessed database path there would create a new authority rather than use the existing one. That startup wiring is therefore deliberately not included in this bundle.

4. Lease acquisition/renewal code must populate the durable expiry fields in the canonical lease row. The reconciler does not invent a TTL or infer expiry from wall-clock age. The authoritative fields are:

```text
cae_program_execution_leases.lease_worker_id
cae_program_execution_leases.lease_expires_at
```

No separate migration script or data backfill is required for the two schema columns; `ensure_schema()` performs the additive schema step safely.

5. Do not enable automatic resume as part of CA-M045. Reconciliation reclaims the worker lease and moves the aggregate to `PAUSED`; subsequent execution resumption remains governed by the existing runtime/operator path.

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/cae/test_ca_m045_zombie_reconciler.py
```

Sandbox execution used the same repository test file with an external dependency shim because the supplied execution environment did not have `psycopg` installed. The implementation test result was:

```text
9 passed
```

A compatibility check against the existing CA-M042 SQLite CAS proof also passed:

```bash
pytest -q tests/cae/test_ca_m042_sqlite_cas.py
```

Result:

```text
4 passed
```

## Expected Test Results (number of automated tests, all passing)

**CA-M045 automated tests:** `9`  
**Expected result:** `9 passed`

The 9 tests prove:

- expired running lease → `PAUSED` + `RECLAIMED` lease + durable transition evidence;
- unexpired lease remains `RUNNING`/`LEASE_ACQUIRED`;
- expired non-running aggregate is not reclaimed;
- repeated startup reconciliation is idempotent and creates no duplicate run/transition;
- workspace fencing prevents cross-workspace reconciliation;
- committed state hash is recomputed from persisted state after recovery;
- worker identity and expiry are retained in immutable transition evidence;
- malformed expiry fails closed with no partial mutation;
- two concurrent startup/reconcile attempts yield exactly one winner.

**Evidence classes:** `SCHEMA`, `EXECUTABLE`, `TEST`.

**False-proof countercase rejected:** directly setting an aggregate lifecycle to `PAUSED` is not used as the acceptance path. The reconciler must discover the expired lease, apply the SQLite CAS, reclaim the lease, and append the durable transition record atomically.

**Residual limitation:** the uploaded repository archive contains no Git metadata, so an exact commit SHA is unavailable. The archive also does not contain the canonical application-level CAE state-store construction in `api/main.py`; therefore this bundle provides the startup callable but does not invent a database path and wire it to a guessed store. Operator review is required for the final lifecycle wiring point and for any clock-skew policy beyond the durable expiry predicate.

**Operator decision requested:** Approve or reject `CA-M045` based on the executable proof above, with the stated startup-wiring and Git-metadata limitations recorded.
