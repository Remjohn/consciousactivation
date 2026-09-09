# CA-M025 Agent Handoff

## Execution scope

Mandate: `CA-M025`  
Requirement requested: `FR-POL-001`  
Target: production-tier campaign execution authorization.

The provided repository snapshot did not contain the requested `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py` or `tests/wave04/test_ca_m025_campaign_auth_policy.py`. The bundle therefore adds both as new files and does not modify any other repository surface.

The bundled CA-M025 mandate document in `docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_04/02_CA_MANDATE_025.md` describes a configurable autonomy-policy decision (`FR-AUTH-001`), while the explicit execution requirement supplied for this task is `FR-POL-001` (role, production tier, and spend thresholds). This implementation follows the explicit task acceptance criteria and records the document mismatch as a residual governance limitation rather than silently changing unrelated policy infrastructure.

## 1. Summary table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py` | Added the canonical production campaign authorization evaluator, typed policy/request models, deterministic policy identity, descriptive immutable decision receipts, authentication enforcement, role allow-list enforcement, production-tier enforcement, campaign remaining-budget enforcement, per-run spend threshold enforcement, and fail-closed invalid-input handling. | `FR-POL-001`: an execution can be authorized only for an authenticated actor with an authorized production role, on the production tier, with spend within both the campaign and per-run thresholds. Unauthenticated, unauthorized, non-production, invalid-spend, and over-budget requests are denied with explicit reason codes and details. |
| `tests/wave04/test_ca_m025_campaign_auth_policy.py` | Added focused runtime-boundary coverage for positive authorization, role denial, unauthenticated denial, tier denial, cumulative budget denial, per-run threshold denial, invalid spend, mapping/API-boundary input, invalid policy rejection, deterministic receipt identity, policy identity changes, descriptive receipts, and the required false-proof countercase. | The test suite exercises the evaluator itself rather than a parser-only or mocked boundary; the contrastive case proves that valid-looking role/tier strings do not authorize an unauthenticated request. |

## 2. Exact paste instructions

Replace/add these repository files exactly:

1. `CA-M025_BUNDLE/packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py`
   → repository path `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py`

2. `CA-M025_BUNDLE/tests/wave04/test_ca_m025_campaign_auth_policy.py`
   → repository path `tests/wave04/test_ca_m025_campaign_auth_policy.py`

No other repository paths are authorized or required by this bundle.

## 3. Runtime boundary

The authoritative enforcement function is:

`CampaignAuthorizationPolicyEngine.evaluate()`

The functional entrypoint is:

`authorize_campaign_execution(request, policy)`

Both paths use the same typed request normalization and fail-closed evaluation logic.

The policy's non-waivable controls are explicitly represented as:

`AUTHENTICATED_ACTOR`, `AUTHORIZED_ROLE`, `PRODUCTION_TIER`, `SPEND_WITHIN_BUDGET`.

## 4. Budget semantics

The implementation treats the campaign budget as:

`remaining_budget_units = budget_limit_units - spend_to_date_units`

An execution is allowed only when:

`estimated_spend_units <= remaining_budget_units`

and, when configured:

`estimated_spend_units <= max_run_spend_units`

Negative spend values are rejected.

The default production authorization roles are `COMMANDER` and `OPERATOR`. The policy can accept a narrower or broader explicit allow-list only from the existing canonical campaign role set; unknown roles are rejected at policy construction.

## 5. Receipt behavior

Every evaluation returns a `CampaignAuthorizationReceipt`.

Denials include:

- decision and stable reason code;
- human-readable message;
- campaign and actor identifiers;
- actor role and authentication state;
- campaign tier;
- requested and cumulative spend;
- campaign budget and remaining budget;
- per-run threshold;
- policy ID/version/digest;
- non-waivable control names;
- evaluation timestamp;
- deterministic receipt identity;
- structured denial details.

This bundle does not add durable receipt persistence or policy-revision binding.

## 6. Automated tests included

- `test_authorize_production_run_for_authenticated_operator_within_budget`
- `test_production_control_roles_are_authorized`
- `test_rejects_authenticated_non_control_role`
- `test_rejects_unauthenticated_production_execution_with_descriptive_receipt`
- `test_rejects_non_production_tiers`
- `test_rejects_when_cumulative_spend_would_exceed_campaign_budget`
- `test_rejects_when_single_run_spend_threshold_is_exceeded`
- `test_rejects_negative_spend_fail_closed`
- `test_mapping_input_uses_same_canonical_evaluator_boundary`
- `test_invalid_policy_cannot_be_used_as_a_silent_less_restrictive_fallback`
- `test_false_proof_countercase_role_and_tier_strings_alone_do_not_authorize`
- `test_receipt_identity_is_deterministic_for_same_evaluation_inputs`
- `test_policy_identity_changes_when_budget_threshold_changes`
- `test_receipts_are_descriptive_for_over_budget_denial`
- `test_production_tier_is_a_hard_constraint_even_for_commanders`

## 7. Manual post-apply commands

No migration or data backfill is required.

The requested focused verification command, to be run after applying the bundle, is:

```bash
python -m pytest tests/wave04/test_ca_m025_campaign_auth_policy.py
```

This command was **not run during bundle preparation**, per the task instruction.

## 8. Evidence and limitations

Evidence locators:

- Runtime boundary: `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py:CampaignAuthorizationPolicyEngine.evaluate`
- Functional boundary: `packages/ca_runtime/src/ca_runtime/campaign_auth_policy.py:authorize_campaign_execution`
- Positive/negative proof suite: `tests/wave04/test_ca_m025_campaign_auth_policy.py`
- False-proof countercase: `test_false_proof_countercase_role_and_tier_strings_alone_do_not_authorize`

Preparation verification performed: Python compilation/syntax check succeeded for both bundled files. No pytest/test execution was performed.

Residual limitation: no repository commit was created by this bundle operation, so there is no new commit SHA to report. Capture the exact commit SHA after applying the two files and completing operator review.

## 9. Operator decision requested

Approve or reject `CA-M025` after applying the bundle and reviewing executable evidence for `FR-POL-001` at the canonical policy evaluator boundary.
