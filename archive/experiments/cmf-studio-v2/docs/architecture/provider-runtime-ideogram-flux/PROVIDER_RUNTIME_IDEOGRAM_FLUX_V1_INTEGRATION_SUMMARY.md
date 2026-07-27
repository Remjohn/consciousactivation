# Provider Runtime Ideogram + Flux V1 Integration Summary

## Branch

`feat/provider-runtime-ideogram-flux-v1`

## Bundle applied

`CCP_PROVIDER_RUNTIME_IDEOGRAM_FLUX_V1_INTEGRATION_BUNDLE.zip`

## Files added

- `APPLY_PROVIDER_RUNTIME_IDEOGRAM_FLUX_V1_PATCH.md`
- `PROVIDER_RUNTIME_IDEOGRAM_FLUX_V1_BUNDLE_MANIFEST.json`
- `PROVIDER_RUNTIME_IDEOGRAM_FLUX_V1_LOCAL_VERIFICATION.json`
- `docs/architecture/provider-runtime-ideogram-flux/README.md`
- `docs/architecture/provider-runtime-ideogram-flux/PROVIDER_ROLES.md`
- `docs/architecture/provider-runtime-ideogram-flux/SAMPLE_FIRST_POLICY.md`
- `docs/architecture/provider-runtime-ideogram-flux/DECISION_LOG.md`
- `docs/architecture/provider-runtime-ideogram-flux/COST_AND_RETRY.md`
- `docs/architecture/provider-runtime-ideogram-flux/OUTPUT_ASSET_REFS.md`
- `docs/architecture/provider-runtime-ideogram-flux/INTEGRATION_POINTS.md`
- `docs/architecture/provider-runtime-ideogram-flux/TEST_PLAN.md`
- `docs/architecture/provider-runtime-ideogram-flux/PROVIDER_RUNTIME_EXISTING_SYSTEM_AUDIT.md`
- `docs/architecture/provider-runtime-ideogram-flux/PROVIDER_RUNTIME_INTEGRATION_MAPPING.md`
- `docs/architecture/provider-runtime-ideogram-flux/PROVIDER_RUNTIME_IDEOGRAM_FLUX_V1_INTEGRATION_SUMMARY.md`
- `fixtures/provider_runtime/ideogram_scene_sample_job.json`
- `fixtures/provider_runtime/flux_reference_edit_sample_job.json`
- `src/ccp_studio/contracts/provider_runtime.py`
- `src/ccp_studio/repositories/provider_runtime.py`
- `src/ccp_studio/services/provider_capability_profile_service.py`
- `src/ccp_studio/services/provider_cost_estimate_service.py`
- `src/ccp_studio/services/provider_retry_policy_service.py`
- `src/ccp_studio/services/provider_sample_approval_service.py`
- `src/ccp_studio/services/provider_decision_log_service.py`
- `src/ccp_studio/services/provider_job_service.py`
- `src/ccp_studio/services/provider_output_asset_service.py`
- `src/ccp_studio/services/ideogram_provider_runtime_service.py`
- `src/ccp_studio/services/flux_provider_runtime_service.py`
- `src/ccp_studio/services/provider_runtime_service.py`
- `registries/canonical/provider_runtime/`
- `registries/canonical/skills/shared/provider_runtime/`
- `tests/cmf_studio/test_provider_runtime_ideogram_flux_v1.py`
- `tests/cmf_studio/test_provider_runtime_capability_preflight_integration_v1.py`
- `tests/cmf_studio/test_provider_runtime_workspace_integration_v1.py`
- `tests/cmf_studio/test_provider_runtime_template_preview_integration_v1.py`
- `tests/cmf_studio/test_provider_runtime_avatar_sample_integration_v1.py`

## Files modified

No existing provider adapter, provider job, provider recovery, composition, capability preflight, workspace, template, or avatar files were modified.

## Existing provider systems inspected

- Existing provider operations contracts and API: `provider_jobs.py`, `api/v1/provider_jobs.py`
- Existing provider recovery flow: `provider_recovery.py`, `api/v1/provider_recovery.py`
- Existing provider adapter contracts: `provider_adapters.py`
- Existing generative adapter contracts/services
- Existing Ideogram composition lineage
- Existing composition provider boundaries for Ideogram and Flux
- Existing capability preflight provider menu and sample-first blocking
- Existing operator-web SuperVisual provider job panels

## Existing Ideogram/Flux/BFL references found

- Ideogram composition lineage and `Ideogram4Adapter`
- Composition Intelligence provider contracts requiring Ideogram and Flux roles
- `ProviderId.BFL_FLUX` and `Flux2Klein9BParameters`
- UX docs and registries describing Ideogram 4 composition JSON and Flux edit roles

## Naming conflicts

The repo already has provider classes with overlapping names in `provider_jobs.py` and `provider_adapters.py`. The bundle adds a separate `provider_runtime.py` module, so no existing provider class was replaced.

## Merge decisions

No target files required merge. Existing provider systems are preserved. This V1 layer is additive and fake-runtime only.

## Tests run

- Baseline before changes:
  - `PYTHONPATH=src python -m compileall -q src`
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
  - Result: `881 passed, 12 skipped`
- Bundle targeted test:
  - `PYTHONPATH=src python -m compileall -q src`
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_provider_runtime_ideogram_flux_v1.py`
  - Result: `18 passed`
- Provider runtime plus optional integration tests:
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio/test_provider_runtime_ideogram_flux_v1.py tests/cmf_studio/test_provider_runtime_capability_preflight_integration_v1.py tests/cmf_studio/test_provider_runtime_workspace_integration_v1.py tests/cmf_studio/test_provider_runtime_template_preview_integration_v1.py tests/cmf_studio/test_provider_runtime_avatar_sample_integration_v1.py`
  - Result: `23 passed`
- Full CMF suite:
  - `PYTHONPATH=src python -m pytest -q tests/cmf_studio`
  - Result: `904 passed, 12 skipped`

## Optional integration tests

Added:

- Capability preflight integration
- Project Workspace / Artifact Store integration
- Template preview sample-first integration
- Avatar face plate sample integration

## Confirmations

- No Ideogram calls were added.
- No Flux calls were added.
- No provider API calls were added.
- No secrets are read or inferred.
- Sample-first batch gate requires scene, face plate, and template preview samples.
- `ProviderDecisionLog` is required by provider jobs.
- `ProviderCostEstimate` is required by decision logs.
- `ProviderJobReceipt` cannot pass with blockers.
- `ProviderOutputAssetRef` requires provider job receipt and `sha256`.
- Retry policy prevents unlimited retries.
- V1 provider outputs cannot claim real provider execution.

## Known limitations

- Fake provider execution only.
- No real provider clients.
- No API endpoints.
- No UI.
- No secret validation.
- No network calls.
- No binary/file upload.
- No image generation.
- No billing reconciliation.

## Next recommended step

Operator Provider Job Sample Approval UI, or Real Ideogram/Flux Adapter V1.1 after provider secrets and sample approval UX are ready.
