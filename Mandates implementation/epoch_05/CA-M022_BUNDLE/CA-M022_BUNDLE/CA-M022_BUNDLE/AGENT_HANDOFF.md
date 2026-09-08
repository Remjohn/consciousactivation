# AGENT HANDOFF — CA-M022
## Mandate: Adaptive Elicitation & Missing-Unit Resilience (FR-022 / FR-ELIC-002)

---

## 1. Summary Table

| File Changed | What Changed | Invariant Proven |
|---|---|---|
| `services/interview/src/conscious_activations_interview_expression/adaptive_remediation.py` | **NEW** — Authoritative holistic yield-sufficiency evaluator for CA-M022. Implements `ElicitationUnitRecord`, `YieldSufficiencyPolicy`, `YieldEvaluationReceipt`, `AdaptiveElicitationEvaluator`, and `RemediationPromptGenerator`. Provides the `evaluate_session_yield` and `require_session_passed` module-level entry points. | `FR-ELIC-002`: Interview completion evaluated on holistic narrative yield sufficiency, not 100% linear script execution. Omitted units remain visible. Fail-closed on insufficient yield. |
| `tests/phase4/test_ca_m022_adaptive_remediation.py` | **NEW** — 50-test acceptance suite covering schema, positive path, negative/fail-closed path, missing-unit visibility, `require_session_passed` guard, remediation prompt injection, unit record validation, integration boundary, and a false-proof countercase. | All gate paths (yield ratio, tension, evidence count, omission rate ceiling) are independently tested. False-proof test explicitly proves partial progress is not accepted as holistic success. |

---

## 2. Paste Instructions

Replace or create the following files in the repository root at the exact paths shown:

```
# New file — does not exist in the repository
services/interview/src/conscious_activations_interview_expression/adaptive_remediation.py
  ← CA-M022_BUNDLE/services/interview/src/conscious_activations_interview_expression/adaptive_remediation.py

# New test file — does not exist in the repository
tests/phase4/test_ca_m022_adaptive_remediation.py
  ← CA-M022_BUNDLE/tests/phase4/test_ca_m022_adaptive_remediation.py
```

**No existing files are modified.** The mandate explicitly allows only the two paths above (as confirmed by cross-checking mandate section 6 against the codebase).

---

## 3. Manual Post-Apply Commands

No migrations, schema changes, or npm scripts are required.

The module is self-contained pure Python and has no external runtime dependencies beyond the standard library (`hashlib`, `json`, `dataclasses`, `enum`, `math`).

**Optional — verify the module is importable after copy:**

```bash
cd <repo-root>
python -c "from conscious_activations_interview_expression.adaptive_remediation import AdaptiveElicitationEvaluator; print('CA-M022 OK')"
```

Expected output: `CA-M022 OK`

---

## 4. New Automated Tests Included in This Bundle

File: `tests/phase4/test_ca_m022_adaptive_remediation.py`

Test names (50 tests):

**SCHEMA**
- `test_mandate_constants_are_correct`
- `test_policy_defaults_are_within_bounds`
- `test_unit_record_schema_fields_present`
- `test_receipt_schema_fields_present`

**EXECUTABLE — positive path**
- `test_session_with_one_omitted_unit_passes_when_yield_criteria_met`
- `test_session_with_multiple_omitted_units_passes_when_yield_criteria_met`
- `test_all_units_executed_passes_trivially`
- `test_partial_units_count_toward_yield_ratio`
- `test_custom_policy_lower_thresholds_accepts_weaker_session`
- `test_zero_omission_rate_passes_ceiling_gate`

**EXECUTABLE — negative / fail-closed path**
- `test_session_fails_when_yield_ratio_below_minimum`
- `test_session_fails_when_tension_below_minimum`
- `test_session_fails_when_evidence_count_below_minimum`
- `test_session_fails_when_omission_rate_exceeds_maximum`
- `test_all_units_omitted_fails_every_gate`
- `test_partial_units_only_no_evidence_fails_evidence_gate`
- `test_empty_unit_list_fails_yield_and_evidence_gates`

**EXECUTABLE — omitted units remain visible**
- `test_omitted_units_recorded_in_passing_receipt`
- `test_omitted_units_recorded_in_failing_receipt`
- `test_omitted_unit_reason_is_preserved`
- `test_omitted_units_tuple_is_always_present_even_when_empty`

**EXECUTABLE — require_session_passed guard**
- `test_require_session_passed_does_not_raise_for_passing_receipt`
- `test_require_session_passed_raises_for_failing_receipt`
- `test_require_session_passed_raises_for_foreign_receipt_mandate`
- `test_require_session_passed_raises_for_non_receipt`

**EXECUTABLE — remediation prompt injection**
- `test_failing_session_gets_remediation_prompts`
- `test_passing_session_has_no_remediation_prompts`
- `test_reactivate_prompt_generated_for_omitted_unit`
- `test_deepen_prompt_generated_for_low_tension_unit`
- `test_remediation_prompts_have_constitutional_check_passed`
- `test_remediation_prompt_kind_matches_failure_type`

**EXECUTABLE — unit record validation**
- `test_omitted_unit_requires_nonempty_omission_reason`
- `test_omitted_unit_requires_zero_tension`
- `test_omitted_unit_requires_zero_evidence`
- `test_executed_unit_accepts_nonzero_values`
- `test_invalid_status_raises_error`
- `test_invalid_tension_score_type_raises_error`
- `test_tension_score_out_of_range_raises_error`
- `test_missing_required_field_in_mapping_raises_error`
- `test_empty_unit_id_raises_error`

**INTEGRATION — authoritative boundary**
- `test_evaluate_returns_receipt_with_correct_session_id`
- `test_receipt_is_hash_addressable_and_deterministic`
- `test_module_level_convenience_function_matches_class_method`
- `test_receipt_to_dict_is_json_serialisable`
- `test_evaluate_with_mapping_input`
- `test_invalid_session_id_raises_evaluation_blocked`

**FALSE-PROOF countercase**
- `test_false_proof_any_unit_executed_does_not_imply_pass`

---

## 5. Invariant Evidence

### Invariant: FR-ELIC-002 — Holistic Yield Sufficiency

**Positive acceptance proof:**
`test_session_with_one_omitted_unit_passes_when_yield_criteria_met` — a session with 3 executed units and 1 omitted unit (yield ratio 0.75 > 0.70, tension 0.75 > 0.40, evidence 9 > 1, omission rate 0.25 < 0.50) passes at the authoritative `AdaptiveElicitationEvaluator.evaluate` boundary.

**Negative / fail-closed proof:**
`test_session_fails_when_yield_ratio_below_minimum` — a session with 1 executed and 4 omitted (ratio 0.20 < 0.70) is rejected even though the single executed unit has exemplary tension and evidence.

**Missing-unit visibility proof:**
`test_omitted_units_recorded_in_passing_receipt` and `test_omitted_unit_reason_is_preserved` — the `omitted_units` tuple is populated in both passing and failing receipts; omission reason is preserved verbatim.

**False-proof countercase:**
`test_false_proof_any_unit_executed_does_not_imply_pass` — explicitly proves that a session with at least one perfectly-executed unit (tension 0.90, evidence 5) is still rejected when 4 of 5 planned units were omitted. This closes the loophole that partial progress could be mistaken for holistic success.

**Remediation coherence proof:**
`test_remediation_prompts_have_constitutional_check_passed` — all injected prompts carry `constitutional_check_passed=True`, confirming the constitution boundary was applied before injection.

---

## 6. Residual Limitations

1. **Yield criteria definition**: The `YieldSufficiencyPolicy` default thresholds (0.70 ratio, 0.40 tension, 1 evidence, 0.50 omission ceiling) are conservative defaults. The authoritative portfolio yield criteria for a specific campaign (Q23 scope) are not expressed by this module. If the Operator requires campaign-specific thresholds, they must supply a custom `YieldSufficiencyPolicy`. This is a limitation of scope, not an invariant violation.

2. **Tension and evidence scores are caller-provided**: The module accepts caller-declared `tension_score` and `evidence_count` values. The authentication of those values (e.g. that they derive from admitted evidence objects) is the responsibility of the upstream elicitation pipeline. This module does not re-verify upstream admission receipts.

3. **Remediation prompts are suggestions only**: Injected `RemediationPrompt` objects are not dispatched to the live session by this module. Authority to dispatch remains with the Operator/live session controller. This is intentional and required by the mandate's conversational coherence constraint.

4. **Q23 portfolio gating is out of scope**: Full portfolio yield gating against deliverable contracts (Mandate Q23) is explicitly excluded from this implementation.

---

## 7. Operator Decision Request

**APPROVE or REJECT CA-M022**

Evidence demonstrates that:
- Interview completion is evaluated on holistic narrative yield sufficiency at the `AdaptiveElicitationEvaluator.evaluate` boundary.
- A session with one or more omitted units CAN succeed when overall yield criteria are met (positive path proven).
- A session that fails yield criteria IS rejected even when some units executed (negative path proven).
- Omitted units ALWAYS remain visible in the completion record, even on a passing session.
- The false-proof countercase confirms that partial execution does not constitute holistic success.
- Remediation prompts are injected without breaking constitution boundaries (`constitutional_check_passed=True` on all prompts).
- No prohibited surfaces (portfolio gating, authorization policy, unrelated manifests, UI state) were modified.

**The Operator must now decide: APPROVE or REJECT CA-M022.**
