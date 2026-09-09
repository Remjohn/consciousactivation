# CA-M004 AGENT HANDOFF — Pipeline Stage Ordering & Causal Flow

**Mandate ID:** CA-M004  
**Canonical Question:** Q04  
**Invariant:** INV-CAUSAL-001  
**Status:** Implementation complete — awaiting Operator approval

## 1. Summary table

| File changed | What changed | Invariant proven |
|--------------|--------------|------------------|
| `services/pipeline/src/cmf_pipeline/workflow/admission/__init__.py` | **NEW** — package export for causal admission types | INV-CAUSAL-001 surface |
| `services/pipeline/src/cmf_pipeline/workflow/admission/causal_admission.py` | **NEW** — `CausalAdmissionService`, `RequiredAncestor`, `AncestorBinding`, structured blocks (missing / wrong-order / stale-identity / invalid-state / placeholder / bypass) | INV-CAUSAL-001 core enforcement at admission boundary |
| `services/pipeline/src/cmf_pipeline/workflow/application/scheduler.py` | Integrated causal evaluation into `ready_nodes`, `safe_parallel_batch`, and new `admit_node`; force-run prohibited | Ordering + ancestor integrity at scheduler gate |
| `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py` | Wired `CausalAdmissionService` into `WorkflowRunService`; explicit `admit_node` call inside `dispatch_node` (fail-closed) | Runtime admission boundary used by production dispatch |
| `tests/pipeline/test_causal_admission.py` | **NEW** — positive valid progression; negative missing / wrong-order / stale digest / revision / invalid state / placeholder / force-bypass / no-binding; scheduler integration; UI runtime-fact projection; legacy regression path | Executable evidence (unit + integration-style) |

## 2. Exact paste instructions

Replace or add files at these repository paths (mirror exactly):

```
CA-M004_BUNDLE/services/pipeline/src/cmf_pipeline/workflow/admission/__init__.py
  → services/pipeline/src/cmf_pipeline/workflow/admission/__init__.py

CA-M004_BUNDLE/services/pipeline/src/cmf_pipeline/workflow/admission/causal_admission.py
  → services/pipeline/src/cmf_pipeline/workflow/admission/causal_admission.py

CA-M004_BUNDLE/services/pipeline/src/cmf_pipeline/workflow/application/scheduler.py
  → services/pipeline/src/cmf_pipeline/workflow/application/scheduler.py

CA-M004_BUNDLE/services/pipeline/src/cmf_pipeline/workflow/application/run_service.py
  → services/pipeline/src/cmf_pipeline/workflow/application/run_service.py

CA-M004_BUNDLE/tests/pipeline/test_causal_admission.py
  → tests/pipeline/test_causal_admission.py
```

No other files are modified. The new `admission/` package is additive.

## 3. Manual post-apply commands

```bash
# From repository root (after pasting files)

# Install / editable install of pipeline package if required by local layout
# pip install -e services/pipeline

# Run only the new causal admission tests (do not run full suite unless desired)
pytest tests/pipeline/test_causal_admission.py -v

# Optional: confirm import surface
python -c "from cmf_pipeline.workflow.admission import CausalAdmissionService; print('OK')"
```

No database migrations are required. No npm / frontend rebuild is required for this mandate (UI projection of blocked state is available via `CausalAdmissionResult.to_runtime_fact()` for downstream wiring).

## 4. Names of new automated tests included in the bundle

- `tests/pipeline/test_causal_admission.py`
  - `TestCausalAdmissionService`
    - `test_positive_valid_progression_admitted`
    - `test_negative_missing_ancestor`
    - `test_negative_wrong_topological_order`
    - `test_negative_wrong_phase_order`
    - `test_negative_stale_digest_mismatch`
    - `test_negative_revision_mismatch`
    - `test_negative_invalid_prerequisite_state`
    - `test_negative_synthesized_placeholder`
    - `test_negative_force_bypass_prohibited`
    - `test_require_admitted_raises`
    - `test_constructor_rejects_allow_force`
    - `test_no_binding_when_state_present_but_no_identity`
    - `test_bindings_from_artifacts_helper`
  - `TestSchedulerCausalIntegration`
    - `test_ready_nodes_requires_succeeded_predecessors`
    - `test_ready_nodes_with_valid_bindings_admits`
    - `test_ready_nodes_blocks_wrong_order_via_causal`
    - `test_admit_node_raises_on_missing`
    - `test_admit_node_succeeds_with_bindings`
    - `test_force_on_admit_blocked`
    - `test_enforce_causal_false_preserves_legacy_topology_only` (regression)
  - `TestRuntimeFactProjection`
    - `test_blocked_fact_surface_for_ui`

## 5. Evidence locators

| Claim | Locator |
|-------|---------|
| Causal order + ancestor integrity enforced at runtime admission | `services/pipeline/src/cmf_pipeline/workflow/admission/causal_admission.py` (`CausalAdmissionService.evaluate` / `require_admitted`) |
| Dispatch path cannot bypass | `services/pipeline/src/cmf_pipeline/workflow/application/run_service.py` (`dispatch_node` → `scheduler.admit_node`) |
| Force-run prohibited | `CausalAdmissionService.__init__` rejects `allow_force=True`; `force=True` yields `BYPASS_ATTEMPT` |
| Positive + negative executable evidence | `tests/pipeline/test_causal_admission.py` |
| UI-facing runtime facts (blocked stage + reason) | `CausalAdmissionResult.to_runtime_fact()` |

## 6. Residual limitations

- Artifact identity bindings (`AncestorBinding`) are expected to be supplied by callers (or derived via `bindings_from_node_states_and_artifacts`). The dispatch path currently passes an empty binding map; production wiring that materializes digests/revisions from repository artifacts remains a follow-on integration (outside this mandate’s smallest safe boundary).
- Full 17-stage product spine is not implemented here (explicitly out of scope).
- UI React components are not modified; they can consume `to_runtime_fact()` projections when ready.
- Program-manifest dependency declarations (`programs/*/program_manifest.yaml`) are not automatically loaded into workflow edges by this change; existing workflow edges remain the dependency source of truth inside the pipeline runtime.

## 7. Operator decision required

**Approve or reject** whether the runtime now demonstrably prevents downstream execution from inventing or bypassing missing upstream meaning for the scoped programs (workflow nodes under `services/pipeline`).

Evidence package: changed files listed above; tests in `tests/pipeline/test_causal_admission.py`; residual limitations in §6.

Commit SHA: *not captured in this execution environment — Operator should record SHA after apply/commit.*
