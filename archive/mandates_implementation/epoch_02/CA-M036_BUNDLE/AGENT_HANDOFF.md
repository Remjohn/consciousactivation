# AGENT HANDOFF — CA-M036 (Real State-Local Context Projection / INV-CTX-002)

**Mandate ID:** `CA-M036`  
**Wave:** 05  
**Canonical Question:** Q36 (Spine Q03)  
**Invariant:** `INV-CTX-002`  
**Status:** IMPLEMENTATION COMPLETE — awaiting Operator approve/reject  

---

## 1. Summary Table

| File Changed / Created | What Changed | Invariant Proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/program_state_runtime.py` | Added `ContextProjectionError`, `NodeDeclarationMissingError`, `ContextStateHashParityError` exception types; added `PrunedContextSnapshot` dataclass; added `_LANE_FIELD_ALLOW_LISTS` dict; added `_verify_state_hash_parity()` and `_compute_pruned_snapshot_hash()` helpers; added `get_pruned_local_context()` method to `UniversalProgramStateRuntime`. Existing `get_local_context()` is unchanged (governance surface). | INV-CTX-002 pruning, lane masking, state_hash parity — all three enforced at the authoritative runtime boundary |
| `services/pipeline/src/cmf_pipeline/adapters/jit_context_budget.py` | **NEW FILE** — pipeline-layer adapter: `compile_jit_context_snapshot()`, `get_jit_context_snapshot()`, `PrunedContextSnapshot` (re-export), `LANE_FIELD_ALLOW_LISTS`, typed errors (`ContextBudgetError`, `MissingNodeDeclarationError`, `StateHashParityError`) | Same INV-CTX-002 contract, usable from pipeline service code without importing ca_runtime directly |
| `services/pipeline/src/cmf_pipeline/adapters/__init__.py` | Added re-exports for all new jit_context_budget symbols | Public adapter surface remains coherent |
| `tests/wave05/__init__.py` | **NEW FILE** — wave05 test package marker | — |
| `tests/wave05/_support.py` | **NEW FILE** — sys.path bootstrap (mirrors phase3/_support.py pattern) | — |
| `tests/wave05/test_ca_m036_context_projection.py` | **NEW FILE** — 25 acceptance / unit / regression tests for CA-M036 | Positive path, negative/fail-closed path, regression, false-proof countercase, lane structural integrity |

---

## 2. Paste Instructions

Replace the following files in your repository with the files from this bundle:

```
BUNDLE PATH                                                          → REPO PATH
---------------------------------------------------------------------  -------
CA-M036_BUNDLE/packages/ca_runtime/src/ca_runtime/
  program_state_runtime.py                                          → packages/ca_runtime/src/ca_runtime/program_state_runtime.py

CA-M036_BUNDLE/services/pipeline/src/cmf_pipeline/adapters/
  jit_context_budget.py                                            → services/pipeline/src/cmf_pipeline/adapters/jit_context_budget.py (NEW)
  __init__.py                                                       → services/pipeline/src/cmf_pipeline/adapters/__init__.py

CA-M036_BUNDLE/tests/wave05/
  __init__.py                                                       → tests/wave05/__init__.py (NEW DIR)
  _support.py                                                       → tests/wave05/_support.py (NEW)
  test_ca_m036_context_projection.py                               → tests/wave05/test_ca_m036_context_projection.py (NEW)
```

For `program_state_runtime.py`, this is a full-file replacement.  
For all other files, create new files or replace in-place.

---

## 3. Post-Apply Commands

No database migrations required (the new code is purely Python).  
No npm scripts required.

**Run tests (do not run in sandbox — per mandate instruction):**

```bash
# From repository root
python -m pytest tests/wave05/test_ca_m036_context_projection.py -v

# Regression check — verify existing tests remain green
python -m pytest tests/phase3/ tests/phase4/ -v --tb=short
```

**Verify the authoritative boundary is exercised (sanity check):**

```bash
python -c "
from ca_runtime.program_state_runtime import UniversalProgramStateRuntime, InMemoryProgramStateStore
from ca_runtime.pi_adapter import AuthorityLane
rt = UniversalProgramStateRuntime(store=InMemoryProgramStateStore())
agg = rt.initialize_program_state(
    program_id='research_source_ingestion_program',
    workspace_id='ws-test-001',
    actor_id='usr_sanity',
    initial_data={'hypothesis': 'test', 'script_draft': 'secret'},
)
snap = rt.get_pruned_local_context(
    agg.aggregate_id,
    node_id='sanity_node',
    declared_inputs=['hypothesis', 'script_draft'],
    active_lane=AuthorityLane.HUNTER,
)
assert 'hypothesis' in snap.pruned_state_data
assert 'script_draft' not in snap.pruned_state_data
assert snap.committed_state_hash == agg.state_hash
print('CA-M036 sanity check PASSED')
"
```

---

## 4. New Automated Tests Included

File: `tests/wave05/test_ca_m036_context_projection.py`

| Test ID | Class | Kind | Coverage |
|---|---|---|---|
| `test_positive_path_hunter_sees_declared_allowed_fields` | TestRuntimeGetPrunedLocalContext | POSITIVE | Pruning + HUNTER lane masking + hash binding |
| `test_positive_path_analyst_sees_declared_analyst_fields` | TestRuntimeGetPrunedLocalContext | POSITIVE | ANALYST lane masking |
| `test_positive_path_commander_sees_governance_fields` | TestRuntimeGetPrunedLocalContext | POSITIVE | COMMANDER lane masking |
| `test_positive_path_snapshot_hash_is_deterministic` | TestRuntimeGetPrunedLocalContext | POSITIVE | Deterministic snapshot_hash |
| `test_positive_path_snapshot_hash_differs_for_different_node_id` | TestRuntimeGetPrunedLocalContext | POSITIVE | Audit isolation by node_id |
| `test_positive_path_committed_state_hash_matches_aggregate` | TestRuntimeGetPrunedLocalContext | POSITIVE | committed_state_hash == aggregate.state_hash |
| `test_negative_path_empty_declared_inputs_raises` | TestRuntimeGetPrunedLocalContext | NEGATIVE | NodeDeclarationMissingError fail-closed |
| `test_negative_path_none_declared_inputs_raises` | TestRuntimeGetPrunedLocalContext | NEGATIVE | NodeDeclarationMissingError fail-closed (None) |
| `test_negative_path_state_hash_parity_failure_raises` | TestRuntimeGetPrunedLocalContext | NEGATIVE | ContextStateHashParityError on tampered hash |
| `test_negative_path_unauthorized_field_not_leaked` | TestRuntimeGetPrunedLocalContext | NEGATIVE | Cross-lane leakage prevention |
| `test_negative_path_all_declared_keys_masked_yields_empty_data` | TestRuntimeGetPrunedLocalContext | NEGATIVE | All-masked yields empty pruned_state_data |
| `test_regression_get_local_context_still_works` | TestRuntimeGetPrunedLocalContext | REGRESSION | Existing get_local_context unaffected |
| `test_regression_execute_transition_unaffected` | TestRuntimeGetPrunedLocalContext | REGRESSION | execute_transition unaffected |
| `test_false_proof_countercase_simple_key_filter_is_not_enough` | TestRuntimeGetPrunedLocalContext | FALSE-PROOF | Hash check required, not just key filtering |
| `test_positive_path_basic_compile` | TestCompileJitContextSnapshot | POSITIVE | Pipeline adapter compile |
| `test_positive_path_composer_lane` | TestCompileJitContextSnapshot | POSITIVE | COMPOSER lane |
| `test_negative_path_empty_declared_inputs_raises` | TestCompileJitContextSnapshot | NEGATIVE | Adapter fail-closed |
| `test_negative_path_tampered_hash_raises` | TestCompileJitContextSnapshot | NEGATIVE | Adapter hash parity |
| `test_negative_path_cross_lane_leakage_is_blocked` | TestCompileJitContextSnapshot | NEGATIVE | ANALYST cannot obtain COMMANDER field |
| `test_positive_integration_with_runtime` | TestGetJitContextSnapshot | POSITIVE | Runtime-integrated adapter |
| `test_negative_aggregate_not_found` | TestGetJitContextSnapshot | NEGATIVE | Missing aggregate |
| `test_valid_hash_returns_hash` | TestVerifyStateHashParity | POSITIVE | Helper returns committed hash |
| `test_invalid_hash_raises` | TestVerifyStateHashParity | NEGATIVE | Helper raises on mismatch |
| `test_all_four_lanes_have_allow_lists` | TestLaneAllowListIntegrity | STRUCTURAL | All lanes registered |
| `test_no_lane_has_empty_allow_list` | TestLaneAllowListIntegrity | STRUCTURAL | No lane starved |
| `test_commander_does_not_see_composer_exclusive_script_draft` | TestLaneAllowListIntegrity | STRUCTURAL | COMMANDER masking |
| `test_hunter_does_not_see_script_draft_or_brief_content` | TestLaneAllowListIntegrity | STRUCTURAL | HUNTER masking |
| `test_all_lanes_allow_declared_inputs_and_repairs` | TestLaneAllowListIntegrity | STRUCTURAL | Audit fields visible to all lanes |

---

## 5. Residual Limitations

1. **Lane allow-lists are explicit enumerations, not schema-driven.**  
   `_LANE_FIELD_ALLOW_LISTS` in `program_state_runtime.py` and `LANE_FIELD_ALLOW_LISTS` in `jit_context_budget.py` enumerate concrete field names.  As new program state schemas are introduced, these lists must be updated.  A schema-driven allow-list generator is deferred to a later mandate.

2. **Node-declared inputs are caller-supplied strings.**  
   The mandate requires nodes to declare their inputs.  This implementation trusts the caller's `declared_inputs` list.  A registry-backed node declaration contract (where each node's allowed inputs are pre-registered) is deferred to a later mandate (Q37 or beyond).

3. **`get_local_context()` still exposes the full aggregate.**  
   Per mandate, the governance/operator surface legitimately needs full visibility.  However, any node execution path that still calls `get_local_context()` instead of `get_pruned_local_context()` will bypass INV-CTX-002.  A follow-on mandate should audit all callers of `get_local_context()` in production paths and migrate them.

4. **M036 is in scope for Wave 05 only.**  
   Live agent host runner loops (Q37), multi-provider routing (Q38), and output self-repair (Q39) are NOT implemented here.

---

## 6. Operator Decision Request

**Approve or reject CA-M036:**

Does the evidence above prove that node execution can now receive strictly pruned, lane-masked context snapshots bound to `state_hash` at the canonical `UniversalProgramStateRuntime` boundary?

- **APPROVE** if: the three invariants (pruning, lane masking, hash parity) are independently verifiable in the tests, no prohibited surfaces were modified, and residual limitations are acceptable.
- **REJECT** if: any of the three invariants cannot be independently proven from the tests alone, or if a prohibited surface boundary was crossed.

**Commit SHA:** _(to be recorded after `git commit` on the applying engineer's workstation)_

