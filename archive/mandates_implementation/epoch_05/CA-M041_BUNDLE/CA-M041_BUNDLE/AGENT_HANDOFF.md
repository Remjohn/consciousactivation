# CA-M041 Agent Handoff

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/gate_resumption.py` | Added a bounded reactive gate-resumption coordinator with strict `AuthorityLane.COMMANDER` enforcement, immutable cryptographic approval receipts, operator approvals, Commander policy overrides, suspension freshness checks, ordered receipt persistence → `RESUME` event enqueue → lock release, asynchronous resolution waiting, retryable reactive dispatch, and append-only receipt persistence. | `INV-GATE-002`: a suspended gate cannot resume through an approval/override unless Commander authority and the exact suspension revision/snapshot are valid; the approval receipt is created and persisted before the suspension lock is released. |
| `tests/cae/test_ca_m041_gate_resumption.py` | Added 12 focused CA-M041 tests covering approval ordering, authority rejection, policy override, stale revision/hash failure, idempotency/conflict handling, receipt tamper detection, restart persistence, async waiting, resume-handler retry behavior, and policy-scope enforcement. | Executable proof suite for `INV-GATE-002` receipt-before-unlock, fail-closed authorization/freshness, reactive `RESUME`, and receipt integrity. |

## Exact paste instructions

This bundle adds two new files. Replace/create the following repository paths exactly:

1. `CA-M041_BUNDLE/packages/ca_runtime/src/ca_runtime/gate_resumption.py`
   → `packages/ca_runtime/src/ca_runtime/gate_resumption.py`

2. `CA-M041_BUNDLE/tests/cae/test_ca_m041_gate_resumption.py`
   → `tests/cae/test_ca_m041_gate_resumption.py`

No other repository files are part of this bundle.

The implementation intentionally does **not** modify `program_operator_runtime.py`, `program_state_runtime.py`, `api/routers/programs.py`, or database schemas. The CA-M041 module emits an authenticated `RESUME` event for the downstream state/lease runtime rather than duplicating CA-M042 CAS mechanics.

## Manual post-apply commands

No database migration is required by this bundle.

Per the execution instruction, the test suite was **not run**. Post-apply validation may be performed with:

```text
pytest tests/cae/test_ca_m041_gate_resumption.py
```

## Automated tests included

- `test_ca_m041_operator_approval_is_immutable_and_receipt_precedes_lock_release`
- `test_ca_m041_non_commander_cannot_resume_and_lock_remains_held`
- `test_ca_m041_policy_override_is_commander_bound_and_resumes_reactively`
- `test_ca_m041_stale_revision_fails_closed_without_receipt_or_unlock`
- `test_ca_m041_stale_snapshot_hash_fails_closed`
- `test_ca_m041_duplicate_identical_approval_is_idempotent_and_conflicting_approval_is_blocked`
- `test_ca_m041_receipt_tampering_is_detectable`
- `test_ca_m041_receipt_store_is_restart_durable_and_append_only`
- `test_ca_m041_async_waiter_observes_reactive_resolution`
- `test_ca_m041_resume_handler_failure_keeps_event_queued_for_retry`
- `test_ca_m041_rejects_non_resumption_policy_scope`
- `test_ca_m041_jsonl_store_rejects_tampered_persisted_receipt`

## Static validation performed

The two bundled Python files were parsed/compiled successfully with Python's AST/compiler checks. No pytest/test command was executed.

SHA-256:
- `packages/ca_runtime/src/ca_runtime/gate_resumption.py`: `81ca28a9ac939c2812086d7695b4eb1ce4255b827440d52b4336250ac12fbe38`
- `tests/cae/test_ca_m041_gate_resumption.py`: `37a2eb4cd2610716c57cec8af79c9aedb508a076dff45124d2057fdc9d257a4a`

## Operator handoff

CA-M041 implementation is bounded to the requested two target paths. Formal Operator sign-off remains required before promoting the reactive resume contract and proceeding to subsequent CAS/ledger work.
