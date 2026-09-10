# Mandate ID & Title

**Mandate ID:** CAE-M059  
**Mandate Title:** Campaign Execution Control Surface  
**Requirement / Invariant:** FR-OPS-CONTROL  
**Status:** IMPLEMENTED — MANDATE VERIFICATION PASS — OPERATOR GATE PENDING  
**Upstream baseline commit:** `e8696a23b867c336636f14496f8174f3771c77af` (`main`)  
**Implementation commit:** Not created or pushed by this execution agent; bundle is the apply-ready patch against the captured upstream baseline.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` | Added typed execution receipt/failure projections; persisted pause/resume/abort control receipts through the canonical CAS lifecycle path; added receipt and failure retrieval methods; preserved Commander authority and lifecycle preconditions. | `FR-OPS-CONTROL`: execution control is performed through the existing Program runtime/state authority, with durable evidence and no second state machine. |
| `api/routers/programs.py` | Added explicit receipt-list, receipt-by-ID, and failure read endpoints for execution aggregates; existing launch/status/pause/resume routes remain backed by the operator runtime service. | Product control surface exposes launch, inspect, pause/resume, failure, and receipt evidence without direct persistence mutation. |
| `api/routers/campaigns.py` | Added a read-only campaign control projection exposing canonical lifecycle, version/checkpoint, capabilities, refs, authority/operator metadata, and failure indicators. Campaign launch is not falsely duplicated because creation already commits the canonical `LAUNCHED` lifecycle. | Campaign control state is surfaced without inventing an unauthorized launch/pause/resume transition. |
| `tests/mandates/test_cae_m059_control_surface.py` | Added six mandate-specific integration/unit tests covering launch/inspect, pause/resume, authority rejection, failure projection, durable receipt reload, API routes, and the false-proof countercase. | The verifier checks persisted runtime state and receipts rather than UI/result-only claims. |

## Files Added and Files Modified

### Added

- `tests/mandates/test_cae_m059_control_surface.py` — self-contained M059 verification suite exercising the scoped runtime and API boundary, including the required false-proof countercase.

### Modified

- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py` — adds the typed control evidence/read surface and records lifecycle-control receipts through the canonical state CAS mutation.
- `api/routers/programs.py` — exposes receipt and failure retrieval paths as read-only product endpoints while retaining existing typed launch/control endpoints.
- `api/routers/campaigns.py` — exposes a read-only campaign control projection and explicitly reports unsupported duplicate control operations rather than fabricating them.

No migration was added and no unrelated repository file is part of this bundle.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. Extract the bundle and copy its contents into the repository root, preserving paths exactly:

```bash
unzip -o CAE-M059_BUNDLE.zip
rsync -a CAE-M059_BUNDLE/ /path/to/consciousactivation/
```

2. No database migration is required by M059. The new control receipts are persisted in the existing Program aggregate `state_data`; the campaign control endpoint is read-only.

3. Install/use the repository's normal Python environment and run the mandate verification command from the repository root:

```bash
pytest -q tests/mandates/test_cae_m059_control_surface.py
```

4. For the sandbox verification used to isolate missing optional repository dependencies, the exact successful command was:

```bash
PYTHONPATH=/tmp/m059_psycopg_stub:/mnt/data/cae_repo:/mnt/data/cae_repo/packages/ca_contracts/src:/mnt/data/cae_repo/packages/ca_runtime/src pytest -q tests/mandates/test_cae_m059_control_surface.py
```

5. Existing broader API collection in the supplied snapshot is environment-blocked by optional packages not present in the bundle (including `cmf_vae`/related non-scoped imports). This limitation does not affect the six M059 tests, which include their own FastAPI route-level integration coverage for the new endpoints.

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/mandates/test_cae_m059_control_surface.py
```

## Expected Test Results (number of automated tests, all passing)

**6 automated M059 tests — all passing.**  
Sandbox result: `6 passed in 0.65s` (after successful `py_compile` of all four scoped source/test files).

### Evidence and limitations

- **Verifier actually measures:** canonical Program aggregate lifecycle/version/state hash changes; persisted operator control receipts; durable SQLite reload of those receipts; Commander-only mutation enforcement; terminal-state resume rejection; API response bodies backed by the same service; campaign projection read-only behavior; and a false-proof countercase where a missing receipt is treated as failure rather than success.
- **Verifier does not measure:** a production worker fleet, external workflow queue throughput, browser UI rendering, or external provider/service availability. Those require a deployed environment and remain outside M059's bounded code/test scope.
- **False-proof countercase:** the tests remove/omit a required receipt and assert the receipt query cannot report it as present; they also verify that a terminal FAILED execution cannot be resumed merely because an API route exists.
- **Environment fidelity:** runtime/state persistence and FastAPI routing are exercised against the repository code with an in-memory/durable SQLite fixture path. Optional production-only packages absent from the supplied snapshot prevented complete collection of unrelated API suites; those failures were not converted into passes.
- **Operator validation required:** yes. The mandate explicitly ends at the operator gate. No M0061 work was started.

### Control-state record

`CAE-M059 → IMPLEMENTED / VERIFICATION PASS / LIMITATION RECORDED / OPERATOR DECISION REQUIRED`  
Required next decision from the mandate: **Do you accept M0059 and authorize M0061?**

### Rollback / recovery

Rollback consists only of reverting the three modified control-path source files and removing the added mandate test. Persisted failed/control receipts are not deleted as part of rollback.
