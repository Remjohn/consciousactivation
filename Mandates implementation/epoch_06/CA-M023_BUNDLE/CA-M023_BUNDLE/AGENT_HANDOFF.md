# CA-M023 — Deterministic Portfolio Yield Gating

## Mandate ID & Title

**Mandate ID:** `CA-M023`  
**Mandate Title:** `Deterministic Portfolio Yield Gating`

**Invariant:** `FR-023` / `INV-YIELD-001`

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py` | Added a deterministic, contract-driven portfolio yield gate; validates a frozen contract hash; evaluates minimum viable candidate count, evidence-backed ratio, and four portfolio diversity dimensions; emits deterministic structured gap/receipt data; blocks downstream media assembly on any failed hard gate. | Insufficient portfolio yield or diversity fails closed before the downstream assembly callback can execute; no heuristic aggregate score can compensate for a failed contract dimension. |
| `tests/interview_intelligence/test_ca_m023_yield_gating.py` | Added 16 self-contained acceptance tests covering schema/binding, positive progression, independent hard gates, multi-gap reports, deterministic receipts, frozen-contract authority, false-proof rejection, and downstream callback blocking/progression. | Executable proof of `INV-YIELD-001` at the implemented gate boundary, including a costly-stage non-invocation counterexample. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

1. `services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py`
   - Adds the CA-M023 authoritative gate surface.
   - Thresholds are supplied by an explicit frozen `FrozenContentPortfolioContract`; the module does not invent policy defaults.
   - The contract is self-bound by SHA-256 and cannot be constructed with a mismatched digest.
   - Yield is conjunctive across all requirements: viable candidates, evidence-backed ratio, audience-island diversity, tension diversity, guest-territory diversity, and archetype diversity.
   - Failing evaluations return auditable structured deficit reports and `gate_downstream_media_assembly()` raises `YieldGateBlockedError` before invoking the downstream callback.

2. `tests/interview_intelligence/test_ca_m023_yield_gating.py`
   - Adds the complete CA-M023 test contract.
   - Includes the required false-proof countercase: an apparently strong overall yield does not unlock assembly when a hard diversity requirement fails.

### Files Modified

None. The supplied archive did not contain pre-existing CA-M023 target files, so both bounded implementation surfaces were added without altering unrelated repository files.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

Copy the two bundle files to these exact repository destinations:

```text
CA-M023_BUNDLE/
├── AGENT_HANDOFF.md
├── services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py
└── tests/interview_intelligence/test_ca_m023_yield_gating.py
```

No database migration is required. No registry update is required. No setup script is required for the CA-M023 target tests beyond the repository's normal Python/pytest environment.

Post-apply verification:

```bash
pytest -q tests/interview_intelligence/test_ca_m023_yield_gating.py
python -m compileall -q services/interview-intelligence/src/cae_interview_intelligence/yield_gating.py tests/interview_intelligence/test_ca_m023_yield_gating.py
```

The target implementation expects the authoritative caller to provide the already-frozen Content Portfolio Contract values and its SHA-256. This prevents CA-M023 from silently creating a second portfolio policy.

## Test Command (exact pytest/test command to verify)

```bash
pytest -q tests/interview_intelligence/test_ca_m023_yield_gating.py
```

## Expected Test Results (number of automated tests, all passing)

**16 automated tests — all passing.**

Observed result in the supplied sandbox:

```text
16 passed
```

Additional repository-level check attempted:

```bash
pytest -q tests/interview_intelligence
```

That broader collection did not complete because three pre-existing interview-intelligence test modules import `psycopg`, which is not installed in the supplied sandbox. The failure is:

```text
ModuleNotFoundError: No module named 'psycopg'
```

The CA-M023 test file itself has no `psycopg` dependency and passed 16/16.

## Evidence Locators

- Positive gate proof: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_positive_path_unlocks_when_every_contract_gate_passes`
- Independent hard-gate proof: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_each_contract_metric_is_independently_hard_gated`
- Evidence-ratio hard gate: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_evidence_backed_ratio_is_hard_gated_even_with_sufficient_count_and_diversity`
- Structured fail-closed report: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_multiple_gaps_are_returned_structured_and_fail_closed`
- Determinism proof: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_receipt_is_deterministic_for_identical_contract_and_metrics`
- False-proof countercase: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_false_proof_high_aggregate_yield_score_does_not_unlock_assembly`
- Costly-stage blocking proof: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_downstream_assembly_callback_is_not_called_when_yield_fails`
- Positive downstream progression: `tests/interview_intelligence/test_ca_m023_yield_gating.py::test_downstream_assembly_callback_runs_after_a_passing_gate`

## Residual Limitations / Operator Decision

The supplied archive contains no `.git` metadata, so an actual repository commit SHA cannot be truthfully captured; no synthetic SHA was created.

The broader subsystem test collection also has a pre-existing sandbox dependency gap (`psycopg` missing). The CA-M023 implementation and its dedicated 16-test contract are independently executable and passing.

**Operator decision requested:** approve or reject `CA-M023` based on the executable evidence above. The implementation proves fail-closed portfolio gating at the new downstream-media-assembly gate boundary; wiring an existing production renderer to this boundary would require an additional repository integration change outside the exact two-file mandate boundary supplied for CA-M023.
