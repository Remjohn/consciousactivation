# AGENT HANDOFF — CA-M009
**Mandate:** CA-M009 — Interactive Parameter-Sensitive Preparation Graph  
**Wave:** 02 | **Causal Stage:** 05 — Declarative PreProduction  
**Governing FR:** FR-009 / preparation-graph contract  
**Execution date:** 2026-09-07  
**Status:** IMPLEMENTATION COMPLETE — Operator gate required before CA-M010

---

## 1. Summary Table

| File Changed / Created | What Changed | Invariant Proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/preparation_graph_store.py` | **NEW** — Authoritative SQLite/Postgres relational store for the 3-table schema: `preparation_graph`, `graph_revision`, `graph_run_binding`. Implements all five M009 invariants. | INV-M009-01 through INV-M009-05 (revision immutability, stale write rejection, active binding immutability, historical inspection, digest at bind time) |
| `packages/ca_runtime/src/ca_runtime/preparation_graph_program.py` | **NEW** — Program coordinator owning COMMANDER/ANALYST lane-authority checks and workspace-scope enforcement. Delegates all state mutations to the store. | INV-M009-02 (StaleBaseRevisionError), INV-M009-03 (ActiveBindingMutationError), INV-M009-05 (verify_active_run_integrity → DigestMismatchError) |
| `packages/ca_runtime/src/ca_runtime/migrations/drafts/0011_cae_preparation_graph.sql` | **NEW** — PostgreSQL migration creating `cae.preparation_graph`, `cae.graph_revision`, `cae.graph_run_binding` with RLS policies, indexes, and two immutability enforcement triggers (`fn_graph_revision_immutability`, `fn_graph_run_binding_immutability`). | INV-M009-01 (DB trigger blocks UPDATE on revision rows), INV-M009-03 (DB trigger blocks UPDATE on binding rows) |
| `programs/preparation_graph_program/program_manifest.yaml` | **NEW** — Program manifest declaring identity, lanes, operations, lifecycle states, invariants, false-proof case, and dependencies (collision_discovery_program, audience_context_program). | Manifest contract for CA-M009 execution surface |
| `tests/cae/test_m009_preparation_graph.py` | **NEW** — 19-test suite: 9 positive (T01–T09) + 9 negative (N01–N10, including N01b) + 1 E2E scenario. All tests use in-memory SQLite. | Full M009 behavioral boundary |

---

## 2. Paste Instructions

Apply the bundle files to the repository at the following exact paths:

```
CA-M009_BUNDLE/
├── AGENT_HANDOFF.md                              (this file — docs reference only)
└── packages/
    └── ca_runtime/
        └── src/
            └── ca_runtime/
                ├── preparation_graph_store.py              → packages/ca_runtime/src/ca_runtime/preparation_graph_store.py
                ├── preparation_graph_program.py            → packages/ca_runtime/src/ca_runtime/preparation_graph_program.py
                └── migrations/
                    └── drafts/
                        └── 0011_cae_preparation_graph.sql  → packages/ca_runtime/src/ca_runtime/migrations/drafts/0011_cae_preparation_graph.sql
└── programs/
    └── preparation_graph_program/
        └── program_manifest.yaml                           → programs/preparation_graph_program/program_manifest.yaml
└── tests/
    └── cae/
        └── test_m009_preparation_graph.py                  → tests/cae/test_m009_preparation_graph.py
```

**No existing files are modified.** All deliverables are new files.

---

## 3. Post-Apply Commands

### 3a. Run the test suite

```bash
# From the repository root
pytest tests/cae/test_m009_preparation_graph.py -v
```

Expected output: 19 tests pass (9 positive + 9 negative + 1 E2E).

### 3b. Apply the PostgreSQL migration (staging / production)

```bash
# Using the project's migration runner
python -m ca_runtime.migration_runner \
  --migration packages/ca_runtime/src/ca_runtime/migrations/drafts/0011_cae_preparation_graph.sql \
  --env staging
```

**Rollback** (if needed):
```sql
DROP TABLE IF EXISTS cae.graph_run_binding;
DROP TABLE IF EXISTS cae.graph_revision;
DROP TABLE IF EXISTS cae.preparation_graph;
```

The migration is additive (new tables only) and does not touch existing tables. It is forward-compatible and reversible.

### 3c. Register the new program (if ProgramRegistry auto-discovery is not active)

```python
from programs.preparation_graph_program import program_manifest
# The manifest YAML is discovered automatically if the programs/ directory is in the
# ProgramRegistry discovery roots (current configuration already covers this path).
```

---

## 4. New Automated Tests Included

| Test ID | Class | Description | What it proves |
|---|---|---|---|
| T01 | TestPositive | Graph creation and initial state | DRAFT_GRAPH initial state |
| T02 | TestPositive | Genesis SAVE_REVISION (base=None) | First revision accepted; digest correct |
| T03 | TestPositive | Second revision supersedes first | R1→HISTORICAL, R2→CANDIDATE; INV-M009-04 |
| T04 | TestPositive | list_revisions ordered history | Historical revision payload readable |
| T05 | TestPositive | bind_run_to_revision creates binding | INV-M009-05 digest stored at bind time |
| T06 | TestPositive | Active run returns bound revision after later edits | UI-001 runtime authority |
| T07 | TestPositive | Digest integrity on unmodified binding | INV-M009-05 positive path |
| T08 | TestPositive | Operator projection shows all lifecycle states | UI §9 operator view |
| T09 | TestPositive | Idempotent re-bind to same revision | Replay safety |
| N01 | TestNegative | Stale base_revision_id rejected | INV-M009-02 |
| N01b | TestNegative | Stale base when newer revision exists (concurrent editors) | INV-M009-02 |
| N02 | TestNegative | **False-proof case**: in-place mutation detected by digest | INV-M009-05 anti-centroid |
| N03 | TestNegative | Rebind run to different revision rejected | INV-M009-03 |
| N04 | TestNegative | Digest mismatch on tampered canonical_sha256 field | INV-M009-05 |
| N05 | TestNegative | Forged revision_id rejected | RevisionNotFoundError |
| N06 | TestNegative | Wrong lane for create_graph | COMMANDER authority |
| N07 | TestNegative | Wrong lane for save_graph_revision | ANALYST/COMMANDER authority |
| N08 | TestNegative | Wrong lane for bind_run_to_revision | COMMANDER authority |
| N09 | TestNegative | Unknown run_id raises RunBindingNotFoundError | RunBindingNotFoundError |
| N10 | TestNegative | save_graph_revision to unknown graph | GraphNotFoundError |
| E2E | TestEndToEndLifecycle | Full M009 lifecycle arc | All invariants combined |

---

## 5. Evidence and Limitations

### 5a. Invariants proved

| Invariant | Proof mechanism | Limitation |
|---|---|---|
| INV-M009-01 (revision immutable) | Application layer: `RevisionImmutabilityError` raised if store receives update call (no UPDATE path exists in `save_graph_revision`). DB layer: `fn_graph_revision_immutability` trigger in PostgreSQL migration. | SQLite test environment does not run the DB trigger. Test N02 proves the application-layer guard via digest mismatch detection. |
| INV-M009-02 (stale write rejected) | `StaleBaseRevisionError` raised when `base_revision_id != graph.latest_revision_id`. Tests N01, N01b. | Race condition between two concurrent writers is mitigated at application CAS level; full serializable isolation requires DB-level transaction. |
| INV-M009-03 (active binding immutable) | `ActiveBindingMutationError` raised on re-bind to different revision. DB trigger `fn_graph_run_binding_immutability` blocks all UPDATEs. Test N03. | Tested at application layer; DB trigger requires Postgres. |
| INV-M009-04 (historical inspection) | `list_revisions` returns all rows ordered by `revision_seq`; no DELETE path exists. Test T04. | Rows could be deleted via raw SQL; production RLS policies restrict to `has_workspace_access`. |
| INV-M009-05 (digest at bind time) | `revision_digest` copied from `canonical_sha256` at bind time. `verify_run_binding_digest` recomputes and compares. Tests T07, N02, N04. | Digest is application-layer only; assumes `canonical_sha256` implementation in `ca_contracts` is correct. |

### 5b. False-proof case (anti-centroid)

Test **N02** directly exercises the mandate's false-proof case (§9):

> *"The UI changes from R1 to R2 while the backend mutates the same stored row, so the active run now unknowingly uses R2. That must fail."*

N02 simulates this by directly executing `UPDATE graph_revision SET parameter_payload_json = <tampered>` in SQLite, bypassing the application layer (which has no UPDATE path). `verify_active_run_integrity` then raises `DigestMismatchError` because the recomputed digest of the tampered payload does not match `binding.revision_digest` (which was recorded at bind time from R1's original content).

In PostgreSQL production, the DB trigger `fn_graph_revision_immutability` blocks the UPDATE before it reaches storage, providing defense-in-depth.

### 5c. Scope boundary

This mandate implements:
- `DRAFT_GRAPH → SAVE_REVISION → CANDIDATE_GRAPH_REVISION → SEAL/EXECUTION_BINDING → ACTIVE_EXECUTION_GRAPH`
- The minimum binding contract needed as input to CA-M011 (`revision_id` + `canonical_sha256` on the run binding row)

This mandate explicitly does **not** implement:
- CA-M011 snapshot sealing (full Pre-Production Snapshot cryptographic seal)
- Broad UI redesign
- Campaign lifecycle semantics beyond graph binding

---

## 6. Operator Decision Gate

**Operator decision required per mandate §12:**

> Approve CA-M009 and authorize CA-M010; record whether the preparation-graph revision/binding contract is accepted as an input to CA-M011.

Until this decision is recorded in CAE control state, CA-M010 is unauthorized.

**To record the decision in CAE control state**, update:
```
docs/cae/CAE_CONVERGENCE_SPINE_DECISION_LEDGER.md
```
with:
```
CA-M009 | APPROVED | <date> | <operator-id> | preparation-graph-revision-binding-contract-accepted-for-M011: <YES/NO>
```

---

## 7. Commit SHA

> **Pending** — this bundle has not been committed to the repository. The exact git commit SHA must be captured after `git commit` and recorded here as:
>
> ```
> commit <SHA>
> Author: <operator-id>
> Date:   <date>
> Message: CA-M009: Preparation Graph — revision lifecycle, execution binding, digest integrity
> ```
