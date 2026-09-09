# CA-M033 Agent Handoff

## Mandate
- Mandate ID: `CA-M033`
- Canonical question: `Q33`
- Objective: enforce `SPECIFIED → IMPLEMENTED → VERIFIED` for the canonical FR contract, with `VERIFIED` gated by discoverable and passing positive + negative automated acceptance tests.
- Test execution in this agent run: **NOT RUN**, per operator instruction.
- Commit SHA: **NOT GENERATED** (bundle-only execution; no repository commit was created).

## Summary

| File changed | What changed | Invariant proven |
|---|---|---|
| `docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md` | Changed the contract header to verification-gated status; kept all 57 FRs stage-mapped; retained `FR-033` as the only `VERIFIED` requirement; moved the other 56 FRs to `IMPLEMENTED`; added the canonical positive/negative test registry and residual-state record. | A documentation-only `VERIFIED` claim is no longer accepted as sufficient evidence; `VERIFIED` requires an explicit executable positive/negative test pair. |
| `docs/cae/cae-bmad/03_product/fr_test_contract_harness.py` | Added the CA-M033 parser, lifecycle validator, pytest locator discovery, pytest execution gate, CLI validation path, and fail-closed decision model. | `SPECIFIED` cannot skip to `VERIFIED`; `VERIFIED` is allowed only after both registered tests are discovered and pass through the repository's real pytest boundary. |
| `tests/cae/test_m033_canonical_fr_test_contract_harness.py` | Added structural, positive, negative, false-proof, discovery, failure, and lifecycle-transition coverage. | The gate is exercised through real pytest subprocess discovery/execution, including a successful `IMPLEMENTED → VERIFIED` path and blocked false-proof/failure paths. |

## Exact paste instructions

Replace the repository file:

`docs/cae/cae-bmad/03_product/FUNCTIONAL_REQUIREMENTS.md`

with the bundled file at the same path.

Add the bundled file:

`docs/cae/cae-bmad/03_product/fr_test_contract_harness.py`

Add the bundled test file:

`tests/cae/test_m033_canonical_fr_test_contract_harness.py`

No other repository files are authorized or included in this bundle.

## Manual post-apply commands

Run from the repository root after applying the three files:

```text
python docs/cae/cae-bmad/03_product/fr_test_contract_harness.py validate
python docs/cae/cae-bmad/03_product/fr_test_contract_harness.py verify
pytest -q tests/cae/test_m033_canonical_fr_test_contract_harness.py
```

No database migration or generated-artifact step is required by CA-M033.

The `verify` command executes the positive and negative acceptance locators registered for every currently `VERIFIED` FR. Under this implementation, that registry contains `FR-033` only.

## Automated tests included

- `test_m033_contract_matrix_is_complete_and_status_consistent`
- `test_m033_registry_locators_are_real_pytest_nodes`
- `test_m033_canonical_document_rejects_unregistered_verified_claim`
- `test_m033_positive_verified_path`
- `test_m033_negative_verified_path`
- `test_m033_failing_positive_path_is_fail_closed`
- `test_m033_specified_cannot_skip_implemented_lifecycle_state`
- `test_m033_missing_positive_locator_is_blocked_before_execution`

## Residual limitations

`FR-001` through `FR-032` and `FR-034` through `FR-057` are intentionally `IMPLEMENTED`, not `VERIFIED`, because CA-M033 does not implement their runtime bodies or invent acceptance-test evidence for them. Each must receive its own positive/negative test registration before being promoted.

The bundled test suite was not executed in this agent run, as explicitly requested.
