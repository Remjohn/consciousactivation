# AGENT HANDOFF — CA-M011: Sealed Pre-Production Pack

**Mandate ID:** CA-M011  
**Wave:** 02  
**Governing Requirement / Invariant:** FR-PREP-001  
**Causal Stage:** Stage 05 — Declarative PreProduction / execution boundary  
**Status:** IMPLEMENTATION COMPLETE — operator gate required before CA-M012 may proceed

---

## 1. Summary Table

| File Changed / Created | What Changed | Invariant Proven |
|---|---|---|
| `services/pipeline/src/cmf_pipeline/preproduction/__init__.py` | **NEW** — Package init; exports public API of the pre-production sealing subsystem | FR-PREP-001 public surface established |
| `services/pipeline/src/cmf_pipeline/preproduction/sealer.py` | **NEW** — Full implementation of `PreProductionSealer`, `PreprodPackDraft`, `SealedPreprodPack`, `ConstituentRef`, lifecycle enums, and admission errors | FR-PREP-001: cryptographic sealing enforced; fail-closed admission proven; mutable-rehydration detection proven |
| `tests/phase6/test_ca_m011_preproduction_pack.py` | **NEW** — Comprehensive positive + negative + anti-centroid test suite (27 tests) | All mandate invariants provable; false-proof case explicitly tested |

---

## 2. Paste Instructions

Apply each file at its exact repo-relative path from the repository root:

```
# From the repository root (Remjohn/consciousactivation):

cp CA-M011_BUNDLE/services/pipeline/src/cmf_pipeline/preproduction/__init__.py \
   services/pipeline/src/cmf_pipeline/preproduction/__init__.py

cp CA-M011_BUNDLE/services/pipeline/src/cmf_pipeline/preproduction/sealer.py \
   services/pipeline/src/cmf_pipeline/preproduction/sealer.py

cp CA-M011_BUNDLE/tests/phase6/test_ca_m011_preproduction_pack.py \
   tests/phase6/test_ca_m011_preproduction_pack.py
```

No existing files are modified.  The `preproduction/` directory is new.

---

## 3. Post-Apply Commands

### 3a. No new SQL migrations required

The `PreProductionSealer` stores all objects via the existing `PipelineRepository.store_object()` path using three new `object_type` string constants:

| Object type constant | Value |
|---|---|
| `PREPROD_PACK_OBJECT_TYPE` | `"preprod_sealed_pack"` |
| `PREPROD_RUN_BINDING_OBJECT_TYPE` | `"preprod_run_binding"` |
| `PREPROD_ADMISSION_RECEIPT_OBJECT_TYPE` | `"preprod_admission_receipt"` |

These are stored in the existing `pipeline_objects` table (from `0001_pipeline_core.sql`).  No schema migration is required.

### 3b. Reinstall the pipeline package (editable install)

The new `preproduction/` subpackage must be visible to the Python import system.  In the `services/pipeline/` directory:

```bash
pip install -e . --break-system-packages
# or, if using a virtual environment:
pip install -e .
```

The `setuptools` `[tool.setuptools.packages.find]` configuration in `pyproject.toml` already uses `where = ["src"]` with `include = ["cmf_pipeline*"]`, so the new subpackage is picked up automatically.

### 3c. (Optional) Verify the import is resolving

```bash
python -c "from cmf_pipeline.preproduction import PreProductionSealer; print('OK')"
```

---

## 4. New Automated Tests Included

All tests are in `tests/phase6/test_ca_m011_preproduction_pack.py`.

### Class `TestPositive` — intended path

| Test name | Property proved |
|---|---|
| `test_compile_and_seal_returns_sealed_pack` | compile_and_seal() returns state=SEALED with 64-char SHA-256 pack_digest |
| `test_pack_digest_is_deterministic` | identical drafts produce identical digests across independent sealer instances |
| `test_sealed_pack_is_retrievable_by_id` | sealed pack survives repository round-trip with digest preserved |
| `test_admitted_run_binding_is_persisted` | run binding receipt is persisted after successful admission |
| `test_constituent_cross_check_passes_for_exact_match` | admission with expected_constituents succeeds when all digests match |
| `test_supersede_marks_old_pack_and_allows_new_seal` | SEALED → SUPERSEDED; new draft → new distinct candidate |
| `test_list_packs_returns_current_sealed_packs` | list_packs() returns all current sealed packs |
| `test_idempotent_seal_replay_returns_same_pack` | same idempotency_key returns same pack (repository idempotency) |
| `test_constituents_are_bound_and_retrievable_from_sealed_pack` | all four constituent types (prompt, model_manifest, media_ref, parameters) survive round-trip |

### Class `TestNegative` — fail-closed boundary

| Test name | Property proved |
|---|---|
| `test_stale_digest_is_rejected_at_admission` | stale pack_digest → DIGEST_MISMATCH rejection |
| `test_forged_pack_id_that_does_not_exist_is_rejected` | non-existent pack_id → PACK_NOT_FOUND rejection |
| `test_mutable_rehydration_after_sealing_is_detected` | **FALSE-PROOF CASE** — tampered constituent after sealing → MUTABLE_REHYDRATION_DETECTED rejection |
| `test_constituent_digest_mismatch_is_rejected` | changed constituent digest → CONSTITUENT_DIGEST_MISMATCH rejection |
| `test_missing_required_constituent_is_rejected` | phantom constituent in expected_constituents → MISSING_REQUIRED_CONSTITUENT rejection |
| `test_invalidated_pack_is_rejected_at_admission` | INVALIDATED pack → PACK_NOT_SEALED / PACK_INVALIDATED rejection |
| `test_no_admission_without_prior_seal` | fabricated pack_id (UI-only bypass attempt) → PACK_NOT_FOUND rejection |
| `test_latest_state_substitution_is_blocked` | new digest from mutated preparation state passed against old pack_id → DIGEST_MISMATCH rejection |
| `test_empty_constituent_list_is_rejected` | zero constituents → PipelineValidationError |
| `test_duplicate_constituent_object_ids_are_rejected` | duplicate object_id → PipelineValidationError |
| `test_invalid_preparation_digest_format_is_rejected` | malformed preparation_digest → PipelineValidationError |
| `test_later_draft_does_not_mutate_original_sealed_pack` | second draft produces new pack_id; original digest unchanged |
| `test_superseded_pack_is_rejected_at_admission` | SUPERSEDED pack → PACK_NOT_SEALED / PACK_SUPERSEDED rejection |
| `test_constituent_with_invalid_digest_format_is_rejected` | non-SHA-256 content_digest → PipelineValidationError |

### Class `TestAntiCentroid` — false-proof / anti-centroid

| Test name | Property proved |
|---|---|
| `test_correct_pack_id_with_wrong_digest_does_not_leak_pack_data` | valid pack_id + wrong digest → DIGEST_MISMATCH; no payload leakage |
| `test_two_different_drafts_never_collide_on_digest` | structurally distinct drafts always yield distinct digests |
| `test_run_binding_not_persisted_on_rejected_admission` | rejected admission leaves NO run binding in repository |
| `test_digest_is_over_actual_bytes_not_metadata_field` | digest captures content, not just metadata field presence |

---

## 5. Architectural Notes

### State Machine

```
PreprodPackDraft (caller-owned, mutable)
    │
    ▼  compile_and_seal()
PreprodPackState.SEALED  (persisted, immutable digest)
    │
    ├──▶  admit_for_execution()  ──▶  ADMITTED  (run binding persisted)
    │                              or REJECTED   (fail-closed; no binding)
    │
    ├──▶  supersede_pack()       ──▶  PreprodPackState.SUPERSEDED
    │                                  (historical digest inspectable)
    │
    └──▶  invalidate_pack()      ──▶  PreprodPackState.INVALIDATED
                                       (historical digest inspectable)
```

### Determinism guarantee

`_pack_identity_payload()` sorts constituents by `(constituent_type, object_id)` before building the canonical payload.  `ca_contracts.canonical_json_bytes()` further enforces `sort_keys=True`.  The resulting SHA-256 is therefore stable across Python dict insertion-order differences, runtime instances, and platform byte-order.

### False-proof (anti-rehydration) gate

During `admit_for_execution()`, after the stored `pack_digest` is compared against the caller-supplied value, the service _recomputes_ the expected digest from the stored constituents.  If any constituent in the database has been mutated (tampered), the recomputed digest will not match the stored `pack_digest`, and admission fails with `MUTABLE_REHYDRATION_DETECTED`.  This directly implements the mandate's Section 9 false-proof requirement.

### Prohibitions respected

- ✅ A UI button alone cannot seal the pack (sealing only via `PreProductionSealer.compile_and_seal()`).
- ✅ A sealed snapshot is never mutated in place (supersede/invalidate create new revisions).
- ✅ Serialisation is deterministic (canonical_json_bytes + sort_keys).
- ✅ Execution is never silently upgraded to a new snapshot (digest must match exactly).
- ✅ Q12–Q16 evidence logic is not implemented.

---

## 6. Operator Gate

**Operator decision required per CA-M011 Section 12:**

> Approve CA-M011 and authorize the evidence chain beginning with CA-M012;
> record any legacy compatibility decision that affects snapshot admissibility.

Until this decision is recorded in CAE control state, CA-M012 remains unauthorized.

---

*Handoff prepared by execution agent for CA-M011.  Commit SHA to be captured by operator at gate.*
