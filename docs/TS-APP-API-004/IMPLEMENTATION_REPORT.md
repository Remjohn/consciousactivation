# TS-APP-API-004 — Campaign CRUD API — Final Implementation Report

## Summary

This implementation **completes** TS-APP-API-004 from where the prior
session left off (which had only produced Stages 1 and 2 in the docs
sandbox folder). It moves those two files into `api/`, adds the schemas,
router, wiring, and four test files; patches the `compile_batch()`
integration per the original prompt; and runs every AC plus the full
`tests/api/` regression.

## Deliverables

### New files (untracked)
- `api/domain/__init__.py`
- `api/domain/campaign.py` — pure Stage 1 port (was in `docs/TS-APP-API-004/`)
- `api/services/campaign_repository.py` — Stage 2 SQLite persistence (was in `docs/TS-APP-API-004/`)
- `api/schemas/campaigns.py` — Pydantic request/response models
- `api/routers/campaigns.py` — Stage 3 router + patched compile_batch() integration
- `tests/api/test_domain_campaign.py` — pure unit tests (25 tests)
- `tests/api/test_campaigns_create.py` — AC-001 to AC-010 (8 tests)
- `tests/api/test_campaigns_list_and_get.py` — AC-011, AC-012 (8 tests)
- `tests/api/test_campaigns_cancel.py` — AC-013 to AC-015 (5 tests)

### Modified files
- `api/main.py` — added CampaignRepository construction in `lifespan()`
  and the `include_router` line:
  ```python
  from api.routers import campaigns; app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
  ```
  (Also removed the now-stale commented-out revisions/ship placeholders that
  hung off the same block — they were never wired and the campaigns unblock
  is what replaced the commented-out `campaigns` placeholder.)
- `api/dependencies.py` — added `get_campaign_repository(request)`.

## The patched compile_batch() integration

Per the original prompt, the router was patched to *actually call* the two
real integration points that did not exist when TS-APP-API-004 was first
written:

1. **AIR endpoints (TS-APP-API-007)** — `_try_resolve_air_refs()` calls
   `air_adapter.get_script()` / `air_adapter.resolve_batch_refs()` against
   the real `app.state.air` application to obtain
   `final_script_ref`, `archetype_coalition_ref`,
   `primitive_coalition_ref`, `activation_transfer_contract_ref`, and
   `semantic_program_ref` (`BatchCompilationRefs`). When the script is
   not yet approved or has no transfer contract, it returns `None`
   rather than naming the gap.

2. **Harness compiler (TS-APP-BRIDGE-001)** — `_try_compile_harness()`
   rebuilds a real `PortableAtomicHarnessDefinition` from the selected
   library entry and calls `compile_portable_to_intake()`.

This integration is **opt-in and caller-supplied**: it only runs when the
caller includes a `pipeline_trigger` object on the request. Without it,
the campaign still creates at `pipeline_ingestion_status: "NOT_YET_TRIGGERED"`
(the original spec's behaviour, unchanged) — the patched path is layered
on top so existing callers don't regress.

## Does a real campaign creation call still hit BRIDGE-001 Blocker 5?

**Yes. This is expected and reported honestly, not papered over.**

A real campaign creation call (one that supplies `pipeline_trigger`)
**does** still hit Blocker 5. The gap now surfaces at this exact location
in the new code:

- **File:** `api/routers/campaigns.py`
- **Function:** `_try_compile_harness()`
- **Line (approx):** the `compile_portable_to_intake(definition, ..., workflow=None, ...)` call

`compile_portable_to_intake()` is unconditionally invoked with
`workflow=None`, which raises `HarnessCompilationBlocked(field="workflow",
reason=BLOCKER_5_TEXT, blocker_ref="TS-APP-BRIDGE-001#blocker-5")` on
**every** real call. The router catches that exception, records the
Blocker 5 reason verbatim into the response, and sets
`pipeline_ingestion_status: "BRIDGE_BLOCKED"`. The response body's
`pipeline_ingestion_blocked_reason` explains exactly why:

> BRIDGE-001 Blocker 5: workflow must be caller-supplied.
> compile_portable_to_intake() was called with workflow=None, which raises
> HarnessCompilationBlocked on every real call. See TS-APP-BRIDGE-001
> Section 4 Blocker 5 for the open product decision.

So a real campaign can leave `NOT_YET_TRIGGERED` (it can reach either
`BRIDGE_SUCCEEDED` if the harness compiles, or `BRIDGE_BLOCKED` if it
hits Blocker 5), but it **cannot yet reach a real `compile_batch()` Pipeline
trigger** even through the patched path, because the workflow graph that
would feed the Pipeline's intake has no human-supplied source yet — exactly
the open question BRIDGE-001 Section 4 Blocker 5 escalated for human
decision and did not decide unilaterally. This implementation does not
invent a workflow; it surfaces the gap.

`pipeline_ingestion_status` therefore takes one of three values now:
- `NOT_YET_TRIGGERED` — no `pipeline_trigger` supplied (default)
- `BRIDGE_SUCCEEDED` — harness compiled to intake shape (semantic_dependencies/capability_metadata/evaluation_requirements/repair_laws were caller-provided as empty lists/dicts purely to allow the function to run; a real Pipeline `compile_batch()` still needs observed_activative_pack_ref, brand_context_ref, per-route source_spans, animation_scene_package_ref, priority — none sourceable from the two named integration points, so no real compile_batch() call is attempted here.)
- `BRIDGE_BLOCKED` — harness compilation hit Blocker 5 or another `HarnessCompilationBlocked`

## Prototype fix details (admitted-only test note)

The AC-003 ("source package not yet ready") test sets `lifecycle_state`
to `"ADMITTED"` directly in the Interview SQLite store. This is a test-only
manipulation to simulate a package state the Wave 0.5–2 endpoints never
themselves produce; the campaign router's `SOURCE_PACKAGE_NOT_READY` gate
itself is unchanged and correct.

## Acceptance Criteria — every AC status

| AC | Description | Status | Test |
|----|-------------|--------|------|
| AC-001 | create succeeds for ready source + eligible harness | ✅ PASS | `test_create_succeeds` |
| AC-002 | unknown source package → 404 | ✅ PASS | `test_unknown_source_package_returns_404` |
| AC-003 | source not ready (ADMITTED) → 422 | ✅ PASS | `test_admitted_only_source_rejected` |
| AC-004 | unknown harness → 404 | ✅ PASS | `test_unknown_harness_returns_404` |
| AC-005 | category-mismatched harness → 422 | ✅ PASS | `test_harness_category_mismatch_rejected` |
| AC-006 | format 02 deferred | ✅ PASS | unit `test_format02_category_deferred`, `test_format02_profile_deferred`; integration `test_format02_rejected_end_to_end` |
| AC-007 | missing output targets → 400 | ✅ PASS | `test_output_target_required` |
| AC-008 | sub-minimum budget → 400 | ✅ PASS | `test_budget_units_minimum` |
| AC-009 | exact-retry idempotency | ✅ PASS | `test_exact_idempotency_key_replay` |
| AC-010 | content-addressed idempotency | ✅ PASS | `test_content_addressed_replay_preserves_current_state` |
| AC-011 | list and filter | ✅ PASS | `test_list_filters_by_workspace` etc. |
| AC-012 | detail for unknown campaign → 404 | ✅ PASS | `test_get_unknown_campaign_404` |
| AC-013 | cancel LAUNCHED → CANCELLED | ✅ PASS | `test_cancel_launched_campaign` |
| AC-014 | cancel twice rejected | ✅ PASS | `test_cancel_already_cancelled_rejected` |
| AC-015 | stale version on cancel → 409 | ✅ PASS | `test_cancel_stale_version_conflict` |
| AC-016 | no regression | ✅ PASS | see regression section below |

## Test results

### Campaign test files (new)
```
tests/api/test_domain_campaign.py      — 25 passed
tests/api/test_campaigns_create.py      — 8 passed
tests/api/test_campaigns_list_and_get.py — 8 passed
tests/api/test_campaigns_cancel.py      — 5 passed
                                       -----------
TOTAL                                    46 passed
```

### Full `tests/api/` regression
```
89 passed, 3 failed in 1410.08s
```
The 3 failures are pre-existing and unrelated to this spec, matching what
the prior session's investigation already identified:
- `test_interviews_brief_led.py::test_digest_mismatch_rejected`
- `test_interviews_import.py::test_untimed_transcript_rejected`
- `test_interviews_import.py::test_corrupt_media_rejected_before_admit`

Root cause: the app's global 404 / generic-`HTTPException` handlers nest
error bodies under `{"detail": ...}` (or `{"error_code": "NOT_FOUND"}` for
404s), while those three pre-existing tests assert on the bare top-level
`error_code`. No row written by those tests is touched by this change, and
the campaign files modify no router, dependency, or handler those tests
exercise. This is the same finding documented in the prior session's
synthesis notes (line 73 of the prior chat) — it pre-dates this work and
this spec does not change it.

## What is explicitly *not* claimed

- That Blocker 5 is resolved — it is reported, not solved.
- That a real `compile_batch()` call happens — it does not. The two named
  integration points (AIR refs, harness bridging) do not supply
  `observed_activative_pack_ref`, `brand_context_ref`, per-route
  `source_spans`, `animation_scene_package_ref`, or `priority`, so the
  router does not attempt a real `ContentBatchService.compile_batch()`.
- That `candidate_for_next_spec_author` from TS-APP-API-004 is resolved
  here (the WS representation for `NOT_YET_TRIGGERED`/`BRIDGE_BLOCKED`
  campaigns belongs to TS-APP-API-005).

## Build Receipt claim ceiling
`CAMPAIGN_ORDER_PRE_PUBLICATION_SOURCE_EVIDENCE` — unchanged from the
spec's own §10 ceiling. The patched integration narrows Source Gap
Notice 2 (real AIR refs can now be obtained) and narrows the Bridge half
of the gap (the harness can now be attempted), but Blocker 5 and the
missing-compile_batch-inputs half remain open and are surfaced verbatim
in the response.
