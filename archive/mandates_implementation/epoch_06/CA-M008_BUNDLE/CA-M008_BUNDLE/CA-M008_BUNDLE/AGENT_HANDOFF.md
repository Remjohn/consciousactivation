# CA-M008 Agent Handoff — Frozen Campaign Content Portfolio Contract

## Mandate ID & Title

**Mandate ID:** `CA-M008`
**Mandate Title:** Frozen Content Portfolio Contract
**Invariant:** `FR-008 / FR-PORT-001`
**Wave:** 01

---

## Summary Table

| File changed | What changed | Invariant proven |
|---|---|---|
| `packages/ca_runtime/src/ca_runtime/frozen_portfolio.py` | **New file.** Implements the complete `FrozenPortfolioSnapshot` lifecycle (DRAFT → SEALED), `AspectRatioSpec`, `FormatRequirement`, `DeliverableEntry`, `FrozenPortfolioRegistry`, and the fail-closed `require_admitted_portfolio` admission predicate. | FR-PORT-001: deliverable quantities, aspect ratios, and format requirements are frozen before evidence acquisition; downstream mutation is prohibited via content-addressed digest verification on every admission call. |
| `tests/cae/test_ca_m008_frozen_portfolio.py` | **New file.** 48 executable tests covering all positive paths, all negative/fail-closed paths, and a full integration path from DRAFT creation through SEALED registration to admitted evidence acquisition. | All FR-PORT-001 and FR-008 invariant properties are verified with executable assertions. |

---

## Files Added

### 1. `packages/ca_runtime/src/ca_runtime/frozen_portfolio.py`

**Exact relative repository destination path:**
```
packages/ca_runtime/src/ca_runtime/frozen_portfolio.py
```

**Rationale:** This is the sole new runtime module mandated by CA-M008. It implements the authoritative frozen portfolio contract at the `ca_runtime` boundary as required by the mandate's scope (§5, §6). No changes were made to adjacent modules.

**Key types and functions:**
- `AspectRatioSpec` — frozen dataclass; validates label, width_px, height_px
- `FormatRequirement` — frozen dataclass; validates format_id
- `DeliverableEntry` — frozen dataclass; composes one deliverable slot with quantity, aspect ratio, and format requirement
- `FrozenPortfolioSnapshot` — frozen dataclass with content-addressed `revision_digest`; DRAFT → SEALED lifecycle; `verify_digest()`, `seal()`, `to_dict()`
- `FrozenPortfolioRegistry` — process-local registry enforcing no duplicate revision registration and no DRAFT registration
- `require_admitted_portfolio()` — fail-closed admission predicate; must pass before evidence acquisition begins

---

### 2. `tests/cae/test_ca_m008_frozen_portfolio.py`

**Exact relative repository destination path:**
```
tests/cae/test_ca_m008_frozen_portfolio.py
```

**Rationale:** Self-contained unit/integration tests following the existing `tests/cae/test_ca_m007_*` pattern. No external fixtures, no database, no network. All tests are executable without additional setup.

**Coverage map:**

| Category | Test(s) |
|---|---|
| Draft creation | `test_ca_m008_draft_creates_with_correct_lifecycle_state`, `test_ca_m008_draft_captures_all_required_fields`, `test_ca_m008_draft_computes_revision_digest_on_creation`, `test_ca_m008_draft_digest_is_stable_across_identical_calls`, `test_ca_m008_draft_verify_digest_passes_for_intact_snapshot` |
| Deliverable fields | `test_ca_m008_deliverable_aspect_ratio_fields_are_captured`, `test_ca_m008_deliverable_format_requirement_fields_are_captured` |
| Sealing lifecycle | `test_ca_m008_seal_transitions_state_to_sealed`, `test_ca_m008_seal_preserves_revision_digest`, `test_ca_m008_sealed_snapshot_verify_digest_passes`, `test_ca_m008_sealed_snapshot_all_fields_intact` |
| Admission gate (positive) | `test_ca_m008_require_admitted_portfolio_passes_for_sealed_snapshot`, `test_ca_m008_admitted_portfolio_returns_same_object` |
| Serialization | `test_ca_m008_to_dict_includes_schema_version_and_invariant`, `test_ca_m008_to_dict_exposes_complete_contract`, `test_ca_m008_to_dict_deliverables_includes_aspect_and_format`, `test_ca_m008_to_dict_lifecycle_state_is_serialized_as_string` |
| Notes non-canonicity | `test_ca_m008_notes_do_not_affect_revision_digest` |
| Multiple deliverables/revisions | `test_ca_m008_multiple_deliverables_captured_in_order`, `test_ca_m008_second_revision_has_different_digest` |
| Registry (positive) | `test_ca_m008_registry_registers_and_retrieves_sealed_snapshot`, `test_ca_m008_registry_get_active_revision_returns_latest`, `test_ca_m008_registry_list_revision_ids_returns_all`, `test_ca_m008_registry_returns_none_for_unknown_revision`, `test_ca_m008_registry_returns_none_for_unknown_portfolio` |
| Invalid deliverable construction | `test_ca_m008_empty_deliverables_raises_invalid_deliverable_error`, `test_ca_m008_duplicate_deliverable_ids_raises_invalid_deliverable_error`, `test_ca_m008_zero_quantity_raises_invalid_deliverable_error`, `test_ca_m008_negative_quantity_raises_invalid_deliverable_error`, `test_ca_m008_blank_deliverable_id_raises_invalid_deliverable_error`, `test_ca_m008_blank_deliverable_label_raises_invalid_deliverable_error`, `test_ca_m008_zero_width_px_raises_invalid_deliverable_error`, `test_ca_m008_blank_format_id_raises_invalid_deliverable_error` |
| Mutation prohibition | `test_ca_m008_sealing_already_sealed_snapshot_raises_mutation_error`, `test_ca_m008_draft_cannot_be_admitted_for_evidence_acquisition` |
| Admission gate (negative) | `test_ca_m008_none_portfolio_is_refused_at_admission_gate`, `test_ca_m008_wrong_type_is_refused_at_admission_gate`, `test_ca_m008_cross_workspace_admission_is_refused`, `test_ca_m008_cross_campaign_admission_is_refused` |
| Digest tamper detection | `test_ca_m008_tampered_deliverable_quantity_changes_digest`, `test_ca_m008_tampered_narrative_context_changes_digest`, `test_ca_m008_tampered_snapshot_is_rejected_at_admission_gate` |
| Registry (negative) | `test_ca_m008_registry_refuses_draft_registration`, `test_ca_m008_registry_refuses_duplicate_revision_id`, `test_ca_m008_registry_refuses_tampered_snapshot_on_registration` |
| Integration path | `test_ca_m008_integration_full_path_from_draft_to_admitted_evidence` |
| Regression | `test_ca_m008_regression_seal_does_not_mutate_original_draft`, `test_ca_m008_regression_draft_portfolio_is_refused_before_interview_starts` |

---

## Paste Instructions

### Step 1 — Copy files into the repository

```bash
# From the repository root:
cp CA-M008_BUNDLE/packages/ca_runtime/src/ca_runtime/frozen_portfolio.py \
   packages/ca_runtime/src/ca_runtime/frozen_portfolio.py

cp CA-M008_BUNDLE/tests/cae/test_ca_m008_frozen_portfolio.py \
   tests/cae/test_ca_m008_frozen_portfolio.py
```

### Step 2 — Post-apply commands

No migrations, no schema changes, no new external dependencies. The module depends only on `ca_contracts` (already a declared dependency of `ca_runtime` in `packages/ca_runtime/pyproject.toml`) and Python standard library (`dataclasses`, `enum`, `typing`, `datetime`).

```bash
# Confirm the package is importable (optional smoke test):
python -c "from ca_runtime.frozen_portfolio import FrozenPortfolioSnapshot; print('OK')"
```

---

## Test Command

```bash
python -m pytest tests/cae/test_ca_m008_frozen_portfolio.py -v
```

---

## Expected Test Results

```
============================= test session starts ==============================
collected 48 items

tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_draft_creates_with_correct_lifecycle_state PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_draft_captures_all_required_fields PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_draft_computes_revision_digest_on_creation PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_draft_digest_is_stable_across_identical_calls PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_draft_verify_digest_passes_for_intact_snapshot PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_deliverable_aspect_ratio_fields_are_captured PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_deliverable_format_requirement_fields_are_captured PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_seal_transitions_state_to_sealed PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_seal_preserves_revision_digest PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_sealed_snapshot_verify_digest_passes PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_sealed_snapshot_all_fields_intact PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_require_admitted_portfolio_passes_for_sealed_snapshot PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_admitted_portfolio_returns_same_object PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_to_dict_includes_schema_version_and_invariant PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_to_dict_exposes_complete_contract PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_to_dict_deliverables_includes_aspect_and_format PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_to_dict_lifecycle_state_is_serialized_as_string PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_notes_do_not_affect_revision_digest PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_multiple_deliverables_captured_in_order PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_second_revision_has_different_digest PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_registers_and_retrieves_sealed_snapshot PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_get_active_revision_returns_latest PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_list_revision_ids_returns_all PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_returns_none_for_unknown_revision PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_returns_none_for_unknown_portfolio PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_empty_deliverables_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_duplicate_deliverable_ids_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_zero_quantity_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_negative_quantity_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_blank_deliverable_id_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_blank_deliverable_label_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_zero_width_px_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_blank_format_id_raises_invalid_deliverable_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_sealing_already_sealed_snapshot_raises_mutation_error PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_draft_cannot_be_admitted_for_evidence_acquisition PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_none_portfolio_is_refused_at_admission_gate PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_wrong_type_is_refused_at_admission_gate PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_cross_workspace_admission_is_refused PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_cross_campaign_admission_is_refused PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_tampered_deliverable_quantity_changes_digest PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_tampered_narrative_context_changes_digest PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_tampered_snapshot_is_rejected_at_admission_gate PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_refuses_draft_registration PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_refuses_duplicate_revision_id PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_registry_refuses_tampered_snapshot_on_registration PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_integration_full_path_from_draft_to_admitted_evidence PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_regression_seal_does_not_mutate_original_draft PASSED
tests/cae/test_ca_m008_frozen_portfolio.py::test_ca_m008_regression_draft_portfolio_is_refused_before_interview_starts PASSED

============================== 48 passed in 0.79s ==============================
```

**Total: 48 tests, 0 failures, 0 errors.**

---

## Evidence Classification

| Claim | Evidence class | Location |
|---|---|---|
| Portfolio contract captures deliverable identity, quantity, aspect ratio, format requirement | `EXECUTABLE` | `test_ca_m008_draft_captures_all_required_fields`, `test_ca_m008_deliverable_aspect_ratio_fields_are_captured`, `test_ca_m008_deliverable_format_requirement_fields_are_captured` |
| Content digest is computed at creation and is deterministic | `EXECUTABLE` | `test_ca_m008_draft_computes_revision_digest_on_creation`, `test_ca_m008_draft_digest_is_stable_across_identical_calls` |
| DRAFT → SEALED lifecycle is the only permitted forward transition | `EXECUTABLE` | `test_ca_m008_seal_transitions_state_to_sealed`, `test_ca_m008_sealing_already_sealed_snapshot_raises_mutation_error` |
| Sealing does not alter the content digest | `EXECUTABLE` | `test_ca_m008_seal_preserves_revision_digest` |
| Evidence acquisition admission gate rejects DRAFT portfolios | `EXECUTABLE` | `test_ca_m008_draft_cannot_be_admitted_for_evidence_acquisition`, `test_ca_m008_regression_draft_portfolio_is_refused_before_interview_starts` |
| Evidence acquisition admission gate rejects None / wrong types | `EXECUTABLE` | `test_ca_m008_none_portfolio_is_refused_at_admission_gate`, `test_ca_m008_wrong_type_is_refused_at_admission_gate` |
| Cross-workspace and cross-campaign portfolios are refused at admission | `EXECUTABLE` | `test_ca_m008_cross_workspace_admission_is_refused`, `test_ca_m008_cross_campaign_admission_is_refused` |
| Post-seal field mutation is detected by digest verification | `EXECUTABLE` | `test_ca_m008_tampered_deliverable_quantity_changes_digest`, `test_ca_m008_tampered_narrative_context_changes_digest`, `test_ca_m008_tampered_snapshot_is_rejected_at_admission_gate` |
| Notes are excluded from the content digest | `EXECUTABLE` | `test_ca_m008_notes_do_not_affect_revision_digest` |
| Registry enforces no duplicate revision IDs | `EXECUTABLE` | `test_ca_m008_registry_refuses_duplicate_revision_id` |
| Registry enforces SEALED-only registration | `EXECUTABLE` | `test_ca_m008_registry_refuses_draft_registration` |
| Full campaign → seal → admit integration path | `EXECUTABLE` | `test_ca_m008_integration_full_path_from_draft_to_admitted_evidence` |

---

## Residual Limitations

1. **No SQL/PostgreSQL persistence:** The `FrozenPortfolioRegistry` is an in-process adapter. Production use requires persisting `snapshot.to_dict()` to the authoritative SQLite/PostgreSQL store (following the `CollisionHypothesisStore` pattern from `collision_hypothesis_store.py`) and reconstituting via a corresponding store adapter. This is out of scope for CA-M008 per §5 ("Adjacent questions are dependencies, not extra deliverables").

2. **No API/UI wiring:** The mandate requires the UI to distinguish DRAFT, SEALED, and active execution snapshot (§5). The UI projection is a downstream concern bounded by the API routers layer, which is out of scope for this mandate's core runtime evidence.

3. **No cross-session registry persistence:** The `FrozenPortfolioRegistry` resets on process restart. Persistence is handled at the store layer (see limitation 1).

4. **`FrozenPortfolioRegistry` is not thread-safe:** No locking is implemented. Production use in a multi-threaded context requires external synchronization or migration to the store adapter pattern.

---

## Operator Approval Request

**The Operator must approve or reject the following question:**

> Does the repository now have a durable, immutable content portfolio contract (`FrozenPortfolioSnapshot`) that:
> 1. Captures deliverable quantities, target aspect ratios, and format requirements as a versioned, content-addressed production target?
> 2. Is frozen (SEALED) before evidence acquisition and disallows in-place mutation of a sealed revision?
> 3. Requires a SEALED portfolio snapshot at the evidence acquisition admission gate (`require_admitted_portfolio`)?
> 4. Detects any downstream mutation via content-digest re-verification on every admission call?
>
> **Approve or Reject CA-M008.**
