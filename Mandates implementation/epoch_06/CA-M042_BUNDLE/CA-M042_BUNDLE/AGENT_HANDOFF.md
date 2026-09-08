# Mandate ID & Title

**Mandate ID:** `CA-M042`  
**Mandate Title:** `Atomic CAS State Transitions in SQLite`  
**Primary Requirement / Invariant:** `INV-CAS-001`  
**Canonical Question:** `Q41`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py` | Added the dedicated SQLite CAS primitive. It performs `UPDATE ... SET version = version + 1 ... WHERE aggregate_id = ? AND version = ?`, treats `cursor.rowcount == 1` as the only success condition, and maps a zero-row predicate miss to a typed CAS conflict/not-found error without retrying the failed write. | **INV-CAS-001:** the database predicate, not a Python read-before-write comparison, controls whether the aggregate advances from version N to N+1. |
| `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | Changed `SqliteProgramStateStore.save_aggregate()` to run inside `BEGIN IMMEDIATE` and route every versioned aggregate update through the CAS primitive. Existing public `ProgramStateVersionConflictError` behavior is preserved; failed CAS operations roll back and therefore cannot be followed by transition-record persistence. | **INV-CAS-001:** stale writers fail closed, successful writers commit exactly one version increment, and the canonical runtime receives the persisted conflict as a typed version mismatch. |
| `tests/cae/test_ca_m042_sqlite_cas.py` | Added four self-contained real-SQLite tests covering N→N+1 success, stale-version rejection with no state mutation, two independent SQLite store connections competing on the same expected version, and receipt/transition consistency after a rejected CAS. | **INV-CAS-001:** executable proof demonstrates one successful logical winner and one deterministic conflict without using a process-local mutex as the concurrency mechanism. |

## Files Added and Files Modified

**Added**

`packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py` — smallest direct implementation surface for the Q41 CAS SQL predicate and its low-level typed conflict evidence. No schema or migration was required because the existing `cae_program_state_aggregates.version` column already supplies the required version field.

`tests/cae/test_ca_m042_sqlite_cas.py` — focused executable proof for the mandate. The concurrency test uses two independent `SqliteProgramStateStore` instances (therefore independent SQLite connections) and a test barrier only to force both workers to reach the persistence boundary before either CAS executes. The barrier is synchronization for the test; it is not a production lock and is not used to establish correctness.

**Modified**

`packages/ca_runtime/src/ca_runtime/program_state_runtime.py` — only the SQLite store integration and import surface were changed. The state machine, authority lanes, receipt construction, gate semantics, tenancy semantics, and other runtime files were left untouched.

**Not changed**

No SQLite migration/schema file was modified because the required aggregate version schema already exists. No unrelated runtime, API, authorization, receipt-chain, replay, lease, or security file was changed. No Q42+ implementation was started.

## Exact paste instructions and post-apply commands

Copy the three files from this bundle into the repository at these exact destinations, replacing/adding them exactly as named:

```text
CA-M042_BUNDLE/packages/ca_runtime/src/ca_runtime/sqlite_cas_transitions.py
CA-M042_BUNDLE/packages/ca_runtime/src/ca_runtime/program_state_runtime.py
CA-M042_BUNDLE/tests/cae/test_ca_m042_sqlite_cas.py
```

There is **no migration** to apply for CA-M042. The existing table `cae_program_state_aggregates` already contains the authoritative integer `version` column used by the CAS predicate.

Normal environment setup for the runtime package, where dependencies are not already installed:

```text
python -m pip install -e packages/ca_contracts -e packages/ca_runtime
```

Then run the exact mandate test command below. For regression coverage of the immediate predecessor gate mandates, also run:

```text
pytest -q tests/cae/test_ca_m040_gate_suspension.py tests/cae/test_ca_m041_gate_resumption.py
```

## Test Command

```text
pytest -q tests/cae/test_ca_m042_sqlite_cas.py
```

## Expected Test Results

**Automated tests included:** 4 CA-M042 tests.  
**Observed CA-M042 result:** `4 passed` (100%).  
**Observed adjacent regression result:** CA-M040 + CA-M041 = `18 passed` (100%); together with CA-M042, the unique focused set is `22 passed`.

**Execution environment:** Python `3.13.5`; SQLite `3.46.1`; real temporary on-disk SQLite databases; two independent SQLite store instances in the concurrency proof; no production process-local mutex or mocked database boundary.

**Executable proof covered:**

1. Matching expected version commits exactly one N→N+1 update and persists the winning state.
2. A stale expected version raises `ProgramStateVersionConflictError` with the observed current version and leaves the already-committed state unchanged.
3. Two independent SQLite connections presenting the same expected version produce exactly one `success` and one `conflict`, with final persisted version N+1 and exactly one transition record.
4. A rejected CAS produces no second transition and does not replace the accepted transition's `last_receipt_id`.

**False-proof countercase rejected:** a test that serializes callers behind one in-process `threading.Lock` is not used as proof. The production implementation relies on SQLite's `BEGIN IMMEDIATE` transaction boundary and the conditional `UPDATE` row-count predicate. The concurrency proof reaches that real database boundary through separate store connections.

**Repository regression limitation:** `tests/cae/test_universal_program_state_runtime.py` currently contains a pre-existing failing test, `test_collision_program_state_machine_execution_lifecycle`, caused by the existing in-memory gate-suspension path requiring a durable execution lease during a test fixture that initializes without one. The same test was executed against the unmodified pre-CA-M042 `program_state_runtime.py` and failed identically. This failure predates and is unrelated to the CA-M042 changes; no unrelated file was modified to suppress it.

**Sandbox dependency limitation:** the sandbox did not have the repository's `psycopg` dependency installed and outbound package installation was unavailable. The CA-M042 SQLite tests were therefore executed with a temporary, out-of-repository `psycopg` compatibility stub plus the repository's local package source paths. This stub was not included in the bundle and does not participate in the SQLite CAS path under test. A normal repository environment should install the declared runtime dependencies before running the exact command above.

**Control-state impact:** no repository control-state file was present in the supplied archive, so no control-state record was modified. The archive also contains no `.git` metadata; consequently an exact Git commit SHA cannot be captured from this delivery. The bundle itself is the immutable handoff artifact for the implemented changes.

**Operator decision requested:** `APPROVE` or `REJECT` CA-M042 based on whether the executable evidence proves atomic SQLite CAS semantics, stale-write rejection, and one-success/one-failure concurrency behavior at the canonical state-runtime boundary.
