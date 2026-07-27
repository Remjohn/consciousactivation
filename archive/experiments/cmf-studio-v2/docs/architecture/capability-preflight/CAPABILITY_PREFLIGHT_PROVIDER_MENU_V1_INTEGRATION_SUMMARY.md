# Capability Preflight + Provider Menu V1 Integration Summary

## Branch

`feat/capability-preflight-provider-menu-v1`

## Bundle Applied

`CCP_CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_INTEGRATION_BUNDLE.zip`

## Files Added

- `APPLY_CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_PATCH.md`
- `CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_BUNDLE_MANIFEST.json`
- `CAPABILITY_PREFLIGHT_PROVIDER_MENU_V1_LOCAL_VERIFICATION.json`
- `docs/architecture/capability-preflight/README.md`
- `docs/architecture/capability-preflight/PROVIDER_MENU.md`
- `docs/architecture/capability-preflight/RUNTIME_AVAILABILITY.md`
- `docs/architecture/capability-preflight/TOOL_SUPPORT.md`
- `docs/architecture/capability-preflight/COST_AND_SAMPLE_POLICY.md`
- `docs/architecture/capability-preflight/SERVICE_PLAN.md`
- `docs/architecture/capability-preflight/TEST_PLAN.md`
- `docs/architecture/capability-preflight/CAPABILITY_PREFLIGHT_EXISTING_SYSTEM_AUDIT.md`
- `docs/architecture/capability-preflight/CAPABILITY_PREFLIGHT_INTEGRATION_MAPPING.md`
- `src/ccp_studio/contracts/capability_preflight.py`
- `src/ccp_studio/repositories/capability_preflight.py`
- `src/ccp_studio/services/capability_preflight_service.py`
- `src/ccp_studio/services/provider_menu_service.py`
- `src/ccp_studio/services/runtime_availability_service.py`
- `src/ccp_studio/services/tool_support_registry_service.py`
- `registries/canonical/capability_preflight/`
- `registries/canonical/skills/shared/capability_preflight/`
- `tests/cmf_studio/test_capability_preflight_provider_menu_v1.py`
- `tests/cmf_studio/test_capability_preflight_golden_path_integration_v1.py`
- `tests/cmf_studio/test_capability_preflight_video_render_integration_v1.py`
- `tests/cmf_studio/test_capability_preflight_provider_batch_integration_v1.py`

## Files Modified

- `src/ccp_studio/services/tool_support_registry_service.py`

The generated bundle listed optional Hyperframes/ffprobe support as degrading `VIDEO_REAL_RENDER`. The integration narrows `VIDEO_REAL_RENDER` to the prompt-required hard gates: Remotion, FFmpeg, and local render worker. Future optional runtime display can be added without degrading the real-render preflight when required capabilities are available.

## Existing Provider / Runtime Systems Inspected

- Provider adapter layer under `src/ccp_studio/providers/`
- Provider adapter contracts and registries under `src/ccp_studio/contracts/provider_adapters.py` and `registries/canonical/providers/`
- Provider job workflow and receipts under `src/ccp_studio/contracts/provider_jobs.py`, `src/ccp_studio/workflows/provider_job_workflow.py`
- Style Route provider blueprint compilation under `src/ccp_studio/services/style_route_engine_service.py`
- Video Editing Engine render contracts under `src/ccp_studio/contracts/video_editing_engine.py` and `src/ccp_studio/services/video_render_contract_service.py`
- Golden Path Orchestrator under `src/ccp_studio/services/format02_golden_path_orchestrator_service.py`
- Approval, cost, and tool registry specs under `docs/tech-specs/` and `docs/architecture/cmf_studio_build_workflow/build_receipts/`

## Naming Conflicts

No direct `capability_preflight` namespace existed. The new namespace is additive and does not replace provider adapters, provider jobs, render contracts, runtime locks, or cost/approval policy contracts.

## Merge Notes

No existing implementation files required merge. Bundle package `__init__.py` files were not copied.

## Tests Run

Baseline before changes:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio
```

Result: `730 passed, 10 skipped`

Targeted and optional integration tests:

```powershell
$env:PYTHONPATH="src"
python -m compileall -q src
python -m pytest -q tests/cmf_studio/test_capability_preflight_provider_menu_v1.py tests/cmf_studio/test_capability_preflight_golden_path_integration_v1.py tests/cmf_studio/test_capability_preflight_video_render_integration_v1.py tests/cmf_studio/test_capability_preflight_provider_batch_integration_v1.py
```

Result: `22 passed`

Full suite:

```powershell
$env:PYTHONPATH="src"
python -m pytest -q tests/cmf_studio
```

Result: `752 passed, 10 skipped`

## Optional Integration Tests

Added:

- Golden Path fake runtime preflight allows pass/degraded and does not execute providers/runtimes.
- Video real render preflight blocks missing Remotion, FFmpeg, and local worker.
- Video real render preflight passes when required runtimes are configured and available.
- Format 02 provider scene batch blocks missing Ideogram/Flux.
- Format 02 provider scene batch blocks batch execution before sample approval.
- Format 02 provider scene batch passes after sample approval.

## Safety Confirmations

- No provider calls were added.
- No runtime calls were added.
- No Remotion calls were added.
- No FFmpeg calls were added.
- No local worker execution was added.
- No secrets are read, printed, inferred, or validated.
- Missing required capabilities block the pipeline.
- Sample-first batch blocking works when `sample_required=True` and `sample_approved=False`.

## Known Limitations

- Config/status driven only.
- No real provider probing.
- No secret validation.
- No shelling out to Remotion or FFmpeg.
- No UI/API endpoints.
- No cost reconciliation or billing ledger.
- No local render worker registration.
- No persistent preflight report store beyond the in-memory repository.

## Next Recommended Step

Project Workspace + Artifact Store V1, so preflight reports, setup offers, and generated artifacts can be persisted and surfaced safely before Template Preview / Atlas V1.
