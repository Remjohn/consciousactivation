# CA-M017 Agent Handoff

## Mandate

- **Mandate ID:** `CA-M017`
- **Title:** Multi-Dimensional Evidence Admission
- **Invariant:** `FR-EV-001`
- **Implementation status:** Files prepared for application; tests intentionally **not executed** per operator instruction.
- **Baseline source:** Supplied repository archive (`codebase_clean.zip`). The archive contains no `.git` directory, so an exact local commit SHA could not be captured and no commit was created.

## Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/evidence_admission.py` | Added a fail-closed admission boundary for `media`, `quote`, and `claim` evidence. It applies independent hard thresholds for admission confidence (`>= 0.80`), corroboration count (`>= 2`), and verbatim fidelity (`>= 0.95`), plus the four FR-EVID-001 constitutional boolean dimensions: fidelity, epistemic legality, identity fit, and domain fit. Produces an immutable, hash-addressable admission/quarantine receipt and exposes an explicit downstream generation barrier. | Admission is true only when **all** declared gates pass. Any failed gate produces `QUARANTINED` state, a failure receipt, and `downstream_generation_allowed == False`; scalar confidence cannot compensate for another failed dimension. |
| `tests/phase4/test_ca_m017_evidence_admission.py` | Added Phase 4 acceptance coverage for positive admission, all three quantitative threshold failures, all four constitutional gate failures, missing/invalid gate inputs, downstream-generation blocking, false-proof resistance, per-type coverage, and deterministic receipt behavior. | Tests encode the fail-closed and unanimous-pass contract at `EvidenceAdmissionBoundary.admit`, including the false-proof case where high confidence plus four true booleans still fails due to insufficient corroboration/fidelity. **Not executed per instruction.** |

## Exact paste instructions

From the root of the repository, replace/add exactly these files and no others:

1. Replace/add `services/interview/src/conscious_activations_interview_expression/evidence_admission.py` with the bundled file at the same path.
2. Replace/add `tests/phase4/test_ca_m017_evidence_admission.py` with the bundled file at the same path.
3. Copy `AGENT_HANDOFF.md` only as an execution handoff artifact; it is not intended to be pasted into the repository unless the operator wants to retain it outside the mandate boundary.

No package initializer, migration, persistence schema, composition module, UI module, or downstream generator was changed.

## Manual post-apply commands

Run the mandate-specific acceptance suite from repository root:

```bash
pytest -q tests/phase4/test_ca_m017_evidence_admission.py
```

Recommended broader regression after the mandate-specific suite is green:

```bash
pytest -q tests/phase4
```

No migration or package-install step is required by these two files.

## New automated tests included

- `test_authoritative_boundary_admits_all_three_evidence_types`
- `test_positive_receipt_is_hash_addressable_and_contains_policy`
- `test_each_quantitative_gate_quarantines_fail_closed`
- `test_minimum_thresholds_are_inclusive`
- `test_each_constitutional_boolean_gate_is_non_compensable`
- `test_high_confidence_cannot_rescue_a_failed_other_gate`
- `test_mapping_boundary_rejects_missing_gate_input_without_defaulting_true`
- `test_boolean_gate_must_not_accept_truthy_non_boolean_value`
- `test_quarantined_evidence_is_barred_from_downstream_generation`
- `test_admit_for_generation_requires_a_passing_receipt`
- `test_generation_requires_authoritative_receipt`
- `test_admitted_receipt_can_cross_generation_barrier`
- `test_invalid_quantitative_inputs_are_rejected_fail_closed`
- `test_policy_cannot_create_invalid_permissive_thresholds`
- `test_false_proof_case_four_booleans_plus_high_confidence_is_still_rejected`
- `test_media_quote_and_claim_have_distinct_auditable_receipts`
- `test_repeat_evaluation_is_deterministic_for_same_candidate`

## Evidence locators

- **Authoritative boundary:** `services/interview/src/conscious_activations_interview_expression/evidence_admission.py:214-311` (`EvidenceAdmissionBoundary.admit`, `require_generation_admission`, `admit_for_generation`).
- **Quantitative gates:** `services/interview/src/conscious_activations_interview_expression/evidence_admission.py:303-330` (`_evaluate_gates`).
- **Fail-closed candidate input validation:** `services/interview/src/conscious_activations_interview_expression/evidence_admission.py:91-199` (`EvidenceCandidate` and `from_mapping`).
- **Positive execution proof:** `tests/phase4/test_ca_m017_evidence_admission.py::test_authoritative_boundary_admits_all_three_evidence_types`.
- **Quantitative negative proof:** `tests/phase4/test_ca_m017_evidence_admission.py::test_each_quantitative_gate_quarantines_fail_closed`.
- **Canonical four-dimension negative proof:** `tests/phase4/test_ca_m017_evidence_admission.py::test_each_constitutional_boolean_gate_is_non_compensable`.
- **False-proof countercase:** `tests/phase4/test_ca_m017_evidence_admission.py::test_false_proof_case_four_booleans_plus_high_confidence_is_still_rejected`.
- **Generation barrier:** `tests/phase4/test_ca_m017_evidence_admission.py::test_quarantined_evidence_is_barred_from_downstream_generation` and `::test_generation_requires_authoritative_receipt`.

## Verification state and limitations

- Syntax-only validation was performed with `python -m py_compile` on both bundled Python files.
- **Tests were not run**, exactly as instructed.
- The supplied archive has no `.git` metadata; therefore this handoff cannot truthfully provide a post-change commit SHA. No commit was created by this execution.
- The repository's canonical CAE mandate documentation names `cae_collision_intelligence/domain.py` and `cae_collision_intelligence/verifier.py` as Q17 physical surfaces, while the supplied epoch schedule and this execution request target the new interview-service `evidence_admission.py` boundary. The bundle follows the explicit execution target supplied for `CA-M017` and does not alter the collision-intelligence files.
- Numeric defaults (`0.80`, `2`, `0.95`) are encoded as explicit policy constants so they cannot silently drift; they are not combined into a score. They should be operator/ruleset-reviewed if a ratified threshold table exists outside the supplied snapshot.
- Existing sovereign-media and temporal-anchoring implementations remain untouched; this mandate bundle only enforces the admission decision and downstream barrier at the new boundary.

## Operator decision

**Approve or reject `CA-M017` based on the post-apply executable evidence.** Approval should require the mandate-specific test suite to pass and the operator to ratify the explicit threshold values used by this boundary.
