# CA-M047 — Multi-Tenant Workspace Isolation

## Mandate ID & Title

**Mandate ID:** CA-M047  
**Mandate Title:** Multi-Tenant Workspace Isolation  
**Task-specified invariant:** INV-ISO-001  
**Repository Q46 invariant label:** INV-TEN-001 in `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_06/07_CA_MANDATE_047.md`

The uploaded repository mandate and the task metadata use different invariant labels. This bundle implements the task-specified `INV-ISO-001` requirement while preserving the repository's existing `INV-TEN-001` terminology; no unrelated rename was made.

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/workspace_isolation.py` | Added fail-closed workspace/campaign authority binding, composite-scope SQLite state store, canonical workspace/campaign-bound SHA-256 identity, partitioned filesystem roots, traversal/absolute-path rejection, symlink-alias rejection, and scoped CAS/read/write/delete/list operations. | Authenticated workspace identity cannot be substituted; database reads/writes require `(workspace_id, campaign_id, aggregate_id)`; otherwise-identical states hash differently across tenants/campaigns; storage cannot resolve outside its tenant/campaign root. |
| `tests/cae/test_ca_m047_workspace_isolation.py` | Added 39 self-contained tests covering authorization, cryptographic identity separation, SQLite isolation/CAS, cross-tenant and cross-campaign access, filesystem partitioning, traversal/absolute paths, symlink aliases, overwrite protection, and the false-proof countercase. | Executable proof of fail-closed cross-workspace/campaign access and state separation. |

## Files Added and Files Modified

### Files Added

`packages/ca_runtime/src/ca_runtime/workspace_isolation.py`

Rationale: the requested target file did not exist in the uploaded repository archive. It is the bounded implementation artifact for workspace/campaign isolation and is intentionally self-contained so the security primitives do not depend on unrelated application imports.

`tests/cae/test_ca_m047_workspace_isolation.py`

Rationale: the requested CA-M047 proof file did not exist in the uploaded repository archive. It provides the mandate-specific executable security matrix.

### Files Modified

None.

No existing repository files were edited.

## Exact paste instructions and post-apply commands

From the repository root, place the two files at these exact destinations, preserving their complete contents:

```text
packages/ca_runtime/src/ca_runtime/workspace_isolation.py
tests/cae/test_ca_m047_workspace_isolation.py
```

No database migration is required by this bundle. The implementation creates its own scoped SQLite table when `WorkspaceIsolatedDatabase` is instantiated; it does not alter the pre-existing program-state schema, API router, authentication middleware, or historical records.

Post-apply verification:

```bash
python -m py_compile   packages/ca_runtime/src/ca_runtime/workspace_isolation.py   tests/cae/test_ca_m047_workspace_isolation.py

PYTHONPATH=packages/ca_runtime/src:packages/ca_contracts/src python -m pytest -q tests/cae/test_ca_m047_workspace_isolation.py
```

The test module intentionally loads the target module directly so this mandate proof remains runnable in the supplied sandbox even though the uploaded environment does not include the optional `psycopg` runtime dependency imported by `ca_runtime/__init__.py`.

## Test Command

```bash
PYTHONPATH=packages/ca_runtime/src:packages/ca_contracts/src python -m pytest -q tests/cae/test_ca_m047_workspace_isolation.py
```

## Expected Test Results

**39 automated tests, all passing.**

Sandbox result:

```text
.......................................                                  [100%]
39 passed in 0.14s
```

The suite proves:
- missing and mismatched workspace authority fail closed;
- campaign substitution fails closed;
- identical payloads produce different digests across workspaces and campaigns;
- the authoritative SQLite primary key is `(workspace_id, campaign_id, aggregate_id)`;
- the same aggregate ID can coexist safely in distinct workspaces/campaigns;
- cross-workspace reads and writes cannot expose or mutate another scope;
- stale CAS versions do not commit;
- workspace/campaign filesystem roots are distinct;
- traversal and absolute paths are rejected;
- cross-workspace and cross-campaign symlink aliases are rejected;
- repeated state-file writes cannot overwrite existing state;
- no aggregate-only public database accessor is exposed as a false-proof guard.

## Evidence and limitations

**Evidence classes:** `EXECUTABLE` and `TEST`.

**Observed repository facts:** the uploaded CA-M047/Q46 document requires API, database, storage, and applicable cryptographic boundary fencing; the requested target files were absent from the archive; existing `tenancy.py` contains authenticated tenant-context primitives; the existing `program_state_runtime.py` SQLite implementation uses aggregate-only predicates in several methods.

**Scope limitation:** because the user-specified implementation boundary was `workspace_isolation.py` plus its CA-M047 tests, this bundle adds the isolation boundary as a reusable subsystem but does not rewrite `api/routers/programs.py` or `program_state_runtime.py`. Direct integration of those existing call paths would require additional in-scope repository edits beyond the exact two target paths supplied for this execution.

**Commit SHA:** unavailable. The uploaded archive contains no `.git` metadata, so no repository commit SHA can be truthfully reported.

**Operator decision requested by the source mandate:** approve or reject CA-M047 after applying the bounded isolation layer and reviewing the residual integration limitation above.
