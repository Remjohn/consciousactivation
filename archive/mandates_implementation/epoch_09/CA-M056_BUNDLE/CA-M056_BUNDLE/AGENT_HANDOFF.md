# CA-M056 — SQLite WAL Concurrency & Tuning

## Mandate ID & Title

**Mandate ID:** CA-M056  
**Mandate Title:** SQLite WAL Concurrency & Tuning  
**Governing Invariant:** INV-WAL-001

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/sqlite_tuning.py` | Added a canonical SQLite tuning policy and live-connection enforcement/verification for WAL journaling, 60-second busy timeout, 256 MiB mmap target, 1,000-page WAL auto-checkpointing, synchronous mode, explicit PASSIVE checkpointing, connection opening, and a dedicated background checkpoint worker. | **INV-WAL-001:** the effective live connection reports `journal_mode=wal`, `busy_timeout=60000`, configured `mmap_size`, and `wal_autocheckpoint`; background checkpoints execute through a dedicated connection and surface checkpoint errors instead of hiding them. |
| `tests/cae/test_ca_m056_sqlite_tuning.py` | Added 11 self-contained tests covering live PRAGMA verification, persistence across reopen, separate-process policy reopen, independent-connection policy consistency, negative PRAGMA verification, checkpoint counters, background checkpointing, write-lock waiting, and the process-local-lock false-proof countercase. | **INV-WAL-001:** positive and negative behavior is exercised against real SQLite connections and durable files rather than constants or a process-local mutex. |

## Files Added and Files Modified

### Files Added

- `packages/ca_runtime/src/ca_runtime/sqlite_tuning.py` — new runtime tuning boundary for CA-M056. The source archive did not contain this file.
- `tests/cae/test_ca_m056_sqlite_tuning.py` — new mandate-specific test suite. The source archive did not contain this file.

### Files Modified

None. No unrelated repository files were changed.

## Exact paste instructions and post-apply commands

Paste the bundle contents into the repository root so the paths are copied exactly as:

```text
packages/ca_runtime/src/ca_runtime/sqlite_tuning.py
tests/cae/test_ca_m056_sqlite_tuning.py
```

No migration is required by these two artifacts, and no existing migration ledger is modified.

Run from the repository root:

```bash
python -m pytest tests/cae/test_ca_m056_sqlite_tuning.py -q
```

The tuning module is intentionally standalone. A caller that opens a CAE SQLite state-store connection should use:

```python
from ca_runtime.sqlite_tuning import open_sqlite_connection

connection = open_sqlite_connection(db_path)
```

or apply the same policy to an existing live connection with `configure_sqlite_connection(...)`.

For periodic background checkpoints:

```python
from ca_runtime.sqlite_tuning import SQLiteBackgroundCheckpointer

with SQLiteBackgroundCheckpointer(db_path):
    # worker activity
    ...
```

## Test Command

```bash
python -m pytest tests/cae/test_ca_m056_sqlite_tuning.py -q
```

A syntax check was also executed with:

```bash
python -m py_compile packages/ca_runtime/src/ca_runtime/sqlite_tuning.py tests/cae/test_ca_m056_sqlite_tuning.py
```

## Expected Test Results

**11 automated tests, all passing.**

Observed verification in the sandbox:

```text
11 passed in 8.66s
```

`py_compile` returned exit code `0` for both files.

### Evidence and limitations

- **EXECUTABLE / TEST:** live SQLite PRAGMAs are queried after configuration; WAL persistence is checked after reopening the database.
- **EXECUTABLE / TEST:** the concurrency proof uses independent SQLite connections in separate threads so the sandbox exercises SQLite's actual connection locking semantics.
- **EXECUTABLE / TEST:** a separate Python process reopens the same database and verifies persisted WAL/busy-timeout/mmap/autocheckpoint policy.
- **NEGATIVE TEST:** an unrelated `threading.Lock` does not prevent another SQLite connection from receiving `database is locked`; this rejects the process-local-mutex false proof.
- **Environment limitation:** the sandbox's filesystem did not propagate SQLite write locks between OS subprocesses, so a process-to-process lock contention test was not used as the positive timing oracle. The implementation itself does not use a process-local lock as a substitute for SQLite locking.
- **Environment limitation:** the repository's normal `ca_runtime` package import currently requires `psycopg`, which is not installed in this sandbox. The mandate test therefore loads the new module directly so its SQLite behavior remains independently verifiable. This does not alter the repository package.
- The uploaded source archive contains no `.git` metadata, so there is no trustworthy source/repository commit SHA to report. **Commit SHA: unavailable in supplied archive; capture the post-apply repository commit SHA after integration.**

### Artifact hashes

- `packages/ca_runtime/src/ca_runtime/sqlite_tuning.py`: `329fdd53532bafb6ae5b1811647327582485a3e8283872d24f6938fbba2fb4ce`
- `tests/cae/test_ca_m056_sqlite_tuning.py`: `1625519f2e6d2695d2bc513dac49a8e21aa93f5ce8fbf057bf9dccf178075940`

**Operator decision required by the mandate:** APPROVE, REJECT with findings, or DEFER with named remediation.
