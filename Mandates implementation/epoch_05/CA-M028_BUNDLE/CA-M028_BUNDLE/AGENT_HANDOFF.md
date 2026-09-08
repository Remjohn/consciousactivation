# CA-M028 AGENT HANDOFF — Policy Revisions Execution Binding (Q27 / FR-POL-002 / INV-POL-001)

## 1. Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/policy_revision_binding.py` | **NEW** — PolicyRevisionBinding record, immutable registry, bind-at-lease/dispatch APIs, payload attachment helpers, drift/stale detection, fail-closed abort of in-flight executions, contrastive bound-vs-prospective audit helper | Active executions remain bound to the exact policy revision digest under which they were authorized; later campaign policy changes are prospective only; drift or stale snapshots abort the lease/dispatch path |
| `tests/wave04/test_ca_m028_policy_revision_binding.py` | **NEW** — Positive bind + payload attachment; prospective Pn → Pn+1 contrast (active stays on Pn, new binds Pn+1); rebind rejection; missing/stale package fail-closed; forced-drift abort; restart recovery via dict rehydration; status/history audit | Executable + TEST evidence for INV-POL-001 / FR-POL-002; contrastive false-proof that live campaign policy is not used for in-flight authorization |

No existing shared registry, migration, program_manifest schema, or program_state_runtime lease implementation was mutated. The binding module is a sibling of `policy_package.py` and is designed to be called from lease acquisition / dispatch creation paths without requiring those files to change in this mandate.

## 2. Exact paste instructions

Copy/replace into the repository root as follows (paths relative to repo root):

```
packages/ca_runtime/src/ca_runtime/policy_revision_binding.py
  ← CA-M028_BUNDLE/packages/ca_runtime/src/ca_runtime/policy_revision_binding.py

tests/wave04/test_ca_m028_policy_revision_binding.py
  ← CA-M028_BUNDLE/tests/wave04/test_ca_m028_policy_revision_binding.py
  (create `tests/wave04/` if absent)
```

Do **not** modify:
- `packages/ca_runtime/src/ca_runtime/policy_package.py`
- `packages/ca_runtime/src/ca_runtime/program_registry.py`
- `packages/ca_runtime/src/ca_runtime/program_state_runtime.py`
- `packages/ca_runtime/src/ca_runtime/program_operator_runtime.py`
- Any shared migration, receipt, or historical policy package

Optional integration (out of scope for this mandate, for a later owner):
- Call `bind_policy_revision_to_execution` / `attach_binding_to_lease_payload` inside `acquire_execution_lease` / dispatch registration.
- Call `require_live_binding` or `detect_and_abort_on_drift` at authorization / gate evaluation points.

## 3. Manual post-apply commands

None required. No schema migrations, database changes, or package installs beyond the existing `ca_runtime` / `ca_contracts` dependency graph.

Suggested verification (do **not** treat a green suite as Operator approval):

```bash
# From repository root, with the ca_runtime package on PYTHONPATH
python -m pytest tests/wave04/test_ca_m028_policy_revision_binding.py -v
```

## 4. Names of new automated tests included in the bundle

File: `tests/wave04/test_ca_m028_policy_revision_binding.py`

- `test_bind_policy_revision_to_execution_positive`
- `test_bind_loaded_package_direct`
- `test_attach_binding_to_lease_and_dispatch_payloads`
- `test_prospective_update_active_stays_on_pn_new_binds_pn1`  ← core INV-POL-001 contrast
- `test_rebind_active_execution_rejected`
- `test_bind_unknown_package_fails_closed`
- `test_resolve_bound_package_missing_after_bind`
- `test_detect_and_abort_on_forced_digest_mismatch`
- `test_check_integrity_raises_on_aborted`
- `test_binding_not_found`
- `test_binding_survives_registry_reload_from_dict`
- `test_complete_binding`
- `test_list_bindings_filter`
- `test_binding_to_dict_schema_identity`
- `test_binding_digest_for_payload_stable`
- `test_history_records_status_transitions`
- `test_integrity_ok_when_prospective_matches_bound`
- `test_require_live_rejects_completed`

## 5. Residual limitations / control-state notes

- The binding registry is process-scoped (same pattern as `PolicyPackageRegistry`). Durable persistence across process restarts is demonstrated via `to_dict` / `from_dict` rehydration; a production durable store is an integration concern outside this mandate’s file boundary.
- Lease and dispatch payload attachment is provided as pure functions; wiring into `program_state_runtime.acquire_execution_lease` is intentionally left to a follow-on integration owner so that this mandate remains bounded to the authorized surfaces.
- Historical policy packages must remain addressable; if retention deletes a revision while an active binding still references it, the runtime fails closed with `STALE_POLICY_SNAPSHOT` (as proven by the missing-after-bind test). No archival mechanism was invented.

## 6. Operator decision request

Approve or reject **CA-M028** based on whether the executable evidence proves the ratified Q27 contract at the canonical authority boundary: active executions remain bound to the exact authorization policy revision under which they were authorized; later campaign policy changes are prospective only; drift/stale snapshots abort in-flight executions.
