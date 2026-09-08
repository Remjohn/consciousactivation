# CA-M003 Agent Handoff

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/subject_constitution.py` | Added a bounded Subject Constitution lifecycle aggregate with signed immutable revisions, deep immutable fields, exception records, versioned amendment packets, operator authorization, stale-parent rejection, approval/rejection states, and tamper-evident amendment receipts. | `INV-SUB-001`: a signed baseline cannot be mutated in place; history is retained; only an explicitly authorized operator can promote an evidence-backed amendment into a new revision with parent lineage and a receipt. |
| `tests/cae/test_ca_m003_subject_constitution.py` | Added acceptance coverage for signed-baseline verification, top-level and nested mutation rejection, signature tampering, exception isolation, valid amendment creation, stale-parent rejection, unauthorized approval, missing evidence, operator identity mismatch, historical retention, duplicate approval rejection, and rejected-amendment behavior. | Positive and negative executable evidence for the CA-M003 lifecycle boundary, including fail-closed adversarial paths. |

## Exact paste instructions

From the root of the repository, replace/add exactly these paths from this bundle:

1. `CA-M003_BUNDLE/packages/ca_runtime/src/ca_runtime/subject_constitution.py` → `packages/ca_runtime/src/ca_runtime/subject_constitution.py`
2. `CA-M003_BUNDLE/tests/cae/test_ca_m003_subject_constitution.py` → `tests/cae/test_ca_m003_subject_constitution.py`

No other repository files are authorized or included in this bundle.

## Manual post-apply commands

No database migration, dependency installation, or generated-artifact step is required by this bounded implementation.

Run the supplied acceptance suite manually after applying the files:

```bash
pytest -q tests/cae/test_ca_m003_subject_constitution.py
```

The execution agent did **not** run tests, per instruction.

## Automated tests included

- `test_ca_m003_01_signed_baseline_is_cryptographically_verifiable_and_immutable`
- `test_ca_m003_02_tampering_with_signed_record_fails_verification`
- `test_ca_m003_03_exception_is_recorded_without_auto_mutating_baseline`
- `test_ca_m003_04_valid_operator_amendment_creates_new_version_and_receipt`
- `test_ca_m003_05_stale_parent_is_fail_closed`
- `test_ca_m003_06_missing_operator_authority_is_fail_closed`
- `test_ca_m003_07_amendment_requires_evidence`
- `test_ca_m003_08_approval_requires_packet_operator_identity`
- `test_ca_m003_09_history_is_preserved_and_direct_baseline_replacement_is_not_an_api`
- `test_ca_m003_10_approved_amendment_cannot_be_approved_twice`
- `test_ca_m003_11_rejected_amendment_leaves_signed_baseline_unchanged`

## Evidence and limitations

- **EXECUTABLE/static evidence:** both delivered Python files parse successfully via `py_compile` and AST parsing. The test suite was intentionally not executed.
- **TEST evidence:** acceptance tests are included but remain unexecuted in this agent run.
- **ARCHITECTURE boundary:** the supplied repository archive did not contain an existing `subject_constitution.py` implementation or `test_ca_m003_subject_constitution.py`, so both are new bounded artifacts at the mandate-specified paths.
- **Persistence limitation:** the current repository did not expose an existing Subject Constitution persistence schema/store at the authorized boundary. The lifecycle therefore keeps authoritative history and receipts in the lifecycle aggregate; a durable database projection would require an additional explicitly authorized persistence surface.
- **UI projection:** no UI file was changed because the mandate's explicit target surface was the runtime aggregate and its direct test, and the supplied archive did not provide an existing Subject Constitution UI projection to modify safely within scope.
- **Cryptographic model:** signatures use HMAC-SHA256 with a trusted runtime signing secret. Operator identity/authority is additionally checked against the amendment packet and the exact `SUBJECT_CONSTITUTION_AMEND` authority scope; possession of a signing secret alone does not satisfy the operator-identity check.
- **Commit SHA:** `NOT AVAILABLE — supplied source archive contains no .git metadata.`

## Operator decision required

Please explicitly approve or reject CA-M003 after reviewing the supplied evidence, with particular attention to whether the bounded lifecycle and amendment authority model are acceptable for the canonical Subject Constitution boundary.
