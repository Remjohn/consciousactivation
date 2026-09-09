# CA-M007 Bundle Handoff

## 1. Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/strategic_execution.py` | Added the bounded Strategic Execution object, exact Guest Genesis / Audience Tensions / Convergence Receipt ancestry binding, signed operator intent contract, raw-topic rejection, cross-workspace checks, stale-lineage checks, deterministic payload digest, and fail-closed downstream admission helper. | `FR-007 / INV-ACT-001`: strategic execution is admitted only as a derived object with complete upstream lineage and valid signed operator intent; arbitrary raw topic insertion is rejected. |
| `tests/cae/test_ca_m007_strategic_execution.py` | Added positive, negative, integrity, stale-lineage, workspace-boundary, and downstream admission coverage for CA-M007. | Executable evidence covers the admission predicate and the fail-closed failure modes rather than only object construction. |

## 2. Exact paste instructions

Replace/add exactly these repository paths from the bundle:

1. Replace `packages/ca_runtime/src/ca_runtime/strategic_execution.py` with the bundled `CA-M007_BUNDLE/packages/ca_runtime/src/ca_runtime/strategic_execution.py`.
2. Replace/add `tests/cae/test_ca_m007_strategic_execution.py` with the bundled `CA-M007_BUNDLE/tests/cae/test_ca_m007_strategic_execution.py`.

No other repository paths are authorized or changed by this bundle.

## 3. Manual post-apply commands

No database migration or data migration is required; the implementation is an in-memory/content-addressed runtime object and does not introduce persistence schema changes.

Per the execution instruction, **tests were not run**.

Recommended verification after paste (operator-run, not executed here):

```text
python -m pytest tests/cae/test_ca_m007_strategic_execution.py
```

## 4. New automated tests included

- `test_ca_m007_valid_derivation_contains_full_upstream_ancestry`
- `test_ca_m007_exact_parent_revisions_and_digests_are_persisted_in_object`
- `test_ca_m007_unsigned_operator_intent_cannot_be_instantiated`
- `test_ca_m007_tampered_operator_intent_signature_is_rejected`
- `test_ca_m007_operator_intent_must_target_exact_execution_object`
- `test_ca_m007_raw_topic_insertion_is_explicitly_rejected`
- `test_ca_m007_missing_genesis_is_fail_closed`
- `test_ca_m007_missing_tensions_is_fail_closed`
- `test_ca_m007_missing_convergence_receipt_is_fail_closed`
- `test_ca_m007_non_converged_receipt_is_not_an_admission_token`
- `test_ca_m007_stale_genesis_digest_is_rejected`
- `test_ca_m007_stale_tensions_revision_is_rejected`
- `test_ca_m007_cross_workspace_lineage_is_rejected`
- `test_ca_m007_downstream_admission_reverifies_full_ancestry`
- `test_ca_m007_payload_digest_detects_mutation`
- `test_ca_m007_payload_serialization_exposes_complete_lineage_and_intent`

## 5. Evidence / limitations

Evidence class: `EXECUTABLE` for the implementation and test definitions in the two files above.

The implementation deliberately reuses the existing `ConvergenceReceipt` contract as the authoritative upstream convergence token; it does not create a parallel convergence authority.

The repository's current signature convention is deterministic SHA-256 content addressing. CA-M007 therefore treats the operator-intent signature as a deterministic, tamper-evident signature of the canonical intent fields. This proves integrity and binding within the repository's existing convention, but it is not a public-key signature scheme.

Tests were intentionally not executed. No commit SHA was available in the supplied working snapshot, so no commit SHA is claimed here.

Operator decision required: approve or reject CA-M007 based on the bundled implementation and subsequent operator-run verification.
